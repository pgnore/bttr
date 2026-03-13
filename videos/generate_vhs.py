#!/usr/bin/env python3
"""
"The Last Roadmap" — VHS Analog Horror
Found footage from a company that planned itself to death.
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
FPS = 24  # VHS frame rate feel
OUT_DIR = "/Users/alexcamilar/BTTR/frames_vhs"
AUDIO_FILE = "/Users/alexcamilar/BTTR/audio_vhs.wav"
VIDEO_OUT = "/Users/alexcamilar/BTTR/bttr_vhs.mp4"

# VHS color palette — warm, desaturated
VHS_BG = (8, 5, 18)           # deep blue-black
VHS_BLUE = (20, 25, 120)      # classic VHS blue screen
VHS_WHITE = (220, 215, 200)   # warm off-white
VHS_YELLOW = (210, 195, 80)   # aged yellow
VHS_RED = (180, 40, 40)       # muted red
VHS_GREEN = (40, 160, 70)     # faded green
VHS_GREY = (130, 125, 115)    # warm grey
VHS_DIM = (60, 55, 50)
STATIC_GREY = (90, 90, 90)
CORP_BLUE = (30, 50, 100)     # corporate background

random.seed(99)
np.random.seed(99)
frames = []

# ─── Fonts ────────────────────────────────────────────────────────
def font(size, bold=False):
    try:
        return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size, index=1 if bold else 0)
    except:
        return ImageFont.load_default()

def mono(size):
    try:
        return ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", size)
    except:
        return ImageFont.load_default()

# ─── VHS Effects ──────────────────────────────────────────────────

def vhs_scanlines(img, weight=0.3):
    arr = np.array(img).astype(np.float32)
    for y in range(0, H, 2):
        arr[y] *= (1 - weight)
    return Image.fromarray(arr.clip(0, 255).astype(np.uint8))

def vhs_color_bleed(img, amount=3):
    """Shift red channel right, blue channel left — VHS chroma smear"""
    arr = np.array(img)
    result = arr.copy()
    result[:, :, 0] = np.roll(arr[:, :, 0], amount, axis=1)   # red right
    result[:, :, 2] = np.roll(arr[:, :, 2], -amount, axis=1)  # blue left
    return Image.fromarray(result)

def vhs_tracking_error(img, severity=0.3):
    """Horizontal bands displaced — the classic VHS tracking glitch"""
    arr = np.array(img)
    num_bands = int(2 + severity * 8)
    for _ in range(num_bands):
        y = random.randint(0, H - 30)
        band_h = random.randint(2, int(8 + severity * 30))
        shift = random.randint(-int(severity * 60), int(severity * 60))
        y2 = min(y + band_h, H)
        arr[y:y2] = np.roll(arr[y:y2], shift, axis=1)
        # white noise in the band
        if random.random() < severity:
            noise = np.random.randint(0, int(50 + severity * 150), (y2 - y, W, 3), dtype=np.uint8)
            arr[y:y2] = np.clip(arr[y:y2].astype(int) + noise.astype(int) - 50, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)

def vhs_noise(img, amount=15):
    arr = np.array(img).astype(np.int16)
    # VHS noise is more luminance than chroma
    lum_noise = np.random.randint(-amount, amount + 1, (H, W, 1), dtype=np.int16)
    noise = np.concatenate([lum_noise, lum_noise, lum_noise], axis=2)
    return Image.fromarray(np.clip(arr + noise, 0, 255).astype(np.uint8))

def vhs_wobble(img, frame_idx, intensity=2.0):
    """Slow horizontal wobble — VHS tape speed variation"""
    arr = np.array(img)
    for y in range(H):
        shift = int(math.sin(y * 0.01 + frame_idx * 0.15) * intensity)
        arr[y] = np.roll(arr[y], shift, axis=0)
    return Image.fromarray(arr)

def vhs_warm_tint(img, strength=0.15):
    """Add warm VHS color cast"""
    arr = np.array(img).astype(np.float32)
    arr[:, :, 0] *= (1 + strength * 0.3)   # slight red boost
    arr[:, :, 1] *= (1 + strength * 0.1)   # tiny green
    arr[:, :, 2] *= (1 - strength * 0.2)   # reduce blue
    return Image.fromarray(arr.clip(0, 255).astype(np.uint8))

def vhs_static(duration_frames):
    """Pure static — like between channels"""
    for _ in range(duration_frames):
        arr = np.random.randint(0, 100, (H, W, 3), dtype=np.uint8)
        # make it more grey/warm
        arr[:, :, 0] = (arr[:, :, 0] * 1.1).clip(0, 100).astype(np.uint8)
        img = Image.fromarray(arr)
        img = vhs_scanlines(img, 0.5)
        frames.append(img)

def apply_vhs(img, frame_idx, degradation=0.0):
    """Apply full VHS treatment. degradation 0.0-1.0 controls how damaged the tape looks."""
    img = vhs_warm_tint(img, 0.15 + degradation * 0.3)
    img = vhs_color_bleed(img, int(2 + degradation * 8))
    img = vhs_wobble(img, frame_idx, 1.5 + degradation * 6)
    img = vhs_noise(img, int(12 + degradation * 50))
    img = vhs_scanlines(img, 0.25 + degradation * 0.2)

    if degradation > 0.3 and random.random() < degradation * 0.4:
        img = vhs_tracking_error(img, degradation)

    return img

# ─── Drawing helpers ──────────────────────────────────────────────

def new_frame(bg=VHS_BG):
    return Image.new("RGB", (W, H), bg)

def text_size(draw, text, fnt):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def center_text(draw, text, y, fnt, fill=VHS_WHITE):
    tw, th = text_size(draw, text, fnt)
    draw.text(((W - tw) // 2, y), text, font=fnt, fill=fill)

def add_frame(img, count=1):
    for _ in range(count):
        frames.append(img.copy())

def draw_rec_indicator(draw, frame_idx):
    """Blinking REC indicator"""
    if (frame_idx // 18) % 2 == 0:  # blink every ~0.75s
        draw.ellipse([(60, 40), (78, 58)], fill=VHS_RED)
        draw.text((88, 36), "REC", font=mono(22), fill=VHS_RED)

def draw_timecode(draw, frame_idx, start_h=14, start_m=22):
    """VHS timecode in bottom right"""
    total_sec = frame_idx / FPS
    h = start_h
    m = start_m + int(total_sec // 60)
    s = int(total_sec) % 60
    tc = f"{h:02d}:{m:02d}:{s:02d}"
    draw.text((W - 220, H - 55), tc, font=mono(22), fill=VHS_WHITE)

def draw_date_stamp(draw):
    draw.text((W - 280, 40), "MAR 15 2019", font=mono(22), fill=VHS_YELLOW)

# ─── SCENES ───────────────────────────────────────────────────────

frame_counter = [0]  # mutable counter for VHS effects

def scene_blue_screen():
    """VHS blue screen — PROPERTY OF NEXUS SOLUTIONS"""
    f_title = font(32, bold=True)
    f_small = font(22)

    for i in range(72):  # 3 seconds
        img = new_frame(VHS_BLUE)
        draw = ImageDraw.Draw(img)

        if i > 12:
            center_text(draw, "PROPERTY OF NEXUS SOLUTIONS INC.", H // 2 - 80, f_title, fill=VHS_WHITE)
            center_text(draw, "INTERNAL USE ONLY — DO NOT DUPLICATE", H // 2 - 30, f_small, fill=VHS_GREY)
            center_text(draw, "Product Management Training Series", H // 2 + 30, f_small, fill=VHS_GREY)
            center_text(draw, "Tape 7 of 12", H // 2 + 70, f_small, fill=VHS_DIM)

        img = apply_vhs(img, frame_counter[0], 0.05)
        frame_counter[0] += 1
        add_frame(img)

    vhs_static(12)

def scene_title_card():
    """Corporate training title card"""
    f_title = font(52, bold=True)
    f_sub = font(28)
    f_small = font(22)

    for i in range(96):  # 4 seconds
        img = new_frame(CORP_BLUE)
        draw = ImageDraw.Draw(img)

        # corporate border
        draw.rectangle([(80, 60), (W - 80, H - 60)], outline=VHS_YELLOW, width=2)
        draw.rectangle([(85, 65), (W - 85, H - 65)], outline=VHS_YELLOW, width=1)

        center_text(draw, "THE PRODUCT ROADMAP PROCESS", H // 2 - 100, f_title, fill=VHS_WHITE)
        center_text(draw, "A Step-by-Step Guide for New Product Managers", H // 2 - 30, f_sub, fill=VHS_GREY)

        center_text(draw, "Presented by the Product Excellence Team", H // 2 + 60, f_small, fill=VHS_DIM)
        center_text(draw, "Q1 2019 Edition", H // 2 + 100, f_small, fill=VHS_DIM)

        draw_rec_indicator(draw, frame_counter[0])
        draw_date_stamp(draw)
        draw_timecode(draw, frame_counter[0])

        img = apply_vhs(img, frame_counter[0], 0.03)
        frame_counter[0] += 1
        add_frame(img)

    vhs_static(6)

def scene_steps_normal(step_num, title, bullets, hold_sec=3.5):
    """A normal corporate training slide"""
    f_step = font(24)
    f_title = font(42, bold=True)
    f_bullet = font(28)
    hold = int(hold_sec * FPS)

    for i in range(hold):
        img = new_frame(CORP_BLUE)
        draw = ImageDraw.Draw(img)

        # step number
        draw.text((140, 120), f"Step {step_num}", font=f_step, fill=VHS_YELLOW)
        # underline
        draw.line([(140, 158), (300, 158)], fill=VHS_YELLOW, width=1)

        # title
        draw.text((140, 180), title, font=f_title, fill=VHS_WHITE)

        # bullets appear one by one
        y = 270
        for bi, bullet in enumerate(bullets):
            appear_frame = 12 + bi * 18  # stagger
            if i >= appear_frame:
                draw.text((160, y), f"  {bullet}", font=f_bullet, fill=VHS_GREY)
            y += 50

        draw_rec_indicator(draw, frame_counter[0])
        draw_date_stamp(draw)
        draw_timecode(draw, frame_counter[0])

        img = apply_vhs(img, frame_counter[0], 0.03)
        frame_counter[0] += 1
        add_frame(img)

def scene_steps_degrading(step_num, title, bullets, degradation=0.2, hold_sec=2.5):
    """Same format but tape is degrading"""
    f_step = font(24)
    f_title = font(42, bold=True)
    f_bullet = font(28)
    hold = int(hold_sec * FPS)

    for i in range(hold):
        img = new_frame(CORP_BLUE)
        draw = ImageDraw.Draw(img)

        draw.text((140, 120), f"Step {step_num}", font=f_step, fill=VHS_YELLOW)
        draw.line([(140, 158), (300, 158)], fill=VHS_YELLOW, width=1)
        draw.text((140, 180), title, font=f_title, fill=VHS_WHITE)

        y = 270
        for bullet in bullets:
            draw.text((160, y), f"  {bullet}", font=f_bullet, fill=VHS_GREY)
            y += 50

        draw_rec_indicator(draw, frame_counter[0])
        draw_date_stamp(draw)
        draw_timecode(draw, frame_counter[0])

        # degradation increases through the hold
        d = degradation + (i / hold) * 0.15
        img = apply_vhs(img, frame_counter[0], d)
        frame_counter[0] += 1
        add_frame(img)

def scene_the_loop():
    """The horror: steps start repeating, accelerating, tape dying"""
    f_step = font(24)
    f_title = font(42, bold=True)
    f_big = font(60, bold=True)

    # the repeating steps — getting faster, more degraded
    loop_steps = [
        (6, "Re-prioritize Based on Feedback", 0.35),
        (7, "Re-align Stakeholders", 0.45),
        (8, "Update the Roadmap", 0.5),
        (9, "Present to Leadership (Again)", 0.55),
        (10, "Re-prioritize (Again)", 0.6),
        (11, "Re-align (Again)", 0.65),
        (14, "Re-prioritize...", 0.7),
        (19, "Re-align...", 0.75),
        (27, "Update...", 0.8),
        (34, "Re-...", 0.85),
        (47, "Re-...", 0.88),
        (83, "...", 0.92),
        (128, "...", 0.95),
    ]

    for step_num, title, deg in loop_steps:
        # each step gets shorter as the loop accelerates
        hold = max(10, int(48 - deg * 40))

        for i in range(hold):
            img = new_frame(CORP_BLUE)
            draw = ImageDraw.Draw(img)

            # step number getting absurd
            step_str = f"Step {step_num}"
            color = VHS_YELLOW if step_num < 15 else VHS_RED
            draw.text((140, 120), step_str, font=f_step, fill=color)
            draw.line([(140, 158), (300, 158)], fill=color, width=1)

            draw.text((140, 180), title, font=f_title, fill=VHS_WHITE)

            # at high step numbers, add desperate notes
            if step_num >= 19:
                draw.text((140, 300), "NOTE: No features have shipped this quarter.",
                         font=font(24), fill=VHS_RED)
            if step_num >= 34:
                draw.text((140, 340), "NOTE: Engineering has stopped attending meetings.",
                         font=font(24), fill=VHS_RED)
            if step_num >= 83:
                draw.text((140, 380), "NOTE: Three PMs have resigned.",
                         font=font(24), fill=VHS_RED)

            draw_rec_indicator(draw, frame_counter[0])
            draw_timecode(draw, frame_counter[0])

            img = apply_vhs(img, frame_counter[0], deg)
            frame_counter[0] += 1
            add_frame(img)

        # brief static between slides as degradation increases
        if deg > 0.6:
            vhs_static(random.randint(2, 5))

def scene_tape_breaks():
    """The tape finally gives out"""
    # heavy static with occasional corporate frames bleeding through
    f_big = font(50, bold=True)
    f_step = font(24)

    for i in range(72):  # 3 seconds of death
        if random.random() < 0.3:
            # ghost frame — a corporate slide bleeds through the static
            img = new_frame(CORP_BLUE)
            draw = ImageDraw.Draw(img)
            step = random.choice([47, 83, 128, 256, 512])
            draw.text((140, 120), f"Step {step}", font=f_step, fill=VHS_RED)
            draw.text((140, 180), "Re-prioritize...", font=f_big, fill=VHS_WHITE)
            img = apply_vhs(img, frame_counter[0], 0.95)
        else:
            # pure static
            arr = np.random.randint(0, 120, (H, W, 3), dtype=np.uint8)
            img = Image.fromarray(arr)
            img = vhs_scanlines(img, 0.4)

        frame_counter[0] += 1
        add_frame(img)

    # final blue screen
    for i in range(24):
        img = new_frame(VHS_BLUE)
        draw = ImageDraw.Draw(img)
        img = vhs_noise(img, 20)
        img = vhs_scanlines(img, 0.3)
        add_frame(img)

def scene_epilogue():
    """The reveal — what happened to Nexus Solutions"""
    f_main = font(38, bold=True)
    f_small = font(26)

    # text appears on blue screen, typed out
    lines = [
        ("Nexus Solutions filed for bankruptcy", VHS_WHITE, 1.5),
        ("in Q3 2021.", VHS_WHITE, 1.2),
        ("", None, 0.5),
        ("In two years of operation, their product team", VHS_GREY, 1.5),
        ("completed 412 roadmap revisions.", VHS_YELLOW, 1.5),
        ("", None, 0.3),
        ("They shipped zero features.", VHS_RED, 2.5),
    ]

    visible_lines = []

    for text, color, hold_sec in lines:
        visible_lines.append((text, color))
        hold = int(hold_sec * FPS)

        for i in range(hold):
            img = new_frame(VHS_BG)
            draw = ImageDraw.Draw(img)

            y = 280
            for lt, lc in visible_lines:
                if lt and lc:
                    center_text(draw, lt, y, f_main if lc != VHS_GREY else f_small, fill=lc)
                y += 55

            draw_timecode(draw, frame_counter[0])
            img = apply_vhs(img, frame_counter[0], 0.1)
            frame_counter[0] += 1
            add_frame(img)

    # hold on "shipped zero features"
    add_frame(frames[-1], count=24)

    vhs_static(8)

def scene_counter():
    """What if they had just built something?"""
    f = font(34)
    f_big = font(50, bold=True)
    f_mono = mono(28)

    lines = [
        ("What if, on day one, someone had said:", VHS_GREY),
        ("", None),
        ('"Skip the roadmap.', VHS_WHITE),
        ('Build one thing.', VHS_WHITE),
        ('See if anyone cares."', VHS_WHITE),
    ]

    for li in range(len(lines)):
        hold = 30 if lines[li][0] else 12
        for i in range(hold):
            img = new_frame(VHS_BG)
            draw = ImageDraw.Draw(img)
            y = 300
            for j in range(li + 1):
                txt, col = lines[j]
                if txt and col:
                    center_text(draw, txt, y, f if col == VHS_GREY else f_big, fill=col)
                y += 58

            img = apply_vhs(img, frame_counter[0], 0.06)
            frame_counter[0] += 1
            add_frame(img)

    add_frame(frames[-1], count=36)
    vhs_static(6)

def scene_bttr_clean():
    """Brief, clean BTTR moment — the tape clears for just a second"""
    f_huge = font(160, bold=True)
    f_sub = font(32)
    f_tiny = mono(20)

    GREEN_CLEAN = (34, 197, 94)

    # sudden clarity — clean frame (no VHS effects)
    for i in range(24):
        img = new_frame((8, 8, 8))
        draw = ImageDraw.Draw(img)
        t = min(1, i / 10)
        alpha = int(t * 255)
        c = (int(34 * t), int(197 * t), int(94 * t))
        center_text(draw, "BTTR", H // 2 - 100, f_huge, fill=c)
        if i > 8:
            t2 = min(1, (i - 8) / 10)
            c2 = (int(150 * t2), int(150 * t2), int(150 * t2))
            center_text(draw, "Build. Test. Trash. Repeat.", H // 2 + 70, f_sub, fill=c2)
        # minimal VHS — it's almost clean, like the truth broke through
        img = vhs_scanlines(img, 0.1)
        add_frame(img)

    # hold clean
    img = new_frame((8, 8, 8))
    draw = ImageDraw.Draw(img)
    center_text(draw, "BTTR", H // 2 - 100, f_huge, fill=GREEN_CLEAN)
    center_text(draw, "Build. Test. Trash. Repeat.", H // 2 + 70, f_sub, fill=(150, 150, 150))
    img = vhs_scanlines(img, 0.08)
    add_frame(img, count=96)  # 4 seconds

    # VHS reclaims — the old format pulls back
    for i in range(36):
        img2 = img.copy()
        deg = i / 36
        img2 = apply_vhs(img2, frame_counter[0], deg * 0.9)
        frame_counter[0] += 1
        add_frame(img2)

    vhs_static(18)

    # final blue screen
    for i in range(48):
        img = new_frame(VHS_BLUE)
        draw = ImageDraw.Draw(img)
        if i > 12:
            center_text(draw, "END OF TAPE", H // 2 - 20, font(30), fill=VHS_WHITE)
        img = vhs_noise(img, 15)
        img = vhs_scanlines(img, 0.3)
        t = max(0, (i - 30) / 18)
        if t > 0:
            overlay = new_frame((0, 0, 0))
            img = Image.blend(img, overlay, t)
        add_frame(img)

    # black
    for _ in range(24):
        frames.append(new_frame((0, 0, 0)))

# ─── AUDIO ────────────────────────────────────────────────────────

def generate_audio(total_frames):
    """VHS audio: tape hiss, 60Hz hum, degrading warble"""
    duration = total_frames / FPS
    sample_rate = 44100
    num_samples = int(duration * sample_rate)
    t_arr = np.arange(num_samples) / sample_rate

    samples = np.zeros(num_samples)

    # 1. Tape hiss — filtered pink noise, always present
    white = np.random.randn(num_samples)
    # simple pink noise approximation: accumulate and normalize
    pink = np.cumsum(white)
    pink = pink - np.linspace(pink[0], pink[-1], num_samples)  # remove drift
    pink = pink / (np.max(np.abs(pink)) + 1e-10)
    # high-pass to make it hissy
    for i in range(1, num_samples):
        pink[i] = 0.98 * pink[i] + 0.02 * white[i]
    pink = pink / (np.max(np.abs(pink)) + 1e-10)
    samples += pink * 0.06

    # 2. 60Hz mains hum + harmonics
    samples += np.sin(2 * np.pi * 60 * t_arr) * 0.04
    samples += np.sin(2 * np.pi * 120 * t_arr) * 0.02
    samples += np.sin(2 * np.pi * 180 * t_arr) * 0.008

    # 3. VCR motor whir — low rumble
    samples += np.sin(2 * np.pi * 30 * t_arr) * 0.03

    # 4. Degradation effects keyed to timeline
    for i in range(num_samples):
        t = t_arr[i]
        progress = t / duration

        # Normal section (0-40%): clean-ish
        if progress < 0.40:
            pass  # just base hiss and hum

        # Loop section (40-65%): increasing warble and distortion
        elif progress < 0.65:
            severity = (progress - 0.40) / 0.25
            # tape speed flutter
            flutter = math.sin(t * 8 * (1 + severity * 3)) * severity * 0.08
            samples[i] += flutter
            # increasing noise
            samples[i] += random.gauss(0, severity * 0.06)
            # occasional loud pops
            if random.random() < severity * 0.003:
                samples[i] += random.choice([-0.4, 0.4])

        # Tape breaking (65-75%): heavy noise, static
        elif progress < 0.75:
            severity = (progress - 0.65) / 0.10
            samples[i] += random.gauss(0, 0.1 + severity * 0.15)
            # buzzing
            samples[i] += np.sin(2 * np.pi * 240 * t) * severity * 0.12
            if random.random() < 0.01:
                samples[i] += random.uniform(-0.5, 0.5)

        # Epilogue (75-85%): quiet, eerie, just hiss
        elif progress < 0.85:
            samples[i] *= 0.5  # everything quieter

        # BTTR clean moment (85-95%): near silence, then tape reclaims
        elif progress < 0.95:
            inner = (progress - 0.85) / 0.10
            if inner < 0.5:
                samples[i] *= 0.15  # almost silent for clean BTTR
            else:
                reclaim = (inner - 0.5) / 0.5
                samples[i] += random.gauss(0, reclaim * 0.1)

        # End of tape (95-100%): fade to nothing
        else:
            fade = 1 - (progress - 0.95) / 0.05
            samples[i] *= fade

    # normalize
    peak = np.max(np.abs(samples))
    if peak > 0:
        samples = samples / peak * 0.55

    with wave.open(AUDIO_FILE, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        for s in samples:
            wf.writeframes(struct.pack('<h', int(max(-0.99, min(0.99, s)) * 32767)))

# ─── MAIN ─────────────────────────────────────────────────────────

def main():
    if os.path.exists(OUT_DIR):
        shutil.rmtree(OUT_DIR)
    os.makedirs(OUT_DIR)

    print("Generating VHS Analog Horror: 'The Last Roadmap'...")

    print("  [1/8] Blue screen")
    scene_blue_screen()

    print("  [2/8] Title card")
    scene_title_card()

    print("  [3/8] Normal steps (1-3)")
    scene_steps_normal(1, "Gather Requirements", [
        "Interview stakeholders across 6 departments",
        "Compile feature requests into master spreadsheet",
        "Cross-reference with competitor analysis",
        "Weight requests by stakeholder seniority",
    ], hold_sec=3.5)

    scene_steps_normal(2, "Score and Prioritize", [
        "Apply RICE framework to all 47 feature requests",
        "Debate confidence scores for 2 hours",
        "Re-score based on VP feedback",
        "Generate final ranked list",
    ], hold_sec=3.5)

    scene_steps_normal(3, "Align Stakeholders", [
        "Schedule alignment meeting (12 attendees)",
        "Present prioritized roadmap",
        "Collect feedback and objections",
        "Schedule follow-up alignment meeting",
    ], hold_sec=3.5)

    print("  [4/8] Steps start degrading (4-5)")
    scene_steps_degrading(4, "Build the Roadmap", [
        "Create Gantt chart with dependencies",
        "Add milestones and checkpoints",
        "Review with engineering for estimates",
        "Adjust timeline based on capacity",
    ], degradation=0.15)

    scene_steps_degrading(5, "Present to Leadership", [
        "Prepare 40-slide deck",
        "Rehearse presentation twice",
        'Leadership says "looks good, but..."',
        "Receive 11 pieces of contradictory feedback",
    ], degradation=0.25)

    print("  [5/8] The loop begins")
    scene_the_loop()

    print("  [6/8] Tape breaks")
    scene_tape_breaks()

    print("  [7/8] Epilogue")
    scene_epilogue()
    scene_counter()

    print("  [8/8] BTTR clean moment + end of tape")
    scene_bttr_clean()

    print(f"\nTotal frames: {len(frames)} ({len(frames)/FPS:.1f}s)")

    print("Saving frames...")
    for i, frame in enumerate(frames):
        frame.save(os.path.join(OUT_DIR, f"frame_{i:05d}.png"))
        if i % 200 == 0:
            print(f"  {i}/{len(frames)}")

    print("Generating VHS audio...")
    generate_audio(len(frames))

    print("Compiling with ffmpeg...")
    cmd = (
        f'ffmpeg -y -framerate {FPS} -i "{OUT_DIR}/frame_%05d.png" '
        f'-i "{AUDIO_FILE}" '
        f'-c:v libx264 -pix_fmt yuv420p -crf 20 -preset fast '
        f'-c:a aac -b:a 128k -shortest '
        f'"{VIDEO_OUT}"'
    )
    os.system(cmd)

    shutil.rmtree(OUT_DIR)
    os.remove(AUDIO_FILE)

    print(f"\nDone! -> {VIDEO_OUT}")
    print(f"Duration: {len(frames)/FPS:.1f}s")

if __name__ == "__main__":
    main()
