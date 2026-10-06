# Brian Mulder

Static personal website at https://www.brianmulder.com/.
GitHub Pages serves the root of the `main` branch. Brian approved publication
on 2 October 2026. The 6 October 2026 résumé refresh is prepared for review;
that earlier approval does not authorize publishing this refresh.

## Public text

- `cv.txt`: primary CV, ASCII, maximum 72 columns, numbered sections.
- `llms.txt`: public professional profile and links for agents.
- `llm.txt`: identical compatibility copy for the explicitly requested URL.
- PDFs remain optional printable formats.

The public sources are `cv.txt` (career content) and `llms.txt` (agent profile).
Edit those files, then run `python3 build_text.py` to regenerate both PDFs
and copy `llms.txt` to its `llm.txt` compatibility alias. The generator reads
only committed public material; it has no private sibling-source dependency.
Install its pinned dependency with `python3 -m pip install -r requirements-cv.txt`.
Render and inspect both PDFs after content changes; their intended lengths are
one page and two pages. Run `python3 validate_site.py` and `git diff --check`.

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
`build_text.py` uses `ReportLab==4.4.9`, pinned in `requirements-cv.txt`.
Its public source is `cv.txt`; the generator also maintains the `llm.txt` alias
from `llms.txt`. PDF generation embeds bundled Liberation Sans regular and bold fonts to
match the website's Arial/Helvetica body and name typography. It keeps the
A4 layout and checks the one-page/two-page pagination. Font provenance and
SIL OFL license are in `assets/fonts/README.md` and `LICENSE.txt`.
`build_social_card.py` uses bundled Liberation Sans under SIL OFL 1.1
(see `assets/fonts/LICENSE.txt` and provenance in `assets/fonts/README.md`).
Its supported cloud build uses Python 3.12.14 and `Pillow==12.3.0`, pinned
in `requirements-social-card.txt`; these are not historical Windows versions.
The cloud runtime already supplies that Pillow version.

Generate a review copy without replacing the published card:

```sh
python3 build_social_card.py --output /tmp/social-card-review.png
python3 test_social_card.py
```

`--font-dir` explicitly selects a directory containing LiberationSans-Regular.ttf
and LiberationSans-Bold.ttf; no platform font fallback is used. Review the
new image visually before intentionally replacing `social-card.png`.
Keep private CV data outside the repository. The public CV build is now
self-contained; the social-card font dependency is bundled with its license.
