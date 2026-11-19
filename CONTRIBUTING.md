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

## Website page for each skill: `site/<skill>.json`

Every skill should have a matching `site/<skill-name>.json`. The file name must equal the `name` in the skill's `SKILL.md`. The release workflow warns if a skill has no site file, and fails if a site file has no skill or is not valid JSON. The `site/` folder is never included in the downloadable zip.

This repository is public, so this file is public: no private, client or member-only information.

Format (all fields required unless marked optional):

```json
{
  "title": "Crib Sheet",
  "tagline": "One line, under ~120 characters, shown on cards.",
  "summary": "2-3 plain sentences for a law student.",
  "whatItDoes": ["3 to 5 bullets, each starting with a verb."],
  "whenToUse": "When to reach for this skill, and when not to.",
  "examplePrompts": ["1 to 8 prompts a student could paste."],
  "whatChanged": "What the skill fixes versus asking Claude with no skill.",
  "pairsWith": [{ "slug": "other-skill", "note": "Why they work together." }],
  "updated": "YYYY-MM-DD",
  "demo": {
    "type": "text-compare",
    "prompt": "The request shown above both versions.",
    "before": { "label": "Without the skill", "caption": "One line.", "content": "Plain text, \\n for line breaks." },
    "after":  { "label": "With the skill",    "caption": "One line.", "content": "Plain text, \\n for line breaks." }
  }
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
