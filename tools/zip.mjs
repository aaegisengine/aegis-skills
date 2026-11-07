// Escritor e leitor mínimo de ZIP (sem dependência), feito pra substituir o
// Compress-Archive do PowerShell 5.1, que grava caminho com barra invertida
// ("pasta\SKILL.md") e quebra o arquivo no iPhone, no Mac e no upload do claude.ai.
//
// Regras que este escritor garante:
//  - separador sempre "/" (APPNOTE 4.4.17)
//  - flag UTF-8 (bit 11) ligada, então acento no nome sai certo em qualquer sistema
//  - DEFLATE com CRC-32 real e data/hora DOS válidas
//  - entradas de pasta explícitas ("pasta/"), que alguns extratores do celular exigem
import { deflateRawSync, inflateRawSync, crc32 } from 'node:zlib';

function dosDateTime(d) {
  const time = (d.getHours() << 11) | (d.getMinutes() << 5) | Math.floor(d.getSeconds() / 2);
  const date = ((d.getFullYear() - 1980) << 9) | ((d.getMonth() + 1) << 5) | d.getDate();
  return { time, date };
}

/**
 * @param {{name:string, data?:Buffer, dir?:boolean, mtime?:Date}[]} entries
 * @returns {Buffer}
 */
export function criarZip(entries) {
  const locais = [];
  const central = [];
  let offset = 0;
  for (const e of entries) {
    let nome = e.name.replace(/\\/g, '/');
    if (e.dir && !nome.endsWith('/')) nome += '/';
    if (nome.startsWith('/') || nome.includes('..')) throw new Error(`caminho inseguro no zip: ${nome}`);
    const nomeBuf = Buffer.from(nome, 'utf8');
    const dados = e.dir ? Buffer.alloc(0) : e.data;
    const comprimido = e.dir ? Buffer.alloc(0) : deflateRawSync(dados, { level: 9 });
    const metodo = e.dir ? 0 : 8;
    const crc = e.dir ? 0 : crc32(dados) >>> 0;
    const { time, date } = dosDateTime(e.mtime || new Date());
    const flag = 0x0800; // UTF-8

    const lh = Buffer.alloc(30);
    lh.writeUInt32LE(0x04034b50, 0);
    lh.writeUInt16LE(20, 4);
    lh.writeUInt16LE(flag, 6);
    lh.writeUInt16LE(metodo, 8);
    lh.writeUInt16LE(time, 10);
    lh.writeUInt16LE(date, 12);
    lh.writeUInt32LE(crc, 14);
    lh.writeUInt32LE(comprimido.length, 18);
    lh.writeUInt32LE(dados.length, 22);
    lh.writeUInt16LE(nomeBuf.length, 26);
    lh.writeUInt16LE(0, 28);
    locais.push(lh, nomeBuf, comprimido);

    const ch = Buffer.alloc(46);
    ch.writeUInt32LE(0x02014b50, 0);
    ch.writeUInt16LE((3 << 8) | 20, 4); // feito em "Unix", versão 2.0: permissões legíveis
    ch.writeUInt16LE(20, 6);
    ch.writeUInt16LE(flag, 8);
    ch.writeUInt16LE(metodo, 10);
    ch.writeUInt16LE(time, 12);
    ch.writeUInt16LE(date, 14);
    ch.writeUInt32LE(crc, 16);
    ch.writeUInt32LE(comprimido.length, 20);
    ch.writeUInt32LE(dados.length, 24);
    ch.writeUInt16LE(nomeBuf.length, 28);
    ch.writeUInt16LE(0, 30);
    ch.writeUInt16LE(0, 32);
    ch.writeUInt16LE(0, 34);
    ch.writeUInt16LE(0, 36);
    const modo = e.dir ? 0o40755 : 0o100644;
    ch.writeUInt32LE(((modo << 16) | (e.dir ? 0x10 : 0)) >>> 0, 38);
    ch.writeUInt32LE(offset, 42);
    central.push(ch, nomeBuf);

    offset += lh.length + nomeBuf.length + comprimido.length;
  }
  const cdBuf = Buffer.concat(central);
  const fim = Buffer.alloc(22);
  fim.writeUInt32LE(0x06054b50, 0);
  fim.writeUInt16LE(0, 4);
  fim.writeUInt16LE(0, 6);
  fim.writeUInt16LE(entries.length, 8);
  fim.writeUInt16LE(entries.length, 10);
  fim.writeUInt32LE(cdBuf.length, 12);
  fim.writeUInt32LE(offset, 16);
  fim.writeUInt16LE(0, 20);
  return Buffer.concat([...locais, cdBuf, fim]);
}

/** Lê o diretório central e descomprime cada arquivo, conferindo o CRC. */
export function lerZip(buf) {
  const eocd = buf.lastIndexOf(Buffer.from([0x50, 0x4b, 0x05, 0x06]));
  if (eocd < 0) throw new Error('fim do diretório central não encontrado');
  const total = buf.readUInt16LE(eocd + 10);
  let p = buf.readUInt32LE(eocd + 16);
  const out = [];
  for (let i = 0; i < total; i++) {
    if (buf.readUInt32LE(p) !== 0x02014b50) throw new Error('diretório central corrompido');
    const flag = buf.readUInt16LE(p + 8);
    const metodo = buf.readUInt16LE(p + 10);
    const crc = buf.readUInt32LE(p + 16);
    const tamC = buf.readUInt32LE(p + 20);
    const tam = buf.readUInt32LE(p + 24);
    const nl = buf.readUInt16LE(p + 28);
    const xl = buf.readUInt16LE(p + 30);
    const cl = buf.readUInt16LE(p + 32);
    const off = buf.readUInt32LE(p + 42);
    const nome = buf.subarray(p + 46, p + 46 + nl).toString(flag & 0x0800 ? 'utf8' : 'latin1');
    const lnl = buf.readUInt16LE(off + 26);
    const lxl = buf.readUInt16LE(off + 28);
    const ini = off + 30 + lnl + lxl;
    const bruto = buf.subarray(ini, ini + tamC);
    const dados = metodo === 8 ? inflateRawSync(bruto) : Buffer.from(bruto);
    if (dados.length !== tam) throw new Error(`${nome}: tamanho não bate`);
    if (!nome.endsWith('/') && (crc32(dados) >>> 0) !== crc) throw new Error(`${nome}: CRC não bate`);
    out.push({ nome, dados, utf8: !!(flag & 0x0800) });
    p += 46 + nl + xl + cl;
  }
  return out;
}
