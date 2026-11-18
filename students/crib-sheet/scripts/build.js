const path = require('path');
const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, PageOrientation, ShadingType,
  LevelFormat, LineRuleType, Table, TableRow, TableCell, WidthType, BorderStyle, ImageRun,
} = require('docx');

const [, , src, out, sizeArg, colsArg] = process.argv;
const SIZE = Number(sizeArg || 11);
const COLS = Number(colsArg || 6);
const FONT = 'Arial Narrow';
const LINE = Math.round(SIZE * 10 * Number(process.env.LINEF || 1.06));
const PAPER = (process.env.PAPER || 'letter').toLowerCase();  // letter | a4
const PAGE_W = PAPER === 'a4' ? 16838 : 15840, MARGIN = 180, GAP = 80;
const COL_W = Math.floor((PAGE_W - 2 * MARGIN - (COLS - 1) * GAP) / COLS);

const unesc = s => s.replace(/\\\|/g, '|');
// Split text into plain / subscript / superscript pieces.
// _x, _{..}, _(..) -> subscript; ^x, ^{..}, ^(..) -> superscript; q1, p2, π1 ... -> auto-subscript digit.
function scripts(s) {
  const out = [];
  const re = /([_^])(\{[^}]*\}|\([^)]*\)|−?[A-Za-z0-9α-ωΑ-Ω.]+)|(?<![A-Z])([qpcvsTPQUDSπ])([12])(?![0-9]|[,.][0-9])/g;
  const auto = process.env.AUTOSUB !== '0';
  let last = 0, m;
  while ((m = re.exec(s))) {
    if (!m[1] && !auto) continue;
    if (m.index > last) out.push({ t: s.slice(last, m.index) });
    if (m[1]) {
      let v = m[2];
      if (/^[{(]/.test(v)) v = v.slice(1, -1);
      out.push({ t: v, sub: m[1] === '_', sup: m[1] === '^' });
    } else {
      out.push({ t: m[3] }); out.push({ t: m[4], sub: true });
    }
    last = re.lastIndex;
  }
  if (last < s.length) out.push({ t: s.slice(last) });
  return out;
}
// **bold** (yellow if it contains "="), ==bold yellow key term==, ~green "what this gives you"~,
// *italic* (case names); \* = literal asterisk.
function runs(text, base = {}) {
  const res = [];
  unesc(text).replace(/\\\*/g, '\u0001').split('==').forEach((key, k) => {
    key.split('**').forEach((seg, i) => {
      const bold = base.bold || i % 2 === 1 || k % 2 === 1;
      const hi = k % 2 === 1 || (i % 2 === 1 && seg.includes('='));
      seg.split('~').forEach((part, j) => {
        const green = j % 2 === 1;
        part.split('*').forEach((piece, m) => {
          for (const p of scripts(piece.replace(/\u0001/g, '*'))) res.push(new TextRun({
            text: p.t, bold, italics: m % 2 === 1 || undefined, color: base.color, font: FONT, size: SIZE,
            highlight: hi ? 'yellow' : undefined,
            shading: green ? { type: ShadingType.CLEAR, color: 'auto', fill: 'C6EFCE' } : undefined,
            subScript: p.sub || undefined, superScript: p.sup || undefined,
          }));
        });
      });
    });
  });
  return res;
}
const tight = { before: 0, after: 0, line: LINE, lineRule: LineRuleType.EXACT };
const para = (text, opts = {}) => new Paragraph({ spacing: tight, ...opts, children: runs(text, opts.base) });

const thin = { style: BorderStyle.SINGLE, size: 2, color: '999999' };
const borders = { top: thin, bottom: thin, left: thin, right: thin };
const cellMargins = { top: 0, bottom: 0, left: 30, right: 30 };

function widths(n, firstPct) {
  if (n === 2) { const a = Math.round(COL_W * (firstPct || 0.17)); return [a, COL_W - a]; }
  const first = Math.round(COL_W * 0.24), rest = Math.floor((COL_W - first) / (n - 1));
  const w = [first, ...Array(n - 1).fill(rest)];
  w[n - 1] += COL_W - w.reduce((x, y) => x + y, 0);
  return w;
}

function buildTable(rawTitle, rows) {
  const m = rawTitle.match(/^(.*) @(\d+)$/);
  const title = m ? m[1] : rawTitle;
  const n = Math.max(...rows.map(r => r.length));
  const w = widths(n, m ? Number(m[2]) / 100 : undefined);
  const trs = [new TableRow({ children: [new TableCell({
    columnSpan: n, width: { size: COL_W, type: WidthType.DXA }, borders, margins: cellMargins,
    shading: { type: ShadingType.CLEAR, color: 'auto', fill: 'D9D9D9' },
    children: [para(title, { base: { bold: true }, keepNext: true })],
  })] })];
  rows.forEach((r, ri) => {
    const header = n > 2 && ri === 0;
    trs.push(new TableRow({ children: r.map((c, ci) => new TableCell({
      width: { size: w[ci], type: WidthType.DXA }, borders, margins: cellMargins,
      columnSpan: (ci === r.length - 1 && r.length < n) ? n - ci : undefined,
      shading: header ? { type: ShadingType.CLEAR, color: 'auto', fill: 'F0F0F0' } : undefined,
      children: [para(c, { keepNext: ri < Math.min(rows.length - 1, rows.length > 7 ? 2 : 99), base: { bold: header || (ci === 0 && n === 2) } })],
    })) }));
  });
  return new Table({ width: { size: COL_W, type: WidthType.DXA }, columnWidths: w, rows: trs });
}

const body = [];
const lines = fs.readFileSync(src, 'utf8').split('\n').map(l => l.trimEnd()).filter(Boolean);
for (let i = 0; i < lines.length; i++) {
  const line = lines[i];
  if (line.startsWith('IMG ')) {
    const files = line.slice(4).trim().split(/\s+/);
    const each = Math.floor(COL_W / files.length);
    const none = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
    const nb = { top: none, bottom: none, left: none, right: none };
    body.push(new Table({ width: { size: COL_W, type: WidthType.DXA }, columnWidths: files.map(() => each),
      borders: { ...nb, insideHorizontal: none, insideVertical: none },
      rows: [new TableRow({ children: files.map(f => {
        const buf = fs.readFileSync(path.join(path.dirname(src), 'img', f));
        const w = buf.readUInt32BE(16), h = buf.readUInt32BE(20);
        const wpx = Math.floor((each - 40) / 1440 * 96 * Number(process.env.IMGS || 1));
        return new TableCell({ width: { size: each, type: WidthType.DXA }, borders: nb,
          margins: { top: 0, bottom: 0, left: 10, right: 10 },
          children: [new Paragraph({ spacing: { before: 0, after: 0 }, alignment: AlignmentType.CENTER,
            children: [new ImageRun({ type: 'png', data: buf, transformation: { width: wpx, height: Math.round(wpx * h / w) } })] })] });
      }) })] }));
    continue;
  }
  if (line.startsWith('R ') && process.env.FLAT) {
    const title = line.slice(2).replace(/ @\d+$/, '');
    const rows = [];
    while (i + 1 < lines.length && lines[i + 1].startsWith('| ')) rows.push(lines[++i].slice(2).split(' | '));
    body.push(para(title, { base: { bold: true }, keepNext: true,
      shading: { type: ShadingType.CLEAR, color: 'auto', fill: 'D9D9D9' } }));
    const n = Math.max(...rows.map(r => r.length));
    const hdr = n > 2 ? rows.shift() : null;
    for (const r of rows) {
      let text;
      if (r.length === 1) text = r[0];
      else if (hdr) text = '**' + r[0] + ':** ' + r.slice(1).map((c, k) => hdr[k + 1] + ' ' + c).join('; ');
      else text = (/^\d+$/.test(r[0]) ? '**' + r[0] + ')** ' : '**' + r[0] + ':** ') + r[1];
      body.push(para(text, { numbering: { reference: 'b', level: 0 } }));
    }
    continue;
  }
  if (line.startsWith('R ')) {
    const rows = [];
    while (i + 1 < lines.length && lines[i + 1].startsWith('| ')) {
      rows.push(lines[++i].slice(2).split(' | '));
    }
    body.push(buildTable(line.slice(2), rows));
    body.push(new Paragraph({ spacing: { before: 0, after: 0, line: 50, lineRule: LineRuleType.EXACT }, children: [] }));
  } else if (line.startsWith('T ')) {
    body.push(para(line.slice(2), { alignment: AlignmentType.CENTER, base: { bold: true } }));
  } else if (line.startsWith('# ')) {
    body.push(para(line.slice(2), {
      spacing: { ...tight, before: 30 }, base: { bold: true, color: 'FFFFFF' }, keepNext: true,
      shading: { type: ShadingType.CLEAR, color: 'auto', fill: '333333' },
    }));
  } else if (line.startsWith('- ')) {
    body.push(para(line.slice(2), { numbering: { reference: 'b', level: 0 } }));
  } else {
    body.push(para(line));
  }
}

const doc = new Document({
  styles: { default: { document: { run: { font: FONT, size: SIZE } } } },
  numbering: { config: [{ reference: 'b', levels: [{
    level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT,
    style: { paragraph: { indent: { left: 80, hanging: 80 } } },
  }] }] },
  sections: [{
    properties: {
      page: {
        size: PAPER === 'a4' ? { width: 11906, height: 16838, orientation: PageOrientation.LANDSCAPE }
                             : { width: 12240, height: 15840, orientation: PageOrientation.LANDSCAPE },
        margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN, header: 0, footer: 0 },
      },
      column: { count: COLS, space: GAP, separate: false },
    },
    children: body,
  }],
});
Packer.toBuffer(doc).then(b => { fs.writeFileSync(out, b); console.log('wrote', out, 'colW', COL_W); });
