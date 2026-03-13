#!/usr/bin/env python3
"""
BTTR Kinetic Typography — "The formula breaks."
Clean, punchy, every word lands with intent.
"""

import os
import math
import random
import struct
import wave
import shutil
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# ─── Config ───────────────────────────────────────────────────────
W, H = 1920, 1080
FPS = 30
OUT_DIR = "/Users/alexcamilar/BTTR/frames_kinetic"
AUDIO_FILE = "/Users/alexcamilar/BTTR/audio_kinetic.wav"
VIDEO_OUT = "/Users/alexcamilar/BTTR/bttr_kinetic.mp4"

BG = (8, 8, 8)
WHITE = (255, 255, 255)
GREEN = (34, 197, 94)
RED = (239, 68, 68)
GREY = (100, 100, 100)
DIM = (45, 45, 45)
AMBER = (255, 176, 0)

frames = []

# ─── Fonts ────────────────────────────────────────────────────────
def font(size, bold=False):
    try:
        idx = 1 if bold else 0
        return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size, index=idx)
    except:
        return ImageFont.load_default()

def mono(size):
    try:
        return ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", size)
    except:
        return ImageFont.load_default()

# ─── Easing functions ─────────────────────────────────────────────
def ease_out_expo(t):
    return 1 if t >= 1 else 1 - pow(2, -10 * t)

def ease_out_back(t):
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * pow(t - 1, 3) + c1 * pow(t - 1, 2)

def ease_out_cubic(t):
    return 1 - pow(1 - t, 3)

def ease_in_cubic(t):
    return t * t * t

def ease_in_out_cubic(t):
    return 4 * t * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 3) / 2

def ease_out_bounce(t):
    n1, d1 = 7.5625, 2.75
    if t < 1 / d1:
        return n1 * t * t
    elif t < 2 / d1:
        t -= 1.5 / d1
        return n1 * t * t + 0.75
    elif t < 2.5 / d1:
        t -= 2.25 / d1
        return n1 * t * t + 0.9375
    else:
        t -= 2.625 / d1
        return n1 * t * t + 0.984375

def lerp(a, b, t):
    return a + (b - a) * t

def color_lerp(c1, c2, t):
    return tuple(int(lerp(c1[i], c2[i], t)) for i in range(3))

# ─── Frame helpers ────────────────────────────────────────────────
def new_frame(bg=BG):
    return Image.new("RGB", (W, H), bg)

def add_frame(img, count=1):
    for _ in range(count):
        frames.append(img.copy())

def black_frames(count):
    for _ in range(count):
        frames.append(new_frame())

def text_size(draw, text, fnt):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def draw_centered(draw, text, y, fnt, fill=WHITE):
    tw, th = text_size(draw, text, fnt)
    draw.text(((W - tw) // 2, y), text, font=fnt, fill=fill)

def draw_at(draw, text, x, y, fnt, fill=WHITE, anchor_center=False):
    if anchor_center:
        tw, th = text_size(draw, text, fnt)
        x -= tw // 2
        y -= th // 2
    draw.text((x, y), text, font=fnt, fill=fill)

# ─── Animation builders ──────────────────────────────────────────

def animate_slam_words(words_data, duration_frames, bg=BG):
    """
    words_data: list of (text, font, color, x, y, entry_frame, entry_from)
    entry_from: "bottom", "left", "right", "top", "scale", "fade"
    """
    for f_idx in range(duration_frames):
        img = new_frame(bg)
        draw = ImageDraw.Draw(img)

        for text, fnt, color, tx, ty, entry_f, entry_type in words_data:
            if f_idx < entry_f:
                continue

            progress = min(1.0, (f_idx - entry_f) / 8)  # 8 frames to settle
            eased = ease_out_expo(progress)

            if entry_type == "bottom":
                cy = lerp(H + 50, ty, eased)
                draw_at(draw, text, tx, int(cy), fnt, fill=color)
            elif entry_type == "top":
                cy = lerp(-100, ty, eased)
                draw_at(draw, text, tx, int(cy), fnt, fill=color)
            elif entry_type == "left":
                cx = lerp(-500, tx, eased)
                draw_at(draw, text, int(cx), ty, fnt, fill=color)
            elif entry_type == "right":
                cx = lerp(W + 200, tx, eased)
                draw_at(draw, text, int(cx), ty, fnt, fill=color)
            elif entry_type == "scale":
                # fake scale by using alpha fade
                alpha = min(255, int(eased * 255))
                c = tuple(int(v * eased) for v in color)
                draw_at(draw, text, tx, ty, fnt, fill=c)
            elif entry_type == "fade":
                alpha = ease_out_cubic(progress)
                c = tuple(int(v * alpha) for v in color)
                draw_at(draw, text, tx, ty, fnt, fill=c)

        add_frame(img)

# ─── SCENES ───────────────────────────────────────────────────────

def scene_opener():
    """Every PM framework — exists because — building was expensive."""
    f_big = font(90, bold=True)
    f_med = font(70, bold=True)

    # "Every PM framework" — slam from bottom
    for i in range(20):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        t = ease_out_expo(min(1, i / 8))
        y = lerp(H, H // 2 - 60, t)
        draw_centered(draw, "Every PM framework", int(y), f_big)
        add_frame(img)

    # hold, then "exists because" from left
    for i in range(20):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        draw_centered(draw, "Every PM framework", H // 2 - 60, f_big)
        if i >= 5:
            t = ease_out_expo(min(1, (i - 5) / 8))
            x = lerp(-600, W // 2, t)
            tw, _ = text_size(draw, "exists because", f_med)
            draw.text((int(x - tw // 2), H // 2 + 50), "exists because", font=f_med, fill=GREY)
        add_frame(img)

    # "building was expensive." — SLAM with scale feel
    for i in range(25):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        draw_centered(draw, "Every PM framework", H // 2 - 60, f_big, fill=DIM)
        draw_centered(draw, "exists because", H // 2 + 50, f_med, fill=DIM)
        if i >= 3:
            t = ease_out_back(min(1, (i - 3) / 10))
            size = int(lerp(140, 80, t))
            ff = font(size, bold=True)
            draw_centered(draw, "building was expensive.", H // 2 + 140, ff, fill=RED)
        add_frame(img)

    black_frames(10)

def scene_frameworks_list():
    """RICE, WSJF, ICE — rapid cascade"""
    frameworks = [
        ("RICE", "Reach x Impact x Confidence / Effort"),
        ("WSJF", "Weighted Shortest Job First"),
        ("ICE",  "Impact, Confidence, Ease"),
    ]

    f_name = font(120, bold=True)
    f_desc = font(32)

    for name, desc in frameworks:
        # slam in
        for i in range(18):
            img = new_frame()
            draw = ImageDraw.Draw(img)
            t = ease_out_expo(min(1, i / 6))
            y = lerp(-150, H // 2 - 80, t)
            draw_centered(draw, name, int(y), f_name, fill=AMBER)
            if i > 4:
                t2 = ease_out_cubic(min(1, (i - 4) / 8))
                c = color_lerp(BG, GREY, t2)
                draw_centered(draw, desc, H // 2 + 60, f_desc, fill=c)
            add_frame(img)

    # "They all solve:"
    f_q = font(55)
    f_quote = font(65, bold=True)

    for i in range(30):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        if i < 12:
            t = ease_out_cubic(min(1, i / 8))
            c = color_lerp(BG, GREY, t)
            draw_centered(draw, "They all solve the same question:", H // 2 - 80, f_q, fill=c)
        else:
            draw_centered(draw, "They all solve the same question:", H // 2 - 80, f_q, fill=GREY)
            t = ease_out_expo(min(1, (i - 12) / 8))
            c = color_lerp(BG, WHITE, t)
            draw_centered(draw, '"What should we build?"', H // 2 + 20, f_quote, fill=c)
        add_frame(img)

    add_frame(img, count=10)
    black_frames(8)

def scene_constraint_gone():
    """That constraint is gone."""
    f = font(110, bold=True)

    # "That constraint" fades in
    for i in range(10):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        t = ease_out_cubic(min(1, i / 8))
        c = color_lerp(BG, WHITE, t)
        draw_centered(draw, "That constraint", H // 2 - 70, f, fill=c)
        add_frame(img)

    # "is gone." SLAMS from right
    for i in range(20):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        draw_centered(draw, "That constraint", H // 2 - 70, f, fill=WHITE)
        if i >= 2:
            t = ease_out_back(min(1, (i - 2) / 8))
            x = lerp(W + 200, W // 2, t)
            tw, _ = text_size(draw, "is gone.", f)
            # color pulse on impact
            if i < 6:
                col = GREEN
            else:
                col = color_lerp(GREEN, WHITE, min(1, (i - 6) / 10))
            draw.text((int(x - tw // 2), H // 2 + 50), "is gone.", font=f, fill=col)
        add_frame(img)

    add_frame(img, count=15)
    black_frames(8)

def scene_rice_formula():
    """The RICE formula builds up, then breaks on Effort → 0"""
    f_var = mono(55)
    f_op = mono(45)
    f_score = mono(70)
    f_effort = mono(60)
    f_msg = font(80, bold=True)

    # build formula piece by piece
    # (Reach × Impact × Confidence) / Effort
    pieces = [
        ("Reach", 12),
        (" x ", 6),
        ("Impact", 12),
        (" x ", 6),
        ("Confidence", 12),
    ]

    # formula build
    built = ""
    for piece_text, hold in pieces:
        built += piece_text
        for i in range(hold):
            img = new_frame()
            draw = ImageDraw.Draw(img)
            # color the latest piece green, rest white
            # simple: just draw the whole string
            tw, _ = text_size(draw, built, f_var)
            x = (W - tw) // 2
            # draw previous in white
            if len(built) > len(piece_text):
                prev = built[:-len(piece_text)]
                draw.text((x, H // 2 - 80), prev, font=f_var, fill=WHITE)
                pw, _ = text_size(draw, prev, f_var)
                # new piece in green fading to white
                t = ease_out_cubic(min(1, i / 8))
                c = color_lerp(GREEN, WHITE, t)
                draw.text((x + pw, H // 2 - 80), piece_text, font=f_var, fill=c)
            else:
                t = ease_out_cubic(min(1, i / 8))
                c = color_lerp(GREEN, WHITE, t)
                draw.text((x, H // 2 - 80), built, font=f_var, fill=c)
            add_frame(img)

    # add divider line and "Effort"
    formula_top = built
    for i in range(15):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        draw_centered(draw, formula_top, H // 2 - 80, f_var, fill=DIM)
        # divider line slides in
        t = ease_out_expo(min(1, i / 8))
        line_w = int(lerp(0, 700, t))
        cx = W // 2
        draw.line([(cx - line_w // 2, H // 2), (cx + line_w // 2, H // 2)],
                  fill=WHITE, width=3)
        if i > 4:
            t2 = ease_out_cubic(min(1, (i - 4) / 8))
            c = color_lerp(BG, WHITE, t2)
            draw_centered(draw, "Effort", H // 2 + 20, f_effort, fill=c)
        add_frame(img)

    add_frame(img, count=10)

    # NOW: Effort countdown with live RICE score
    efforts = [
        (3.0, 10), (2.0, 8), (1.0, 8), (0.5, 8),
        (0.1, 10), (0.01, 10), (0.001, 12),
    ]

    for eff, hold in efforts:
        score = int(8000 * 2 * 0.6 / eff)
        for i in range(hold):
            img = new_frame()
            draw = ImageDraw.Draw(img)
            draw_centered(draw, formula_top, H // 2 - 120, f_var, fill=DIM)
            draw.line([(W // 2 - 350, H // 2 - 40), (W // 2 + 350, H // 2 - 40)],
                      fill=WHITE, width=3)

            # effort value — gets redder as it shrinks
            redness = max(0, 1 - eff / 3.0)
            eff_color = color_lerp(WHITE, RED, redness)
            draw_centered(draw, f"Effort = {eff}", H // 2 - 10, f_effort, fill=eff_color)

            # RICE score — gets bigger and greener
            score_str = f"{score:,}"
            s_size = min(90, 50 + int(redness * 40))
            draw_centered(draw, score_str, H // 2 + 80, mono(s_size), fill=GREEN)

            # shake when effort < 0.1
            if eff < 0.1:
                from PIL import ImageChops
                dx = random.randint(-int(redness * 15), int(redness * 15))
                dy = random.randint(-int(redness * 8), int(redness * 8))
                img = ImageChops.offset(img, dx, dy)

            add_frame(img)

    # EFFORT = 0 — THE BREAK
    # flash
    for i in range(3):
        frames.append(new_frame(WHITE))
    for i in range(2):
        frames.append(new_frame(RED))

    # scattered text — the formula fragments fly apart
    for i in range(25):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        t = i / 25.0

        # fragments scatter outward from center
        fragments = [
            ("Reach", -1, -1), ("Impact", 1, -0.5), ("Confidence", -0.5, 1),
            ("Effort", 0, 1.5), ("x", -1.5, 0.3), ("x", 1.2, -1),
            ("/", 0.3, -1.3),
        ]
        for text, vx, vy in fragments:
            x = int(W // 2 + vx * t * 800 + random.randint(-5, 5))
            y = int(H // 2 + vy * t * 500 + random.randint(-5, 5))
            alpha = max(0, 1 - t * 1.2)
            c = tuple(int(v * alpha) for v in RED)
            sz = random.choice([30, 40, 50, 60])
            draw.text((x, y), text, font=mono(sz), fill=c)

        # "÷ 0" flashing in center
        if i % 3 != 0:
            draw_centered(draw, "÷ 0", H // 2 - 40, font(140, bold=True), fill=RED)

        add_frame(img)

    black_frames(10)

    # quiet aftermath
    for i in range(30):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        t = ease_out_cubic(min(1, i / 15))
        c = color_lerp(BG, WHITE, t)
        draw_centered(draw, "When effort hits zero,", H // 2 - 50, font(65, bold=True), fill=c)
        if i > 10:
            t2 = ease_out_cubic(min(1, (i - 10) / 12))
            c2 = color_lerp(BG, RED, t2)
            draw_centered(draw, "the formula divides by zero.", H // 2 + 40, font(65, bold=True), fill=c2)
        add_frame(img)

    add_frame(img, count=15)
    black_frames(10)

def scene_new_question():
    """The question shifts."""
    f = font(65, bold=True)
    f_big = font(85, bold=True)

    # old question strikes through
    old_q = '"What should we build?"'

    for i in range(30):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        draw_centered(draw, old_q, H // 2 - 40, f, fill=GREY)

        # strikethrough line grows
        if i > 8:
            t = ease_out_expo(min(1, (i - 8) / 10))
            tw, _ = text_size(draw, old_q, f)
            cx = W // 2
            line_w = int(tw * t)
            draw.line([(cx - line_w // 2, H // 2 - 5), (cx + line_w // 2, H // 2 - 5)],
                      fill=RED, width=4)
        add_frame(img)

    # new question replaces
    new_q = '"What did we learn?"'

    for i in range(35):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        # old fades
        t_fade = ease_in_cubic(min(1, i / 10))
        c_old = color_lerp(GREY, BG, t_fade)
        draw_centered(draw, old_q, H // 2 - 40, f, fill=c_old)
        tw, _ = text_size(draw, old_q, f)
        r_fade = color_lerp(RED, BG, t_fade)
        draw.line([(W // 2 - tw // 2, H // 2 - 5), (W // 2 + tw // 2, H // 2 - 5)],
                  fill=r_fade, width=4)

        # new appears
        if i > 6:
            t2 = ease_out_expo(min(1, (i - 6) / 10))
            c_new = color_lerp(BG, GREEN, t2)
            draw_centered(draw, new_q, H // 2 - 40, f_big, fill=c_new)
        add_frame(img)

    add_frame(img, count=15)
    black_frames(8)

def scene_bttr_reveal():
    """BTTR — Build. Test. Trash. Repeat."""
    f_huge = font(220, bold=True)
    f_word = font(55, bold=True)
    f_sub = font(36)

    # letters slam in one at a time
    letters = ["B", "T", "T", "R"]
    letter_colors = [GREEN, WHITE, RED, GREEN]

    for li, (letter, lc) in enumerate(zip(letters, letter_colors)):
        for i in range(10):
            img = new_frame()
            draw = ImageDraw.Draw(img)

            # draw already-placed letters
            total_w = sum(text_size(draw, l, f_huge)[0] for l in letters) + 30 * 3
            start_x = (W - total_w) // 2

            cx = start_x
            for j in range(li + 1):
                lw, _ = text_size(draw, letters[j], f_huge)
                if j < li:
                    draw.text((cx, H // 2 - 140), letters[j], font=f_huge, fill=letter_colors[j])
                elif j == li:
                    t = ease_out_back(min(1, i / 7))
                    y = lerp(-200, H // 2 - 140, t)
                    draw.text((cx, int(y)), letter, font=f_huge, fill=lc)
                cx += lw + 30
            add_frame(img)

    # hold full BTTR
    for i in range(15):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        total_w = sum(text_size(draw, l, f_huge)[0] for l in letters) + 30 * 3
        start_x = (W - total_w) // 2
        cx = start_x
        for j, (l, lc) in enumerate(zip(letters, letter_colors)):
            lw, _ = text_size(draw, l, f_huge)
            draw.text((cx, H // 2 - 140), l, font=f_huge, fill=lc)
            cx += lw + 30
        add_frame(img)

    # words appear below: Build. Test. Trash. Repeat.
    words = [
        ("Build.", GREEN, "left"),
        ("Test.", WHITE, "bottom"),
        ("Trash.", RED, "right"),
        ("Repeat.", GREEN, "top"),
    ]

    for wi in range(len(words)):
        for i in range(12):
            img = new_frame()
            draw = ImageDraw.Draw(img)

            # BTTR stays dimmed
            total_w = sum(text_size(draw, l, f_huge)[0] for l in letters) + 30 * 3
            start_x = (W - total_w) // 2
            cx = start_x
            for j, (l, lc) in enumerate(zip(letters, letter_colors)):
                lw, _ = text_size(draw, l, f_huge)
                draw.text((cx, H // 2 - 140), l, font=f_huge, fill=lc)
                cx += lw + 30

            # arrange words horizontally
            word_strs = [w[0] for w in words[:wi + 1]]
            total_ww = sum(text_size(draw, w, f_word)[0] for w in word_strs)
            gap = 30
            total_ww += gap * (len(word_strs) - 1)
            wx = (W - total_ww) // 2
            wy = H // 2 + 110

            for wj in range(wi + 1):
                wtext, wcol, wdir = words[wj]
                ww, _ = text_size(draw, wtext, f_word)

                if wj < wi:
                    draw.text((wx, wy), wtext, font=f_word, fill=wcol)
                else:
                    t = ease_out_expo(min(1, i / 7))
                    if wdir == "left":
                        ax = lerp(-300, wx, t)
                        draw.text((int(ax), wy), wtext, font=f_word, fill=wcol)
                    elif wdir == "right":
                        ax = lerp(W + 200, wx, t)
                        draw.text((int(ax), wy), wtext, font=f_word, fill=wcol)
                    elif wdir == "bottom":
                        ay = lerp(H + 50, wy, t)
                        draw.text((wx, int(ay)), wtext, font=f_word, fill=wcol)
                    elif wdir == "top":
                        ay = lerp(-100, wy, t)
                        draw.text((wx, int(ay)), wtext, font=f_word, fill=wcol)
                wx += ww + gap
            add_frame(img)

    add_frame(img, count=20)
    black_frames(8)

def scene_idea_build_signal():
    """The cycle: IDEA → BUILD → SIGNAL"""
    f_label = font(100, bold=True)
    f_arrow = mono(70)
    f_desc = font(30)

    steps = [
        ("IDEA", GREEN, "Have the idea. Be specific."),
        ("BUILD", WHITE, "Ship it fast. Ugly is fine."),
        ("SIGNAL", AMBER, "Read the data. Be honest."),
    ]

    # each step enters and holds
    visible = []
    for si, (word, color, desc) in enumerate(steps):
        visible.append((word, color, desc))

        for i in range(22):
            img = new_frame()
            draw = ImageDraw.Draw(img)

            # layout: centered, stacked with arrows
            total_h = len(visible) * 120 + (len(visible) - 1) * 40
            start_y = (H - total_h) // 2

            for vi, (vw, vc, vd) in enumerate(visible):
                y = start_y + vi * 160

                if vi < si:
                    # already placed — dim
                    draw_centered(draw, vw, y, f_label, fill=tuple(int(v * 0.4) for v in vc))
                    draw_centered(draw, vd, y + 90, f_desc, fill=DIM)
                elif vi == si:
                    # animating in
                    t = ease_out_expo(min(1, i / 8))
                    # scale effect: start big, settle
                    sz = int(lerp(140, 100, t))
                    ff = font(sz, bold=True)
                    c = color_lerp(BG, color, t)
                    draw_centered(draw, word, y - (sz - 100) // 2, ff, fill=c)
                    if i > 6:
                        t2 = ease_out_cubic(min(1, (i - 6) / 10))
                        dc = color_lerp(BG, GREY, t2)
                        draw_centered(draw, desc, y + 90, f_desc, fill=dc)

                # arrow between items
                if vi < len(visible) - 1 and vi < si:
                    ay = start_y + vi * 160 + 115
                    draw_centered(draw, "|", ay, mono(30), fill=DIM)

            add_frame(img)

    # hold final
    add_frame(img, count=20)
    black_frames(5)

    # compress into single line
    for i in range(20):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        t = ease_out_expo(min(1, i / 12))

        line = "IDEA  →  BUILD  →  SIGNAL"
        c = color_lerp(DIM, GREEN, t)
        draw_centered(draw, line, H // 2 - 30, mono(60), fill=c)
        add_frame(img)

    add_frame(img, count=20)
    black_frames(8)

def scene_manifesto():
    """Quick manifesto hits"""
    hits = [
        ("Stop scoring.", RED, "Start shipping.", GREEN),
        ("Stop debating.", RED, "Start testing.", GREEN),
        ("Stop predicting.", RED, "Start learning.", GREEN),
    ]

    f = font(80, bold=True)

    for old, old_c, new, new_c in hits:
        # old text
        for i in range(8):
            img = new_frame()
            draw = ImageDraw.Draw(img)
            t = ease_out_expo(min(1, i / 5))
            x = lerp(-600, W // 2, t)
            tw, _ = text_size(draw, old, f)
            draw.text((int(x - tw // 2), H // 2 - 50), old, font=f, fill=old_c)
            add_frame(img)

        # new text replaces
        for i in range(12):
            img = new_frame()
            draw = ImageDraw.Draw(img)
            t_out = ease_in_cubic(min(1, i / 5))
            t_in = ease_out_expo(max(0, min(1, (i - 3) / 6)))

            c_old = color_lerp(old_c, BG, t_out)
            draw_centered(draw, old, H // 2 - 50, f, fill=c_old)

            if i > 3:
                c_new = color_lerp(BG, new_c, t_in)
                draw_centered(draw, new, H // 2 - 50, f, fill=c_new)
            add_frame(img)

        add_frame(img, count=6)

    black_frames(8)

def scene_truth():
    """Truth isn't predicted. It's revealed through action."""
    f = font(70, bold=True)

    # line 1 fades in
    for i in range(20):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        t = ease_out_cubic(min(1, i / 12))
        c = color_lerp(BG, WHITE, t)
        draw_centered(draw, "Truth isn't predicted.", H // 2 - 60, f, fill=c)
        add_frame(img)

    # line 2 fades in
    for i in range(25):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        draw_centered(draw, "Truth isn't predicted.", H // 2 - 60, f, fill=WHITE)
        t = ease_out_cubic(min(1, i / 12))
        c = color_lerp(BG, GREEN, t)
        draw_centered(draw, "It's revealed through action.", H // 2 + 30, f, fill=c)
        add_frame(img)

    add_frame(img, count=25)
    black_frames(10)

def scene_logo_hold():
    """BTTR logo with extended hold and clean fadeout"""
    f_huge = font(200, bold=True)
    f_sub = font(36)
    f_tiny = mono(22)

    # fade in
    for i in range(20):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        t = ease_out_cubic(min(1, i / 15))
        c = color_lerp(BG, GREEN, t)
        draw_centered(draw, "BTTR", H // 2 - 110, f_huge, fill=c)
        if i > 8:
            t2 = ease_out_cubic(min(1, (i - 8) / 10))
            c2 = color_lerp(BG, GREY, t2)
            draw_centered(draw, "the better framework", H // 2 + 100, f_sub, fill=c2)
        add_frame(img)

    # hold
    logo_img = new_frame()
    d = ImageDraw.Draw(logo_img)
    draw_centered(d, "BTTR", H // 2 - 110, f_huge, fill=GREEN)
    draw_centered(d, "the better framework", H // 2 + 100, f_sub, fill=GREY)
    add_frame(logo_img, count=120)  # 4 seconds

    # clean fade to black
    for i in range(30):
        t = i / 30.0
        overlay = new_frame()
        img = Image.blend(logo_img, overlay, t)
        add_frame(img)

    black_frames(15)

# ─── AUDIO ────────────────────────────────────────────────────────

def generate_audio(total_frames):
    """Minimal, clean audio — low drone with subtle hits on slams"""
    duration = total_frames / FPS
    sample_rate = 44100
    num_samples = int(duration * sample_rate)
    t_arr = np.arange(num_samples) / sample_rate

    samples = np.zeros(num_samples)

    # ultra-low drone
    samples += np.sin(2 * np.pi * 40 * t_arr) * 0.08
    samples += np.sin(2 * np.pi * 80 * t_arr) * 0.04

    # gentle shimmer
    samples += np.sin(2 * np.pi * 160 * t_arr) * 0.015 * np.sin(2 * np.pi * 0.3 * t_arr)

    # tension ramp during RICE section (~30-50% of video)
    for i in range(num_samples):
        t = t_arr[i]
        progress = t / duration

        if 0.30 < progress < 0.48:
            tension = (progress - 0.30) / 0.18
            freq = 100 + tension * 400
            samples[i] += np.sin(2 * np.pi * freq * t) * 0.12 * tension

        # post-break silence
        if 0.48 < progress < 0.52:
            samples[i] *= 0.2

        # final section — warmth
        if progress > 0.85:
            fade = 1 - (progress - 0.85) / 0.15
            samples[i] *= fade

    # normalize
    peak = np.max(np.abs(samples))
    if peak > 0:
        samples = samples / peak * 0.5

    with wave.open(AUDIO_FILE, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        for s in samples:
            wf.writeframes(struct.pack('<h', int(s * 32767)))

# ─── MAIN ─────────────────────────────────────────────────────────

def main():
    if os.path.exists(OUT_DIR):
        shutil.rmtree(OUT_DIR)
    os.makedirs(OUT_DIR)

    print("Generating Kinetic Typography video...")

    print("  [1/8] Opener")
    scene_opener()

    print("  [2/8] Frameworks list")
    scene_frameworks_list()

    print("  [3/8] Constraint gone")
    scene_constraint_gone()

    print("  [4/8] RICE formula breaks")
    scene_rice_formula()

    print("  [5/8] New question")
    scene_new_question()

    print("  [6/8] BTTR reveal")
    scene_bttr_reveal()

    print("  [7/8] IDEA BUILD SIGNAL + manifesto")
    scene_idea_build_signal()
    scene_manifesto()

    print("  [8/8] Truth + logo")
    scene_truth()
    scene_logo_hold()

    print(f"\nTotal frames: {len(frames)} ({len(frames)/FPS:.1f}s)")

    print("Saving frames...")
    for i, frame in enumerate(frames):
        frame.save(os.path.join(OUT_DIR, f"frame_{i:05d}.png"))
        if i % 200 == 0:
            print(f"  {i}/{len(frames)}")

    print("Generating audio...")
    generate_audio(len(frames))

    print("Compiling with ffmpeg...")
    cmd = (
        f'ffmpeg -y -framerate {FPS} -i "{OUT_DIR}/frame_%05d.png" '
        f'-i "{AUDIO_FILE}" '
        f'-c:v libx264 -pix_fmt yuv420p -crf 18 -preset fast '
        f'-c:a aac -b:a 128k -shortest '
        f'"{VIDEO_OUT}"'
    )
    os.system(cmd)

    shutil.rmtree(OUT_DIR)
    os.remove(AUDIO_FILE)

    print(f"\nDone! → {VIDEO_OUT}")
    print(f"Duration: {len(frames)/FPS:.1f}s")

if __name__ == "__main__":
    main()
