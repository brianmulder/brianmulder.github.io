# Brian Mulder

Static personal website at https://www.brianmulder.com/.
GitHub Pages serves the root of the `main` branch. Brian approved publication
on 2 October 2026.

## Public text

- `cv.txt`: primary CV, ASCII, maximum 72 columns, numbered sections.
- `llms.txt`: public professional profile and links for agents.
- `llm.txt`: identical compatibility copy for the explicitly requested URL.
- PDFs remain optional printable formats.

Generate with `python build_text.py` in a runtime with ReportLab.
The CV draws from `../cv/build_cv.py` in public mode, so the text and PDF
versions use the same career content. The agent profile is maintained in
`build_text.py`. Run that script after editing either source.

The agent profile follows the proposal at https://llmstxt.org/.
No private contact details or regular workplace location should appear.
Use the simple public title Software Engineer in the website, CVs and metadata.

## Cloud development

The canonical source is `brianmulder/brianmulder.github.io` on `main`.
The canonical development home is the saved **brianmulder.com** Codex Cloud
environment. Start a task there and enter the mounted repository directory
(`/workspace/brianmulder.github.io` in the verified runtime). The runtime may
provide a working branch rather than `main`; check HEAD and status first.
No package dependencies, local build, secrets or custom Actions workflow are
needed to maintain and deploy the committed static site.

```sh
git status --short --branch
git rev-parse HEAD
python3 validate_site.py
git diff --check
```

For an optional local preview, run `python3 -m http.server 8000 --bind 127.0.0.1`
from the repository root. The validator is offline and uses Python's standard
library; it does not check remote links, visual layout or live deployment.

Publish through the connected GitHub integration: create a dedicated branch
from current `main`, commit only the reviewed changes, open a pull request and
merge after required review. GitHub Pages publishes root `/` from `main`;
there is no separate site upload command. Check the Pages deployment for the
merged commit, then verify `https://www.brianmulder.com/`, `/cv.txt`, `/llms.txt`
and `/llm.txt` against that commit. A successful commit alone is not proof of
a successful deployment. Environment publication is a separate platform
action; these instructions do not establish whether its UI configuration is
draft or published.

For rollback, revert the migration or content commit through a new reviewed
pull request; do not reset or force-push `main`. Verify Pages again after the
revert. Legacy laptop checkouts remain reference/archive copies, not a second
active development home. Leave their uncommitted work intact; any future
local pointer should name this repository and cloud environment.

## Optional asset regeneration dependencies

Static maintenance is self-contained; asset regeneration is not.
`build_text.py` requires ReportLab and the absent sibling `../cv/build_cv.py`
public-mode source. The PDF regeneration source is not in this repository.
`build_social_card.py` requires Pillow and `C:/Windows/Fonts/arial*.ttf`.
Do not run these generators in the cloud environment or replace the committed
CVs, PDFs or social card with substitutes.

The minimal later portability fix is to review and extract only public CV
source into this repository, pin generator dependencies, and supply an
explicit licensed portable font path. Keep private CV data outside the repo.
That is separate work; the existing committed assets remain usable as-is.
