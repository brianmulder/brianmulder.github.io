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
