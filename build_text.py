"""Build public text from the same professional content as the public PDFs."""

from html import unescape
from pathlib import Path
import re
import runpy
import sys
import textwrap
import unicodedata

ROOT = Path(__file__).resolve().parent
sys.argv = [str(ROOT.parent / 'cv' / 'build_cv.py'), '--public']
cv = runpy.run_path(sys.argv[0])


def ascii_text(value):
    value = re.sub(r'<[^>]+>', '', value)
    value = unescape(value)
    for old, new in {'\u2019': "'", '\u2018': "'", '\u201c': '"',
                     '\u201d': '"', '\u2013': '-', '\u2014': ' - ',
                     '\u2022': '-', '\u00a0': ' '}.items():
        value = value.replace(old, new)
    return unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode()


def paragraphs(items):
    for item in items:
        if hasattr(item, 'text'):
            yield item
        elif hasattr(item, '_content'):
            yield from paragraphs(item._content)


groups = {}
current = None
for para in paragraphs(cv['opening_page']()):
    if para.style.name == 'section':
        current = ascii_text(para.text)
        groups[current] = []
    elif current:
        groups[current].append(ascii_text(para.text))

employment = []
cv['employment_page'](employment)
roles = list(paragraphs(employment))[1:]
lines = [
    'Brian Mulder'.ljust(72 - len('Curriculum Vitae')) + 'Curriculum Vitae',
    'Independent engineering & consulting'.ljust(72 - len('October 2026')) + 'October 2026',
    '',
    '                              BRIAN MULDER',
    'Software Engineer'.center(72).rstrip(),
    '',
    '   Sydney, Australia | Australian permanent resident',
    '   https://www.brianmulder.com/',
    '   https://www.linkedin.com/in/brianmulder-tech/',
    '',
    'Contents',
    '',
    '   1. Profile',
    '   2. Selected projects and capabilities',
    '   3. Technical skill set',
    '   4. Employment and project detail',
    '   5. Education',
    '   6. Contact and links',
]


def heading(text):
    lines.extend(['', '', text, ''])


def body(text):
    lines.extend(textwrap.wrap(text, width=72, initial_indent='   ',
                              subsequent_indent='     ' if text.startswith('- ') else '   ',
                              break_long_words=False, break_on_hyphens=False))
    lines.append('')


for title, key in [('1. Profile', 'PROFILE'),
                   ('2. Selected projects and capabilities', 'SELECTED PROJECTS & CAPABILITIES'),
                   ('3. Technical skill set', 'TECHNICAL SKILL SET')]:
    heading(title)
    for text in groups[key]:
        body(text)

heading('4. Employment and project detail')
role_number = 0
for para in roles:
    if para.style.name == 'role':
        role_number += 1
        lines.append('')
        body(f'4.{role_number}. ' + ascii_text(para.text))
    else:
        body(ascii_text(para.text))

heading('5. Education')
for text in groups['EDUCATION']:
    body(text)
heading('6. Contact and links')
for text in ['Website: https://www.brianmulder.com/',
             'Email: hello@mail.brianmulder.com',
             'LinkedIn: https://www.linkedin.com/in/brianmulder-tech/',
             'GitHub: https://github.com/brianmulder',
             'Tessur: https://tessur.com/',
             'Secure Measure: https://www.securemeasure.com.au/']:
    body(text)

output = '\n'.join(lines).rstrip() + '\n'
assert output.isascii()
assert max(map(len, output.splitlines())) <= 72
(ROOT / 'cv.txt').write_text(output, encoding='ascii')

profile = '''# brian mulder

> software engineer & consultant. co-founder of tessur. sydney, australia.

i design and build software for clients. nuts about ai and agents.
previously Amazon Web Services, CBA, and Optus. available for projects, contracts, and
ai workshops.

at tessur, we're building an on-device assistant to help people and their
agents check actions against their context and what matters to them.
i also run ai adoption workshops through secure measure for engineering
teams as they work through ai-assisted development.

contact: hello@mail.brianmulder.com
updated: 2 october 2026. confirm availability and scope directly.

## links

- [cv in plain text](https://www.brianmulder.com/cv.txt): career history and skills.
- [website](https://www.brianmulder.com/)
- [tessur](https://tessur.com/)
- [secure measure](https://www.securemeasure.com.au/)
- [linkedin](https://www.linkedin.com/in/brianmulder-tech/)
- [github](https://github.com/brianmulder)

## printable cv

- [one-page pdf](https://www.brianmulder.com/Brian-Mulder-CV.pdf)
- [detailed pdf](https://www.brianmulder.com/Brian-Mulder-CV-Detailed.pdf)
'''
assert profile.isascii()
for name in ['llms.txt', 'llm.txt']:
    (ROOT / name).write_text(profile, encoding='ascii')
print('Built cv.txt, llms.txt and llm.txt (identical alias).')
