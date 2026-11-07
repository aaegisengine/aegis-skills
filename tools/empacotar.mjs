#!/usr/bin/env node
// Empacota as 12 AEGIS SKILLS do jeito que o comprador consegue abrir.
//
//   node tools/empacotar.mjs            valida + gera tudo em _dist/v2/
//   node tools/empacotar.mjs --checar   só valida (não escreve nada)
//
// Nasceu em 07/11/2026 depois de 3 reembolsos ("arquivos não abrem"): os ZIPs
// antigos saíram do Compress-Archive do PowerShell 5.1 com "pasta\SKILL.md"
// (barra invertida), que o iPhone, o Mac e o upload do claude.ai não entendem,
// e a pasta de dentro tinha nome diferente do `name` da skill.
//
// Saída:
//   _dist/v2/skills/<name>.zip        um por skill, pronto pro claude.ai (Settings > Capabilities > Skills)
//   _dist/v2/prompts/<name>.txt       versão "cole em qualquer IA" (Claude grátis, ChatGPT, Gemini)
//   _dist/v2/hotmart-7/ e hotmart-5/  o que sobe em cada produto da Hotmart (zips + .docx)
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { criarZip, lerZip } from './zip.mjs';
import { run, par, montarDocx } from './docx.mjs';

const RAIZ = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SAIDA = path.join(RAIZ, '_dist', 'v2');
const SO_CHECAR = process.argv.includes('--checar');

export const PACOTES = {
  'hotmart-7': {
    titulo: 'AEGIS SKILLS · 7 skills de leitura de gráfico',
    skills: ['leitura', 'zonas', 'figuras', 'ondas', 'renko', 'autopsia', 'backtest'],
    extras: ['_dist/AEGIS-SKILLS-42-Prompts.pdf'],
  },
  'hotmart-5': {
    titulo: 'AEGIS SKILLS · 5 skills de plano e validação',
    skills: ['day-trade-plan', 'session-news-radar', 'swing-trade-plan', 'crypto-trade-plan', 'setup-backtest'],
    extras: ['_pdf-trader/AEGIS-SKILLS-Trader-30-Prompts.pdf'],
  },
};

export const TITULOS = {
  'leitura-de-grafico': 'Leitura de Gráfico',
  'zonas-suporte-resistencia': 'Zonas de Suporte e Resistência',
  'figuras-candle': 'Figuras de Candle',
  'ondas-elliott': 'Ondas de Elliott',
  'leitura-renko': 'Leitura Renko',
  'autopsia-de-trade': 'Autópsia de Trade',
  'backtest-honesto': 'Backtest Honesto',
  'day-trade-plan': 'Day Trade Plan',
  'session-news-radar': 'Session News Radar',
  'swing-trade-plan': 'Swing Trade Plan',
  'crypto-trade-plan': 'Crypto Trade Plan',
  'setup-backtest': 'Setup Backtest',
};

const IGNORAR = new Set(['.DS_Store', 'Thumbs.db', '__pycache__', 'node_modules', 'evals']);
const TETO_PROMPT = 28000; // acima disso o ChatGPT recusa a mensagem colada
const LIMITE_PARTE = 26000; // passou disso, a versão de colar sai em 2 partes

function listar(dir, base = dir) {
  const out = [];
  for (const nome of fs.readdirSync(dir).sort()) {
    if (IGNORAR.has(nome) || nome.endsWith('.pyc')) continue;
    const abs = path.join(dir, nome);
    if (fs.statSync(abs).isDirectory()) out.push(...listar(abs, base));
    else out.push(path.relative(base, abs).split(path.sep).join('/'));
  }
  return out;
}

function frontmatter(texto, arquivo) {
  const t = texto.replace(/^﻿/, '').replace(/\r\n/g, '\n');
  const m = t.match(/^---\n([\s\S]*?)\n---\n?/);
  if (!m) throw new Error(`${arquivo}: sem frontmatter YAML no topo`);
  const campos = {};
  for (const linha of m[1].split('\n')) {
    if (!linha.trim()) continue;
    const mm = linha.match(/^([a-z][a-z-]*):\s?(.*)$/);
    if (!mm) throw new Error(`${arquivo}: linha de frontmatter que este validador não entende: "${linha.slice(0, 60)}" (use name/description numa linha só)`);
    let v = mm[2].trim();
    if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) v = v.slice(1, -1);
    campos[mm[1]] = v;
  }
  return { campos, corpo: t.slice(m[0].length) };
}

function validar(pasta) {
  const erros = [];
  const avisos = [];
  const dir = path.join(RAIZ, pasta);
  const skillMd = path.join(dir, 'SKILL.md');
  if (!fs.existsSync(skillMd)) return { erros: [`${pasta}: SKILL.md não existe`], avisos };
  const arquivos = listar(dir);
  const skillMds = arquivos.filter((a) => a.split('/').pop() === 'SKILL.md');
  if (skillMds.length !== 1) erros.push(`${pasta}: tem ${skillMds.length} SKILL.md (claude.ai aceita exatamente 1)`);

  let fm;
  try {
    fm = frontmatter(fs.readFileSync(skillMd, 'utf8'), `${pasta}/SKILL.md`);
  } catch (e) {
    return { erros: [...erros, e.message], avisos };
  }
  const { campos, corpo } = fm;
  const extras = Object.keys(campos).filter((k) => !['name', 'description', 'license', 'allowed-tools', 'metadata', 'compatibility'].includes(k));
  if (extras.length) erros.push(`${pasta}: campo não permitido no frontmatter: ${extras.join(', ')}`);
  const nome = campos.name || '';
  if (!nome) erros.push(`${pasta}: falta name`);
  else {
    if (!/^[a-z0-9]+(-[a-z0-9]+)*$/.test(nome)) erros.push(`${pasta}: name "${nome}" fora do padrão (minúsculas, números e hífen)`);
    if (nome.length > 64) erros.push(`${pasta}: name com ${nome.length} caracteres (máx 64)`);
  }
  const desc = campos.description || '';
  if (!desc) erros.push(`${pasta}: falta description`);
  if (desc.length > 1024) erros.push(`${pasta}: description com ${desc.length} caracteres (máx 1024)`);
  else if (desc.length > 900) avisos.push(`${pasta}: description com ${desc.length} caracteres (alvo ≤900)`);
  if (/[<>]/.test(desc)) erros.push(`${pasta}: description com < ou > (o upload recusa)`);

  // Regra de Ouro da casa: zero travessão em tudo que o comprador lê.
  for (const rel of arquivos.filter((a) => /\.(md|txt|csv)$/i.test(a))) {
    const linhas = fs.readFileSync(path.join(dir, rel), 'utf8').split('\n');
    linhas.forEach((l, i) => {
      if (/[—–]/.test(l)) erros.push(`${pasta}/${rel}:${i + 1}: travessão: ${l.trim().slice(0, 70)}`);
    });
  }
  if (corpo.split('\n').length > 500) avisos.push(`${pasta}: SKILL.md com ${corpo.split('\n').length} linhas (recomendado <500)`);
  return { erros, avisos, nome, desc, corpo, arquivos, dir };
}

function zipDaSkill(v) {
  // Pasta leva a data do SKILL.md: o mesmo conteúdo gera o mesmo ZIP, byte a byte.
  const quando = fs.statSync(path.join(v.dir, 'SKILL.md')).mtime;
  const entradas = [{ name: `${v.nome}/`, dir: true, mtime: quando }];
  const pastas = new Set();
  for (const rel of v.arquivos) {
    const partes = rel.split('/');
    for (let i = 1; i < partes.length; i++) {
      const p = `${v.nome}/${partes.slice(0, i).join('/')}/`;
      if (!pastas.has(p)) { pastas.add(p); entradas.push({ name: p, dir: true, mtime: quando }); }
    }
    const abs = path.join(v.dir, ...partes);
    entradas.push({ name: `${v.nome}/${rel}`, data: fs.readFileSync(abs), mtime: fs.statSync(abs).mtime });
  }
  const buf = criarZip(entradas);
  // Confere lendo de volta: nada de barra invertida, SKILL.md no lugar, CRC ok.
  const lido = lerZip(buf);
  const nomes = lido.map((e) => e.nome);
  if (nomes.some((n) => n.includes('\\'))) throw new Error(`${v.nome}.zip: barra invertida no caminho`);
  if (!nomes.includes(`${v.nome}/SKILL.md`)) throw new Error(`${v.nome}.zip: falta ${v.nome}/SKILL.md`);
  if (nomes.filter((n) => n.endsWith('/SKILL.md')).length !== 1) throw new Error(`${v.nome}.zip: mais de um SKILL.md`);
  return buf;
}

/** Texto que o comprador cola em qualquer IA. Sem scripts: quem tem execução de código usa o ZIP. */
function promptDeCola(v) {
  const titulo = TITULOS[v.nome] || v.nome;
  const refs = v.arquivos.filter((a) => a.startsWith('references/') && a.endsWith('.md'));
  const temScript = v.arquivos.some((a) => a.startsWith('scripts/'));
  const avisoScript = temScript
    ? ['Se as instruções mandarem rodar um script (pasta scripts/) e você não tiver esse arquivo, faça a mesma conta',
       'passo a passo na conversa, mostrando a fórmula, para o usuário conferir.']
    : [];
  const blocosRef = refs.map((rel) => [
    '',
    `----- REFERÊNCIA: ${rel} -----`,
    fs.readFileSync(path.join(v.dir, ...rel.split('/')), 'utf8').replace(/\r\n/g, '\n').trim(),
  ].join('\n'));
  const cab = [`AEGIS SKILLS · ${titulo} · versão para colar em qualquer IA`, ''];
  const corpo = v.corpo.trim();
  const tamanhoUnico = corpo.length + blocosRef.join('\n').length + 1200;

  if (tamanhoUnico <= LIMITE_PARTE || !refs.length) {
    return [
      ...cab,
      'COMO USAR: copie tudo, da linha INÍCIO até a linha FIM, e cole como primeira mensagem de uma conversa nova',
      '(ou nas instruções de um Projeto do Claude). Depois envie o seu pedido.',
      '',
      '===== INÍCIO =====',
      'Siga as instruções abaixo durante toda esta conversa, como se fossem as suas regras de trabalho.',
      'Quando terminar de ler, responda apenas: "Pronto. Envie o print ou o pedido." e espere.',
      ...avisoScript,
      ...(refs.length ? ['As referências citadas (references/...) estão logo depois das instruções principais.'] : []),
      '',
      corpo,
      ...blocosRef,
      '===== FIM =====',
    ].join('\n') + '\n';
  }

  // Longa demais pra uma mensagem só (o ChatGPT recusa acima de ~28 mil caracteres): vai em 2 partes.
  return [
    ...cab,
    'COMO USAR: esta skill vai em DUAS partes, porque é longa. Copie a PARTE 1 (de INÍCIO até FIM) e cole numa conversa nova.',
    'Espere a IA responder "OK, mande a parte 2." Depois copie e cole a PARTE 2. Aí envie o seu pedido.',
    '',
    '===== INÍCIO PARTE 1 DE 2 =====',
    'Esta é a parte 1 de 2 das instruções que você vai seguir durante toda esta conversa, como se fossem as suas regras de trabalho.',
    'Leia e responda apenas: "OK, mande a parte 2." Não faça mais nada até receber a parte 2.',
    ...avisoScript,
    '',
    corpo,
    '===== FIM PARTE 1 DE 2 =====',
    '',
    '===== INÍCIO PARTE 2 DE 2 =====',
    'Esta é a parte 2 de 2: as referências (references/...) citadas nas instruções da parte 1. Elas valem durante toda a conversa.',
    'Quando terminar de ler, responda apenas: "Pronto. Envie o print ou o pedido." e espere.',
    ...blocosRef,
    '===== FIM PARTE 2 DE 2 =====',
  ].join('\n') + '\n';
}

/** Tamanho de cada bloco colável (de INÍCIO a FIM), pra conferir o teto. */
function blocosColaveis(txt) {
  return [...txt.matchAll(/===== INÍCIO[^\n]*=====\n([\s\S]*?)\n===== FIM[^\n]*=====/g)].map((m) => m[1].length);
}

// ---------- DOCX do pacote ----------
function docx(tituloPacote, itens) {
  const corpo = [];
  corpo.push(par(run(tituloPacote, { b: true, sz: 36 }), { depois: 200 }));
  corpo.push(par(run('Versão para colar em qualquer IA', { b: true, sz: 26, cor: '0000FE' }), { depois: 200 }));
  const intro = [
    'Este arquivo é para quem NÃO tem o Claude pago (Pro/Max) ou usa outra IA (ChatGPT, Gemini, Grok, Claude grátis).',
    'Quem tem o Claude pago instala os arquivos .zip (passo a passo no PDF COMECE AQUI) e não precisa deste arquivo.',
    '',
    'Como usar:',
    '1. Escolha a skill na lista abaixo. Cada uma começa numa página nova.',
    '2. Copie o texto inteiro da skill, da linha INÍCIO até a linha FIM.',
    '3. Abra uma conversa NOVA na sua IA e cole como primeira mensagem.',
    '4. Espere a resposta "Pronto. Envie o print ou o pedido."',
    '5. Envie o print do gráfico ou o seu pedido.',
    '',
    'Skill marcada com PARTE 1 e PARTE 2: cole a parte 1, espere "OK, mande a parte 2." e cole a parte 2.',
    '',
    'Dica: no Claude, crie um Projeto e cole o texto nas instruções uma vez só. No ChatGPT as instruções de GPT têm limite',
    'de tamanho, então cole no começo de cada conversa nova.',
    '',
    'Skills neste arquivo:',
    ...itens.map((it, i) => `${i + 1}. ${it.titulo}`),
  ];
  for (const l of intro) corpo.push(par(run(l, { sz: 22 })));
  itens.forEach((it) => {
    corpo.push(par(run(it.titulo, { b: true, sz: 32 }), { quebra: true, depois: 120 }));
    for (const l of it.texto.split('\n')) {
      const destaque = /^===== (INÍCIO|FIM)( PARTE \d DE \d)? =====$/.test(l);
      corpo.push(par(run(l, { sz: 19, b: destaque, cor: destaque ? '0000FE' : null }), { depois: 0 }));
    }
  });
  return montarDocx(corpo);
}

// ---------- principal ----------
const iSo = process.argv.indexOf('--so');
const SO = iSo > 0 ? process.argv[iSo + 1] : null;
if (SO && !PACOTES[SO]) throw new Error('pacote desconhecido: ' + SO);
const PACOTES_ATIVOS = SO ? { [SO]: PACOTES[SO] } : PACOTES;
const todas = [...new Set(Object.values(PACOTES_ATIVOS).flatMap((p) => p.skills))];
let falhou = false;
const validas = {};
for (const pasta of todas) {
  const v = validar(pasta);
  for (const a of v.avisos) console.log(`  aviso  ${a}`);
  if (v.erros.length) {
    falhou = true;
    for (const e of v.erros) console.log(`  ERRO   ${e}`);
  } else {
    validas[pasta] = v;
    console.log(`  ok     ${pasta} -> ${v.nome} (description ${v.desc.length}c, ${v.arquivos.length} arquivo(s))`);
  }
}
if (falhou) {
  console.log('\nReprovado: corrija os erros acima antes de empacotar.');
  process.exit(1);
}
if (SO_CHECAR) {
  console.log('\nTudo válido (modo --checar, nada foi escrito).');
  process.exit(0);
}

// Limpa só o que este script gera (a pasta prompt-master/ vem de outro gerador).
for (const d of SO ? [SO] : ['skills', 'prompts', ...Object.keys(PACOTES)]) fs.rmSync(path.join(SAIDA, d), { recursive: true, force: true });
for (const d of ['skills', 'prompts', ...Object.keys(PACOTES_ATIVOS)]) fs.mkdirSync(path.join(SAIDA, d), { recursive: true });

const manifesto = { gerado_em: new Date().toISOString(), skills: {}, pacotes: {} };
for (const [pasta, v] of Object.entries(validas)) {
  const zip = zipDaSkill(v);
  fs.writeFileSync(path.join(SAIDA, 'skills', `${v.nome}.zip`), zip);
  const txt = promptDeCola(v);
  const blocos = blocosColaveis(txt);
  if (!blocos.length) throw new Error(`${v.nome}: versão de colar sem bloco INÍCIO/FIM`);
  for (const n of blocos) if (n > TETO_PROMPT) throw new Error(`${v.nome}: bloco de colar com ${n} caracteres (teto ${TETO_PROMPT})`);
  if (blocos.length > 1) console.log(`  info   ${v.nome}: versão de colar em ${blocos.length} partes (${blocos.join(' + ')} caracteres)`);
  fs.writeFileSync(path.join(SAIDA, 'prompts', `${v.nome}.txt`), txt);
  manifesto.skills[v.nome] = { pasta, zip_bytes: zip.length, prompt_chars: txt.length };
}
for (const [id, pac] of Object.entries(PACOTES_ATIVOS)) {
  const itens = [];
  for (const pasta of pac.skills) {
    const v = validas[pasta];
    fs.copyFileSync(path.join(SAIDA, 'skills', `${v.nome}.zip`), path.join(SAIDA, id, `${v.nome}.zip`));
    itens.push({ titulo: TITULOS[v.nome] || v.nome, texto: fs.readFileSync(path.join(SAIDA, 'prompts', `${v.nome}.txt`), 'utf8') });
  }
  const n = pac.skills.length;
  const nomeDocx = `AEGIS SKILLS - ${n} skills - versao para colar em qualquer IA.docx`;
  const buf = docx(pac.titulo, itens);
  lerZip(buf); // confere
  fs.writeFileSync(path.join(SAIDA, id, nomeDocx), buf);
  for (const rel of pac.extras || []) {
    const abs = path.join(RAIZ, rel);
    if (!fs.existsSync(abs)) throw new Error(`${id}: falta o arquivo extra ${rel}`);
    fs.copyFileSync(abs, path.join(SAIDA, id, path.basename(rel)));
  }
  manifesto.pacotes[id] = fs.readdirSync(path.join(SAIDA, id));
}
fs.writeFileSync(path.join(SAIDA, 'manifesto.json'), JSON.stringify(manifesto, null, 2));
console.log(`\nGerado em ${path.relative(RAIZ, SAIDA)}:`);
for (const [id, arqs] of Object.entries(manifesto.pacotes)) console.log(`  ${id}: ${arqs.join(' · ')}`);
