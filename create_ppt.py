"""Generate the WorldWithWeb Demo Session PowerPoint."""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Brand colors
DARK_BG = RGBColor(0x1A, 0x1A, 0x2E)
ACCENT_BLUE = RGBColor(0x00, 0xB4, 0xD8)
ACCENT_GREEN = RGBColor(0x00, 0xE6, 0x76)
ACCENT_ORANGE = RGBColor(0xFF, 0x9F, 0x1C)
ACCENT_PURPLE = RGBColor(0xBB, 0x86, 0xFC)
ACCENT_RED = RGBColor(0xFF, 0x45, 0x6E)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY = RGBColor(0xCC, 0xCC, 0xCC)
MID_GRAY = RGBColor(0x99, 0x99, 0x99)
DARK_CARD = RGBColor(0x25, 0x25, 0x40)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
W = prs.slide_width
H = prs.slide_height


def set_slide_bg(slide, color=DARK_BG):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_shape(slide, left, top, width, height, fill_color, border_color=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.5)
    else:
        shape.line.fill.background()
    return shape


def add_text_box(slide, left, top, width, height):
    return slide.shapes.add_textbox(left, top, width, height)


def set_text(tf, text, size=18, color=WHITE, bold=False, alignment=PP_ALIGN.LEFT, font_name="Calibri"):
    tf.clear()
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    return p


def add_paragraph(tf, text, size=18, color=WHITE, bold=False, alignment=PP_ALIGN.LEFT, space_before=Pt(6), font_name="Calibri"):
    p = tf.add_paragraph()
    p.text = text
    p.font.size = Pt(size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    if space_before:
        p.space_before = space_before
    return p


def add_bullet_slide(slide, title_text, bullets, accent_color=ACCENT_BLUE):
    """Helper for slides with a title and bullet points."""
    set_slide_bg(slide)

    # Accent bar
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(0.15), H)
    bar.fill.solid()
    bar.fill.fore_color.rgb = accent_color
    bar.line.fill.background()

    # Title
    tb = add_text_box(slide, Inches(0.8), Inches(0.5), Inches(11), Inches(1))
    set_text(tb.text_frame, title_text, size=40, bold=True, color=WHITE)

    # Bullets
    tb2 = add_text_box(slide, Inches(1.2), Inches(1.8), Inches(10.5), Inches(5))
    tf = tb2.text_frame
    tf.word_wrap = True
    for i, bullet in enumerate(bullets):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
            p.space_before = Pt(14)
        p.text = bullet
        p.font.size = Pt(24)
        p.font.color.rgb = WHITE
        p.font.name = "Calibri"
        p.level = 0


# =====================================================
# SLIDE 1 - Title
# =====================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
set_slide_bg(slide)

# Accent line
line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.5), Inches(2.8), Inches(4.3), Pt(4))
line.fill.solid()
line.fill.fore_color.rgb = ACCENT_BLUE
line.line.fill.background()

tb = add_text_box(slide, Inches(1.5), Inches(1.2), Inches(10.3), Inches(1.5))
set_text(tb.text_frame, "WorldWithWeb", size=56, bold=True, color=WHITE, alignment=PP_ALIGN.CENTER)

tb2 = add_text_box(slide, Inches(1.5), Inches(3.2), Inches(10.3), Inches(1.5))
set_text(tb2.text_frame, "Learn Tech. Build Real Things.", size=36, color=ACCENT_BLUE, alignment=PP_ALIGN.CENTER)

tb3 = add_text_box(slide, Inches(1.5), Inches(5.0), Inches(10.3), Inches(1))
set_text(tb3.text_frame, "Demo Session  |  Classes 8th - 10th", size=22, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)


# =====================================================
# SLIDE 2 - Quick Question
# =====================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

tb = add_text_box(slide, Inches(1.5), Inches(1.5), Inches(10.3), Inches(2))
set_text(tb.text_frame, "Quick Question...", size=48, bold=True, color=ACCENT_GREEN, alignment=PP_ALIGN.CENTER)

tb2 = add_text_box(slide, Inches(1.5), Inches(3.5), Inches(10.3), Inches(2))
set_text(tb2.text_frame, '"What did you use AI for today?"', size=40, color=WHITE, alignment=PP_ALIGN.CENTER)

tb3 = add_text_box(slide, Inches(2), Inches(5.5), Inches(9.3), Inches(1))
set_text(tb3.text_frame, "ChatGPT for homework?    Image generators?    Gaming AI?", size=22, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)


# =====================================================
# SLIDE 3 - The Gap
# =====================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

tb = add_text_box(slide, Inches(1.5), Inches(0.8), Inches(10.3), Inches(1.5))
set_text(tb.text_frame, "You're already using AI.", size=44, bold=True, color=WHITE, alignment=PP_ALIGN.CENTER)

tb2 = add_text_box(slide, Inches(1.5), Inches(2.5), Inches(10.3), Inches(1.5))
set_text(tb2.text_frame, "But there's a difference between", size=32, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)

# Two cards
card1 = add_shape(slide, Inches(2.5), Inches(4), Inches(3.5), Inches(2), DARK_CARD, ACCENT_ORANGE)
tb_c1 = add_text_box(slide, Inches(2.5), Inches(4.3), Inches(3.5), Inches(1.5))
set_text(tb_c1.text_frame, "Using a tool", size=30, bold=True, color=ACCENT_ORANGE, alignment=PP_ALIGN.CENTER)

card2 = add_shape(slide, Inches(7.3), Inches(4), Inches(3.5), Inches(2), DARK_CARD, ACCENT_GREEN)
tb_c2 = add_text_box(slide, Inches(7.3), Inches(4.3), Inches(3.5), Inches(1.5))
set_text(tb_c2.text_frame, "Building one", size=30, bold=True, color=ACCENT_GREEN, alignment=PP_ALIGN.CENTER)


# =====================================================
# SLIDE 4 - Live Demo Title
# =====================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

tb = add_text_box(slide, Inches(1.5), Inches(2), Inches(10.3), Inches(2))
set_text(tb.text_frame, "Let me show you what I built.", size=48, bold=True, color=WHITE, alignment=PP_ALIGN.CENTER)

tb2 = add_text_box(slide, Inches(1.5), Inches(4.2), Inches(10.3), Inches(1))
set_text(tb2.text_frame, "7 projects. All Python. All real.", size=28, color=ACCENT_BLUE, alignment=PP_ALIGN.CENTER)

tb3 = add_text_box(slide, Inches(1.5), Inches(5.5), Inches(10.3), Inches(1))
set_text(tb3.text_frame, "[ LIVE DEMO ]", size=24, color=ACCENT_GREEN, bold=True, alignment=PP_ALIGN.CENTER)


# =====================================================
# SLIDE 5 - Demo: Network Sentinel
# =====================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, W, Inches(0.08))
bar.fill.solid()
bar.fill.fore_color.rgb = ACCENT_RED
bar.line.fill.background()

tb = add_text_box(slide, Inches(0.8), Inches(0.4), Inches(3), Inches(0.6))
set_text(tb.text_frame, "DEMO 1", size=16, color=ACCENT_RED, bold=True)

tb2 = add_text_box(slide, Inches(0.8), Inches(1), Inches(11), Inches(1.2))
set_text(tb2.text_frame, "Network Sentinel", size=44, bold=True, color=WHITE)

tb3 = add_text_box(slide, Inches(0.8), Inches(2.5), Inches(10), Inches(1))
set_text(tb3.text_frame, '"This scans your own machine for open ports --\nthe same way hackers find entry points."', size=26, color=LIGHT_GRAY)

tb4 = add_text_box(slide, Inches(0.8), Inches(4.5), Inches(10), Inches(2))
tf = tb4.text_frame
tf.word_wrap = True
set_text(tf, "What it does:", size=20, color=ACCENT_RED, bold=True)
add_paragraph(tf, "Scans network ports on any machine", size=22, color=WHITE)
add_paragraph(tf, "Shows which doors are open to attackers", size=22, color=WHITE)
add_paragraph(tf, "Real tool. Real cybersecurity.", size=22, color=WHITE)


# =====================================================
# SLIDE 6 - Demo: Password Fortress
# =====================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, W, Inches(0.08))
bar.fill.solid()
bar.fill.fore_color.rgb = ACCENT_ORANGE
bar.line.fill.background()

tb = add_text_box(slide, Inches(0.8), Inches(0.4), Inches(3), Inches(0.6))
set_text(tb.text_frame, "DEMO 2", size=16, color=ACCENT_ORANGE, bold=True)

tb2 = add_text_box(slide, Inches(0.8), Inches(1), Inches(11), Inches(1.2))
set_text(tb2.text_frame, "Password Fortress", size=44, bold=True, color=WHITE)

tb3 = add_text_box(slide, Inches(0.8), Inches(2.5), Inches(10), Inches(1.2))
set_text(tb3.text_frame, '"Let\'s crack a password. Right now."', size=28, color=LIGHT_GRAY)

# Two cards
card1 = add_shape(slide, Inches(1), Inches(4), Inches(4.5), Inches(2.5), DARK_CARD, ACCENT_ORANGE)
tb_c = add_text_box(slide, Inches(1.3), Inches(4.3), Inches(4), Inches(2))
tf = tb_c.text_frame
set_text(tf, 'Password: "abc"', size=22, bold=True, color=ACCENT_ORANGE)
add_paragraph(tf, "Cracked in 0.001 seconds", size=20, color=ACCENT_RED)
add_paragraph(tf, "Your Instagram is gone.", size=18, color=LIGHT_GRAY)

card2 = add_shape(slide, Inches(6.5), Inches(4), Inches(5.5), Inches(2.5), DARK_CARD, ACCENT_GREEN)
tb_c2 = add_text_box(slide, Inches(6.8), Inches(4.3), Inches(5), Inches(2))
tf2 = tb_c2.text_frame
set_text(tf2, 'Password: "X#9kL2$m"', size=22, bold=True, color=ACCENT_GREEN)
add_paragraph(tf2, "Would take years to crack", size=20, color=ACCENT_GREEN)
add_paragraph(tf2, "This is why password strength matters.", size=18, color=LIGHT_GRAY)


# =====================================================
# SLIDE 7 - Demo: Quiz Master
# =====================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, W, Inches(0.08))
bar.fill.solid()
bar.fill.fore_color.rgb = ACCENT_BLUE
bar.line.fill.background()

tb = add_text_box(slide, Inches(0.8), Inches(0.4), Inches(3), Inches(0.6))
set_text(tb.text_frame, "DEMO 3", size=16, color=ACCENT_BLUE, bold=True)

tb2 = add_text_box(slide, Inches(0.8), Inches(1), Inches(11), Inches(1.2))
set_text(tb2.text_frame, "AI Quiz Master", size=44, bold=True, color=WHITE)

tb3 = add_text_box(slide, Inches(0.8), Inches(2.5), Inches(10), Inches(1))
set_text(tb3.text_frame, '"Pick ANY topic. The AI generates a quiz in real-time."', size=26, color=LIGHT_GRAY)

tb4 = add_text_box(slide, Inches(0.8), Inches(4), Inches(10), Inches(2))
tf = tb4.text_frame
set_text(tf, "What's happening behind the scenes:", size=20, color=ACCENT_BLUE, bold=True)
add_paragraph(tf, "Python sends a prompt to an AI model", size=22, color=WHITE)
add_paragraph(tf, "AI generates questions in JSON format", size=22, color=WHITE)
add_paragraph(tf, "Streamlit renders it as a web app", size=22, color=WHITE)
add_paragraph(tf, '"I built this. The AI is the brain, but I wrote the body."', size=22, color=ACCENT_GREEN, bold=True)


# =====================================================
# SLIDE 8 - Demo: Chatbot + Story Forge
# =====================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, W, Inches(0.08))
bar.fill.solid()
bar.fill.fore_color.rgb = ACCENT_PURPLE
bar.line.fill.background()

tb = add_text_box(slide, Inches(0.8), Inches(0.4), Inches(3), Inches(0.6))
set_text(tb.text_frame, "DEMOS 4 & 5", size=16, color=ACCENT_PURPLE, bold=True)

tb2 = add_text_box(slide, Inches(0.8), Inches(1), Inches(11), Inches(1.2))
set_text(tb2.text_frame, "AI Chatbot  &  Story Forge", size=44, bold=True, color=WHITE)

# Two cards side by side
card1 = add_shape(slide, Inches(0.8), Inches(2.8), Inches(5.5), Inches(3.5), DARK_CARD, ACCENT_PURPLE)
tb_c = add_text_box(slide, Inches(1.1), Inches(3.1), Inches(5), Inches(3))
tf = tb_c.text_frame
set_text(tf, "AI Chatbot", size=26, bold=True, color=ACCENT_PURPLE)
add_paragraph(tf, '"Looks like ChatGPT?"', size=20, color=LIGHT_GRAY)
add_paragraph(tf, "", size=10)
add_paragraph(tf, "But I control:", size=20, color=WHITE)
add_paragraph(tf, "  Which AI model it uses", size=20, color=WHITE)
add_paragraph(tf, "  What personality it has", size=20, color=WHITE)
add_paragraph(tf, "  What data it can see", size=20, color=WHITE)

card2 = add_shape(slide, Inches(7), Inches(2.8), Inches(5.5), Inches(3.5), DARK_CARD, ACCENT_GREEN)
tb_c2 = add_text_box(slide, Inches(7.3), Inches(3.1), Inches(5), Inches(3))
tf2 = tb_c2.text_frame
set_text(tf2, "Story Forge", size=26, bold=True, color=ACCENT_GREEN)
add_paragraph(tf2, '"Choose your adventure."', size=20, color=LIGHT_GRAY)
add_paragraph(tf2, "", size=10)
add_paragraph(tf2, "You pick a genre + character", size=20, color=WHITE)
add_paragraph(tf2, "AI writes the story in real-time", size=20, color=WHITE)
add_paragraph(tf2, "Your choices shape the plot", size=20, color=WHITE)


# =====================================================
# SLIDE 9 - Behind the Curtain
# =====================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

tb = add_text_box(slide, Inches(1.5), Inches(0.8), Inches(10.3), Inches(1.5))
set_text(tb.text_frame, "Behind the curtain...", size=44, bold=True, color=ACCENT_BLUE, alignment=PP_ALIGN.CENTER)

# Code-like card
card = add_shape(slide, Inches(2), Inches(2.5), Inches(9.3), Inches(2.5), RGBColor(0x0D, 0x11, 0x17))
tb_code = add_text_box(slide, Inches(2.5), Inches(2.7), Inches(8.5), Inches(2.2))
tf = tb_code.text_frame
set_text(tf, "utils.py  --  70 lines of Python", size=16, color=MID_GRAY, font_name="Consolas")
add_paragraph(tf, "", size=8)
add_paragraph(tf, 'url = "https://ai.googleapis.com/v1/models/gemma:generateContent"', size=16, color=ACCENT_GREEN, font_name="Consolas")
add_paragraph(tf, 'response = requests.post(url, json=data)', size=16, color=ACCENT_GREEN, font_name="Consolas")
add_paragraph(tf, 'return response.json()["candidates"][0]["content"]', size=16, color=ACCENT_GREEN, font_name="Consolas")

tb3 = add_text_box(slide, Inches(1.5), Inches(5.5), Inches(10.3), Inches(1.5))
set_text(tb3.text_frame, "This is ALL the code that connects to AI.\nNot magic. Python + an API + knowing how the internet works.", size=24, color=WHITE, alignment=PP_ALIGN.CENTER)


# =====================================================
# SLIDE 10 - Three Levels
# =====================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

tb = add_text_box(slide, Inches(1.5), Inches(0.3), Inches(10.3), Inches(1))
set_text(tb.text_frame, "Three Levels of Tech", size=44, bold=True, color=WHITE, alignment=PP_ALIGN.CENTER)

# Level 1
card1 = add_shape(slide, Inches(0.8), Inches(1.6), Inches(3.7), Inches(4.5), DARK_CARD, MID_GRAY)
tb1 = add_text_box(slide, Inches(1.1), Inches(1.9), Inches(3.2), Inches(4))
tf = tb1.text_frame
set_text(tf, "Level 1", size=18, color=MID_GRAY, bold=True)
add_paragraph(tf, "USER", size=32, bold=True, color=MID_GRAY)
add_paragraph(tf, "", size=8)
add_paragraph(tf, "You type prompts into ChatGPT", size=18, color=LIGHT_GRAY)
add_paragraph(tf, "", size=8)
add_paragraph(tf, "Everyone is here.", size=18, color=MID_GRAY)
add_paragraph(tf, "No advantage.", size=18, color=MID_GRAY)

# Level 2
card2 = add_shape(slide, Inches(4.8), Inches(1.6), Inches(3.7), Inches(4.5), DARK_CARD, ACCENT_BLUE)
tb2 = add_text_box(slide, Inches(5.1), Inches(1.9), Inches(3.2), Inches(4))
tf2 = tb2.text_frame
set_text(tf2, "Level 2", size=18, color=ACCENT_BLUE, bold=True)
add_paragraph(tf2, "BUILDER", size=32, bold=True, color=ACCENT_BLUE)
add_paragraph(tf2, "", size=8)
add_paragraph(tf2, "You make AI do what YOU want", size=18, color=WHITE)
add_paragraph(tf2, "Build apps, tools, businesses", size=18, color=WHITE)
add_paragraph(tf2, "", size=8)
add_paragraph(tf2, "Few people are here.", size=18, color=ACCENT_BLUE)
add_paragraph(tf2, "This is where jobs are.", size=18, color=ACCENT_BLUE)

# Level 3
card3 = add_shape(slide, Inches(8.8), Inches(1.6), Inches(3.7), Inches(4.5), DARK_CARD, ACCENT_GREEN)
tb3 = add_text_box(slide, Inches(9.1), Inches(1.9), Inches(3.2), Inches(4))
tf3 = tb3.text_frame
set_text(tf3, "Level 3", size=18, color=ACCENT_GREEN, bold=True)
add_paragraph(tf3, "CREATOR", size=32, bold=True, color=ACCENT_GREEN)
add_paragraph(tf3, "", size=8)
add_paragraph(tf3, "You understand the systems behind AI", size=18, color=WHITE)
add_paragraph(tf3, "You CREATE the next ChatGPT", size=18, color=WHITE)
add_paragraph(tf3, "", size=8)
add_paragraph(tf3, "Almost nobody your age", size=18, color=ACCENT_GREEN)
add_paragraph(tf3, "is here. This is the future.", size=18, color=ACCENT_GREEN)

# Bottom quote
tb_q = add_text_box(slide, Inches(1.5), Inches(6.4), Inches(10.3), Inches(0.8))
set_text(tb_q.text_frame, "We take you from Level 1 to Level 2. And prepare you for Level 3.", size=22, color=ACCENT_BLUE, bold=True, alignment=PP_ALIGN.CENTER)


# =====================================================
# SLIDE 11 - Why Still Study?
# =====================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

tb = add_text_box(slide, Inches(1.5), Inches(0.5), Inches(10.3), Inches(1))
set_text(tb.text_frame, '"But AI can write code. Why learn?"', size=44, bold=True, color=ACCENT_ORANGE, alignment=PP_ALIGN.CENTER)

quotes = [
    ("Calculators exist. We still learn math.", WHITE),
    ("You need to know WHEN to use AI,", WHITE),
    ("WHETHER the answer is right,", WHITE),
    ("and WHAT to ask.", WHITE),
    ("", WHITE),
    ("If you can't tell whether AI's output is correct,", LIGHT_GRAY),
    ("secure, or efficient --", LIGHT_GRAY),
    ("", LIGHT_GRAY),
    ("you're not the builder. You're the passenger.", ACCENT_ORANGE),
]

tb2 = add_text_box(slide, Inches(2), Inches(2.2), Inches(9.3), Inches(4.5))
tf = tb2.text_frame
tf.word_wrap = True
for i, (text, color) in enumerate(quotes):
    if i == 0:
        set_text(tf, text, size=26, color=color)
    else:
        add_paragraph(tf, text, size=26, color=color, space_before=Pt(4))


# =====================================================
# SLIDE 12 - The Real Talk
# =====================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

tb = add_text_box(slide, Inches(1.5), Inches(0.5), Inches(10.3), Inches(1))
set_text(tb.text_frame, "Let's address the hype.", size=40, bold=True, color=WHITE, alignment=PP_ALIGN.CENTER)

rows = [
    ('"AI will replace coders"', "AI replaces coders who can't think.\nIt amplifies coders who can.", ACCENT_RED),
    ('"I can just use ChatGPT"', "Sure. So can everyone else.\nWhat's YOUR edge?", ACCENT_ORANGE),
    ('"School math is useless"', "The password cracker you just saw?\nThat's combinatorics from your math class.", ACCENT_BLUE),
    ('"I want to be a hacker"', "Great. Hackers are the best learners\nI know. Let's channel that.", ACCENT_GREEN),
]

for i, (say, respond, color) in enumerate(rows):
    y = Inches(1.8) + Inches(1.35) * i
    card = add_shape(slide, Inches(0.8), y, Inches(11.7), Inches(1.15), DARK_CARD, color)
    tb_s = add_text_box(slide, Inches(1.2), y + Emu(Inches(0.15).emu), Inches(4), Inches(0.9))
    set_text(tb_s.text_frame, say, size=18, color=color, bold=True)
    tb_r = add_text_box(slide, Inches(5.5), y + Emu(Inches(0.1).emu), Inches(6.5), Inches(0.95))
    set_text(tb_r.text_frame, respond, size=18, color=WHITE)


# =====================================================
# SLIDE 13 - Portfolio Pitch
# =====================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

tb = add_text_box(slide, Inches(1.5), Inches(0.5), Inches(10.3), Inches(1.2))
set_text(tb.text_frame, "Start Your Portfolio Now.", size=44, bold=True, color=WHITE, alignment=PP_ALIGN.CENTER)

tb_sub = add_text_box(slide, Inches(1.5), Inches(1.5), Inches(10.3), Inches(1))
set_text(tb_sub.text_frame, "In 8th-10th grade, nobody expects you to have one.\nThat's exactly why having one is powerful.", size=24, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)

# Two comparison cards
card1 = add_shape(slide, Inches(1.5), Inches(3.3), Inches(4.8), Inches(3), DARK_CARD, MID_GRAY)
tb_c1 = add_text_box(slide, Inches(1.8), Inches(3.6), Inches(4.3), Inches(2.5))
tf = tb_c1.text_frame
set_text(tf, "Student A", size=24, bold=True, color=MID_GRAY)
add_paragraph(tf, "", size=10)
add_paragraph(tf, '"I know Python."', size=22, color=LIGHT_GRAY)
add_paragraph(tf, "", size=8)
add_paragraph(tf, "No proof. No projects.", size=20, color=MID_GRAY)
add_paragraph(tf, "Just a claim.", size=20, color=MID_GRAY)

card2 = add_shape(slide, Inches(7), Inches(3.3), Inches(4.8), Inches(3), DARK_CARD, ACCENT_GREEN)
tb_c2 = add_text_box(slide, Inches(7.3), Inches(3.6), Inches(4.3), Inches(2.5))
tf2 = tb_c2.text_frame
set_text(tf2, "Student B", size=24, bold=True, color=ACCENT_GREEN)
add_paragraph(tf2, "", size=10)
add_paragraph(tf2, "Opens laptop. Shows a live", size=22, color=WHITE)
add_paragraph(tf2, "AI chatbot they built.", size=22, color=WHITE)
add_paragraph(tf2, "", size=8)
add_paragraph(tf2, "7 projects. Real portfolio.", size=20, color=ACCENT_GREEN)


# =====================================================
# SLIDE 14 - The 3 Phases
# =====================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

tb = add_text_box(slide, Inches(1.5), Inches(0.3), Inches(10.3), Inches(1))
set_text(tb.text_frame, "Your 6-Week Journey", size=44, bold=True, color=WHITE, alignment=PP_ALIGN.CENTER)

tb_sub = add_text_box(slide, Inches(1.5), Inches(1.1), Inches(10.3), Inches(0.6))
set_text(tb_sub.text_frame, "Learn.  Build.  Amplify.", size=26, color=ACCENT_BLUE, alignment=PP_ALIGN.CENTER)

# Phase 1
card1 = add_shape(slide, Inches(0.5), Inches(2.2), Inches(3.9), Inches(4.5), DARK_CARD, ACCENT_ORANGE)
tb1 = add_text_box(slide, Inches(0.8), Inches(2.5), Inches(3.4), Inches(4))
tf = tb1.text_frame
set_text(tf, "Phase 1: Foundation", size=20, bold=True, color=ACCENT_ORANGE)
add_paragraph(tf, "Weeks 1-2", size=16, color=MID_GRAY)
add_paragraph(tf, "", size=8)
add_paragraph(tf, "Python fundamentals", size=18, color=WHITE)
add_paragraph(tf, "Logic & problem-solving", size=18, color=WHITE)
add_paragraph(tf, "No AI. Intentionally.", size=18, color=WHITE)
add_paragraph(tf, "", size=6)
add_paragraph(tf, "Project:", size=16, color=MID_GRAY)
add_paragraph(tf, "Password Fortress", size=18, bold=True, color=ACCENT_ORANGE)
add_paragraph(tf, "", size=6)
add_paragraph(tf, "AI role: None.", size=16, color=MID_GRAY)
add_paragraph(tf, '"Learn to think first."', size=16, color=LIGHT_GRAY)

# Phase 2
card2 = add_shape(slide, Inches(4.7), Inches(2.2), Inches(3.9), Inches(4.5), DARK_CARD, ACCENT_BLUE)
tb2 = add_text_box(slide, Inches(5.0), Inches(2.5), Inches(3.4), Inches(4))
tf2 = tb2.text_frame
set_text(tf2, "Phase 2: Building", size=20, bold=True, color=ACCENT_BLUE)
add_paragraph(tf2, "Weeks 3-4", size=16, color=MID_GRAY)
add_paragraph(tf2, "", size=8)
add_paragraph(tf2, "APIs, web apps, OOP", size=18, color=WHITE)
add_paragraph(tf2, "How AI models work", size=18, color=WHITE)
add_paragraph(tf2, "Connect to real AI", size=18, color=WHITE)
add_paragraph(tf2, "", size=6)
add_paragraph(tf2, "Projects:", size=16, color=MID_GRAY)
add_paragraph(tf2, "Quiz Master, Space Defender", size=17, bold=True, color=ACCENT_BLUE)
add_paragraph(tf2, "", size=6)
add_paragraph(tf2, "AI role: Learning tool.", size=16, color=MID_GRAY)
add_paragraph(tf2, '"Ask better questions."', size=16, color=LIGHT_GRAY)

# Phase 3
card3 = add_shape(slide, Inches(8.9), Inches(2.2), Inches(3.9), Inches(4.5), DARK_CARD, ACCENT_GREEN)
tb3 = add_text_box(slide, Inches(9.2), Inches(2.5), Inches(3.4), Inches(4))
tf3 = tb3.text_frame
set_text(tf3, "Phase 3: Amplify", size=20, bold=True, color=ACCENT_GREEN)
add_paragraph(tf3, "Weeks 5-6", size=16, color=MID_GRAY)
add_paragraph(tf3, "", size=8)
add_paragraph(tf3, "Full AI-powered apps", size=18, color=WHITE)
add_paragraph(tf3, "Design your own project", size=18, color=WHITE)
add_paragraph(tf3, "Portfolio ready", size=18, color=WHITE)
add_paragraph(tf3, "", size=6)
add_paragraph(tf3, "Projects:", size=16, color=MID_GRAY)
add_paragraph(tf3, "Chatbot, Tutor, Story Forge", size=17, bold=True, color=ACCENT_GREEN)
add_paragraph(tf3, "", size=6)
add_paragraph(tf3, "AI role: Co-builder.", size=16, color=MID_GRAY)
add_paragraph(tf3, '"You + AI = 10x"', size=16, color=LIGHT_GRAY)


# =====================================================
# SLIDE 15 - The Logic
# =====================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

tb = add_text_box(slide, Inches(1.5), Inches(1), Inches(10.3), Inches(1))
set_text(tb.text_frame, "The Difference", size=44, bold=True, color=WHITE, alignment=PP_ALIGN.CENTER)

# Without
card1 = add_shape(slide, Inches(1.5), Inches(2.5), Inches(10.3), Inches(1.5), DARK_CARD, ACCENT_RED)
tb1 = add_text_box(slide, Inches(2), Inches(2.7), Inches(9.3), Inches(1.2))
tf = tb1.text_frame
set_text(tf, "Without foundation      -->      Use AI blindly      -->      You're replaceable", size=24, color=ACCENT_RED, alignment=PP_ALIGN.CENTER, font_name="Consolas")

# With
card2 = add_shape(slide, Inches(1.5), Inches(4.5), Inches(10.3), Inches(1.5), DARK_CARD, ACCENT_GREEN)
tb2 = add_text_box(slide, Inches(2), Inches(4.7), Inches(9.3), Inches(1.2))
tf2 = tb2.text_frame
set_text(tf2, "With foundation         -->      Direct AI           -->      You're invaluable", size=24, color=ACCENT_GREEN, alignment=PP_ALIGN.CENTER, font_name="Consolas")


# =====================================================
# SLIDE 16 - Interactive: What would YOU build?
# =====================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

tb = add_text_box(slide, Inches(1.5), Inches(1.5), Inches(10.3), Inches(2))
set_text(tb.text_frame, "If you could build ANY\napp or tool...", size=48, bold=True, color=WHITE, alignment=PP_ALIGN.CENTER)

tb2 = add_text_box(slide, Inches(1.5), Inches(4.2), Inches(10.3), Inches(1.5))
set_text(tb2.text_frame, "What would it be?", size=44, color=ACCENT_GREEN, bold=True, alignment=PP_ALIGN.CENTER)

tb3 = add_text_box(slide, Inches(1.5), Inches(6), Inches(10.3), Inches(0.8))
set_text(tb3.text_frame, "[ Open discussion -- let students share ideas ]", size=20, color=MID_GRAY, alignment=PP_ALIGN.CENTER)


# =====================================================
# SLIDE 17 - What's Next
# =====================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

tb = add_text_box(slide, Inches(1.5), Inches(0.5), Inches(10.3), Inches(1))
set_text(tb.text_frame, "What's Coming Next", size=44, bold=True, color=WHITE, alignment=PP_ALIGN.CENTER)

sessions = [
    ("Week 1-2", "Python Fundamentals + Password Fortress", ACCENT_ORANGE),
    ("Week 3-4", "APIs + Web Apps + AI Integration", ACCENT_BLUE),
    ("Week 5-6", "Full AI Apps + Your Own Project", ACCENT_GREEN),
    ("Bonus Sessions", "Linux, Git, Web Scraping, CTF, Hackathon", ACCENT_PURPLE),
]

for i, (week, desc, color) in enumerate(sessions):
    y = Inches(2) + Inches(1.3) * i
    card = add_shape(slide, Inches(1.5), y, Inches(10.3), Inches(1.05), DARK_CARD, color)
    tb_w = add_text_box(slide, Inches(1.8), y + Emu(Inches(0.15).emu), Inches(2.5), Inches(0.8))
    set_text(tb_w.text_frame, week, size=22, bold=True, color=color)
    tb_d = add_text_box(slide, Inches(4.5), y + Emu(Inches(0.15).emu), Inches(7), Inches(0.8))
    set_text(tb_d.text_frame, desc, size=22, color=WHITE)


# =====================================================
# SLIDE 18 - Closing
# =====================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide)

line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(4.5), Inches(2.5), Inches(4.3), Pt(4))
line.fill.solid()
line.fill.fore_color.rgb = ACCENT_BLUE
line.line.fill.background()

tb = add_text_box(slide, Inches(1.5), Inches(1), Inches(10.3), Inches(1.5))
set_text(tb.text_frame, "WorldWithWeb", size=52, bold=True, color=WHITE, alignment=PP_ALIGN.CENTER)

tb2 = add_text_box(slide, Inches(1.5), Inches(3), Inches(10.3), Inches(1))
set_text(tb2.text_frame, "Don't learn to code. Code to learn.", size=30, color=ACCENT_BLUE, alignment=PP_ALIGN.CENTER)

tb3 = add_text_box(slide, Inches(1.5), Inches(4.5), Inches(10.3), Inches(1.5))
tf = tb3.text_frame
set_text(tf, "worldwithweb.com", size=24, color=LIGHT_GRAY, alignment=PP_ALIGN.CENTER)
add_paragraph(tf, "", size=10)
add_paragraph(tf, "Let's build something.", size=28, color=ACCENT_GREEN, bold=True, alignment=PP_ALIGN.CENTER)


# Save
output_path = r"c:\Users\naaz.verma\personal\python_projects\WorldWithWeb_Demo_Session.pptx"
prs.save(output_path)
print(f"Saved to {output_path}")
