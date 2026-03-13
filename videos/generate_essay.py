#!/usr/bin/env python3
"""
"Dear Junior PM" — Essay Film / Kogonada Style
A letter to your younger self about building products.
Slow, deliberate, every word earns its place.
"""

import os
import math
import struct
import wave
import shutil
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# ─── Config ───────────────────────────────────────────────────────
W, H = 1920, 1080
FPS = 24
OUT_DIR = "/Users/alexcamilar/BTTR/frames_essay"
AUDIO_FILE = "/Users/alexcamilar/BTTR/audio_essay.wav"
VIDEO_OUT = "/Users/alexcamilar/BTTR/bttr_essay.mp4"

BG = (5, 5, 5)
WHITE = (240, 240, 240)
DIM = (90, 90, 90)
FAINT = (45, 45, 45)
GREEN = (34, 197, 94)
WARM = (200, 185, 165)  # warm off-white for the letter

frames = []

# ─── Fonts ────────────────────────────────────────────────────────
def serif(size):
    """Use Georgia/Times for essay feel — fall back to Helvetica"""
    try:
        return ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", size)
    except:
        try:
            return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)
        except:
            return ImageFont.load_default()

def serif_italic(size):
    try:
        return ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Italic.ttf", size)
    except:
        try:
            return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size, index=2)
        except:
            return serif(size)

def serif_bold(size):
    try:
        return ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Bold.ttf", size)
    except:
        try:
            return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size, index=1)
        except:
            return serif(size)

def mono(size):
    try:
        return ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", size)
    except:
        return ImageFont.load_default()

# ─── Helpers ──────────────────────────────────────────────────────

def ease_out(t):
    return 1 - pow(1 - t, 3)

def new_frame():
    return Image.new("RGB", (W, H), BG)

def add_frame(img, count=1):
    for _ in range(count):
        frames.append(img.copy())

def text_width(draw, text, fnt):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    return bbox[2] - bbox[0]

def center_x(draw, text, fnt):
    return (W - text_width(draw, text, fnt)) // 2

# ─── Core animation: fade a line in, hold, fade out ───────────────

def fade_line(text, fnt, color=WHITE, y=None, hold_sec=3.0,
              fade_in_sec=1.0, fade_out_sec=0.8, gap_after_sec=0.3):
    """Single line fades in, holds, fades out."""
    if y is None:
        y = H // 2 - 15

    fade_in = int(fade_in_sec * FPS)
    hold = int(hold_sec * FPS)
    fade_out = int(fade_out_sec * FPS)
    gap = int(gap_after_sec * FPS)

    # fade in
    for i in range(fade_in):
        t = ease_out(i / max(1, fade_in - 1))
        img = new_frame()
        draw = ImageDraw.Draw(img)
        c = tuple(int(v * t) for v in color)
        x = center_x(draw, text, fnt)
        draw.text((x, y), text, font=fnt, fill=c)
        add_frame(img)

    # hold
    img = new_frame()
    draw = ImageDraw.Draw(img)
    x = center_x(draw, text, fnt)
    draw.text((x, y), text, font=fnt, fill=color)
    add_frame(img, count=hold)

    # fade out
    for i in range(fade_out):
        t = 1 - ease_out(i / max(1, fade_out - 1))
        img = new_frame()
        draw = ImageDraw.Draw(img)
        c = tuple(int(v * t) for v in color)
        x = center_x(draw, text, fnt)
        draw.text((x, y), text, font=fnt, fill=c)
        add_frame(img)

    # gap (black)
    for _ in range(gap):
        frames.append(new_frame())


def fade_two_lines(line1, line2, fnt1, fnt2, color1=WHITE, color2=WHITE,
                   y1=None, y2=None, hold_sec=3.5, stagger_sec=0.6):
    """Two lines, second staggers in after first."""
    if y1 is None:
        y1 = H // 2 - 40
    if y2 is None:
        y2 = H // 2 + 25

    fade_in = int(1.0 * FPS)
    stagger = int(stagger_sec * FPS)
    hold = int(hold_sec * FPS)
    fade_out = int(0.8 * FPS)

    total = fade_in + stagger + hold + fade_out

    for i in range(total):
        img = new_frame()
        draw = ImageDraw.Draw(img)

        # line 1
        t1 = ease_out(min(1, i / max(1, fade_in)))
        if i > fade_in + stagger + hold:
            out_i = i - (fade_in + stagger + hold)
            t1 = 1 - ease_out(min(1, out_i / max(1, fade_out)))

        c1 = tuple(int(v * t1) for v in color1)
        x1 = center_x(draw, line1, fnt1)
        draw.text((x1, y1), line1, font=fnt1, fill=c1)

        # line 2 — staggered
        if i > stagger:
            t2 = ease_out(min(1, (i - stagger) / max(1, fade_in)))
            if i > fade_in + stagger + hold:
                out_i = i - (fade_in + stagger + hold)
                t2 = 1 - ease_out(min(1, out_i / max(1, fade_out)))
            c2 = tuple(int(v * t2) for v in color2)
            x2 = center_x(draw, line2, fnt2)
            draw.text((x2, y2), line2, font=fnt2, fill=c2)

        add_frame(img)

    # gap
    for _ in range(int(0.3 * FPS)):
        frames.append(new_frame())

# ─── THE LETTER ───────────────────────────────────────────────────

def scene_letter():
    f = serif(42)
    f_italic = serif_italic(42)
    f_bold = serif_bold(42)
    f_small = serif(32)
    f_small_italic = serif_italic(32)
    f_large = serif_bold(56)
    f_mono = mono(34)

    # opening black
    for _ in range(int(2.0 * FPS)):
        frames.append(new_frame())

    # "Dear Junior PM,"
    fade_line("Dear Junior PM,", f_italic, color=WARM, hold_sec=3.0)

    # the letter
    fade_line("You're going to spend your first year", f, color=WHITE, hold_sec=2.5)
    fade_line("learning how to say no to the right things.", f, color=WHITE, hold_sec=3.0)

    fade_line("That's the wrong lesson.", f_bold, color=WHITE, hold_sec=3.0)

    # pause
    for _ in range(int(1.5 * FPS)):
        frames.append(new_frame())

    fade_two_lines(
        "The skill isn't knowing what to cut.",
        "It's knowing what to try.",
        f, f, color1=DIM, color2=WHITE, hold_sec=3.0
    )

    # pause
    for _ in range(int(1.0 * FPS)):
        frames.append(new_frame())

    fade_line("You'll build spreadsheets to rank ideas.", f, color=DIM, hold_sec=2.5)
    fade_line("You'll score them 1 to 10.", f, color=DIM, hold_sec=2.0)
    fade_line("You'll feel productive.", f, color=DIM, hold_sec=2.5)

    fade_line("You'll be wrong.", f_bold, color=WHITE, hold_sec=3.0)

    for _ in range(int(1.2 * FPS)):
        frames.append(new_frame())

    fade_two_lines(
        "Not because the scores were bad.",
        "Because scoring is not knowing.",
        f, f_bold, color1=DIM, color2=WHITE, hold_sec=3.5
    )

    for _ in range(int(1.5 * FPS)):
        frames.append(new_frame())

    # the turn
    fade_line("Here is what I wish someone had told me:", f_italic, color=WARM, hold_sec=3.5)

    for _ in range(int(1.0 * FPS)):
        frames.append(new_frame())

    fade_line("The best PMs I've ever worked with", f, color=WHITE, hold_sec=2.5)
    fade_line("are not the ones who predicted correctly.", f, color=WHITE, hold_sec=3.0)

    fade_two_lines(
        "They're the ones who found out fastest.",
        "",
        f_bold, f, color1=GREEN, hold_sec=4.0
    )

    for _ in range(int(1.5 * FPS)):
        frames.append(new_frame())

    fade_line("They shipped ugly things on Tuesday", f, color=WHITE, hold_sec=2.5)
    fade_line("and had answers by Friday.", f, color=WHITE, hold_sec=3.0)

    fade_line("While the rest of us were still aligning.", f, color=DIM, hold_sec=3.5)

    for _ in range(int(1.5 * FPS)):
        frames.append(new_frame())

    # the insight
    fade_line("You will be afraid to ship something ugly.", f, color=WHITE, hold_sec=3.0)
    fade_line("You will be afraid to kill something you built.", f, color=WHITE, hold_sec=3.0)
    fade_line("You will be afraid of being wrong in public.", f, color=WHITE, hold_sec=3.0)

    for _ in range(int(1.0 * FPS)):
        frames.append(new_frame())

    fade_two_lines(
        "But the only real failure in product",
        "is learning nothing.",
        f, f_bold, color1=DIM, color2=WHITE, hold_sec=4.0
    )

    for _ in range(int(2.0 * FPS)):
        frames.append(new_frame())

    # the framework
    fade_line("So here is the entire framework:", f_italic, color=WARM, hold_sec=2.5)

    for _ in range(int(0.8 * FPS)):
        frames.append(new_frame())

    fade_line("Have an idea.", f_large, color=GREEN, hold_sec=3.0,
              fade_in_sec=1.2)
    fade_line("Build it.", f_large, color=GREEN, hold_sec=3.0,
              fade_in_sec=1.2)
    fade_line("Read the signal.", f_large, color=GREEN, hold_sec=3.0,
              fade_in_sec=1.2)

    for _ in range(int(1.5 * FPS)):
        frames.append(new_frame())

    fade_two_lines(
        "If it works, do more.",
        "If it doesn't, do something else.",
        f, f, color1=WHITE, color2=WHITE, hold_sec=3.5
    )

    for _ in range(int(1.0 * FPS)):
        frames.append(new_frame())

    fade_line("That's it.", f_bold, color=WHITE, hold_sec=3.5)

    for _ in range(int(2.0 * FPS)):
        frames.append(new_frame())

    # the close
    fade_line("Every complicated process you'll encounter", f, color=DIM, hold_sec=2.5)
    fade_line("exists because someone was afraid", f, color=DIM, hold_sec=2.5)
    fade_line("to be wrong cheaply.", f_bold, color=WHITE, hold_sec=3.5)

    for _ in range(int(2.0 * FPS)):
        frames.append(new_frame())

    fade_line("Don't be that person.", f, color=WHITE, hold_sec=3.5)

    for _ in range(int(1.5 * FPS)):
        frames.append(new_frame())

    fade_line("Ship it. Learn. Move on.", f_italic, color=WARM, hold_sec=4.0)

    for _ in range(int(2.5 * FPS)):
        frames.append(new_frame())

    # signature
    fade_line("— You, eventually", f_small_italic, color=DIM, hold_sec=4.0,
              fade_in_sec=1.5, y=H // 2 + 10)

    for _ in range(int(3.0 * FPS)):
        frames.append(new_frame())

    # BTTR — barely there, like an afterthought
    fade_line("BTTR", serif_bold(28), color=FAINT, hold_sec=3.0,
              fade_in_sec=2.0, fade_out_sec=2.0, y=H // 2)

    # final black
    for _ in range(int(2.0 * FPS)):
        frames.append(new_frame())


# ─── AUDIO ────────────────────────────────────────────────────────

def generate_audio(total_frames):
    """
    Barely-there ambient pad. A sustained chord that evolves glacially.
    This should feel like silence with warmth — not music.
    Peak level kept very low.
    """
    duration = total_frames / FPS
    sample_rate = 44100
    num_samples = int(duration * sample_rate)
    t_arr = np.arange(num_samples) / sample_rate

    samples = np.zeros(num_samples)

    # fundamental: very low C (65.4 Hz) — felt more than heard
    samples += np.sin(2 * np.pi * 65.41 * t_arr) * 0.06

    # fifth: G (98 Hz) — adds warmth
    samples += np.sin(2 * np.pi * 98.0 * t_arr) * 0.03

    # octave: C (130.8 Hz) — very quiet
    samples += np.sin(2 * np.pi * 130.81 * t_arr) * 0.015

    # slow modulation — the chord "breathes"
    breath = np.sin(2 * np.pi * 0.04 * t_arr)  # one cycle every 25 seconds
    samples *= (0.85 + 0.15 * breath)

    # very subtle high shimmer — sine at ~523 Hz modulated slowly
    shimmer = np.sin(2 * np.pi * 523.25 * t_arr) * 0.004
    shimmer *= (0.5 + 0.5 * np.sin(2 * np.pi * 0.07 * t_arr))
    samples += shimmer

    # fade in over first 4 seconds
    fade_in_samples = int(4.0 * sample_rate)
    fade_in = np.linspace(0, 1, fade_in_samples)
    samples[:fade_in_samples] *= fade_in

    # fade out over last 5 seconds
    fade_out_samples = int(5.0 * sample_rate)
    fade_out = np.linspace(1, 0, fade_out_samples)
    samples[-fade_out_samples:] *= fade_out

    # keep it QUIET — peak at ~0.15 (very soft)
    peak = np.max(np.abs(samples))
    if peak > 0:
        samples = samples / peak * 0.15

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

    print("Generating Essay Film: 'Dear Junior PM'...")

    print("  Composing the letter...")
    scene_letter()

    print(f"\nTotal frames: {len(frames)} ({len(frames)/FPS:.1f}s)")

    print("Saving frames...")
    for i, frame in enumerate(frames):
        frame.save(os.path.join(OUT_DIR, f"frame_{i:05d}.png"))
        if i % 400 == 0:
            print(f"  {i}/{len(frames)}")

    print("Generating ambient audio...")
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
