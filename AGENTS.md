# Website maintenance

Canonical repository: `brianmulder/brianmulder.github.io`, branch `main`.
Canonical execution home: the saved **brianmulder.com** Codex Cloud environment.
GitHub Pages serves the repository root; no package installation or build is needed.

- Read README.md before editing. Preserve unrelated public content and assets.
- Run `python3 validate_site.py` and `git diff --check` before committing.
- Use the connected GitHub integration for branches, commits and pull requests.
  Do not assume shell Git has write credentials. Never force-push main.
- Merge only within the authorized task scope and any required repository review.
  Verify the resulting Pages deployment and public URLs before claiming success.
- Do not run the CV/text generator: its source is absent here. Do not import
  private CV material or secrets. Social-card review generation is supported
  with bundled licensed fonts; use --output to avoid replacing published assets.
- Local checkouts are legacy/reference copies. Do not delete or overwrite them;
  direct future development to the cloud environment and canonical repository.
