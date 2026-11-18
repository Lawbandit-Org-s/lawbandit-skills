# Adding or updating a skill (maintainers)

## Folder rules
- One folder per skill, inside the audience folder: `students/`, `professors/`, or `attorneys/`.
- The folder name must match the `name` field in the skill's `SKILL.md` (lowercase, hyphens), e.g. `students/crib-sheet/`.
- Every skill folder needs a `SKILL.md` and a `README.md` with install notes and any tools it needs.
- Do not commit private client data, API keys, or anything meant for members only. Members-only skills go in the private repository.

## Adding a new skill
1. Create the folder in the right audience folder.
2. Add the skill to the catalog table in the root `README.md` and in the audience folder's `README.md`.
   The download link format is `../../releases/download/latest/<skill-name>.zip`.
3. Add a line to `CHANGELOG.md`.
4. Push to `main`. The release workflow builds a zip for every skill and updates the **latest** release automatically.

## Versioning
Note every change in `CHANGELOG.md` under the skill's name with a version number (e.g. `crib-sheet 1.1.0`).
