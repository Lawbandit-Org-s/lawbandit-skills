---
name: crib-sheet
description: Build an exam crib sheet (cheat sheet, formula sheet, attack sheet, or note sheet you can bring in) as a dense Word file. It is landscape with narrow columns, cut to the page limit the exam allows and filled edge to edge. It first asks the student about the exam and how they like information laid out. Then it builds either "recipe" tables for problem-solving classes (given → numbered steps → shortcut → check), "rule blocks" for law and other rules-based classes (issue checklist → rule and elements → tests → key cases → "Here," analysis prompts → defenses → traps), or a mix of both. Key terms and equations are highlighted yellow, a green label says what each step gives you, case names are in italics, and small charts are included. Use when someone says "make a crib sheet", "cheat sheet", "formula sheet", "attack outline on one page", "one-page sheet for my exam", "notes sheet I can bring in", "condense my outline to N pages", or wants to shrink, refit, or add to an existing sheet. Works for any class: law (torts, contracts, evidence, tax), economics, statistics, finance, accounting, sciences.
argument-hint: [class] [exam] [topics or weeks]
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, AskUserQuestion, SendUserFile
---

# Crib sheet builder

This skill makes the densest sheet that is still readable, where a student can find the right recipe
or rule for an exam question in seconds. It shows **which tool fits the question, where every number
or element comes from, and what each step produces**.

## Step 0: check the computer (do this first, every new setup)

Run `python3 <skill dir>/scripts/check_setup.py` (`python` on Windows). It reports the operating system,
which tools are present, a **mode**, and the install command for each missing tool on that OS.

| Tool | Needed for | If missing |
|---|---|---|
| node + `docx` npm package | making the .docx | `check_setup.py --install` installs `docx` next to the scripts (no admin rights) once node exists |
| Microsoft Word **or** LibreOffice | exporting a PDF to measure the fit | LibreOffice is free; Word is better if the student will print from Word |
| poppler **or** pdfplumber | measuring how full the columns are | `pip install pdfplumber` is the easiest on every OS |
| matplotlib | charts (optional) | `pip install matplotlib` |

If anything is missing, **tell the student in plain words what it is for** and ask with
AskUserQuestion how to proceed:
- **Install it now (recommended).** Give the exact command for their OS from the script's output,
  and run it yourself if you have a shell and they agree. Installing an app (node, LibreOffice,
  Word) needs their permission.
- **Use what's here.** E.g. LibreOffice instead of Word, or skip measuring and check the page by eye.
- **No setup (content only).** If there's no shell or nothing can be installed (e.g. a chat-only
  app): build the sheet content and give the .docx if possible. Otherwise give the source text
  plus instructions to paste it into Word or Google Docs in landscape, N columns, 5.5–7pt Arial Narrow,
  0.25 in margins, with the student checking the page count themselves.

Also ask **which app they will print from**. LibreOffice lays the page out about 10% shorter than
Word, so if they measure with LibreOffice but print from Word, aim for the last column at ~80% full, not ~88%.

## Step 1: ask about the exam and the student's style

Ask these questions with AskUserQuestion; don't guess. Combine them into one or two rounds. Skip any
question the student already answered, and offer recommended defaults.

1. **Class and exam.** Which class, midterm or final, and which weeks or topics are covered?
2. **Exam format.** Problem-solving (calculations), essay or issue-spotter, short answer / multiple
   choice, or a mix. This decides the layout:
   - **calculations → recipe tables**
   - **essays → rule blocks**
   - **mixed → both**, with the issue checklist first
3. **What's allowed.** Page count, one side or two, letter or A4, handwritten-only rules, minimum
   font size if any. Open book? (If it's open book, the sheet can be an index into the outline
   rather than a copy of it.)
4. **Materials.** Where are the syllabus, slides, lecture notes or transcripts, casebook excerpts,
   practice exams with answers, and any existing outline? Ask for **their own outline or a past
   sheet they liked** and copy its conventions (abbreviations, essay order, color habits).
5. **Style.**
   - Density: tiny text with everything in, or bigger text with only the essentials?
   - Columns: 6 is very dense, 4–5 is readable, 3 matches a typical law attack outline.
   - Highlighting: yes or no. Plain words or symbols?
   - Include cases? If so, as name only or name + one-line facts/holding.
   - Include worked check examples? Include charts?
6. **Course AI policy.** Are there graded problem sets or take-home exams AI may not touch? If so,
   use them only for coverage and notation. Never solve, check, or quote their answers.

## Hard rules

1. **Respect the course's AI and honor-code rules** (step 0 question 6). Worked examples use made-up facts and numbers.
2. **Cover the whole course scope, not just the parts the student mentioned.** Read the syllabus,
   all materials, and especially practice exams. Add anything a practice exam tests that the sheet lacks.
3. **Fit the allowed page limit exactly**, filled to the bottom of the last column. Use the build-and-fit loop.
4. **Never refer to "the slide" or "the example from class."** The student won't remember it under
   exam pressure. Write the general rule plus the sheet's own example.

## Layout A: recipe tables (calculations)

- **One table per problem type**, with rows in this order:
  - `Given`: the inputs, and what each letter means
  - numbered steps `1, 2, 3 …`
  - `Shortcut`: a closed-form formula, **labeled as a shortcut**
  - `Check`: a tiny worked example with made-up numbers
- **Start from the beginning every time.** Write the full formula before simplifying it, and show
  each algebra move ("multiply out", "derivative wrt x only", "× 6 both sides").
- **Never use a number without saying where it came from.**
- Add a **SYMBOLS** table for Greek letters and notation, plus a "Marks" row explaining the colors.
- Put charts where a picture helps (curves, shifts, best responses), two side by side per column.

## Layout B: rule blocks (law and other rules-based classes)

- **First table: ATTACK ORDER.** The essay order the professor wants (e.g. Issue → Rule → Analysis
  → Defenses → Conclusion), with one line per step on what to write.
- **One table per claim or doctrine.** The title gives the rule as a formula, e.g. `==NEGLIGENCE== = duty + breach + …`.
  Then one row per element:
  - `Element`: the test in plain words, with the key term highlighted, and a green label for the
    question the element answers (`~is there a duty?~`)
  - `Here,`: an analysis prompt telling the student which facts to look for and which way they cut
  - cases inline in *italics*, with only what makes the case useful (e.g. "*Carroll Towing*: B < PL"),
    shown as name only or name + one-line holding, per the student's choice
- Separate tables for **defenses**, **exceptions** (majority vs. minority rule), and **remedies**.
- A **Traps** bullet listing the common mistakes for the class.
- Policy arguments go in one short bullet per doctrine, only if the professor tests policy.

Both layouts: **every step or element gets a green label saying what it gives you**; equations and
key terms are bold or yellow; cut filler words, redundant rows, and obvious index tables once space is tight;
**organize by week or doctrine** with dark section headers.

## Files

| File | What |
|---|---|
| `scripts/build.js` | source text → .docx (called by fit.py). `node build.js SRC OUT SIZE COLS`; env `LINEF`, `IMGS`, `PAPER=a4`, `AUTOSUB=0`, `FLAT=1` |
| `scripts/check_setup.py` | detects OS and tools, prints the mode and install commands; `--install` adds the docx package |
| `scripts/fit.py` | build + export PDF (Word on macOS/Windows, or LibreOffice) + measure fill: `fit.py SRC OUT.docx SIZE LINEF IMGS [COLS] [--pages N] [--a4] [--no-autosub] [--converter word\|libreoffice\|none]` |
| `README.md` | install instructions for people (not for Claude) |
| `assets/examples/quant/` | a full one-page economics sheet (layout A), `charts.py` chart template and `img/` |
| `assets/examples/law/` | a short negligence sample (layout B) |

Work in a scratch folder with `sheet.txt` and an `img/` folder next to it (build.js reads images
from `img/` beside the source). Save the final .docx in the class folder the student names.

## Source markup (sheet.txt)

```
T TITLE LINE                      centered bold title
# SECTION                         dark bar section header
R TABLE TITLE [@pct]              table; @pct = width of first column as % (default 17)
| label | text                    2-cell row: bold label + text
| a | b | c                       3+ cells: FIRST row is the gray header row
| one cell                        spans the full width
- bullet text
IMG a.png b.png                   images side by side (from img/)
**bold**                          bold; if it contains "=" it is also highlighted YELLOW
==key term==                      bold + yellow highlight (rule names, tests, holdings)
~text~                            green shading = "what this step / element gives you"
*Case Name*                       italic;  \* = a literal asterisk (e.g. Q\*, P\*L)
_x  _{..}  _(..)                  subscript      ^x  ^{..}  ^(..)  superscript
q1 p2 c1 π1 U1 …                  auto-subscript the 1/2 (turn off with AUTOSUB=0 for non-math classes)
\|                                literal pipe inside a cell
```

## Build and fit loop

1. Write `sheet.txt`. For charts, copy `assets/examples/quant/charts.py` and edit the figures
   (0.84×0.72 in, 400 dpi, 4.3pt font).
2. Run `python3 <skill dir>/scripts/fit.py sheet.txt "<class folder>/<name>.docx" 11 0.96 0.95 6 --pages 1`
   (add `--a4` for A4 paper, `--no-autosub` for non-math classes). It prints the page count and fill
   along with a verdict: FITS / TOO LONG / ROOM LEFT.
   - On macOS with Word, a timing failure is common: just rerun.
   - In BUILD ONLY mode (no converter), it still writes the .docx: ask the student for the page count after they open it.
3. Read the result:
   - **Too many pages:** shrink in this order: cut filler words → cut redundant rows → LINEF down to
     0.92 → SIZE down to 10 → IMGS down.
   - **Room left** (last column ends well short): raise LINEF/SIZE/IMGS, or add missing content
     (check rows, traps, cases, charts).
   - **Target:** exactly the allowed page count, with the last column ≥ ~88% of the page height
     (≈80% if measuring with LibreOffice for a sheet printed from Word).
4. Render it (`pdftoppm -png -r 150 -f 1 -l 1 PDF pg`) and look at it. Check the highlights, italics,
   subscripts, table breaks, and chart legibility.
5. Send the .docx and summarize it in a few lines.

Starting points:
- **Dense quant sheet:** SIZE 11 (5.5pt Arial Narrow), LINEF 0.96, IMGS 0.95, 6 columns.
- **Law sheet:** SIZE 14–16, 4–5 columns, AUTOSUB=0.

## Revisions

- **A rebuild overwrites hand edits** in the .docx. Fold the student's edits into `sheet.txt` first,
  or tell them plainly that their manual changes were replaced.
- When asked to "make room", cut first and shrink the type last.

## Practicing with the sheet

When the student practices problems against the sheet, tag each answer step with where it is on the
sheet (**section › table › row**). Show the sheet's formula or rule, then apply it. Write practice
questions as dense, exam-length fact patterns. Go one step at a time when the student wants to do the work themselves.
