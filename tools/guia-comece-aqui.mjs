#!/usr/bin/env node
// Gera o PDF "COMECE AQUI" de cada pacote, em formato de celular (9:16).
//   node tools/guia-comece-aqui.mjs     -> _dist/v2/hotmart-7/ e hotmart-5/
// Rodar DEPOIS do empacotar.mjs (ele limpa _dist/v2).
//
// Existe porque o comprador de R$ 10 abre a compra no celular, vê um monte de .zip
// e acha que "o arquivo não abre". O guia diz, antes de tudo, qual arquivo é pra quem.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const RAIZ = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SAIDA = path.join(RAIZ, '_dist', 'v2');
const FONTE = 'D:/Aegis/Aegis/artes/templates/_fontes-embed-inter-var.css';
const PLAYWRIGHT = 'D:/Aegis/Aegis/node_modules/playwright/index.mjs';

const PACOTES = {
  'hotmart-7': {
    nome: '7 skills de leitura de gráfico',
    prompts: 'AEGIS-SKILLS-42-Prompts.pdf',
    promptsDesc: 'guia com 42 prompts prontos, 6 por skill',
    skills: [
      ['leitura-de-grafico', 'Leitura de Gráfico', 'faça a leitura desse gráfico', 'A carro-chefe. Antes: estrutura, zonas e cenários. Depois: confere a leitura com o que aconteceu.'],
      ['zonas-suporte-resistencia', 'Zonas de S/R', 'marque as zonas de suporte e resistência', 'Zonas (não linhas), com toques, força e frescor. Máximo 6.'],
      ['figuras-candle', 'Figuras de Candle', 'que figuras tem nesse gráfico e quais importam?', 'Nomeia a figura e julga pelo lugar onde ela apareceu.'],
      ['ondas-elliott', 'Ondas de Elliott', 'conte as ondas desse gráfico', 'Contagem com as 3 regras conferidas e contagem alternativa sempre.'],
      ['leitura-renko', 'Leitura Renko', 'leia esse renko pra mim', 'A gramática do tijolo: sequências, flips, congestão, rompimento.'],
      ['autopsia-de-trade', 'Autópsia de Trade', 'faça a autópsia dessa operação', 'Separa erro de leitura, disciplina, execução e variância. Uma lição.'],
      ['backtest-honesto', 'Backtest Honesto', 'como eu testo esse setup sem me enganar?', 'Desenha o teste e ataca resultado pronto (overfitting, amostra, vieses).'],
    ],
  },
  'hotmart-5': {
    nome: '5 skills de plano e validação',
    prompts: 'AEGIS-SKILLS-Trader-30-Prompts.pdf',
    promptsDesc: 'guia com 30 prompts prontos, 6 por skill',
    skills: [
      ['day-trade-plan', 'Day Trade Plan', 'monte o plano de amanhã no WIN, risco de R$ 100', 'Plano do dia: agenda, níveis, 3 cenários com R e contratos calculados.'],
      ['session-news-radar', 'Session News Radar', 'o que tem hoje que pode mexer no dólar?', 'Agenda da sessão pro SEU ativo, em horário de Brasília.'],
      ['swing-trade-plan', 'Swing Trade Plan', 'monte um swing em PETR4', 'Tese, catalisadores, stop estrutural e invalidação separada do stop.'],
      ['crypto-trade-plan', 'Crypto Trade Plan', 'estou long 10x em BTC, onde liquida?', 'Funding, OI, liquidação e tamanho de posição calculado.'],
      ['setup-backtest', 'Setup Backtest', 'analise minha planilha de trades', 'Métricas em R, Monte Carlo e veredito: vale ou não vale operar.'],
    ],
  },
};

const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

function html(id, p) {
  const n = p.skills.length;
  const docx = `AEGIS SKILLS - ${n} skills - versao para colar em qualquer IA.docx`;
  const zips = p.skills.map(([nome]) => `<li><span class="mono">${nome}.zip</span></li>`).join('');
  const exemplos = p.skills
    .map(([, titulo, pedido, oque]) => `<div class="ex"><b>${esc(titulo)}</b><span>${esc(oque)}</span><i>"${esc(pedido)}"</i></div>`)
    .join('');
  return `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<style>
${fs.readFileSync(FONTE, 'utf8')}
@page { size: 110mm 195.5mm; margin: 0; }
:root { --azul:#0000FE; --tinta:#1A1511; --papel:#FDFBEF; --cinza:#6b645c; --linha:#e4ddd0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: var(--papel); }
body { font-family: 'Inter V3', 'Segoe UI', Arial, sans-serif; color: var(--tinta); font-size: 9.6pt; line-height: 1.42; }
.pg { width: 110mm; height: 195.5mm; padding: 11mm 9mm 9mm; page-break-after: always; position: relative; overflow: hidden; display: flex; flex-direction: column; }
.pg:last-child { page-break-after: auto; }
.topo { font-size: 6.6pt; letter-spacing: .14em; text-transform: uppercase; font-weight: 600; color: var(--cinza); margin-bottom: 6mm; display: flex; justify-content: space-between; }
h1 { font-size: 30pt; line-height: 1.02; font-weight: 800; letter-spacing: -.02em; }
h2 { font-size: 15pt; line-height: 1.12; font-weight: 750; letter-spacing: -.01em; margin-bottom: 3.5mm; }
h3 { font-size: 10.5pt; font-weight: 700; margin: 3.5mm 0 1.5mm; }
p { margin-bottom: 2.4mm; }
.azul { color: var(--azul); }
.mono { font-family: Consolas, 'Courier New', monospace; font-size: 8.4pt; }
.capa { background: var(--tinta); color: var(--papel); }
.capa .topo { color: #b9ae9f; }
.capa .sub { font-size: 12pt; margin-top: 5mm; font-weight: 500; color: #e9e1d2; }
.capa .faixa { margin-top: auto; border-top: 1px solid #3a322b; padding-top: 4mm; font-size: 9pt; color: #d8cfbf; }
.capa .faixa b { color: #fff; }
.tag { display: inline-block; background: var(--azul); color: #fff; font-weight: 700; font-size: 7pt; letter-spacing: .12em; padding: 1.2mm 2.4mm; border-radius: 1mm; text-transform: uppercase; margin-bottom: 5mm; }
.card { border: 1px solid var(--linha); background: #fff; border-radius: 2.4mm; padding: 3.4mm 3.6mm; margin-bottom: 3mm; }
.card.dest { border: 1.6px solid var(--azul); }
.card .k { font-size: 6.8pt; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--azul); margin-bottom: 1mm; }
.card .t { font-weight: 700; font-size: 10.4pt; margin-bottom: 1mm; }
ul, ol { padding-left: 4.6mm; margin-bottom: 2.4mm; }
li { margin-bottom: 1.1mm; }
ol.passos { list-style: none; padding: 0; counter-reset: p; }
ol.passos li { counter-increment: p; position: relative; padding-left: 7.6mm; margin-bottom: 2.6mm; }
ol.passos li::before { content: counter(p); position: absolute; left: 0; top: -.2mm; width: 5.2mm; height: 5.2mm; border-radius: 50%; background: var(--azul); color: #fff; font-weight: 700; font-size: 7.6pt; display: flex; align-items: center; justify-content: center; }
.alerta { background: var(--tinta); color: var(--papel); border-radius: 2.4mm; padding: 3.2mm 3.6mm; margin: 2mm 0 3mm; }
.alerta b { color: #fff; }
.ex { border-bottom: 1px solid var(--linha); padding: 1.9mm 0; display: grid; grid-template-columns: 1fr; gap: .4mm; }
.ex b { font-size: 9.4pt; }
.ex span { font-size: 8.4pt; color: var(--cinza); }
.ex i { font-size: 8.6pt; color: var(--azul); font-style: normal; font-weight: 600; }
.faq b { display: block; margin-top: 2.6mm; font-size: 9.4pt; }
.faq span { display: block; font-size: 8.8pt; }
.rodape { margin-top: auto; font-size: 6.8pt; color: var(--cinza); border-top: 1px solid var(--linha); padding-top: 2.4mm; }
.arq { display: flex; gap: 2.4mm; align-items: flex-start; padding: 2mm 0; border-bottom: 1px solid var(--linha); }
.arq .ic { flex: none; width: 10mm; height: 10mm; border-radius: 1.6mm; background: var(--tinta); color: #fff; font-size: 6.4pt; font-weight: 800; display: flex; align-items: center; justify-content: center; letter-spacing: .04em; }
.arq .ic.z { background: var(--azul); }
.arq .ic.d { background: #2b579a; }
.arq .ic.p { background: #b3261e; }
.arq div b { display: block; font-size: 9.2pt; }
.arq div span { font-size: 8.3pt; color: var(--cinza); }
</style></head><body>

<section class="pg capa">
  <div class="topo"><span>AEGIS SKILLS</span><span>Leia em 2 minutos</span></div>
  <div class="tag">Comece aqui</div>
  <h1>Antes de abrir qualquer arquivo, leia isto.</h1>
  <p class="sub">${esc(p.nome)}. Este guia diz qual arquivo é pra você e como usar em menos de 5 minutos.</p>
  <div class="faixa"><b>Resumo:</b> tem Claude pago? Envie os .zip pro Claude pelo computador. Não tem, ou usa ChatGPT ou Gemini? Abra o arquivo .docx e cole o texto na sua IA. Funciona no celular.</div>
</section>

<section class="pg">
  <div class="topo"><span>01 · O que você recebeu</span><span>${n} skills</span></div>
  <h2>Os arquivos da sua compra</h2>
  <div class="arq"><div class="ic p">PDF</div><div><b>COMECE AQUI</b><span>Este guia.</span></div></div>
  <div class="arq"><div class="ic d">DOCX</div><div><b>Versão para colar em qualquer IA</b><span>As ${n} skills em texto. Abre no celular. Serve pra Claude grátis, ChatGPT, Gemini e Grok.</span></div></div>
  <div class="arq"><div class="ic z">ZIP</div><div><b>Um .zip por skill</b><span>Pra instalar no Claude pago (Pro, Max ou Team). <u>Não é pra abrir</u>: é pra enviar ao Claude do jeito que veio.</span></div></div>
  <div class="arq"><div class="ic p">PDF</div><div><b>Prompts prontos</b><span>${esc(p.promptsDesc)}. Copie e use depois de instalar.</span></div></div>
  <h3>Os ${n} arquivos .zip</h3>
  <ul>${zips}</ul>
</section>

<section class="pg">
  <div class="topo"><span>02 · Escolha o seu caminho</span><span>3 caminhos</span></div>
  <h2>Qual é o seu caso?</h2>
  <div class="card dest"><div class="k">Caminho A</div><div class="t">Tenho Claude pago (Pro, Max ou Team)</div>Instale os .zip uma vez pelo computador. Depois as skills ficam na sua conta e acordam sozinhas quando o pedido combina. <b>Página 3.</b></div>
  <div class="card dest"><div class="k">Caminho B</div><div class="t">Não tenho Claude pago, ou uso ChatGPT, Gemini ou Grok</div>Use o arquivo .docx. Copie a skill, cole numa conversa nova e mande o pedido. Funciona no celular. <b>Página 4.</b></div>
  <div class="card"><div class="k">Caminho C</div><div class="t">Uso o Claude Code (terminal ou desktop)</div>Descompacte os .zip na pasta de skills. <b>Página 5.</b></div>
  <div class="alerta"><b>Por que o .zip "não abre" no celular:</b> ele não é um documento pra ler. É o pacote que o Claude instala. No celular, use o caminho B.</div>
</section>

<section class="pg">
  <div class="topo"><span>03 · Caminho A</span><span>Claude pago</span></div>
  <h2>Instalar no Claude (Pro, Max ou Team)</h2>
  <ol class="passos">
    <li>No <b>computador</b>, baixe os .zip da sua compra. <b>Não descompacte.</b></li>
    <li>Abra <b>claude.ai</b> no navegador e entre na sua conta.</li>
    <li>Vá em <b>Settings (Configurações) → Capabilities</b>. Ligue <b>Code execution and file creation</b>, se estiver desligado. As skills dependem disso.</li>
    <li>Na mesma tela, em <b>Skills</b>, clique em <b>Upload skill</b> e envie um .zip.</li>
    <li>Repita pra cada .zip. Confira se cada skill aparece ligada na lista.</li>
    <li>Abra uma conversa nova e faça o pedido normal, com o print se for de gráfico. A skill entra sozinha.</li>
  </ol>
  <div class="alerta"><b>Deu erro no upload?</b> Quase sempre é o arquivo descompactado ou renomeado. Baixe de novo da Hotmart e envie o .zip original.</div>
  <p>Quer forçar uma skill? Cite o nome: <span class="azul"><b>"use a skill ${esc(p.skills[0][0])}"</b></span>.</p>
  <p>Os nomes dos menus podem aparecer em inglês ou português, conforme o idioma da sua conta.</p>
</section>

<section class="pg">
  <div class="topo"><span>04 · Caminho B</span><span>Qualquer IA, até no celular</span></div>
  <h2>Usar no Claude grátis, ChatGPT, Gemini ou Grok</h2>
  <ol class="passos">
    <li>Abra o arquivo <b>.docx</b> (o celular abre direto, ou use Word ou Google Docs).</li>
    <li>Ache a skill que você quer. Cada uma começa numa página nova.</li>
    <li>Copie tudo da linha <b class="azul">===== INÍCIO =====</b> até a linha <b class="azul">===== FIM =====</b>.</li>
    <li>Abra uma <b>conversa nova</b> na sua IA e cole.</li>
    <li>Espere a resposta <b>"Pronto. Envie o print ou o pedido."</b></li>
    <li>Envie o print do gráfico ou o pedido.</li>
  </ol>
  <div class="card"><div class="k">Skill em 2 partes</div>As mais longas vêm marcadas <b>PARTE 1</b> e <b>PARTE 2</b>. Cole a parte 1, espere <b>"OK, mande a parte 2."</b> e cole a parte 2.</div>
  <p>Toda conversa nova começa do zero: cole de novo. No Claude dá pra evitar isso criando um <b>Projeto</b> e colando o texto nas instruções.</p>
</section>

<section class="pg">
  <div class="topo"><span>05 · Caminho C e como pedir</span><span>Exemplos</span></div>
  <h2>Claude Code</h2>
  <p>Descompacte cada .zip dentro de <span class="mono">~/.claude/skills/</span> (no Windows, <span class="mono">C:\\Users\\SEU_USUARIO\\.claude\\skills\\</span>). Cada skill fica numa pasta com um <span class="mono">SKILL.md</span>. Não precisa reiniciar.</p>
  <h3>O que cada uma faz e como pedir</h3>
  ${exemplos}
</section>

<section class="pg">
  <div class="topo"><span>06 · Deu problema?</span><span>Respostas rápidas</span></div>
  <h2>Print bom e respostas rápidas</h2>
  <p><b>Print que a IA lê bem:</b> eixo de preço visível, gráfico limpo (pouco indicador), uns 100 candles na tela, print direto da plataforma (foto da tela com o celular piora a leitura).</p>
  <div class="faq">
    <b>"O arquivo não abre."</b><span>O .zip não é pra abrir: é pra enviar ao Claude (caminho A). Pra ler ou usar no celular, abra o .docx (caminho B).</span>
    <b>"Não acho Upload skill."</b><span>Precisa de plano pago do Claude e de Code execution ligado em Settings → Capabilities. Sem plano pago, use o caminho B.</span>
    <b>"A skill não entrou na conversa."</b><span>Confira se ela está ligada na lista de skills e cite o nome no pedido.</span>
    <b>"A IA inventou um preço."</b><span>As skills marcam cada preço como lido no eixo ou aproximado. Se o eixo não aparece no print, ela avisa. Mande um print com o eixo legível.</span>
    <b>"Ainda não funcionou."</b><span>Fale com a gente pela página da sua compra na Hotmart, com o print da tela do erro.</span>
  </div>
  <div class="rodape">Nenhuma skill dá sinal de compra ou venda. Elas descrevem cenários com invalidação, e a decisão é sua. Material educacional, não é recomendação de investimento. Versão viva do pacote: github.com/aaegisengine/aegis-skills · Licença CC BY-NC 4.0: uso pessoal livre, revenda proibida.</div>
</section>
</body></html>`;
}

const { chromium } = await import(pathToFileURL(PLAYWRIGHT).href);
const browser = await chromium.launch();
try {
  for (const [id, p] of Object.entries(PACOTES)) {
    const dir = path.join(SAIDA, id);
    if (!fs.existsSync(dir)) throw new Error(`${dir} não existe: rode tools/empacotar.mjs antes`);
    const arqHtml = path.join(dir, '_comece-aqui.html');
    fs.writeFileSync(arqHtml, html(id, p));
    const page = await browser.newPage();
    await page.goto(pathToFileURL(arqHtml).href, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    const destino = path.join(dir, `COMECE AQUI - AEGIS SKILLS ${p.skills.length} skills.pdf`);
    await page.pdf({ path: destino, preferCSSPageSize: true, printBackground: true });
    // Prova visual de cada página, pra conferir sem abrir o PDF.
    const prova = path.join(dir, '_prova');
    fs.mkdirSync(prova, { recursive: true });
    await page.setViewportSize({ width: 416, height: 739 });
    const paginas = await page.$$('section.pg');
    for (let i = 0; i < paginas.length; i++) await paginas[i].screenshot({ path: path.join(prova, `p${i + 1}.png`) });
    await page.close();
    fs.rmSync(arqHtml);
    console.log(`ok  ${path.relative(RAIZ, destino)} (${paginas.length} páginas)`);
  }
} finally {
  await browser.close();
}
