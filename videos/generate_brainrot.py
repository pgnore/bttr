#!/usr/bin/env python3
"""
"POV: You're a PM in 2024" — Brainrot / Shitpost Edit
Short, fast, bass hits, dramatic zooms, meme energy.
"""

import os
import math
import random
import struct
import wave
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageFilter
import numpy as np

# ─── Config ───────────────────────────────────────────────────────
W, H = 1080, 1920  # VERTICAL — 9:16 for Reels/TikTok/Shorts
FPS = 30
OUT_DIR = "/Users/alexcamilar/BTTR/frames_brainrot"
AUDIO_FILE = "/Users/alexcamilar/BTTR/audio_brainrot.wav"
VIDEO_OUT = "/Users/alexcamilar/BTTR/bttr_brainrot.mp4"

BG = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (34, 197, 94)
RED = (239, 68, 68)
YELLOW = (255, 220, 50)
GREY = (140, 140, 140)
DIM = (60, 60, 60)
IMPACT_SHADOW = (0, 0, 0)

random.seed(55)
np.random.seed(55)
frames = []

# ─── Fonts ────────────────────────────────────────────────────────
def impact(size):
    """Bold impact-style font"""
    try:
        return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size, index=1)
    except:
        return ImageFont.load_default()

def mono(size):
    try:
        return ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", size)
    except:
        return ImageFont.load_default()

# ─── Helpers ──────────────────────────────────────────────────────
def new_frame(bg=BG):
    return Image.new("RGB", (W, H), bg)

def add_frame(img, count=1):
    for _ in range(count):
        frames.append(img.copy())

def text_size(draw, text, fnt):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def draw_outlined(draw, text, x, y, fnt, fill=WHITE, outline=IMPACT_SHADOW, thickness=4):
    """Draw text with thick outline — the meme caption look"""
    for dx in range(-thickness, thickness + 1):
        for dy in range(-thickness, thickness + 1):
            if dx * dx + dy * dy <= thickness * thickness:
                draw.text((x + dx, y + dy), text, font=fnt, fill=outline)
    draw.text((x, y), text, font=fnt, fill=fill)

def center_outlined(draw, text, y, fnt, fill=WHITE, outline=IMPACT_SHADOW):
    tw, _ = text_size(draw, text, fnt)
    x = (W - tw) // 2
    draw_outlined(draw, text, x, y, fnt, fill, outline)

def shake(img, amount=10):
    dx = random.randint(-amount, amount)
    dy = random.randint(-amount, amount)
    return ImageChops.offset(img, dx, dy)

def zoom_crop(img, factor=1.2):
    """Zoom into center of image"""
    w, h = img.size
    nw, nh = int(w / factor), int(h / factor)
    left = (w - nw) // 2
    top = (h - nh) // 2
    cropped = img.crop((left, top, left + nw, top + nh))
    return cropped.resize((w, h), Image.LANCZOS)

def flash_frame(color=WHITE, count=2):
    for _ in range(count):
        frames.append(new_frame(color))

# ─── Slide builders ───────────────────────────────────────────────

def slam_text(lines, hold=12, bg=BG, shake_amount=0, zoom=1.0, flash_color=None):
    """
    lines: list of (text, font_size, color, y_position)
    """
    if flash_color:
        flash_frame(flash_color, 2)

    for i in range(hold):
        img = new_frame(bg)
        draw = ImageDraw.Draw(img)

        for text, size, color, y in lines:
            fnt = impact(size)
            center_outlined(draw, text, y, fnt, fill=color)

        if zoom > 1.0:
            # progressive zoom over the hold
            z = 1.0 + (zoom - 1.0) * (i / max(1, hold - 1))
            img = zoom_crop(img, z)

        if shake_amount > 0 and i < 4:
            img = shake(img, shake_amount)

        add_frame(img)

def day_slide(time_text, activity, hold=14, color=WHITE, shake_amt=0, zoom=1.0):
    """Standard day-in-the-life slide"""
    lines = [
        (time_text, 42, YELLOW, H // 2 - 120),
        (activity, 56, color, H // 2 - 20),
    ]
    slam_text(lines, hold=hold, shake_amount=shake_amt, zoom=zoom)

def counter_slide(label, number, color=RED, hold=18, shake_amt=15):
    """Big number reveal"""
    lines = [
        (label, 40, GREY, H // 2 - 100),
        (number, 140, color, H // 2 - 50),
    ]
    slam_text(lines, hold=hold, shake_amount=shake_amt, flash_color=color if color == RED else None)

# ─── SCENES ───────────────────────────────────────────────────────

def scene_opening():
    """POV title"""
    # black
    add_frame(new_frame(), count=8)

    slam_text([
        ("POV:", 50, GREY, H // 2 - 200),
        ("you're a PM", 72, WHITE, H // 2 - 100),
        ("in 2024", 72, WHITE, H // 2),
    ], hold=24)

    add_frame(new_frame(), count=4)

def scene_traditional_week():
    """The traditional PM's hellish week"""

    # Monday
    day_slide("MONDAY 9:00 AM", "Prioritization", hold=10)
    day_slide("", "meeting.", hold=10, color=GREY)

    day_slide("MONDAY 2:00 PM", "Still in the", hold=8)
    slam_text([
        ("MONDAY 2:00 PM", 42, YELLOW, H // 2 - 120),
        ("Still in the", 56, WHITE, H // 2 - 20),
        ("meeting.", 56, WHITE, H // 2 + 50),
    ], hold=12, zoom=1.15)

    # Tuesday
    day_slide("TUESDAY", "Scoring features", hold=8)
    slam_text([
        ("TUESDAY", 42, YELLOW, H // 2 - 180),
        ("Scoring features", 56, WHITE, H // 2 - 80),
        ("1 to 10.", 56, WHITE, H // 2 - 10),
        ("", 30, DIM, H // 2 + 60),
        ("\"What's our confidence", 36, GREY, H // 2 + 100),
        ("level on this one?\"", 36, GREY, H // 2 + 150),
    ], hold=18)

    # Wednesday
    day_slide("WEDNESDAY", "Aligning", hold=8)
    slam_text([
        ("WEDNESDAY", 42, YELLOW, H // 2 - 120),
        ("stakeholders.", 56, WHITE, H // 2 - 20),
        ("(12 people in the room)", 32, GREY, H // 2 + 60),
    ], hold=14)

    # Thursday
    slam_text([
        ("THURSDAY", 42, YELLOW, H // 2 - 150),
        ("VP changed", 64, WHITE, H // 2 - 60),
        ("their mind.", 64, WHITE, H // 2 + 20),
    ], hold=10, shake_amount=8)

    slam_text([
        ("re-score", 80, RED, H // 2 - 40),
        ("everything.", 80, RED, H // 2 + 60),
    ], hold=14, shake_amount=15, zoom=1.2)

    # Friday
    slam_text([
        ("FRIDAY", 42, YELLOW, H // 2 - 150),
        ("Planning the", 56, WHITE, H // 2 - 60),
        ("planning meeting", 56, WHITE, H // 2 + 20),
        ("for next week.", 56, WHITE, H // 2 + 100),
    ], hold=18)

    # THE COUNTER
    add_frame(new_frame(), count=6)

    counter_slide("features shipped this week:", "0", color=RED, hold=24, shake_amt=20)

    add_frame(new_frame(), count=8)

def scene_meanwhile():
    """The intern with Claude"""

    slam_text([
        ("meanwhile", 40, GREY, H // 2 - 100),
        ("the intern", 64, GREEN, H // 2 - 10),
        ("with Claude:", 64, GREEN, H // 2 + 70),
    ], hold=22)

    add_frame(new_frame(), count=4)

    # rapid fire — each gets faster
    slam_text([
        ("9:00 AM", 42, YELLOW, H // 2 - 100),
        ("had an idea", 60, WHITE, H // 2),
    ], hold=12)

    slam_text([
        ("10:30 AM", 42, YELLOW, H // 2 - 100),
        ("shipped it", 60, WHITE, H // 2),
    ], hold=10)

    slam_text([
        ("12:00 PM", 42, YELLOW, H // 2 - 100),
        ("got signal", 60, GREEN, H // 2),
        ("(14% activation)", 36, GREEN, H // 2 + 70),
    ], hold=12)

    slam_text([
        ("1:00 PM", 42, YELLOW, H // 2 - 100),
        ("trashed it.", 60, RED, H // 2),
        ("started the", 60, WHITE, H // 2 + 70),
        ("next one.", 60, WHITE, H // 2 + 140),
    ], hold=14, shake_amount=5)

    slam_text([
        ("3:00 PM", 42, YELLOW, H // 2 - 120),
        ("second idea", 50, WHITE, H // 2 - 30),
        ("shipped.", 50, WHITE, H // 2 + 30),
        ("26% activation.", 50, GREEN, H // 2 + 110),
    ], hold=14)

    add_frame(new_frame(), count=4)

    counter_slide("ideas tested today:", "3", color=GREEN, hold=20, shake_amt=12)

    add_frame(new_frame(), count=6)

def scene_punchline():
    """The punchline"""
    slam_text([
        ("your", 50, WHITE, H // 2 - 160),
        ("roadmap", 80, RED, H // 2 - 70),
        ("is a to-do list", 50, WHITE, H // 2 + 40),
        ("for a to-do list", 50, WHITE, H // 2 + 110),
    ], hold=24, zoom=1.1)

    flash_frame(RED, 2)
    add_frame(new_frame(), count=6)

    # the quiet truth
    slam_text([
        ("stop scoring.", 60, DIM, H // 2 - 80),
        ("start shipping.", 60, GREEN, H // 2 + 10),
    ], hold=22)

    add_frame(new_frame(), count=6)

def scene_logo():
    """BTTR logo — short"""
    slam_text([
        ("BTTR", 120, GREEN, H // 2 - 120),
        ("Build. Test. Trash. Repeat.", 32, GREY, H // 2 + 20),
    ], hold=60)  # 2 seconds

    # fade out
    base = frames[-1]
    for i in range(20):
        t = i / 20
        black = new_frame()
        img = Image.blend(base, black, t)
        add_frame(img)

    add_frame(new_frame(), count=10)

# ─── AUDIO ────────────────────────────────────────────────────────

def generate_audio(total_frames):
    """
    Trap-lite beat: 808 kicks on punchlines, hi-hat pattern, bass drops.
    Kept tight and controlled — NOT the VHS buzzing problem.
    Peak level capped at 0.4.
    """
    duration = total_frames / FPS
    sample_rate = 44100
    num_samples = int(duration * sample_rate)
    t_arr = np.arange(num_samples) / sample_rate

    samples = np.zeros(num_samples)

    def add_808(samples, time_sec, volume=0.3, duration=0.2):
        """808 kick: sine sweep from ~150Hz to ~40Hz"""
        start = int(time_sec * sample_rate)
        length = int(duration * sample_rate)
        if start + length > len(samples):
            length = len(samples) - start
        if length <= 0:
            return
        t = np.arange(length) / sample_rate
        freq = 150 * np.exp(-t * 12) + 40  # sweep down
        phase = np.cumsum(freq) / sample_rate * 2 * np.pi
        envelope = np.exp(-t * 8)
        kick = np.sin(phase) * envelope * volume
        samples[start:start + length] += kick

    def add_hihat(samples, time_sec, volume=0.04):
        """Hi-hat: short burst of filtered noise"""
        start = int(time_sec * sample_rate)
        length = int(0.03 * sample_rate)
        if start + length > len(samples):
            return
        t = np.arange(length) / sample_rate
        noise = np.random.randn(length) * volume
        envelope = np.exp(-t * 200)
        samples[start:start + length] += noise * envelope

    def add_bass_drop(samples, time_sec, volume=0.25):
        """Deep bass hit for reveals"""
        start = int(time_sec * sample_rate)
        length = int(0.4 * sample_rate)
        if start + length > len(samples):
            length = len(samples) - start
        if length <= 0:
            return
        t = np.arange(length) / sample_rate
        wave = np.sin(2 * np.pi * 45 * t) * volume
        envelope = np.exp(-t * 5)
        samples[start:start + length] += wave * envelope

    # map scenes to timeline (approximate frame counts / FPS)
    # Scene timing (cumulative seconds, approximate):
    #   opening: 0-1.5
    #   monday: 1.5-5
    #   tuesday: 5-7.5
    #   wednesday: 7.5-9
    #   thursday: 9-11
    #   friday: 11-12.5
    #   "0 shipped": 12.5-14.5
    #   meanwhile: 14.5-16
    #   intern rapid: 16-21
    #   "3 tested": 21-22.5
    #   punchline: 22.5-26
    #   logo: 26-28

    # hi-hat pattern — steady 8th notes through most of it
    bpm = 140
    beat_dur = 60.0 / bpm
    eighth = beat_dur / 2

    t = 1.0  # start after opening
    while t < duration - 2:
        add_hihat(samples, t, volume=0.03)
        t += eighth
        # skip some for variety
        if random.random() < 0.15:
            t += eighth

    # 808 kicks on key moments
    kick_times = [
        1.5,    # "prioritization meeting" lands
        3.5,    # "still in the meeting"
        5.2,    # "scoring features"
        7.5,    # "aligning stakeholders"
        9.0,    # "VP changed their mind"
        10.0,   # "re-score everything"
        11.2,   # "planning the planning meeting"
        13.0,   # "0" reveal
        15.0,   # "the intern with Claude"
        17.0,   # "shipped it"
        18.5,   # "got signal"
        19.8,   # "trashed it"
        21.5,   # "3" reveal
        23.0,   # "roadmap is a to-do list"
        25.0,   # "start shipping"
    ]
    for kt in kick_times:
        if kt < duration:
            add_808(samples, kt, volume=0.2)

    # bass drops on the big reveals
    add_bass_drop(samples, 13.0, volume=0.2)   # "0 shipped"
    add_bass_drop(samples, 21.5, volume=0.2)   # "3 tested"
    add_bass_drop(samples, 23.0, volume=0.15)  # punchline

    # fade out at end
    fade_start = int((duration - 2) * sample_rate)
    fade_len = int(2 * sample_rate)
    if fade_start + fade_len <= num_samples:
        fade = np.linspace(1, 0, fade_len)
        samples[fade_start:fade_start + fade_len] *= fade

    # normalize — keep it controlled
    peak = np.max(np.abs(samples))
    if peak > 0:
        samples = samples / peak * 0.40  # cap at 0.4

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

    print("Generating Brainrot Edit: 'POV: You're a PM in 2024'...")

    print("  [1/5] Opening")
    scene_opening()

    print("  [2/5] Traditional PM week")
    scene_traditional_week()

    print("  [3/5] Meanwhile, the intern")
    scene_meanwhile()

    print("  [4/5] Punchline")
    scene_punchline()

    print("  [5/5] Logo")
    scene_logo()

    print(f"\nTotal frames: {len(frames)} ({len(frames)/FPS:.1f}s)")

    print("Saving frames...")
    for i, frame in enumerate(frames):
        frame.save(os.path.join(OUT_DIR, f"frame_{i:05d}.png"))
        if i % 200 == 0:
            print(f"  {i}/{len(frames)}")

    print("Generating beat...")
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
