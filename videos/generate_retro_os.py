#!/usr/bin/env python3
"""
"Upgrade Your PM OS" — Retro OS / Windows 95 Style
A fake operating system boots up, tries to run "Roadmap.exe",
crashes through increasingly absurd error dialogs, then
upgrades to BTTR OS.
"""

import os
import math
import random
import struct
import wave
import shutil
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# --- Config ---
W, H = 1920, 1080
FPS = 24
OUT_DIR = "/Users/alexcamilar/BTTR/frames_retro"
AUDIO_FILE = "/Users/alexcamilar/BTTR/audio_retro.wav"
VIDEO_OUT = "/Users/alexcamilar/BTTR/bttr_retro_os.mp4"

# Windows 95 palette
TEAL_BG = (0, 128, 128)
GREY_BG = (192, 192, 192)
TITLE_BLUE = (0, 0, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREY = (128, 128, 128)
LIGHT_GREY = (223, 223, 223)
RED = (200, 0, 0)
BTTR_GREEN = (34, 197, 94)
BSOD_BLUE = (0, 0, 170)

random.seed(42)
np.random.seed(42)
frames = []

# --- Fonts ---
def sys_font(size):
    """MS Sans Serif vibe — Helvetica is close enough"""
    try:
        return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size, index=0)
    except:
        return ImageFont.load_default()

def sys_bold(size):
    try:
        return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size, index=1)
    except:
        return sys_font(size)

def mono(size):
    try:
        return ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", size)
    except:
        return ImageFont.load_default()

# --- Helpers ---
def new_frame(bg=TEAL_BG):
    return Image.new("RGB", (W, H), bg)

def add_frame(img, count=1):
    for _ in range(count):
        frames.append(img.copy())

def text_size(draw, text, fnt):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def center_text(draw, text, fnt, y, fill=BLACK):
    tw, _ = text_size(draw, text, fnt)
    x = (W - tw) // 2
    draw.text((x, y), text, font=fnt, fill=fill)

# --- Win95 UI Components ---

def draw_bevel_rect(draw, x, y, w, h, raised=True):
    """Draw a beveled rectangle — the Win95 3D look"""
    tl = WHITE if raised else DARK_GREY
    br = DARK_GREY if raised else WHITE
    # fill
    draw.rectangle([x, y, x + w, y + h], fill=GREY_BG)
    # top & left highlight
    draw.line([(x, y), (x + w, y)], fill=tl)
    draw.line([(x, y), (x, y + h)], fill=tl)
    draw.line([(x + 1, y + 1), (x + w - 1, y + 1)], fill=tl)
    draw.line([(x + 1, y + 1), (x + 1, y + h - 1)], fill=tl)
    # bottom & right shadow
    draw.line([(x, y + h), (x + w, y + h)], fill=br)
    draw.line([(x + w, y), (x + w, y + h)], fill=br)
    draw.line([(x + 1, y + h - 1), (x + w - 1, y + h - 1)], fill=br)
    draw.line([(x + w - 1, y + 1), (x + w - 1, y + h - 1)], fill=br)

def draw_button(draw, x, y, w, h, text, pressed=False):
    """Draw a Win95-style button"""
    draw_bevel_rect(draw, x, y, w, h, raised=not pressed)
    fnt = sys_font(14)
    tw, th = text_size(draw, text, fnt)
    tx = x + (w - tw) // 2 + (1 if pressed else 0)
    ty = y + (h - th) // 2 + (1 if pressed else 0)
    draw.text((tx, ty), text, font=fnt, fill=BLACK)

def draw_window(draw, x, y, w, h, title, active=True):
    """Draw a Win95-style window frame"""
    # outer bevel
    draw_bevel_rect(draw, x, y, w, h, raised=True)
    # title bar
    tb_color = TITLE_BLUE if active else DARK_GREY
    draw.rectangle([x + 3, y + 3, x + w - 3, y + 23], fill=tb_color)
    fnt = sys_bold(14)
    draw.text((x + 6, y + 5), title, font=fnt, fill=WHITE)
    # close button
    bx = x + w - 22
    draw_bevel_rect(draw, bx, y + 5, 16, 14, raised=True)
    draw.text((bx + 3, y + 4), "x", font=sys_font(12), fill=BLACK)
    # content area (inset)
    draw.rectangle([x + 3, y + 26, x + w - 3, y + h - 3], fill=WHITE,
                    outline=DARK_GREY)
    return (x + 5, y + 28)  # content origin

def draw_error_dialog(img, title, message, buttons=["OK"], icon="error",
                      cx=None, cy=None, width=420, height=180):
    """Draw a Win95 error dialog centered on screen"""
    draw = ImageDraw.Draw(img)
    if cx is None:
        cx = (W - width) // 2
    if cy is None:
        cy = (H - height) // 2

    # window
    content_origin = draw_window(draw, cx, cy, width, height, title)
    ox, oy = content_origin

    # icon area
    icon_x = ox + 10
    icon_y = oy + 15
    if icon == "error":
        # red circle with X
        draw.ellipse([icon_x, icon_y, icon_x + 32, icon_y + 32], fill=RED)
        draw.text((icon_x + 9, icon_y + 5), "X", font=sys_bold(18), fill=WHITE)
    elif icon == "warning":
        # yellow triangle
        pts = [(icon_x + 16, icon_y), (icon_x, icon_y + 32), (icon_x + 32, icon_y + 32)]
        draw.polygon(pts, fill=(255, 255, 0), outline=BLACK)
        draw.text((icon_x + 11, icon_y + 10), "!", font=sys_bold(16), fill=BLACK)
    elif icon == "info":
        draw.ellipse([icon_x, icon_y, icon_x + 32, icon_y + 32], fill=TITLE_BLUE)
        draw.text((icon_x + 12, icon_y + 5), "i", font=sys_bold(18), fill=WHITE)

    # message text — wrap manually
    fnt = sys_font(15)
    lines = message.split("\n")
    ty = oy + 12
    for line in lines:
        draw.text((ox + 55, ty), line, font=fnt, fill=BLACK)
        ty += 20

    # buttons
    btn_w = 80
    btn_h = 26
    total_btn_w = len(buttons) * btn_w + (len(buttons) - 1) * 10
    btn_x = cx + (width - total_btn_w) // 2
    btn_y = cy + height - 42
    for btn_text in buttons:
        draw_button(draw, btn_x, btn_y, btn_w, btn_h, btn_text)
        btn_x += btn_w + 10

    return img

def draw_progress_bar(draw, x, y, w, h, progress, label=None):
    """Win95 progress bar"""
    # sunken rect
    draw.rectangle([x, y, x + w, y + h], fill=WHITE, outline=DARK_GREY)
    draw.line([(x, y), (x + w, y)], fill=DARK_GREY)
    draw.line([(x, y), (x, y + h)], fill=DARK_GREY)
    # fill
    fill_w = int((w - 2) * progress)
    if fill_w > 0:
        draw.rectangle([x + 1, y + 1, x + 1 + fill_w, y + h - 1], fill=TITLE_BLUE)
    if label:
        fnt = sys_font(12)
        tw, th = text_size(draw, label, fnt)
        draw.text((x + (w - tw) // 2, y + (h - th) // 2), label, font=fnt,
                  fill=BLACK if progress < 0.5 else WHITE)


# --- SCENES ---

def scene_boot():
    """Fake BIOS boot sequence"""
    boot_lines = [
        "PM-BIOS v4.2 (c) 2019 Legacy Systems Inc.",
        "",
        "Detecting installed frameworks...",
        "  RICE Score Engine............ OK",
        "  WSJF Calculator.............. OK",
        "  ICE Prioritizer.............. OK",
        "  Stakeholder Alignment Bus.... OK",
        "  Roadmap Rendering Engine..... OK",
        "",
        "Memory Test: 640K meetings ought to be enough for anybody",
        "",
        "Loading PM_OS v3.1...",
    ]

    fnt = mono(16)
    for line_idx in range(len(boot_lines)):
        img = new_frame(BLACK)
        draw = ImageDraw.Draw(img)
        y = 40
        for i in range(line_idx + 1):
            draw.text((40, y), boot_lines[i], font=fnt, fill=(0, 255, 0))
            y += 22
        # cursor blink
        draw.text((40, y), "_", font=fnt, fill=(0, 255, 0))
        hold = 3 if line_idx < 6 else 6 if "Loading" in boot_lines[line_idx] else 4
        add_frame(img, count=hold)

    # "Loading" with dots animation
    for dots in range(8):
        img = new_frame(BLACK)
        draw = ImageDraw.Draw(img)
        y = 40
        for i, line in enumerate(boot_lines[:-1]):
            draw.text((40, y), line, font=fnt, fill=(0, 255, 0))
            y += 22
        draw.text((40, y), boot_lines[-1] + "." * (dots % 4), font=fnt, fill=(0, 255, 0))
        add_frame(img, count=4)


def scene_desktop():
    """Teal desktop with taskbar, icons appear"""
    # base desktop
    def draw_desktop(draw, show_icons=True):
        # taskbar
        draw_bevel_rect(draw, 0, H - 36, W, 36, raised=True)
        # start button
        draw_bevel_rect(draw, 4, H - 32, 70, 28, raised=True)
        fnt = sys_bold(14)
        draw.text((14, H - 26), "Start", font=fnt, fill=BLACK)
        # clock
        fnt_sm = sys_font(13)
        draw.text((W - 60, H - 26), "9:00 AM", font=fnt_sm, fill=BLACK)

        if show_icons:
            # desktop icons
            icons = [
                ("Roadmap.exe", 40, 30),
                ("Priorities.xls", 40, 120),
                ("Meetings.doc", 40, 210),
                ("Alignment.ppt", 40, 300),
            ]
            fnt_icon = sys_font(12)
            for name, ix, iy in icons:
                # icon square
                draw.rectangle([ix, iy, ix + 40, iy + 40], fill=GREY_BG, outline=DARK_GREY)
                draw.rectangle([ix + 5, iy + 5, ix + 35, iy + 35], fill=WHITE, outline=DARK_GREY)
                # file type indicator
                ext = name.split(".")[-1]
                draw.text((ix + 10, iy + 12), ext[:3], font=sys_font(11), fill=TITLE_BLUE)
                # label
                tw, _ = text_size(draw, name, fnt_icon)
                lx = ix + 20 - tw // 2
                draw.text((lx, iy + 44), name, font=fnt_icon, fill=WHITE)

    # desktop appears
    for i in range(18):
        img = new_frame(TEAL_BG)
        draw = ImageDraw.Draw(img)
        draw_desktop(draw, show_icons=(i > 6))
        add_frame(img)

    # hold on desktop
    img = new_frame(TEAL_BG)
    draw = ImageDraw.Draw(img)
    draw_desktop(draw)
    add_frame(img, count=24)

    return img


def scene_roadmap_exe():
    """Double-click Roadmap.exe — it tries to load"""
    # "Opening Roadmap.exe..." window with progress bar
    for progress_pct in range(0, 76, 2):
        img = new_frame(TEAL_BG)
        draw = ImageDraw.Draw(img)
        # taskbar
        draw_bevel_rect(draw, 0, H - 36, W, 36, raised=True)
        draw_bevel_rect(draw, 4, H - 32, 70, 28, raised=True)
        draw.text((14, H - 26), "Start", font=sys_bold(14), fill=BLACK)

        # loading window
        wx, wy = 500, 350
        ww, wh = 500, 160
        draw_window(draw, wx, wy, ww, wh, "Roadmap.exe")

        fnt = sys_font(14)
        draw.text((wx + 20, wy + 40), "Loading Q3 2024 Roadmap...", font=fnt, fill=BLACK)
        draw.text((wx + 20, wy + 62), "Aligning stakeholders: " + str(progress_pct) + "%",
                  font=fnt, fill=BLACK)

        draw_progress_bar(draw, wx + 20, wy + 90, ww - 50, 20, progress_pct / 100,
                          label=f"{progress_pct}%")

        add_frame(img)

    # FREEZE at 74% — hold for dramatic effect
    img_frozen = frames[-1].copy()
    add_frame(img_frozen, count=30)


def scene_error_cascade():
    """Cascade of increasingly absurd error dialogs"""
    errors = [
        ("Roadmap.exe - Error", "Roadmap.exe has encountered a problem.\n\nReason: Too many priorities (found 847).\nExpected: 3-5 priorities.", ["OK"], "error"),
        ("Priority Conflict", "FATAL: Feature #421 scored 8.5 AND 3.2\ndepending on who you ask.\n\nWould you like to schedule a meeting?", ["Yes", "Also Yes"], "warning"),
        ("Stakeholder Alignment Service", "Cannot align stakeholders.\n\n12 people need to approve.\n11 are in other meetings.\n1 is 'thinking about it.'", ["Wait", "Wait More"], "error"),
        ("RICE Score Overflow", "RICE Score calculation failed.\n\nDivision by zero in Effort field.\nEffort was estimated as 'basically free'\nbut took 6 months.", ["Cry", "Resign"], "error"),
        ("Meeting Recursion Error", "Stack overflow in Meeting.exe\n\nThis meeting is to plan the meeting\nthat plans the planning meeting.\n\nRecursion depth: 47", ["OK"], "error"),
        ("Confidence Interval Warning", "WARNING: Confidence score is\nstatistically indistinguishable from\na random number generator.\n\nContinue anyway?", ["Sure", "Why Not"], "warning"),
    ]

    base_img = frames[-1].copy()

    for idx, (title, msg, btns, icon) in enumerate(errors):
        # each error offsets slightly for cascade effect
        offset_x = 80 + idx * 30
        offset_y = 60 + idx * 25
        w = 440 if idx < 3 else 460
        h = 190

        img = base_img.copy()
        draw_error_dialog(img, title, msg, btns, icon,
                          cx=(W - w) // 2 + offset_x - 150,
                          cy=(H - h) // 2 + offset_y - 100,
                          width=w, height=h)
        base_img = img.copy()
        add_frame(img, count=28)

    # rapid additional popups
    extra_titles = [
        "Error", "Error (2)", "Error (3)", "Something Went Wrong",
        "Really Wrong", "So Wrong", "Help", "HELP", "PLEASE",
    ]
    for i, t in enumerate(extra_titles):
        img = base_img.copy()
        rx = random.randint(100, W - 500)
        ry = random.randint(50, H - 250)
        draw_error_dialog(img, t, "An error occurred in an error\nabout an error.\n\nThis is fine.",
                          ["OK"], "error", cx=rx, cy=ry, width=380, height=160)
        base_img = img.copy()
        add_frame(img, count=4)

    # hold on the chaos
    add_frame(base_img, count=20)


def scene_bsod():
    """Blue Screen of Death"""
    img = new_frame(BSOD_BLUE)
    draw = ImageDraw.Draw(img)
    fnt = mono(18)
    fnt_sm = mono(14)

    lines = [
        "PM_OS v3.1",
        "",
        "A fatal exception has occurred in ROADMAP.EXE",
        "",
        "The current prioritization framework has performed an",
        "illegal operation and will be shut down.",
        "",
        "Error: RICE_SCORE_MEANINGLESS (0x00000000)",
        "  at PrioritizationEngine.score()",
        "  at MeetingScheduler.align()",
        "  at RoadmapBuilder.build()",
        "  at QuarterlyPlanning.plan()",
        "  at QuarterlyPlanning.planThePlan()",
        "  at QuarterlyPlanning.planThePlanForThePlan()",
        "",
        "* Press any key to install a better framework.",
        "* Or press CTRL+ALT+DEL to schedule another meeting.",
        "",
        "Press any key to continue...",
    ]

    y = 80
    for line in lines:
        draw.text((80, y), line, font=fnt if "PM_OS" in line or "fatal" in line else fnt_sm,
                  fill=WHITE)
        y += 26

    add_frame(img, count=72)  # 3 seconds to read

    # flicker
    for _ in range(6):
        add_frame(new_frame(BLACK), count=2)
        add_frame(img, count=2)

    add_frame(new_frame(BLACK), count=12)


def scene_upgrade():
    """BTTR OS boots up — clean, green, modern"""
    fnt = mono(16)
    fnt_lg = mono(24)

    # boot text
    boot_lines = [
        "Installing BTTR OS v1.0...",
        "",
        "Removing unnecessary frameworks:",
        "  [-] RICE Score Engine........... removed",
        "  [-] WSJF Calculator............. removed",
        "  [-] ICE Prioritizer............. removed",
        "  [-] Stakeholder Alignment Bus... removed",
        "",
        "Installing BTTR components:",
        "  [+] Build Engine................ installed",
        "  [+] Signal Reader............... installed",
        "  [+] Trash Collector............. installed",
        "  [+] Repeat Scheduler............ installed",
        "",
        "Configuration:",
        "  Effort estimation:  DISABLED (AI builds everything)",
        "  Meeting scheduler:  DISABLED (ship instead)",
        "  Score calculator:   DISABLED (test instead)",
        "",
        "BTTR OS ready.",
    ]

    for line_idx in range(len(boot_lines)):
        img = new_frame(BLACK)
        draw = ImageDraw.Draw(img)
        y = 60
        for i in range(line_idx + 1):
            line = boot_lines[i]
            color = BTTR_GREEN if "[+]" in line or "ready" in line.lower() else \
                    RED if "[-]" in line or "DISABLED" in line else \
                    (0, 200, 0)
            draw.text((60, y), line, font=fnt, fill=color)
            y += 24
        hold = 2 if "[-]" in boot_lines[line_idx] or "[+]" in boot_lines[line_idx] else 5
        if "ready" in boot_lines[line_idx].lower():
            hold = 20
        add_frame(img, count=hold)

    add_frame(new_frame(BLACK), count=12)


def scene_bttr_desktop():
    """New clean desktop — BTTR OS"""
    def draw_bttr_desktop(draw, cycle_state=None):
        # dark background instead of teal
        # (already black from new_frame)

        # minimal taskbar — dark, clean
        draw.rectangle([0, H - 36, W, H], fill=(20, 20, 20))
        draw.line([(0, H - 36), (W, H - 36)], fill=BTTR_GREEN)

        # BTTR logo in taskbar
        fnt = sys_bold(14)
        draw.text((14, H - 26), "BTTR", font=fnt, fill=BTTR_GREEN)

        # clock
        draw.text((W - 80, H - 26), "9:15 AM", font=sys_font(13), fill=(100, 100, 100))

        # single window: "BTTR Cycle"
        # dark window style
        wx, wy = 400, 150
        ww, wh = 700, 500
        draw.rectangle([wx, wy, wx + ww, wy + wh], fill=(15, 15, 15), outline=BTTR_GREEN)
        # title bar
        draw.rectangle([wx, wy, wx + ww, wy + 28], fill=(20, 20, 20))
        draw.line([(wx, wy + 28), (wx + ww, wy + 28)], fill=BTTR_GREEN)
        draw.text((wx + 10, wy + 6), "bttr-cycle.exe", font=mono(14), fill=BTTR_GREEN)

        if cycle_state:
            fnt_mono = mono(20)
            fnt_mono_sm = mono(16)
            cy = wy + 50

            for step, (label, status, color) in enumerate(cycle_state):
                prefix = ">" if status == "active" else " "
                status_text = f"  {prefix} {label}"
                draw.text((wx + 30, cy), status_text, font=fnt_mono, fill=color)

                if status == "done":
                    # checkmark
                    draw.text((wx + ww - 60, cy), "[OK]", font=fnt_mono_sm, fill=BTTR_GREEN)
                elif status == "active":
                    # blinking cursor
                    draw.text((wx + ww - 60, cy), "[...]", font=fnt_mono_sm, fill=BTTR_GREEN)

                cy += 50

    # desktop appears
    for i in range(12):
        img = new_frame(BLACK)
        draw = ImageDraw.Draw(img)
        draw_bttr_desktop(draw)
        add_frame(img)

    # cycle animation
    cycle_steps = [
        [("IDEA: Activation flow for new users", "active", BTTR_GREEN),
         ("BUILD", "pending", (60, 60, 60)),
         ("SIGNAL", "pending", (60, 60, 60)),
         ("DECIDE", "pending", (60, 60, 60))],

        [("IDEA: Activation flow for new users", "done", BTTR_GREEN),
         ("BUILD: Shipped in 2 hours", "active", BTTR_GREEN),
         ("SIGNAL", "pending", (60, 60, 60)),
         ("DECIDE", "pending", (60, 60, 60))],

        [("IDEA: Activation flow for new users", "done", BTTR_GREEN),
         ("BUILD: Shipped in 2 hours", "done", BTTR_GREEN),
         ("SIGNAL: 14% activation rate", "active", BTTR_GREEN),
         ("DECIDE", "pending", (60, 60, 60))],

        [("IDEA: Activation flow for new users", "done", BTTR_GREEN),
         ("BUILD: Shipped in 2 hours", "done", BTTR_GREEN),
         ("SIGNAL: 14% activation rate", "done", BTTR_GREEN),
         ("DECIDE: Iterate - target 25%", "active", WHITE)],
    ]

    for state in cycle_steps:
        img = new_frame(BLACK)
        draw = ImageDraw.Draw(img)
        draw_bttr_desktop(draw, cycle_state=state)
        add_frame(img, count=24)

    # final hold
    img = new_frame(BLACK)
    draw = ImageDraw.Draw(img)
    draw_bttr_desktop(draw, cycle_state=cycle_steps[-1])

    # add "Time elapsed: 1 day" at bottom of window
    fnt_result = mono(18)
    draw.text((430, 600), "Time elapsed: 1 afternoon", font=fnt_result, fill=BTTR_GREEN)
    draw.text((430, 630), "Meetings held: 0", font=fnt_result, fill=BTTR_GREEN)
    draw.text((430, 660), "Scores calculated: 0", font=fnt_result, fill=BTTR_GREEN)
    draw.text((430, 690), "Things learned: 1", font=fnt_result, fill=WHITE)

    add_frame(img, count=48)


def scene_final():
    """BTTR tagline and fade out"""
    # "Upgrade your PM OS."
    for i in range(30):
        t = min(1.0, i / 20)
        img = new_frame(BLACK)
        draw = ImageDraw.Draw(img)
        c = tuple(int(v * t) for v in BTTR_GREEN)
        fnt = sys_bold(64)
        text = "BTTR"
        tw, _ = text_size(draw, text, fnt)
        draw.text(((W - tw) // 2, H // 2 - 80), text, font=fnt, fill=c)

        fnt_sub = mono(24)
        sub = "Build. Test. Trash. Repeat."
        sw, _ = text_size(draw, sub, fnt_sub)
        c2 = tuple(int(v * t) for v in (120, 120, 120))
        draw.text(((W - sw) // 2, H // 2 + 10), sub, font=fnt_sub, fill=c2)

        add_frame(img)

    # hold
    add_frame(frames[-1], count=48)

    # fade out
    base = frames[-1]
    for i in range(24):
        t = i / 24
        black = new_frame(BLACK)
        img = Image.blend(base, black, t)
        add_frame(img)

    add_frame(new_frame(BLACK), count=12)


# --- AUDIO ---

def generate_audio(total_frames):
    """
    Retro computer sounds: startup chime, HDD clicking, error beeps,
    dramatic BSOD chord, then clean modern boot sound.
    """
    duration = total_frames / FPS
    sample_rate = 44100
    num_samples = int(duration * sample_rate)
    samples = np.zeros(num_samples)

    def add_beep(time_sec, freq=800, dur=0.08, vol=0.15):
        start = int(time_sec * sample_rate)
        length = int(dur * sample_rate)
        if start + length > len(samples):
            length = len(samples) - start
        if length <= 0:
            return
        t = np.arange(length) / sample_rate
        tone = np.sin(2 * np.pi * freq * t) * vol
        envelope = np.ones(length)
        # quick attack/release
        attack = min(int(0.005 * sample_rate), length)
        release = min(int(0.01 * sample_rate), length)
        envelope[:attack] = np.linspace(0, 1, attack)
        envelope[-release:] = np.linspace(1, 0, release)
        samples[start:start + length] += tone * envelope

    def add_click(time_sec, vol=0.06):
        """HDD click sound"""
        start = int(time_sec * sample_rate)
        length = int(0.005 * sample_rate)
        if start + length > len(samples):
            return
        click = np.random.randn(length) * vol
        click *= np.exp(-np.arange(length) / (0.001 * sample_rate))
        samples[start:start + length] += click

    def add_chord(time_sec, freqs, dur=1.0, vol=0.1):
        """Multi-frequency chord"""
        start = int(time_sec * sample_rate)
        length = int(dur * sample_rate)
        if start + length > len(samples):
            length = len(samples) - start
        if length <= 0:
            return
        t = np.arange(length) / sample_rate
        chord = np.zeros(length)
        for f in freqs:
            chord += np.sin(2 * np.pi * f * t)
        chord = chord / len(freqs) * vol
        envelope = np.exp(-t * 2)
        samples[start:start + length] += chord * envelope

    def add_error_beep(time_sec, vol=0.12):
        """Classic Windows error: two-tone beep"""
        add_beep(time_sec, freq=440, dur=0.1, vol=vol)
        add_beep(time_sec + 0.12, freq=330, dur=0.15, vol=vol)

    # Scene timing (approximate from frame counts):
    # Boot: 0-4s
    # Desktop: 4-6s
    # Roadmap loading: 6-9s
    # Error cascade: 9-18s
    # BSOD: 18-22s
    # Upgrade boot: 22-28s
    # BTTR desktop: 28-36s
    # Final: 36-40s

    # Boot sequence — startup chime
    add_chord(0.5, [523.25, 659.25, 783.99], dur=0.8, vol=0.12)  # C major

    # HDD clicks during boot
    for t in np.arange(1.0, 4.0, 0.3):
        add_click(t + random.uniform(-0.05, 0.05))

    # Desktop appear — small chime
    add_beep(4.5, freq=880, dur=0.1, vol=0.08)
    add_beep(4.65, freq=1100, dur=0.12, vol=0.08)

    # Roadmap loading — HDD activity
    for t in np.arange(6.0, 9.0, 0.15):
        add_click(t + random.uniform(-0.03, 0.03), vol=0.04)

    # Progress bar tick sounds
    for t in np.arange(6.5, 8.5, 0.25):
        add_beep(t, freq=600, dur=0.02, vol=0.03)

    # Error dialogs — each gets a beep
    error_times = [9.5, 11.0, 12.5, 14.0, 15.5, 17.0]
    for et in error_times:
        add_error_beep(et, vol=0.10)

    # Rapid error cascade
    for t in np.arange(17.5, 18.5, 0.1):
        add_error_beep(t, vol=0.06)

    # BSOD — dramatic low chord
    add_chord(19.0, [110, 138.59, 164.81], dur=2.0, vol=0.20)  # A minor, ominous

    # Silence gap
    # ...

    # BTTR boot — clean ascending tones
    bttr_boot_start = 22.5
    notes = [261.63, 329.63, 392.0, 523.25]  # C E G C (major arpeggio)
    for i, note in enumerate(notes):
        add_beep(bttr_boot_start + i * 0.2, freq=note, dur=0.15, vol=0.10)

    # Soft clicks for install
    for t in np.arange(23.0, 27.0, 0.2):
        add_click(t, vol=0.03)

    # Cycle steps — subtle confirmation tones
    cycle_times = [29.0, 30.0, 31.0, 32.0]
    for ct in cycle_times:
        add_beep(ct, freq=880, dur=0.05, vol=0.06)

    # Final — warm chord
    add_chord(36.0, [261.63, 329.63, 392.0, 523.25], dur=2.5, vol=0.15)

    # Fade out
    fade_start = int((duration - 2) * sample_rate)
    fade_len = int(2 * sample_rate)
    if fade_start + fade_len <= num_samples and fade_start > 0:
        fade = np.linspace(1, 0, fade_len)
        samples[fade_start:fade_start + fade_len] *= fade

    # Normalize — keep it moderate
    peak = np.max(np.abs(samples))
    if peak > 0:
        samples = samples / peak * 0.35

    with wave.open(AUDIO_FILE, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        for s in samples:
            wf.writeframes(struct.pack('<h', int(max(-0.99, min(0.99, s)) * 32767)))


# --- MAIN ---

def main():
    if os.path.exists(OUT_DIR):
        shutil.rmtree(OUT_DIR)
    os.makedirs(OUT_DIR)

    print("Generating Retro OS: 'Upgrade Your PM OS'...")

    print("  [1/7] BIOS Boot")
    scene_boot()

    print("  [2/7] Desktop")
    scene_desktop()

    print("  [3/7] Roadmap.exe")
    scene_roadmap_exe()

    print("  [4/7] Error Cascade")
    scene_error_cascade()

    print("  [5/7] Blue Screen of Death")
    scene_bsod()

    print("  [6/7] BTTR OS Upgrade")
    scene_upgrade()

    print("  [7/7] BTTR Desktop + Final")
    scene_bttr_desktop()
    scene_final()

    print(f"\nTotal frames: {len(frames)} ({len(frames)/FPS:.1f}s)")

    print("Saving frames...")
    for i, frame in enumerate(frames):
        frame.save(os.path.join(OUT_DIR, f"frame_{i:05d}.png"))
        if i % 200 == 0:
            print(f"  {i}/{len(frames)}")

    print("Generating retro audio...")
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
