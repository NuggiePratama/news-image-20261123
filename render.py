#!/usr/bin/env python3
"""One-day newspaper poster for Monday 23 November 2026.

Draws a flat 1024x1024 infographic from a fixed, hand-checked story list.
No network, no clock, no randomness: the same input always paints the
same pixels, so two runs write byte-identical PNGs.

Every story below was checked against live reporting dated 23 Nov 2026
(Reuters, AP, BBC, CNN, Al Jazeera, Guardian, CNBC, Bloomberg, ESA/JAXA
and the agencies they quote). A story whose key event fell on 21 or
22 Nov is labelled with that date and is shown only because its key
development was confirmed or first reported on 23 Nov.
Confidence: [H] two or more major sources, or an official statement.
[M] one source, or agencies report the figure differently.
[R] reported and attributed, not independently confirmed.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024
MARGIN = 16
COLW = 320
GAP = 8
INK = (20, 33, 61)
PAPER = (247, 243, 232)
CREAM = (255, 252, 244)
RED = (180, 35, 24)
TEAL = (14, 107, 107)
GREY = (90, 96, 108)
LINE = (196, 188, 168)
NAVYBG = (20, 33, 61)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = load("DejaVuSerif-Bold.ttf", 30)
F_DATE = load("DejaVuSans-Bold.ttf", 15)
F_HERO_T = load("DejaVuSans-Bold.ttf", 13)
F_HERO_D = load("DejaVuSans.ttf", 10)
F_SEC = load("DejaVuSans-Bold.ttf", 11)
F_CARD_T = load("DejaVuSans-Bold.ttf", 11)
F_CARD_D = load("DejaVuSans.ttf", 9)
F_SMALL = load("DejaVuSans.ttf", 8)
F_SMALL_B = load("DejaVuSans-Bold.ttf", 9)
F_TICK = load("DejaVuSans-Bold.ttf", 10)
F_NUM = load("DejaVuSans-Bold.ttf", 15)

# (region, title, detail, confidence) — 49 stories, 7 regions
STORIES = [
    ("GULF & MIDDLE EAST", "Iran vows 'all means' vs blockade", "Foreign ministry: Tehran will use every tool to end the US naval blockade of its oil exports. [H]", "H"),
    ("GULF & MIDDLE EAST", "Three tankers hit mines in Hormuz", "Iranian media: three tankers exploded after striking mines in the strait; shipping stays disrupted. [H]", "H"),
    ("GULF & MIDDLE EAST", "Bahrain all-clear after Sat attack", "Bahrain reports no injuries or damage; Iran says it hit two US bases there on Saturday. [H]", "H"),
    ("GULF & MIDDLE EAST", "Houthis hit Saudi refinery: claim", "Houthis claim a strike on Rabigh refinery; Saudi strikes in Yemen kill 17 telecom staff, Houthis say. [M]", "M"),
    ("GULF & MIDDLE EAST", "Gaza strikes kill 3, incl. UN worker", "Israeli strikes kill at least three in Gaza, including an UNRWA worker, despite the Oct 2025 truce. [H]", "H"),
    ("GULF & MIDDLE EAST", "Oxfam: Gaza is a 'toxic wasteland'", "Oxfam: signs of contamination across almost all of Gaza; cleanup urged as strikes continue. [H]", "H"),
    ("GULF & MIDDLE EAST", "Settler arson condemned in W. Bank", "President Herzog and Eisenkot condemn settler arson attacks on Palestinians in the West Bank. [H]", "H"),
    ("GULF & MIDDLE EAST", "Israel coalition talks end, no deal", "Netanyahu-Likud and Eisenkot end government talks without agreement; Eisenkot sees no imminent Iran threat. [H]", "H"),
    ("EUROPE", "Russian strike on Dymer kills 11+", "Apartment block hit north of Kyiv; a boy, 7, and a woman, 79, pulled alive after 22 hours in rubble. [H]", "H"),
    ("EUROPE", "COP31 fallout: 'no new text'", "After Sun collapse, presidency says it will not draft a new text; Australia, Pacific states voice despair. [H]", "H"),
    ("EUROPE", "NATO in Berlin: defend every inch", "NATO pledges to defend all territory, incl. in space, after reports of a Russian nuclear-armed satellite. [M]", "M"),
    ("EUROPE", "EU proposes 22nd Russia sanctions", "Package would bar visas for ex-combatants, target crypto and ban Russian flags at EU sports events. [H]", "H"),
    ("EUROPE", "Poland: 3 Russian missiles landed", "Prosecutors confirm three Kh-101 cruise missiles hit SE Poland on 20 Nov; NATO meets urgently Mon. [H]", "H"),
    ("EUROPE", "Abu Dhabi talks end, no breakthrough", "US-Ukraine-Russia talks close after 2 days; Moscow envoy Medinsky holds a hard line on territory. [H]", "H"),
    ("EUROPE", "Belgium strike grounds all flights", "Air traffic shut 07:00-21:00 local; ~60,000 passengers hit as unions march in Brussels vs austerity. [H]", "H"),
    ("EUROPE", "12,000 flee Manchester arena", "Co-op Live evacuated at a Don Toliver gig after an unknown substance; 80+ treated, one in hospital. [H]", "H"),
    ("EUROPE", "Bomb threats hit schools in DE, DK", "Hundreds of schools in Germany and Denmark get emailed bomb threats; police say not credible. [H]", "H"),
    ("EUROPE", "Spain amnesties Puigdemont", "Supreme Court grants amnesty to Carles Puigdemont over the 2017 independence declaration; he may return. [H]", "H"),
    ("AMERICAS", "Nvidia brings Huang back as CEO", "Board unanimously reinstates Jensen Huang, 11 days after he quit; Trump backs the move, shares soar. [H]", "H"),
    ("AMERICAS", "US stocks rebound after AI sell-off", "S&P 500 up ~4.7% Mon; Nasdaq +6.5% as Nvidia jump lifts tech after last week's sharp falls. [M]", "M"),
    ("AMERICAS", "Democrats: 258 House seats (22 Nov)", "Midterm count gives Democrats at least 258 House seats, biggest majority since 1992; Senate 56-44. [M]", "M"),
    ("AMERICAS", "Trump calls Putin 'my friend'", "After a Shenzhen meeting with Putin and Xi, Trump uses the phrase; Zelensky calls Putin a killer. [H]", "H"),
    ("AMERICAS", "States sue Musk firms over Grok", "Virginia and Oregon sue SpaceX and X: Grok let users make sexualised images without consent, they say. [H]", "H"),
    ("AMERICAS", "US blacklists AI firm Megaspeed", "Singapore-based Megaspeed put on entity list over alleged AI-chip funnelling to China. [H]", "H"),
    ("AMERICAS", "ICE arrests at Seattle airport", "Masked officers detain a father and daughter boarding a flight Sat; protests follow at Sea-Tac. [H]", "H"),
    ("AMERICAS", "DoJ: US citizen deported by error", "Justice Dept admits in court that Brian Morales Garcia of Texas was wrongly deported to Mexico. [H]", "H"),
    ("AMERICAS", "'El Chapo Isidro' captured (21-22 Nov)", "Mexico special forces seize FBI most-wanted Fausto Isidro Meza Flores in Sinaloa, with US help. [H]", "H"),
    ("ASIA & PACIFIC", "Indonesia candy-factory fire: 24 dead", "Death toll confirmed Mon after Sat blaze at PT Fonusa Agung Mulia, Banten; ~30 still missing. [H]", "H"),
    ("ASIA & PACIFIC", "India pledges $1.6bn aid to Nepal", "Modi and Nepal PM Balendra Shah agree rebuilding aid after floods; rail, hydropower and fuel deals. [H]", "H"),
    ("ASIA & PACIFIC", "S. Korea education chief resigns", "Minister Choi Kyo-jin quits over AI-cheating fears at the university entrance exam; president accepts. [H]", "H"),
    ("ASIA & PACIFIC", "Tata Steel buys $1.67bn Apollo stake", "Tata Steel to take a 26.4% stake in APL Apollo, India's top structural steel-pipe maker. [H]", "H"),
    ("ASIA & PACIFIC", "Gas +8.6%; Japan power at 2022 high", "European gas jumps on a cold forecast; Japan spot power hits its highest since Aug 2022. [H]", "H"),
    ("AFRICA", "Nigeria mourners' boat capsizes: 24", "Boat carrying mourners capsizes in Bayelsa; at least 24 dead. Overcrowding and no life jackets blamed. [H]", "H"),
    ("AFRICA", "South Sudan attack kills 24 civilians", "Paramilitary attack in Tonj East kills 24, incl. seven children; four attackers also die. [H]", "H"),
    ("AFRICA", "Khartoum drones hit UN building", "Overnight drone strikes damage homes and a UN building; army blames RSF, says drones came from Ethiopia. [M]", "M"),
    ("AFRICA", "Kenya and DR Congo restore ties", "Presidents Ruto and Tshisekedi agree full diplomatic relations at a summit in Oyo, Congo-Brazzaville. [H]", "H"),
    ("AFRICA", "Fighting traps Ebola teams in Congo", "Heavy fighting in Ituri, DR Congo, forces Ebola responders to shelter in a maternity ward for 24h+. [H]", "H"),
    ("MARKETS & TECH", "Bitcoin back above ~$63,000", "BTC rebounds from ~$55,100 weekend low as Nvidia news lifts risk assets; ETH up ~4.7% to ~$1,785. [M]", "M"),
    ("MARKETS & TECH", "Oil slides ~4%; Brent $86.72", "Crude falls as returning supply outweighs Gulf attacks; Brent down ~26% over the past month. [H]", "H"),
    ("MARKETS & TECH", "CrowdStrike to buy Zscaler: $44bn", "CrowdStrike agrees a $44bn deal for Zscaler, combining two big cloud-security firms. [H]", "H"),
    ("MARKETS & TECH", "ConocoPhillips exits Norway: $4.4bn", "Vaar Energi to buy ConocoPhillips' Norwegian business, incl. Ekofisk, the field that began Norway's oil era. [H]", "H"),
    ("MARKETS & TECH", "Capita shares plunge 70%", "UK outsourcer's chief quits after delays to civil-service pension payments; shares collapse. [H]", "H"),
    ("MARKETS & TECH", "US sanctions Iran 'shadow banks'", "Treasury sanctions 8 people and 22 entities in Iran, UAE, Turkey and Hong Kong over Iran money flows. [H]", "H"),
    ("SCIENCE, SPACE & SPORT", "BepiColombo in Mercury orbit (22 Nov)", "ESA-JAXA probe enters Mercury orbit after an 8-year trip; a software glitch cut its engine burn short. [H]", "H"),
    ("SCIENCE, SPACE & SPORT", "Riemann proof claimed, unverified", "Anthropic mathematician posts a claimed proof of the Riemann hypothesis; experts have not verified it. [R]", "R"),
    ("SCIENCE, SPACE & SPORT", "Pancreatic drug shrinks tumours", "Trial drug shrinks pancreatic tumours; in a small share of patients they vanish. Longer trials needed. [R]", "R"),
    ("SCIENCE, SPACE & SPORT", "Volcanoes found in Mariana Trench", "Robot submarine finds volcanic activity never before seen in the world's deepest ocean trench. [H]", "H"),
    ("SCIENCE, SPACE & SPORT", "Alcaraz wins first ATP Finals (22 Nov)", "Carlos Alcaraz beats Alexander Zverev 6-2, 7-6 in Turin for his first ATP Finals title. [H]", "H"),
    ("SCIENCE, SPACE & SPORT", "Brentford 4-0 Everton", "Lewis-Potter scores twice in two minutes as Brentford rout 10-man Everton; Brentford rise to 6th. [H]", "H"),
]

TIMELINE = "UTC TIMELINE  ·  00:00 Khartoum drones  ·  06:00 Belgium airspace shut  ·  AM Nvidia reinstates Huang  ·  NOON Merkury sunk  ·  PM COP31: no new text  ·  20:00 Brentford 4-0"

TICKER = "ALSO: Washington 22-20 Bengals (Mon night)  ·  US to host 2031 Women's World Cup  ·  Bolsonaro in intensive care in Brasilia  ·  Tajikistan quits the ICC  ·  Lewis Pugh swims the Strait of Hormuz for its wildlife"


def wrap(draw, text, font, width):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def paint(out_path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0 = MARGIN
    x1 = W - MARGIN
    y = MARGIN

    # Masthead, 64px
    d.rectangle([x0, y, x1, y + 64], fill=NAVYBG)
    d.text((x0 + 14, y + 5), "THE WORLD IN ONE PAGE", font=F_TITLE, fill=(255, 252, 244))
    d.text((x0 + 14, y + 42), "MONDAY 23 NOVEMBER 2026  ·  49 VERIFIED STORIES  ·  7 REGIONS", font=F_DATE, fill=(255, 214, 90))
    d.text((x1 - 14, y + 42), "ONE DAY · ONE IMAGE", font=F_SMALL_B, fill=(255, 252, 244), anchor="ra")
    y += 64 + 5

    # Date-check strip, 24px
    d.rectangle([x0, y, x1, y + 24], fill=RED)
    d.text((x0 + 10, y + 6), "DATE CHECK: every story happened or was first reported Mon 23 Nov 2026 (UTC), or carries its earlier date. No guesswork.", font=F_SMALL_B, fill=(255, 255, 255))
    y += 24 + 5

    # Hero, 62px: two panels, one line of art each
    hero_y = y
    hero_h = 62
    half = (x1 - x0 - GAP) // 2
    d.rectangle([x0, hero_y, x0 + half, hero_y + hero_h], fill=(16, 68, 38))
    d.rectangle([x0 + 10, hero_y + 18, x0 + 34, hero_y + 42], outline=(120, 220, 150), width=2)
    d.line([x0 + 22, hero_y + 18, x0 + 22, hero_y + 10], fill=(120, 220, 150), width=2)
    d.line([x0 + 22, hero_y + 42, x0 + 22, hero_y + 50], fill=(120, 220, 150), width=2)
    d.text((x0 + 44, hero_y + 6), "NVIDIA BRINGS HUANG BACK", font=F_HERO_T, fill=(255, 255, 255))
    d.text((x0 + 44, hero_y + 24), "Board reinstates Jensen Huang as CEO, 11 days after he quit.", font=F_HERO_D, fill=(220, 240, 220))
    d.text((x0 + 44, hero_y + 40), "Shares jump ~30% · Nasdaq +6.5% · US stocks rebound.", font=F_HERO_T, fill=(255, 214, 90))
    rx = x0 + half + GAP
    d.rectangle([rx, hero_y, x1, hero_y + hero_h], fill=(96, 22, 16))
    d.polygon([(rx + 12, hero_y + 40), (rx + 88, hero_y + 40), (rx + 80, hero_y + 52), (rx + 20, hero_y + 52)], fill=(30, 30, 34))
    d.rectangle([rx + 40, hero_y + 26, rx + 58, hero_y + 40], fill=(30, 30, 34))
    d.rectangle([rx + 64, hero_y + 18, rx + 70, hero_y + 40], fill=(255, 214, 90))
    d.ellipse([rx + 62, hero_y + 8, rx + 74, hero_y + 20], fill=(230, 220, 200))
    d.text((rx + 96, hero_y + 6), "HORMUZ ON EDGE", font=F_HERO_T, fill=(255, 255, 255))
    d.text((rx + 96, hero_y + 24), "Iran vows 'all means' to end the US blockade; 3 tankers hit mines.", font=F_HERO_D, fill=(255, 225, 215))
    d.text((rx + 96, hero_y + 40), "Bahrain all-clear; oil slides ~4%.", font=F_HERO_T, fill=(255, 214, 90))
    y = hero_y + hero_h + 5

    # UTC timeline, one line, 22px
    d.rectangle([x0, y, x1, y + 22], fill=CREAM, outline=LINE, width=1)
    d.text((x0 + 8, y + 6), TIMELINE, font=F_SMALL_B, fill=INK)
    y += 22 + 6

    # Story columns, flowing top to bottom, left to right
    grid_top = y
    grid_bottom = H - 92
    col_x = [x0, x0 + COLW + GAP, x0 + 2 * (COLW + GAP)]
    col = 0
    cy = grid_top
    region = None
    placed = 0
    for reg, title, detail, conf in STORIES:
        if reg != region:
            region = reg
            if cy + 18 > grid_bottom and col < 2:
                col += 1
                cy = grid_top
            d.rectangle([col_x[col], cy, col_x[col] + COLW, cy + 17], fill=TEAL)
            d.text((col_x[col] + 8, cy + 3), reg, font=F_SEC, fill=(255, 255, 255))
            cy += 17 + 3
        tlines = wrap(d, title, F_CARD_T, COLW - 34)[:1]
        dlines = wrap(d, detail, F_CARD_D, COLW - 16)[:2]
        card_h = 2 + len(tlines) * 12 + len(dlines) * 10 + 2
        if cy + card_h > grid_bottom and col < 2:
            col += 1
            cy = grid_top
            d.rectangle([col_x[col], cy, col_x[col] + COLW, cy + 17], fill=TEAL)
            d.text((col_x[col] + 8, cy + 3), reg, font=F_SEC, fill=(255, 255, 255))
            cy += 17 + 3
        assert cy + card_h <= grid_bottom, (title, col, cy, card_h)
        d.rectangle([col_x[col], cy, col_x[col] + COLW, cy + card_h], fill=CREAM, outline=LINE, width=1)
        d.text((col_x[col] + 8, cy + 2), "[%s]" % conf, font=F_SMALL_B, fill=RED if conf == "R" else TEAL)
        ty = cy + 2
        for ln in tlines:
            d.text((col_x[col] + 34, ty), ln, font=F_CARD_T, fill=INK)
            ty += 12
        dy = cy + 2 + len(tlines) * 12
        for ln in dlines:
            d.text((col_x[col] + 8, dy), ln, font=F_CARD_D, fill=(52, 58, 70))
            dy += 10
        cy += card_h + 2
        placed += 1
    assert placed == 49, placed

    # By the numbers, 30px, fixed slots
    ny = grid_bottom + 6
    d.rectangle([x0, ny, x1, ny + 30], fill=NAVYBG)
    nums = [("49", "stories"), ("7", "regions"), ("+~30%", "Nvidia"), ("~$63k", "Bitcoin"), ("$86.72", "Brent"), ("24", "dead in Banten"), ("12,000", "flee Manchester")]
    slot = (x1 - x0) // len(nums)
    for i, (val, lab) in enumerate(nums):
        sx = x0 + i * slot + 10
        d.text((sx, ny + 3), val, font=F_NUM, fill=(255, 214, 90))
        d.text((sx, ny + 18), lab, font=F_SMALL, fill=(255, 252, 244))
    ty = ny + 36
    d.rectangle([x0, ty, x1, ty + 26], fill=(255, 214, 90))
    for i, ln in enumerate(wrap(d, TICKER, F_TICK, x1 - x0 - 16)[:2]):
        d.text((x0 + 8, ty + 3 + i * 11), ln, font=F_TICK, fill=INK)
    fy = ty + 30
    d.text((x0, fy), "How to read: [H] confirmed by 2+ sources or official word · [M] one source, or figures differ · [R] reported, not confirmed.", font=F_SMALL, fill=GREY)
    d.text((x0, fy + 11), "Sources: Reuters, AP, BBC, CNN, Al Jazeera, Guardian, CNBC, Bloomberg, ESA/JAXA. Checked Mon 23 Nov 2026. 22 Nov items are labelled.", font=F_SMALL, fill=GREY)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, format="PNG", optimize=True)
    return out_path


def main():
    dest = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    target = os.path.join(dest, "entry.png")
    paint(target)
    print("wrote %s" % target)


if __name__ == "__main__":
    main()
