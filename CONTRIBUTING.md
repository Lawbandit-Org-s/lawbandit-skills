# Adding or updating a skill (maintainers)

## Folder rules
- One folder per skill, inside the audience folder: `students/`, `professors/`, or `attorneys/`.
- The folder name must match the `name` field in the skill's `SKILL.md` (lowercase, hyphens), e.g. `students/crib-sheet/`.
- Every skill folder needs a `SKILL.md` and a `README.md` with install notes and any tools it needs.
- Do not commit private client data, API keys, or anything meant for members only. Members-only skills go in the private repository.

## Adding a new skill
1. Create the folder in the right audience folder.
2. Create `site/<skill-name>.json` (see "Website page for each skill" below). It powers the skill's page on the website.
3. Add the skill to the catalog table in the root `README.md` and in the audience folder's `README.md`.
   The download link format is `../../releases/download/latest/<skill-name>.zip`.
4. Add a line to `CHANGELOG.md`.
5. Push to `main`. The release workflow builds a zip for every skill and updates the **latest** release automatically.

When you rename or delete a skill, rename or delete its `site/<skill-name>.json` in the same commit.

## Website page for each skill

Every skill has a page on the website. Its text lives in `site/<skill-name>.json` at the **root** of the repo (never inside the skill folder, so it is never in the download zip). The `skills_upload` and `skills_site_set` MCP tools write it for you.

Fields: `title`, `audience`, `tagline` (under ~120 chars), `summary` (2-3 sentences), `updated` (ISO date), `whatItDoes` (3-5 bullets starting with a verb), `whenToUse`, `pairsWith` (`[{slug, note}]`, existing skills only; in the public repo, public skills only), `examplePrompts` (1-8), `whatChanged`, and an optional `demo`.

In the public repo this file is public: no private, client or member-only information.

### Demo type `text-compare`

Two text panels (`before` / `after`), each with `label`, `caption` and `content`. For this type, `after` must be real output of the skill (not invented).

### Demo type `html`

An animated, side-by-side demo drawn with HTML + CSS.

```json
"demo": {
  "type": "html",
  "prompt": "optional, shown above, as the user would type it",
  "height": 380,
  "panels": [
    { "label": "Without the skill", "caption": "one line", "html": "<style>...</style><div>...</div>" },
    { "label": "With the skill", "caption": "one line", "html": "..." }
  ]
}
```

Rules checked by the MCP:

- Panels of an `html` demo may be illustrative (they are drawings, not real output), but the `caption` of each panel must say "Illustrative".
- `panels`: 1 or 2 items. Each `html` is a non-empty string of at most 40,000 characters.
- `height`: number from 200 to 640 (optional, default 380). `label`, `caption`, `prompt` are optional.
- Rejected if the html contains `<script`, `<iframe`, `<object`, `<embed`, `<form`, `<link`, `<meta`, `<base`, `on*=` attributes (onclick, onload...) or `javascript:`. The site strips them too, but the MCP warns you first.
- Secret scan and the public-repo rule (nothing private) still apply.

Rules for writing the HTML:

- HTML + CSS only. Animations must be CSS (`@keyframes`, transitions). JavaScript and SMIL cannot be paused, and scripts do not run.
- Use `animation: ... infinite;` with `animation-fill-mode: both`. Total loop between 6 and 10 seconds. Stagger elements with `animation-delay` (e.g. `style="--i:3"` and `animation-delay: calc(var(--i)*.7s)`).
- Design so that 90% of the loop looks finished and readable: with "reduced motion" the site shows that frozen point.
- Colors ONLY with the site variables, so they work in light and dark: `--bg`, `--fg`, `--body`, `--muted`, `--muted-fg`, `--border`, `--accent`, `--link`, `--mark-bg`, `--mark-fg`, `--tag-bg`, `--tag-fg`. For red/green status you may use fixed colors.
- Font: system default; the class `mono` applies monospace.
- Images only as `data:` URIs or https. No external fonts or CSS.
- The iframe background is transparent. The body has 16px padding and `overflow: hidden`.

Example (the `crib-sheet` demo): 

```json
"demo": {
  "type": "html",
  "prompt": "Make me a 1-page crib sheet for my Torts exam on negligence.",
  "height": 340,
  "panels": [
    {
      "label": "Without the skill",
      "caption": "Illustrative: the text keeps going past the page limit.",
      "html": "<style>.pg{height:100%;border:1px solid var(--border);border-radius:8px;padding:14px 16px;position:relative;overflow:hidden}.ln{height:7px;border-radius:4px;background:var(--border);margin:11px 0;transform-origin:left;opacity:0;animation:ln 9s infinite both;animation-delay:calc(var(--i)*.22s)}@keyframes ln{0%{opacity:0;transform:scaleX(0)}6%{opacity:1;transform:scaleX(1)}88%{opacity:1}96%,100%{opacity:0}}.limit{position:absolute;left:0;right:0;top:62%;border-top:2px dashed #e5484d;animation:lim 9s infinite both}.tag{position:absolute;right:10px;top:calc(62% + 6px);font:600 11px ui-monospace,monospace;color:#e5484d;animation:lim 9s infinite both}@keyframes lim{0%,35%{opacity:0}45%,88%{opacity:1}96%,100%{opacity:0}}</style><div class=\"pg\"><div class=\"ln\" style=\"--i:0;width:92%\"></div><div class=\"ln\" style=\"--i:1;width:78%\"></div><div class=\"ln\" style=\"--i:2;width:85%\"></div><div class=\"ln\" style=\"--i:3;width:96%\"></div><div class=\"ln\" style=\"--i:4;width:74%\"></div><div class=\"ln\" style=\"--i:5;width:88%\"></div><div class=\"ln\" style=\"--i:6;width:81%\"></div><div class=\"ln\" style=\"--i:7;width:93%\"></div><div class=\"ln\" style=\"--i:8;width:77%\"></div><div class=\"ln\" style=\"--i:9;width:90%\"></div><div class=\"ln\" style=\"--i:10;width:83%\"></div><div class=\"ln\" style=\"--i:11;width:95%\"></div><div class=\"ln\" style=\"--i:12;width:72%\"></div><div class=\"ln\" style=\"--i:13;width:86%\"></div><div class=\"ln\" style=\"--i:14;width:91%\"></div><div class=\"ln\" style=\"--i:15;width:79%\"></div><div class=\"limit\"></div><div class=\"tag\">PAGE LIMIT</div></div>"
    },
    {
      "label": "With the skill",
      "caption": "Illustrative: a simplified version of the real sheet. Every element gets a row.",
      "html": "<style>.pg{height:100%;border:1px solid var(--border);border-radius:8px;padding:12px 14px;overflow:hidden}.r{display:grid;grid-template-columns:70px 1fr;gap:8px;padding:5px 4px;border-radius:4px;opacity:0;transform:translateY(8px);animation:row 9s infinite both;animation-delay:calc(var(--i)*.7s)}.r b{color:var(--fg)}.r.h{background:var(--muted);font-style:italic;color:var(--muted-fg)}.r.t{display:block;border-bottom:1px solid var(--border);margin-bottom:6px;font-weight:600}mark{background:var(--mark-bg);color:var(--mark-fg);padding:0 2px;border-radius:2px}.g{background:var(--tag-bg);color:var(--tag-fg);font-size:11px;padding:0 4px;border-radius:2px;margin-left:4px}@keyframes row{0%{opacity:0;transform:translateY(8px)}5%{opacity:1;transform:none}86%{opacity:1;transform:none}95%,100%{opacity:0}}</style><div class=\"pg\"><div class=\"r t\" style=\"--i:0\"><mark>NEGLIGENCE</mark> = duty + breach + cause + damages</div><div class=\"r\" style=\"--i:1\"><b>Duty</b><span>reasonable care owed <span class=\"g\">is there a duty?</span></span></div><div class=\"r h\" style=\"--i:2\"><b>Here,</b><span>Did D's conduct create the risk?</span></div><div class=\"r\" style=\"--i:3\"><b>Breach</b><span><mark>B &lt; P × L</mark> (<i>Carroll Towing</i>) <span class=\"g\">did D fall short?</span></span></div><div class=\"r\" style=\"--i:4\"><b>Cause</b><span><mark>but-for</mark>; substantial factor if several</span></div><div class=\"r\" style=\"--i:5\"><b>Damages</b><span>actual harm required <span class=\"g\">what P recovers</span></span></div></div>"
    }
  ]
}
```


Rules:
- `whatItDoes`: 3 to 5 bullets. `tagline`: one line. `summary`: 2-3 sentences. Plain English, no marketing filler.
- `pairsWith` is optional and defaults to `[]`. Each `slug` must be an existing skill (in the public repo, only public skills).
- `updated` is an ISO date. Bump it whenever the skill changes.
- `demo.after` must be real output from the skill, not an invented sample.
- `demo.before` should be real output from Claude without the skill. If it is illustrative, say so in its caption.
- `demo.after.content` may use the sheet markup (`==x==` yellow, `~x~` green label, `*x*` italic). The website renders it.

## Versioning
Note every change in `CHANGELOG.md` under the skill's name with a version number (e.g. `crib-sheet 1.1.0`).
