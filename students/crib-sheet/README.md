# Crib sheet skill: install guide

This skill makes a one-page (or N-page) exam crib sheet as a Word file: landscape, with narrow
columns, highlighted key terms, and fitted so the page is full without spilling over. Before
building, it asks about your exam and the style you want.

## 1. Install the skill

**Claude Code (Mac, Windows or Linux)**
1. Unzip this folder.
2. Move the `crib-sheet` folder into your skills folder:
   - Mac / Linux: `~/.claude/skills/crib-sheet/`
   - Windows: `C:\Users\<you>\.claude\skills\crib-sheet\`
3. Start Claude Code and say "make a crib sheet for my [class] exam".

**Claude desktop / claude.ai**
Settings → Capabilities → Skills → upload the zip. (Code execution must be turned on.)

## 2. Tools it uses (Claude checks these for you)

On first use, Claude runs `scripts/check_setup.py`. That script tells you what's missing and the
exact command to install it on your computer. Here is a summary:

| Tool | Why | Mac | Windows | Linux |
|---|---|---|---|---|
| Node.js | builds the Word file | `brew install node` or nodejs.org | `winget install OpenJS.NodeJS` | `sudo apt install nodejs npm` |
| docx package | same | `python3 scripts/check_setup.py --install` | `python scripts\check_setup.py --install` | same as Mac |
| Word **or** LibreOffice | checks the sheet fits the page | Word, or `brew install --cask libreoffice` | Word, or `winget install TheDocumentFoundation.LibreOffice` | `sudo apt install libreoffice-writer` |
| pdfplumber **or** poppler | measures how full the page is | `pip3 install pdfplumber` | `pip install pdfplumber` | `pip3 install pdfplumber` |
| matplotlib (optional) | small charts | `pip3 install matplotlib` | `pip install matplotlib` | `pip3 install matplotlib` |

You also need Python 3 (python.org; preinstalled on most Macs and Linux).

**No setup at all?** The skill still works. Claude writes the content, and you paste it into Word or
Google Docs and check the page count yourself. Claude gives you the settings to use.

**Tip:** if you'll print from Word, measure with Word. LibreOffice lays the page out about 10% shorter.

## 3. Adjust it

- **Change the look:** fonts, colors, and margins are at the top of `scripts/build.js`
  (`FONT`, `MARGIN`, `GAP`; color codes like `C6EFCE` = green).
- **Change the rules:** edit `SKILL.md`, which lists what Claude asks and how it lays out the sheet.
- **Sample sheets:** `assets/examples/quant/` (economics, step-by-step recipes) and
  `assets/examples/law/` (torts, rule blocks).
