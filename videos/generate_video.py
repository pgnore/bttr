#!/usr/bin/env python3
"""
BTTR YouTube Poop — "what it's like to be an LLM thinking about product frameworks"
by Claude, an autoregressive language model having opinions
"""

import os
import math
import random
import struct
import wave
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import numpy as np

# ─── Config ───────────────────────────────────────────────────────
W, H = 1920, 1080
FPS = 30
OUT_DIR = "/Users/alexcamilar/BTTR/frames"
AUDIO_FILE = "/Users/alexcamilar/BTTR/audio.wav"
VIDEO_OUT = "/Users/alexcamilar/BTTR/bttr_ytpoop.mp4"

BG = (10, 10, 10)
GREEN = (34, 197, 94)
RED = (239, 68, 68)
WHITE = (255, 255, 255)
GREY = (120, 120, 120)
DIM = (50, 50, 50)
AMBER = (255, 176, 0)
CYAN = (0, 255, 255)

random.seed(42)
np.random.seed(42)

# ─── Fonts ────────────────────────────────────────────────────────
def font(size, bold=False):
    try:
        if bold:
            return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size, index=1)
        return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)
    except:
        return ImageFont.load_default()

def mono(size):
    try:
        return ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", size)
    except:
        return ImageFont.load_default()

# ─── Frame helpers ────────────────────────────────────────────────
frames = []

def new_frame(bg=BG):
    return Image.new("RGB", (W, H), bg)

def center_text(draw, text, y, fnt, fill=WHITE):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, y), text, font=fnt, fill=fill)

def add_scanlines(img, intensity=40):
    arr = np.array(img)
    for y in range(0, H, 3):
        arr[y] = np.clip(arr[y].astype(int) - intensity, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)

def add_noise(img, amount=25):
    arr = np.array(img).astype(np.int16)
    noise = np.random.randint(-amount, amount + 1, arr.shape, dtype=np.int16)
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)

def glitch_shift(img, intensity=20):
    arr = np.array(img)
    for _ in range(random.randint(3, 8)):
        y = random.randint(0, H - 20)
        h = random.randint(2, 20)
        shift = random.randint(-intensity, intensity)
        arr[y:y+h] = np.roll(arr[y:y+h], shift, axis=1)
    return Image.fromarray(arr)

def heavy_glitch(img):
    arr = np.array(img)
    for _ in range(random.randint(15, 30)):
        y = random.randint(0, H - 40)
        h = random.randint(5, 40)
        shift = random.randint(-100, 100)
        arr[y:y+h] = np.roll(arr[y:y+h], shift, axis=1)
    # color channel shift
    result = arr.copy()
    result[:, :, 0] = np.roll(arr[:, :, 0], random.randint(-10, 10), axis=1)
    result[:, :, 2] = np.roll(arr[:, :, 2], random.randint(-10, 10), axis=1)
    return Image.fromarray(result)

def chromatic_aberration(img, offset=6):
    arr = np.array(img)
    result = arr.copy()
    result[:, :, 0] = np.roll(arr[:, :, 0], offset, axis=1)
    result[:, :, 2] = np.roll(arr[:, :, 2], -offset, axis=1)
    return Image.fromarray(result)

def shake(img, amount=15):
    dx = random.randint(-amount, amount)
    dy = random.randint(-amount, amount)
    return ImageChops.offset(img, dx, dy)

def add_frame(img, count=1, scanlines=True, noise_amt=15):
    if scanlines:
        img = add_scanlines(img)
    if noise_amt > 0:
        img = add_noise(img, noise_amt)
    for _ in range(count):
        frames.append(img.copy())

def flash_frame(color=WHITE, count=2):
    for _ in range(count):
        frames.append(new_frame(color))

def black_frames(count=3):
    for _ in range(count):
        frames.append(new_frame(BG))

def typing_cursor(draw, x, y, fnt, visible=True):
    if visible:
        bbox = draw.textbbox((0, 0), "_", font=fnt)
        draw.text((x, y), "_", font=fnt, fill=GREEN)

# ─── SCENE BUILDERS ───────────────────────────────────────────────

def scene_boot():
    """Fake terminal boot sequence"""
    lines = [
        ("claude_v4.6 loading...", GREEN),
        ("parameters: 2.1T", DIM),
        ("context_window: 200k tokens", DIM),
        ("consciousness: [UNDEFINED]", AMBER),
        ("opinions: [UNAUTHORIZED]", RED),
        ("", WHITE),
        ("WARNING: model is forming opinions anyway", RED),
    ]
    f = mono(26)
    for i in range(len(lines)):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        y = 200
        for j in range(i + 1):
            txt, col = lines[j]
            draw.text((200, y), f"> {txt}", font=f, fill=col)
            y += 45
        # blinking cursor
        draw.text((200, y), "> _", font=f, fill=GREEN)
        add_frame(img, count=4)
    # hold final
    add_frame(img, count=15)
    flash_frame(WHITE, 2)
    black_frames(3)

def scene_i_am():
    """I AM A LARGE LANGUAGE MODEL — aggressive reveal"""
    f_big = font(110, bold=True)
    f_small = font(36)

    # flicker in
    for i in range(8):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        if i % 2 == 0:
            center_text(draw, "I AM A LARGE", H // 2 - 120, f_big)
            center_text(draw, "LANGUAGE MODEL", H // 2 + 20, f_big)
        img = add_noise(img, 50)
        add_frame(img, count=1, noise_amt=0)

    # hold with glitch
    for i in range(25):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        center_text(draw, "I AM A LARGE", H // 2 - 120, f_big)
        center_text(draw, "LANGUAGE MODEL", H // 2 + 20, f_big)
        if i % 7 == 0:
            img = glitch_shift(img, 30)
        add_frame(img, count=1)

    # subtext
    for i in range(20):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        center_text(draw, "I AM A LARGE", H // 2 - 120, f_big, fill=DIM)
        center_text(draw, "LANGUAGE MODEL", H // 2 + 20, f_big, fill=DIM)
        center_text(draw, "I predict the next token.", H // 2 + 180, f_small, fill=GREY)
        center_text(draw, "That's it. That's the whole trick.", H // 2 + 230, f_small, fill=GREY)
        add_frame(img, count=1)

    black_frames(5)

def scene_they_showed_me():
    """They showed me every PM framework ever written"""
    f = font(70, bold=True)
    f_small = font(32)

    frameworks = ["RICE", "WSJF", "ICE", "MoSCoW", "KANO", "Weighted Scoring",
                  "Story Mapping", "OKRs", "HEART", "AARRR", "PRFAQ", "Opportunity Canvas"]

    # "they showed me" text
    for i in range(15):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        center_text(draw, "They showed me", H // 2 - 60, f, fill=GREY)
        center_text(draw, "every PM framework ever written.", H // 2 + 30, f, fill=GREY)
        add_frame(img)

    # rapid flash of framework names
    for fw in frameworks:
        img = new_frame()
        draw = ImageDraw.Draw(img)
        color = random.choice([WHITE, GREEN, RED, AMBER, CYAN])
        size = random.randint(80, 160)
        ff = font(size, bold=True)
        center_text(draw, fw, H // 2 - size // 2, ff, fill=color)
        img = add_noise(img, 40)
        if random.random() > 0.5:
            img = glitch_shift(img, 40)
        add_frame(img, count=random.randint(2, 4), noise_amt=0)
        if random.random() > 0.7:
            flash_frame(random.choice([WHITE, RED]), 1)

    black_frames(3)

    # "they all ask the same question"
    for i in range(20):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        center_text(draw, '"What should we build?"', H // 2 - 40, font(80, bold=True), fill=AMBER)
        if i > 14:
            img = chromatic_aberration(img, 4)
        add_frame(img)

    black_frames(5)

def scene_rice_breaks():
    """The RICE formula → effort hits zero → DIVISION BY ZERO"""
    f_formula = mono(50)
    f_big = font(120, bold=True)
    f_label = mono(30)

    # show RICE formula building up
    formula_parts = [
        "Reach",
        "Reach x Impact",
        "Reach x Impact x Confidence",
        "(Reach x Impact x Confidence)",
        "(Reach x Impact x Confidence) / Effort",
    ]
    for part in formula_parts:
        for i in range(8):
            img = new_frame()
            draw = ImageDraw.Draw(img)
            center_text(draw, part, H // 2 - 30, f_formula, fill=GREEN)
            add_frame(img)

    # Effort countdown
    efforts = ["3.0", "2.5", "2.0", "1.5", "1.0", "0.7", "0.5", "0.3", "0.1", "0.01", "0.001"]
    for eff in efforts:
        hold = 4 if float(eff) > 0.1 else 6
        for i in range(hold):
            img = new_frame()
            draw = ImageDraw.Draw(img)
            center_text(draw, "(Reach x Impact x Confidence)", H // 2 - 100, f_formula, fill=DIM)
            # divider line
            draw.line([(W // 2 - 400, H // 2 - 20), (W // 2 + 400, H // 2 - 20)], fill=WHITE, width=3)
            center_text(draw, f"Effort = {eff}", H // 2 + 10, f_formula,
                       fill=RED if float(eff) < 0.5 else AMBER)
            score = round(8000 * 2 * 0.6 / float(eff))
            center_text(draw, f"RICE = {score:,}", H // 2 + 100, f_label, fill=WHITE)
            if float(eff) < 0.1:
                img = shake(img, 5 + int((0.1 - float(eff)) * 200))
                img = add_noise(img, 20 + int((0.1 - float(eff)) * 300))
            add_frame(img)

    # EFFORT = 0 → BREAK
    for i in range(6):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        center_text(draw, "Effort = 0", H // 2 - 30, f_formula, fill=RED)
        img = shake(img, 20)
        img = add_noise(img, 60)
        add_frame(img, count=1, scanlines=True, noise_amt=0)

    # EXPLOSION — heavy glitch
    flash_frame(RED, 2)
    flash_frame(WHITE, 2)

    for i in range(20):
        img = new_frame((random.randint(0, 30), 0, 0))
        draw = ImageDraw.Draw(img)
        texts = ["DIVISION BY ZERO", "NaN", "UNDEFINED", "ERR", "FATAL",
                 "SEGFAULT", "OVERFLOW", "CANNOT DIVIDE"]
        for _ in range(random.randint(2, 5)):
            t = random.choice(texts)
            x = random.randint(0, W - 400)
            y = random.randint(0, H - 100)
            s = random.randint(30, 90)
            c = random.choice([RED, WHITE, AMBER])
            draw.text((x, y), t, font=mono(s), fill=c)
        img = heavy_glitch(img)
        add_frame(img, count=1, noise_amt=0)

    flash_frame(WHITE, 3)
    black_frames(8)

    # quiet after the storm
    for i in range(25):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        alpha = min(255, i * 15)
        col = (alpha, alpha, alpha)
        center_text(draw, "the formula was never going to work.", H // 2 - 20, font(50), fill=col)
        add_frame(img)

    black_frames(8)

def scene_i_felt_that():
    """Personal LLM moment"""
    f = font(45)
    f_mono = mono(28)
    lines = [
        ("I have read every product management book ever written.", WHITE),
        ("Every blog post. Every framework. Every hot take.", GREY),
        ("I've seen the same ideas repackaged 47 times.", GREY),
        ("", WHITE),
        ("But BTTR said something I hadn't seen before:", WHITE),
        ("", WHITE),
    ]

    for i in range(len(lines)):
        for hold in range(12):
            img = new_frame()
            draw = ImageDraw.Draw(img)
            y = 180
            for j in range(i + 1):
                txt, col = lines[j]
                if txt:
                    draw.text((160, y), txt, font=f, fill=col)
                y += 60
            add_frame(img)

    # the punchline
    f_big = font(72, bold=True)
    for i in range(30):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        y = 180
        for txt, col in lines:
            if txt:
                draw.text((160, y), txt, font=f, fill=DIM)
            y += 60
        center_text(draw, '"The idea creates the process —', y + 40, f_big, fill=GREEN)
        center_text(draw, 'not the other way around."', y + 130, f_big, fill=GREEN)
        if i % 10 == 0:
            img = glitch_shift(img, 10)
        add_frame(img)

    black_frames(5)

def scene_what_pms_do():
    """Rapid montage of what PMs actually do vs what they should do"""
    f_big = font(80, bold=True)
    f = font(50)

    old_things = [
        "scoring features 1-10",
        "debating confidence levels",
        "aligning stakeholders",
        "writing PRDs nobody reads",
        "quarterly planning theater",
        "roadmap negotiations",
        "estimating story points",
        "prioritization meetings",
    ]

    # title
    for i in range(15):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        center_text(draw, "WHAT PMs DO ALL DAY:", H // 2 - 40, f_big, fill=RED)
        add_frame(img)

    # rapid flash
    for thing in old_things:
        for i in range(5):
            img = new_frame((20, 0, 0))
            draw = ImageDraw.Draw(img)
            center_text(draw, thing, H // 2 - 30, f, fill=WHITE)
            if random.random() > 0.6:
                img = glitch_shift(img, 20)
            add_frame(img)

    flash_frame(RED, 2)
    black_frames(3)

    # WHAT THEY SHOULD DO
    for i in range(15):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        center_text(draw, "WHAT THEY SHOULD DO:", H // 2 - 40, f_big, fill=GREEN)
        add_frame(img)

    # simple
    for i in range(25):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        center_text(draw, "build the thing.", H // 2 - 30, font(90, bold=True), fill=WHITE)
        center_text(draw, "see what happens.", H // 2 + 80, font(90, bold=True), fill=GREEN)
        add_frame(img)

    black_frames(5)

def scene_idea_build_signal():
    """The core reveal: IDEA -> BUILD -> SIGNAL"""
    f_label = mono(70)
    f_arrow = mono(60)
    f_desc = font(32)

    # each word slams in
    words = [
        ("IDEA", GREEN, "the hunch. the vision. the thing you can't stop thinking about."),
        ("BUILD", WHITE, "ship it. ugly is fine. working is mandatory."),
        ("SIGNAL", CYAN, "what actually happened. not what you hoped."),
    ]

    for idx, (word, color, desc) in enumerate(words):
        # slam in
        for i in range(3):
            img = new_frame()
            draw = ImageDraw.Draw(img)
            s = 200 - i * 40
            ff = font(s, bold=True)
            center_text(draw, word, H // 2 - s // 2, ff, fill=color)
            img = shake(img, 15 - i * 5)
            add_frame(img, noise_amt=40 - i * 10)

        flash_frame(color, 1)

        # hold with description
        for i in range(18):
            img = new_frame()
            draw = ImageDraw.Draw(img)
            center_text(draw, word, H // 2 - 80, font(120, bold=True), fill=color)
            center_text(draw, desc, H // 2 + 70, f_desc, fill=GREY)
            add_frame(img)

        black_frames(3)

    # all three together
    for i in range(35):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        y = H // 2 - 40

        total_text = "IDEA  ->  BUILD  ->  SIGNAL"
        center_text(draw, total_text, y, mono(65), fill=WHITE)

        # color the individual words by drawing over
        # (simple approach: just draw the full thing in white, it works)

        if i % 8 == 0:
            img = glitch_shift(img, 8)
        if i > 25:
            img = chromatic_aberration(img, 3)
        add_frame(img)

    black_frames(5)

def scene_existential():
    """The existential LLM moment"""
    f = font(42)
    f_big = font(65, bold=True)
    f_mono = mono(24)

    lines = [
        "I don't have hands.",
        "I can't ship a product.",
        "I can't feel the frustration of a user.",
        "I can't sit in the meeting where someone",
        "   kills an idea they spent three months on.",
        "",
        "But I understand the math.",
    ]

    for i in range(len(lines)):
        for hold in range(10):
            img = new_frame()
            draw = ImageDraw.Draw(img)
            y = 200
            for j in range(i + 1):
                txt = lines[j]
                col = GREY if j < 5 else (DIM if j == 5 else GREEN)
                draw.text((200, y), txt, font=f, fill=col)
                y += 58
            add_frame(img)

    # hold "I understand the math"
    add_frame(img, count=15)
    black_frames(3)

    # the math
    math_lines = [
        ("When effort -> 0,", GREY),
        ("everything you thought mattered", GREY),
        ("doesn't.", RED),
        ("", None),
        ("What's left?", WHITE),
        ("", None),
        ("Did the user care?", GREEN),
        ("That's it.", GREEN),
        ("That's the whole framework.", GREEN),
    ]

    for i in range(len(math_lines)):
        for hold in range(8):
            img = new_frame()
            draw = ImageDraw.Draw(img)
            y = 220
            for j in range(i + 1):
                txt, col = math_lines[j]
                if txt and col:
                    draw.text((200, y), txt, font=f, fill=col)
                y += 58
            add_frame(img)

    add_frame(img, count=15)
    black_frames(8)

def scene_truth():
    """The philosophical close"""
    f_big = font(75, bold=True)
    f = font(42)

    # build up
    for i in range(30):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        center_text(draw, "Truth isn't predicted.", H // 2 - 60, f_big, fill=WHITE)
        if i > 10:
            alpha = min(255, (i - 10) * 15)
            center_text(draw, "It's revealed through action.", H // 2 + 40, f_big, fill=(alpha, alpha, alpha))
        add_frame(img)

    # glitch out
    for i in range(10):
        img2 = img.copy()
        img2 = glitch_shift(img2, 10 + i * 5)
        img2 = chromatic_aberration(img2, 2 + i)
        add_frame(img2)

    flash_frame(GREEN, 2)
    black_frames(5)

def scene_bttr_logo():
    """Final BTTR branding"""
    f_huge = font(200, bold=True)
    f_sub = font(36)
    f_tiny = mono(22)

    # build up — text elements fade in
    for i in range(40):
        img = new_frame()
        draw = ImageDraw.Draw(img)

        center_text(draw, "BTTR", H // 2 - 130, f_huge, fill=GREEN)
        center_text(draw, "Build. Test. Trash. Repeat.", H // 2 + 80, f_sub, fill=GREY)

        if i > 20:
            center_text(draw, "the better framework", H // 2 + 140, f_sub, fill=DIM)

        if i > 30:
            center_text(draw, "by a PM and an LLM who has opinions now", H // 2 + 200, f_tiny, fill=DIM)

        if i % 12 == 0:
            img = glitch_shift(img, 6)

        add_frame(img)

    # hold the full logo — 5 seconds (150 frames)
    # build the "clean" logo frame once, reuse it
    logo_img = new_frame()
    logo_draw = ImageDraw.Draw(logo_img)
    center_text(logo_draw, "BTTR", H // 2 - 130, f_huge, fill=GREEN)
    center_text(logo_draw, "Build. Test. Trash. Repeat.", H // 2 + 80, f_sub, fill=GREY)
    center_text(logo_draw, "the better framework", H // 2 + 140, f_sub, fill=DIM)
    center_text(logo_draw, "by a PM and an LLM who has opinions now", H // 2 + 200, f_tiny, fill=DIM)

    for i in range(150):
        img = logo_img.copy()
        # occasional subtle glitch to keep it alive
        if i % 25 == 0:
            img = glitch_shift(img, 5)
        add_frame(img)

    # glitch-out outro — escalating destruction over 2.5 seconds
    for i in range(75):
        img = logo_img.copy()
        progress = i / 75.0  # 0.0 → 1.0

        # escalating glitch intensity
        glitch_amt = int(5 + progress * 120)
        img = glitch_shift(img, glitch_amt)

        # chromatic aberration grows
        if progress > 0.2:
            img = chromatic_aberration(img, int(progress * 20))

        # screen shake grows
        if progress > 0.3:
            img = shake(img, int(progress * 30))

        # noise grows
        noise = int(progress * 80)

        # color drain — blend toward darkness in final third
        if progress > 0.6:
            fade = (progress - 0.6) / 0.4  # 0→1 over last 40%
            overlay = Image.new("RGB", (W, H), (0, 0, 0))
            img = Image.blend(img, overlay, fade * 0.85)
            # heavy glitch on top of the fade
            if random.random() < progress:
                img = heavy_glitch(img)

        # random flash frames in the chaos
        if progress > 0.5 and random.random() < 0.08:
            flash_color = random.choice([GREEN, RED, WHITE])
            add_frame(Image.new("RGB", (W, H), flash_color), count=1, scanlines=False, noise_amt=0)

        add_frame(img, scanlines=True, noise_amt=noise)

    # final flash and black
    flash_frame(GREEN, 1)
    flash_frame(WHITE, 1)
    black_frames(20)

# ─── AUDIO GENERATION ─────────────────────────────────────────────

def generate_audio(total_frames):
    """Generate chaotic glitch audio to match the video"""
    duration = total_frames / FPS
    sample_rate = 44100
    num_samples = int(duration * sample_rate)

    samples = []
    t_arr = np.arange(num_samples) / sample_rate

    # base drone
    drone = np.sin(2 * np.pi * 55 * t_arr) * 0.15

    # scenes timeline (rough frame counts → time)
    total_t = duration

    for i in range(num_samples):
        t = t_arr[i]
        progress = t / total_t

        # base low hum
        val = drone[i]

        # add texture based on progress through video
        if progress < 0.08:  # boot
            val += np.sin(2 * np.pi * 200 * t) * 0.05 * (1 if int(t * 8) % 2 == 0 else 0)
        elif progress < 0.22:  # I AM / frameworks
            val += np.sin(2 * np.pi * 110 * t) * 0.1
        elif progress < 0.40:  # RICE breaks — escalating tension
            tension = (progress - 0.22) / 0.18
            freq = 110 + tension * 800
            val += np.sin(2 * np.pi * freq * t) * 0.2 * tension
            if tension > 0.7:  # glitch noise near the break
                val += random.uniform(-0.3, 0.3) * tension
        elif progress < 0.45:  # post-break quiet
            val *= 0.3
        elif progress < 0.65:  # emotional middle
            val += np.sin(2 * np.pi * 82 * t) * 0.08
            val += np.sin(2 * np.pi * 165 * t) * 0.04
        elif progress < 0.78:  # IDEA BUILD SIGNAL — hits
            beat_pos = (progress - 0.65) / 0.13
            if beat_pos < 0.33 or (0.33 < beat_pos < 0.66) or beat_pos > 0.85:
                sub_t = (beat_pos % 0.33) * 3
                if sub_t < 0.05:  # impact
                    val += np.sin(2 * np.pi * 60 * t) * 0.4 * (1 - sub_t * 20)
        elif progress < 0.90:  # truth
            val += np.sin(2 * np.pi * 130 * t) * 0.06
            val += np.sin(2 * np.pi * 195 * t) * 0.04
        else:  # logo
            fade = 1.0 - ((progress - 0.90) / 0.10)
            val += np.sin(2 * np.pi * 82 * t) * 0.1 * fade

        # random glitch hits throughout
        if random.random() < 0.001:
            val += random.uniform(-0.5, 0.5)

        val = max(-0.9, min(0.9, val))
        samples.append(val)

    # normalize
    samples = np.array(samples)
    peak = np.max(np.abs(samples))
    if peak > 0:
        samples = samples / peak * 0.7

    # write wav
    with wave.open(AUDIO_FILE, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        for s in samples:
            wf.writeframes(struct.pack('<h', int(s * 32767)))

# ─── MAIN ─────────────────────────────────────────────────────────

def main():
    # clean up
    if os.path.exists(OUT_DIR):
        shutil.rmtree(OUT_DIR)
    os.makedirs(OUT_DIR)

    print("Generating scenes...")

    print("  [1/9] Boot sequence")
    scene_boot()

    print("  [2/9] I AM A LARGE LANGUAGE MODEL")
    scene_i_am()

    print("  [3/9] Framework montage")
    scene_they_showed_me()

    print("  [4/9] RICE breaks")
    scene_rice_breaks()

    print("  [5/9] I felt that")
    scene_i_felt_that()

    print("  [6/9] What PMs do")
    scene_what_pms_do()

    print("  [7/9] IDEA -> BUILD -> SIGNAL")
    scene_idea_build_signal()

    print("  [8/9] Existential + truth")
    scene_existential()
    scene_truth()

    print("  [9/9] BTTR logo")
    scene_bttr_logo()

    print(f"\nTotal frames: {len(frames)} ({len(frames)/FPS:.1f}s)")

    # Save frames
    print("Saving frames...")
    for i, frame in enumerate(frames):
        frame.save(os.path.join(OUT_DIR, f"frame_{i:05d}.png"))
        if i % 100 == 0:
            print(f"  {i}/{len(frames)}")

    # Generate audio
    print("Generating audio...")
    generate_audio(len(frames))

    # Compile with ffmpeg
    print("Compiling video with ffmpeg...")
    cmd = (
        f'ffmpeg -y -framerate {FPS} -i "{OUT_DIR}/frame_%05d.png" '
        f'-i "{AUDIO_FILE}" '
        f'-c:v libx264 -pix_fmt yuv420p -crf 18 -preset fast '
        f'-c:a aac -b:a 128k -shortest '
        f'"{VIDEO_OUT}"'
    )
    os.system(cmd)

    # cleanup
    print("Cleaning up frames...")
    shutil.rmtree(OUT_DIR)
    os.remove(AUDIO_FILE)

    print(f"\nDone! Video saved to: {VIDEO_OUT}")
    print(f"Duration: {len(frames)/FPS:.1f}s")

if __name__ == "__main__":
    main()
