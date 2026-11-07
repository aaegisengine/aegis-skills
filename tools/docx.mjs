// DOCX mínimo, sem dependência. Abre no Word, Google Docs, Pages e na
// pré-visualização do iPhone e do Android. Cada linha vira um parágrafo, então
// copiar o texto não gruda palavra (o defeito do PDF antigo do Prompt Master).
import { criarZip, lerZip } from './zip.mjs';

const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

export function run(texto, { b = false, sz = 21, cor = null, mono = false } = {}) {
  const props = [
    mono ? '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:cs="Consolas"/>' : '',
    b ? '<w:b/>' : '',
    cor ? `<w:color w:val="${cor}"/>` : '',
    `<w:sz w:val="${sz}"/>`,
  ].join('');
  return `<w:r><w:rPr>${props}</w:rPr><w:t xml:space="preserve">${esc(texto)}</w:t></w:r>`;
}

export const par = (runs, { quebra = false, depois = 60 } = {}) =>
  `<w:p><w:pPr>${quebra ? '<w:pageBreakBefore/>' : ''}<w:spacing w:after="${depois}"/></w:pPr>${runs}</w:p>`;

/** @param {string[]} paragrafos XML de <w:p> já montados */
export function montarDocx(paragrafos) {
  const documento = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>${paragrafos.join('')}<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" w:header="0" w:footer="0" w:gutter="0"/></w:sectPr></w:body></w:document>`;
  const tipos = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>`;
  const rels = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>`;
  const buf = criarZip([
    { name: '[Content_Types].xml', data: Buffer.from(tipos) },
    { name: '_rels/', dir: true },
    { name: '_rels/.rels', data: Buffer.from(rels) },
    { name: 'word/', dir: true },
    { name: 'word/document.xml', data: Buffer.from(documento) },
  ]);
  lerZip(buf);
  return buf;
}
