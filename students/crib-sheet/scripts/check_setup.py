#!/usr/bin/env python3
"""Check what this computer has for building and fitting a crib sheet.

Usage: python3 check_setup.py [--install]
  --install  also installs the docx npm package next to build.js (no admin rights needed)

Prints one line per tool (OK / MISSING), then the setup mode the skill should use
and the install commands for anything missing on this operating system.
"""
import os, platform, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OS = {'Darwin': 'mac', 'Windows': 'windows'}.get(platform.system(), 'linux')


def run(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=60).stdout.strip()
    except Exception:
        return ''


def has_docx_module():
    if os.path.isdir(os.path.join(HERE, 'node_modules', 'docx')):
        return True
    root = run(['npm', 'root', '-g']) if shutil.which('npm') else ''
    return bool(root) and os.path.isdir(os.path.join(root, 'docx'))


def find_word():
    if OS == 'mac':
        return os.path.isdir('/Applications/Microsoft Word.app')
    if OS == 'windows':
        out = run(['powershell', '-NoProfile', '-Command',
                   "[bool](Get-ItemProperty 'HKLM:\\SOFTWARE\\Classes\\Word.Application' -ErrorAction SilentlyContinue)"])
        return out.lower() == 'true'
    return False


def find_soffice():
    for name in ('soffice', 'libreoffice'):
        if shutil.which(name):
            return shutil.which(name)
    for p in ('/Applications/LibreOffice.app/Contents/MacOS/soffice',
              r'C:\Program Files\LibreOffice\program\soffice.exe'):
        if os.path.exists(p):
            return p
    return None


def has_py(mod):
    try:
        __import__(mod)
        return True
    except Exception:
        return False


if '--install' in sys.argv and shutil.which('npm') and not has_docx_module():
    print('Installing docx next to build.js ...')
    run(['npm', 'install', '--prefix', HERE, 'docx@9'])

checks = {
    'node': bool(shutil.which('node')),
    'docx (npm)': has_docx_module(),
    'Microsoft Word': find_word(),
    'LibreOffice': bool(find_soffice()),
    'poppler (pdftotext)': bool(shutil.which('pdftotext')),
    'pdfplumber (python)': has_py('pdfplumber'),
    'matplotlib (python)': has_py('matplotlib'),
}
print(f'Operating system: {OS} ({platform.platform()})')
for k, v in checks.items():
    print(f'  {"OK     " if v else "MISSING"} {k}')

can_build = checks['node'] and checks['docx (npm)']
converter = 'word' if checks['Microsoft Word'] else 'libreoffice' if checks['LibreOffice'] else None
can_measure = checks['poppler (pdftotext)'] or checks['pdfplumber (python)']
if can_build and converter and can_measure:
    mode = f'FULL: build + export with {converter} + measure fill'
elif can_build and converter:
    mode = 'BUILD + PAGE COUNT: can export a PDF but not measure column fill (install poppler or pdfplumber)'
elif can_build:
    mode = 'BUILD ONLY: makes the .docx; the student checks the fit by opening it in Word / Google Docs / Pages'
else:
    mode = 'CONTENT ONLY: cannot make the .docx here (install node + docx), or write the sheet as text'
print('\nMode:', mode)

INSTALL = {
    'mac': {
        'node': 'brew install node   (or the installer from https://nodejs.org)',
        'docx (npm)': f'python3 "{__file__}" --install',
        'Microsoft Word': 'optional; free alternative: brew install --cask libreoffice',
        'LibreOffice': 'brew install --cask libreoffice   (only needed if there is no Word)',
        'poppler (pdftotext)': 'brew install poppler   (or: pip3 install pdfplumber)',
        'pdfplumber (python)': 'pip3 install pdfplumber   (only needed if there is no poppler)',
        'matplotlib (python)': 'pip3 install matplotlib   (only for charts)',
    },
    'windows': {
        'node': 'winget install OpenJS.NodeJS   (or https://nodejs.org)',
        'docx (npm)': f'python "{__file__}" --install',
        'Microsoft Word': 'optional; free alternative: winget install TheDocumentFoundation.LibreOffice',
        'LibreOffice': 'winget install TheDocumentFoundation.LibreOffice   (only needed if there is no Word)',
        'poppler (pdftotext)': 'pip install pdfplumber   (easier than poppler on Windows)',
        'pdfplumber (python)': 'pip install pdfplumber',
        'matplotlib (python)': 'pip install matplotlib   (only for charts)',
    },
    'linux': {
        'node': 'sudo apt install nodejs npm',
        'docx (npm)': f'python3 "{__file__}" --install',
        'Microsoft Word': 'not available on Linux; use LibreOffice',
        'LibreOffice': 'sudo apt install libreoffice-writer',
        'poppler (pdftotext)': 'sudo apt install poppler-utils',
        'pdfplumber (python)': 'pip3 install pdfplumber',
        'matplotlib (python)': 'pip3 install matplotlib   (only for charts)',
    },
}
# Word and LibreOffice are alternatives, as are poppler and pdfplumber: only report a gap if both are missing.
skip = set()
if checks['Microsoft Word'] or checks['LibreOffice']:
    skip |= {'Microsoft Word', 'LibreOffice'}
elif OS != 'linux':
    skip.add('LibreOffice')  # suggest via the Word line
if can_measure:
    skip |= {'poppler (pdftotext)', 'pdfplumber (python)'}
elif OS == 'windows':
    skip.add('poppler (pdftotext)')
else:
    skip.add('pdfplumber (python)')
missing = [k for k, v in checks.items() if not v and k not in skip]
if missing:
    print('\nTo install what is missing:')
    for k in missing:
        print(f'  {k}: {INSTALL[OS][k]}')
