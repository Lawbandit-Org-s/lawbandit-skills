#!/usr/bin/env python3
"""Build the crib sheet, export a PDF, and report whether it fits.

Usage: python3 fit.py SRC.txt OUT.docx SIZE LINEF IMGS [COLS] [--pages N] [--a4] [--no-autosub]
                      [--converter word|libreoffice|none]
  SIZE  font size in half-points (11 = 5.5pt)     LINEF line-height factor (0.96 = tight)
  IMGS  image scale (0.95)                          COLS  page columns (default 6)
  --pages N  pages allowed (default 1)

Works on macOS (Word or LibreOffice), Windows (Word or LibreOffice) and Linux (LibreOffice).
Prints: pages, how far down the last column the text reaches, and the PDF path.
LibreOffice may substitute fonts (e.g. Arial Narrow), so its fit is approximate: leave a little room.
"""
import argparse, os, platform, shutil, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
OS = {'Darwin': 'mac', 'Windows': 'windows'}.get(platform.system(), 'linux')

ap = argparse.ArgumentParser()
for a in ('src', 'out', 'size', 'linef', 'imgs'):
    ap.add_argument(a)
ap.add_argument('cols', nargs='?', default='6')
ap.add_argument('--pages', type=int, default=1)
ap.add_argument('--a4', action='store_true')
ap.add_argument('--no-autosub', action='store_true')
ap.add_argument('--converter', choices=['word', 'libreoffice', 'none'])
a = ap.parse_args()
src, out = os.path.abspath(a.src), os.path.abspath(a.out)

# 1. build the .docx
env = dict(os.environ, LINEF=a.linef, IMGS=a.imgs)
if a.a4: env['PAPER'] = 'a4'
if a.no_autosub: env['AUTOSUB'] = '0'
if shutil.which('npm') and not os.path.isdir(os.path.join(HERE, 'node_modules', 'docx')):
    env['NODE_PATH'] = subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True, shell=OS == 'windows').stdout.strip()
r = subprocess.run(['node', os.path.join(HERE, 'build.js'), src, out, a.size, a.cols], env=env, capture_output=True, text=True)
if r.returncode:
    sys.exit('Build failed:\n' + r.stderr[-1500:] + '\nRun check_setup.py to see what is missing.')

# 2. export a PDF
def soffice():
    for p in (shutil.which('soffice'), shutil.which('libreoffice'),
              '/Applications/LibreOffice.app/Contents/MacOS/soffice', r'C:\Program Files\LibreOffice\program\soffice.exe'):
        if p and os.path.exists(p):
            return p

conv = a.converter
if not conv:
    word = (OS == 'mac' and os.path.isdir('/Applications/Microsoft Word.app')) or OS == 'windows'
    conv = 'word' if word else 'libreoffice' if soffice() else 'none'

pdf = None
if conv == 'word' and OS == 'mac':
    # Word is sandboxed on macOS: it may only write inside its own container.
    pdf = os.path.expanduser('~/Library/Containers/com.microsoft.Word/Data/crib_check.pdf')
    if os.path.exists(pdf): os.remove(pdf)
    script = f'''tell application "Microsoft Word"
  open (POSIX file "{out}")
  delay 8
  set d to active document
  save as d file name "{pdf}" file format format PDF
  close d saving no
end tell'''
    subprocess.run(['osascript', '-e', script], capture_output=True)
elif conv == 'word' and OS == 'windows':
    pdf = os.path.splitext(out)[0] + '_check.pdf'
    ps = (f"$w=New-Object -ComObject Word.Application; $w.Visible=$false; "
          f"$d=$w.Documents.Open('{out}'); $d.SaveAs([ref]'{pdf}',[ref]17); $d.Close($false); $w.Quit()")
    r = subprocess.run(['powershell', '-NoProfile', '-Command', ps], capture_output=True, text=True)
    if r.returncode and soffice():
        conv = 'libreoffice'  # Word not actually installed: fall back
if conv == 'libreoffice':
    tmp = tempfile.mkdtemp()
    subprocess.run([soffice(), '--headless', '--convert-to', 'pdf', '--outdir', tmp, out], capture_output=True, timeout=180)
    pdf = os.path.join(tmp, os.path.splitext(os.path.basename(out))[0] + '.pdf')
if conv == 'none' or not pdf or not os.path.exists(pdf):
    print(f'Built {out}, but could not export a PDF (converter: {conv}). '
          'Open the .docx in Word, Google Docs or Pages and check the page count by eye.'
          + (' On macOS a Word timing failure is common: rerun.' if conv == 'word' else ''))
    sys.exit(2)

# 3. measure: page count and bottom of the text in the last column of the last page
pw, ph = (842, 595) if a.a4 else (792, 612)
xmin = pw - 9 - (pw - 18) / int(a.cols)
pages, bottom = None, None
if shutil.which('pdftotext'):
    info = subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout
    pages = int(next(l.split()[-1] for l in info.splitlines() if l.startswith('Pages')))
    bbox = subprocess.run(['pdftotext', '-f', str(pages), '-l', str(pages), '-bbox', pdf, '-'], capture_output=True, text=True).stdout
    ys = []
    for line in bbox.splitlines():
        if '<word' in line:
            f = line.split('"')
            if float(f[1]) > xmin: ys.append(float(f[7]))
    bottom = max(ys) if ys else None
else:
    try:
        import pdfplumber
        with pdfplumber.open(pdf) as doc:
            pages = len(doc.pages)
            ws = [w for w in doc.pages[-1].extract_words() if w['x0'] > xmin]
            bottom = max((w['bottom'] for w in ws), default=None)
    except ImportError:
        print('(install poppler or pdfplumber to measure fill)')

verdict = ('TOO LONG: shrink' if pages and pages > a.pages else
           'ROOM LEFT: grow or add content' if pages and pages < a.pages or (bottom or 0) < 0.88 * ph else
           'FITS' if pages else 'UNKNOWN')
print(f'converter={conv} size={a.size} line={a.linef} img={a.imgs} cols={a.cols} pages={pages}/{a.pages} '
      f'last_col_bottom={bottom and round(bottom)} (page height {ph}) -> {verdict}\npdf={pdf}')
