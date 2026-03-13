#!/usr/bin/env python3
"""
"bttr init" — Terminal/Hacker Aesthetic
A fictional CLI tool that roasts your roadmap and teaches BTTR.
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
FPS = 24
OUT_DIR = "/Users/alexcamilar/BTTR/frames_term"
AUDIO_FILE = "/Users/alexcamilar/BTTR/audio_term.wav"
VIDEO_OUT = "/Users/alexcamilar/BTTR/bttr_terminal.mp4"

# Terminal colors
BG = (13, 17, 23)         # GitHub dark
TITLE_BG = (30, 34, 42)   # title bar
TEXT = (201, 209, 217)     # default text
GREEN = (63, 185, 80)     # success
RED = (248, 81, 73)       # error/warning
YELLOW = (210, 153, 34)   # warning
BLUE = (88, 166, 255)     # info
CYAN = (96, 206, 206)     # accent
PURPLE = (188, 140, 255)  # commands
DIM = (110, 118, 129)     # dim text
BRIGHT = (255, 255, 255)
CURSOR_GREEN = (63, 185, 80)

random.seed(77)
np.random.seed(77)
frames = []

# ─── Fonts ────────────────────────────────────────────────────────
def mono(size):
    try:
        return ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", size)
    except:
        return ImageFont.load_default()

# ─── Helpers ──────────────────────────────────────────────────────
FONT_SIZE = 18
LINE_H = 28
MARGIN_X = 45
MARGIN_Y = 55  # below title bar
TITLE_H = 38

def new_frame():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    # title bar
    draw.rectangle([(0, 0), (W, TITLE_H)], fill=TITLE_BG)
    # traffic lights
    draw.ellipse([(16, 11), (28, 23)], fill=(255, 95, 87))
    draw.ellipse([(36, 11), (48, 23)], fill=(255, 189, 46))
    draw.ellipse([(56, 11), (68, 23)], fill=(39, 201, 63))
    # title
    draw.text((W // 2 - 60, 10), "Terminal", font=mono(14), fill=DIM)
    return img

def add_frame(img, count=1):
    for _ in range(count):
        frames.append(img.copy())

def add_subtle_glow(img):
    """Very subtle CRT-ish glow on bright pixels"""
    arr = np.array(img).astype(np.float32)
    # darken every other line slightly
    arr[::3, :, :] *= 0.95
    return Image.fromarray(arr.clip(0, 255).astype(np.uint8))

# ─── Terminal State ───────────────────────────────────────────────

class Terminal:
    def __init__(self):
        self.lines = []  # list of (text, color) tuples
        self.cursor_visible = True
        self.prompt = "~/products/pulse"

    def render(self, typing_text=None, typing_color=TEXT, show_cursor=True):
        img = new_frame()
        draw = ImageDraw.Draw(img)
        f = mono(FONT_SIZE)

        y = MARGIN_Y
        for text, color in self.lines:
            # handle long lines wrapping
            draw.text((MARGIN_X, y), text, font=f, fill=color)
            y += LINE_H
            if y > H - 40:
                # scroll: drop oldest lines
                break

        # current typing line with cursor
        if typing_text is not None:
            draw.text((MARGIN_X, y), typing_text, font=f, fill=typing_color)
            if show_cursor:
                tw = draw.textbbox((0, 0), typing_text, font=f)[2]
                draw.rectangle([(MARGIN_X + tw + 2, y + 2),
                               (MARGIN_X + tw + 12, y + LINE_H - 4)],
                              fill=CURSOR_GREEN)

        img = add_subtle_glow(img)
        return img

    def add_line(self, text, color=TEXT):
        self.lines.append((text, color))
        # keep within screen
        max_lines = (H - MARGIN_Y - 40) // LINE_H
        if len(self.lines) > max_lines:
            self.lines = self.lines[-max_lines:]

    def add_prompt(self):
        self.add_line(f"  {self.prompt} $", DIM)

    def clear(self):
        self.lines = []


term = Terminal()

# ─── Animation helpers ────────────────────────────────────────────

def type_command(cmd, color=BRIGHT, chars_per_frame=2, pre_delay=6, post_delay=12):
    """Animate typing a command character by character"""
    prompt = f"  {term.prompt} $ "

    # show empty prompt with blinking cursor
    for _ in range(pre_delay):
        img = term.render(prompt, DIM, show_cursor=True)
        add_frame(img)

    # type each character
    typed = ""
    for i in range(0, len(cmd), chars_per_frame):
        chunk = cmd[i:i + chars_per_frame]
        typed += chunk
        img = term.render(prompt + typed, DIM, show_cursor=True)
        add_frame(img)
        # occasional pause for realism
        if random.random() < 0.1:
            add_frame(img)

    # brief pause before "enter"
    for _ in range(post_delay):
        blink = (_ // 8) % 2 == 0
        img = term.render(prompt + typed, DIM, show_cursor=blink)
        add_frame(img)

    # add the command to history
    term.add_line(prompt + cmd, DIM)

def output_lines(lines_data, delay_per_line=3, extra_hold=0):
    """Output lines one at a time with delay"""
    for text, color in lines_data:
        term.add_line(text, color)
        img = term.render(show_cursor=False)
        add_frame(img, count=delay_per_line)

    if extra_hold > 0:
        add_frame(img, count=extra_hold)

def output_instant(lines_data, hold=12):
    """Output all lines at once"""
    for text, color in lines_data:
        term.add_line(text, color)
    img = term.render(show_cursor=False)
    add_frame(img, count=hold)

def blank_hold(count=12):
    img = term.render(show_cursor=False)
    add_frame(img, count=count)

def progress_bar(label, duration_frames=36, color=GREEN):
    """Animated progress bar"""
    f = mono(FONT_SIZE)
    bar_width = 40

    for i in range(duration_frames):
        progress = i / (duration_frames - 1)
        filled = int(progress * bar_width)
        bar = "[" + "#" * filled + "-" * (bar_width - filled) + "]"
        pct = f"{int(progress * 100):3d}%"

        # temporarily show progress (don't add to history)
        # remove last progress line if exists
        if term.lines and term.lines[-1][0].startswith(f"  {label}"):
            term.lines.pop()

        term.add_line(f"  {label} {bar} {pct}", color if progress < 1 else GREEN)
        img = term.render(show_cursor=False)
        add_frame(img)

# ─── SCENES ───────────────────────────────────────────────────────

def scene_open():
    """Terminal opens, user navigates to project"""
    type_command("cd ~/products/pulse", chars_per_frame=2, pre_delay=18, post_delay=6)
    blank_hold(6)

    type_command("ls", chars_per_frame=1, pre_delay=6, post_delay=4)
    output_lines([
        ("  roadmap_v14_FINAL_v3.xlsx    quarterly_planning_deck.pptx", BLUE),
        ("  feature_requests_master.csv  stakeholder_alignment_notes/", BLUE),
        ("  rice_scores_2024.xlsx        prioritization_matrix.xlsx", BLUE),
        ("  meeting_notes/               roadmap_v14_FINAL_v3_REAL.xlsx", BLUE),
    ], delay_per_line=4, extra_hold=18)

def scene_install():
    """Install bttr"""
    type_command("pip install bttr", chars_per_frame=2, pre_delay=8)
    output_lines([
        ("  Collecting bttr", DIM),
        ("    Downloading bttr-0.1.0.tar.gz (12 kB)", DIM),
    ], delay_per_line=4)

    progress_bar("Installing", duration_frames=30, color=CYAN)

    output_lines([
        ("  Successfully installed bttr-0.1.0", GREEN),
        ("", TEXT),
    ], delay_per_line=4, extra_hold=8)

def scene_init():
    """bttr init — sets up the project"""
    type_command("bttr init", chars_per_frame=2, pre_delay=8)

    output_lines([
        ("", TEXT),
        ("  ████████╗████████╗████████╗██████╗ ", GREEN),
        ("  ██╔═══██║╚══██╔══╝╚══██╔══╝██╔══██╗", GREEN),
        ("  ████████║   ██║      ██║   ██████╔╝", GREEN),
        ("  ██╔═══██║   ██║      ██║   ██╔══██╗", GREEN),
        ("  ████████║   ██║      ██║   ██║  ██║", GREEN),
        ("  ╚═══════╝   ╚═╝      ╚═╝   ╚═╝  ╚═╝", GREEN),
        ("", TEXT),
        ("  Build. Test. Trash. Repeat.            v0.1.0", DIM),
        ("", TEXT),
    ], delay_per_line=2, extra_hold=18)

    output_lines([
        ("  Initializing BTTR in ~/products/pulse...", TEXT),
        ("  Created .bttr/config.yml", DIM),
        ("  Created .bttr/cycles/", DIM),
        ("", TEXT),
        ("  Ready. Run `bttr scan` to analyze your current process.", GREEN),
        ("", TEXT),
    ], delay_per_line=4, extra_hold=8)

def scene_scan():
    """bttr scan — the roast"""
    type_command("bttr scan --roadmap *.xlsx --verbose", chars_per_frame=2, pre_delay=8)

    output_lines([
        ("", TEXT),
        ("  Scanning project artifacts...", CYAN),
    ], delay_per_line=3)

    progress_bar("Analyzing", duration_frames=42, color=CYAN)

    output_lines([
        ("", TEXT),
        ("  ═══════════════════════════════════════════════════════", DIM),
        ("  ROADMAP DIAGNOSTIC REPORT", BRIGHT),
        ("  ═══════════════════════════════════════════════════════", DIM),
        ("", TEXT),
    ], delay_per_line=3, extra_hold=8)

    # the findings — increasingly damning
    output_lines([
        ("  Features on roadmap:                  47", TEXT),
        ("  Features with success criteria:         0", RED),
        ("  Features shipped this quarter:          0", RED),
        ("  Features 'in progress' > 6 months:     12", RED),
        ("  Roadmap revision count:                14", YELLOW),
        ("  Avg. time from idea to ship:           never", RED),
        ("", TEXT),
    ], delay_per_line=6, extra_hold=6)

    output_lines([
        ("  RICE scores found:                    47", TEXT),
        ("  Confidence level = 'High':            41/47", YELLOW),
        ("  Confidence level actually validated:    0/47", RED),
        ("", TEXT),
    ], delay_per_line=6, extra_hold=8)

    output_lines([
        ("  Planning documents found:             83", TEXT),
        ("  PRDs:                                 24", DIM),
        ("  Alignment decks:                      31", DIM),
        ("  Meeting notes (prioritization):       28", DIM),
        ("  Working prototypes:                    0", RED),
        ("", TEXT),
    ], delay_per_line=5, extra_hold=8)

    # the diagnosis
    output_lines([
        ("  ─────────────────────────────────────────────────────", DIM),
        ("  DIAGNOSIS", BRIGHT),
        ("  ─────────────────────────────────────────────────────", DIM),
        ("", TEXT),
    ], delay_per_line=3, extra_hold=6)

    output_lines([
        ("  Planning velocity:    412 documents / quarter", YELLOW),
        ("  Shipping velocity:      0 features / quarter", RED),
        ("", TEXT),
        ("  Status: TERMINAL PLANNING ADDICTION", RED),
        ("", TEXT),
        ("  You have mass but no velocity.", RED),
        ("  83 documents describe things nobody has ever touched.", RED),
        ("", TEXT),
        ("  Recommendation: stop planning. start a cycle.", GREEN),
        ("", TEXT),
    ], delay_per_line=5, extra_hold=24)

def scene_cycle():
    """bttr cycle new — create first cycle"""
    type_command("bttr cycle new", chars_per_frame=2, pre_delay=12)

    output_lines([
        ("", TEXT),
        ("  Starting new BTTR cycle...", CYAN),
        ("", TEXT),
        ("  What's the idea? (describe it messy, I'll clean it up)", GREEN),
        ("", TEXT),
    ], delay_per_line=4, extra_hold=8)

    # user types their idea
    type_command(
        'bttr cycle new --idea "show users their first insight within 60s of signup"',
        chars_per_frame=2, pre_delay=6, post_delay=8
    )

    output_lines([
        ("", TEXT),
        ("  Sharpening idea...", CYAN),
        ("", TEXT),
        ("  ┌─────────────────────────────────────────────────────┐", GREEN),
        ("  │ CYCLE #1                           2024-03-15      │", GREEN),
        ("  │                                                     │", GREEN),
        ("  │ IDEA:   Show new users a personalized insight       │", GREEN),
        ("  │         within 60s of signup. Onboarding should     │", GREEN),
        ("  │         deliver value, not explain features.        │", GREEN),
        ("  │                                                     │", GREEN),
        ("  │ BUILD:  AI onboarding flow — import sample data,    │", GREEN),
        ("  │         surface personalized insight. Ship today.   │", GREEN),
        ("  │                                                     │", GREEN),
        ("  │ SIGNAL: Activation rate (baseline: 12%)             │", GREEN),
        ("  │         Target: 20%+ in 15% rollout                │", GREEN),
        ("  │                                                     │", GREEN),
        ("  │ STATUS: idea shaped                                 │", GREEN),
        ("  └─────────────────────────────────────────────────────┘", GREEN),
        ("", TEXT),
    ], delay_per_line=3, extra_hold=30)

def scene_build():
    """bttr build — the build phase"""
    type_command("bttr build --start", chars_per_frame=2, pre_delay=8)

    output_lines([
        ("", TEXT),
        ("  Timer started. Clock is ticking.", YELLOW),
        ("", TEXT),
        ("  Scope check:", CYAN),
        ("    Does the prototype need to be pretty?   NO", DIM),
        ("    Does it need production architecture?    NO", DIM),
        ("    Does it need stakeholder approval?       NO", DIM),
        ("    Does it need to get signal?              YES", GREEN),
        ("", TEXT),
        ("  Ship when it works. Not when it's perfect.", GREEN),
        ("", TEXT),
    ], delay_per_line=4, extra_hold=18)

    # time skip
    term.add_line("", TEXT)
    term.add_line("  . . .", DIM)
    term.add_line("", TEXT)
    img = term.render(show_cursor=False)
    add_frame(img, count=18)

    type_command("bttr build --complete", chars_per_frame=2, pre_delay=8)

    output_lines([
        ("", TEXT),
        ("  Build completed in 4h 23m.", GREEN),
        ("  Deployed to 15% of new signups via feature flag.", CYAN),
        ("", TEXT),
        ("  Time from idea to live users: 4 hours.", GREEN),
        ("  Time previously spent planning this feature: 6 weeks.", RED),
        ("", TEXT),
    ], delay_per_line=5, extra_hold=24)

def scene_signal():
    """bttr signal — reading results"""
    type_command("bttr signal --read --days 4", chars_per_frame=2, pre_delay=12)

    output_lines([
        ("", TEXT),
        ("  Fetching signal data...", CYAN),
    ], delay_per_line=4)

    progress_bar("Collecting", duration_frames=30, color=CYAN)

    output_lines([
        ("", TEXT),
        ("  ═══════════════════════════════════════════════════════", DIM),
        ("  SIGNAL REPORT — Cycle #1 (4 days)", BRIGHT),
        ("  ═══════════════════════════════════════════════════════", DIM),
        ("", TEXT),
        ("  Activation rate (control):     12.1%", DIM),
        ("  Activation rate (test group):  14.3%", YELLOW),
        ("  Target:                        20.0%", DIM),
        ("  Verdict:                       BELOW TARGET", YELLOW),
        ("", TEXT),
    ], delay_per_line=5, extra_hold=12)

    output_lines([
        ("  But wait —", BRIGHT),
        ("", TEXT),
        ("  Users who completed the insight:      38.2% activation", GREEN),
        ("  Users who skipped the insight:          8.1% activation", RED),
        ("", TEXT),
        ("  60% of users skipped — the UI buried it.", YELLOW),
        ("  The idea works. The shape doesn't.", CYAN),
        ("", TEXT),
    ], delay_per_line=6, extra_hold=18)

def scene_decide():
    """bttr decide — the iterate/pivot/trash decision"""
    type_command("bttr decide", chars_per_frame=2, pre_delay=10)

    output_lines([
        ("", TEXT),
        ("  ┌──────────────────────────────────────────────┐", CYAN),
        ("  │              DECISION TIME                   │", CYAN),
        ("  ├──────────────────────────────────────────────┤", CYAN),
        ("  │                                              │", CYAN),
        ("  │  [1] ITERATE  — right idea, wrong shape      │", GREEN),
        ("  │  [2] PIVOT    — wrong idea, new direction     │", YELLOW),
        ("  │  [3] TRASH    — no signal, move on            │", RED),
        ("  │                                              │", CYAN),
        ("  └──────────────────────────────────────────────┘", CYAN),
        ("", TEXT),
        ("  Signal says: right idea, wrong shape.", GREEN),
        ("  Users who see the insight love it. Most don't see it.", GREEN),
        ("", TEXT),
        ("  Recommendation: ITERATE", GREEN),
        ("  Next build: make the insight un-skippable.", GREEN),
        ("", TEXT),
    ], delay_per_line=4, extra_hold=12)

    type_command("1", chars_per_frame=1, pre_delay=8, post_delay=4)

    output_lines([
        ("", TEXT),
        ("  ┌─────────────────────────────────────────────────────┐", GREEN),
        ("  │ CYCLE #1 COMPLETE          2024-03-15 > 2024-03-19 │", GREEN),
        ("  │                                                     │", GREEN),
        ("  │ IDEA:     Personalized insight in first 60 seconds  │", GREEN),
        ("  │ BUILD:    AI onboarding flow (shipped in 4 hours)   │", GREEN),
        ("  │ SIGNAL:   14.3% overall, 38.2% for completers      │", GREEN),
        ("  │ DECISION: ITERATE — make insight un-skippable       │", GREEN),
        ("  │                                                     │", GREEN),
        ("  │ LEARNED:  The value lands. The packaging doesn't.   │", CYAN),
        ("  └─────────────────────────────────────────────────────┘", GREEN),
        ("", TEXT),
        ("  Cycle #2 initialized. Run `bttr cycle start` when ready.", DIM),
        ("", TEXT),
    ], delay_per_line=3, extra_hold=30)

def scene_version():
    """The punchline"""
    type_command("bttr --version", chars_per_frame=2, pre_delay=18)

    output_lines([
        ("", TEXT),
        ("  bttr v0.1.0", GREEN),
        ("  The Better Framework", DIM),
        ("", TEXT),
        ("  This tool was built in 2 hours.", DIM),
        ("  Using BTTR itself.", DIM),
        ("", TEXT),
        ("  The idea creates the process —", GREEN),
        ("  not the other way around.", GREEN),
        ("", TEXT),
    ], delay_per_line=6, extra_hold=12)

    # final prompt — cursor blinking, waiting
    term.add_prompt()
    for i in range(96):  # 4 seconds
        blink = (i // 10) % 2 == 0
        img = term.render(typing_text=f"  {term.prompt} $ ", typing_color=DIM, show_cursor=blink)
        add_frame(img)

    # fade to black
    last = frames[-1]
    for i in range(36):
        t = i / 36
        black = Image.new("RGB", (W, H), (0, 0, 0))
        img = Image.blend(last, black, t)
        add_frame(img)

    for _ in range(18):
        frames.append(Image.new("RGB", (W, H), (0, 0, 0)))

# ─── AUDIO ────────────────────────────────────────────────────────

def generate_audio(total_frames):
    """Terminal audio: keyboard clicks, subtle room tone, no music"""
    duration = total_frames / FPS
    sample_rate = 44100
    num_samples = int(duration * sample_rate)
    t_arr = np.arange(num_samples) / sample_rate

    samples = np.zeros(num_samples)

    # 1. Room tone — very subtle low-frequency presence
    samples += np.random.randn(num_samples) * 0.003  # barely there noise floor

    # 2. Computer fan — extremely subtle constant tone
    samples += np.sin(2 * np.pi * 120 * t_arr) * 0.004
    samples += np.sin(2 * np.pi * 240 * t_arr) * 0.002

    # 3. Keyboard typing sounds — synthesized click patterns
    # Generate click at specific times based on frame-to-time mapping
    # A "click" is a short burst of filtered noise

    def add_click(samples, time_sec, volume=0.15):
        """Add a synthetic keypress click at a given time"""
        start = int(time_sec * sample_rate)
        click_len = int(0.008 * sample_rate)  # 8ms
        if start + click_len >= len(samples):
            return
        # sharp attack, fast decay
        t = np.arange(click_len) / sample_rate
        click = np.random.randn(click_len) * volume
        envelope = np.exp(-t * 800)  # fast decay
        click *= envelope
        # add a subtle tonal component (key bottoming out)
        click += np.sin(2 * np.pi * 3200 * t) * volume * 0.3 * envelope
        samples[start:start + click_len] += click

    def add_enter(samples, time_sec, volume=0.2):
        """Slightly different sound for enter key"""
        start = int(time_sec * sample_rate)
        click_len = int(0.02 * sample_rate)  # 20ms — heavier
        if start + click_len >= len(samples):
            return
        t = np.arange(click_len) / sample_rate
        click = np.random.randn(click_len) * volume
        envelope = np.exp(-t * 400)
        click *= envelope
        click += np.sin(2 * np.pi * 1800 * t) * volume * 0.4 * envelope
        samples[start:start + click_len] += click

    def add_beep(samples, time_sec, freq=880, dur=0.05, volume=0.06):
        """Terminal beep"""
        start = int(time_sec * sample_rate)
        length = int(dur * sample_rate)
        if start + length >= len(samples):
            return
        t = np.arange(length) / sample_rate
        envelope = np.ones(length)
        fade = min(length, int(0.005 * sample_rate))
        envelope[:fade] = np.linspace(0, 1, fade)
        envelope[-fade:] = np.linspace(1, 0, fade)
        samples[start:start + length] += np.sin(2 * np.pi * freq * t) * volume * envelope

    # walk through frames and add clicks where typing happens
    # approximate typing regions (in seconds):
    typing_regions = [
        (0.5, 2.5),     # cd command
        (3.5, 4.0),     # ls
        (6.5, 8.5),     # pip install
        (12.0, 13.0),   # bttr init
        (20.5, 22.0),   # bttr scan
        (36.0, 40.0),   # bttr cycle new --idea
        (48.0, 49.5),   # bttr build --start
        (55.0, 56.5),   # bttr build --complete
        (62.0, 64.0),   # bttr signal --read
        (74.0, 75.0),   # bttr decide
        (77.0, 77.3),   # "1"
        (86.0, 87.5),   # bttr --version
    ]

    for start, end in typing_regions:
        t = start
        while t < end:
            add_click(samples, t, volume=random.uniform(0.08, 0.18))
            t += random.uniform(0.04, 0.12)  # variable typing speed
        # enter at end
        add_enter(samples, end + 0.05)

    # beeps at key moments
    add_beep(samples, 14.5, freq=660, dur=0.08)   # bttr init banner
    add_beep(samples, 28.0, freq=440, dur=0.1)    # diagnosis
    add_beep(samples, 45.0, freq=880, dur=0.06)   # cycle created
    add_beep(samples, 59.0, freq=660, dur=0.08)   # build complete
    add_beep(samples, 68.0, freq=440, dur=0.1)    # signal "but wait"
    add_beep(samples, 82.0, freq=880, dur=0.06)   # cycle complete

    # 4. Subtle hard drive activity during "processing" sections
    processing_regions = [(9.0, 11.0), (22.5, 25.0), (64.5, 66.0)]
    for ps, pe in processing_regions:
        for i in range(num_samples):
            t = t_arr[i]
            if ps < t < pe:
                # random clicking/seeking sounds
                if random.random() < 0.003:
                    click_len = min(int(0.003 * sample_rate), num_samples - i)
                    samples[i:i + click_len] += np.random.randn(click_len) * 0.02

    # normalize
    peak = np.max(np.abs(samples))
    if peak > 0:
        samples = samples / peak * 0.6

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

    print("Generating Terminal video: 'bttr init'...")

    print("  [1/8] Open terminal")
    scene_open()

    print("  [2/8] Install bttr")
    scene_install()

    print("  [3/8] bttr init")
    scene_init()

    print("  [4/8] bttr scan (the roast)")
    scene_scan()

    print("  [5/8] bttr cycle new")
    scene_cycle()

    print("  [6/8] bttr build")
    scene_build()

    print("  [7/8] bttr signal")
    scene_signal()

    print("  [8/8] bttr decide + version")
    scene_decide()
    scene_version()

    print(f"\nTotal frames: {len(frames)} ({len(frames)/FPS:.1f}s)")

    print("Saving frames...")
    for i, frame in enumerate(frames):
        frame.save(os.path.join(OUT_DIR, f"frame_{i:05d}.png"))
        if i % 300 == 0:
            print(f"  {i}/{len(frames)}")

    print("Generating terminal audio...")
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
