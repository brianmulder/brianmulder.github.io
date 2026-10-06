"""Build printable public CVs from cv.txt; maintain llm.txt compatibility copy.

Only committed public sources are read. No sibling/private CV is imported.
"""
from html import escape
from pathlib import Path
import re

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate

ROOT = Path(__file__).resolve().parent
INK = colors.HexColor('#24292c')
for name, filename in [('CVSans', 'LiberationSans-Regular.ttf'),
                       ('CVSans-Bold', 'LiberationSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(ROOT / 'assets' / 'fonts' / filename)))
pdfmetrics.registerFontFamily('CVSans', normal='CVSans', bold='CVSans-Bold',
                              italic='CVSans', boldItalic='CVSans-Bold')
STYLES = {
    'name': ParagraphStyle('name', fontName='CVSans-Bold', fontSize=25,
                           leading=29, textColor=INK, spaceAfter=2),
    'subtitle': ParagraphStyle('subtitle', fontName='CVSans', fontSize=12,
                               leading=15, textColor=INK, spaceAfter=5),
    'contact': ParagraphStyle('contact', fontName='CVSans', fontSize=9.5,
                              leading=12, textColor=INK, spaceAfter=3),
    'section': ParagraphStyle('section', fontName='CVSans-Bold', fontSize=10.5,
                              leading=13, textColor=INK, spaceBefore=7, spaceAfter=5,
                              keepWithNext=True),
    'body': ParagraphStyle('body', fontName='CVSans', fontSize=10.5,
                           leading=13, textColor=INK, spaceAfter=3.8),
    'role': ParagraphStyle('role', fontName='CVSans-Bold', fontSize=10.5,
                           leading=13, textColor=INK, spaceBefore=7, spaceAfter=4,
                           keepWithNext=True),
}


def markup(text):
    """Escape source prose and make explicit public URLs clickable."""
    chunks = re.split(r'(https://[^\s]+)', text)
    return ''.join(f'<link href="{escape(s, quote=True)}" color="#24292c">'
                   f'{escape(s)}</link>' if s.startswith('https://') else escape(s)
                   for s in chunks)


def para(text, kind='body'):
    if text.startswith('- '):
        text = '\u2022 ' + text[2:]
        if ' | ' in text and ' - ' in text:
            label, rest = text.split(' - ', 1)
            return Paragraph('<b>' + markup(label) + '</b> - ' + markup(rest), STYLES[kind])
    return Paragraph(markup(text), STYLES[kind])


def read_sections():
    text = (ROOT / 'cv.txt').read_text(encoding='ascii')
    if max(map(len, text.splitlines())) > 72:
        raise ValueError('cv.txt exceeds 72 columns')
    sections = {}
    current = None
    for block in re.split(r'\n\s*\n', text.strip()):
        block = ' '.join(line.strip() for line in block.splitlines())
        if re.match(r'^[1-6]\. ', block):
            current = block.split('.')[0]
            sections[current] = []
        elif current:
            sections[current].append(block)
    if set(sections) != set('123456'):
        raise ValueError('Expected six numbered public CV sections')
    return sections


def opening(sections):
    story = [para('BRIAN MULDER', 'name'), para('Software Engineer', 'subtitle')]
    story.append(Paragraph('<link href="mailto:hello@mail.brianmulder.com">'
                           'hello@mail.brianmulder.com</link>   |   '
                           '<link href="https://www.brianmulder.com/">brianmulder.com</link>'
                           '   |   Sydney', STYLES['contact']))
    story.append(Paragraph('<link href="https://www.linkedin.com/in/brianmulder-tech/">'
                           'linkedin.com/in/brianmulder-tech</link>   |   '
                           '<link href="https://github.com/brianmulder">github.com/brianmulder</link>'
                           '   |   Australian permanent resident', STYLES['contact']))
    for title, key in [('PROFILE', '1'), ('SELECTED PROJECTS & CAPABILITIES', '2'),
                       ('TECHNICAL SKILL SET', '3')]:
        story.append(para(title, 'section'))
        story.extend(para(text) for text in sections[key])
    story.append(para('CAREER AT A GLANCE', 'section'))
    roles = [re.sub(r'^4\.\d+\. ', '', text) for text in sections['4']
             if re.match(r'^4\.\d+\. ', text)]
    for text in roles:
        if text.startswith('Optus -'):
            periods = next(item for item in sections['4']
                           if item.startswith('- Technical Product Management:'))
            match = re.fullmatch(
                r'- Technical Product Management: (.+)\. Engineering Capability: (.+)\.',
                periods)
            if not match:
                raise ValueError('Expected two dated Optus role periods in cv.txt')
            for title, dates in zip(('Technical Product Management', 'Engineering Capability'),
                                    match.groups()):
                story.append(para(f'Optus - Associate Director, {title} | {dates}', 'contact'))
        elif text.startswith('Commonwealth Bank -'):
            story.append(para('CBA - Scalable Systems Engineer; Engineering Lead; Tower Lead | Sep 2016 - Jan 2023', 'contact'))
        else:
            story.append(para(text, 'contact'))
    story.append(para('EDUCATION', 'section'))
    story.extend(para(text, 'contact') for text in sections['5'])
    return story


def employment(sections):
    story = [para('BRIAN MULDER | EMPLOYMENT & PROJECT DETAIL', 'section')]
    for text in sections['4']:
        role = re.match(r'^4\.\d+\. ', text)
        story.append(para(text[role.end():] if role else text, 'role' if role else 'body'))
    return story


def footer(canvas, doc):
    canvas.setTitle('Brian Mulder - Curriculum Vitae')
    canvas.setAuthor('Brian Mulder')
    canvas.setFont('CVSans', 9)
    canvas.setFillColor(colors.HexColor('#626a6d'))
    canvas.drawRightString(A4[0] - 42, 24, str(doc.page))


def public_canvas(*args, **kwargs):
    # Avoid adding an unused, unembedded Helvetica default font resource.
    kwargs['initialFontName'] = 'CVSans'
    return Canvas(*args, **kwargs)


def build():
    sections = read_sections()
    for name, detailed in [('Brian-Mulder-CV.pdf', False),
                           ('Brian-Mulder-CV-Detailed.pdf', True)]:
        story = opening(sections)
        if detailed:
            story += [PageBreak()] + employment(sections)
        doc = SimpleDocTemplate(str(ROOT / name), pagesize=A4, leftMargin=42,
                                rightMargin=42, topMargin=34, bottomMargin=42,
                                pageCompression=1, invariant=1)
        doc.build(story, onFirstPage=footer, onLaterPages=footer,
                  canvasmaker=public_canvas)
        if doc.page != (2 if detailed else 1):
            raise ValueError(f'{name}: unexpected pagination ({doc.page})')
    profile = (ROOT / 'llms.txt').read_text(encoding='ascii')
    (ROOT / 'llm.txt').write_text(profile, encoding='ascii')
    print('Built both public PDFs from cv.txt; copied llms.txt to llm.txt.')


if __name__ == '__main__':
    build()
