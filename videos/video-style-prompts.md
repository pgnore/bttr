# BTTR Video Style Prompts

Three reusable prompts for generating short-form promotional videos using Python (PIL/Pillow + numpy + ffmpeg). Each prompt captures the full creative and technical specification for a distinct style.

---

## Style 1: YouTube Poop / Glitch Essay

### The Vibe
Aggressive, chaotic, deeply online. The visual language of YouTube Poop meets a genuine philosophical argument. Text slams onto screen, gets glitched apart, and the whole thing feels like it's barely holding together. The chaos IS the medium — it mirrors the breakdown of old frameworks. Think: "what if a shitpost had a thesis."

### Prompt

```
Generate a Python script that creates a short-form video (30-45 seconds, 1920x1080, 30fps) in the "YouTube Poop / Glitch Essay" style and compiles it to MP4 using ffmpeg.

VISUAL STYLE:
- Dark background (near-black, RGB 10,10,10)
- Bold sans-serif text (Helvetica Bold or Impact equivalent) for headlines
- Monospace font (Menlo/Consolas) for terminal/code elements
- Color palette: green (#22c55e) for positive/BTTR, red (#ef4444) for broken things, amber (#ffb000) for warnings, cyan (#00ffff) for accents, white for neutral, grey (#787878) for secondary text
- Every single frame gets scanlines (darken every 3rd row by ~40 intensity) and film grain (random noise +/-15 per pixel channel). This is non-negotiable — it's what makes it feel analog/degraded rather than clean
- Text is always centered horizontally, positioned at specific Y coordinates

CORE VISUAL EFFECTS (implement each as a reusable function):
1. `add_scanlines(img, intensity=40)` — Darken every 3rd row of pixels using numpy array manipulation. Apply to nearly every frame.
2. `add_noise(img, amount=25)` — Add random integer noise (-amount to +amount) to all RGB channels, clip to 0-255. Use numpy int16 to avoid overflow.
3. `glitch_shift(img, intensity=20)` — Select 3-8 random horizontal bands (2-20px tall), roll each left/right by a random amount up to `intensity` pixels using np.roll on the row slice.
4. `heavy_glitch(img)` — 15-30 random horizontal band shifts (5-40px tall, +/-100px shift), PLUS per-channel horizontal offset: roll the red channel +/-10px, roll the blue channel +/-10px independently. This creates the RGB split look.
5. `chromatic_aberration(img, offset=6)` — Roll red channel right by `offset` pixels, blue channel left by `offset` pixels. Creates color fringing on all edges.
6. `shake(img, amount=15)` — Use PIL ImageChops.offset to shift the entire image by random dx/dy within `amount`. Creates a camera shake effect.
7. `flash_frame(color, count)` — Insert solid-color frames (usually white or red) for 1-3 frames. Creates the "flash cut" punctuation between scenes.

SCENE STRUCTURE:
The video should follow this pattern — build tension, break something, reveal the alternative:

1. OPENING (~3-5s): Terminal-style boot sequence. Green monospace text appearing line by line on black. Each line holds for ~4 frames then the next appears. Include a blinking cursor. End with a white flash.

2. TITLE SLAM (~3-5s): Big bold text flickers in (alternate between visible and invisible every other frame for 8 frames), then holds with occasional glitch_shift every ~7 frames for 25 frames. Add quieter subtext below after a beat. End with black frames.

3. RAPID MONTAGE (~3-5s): Flash through 8-12 items (framework names, PM activities, etc.) — each item gets its own frame with a random font size (80-160), random color from the palette, random chance of glitch_shift(40), and holds for only 2-4 frames. Intersperse random flash_frames. This should feel overwhelming and chaotic.

4. THE BREAKDOWN (~5-8s): Build a formula or concept piece by piece (8 frames per piece). Then break it — an escalating sequence where: the text shakes more, noise increases, the font color shifts to red, and finally EXPLODES into 20 frames of heavy_glitch with random error text scattered at random positions in random sizes and random colors. Bookend with flash_frame(RED) + flash_frame(WHITE).

5. THE QUIET AFTER (~3-5s): After the chaos, simple white text fades in (increase alpha over 25 frames by ramping RGB values from 0 to 255). Black frames. The contrast with the previous chaos makes this land hard.

6. THE ARGUMENT (~8-12s): Slower-paced text, left-aligned at x=160-200, building line by line. Each line holds for 10-12 frames. Use grey for setup text, white for important points, green for the thesis. Occasional glitch_shift(10) on every 10th frame to maintain the visual language.

7. WORD SLAMS (~5-7s): 3 key words slam in one at a time. Each word: 3 frames of size-decreasing text (200pt -> 120pt) with shake(15) and noise(40), then a 1-frame flash in the word's color, then 18 frames holding at 120pt with a description line below. Then all 3 words shown together for 35 frames with monospace font, with occasional glitch and chromatic_aberration in the last third.

8. LOGO (~8-12s): Brand text fades in over 40 frames. Hold clean for 150 frames (~5 seconds) with occasional subtle glitch every 25 frames. Then GLITCH OUTRO: 75 frames of escalating destruction — glitch intensity rises from 5 to 125, chromatic aberration grows from 0 to 20, shake grows from 0 to 30, noise grows from 0 to 80, and in the final 40% blend toward black while applying heavy_glitch randomly. Insert occasional random flash frames in the chaos. End with green flash, white flash, 20 black frames.

AUDIO DESIGN:
Generate a WAV file (44100Hz, mono, 16-bit) using numpy:
- Base: Low sine drone at 55Hz, amplitude 0.15 — runs the entire duration
- Layer effects based on timeline position (use progress = current_time / total_duration):
  - Boot section (0-8%): Intermittent 200Hz beeps (on/off every 1/8 second)
  - Middle section (8-22%): 110Hz undertone at 0.1 amplitude
  - Tension ramp (22-40%): Rising frequency (110Hz to 910Hz), rising amplitude (0 to 0.2), with random noise spikes (+/-0.3) when tension > 0.7
  - Quiet section (40-45%): All amplitudes multiplied by 0.3
  - Emotional middle (45-65%): Two sine layers — 82Hz at 0.08, 165Hz at 0.04
  - Impact hits (65-78%): Bass hit (60Hz, amplitude 0.4, fast decay over 0.05s) triggered at the start of each of 3 equal sub-sections
  - Resolution (78-90%): Two sine layers — 130Hz at 0.06, 195Hz at 0.04
  - Outro (90-100%): 82Hz at 0.1, amplitude multiplied by a linear fade from 1 to 0
- Random glitch hits: 0.1% chance per sample of a random spike (+/-0.5)
- Normalize: divide by peak, multiply by 0.7
- Clamp all values to [-0.9, 0.9] before writing

TECHNICAL NOTES:
- Use PIL (Pillow) for all image creation and compositing
- Use numpy for all pixel manipulation (convert to/from array)
- Use random.seed(42) and np.random.seed(42) for reproducibility
- Store all frames in a Python list, save as numbered PNGs, compile with ffmpeg
- ffmpeg command: `ffmpeg -y -framerate 30 -i frames/frame_%05d.png -i audio.wav -c:v libx264 -pix_fmt yuv420p -crf 18 -preset fast -c:a aac -b:a 128k -shortest output.mp4`
- Clean up frames directory and audio file after compilation
```

---

## Style 2: VHS Analog Horror

### The Vibe
Found footage. A corporate training tape from a company that no longer exists. The VHS format itself is the metaphor — the old way of thinking is a degrading tape that eventually destroys itself. It starts clean and professional, then the tape degrades as the content gets more absurd, until the whole thing breaks apart. The horror is corporate: planning loops, infinite meetings, zero output. Think: "Local 58" meets "Office Space."

### Prompt

```
Generate a Python script that creates a short-form video (50-70 seconds, 1920x1080, 24fps) in the "VHS Analog Horror" style and compiles it to MP4 using ffmpeg.

VISUAL STYLE:
- Deep blue-black background (8, 5, 18) for main content
- Corporate blue (30, 50, 100) for "training slides"
- VHS blue screen (20, 25, 120) for title cards and end cards
- Color palette is WARM and desaturated: off-white (220, 215, 200), aged yellow (210, 195, 80), muted red (180, 40, 40), faded green (40, 160, 70), warm grey (130, 125, 115)
- Sans-serif font (Helvetica) for corporate content, monospace for timestamps
- Every frame includes VHS artifacts through a composited `apply_vhs()` function

VHS EFFECT PIPELINE (implement each as a reusable function, compose them in order):
The key insight: ALL effects take a `degradation` parameter (0.0 = clean tape, 1.0 = nearly destroyed). This drives the entire visual arc.

1. `vhs_warm_tint(img, strength=0.15)` — Multiply red channel by (1 + strength*0.3), green by (1 + strength*0.1), blue by (1 - strength*0.2). Use float32 arrays, clip to 0-255.

2. `vhs_color_bleed(img, amount=3)` — Roll red channel RIGHT by `amount` pixels, blue channel LEFT by `amount`. This creates the horizontal chroma smear that real VHS has because chroma is lower bandwidth than luma.

3. `vhs_wobble(img, frame_idx, intensity=2.0)` — For each row y, shift horizontally by `int(sin(y * 0.01 + frame_idx * 0.15) * intensity)` pixels. This simulates tape speed variation — the whole image gently waves left-right with a pattern that moves vertically over time.

4. `vhs_noise(img, amount=15)` — VHS noise is primarily LUMINANCE noise, not chroma. Generate a single-channel noise array (H x W x 1), concatenate it 3 times for RGB. This looks more authentic than per-channel noise.

5. `vhs_scanlines(img, weight=0.3)` — Darken every other row by multiplying by (1 - weight). Use float32 to avoid overflow.

6. `vhs_tracking_error(img, severity=0.3)` — The signature VHS glitch. Generate (2 + severity*8) horizontal bands at random y positions, each 2 to (8 + severity*30) pixels tall, shifted horizontally by +/-(severity*60) pixels. At higher severity, add random noise (0 to 50+severity*150) inside the bands. This is what people mean when they say "VHS tracking."

7. `vhs_static(duration_frames)` — Pure between-channel static. Each frame is random noise (0-100 per channel), tinted slightly warm (red channel * 1.1), with heavy scanlines applied.

8. `apply_vhs(img, frame_idx, degradation=0.0)` — THE MASTER FUNCTION. Composes all effects in order: warm_tint(0.15 + deg*0.3) -> color_bleed(2 + deg*8) -> wobble(1.5 + deg*6) -> noise(12 + deg*50) -> scanlines(0.25 + deg*0.2). When degradation > 0.3, randomly trigger tracking_error with probability (deg*0.4).

VHS OVERLAY ELEMENTS (draw on top of content, before VHS effects):
- `draw_rec_indicator(draw, frame_idx)` — Blinking "REC" with red dot at top-left. Blinks every ~18 frames. Use monospace font.
- `draw_timecode(draw, frame_idx)` — HH:MM:SS timecode at bottom-right in monospace. Advances with real frame time.
- `draw_date_stamp(draw)` — Date stamp at top-right in monospace yellow.

SCENE STRUCTURE — THE NARRATIVE ARC:
The video tells a STORY. A corporate training tape about "The Product Roadmap Process" that reveals, through its own degradation, that the process is broken.

1. BLUE SCREEN TITLE (~3s): "PROPERTY OF [COMPANY NAME] INC. / INTERNAL USE ONLY — DO NOT DUPLICATE / Product Management Training Series / Tape 7 of 12". Minimal VHS effects (degradation 0.03-0.05). End with 12 frames of static.

2. CORPORATE TITLE CARD (~4s): Formal training title with corporate double-border frame (yellow on dark blue). Include REC indicator, date stamp, timecode. Light VHS (degradation 0.03).

3. NORMAL STEPS 1-3 (~10-12s each 3-4s): Standard corporate training slides. Step number in yellow at top with underline. Title in white below. 3-4 bullet points that stagger in (each appears ~18 frames after the last). Full VHS overlays. Degradation stays at 0.03. The content should be realistic corporate PM activities: gathering requirements, scoring with RICE, aligning stakeholders.

4. DEGRADING STEPS 4-5 (~5-7s): Same slide format but degradation rises to 0.15-0.25. Content starts showing cracks: "Leadership says 'looks good, but...'" / "Receive 11 pieces of contradictory feedback." The VHS effects are now noticeable — wobble is stronger, occasional tracking errors appear.

5. THE LOOP (~15-20s): THE HORROR CORE. Steps start repeating with increasing step numbers (6, 7, 8... 14... 27... 47... 83... 128). Same titles cycling: "Re-prioritize" / "Re-align" / "Update the Roadmap" / "Present to Leadership (Again)". Each step: degradation increases (0.35 to 0.95), hold time DECREASES (from 48 frames down to 10), and at step 19+ add red WARNING notes at the bottom: "NOTE: No features have shipped this quarter." At step 34+: "NOTE: Engineering has stopped attending meetings." At step 83+: "NOTE: Three PMs have resigned." Insert bursts of static between slides when degradation > 0.6. The titles deteriorate: "Re-prioritize..." -> "Re-..." -> "...". Step numbers go: 6,7,8,9,10,11,14,19,27,34,47,83,128.

6. TAPE BREAKS (~3s): 72 frames alternating between pure static (70% chance) and ghost frames where a corporate slide bleeds through at degradation 0.95 (30% chance). The ghost frames show random absurd step numbers (47, 83, 128, 256, 512).

7. EPILOGUE (~8-10s): Quiet revelation on dark background. Text appears line by line (each with its own hold time): "[Company] filed for bankruptcy in Q3 2021." "In two years of operation, their product team completed 412 roadmap revisions." "They shipped zero features." — this last line in RED, held for 2.5s. Use light VHS (degradation 0.1). End with static.

8. THE COUNTER-ARGUMENT (~8s): "What if, on day one, someone had said:" (grey) then '"Skip the roadmap. Build one thing. See if anyone cares."' (white, larger font). Light VHS. Hold for emphasis.

9. CLEAN BTTR MOMENT (~6-8s): The tape CLEARS. Near-zero VHS effects (just subtle scanlines at 0.1 weight). Clean dark background with brand text fading in over 24 frames. Hold clean for 96 frames (4 seconds). Then VHS reclaims: degradation ramps from 0 to 0.9 over 36 frames. Static for 18 frames. "END OF TAPE" on blue screen, fading to black.

AUDIO DESIGN:
Generate a WAV file (44100Hz, mono, 16-bit). The audio IS the VHS tape.

Base layers (always present):
- Pink noise tape hiss at 0.06 amplitude. Generate white noise with np.random.randn, then do cumulative sum, remove linear drift, normalize, high-pass by mixing 98% accumulated + 2% raw white. This creates the hissy, warm texture of magnetic tape.
- 60Hz mains hum at 0.04 amplitude + harmonics at 120Hz (0.02) and 180Hz (0.008). This is the AC mains coupling that real VHS tapes pick up.
- 30Hz VCR motor rumble at 0.03 amplitude.

Timeline-keyed degradation (use progress = current_time / total_duration):
- 0-40% (normal section): Just base layers. Clean tape.
- 40-65% (loop section): Add tape speed flutter: sin(t * 8 * (1 + severity*3)) * severity * 0.08. Add Gaussian noise (0, severity * 0.06). Random loud pops: 0.3% chance per sample of +/-0.4 spike.
- 65-75% (tape breaking): Heavy Gaussian noise (0, 0.1 + severity*0.15). Buzzing: 240Hz sine at (severity * 0.12). Occasional random spikes (1% chance, +/-0.5).
- 75-85% (epilogue): All samples multiplied by 0.5. Quiet, eerie.
- 85-95% (BTTR clean moment): First half: all samples * 0.15 (near silence). Second half: Gaussian noise ramps back in.
- 95-100% (end): Linear fade to zero.

IMPORTANT: Normalize to peak 0.55 (not higher — VHS audio should feel muted, not loud). The hiss and hum should be SUBTLE background texture, not the dominant sound.

TECHNICAL NOTES:
- 24fps gives a more cinematic/vintage feel than 30fps
- The degradation parameter is the single most important creative control — it drives the entire visual and audio arc
- The narrative structure (professional -> absurd -> broken -> revelation) is essential to the style
- The corporate content should feel REAL enough to be uncomfortable — realistic PM activities, not cartoonish
- Use random.seed(99) for reproducibility
- ffmpeg: same as Style 1 but with -framerate 24
```

---

## Style 3: Retro OS / Windows 95

### The Vibe
Nostalgia weaponized. A fake operating system called "PM_OS" boots up, tries to run "Roadmap.exe", and crashes through increasingly absurd error dialogs until a Blue Screen of Death. Then BTTR OS installs — clean, dark, modern. The Win95 UI is the visual metaphor for outdated systems. Everyone over 25 gets the reference. The humor lives in the error messages. Think: "If your PM framework was software, it would be this."

### Prompt

```
Generate a Python script that creates a short-form video (35-40 seconds, 1920x1080, 24fps) in the "Retro OS / Windows 95" style and compiles it to MP4 using ffmpeg.

VISUAL STYLE:
- Teal desktop background (0, 128, 128) — the iconic Win95 color
- Grey system chrome (192, 192, 192)
- Title bar blue (0, 0, 128)
- BSOD blue (0, 0, 170)
- White (255, 255, 255), black (0, 0, 0), dark grey (128, 128, 128)
- System font: Helvetica (index 0 for regular, index 1 for bold) — approximates MS Sans Serif
- Monospace: Menlo — for BIOS text and code
- The brand color for the "upgrade": green (34, 197, 94)

WIN95 UI COMPONENTS (implement each as a reusable drawing function):
These are the building blocks. Getting them right is what makes the style feel authentic.

1. `draw_bevel_rect(draw, x, y, w, h, raised=True)` — THE fundamental Win95 element. Fill with grey (192,192,192). Draw TWO highlight lines (white) on top edge and left edge (at offset 0 AND offset 1 inward). Draw TWO shadow lines (dark grey 128,128,128) on bottom edge and right edge (at offset 0 AND offset 1 inward). When `raised=False`, swap the colors (shadow on top-left, highlight on bottom-right) — this creates the "pressed button" / "sunken panel" look. The double-line bevel is what gives Win95 its chunky 3D feel.

2. `draw_button(draw, x, y, w, h, text, pressed=False)` — A beveled rectangle with centered text inside. When pressed, offset the text by +1px in both x and y (simulates the button pushing in). Use the system font at ~14px.

3. `draw_window(draw, x, y, w, h, title, active=True)` — The full window frame:
   - Outer beveled rectangle (raised)
   - Title bar: filled rectangle inside the frame, 20px tall, colored TITLE_BLUE when active, DARK_GREY when inactive
   - Title text: bold system font, white, positioned at (x+6, y+5)
   - Close button: small beveled rect (16x14) at top-right of title bar with "x" text
   - Content area: white-filled rectangle below the title bar with DARK_GREY outline
   - Return the content area's top-left corner coordinates for placing content

4. `draw_error_dialog(img, title, message, buttons, icon, cx, cy, width, height)` — A complete error dialog:
   - A window frame via draw_window()
   - Icon area at left of content: "error" = red circle (32px) with white "X", "warning" = yellow triangle with black "!", "info" = blue circle with white "i"
   - Message text at right of icon, split on "\n", each line 20px apart, in system font ~15px
   - Button row at bottom, centered, each button 80x26px with 10px spacing
   - The buttons should have FUNNY text — "OK" / "Also OK" / "Cry" / "Resign" / "Wait" / "Wait More" / "Sure" / "Why Not"

5. `draw_progress_bar(draw, x, y, w, h, progress, label)` — Sunken rectangle (dark grey top-left lines = inset look) with blue fill proportional to progress (0.0-1.0). Optional centered label that switches from black text to white text when fill passes 50%.

SCENE STRUCTURE:

1. BIOS BOOT (~4s): Black background, green monospace text appearing line by line. Content: "PM-BIOS v4.2 (c) 2019 Legacy Systems Inc." then "Detecting installed frameworks..." followed by dotted-leader lines for RICE, WSJF, ICE, etc. each ending in "OK". Include a joke: "Memory Test: 640K meetings ought to be enough for anybody." End with "Loading PM_OS v3.1..." animated with cycling dots (0-3 dots, 4 frames each, 8 cycles). Each line holds for 3-6 frames depending on importance.

2. DESKTOP (~2-3s): Teal background with taskbar at bottom (beveled rect, Start button with bold "Start" text, clock showing "9:00 AM" at right). After 6 frames, desktop icons appear: 4 icons in a column at top-left (Roadmap.exe, Priorities.xls, Meetings.doc, Alignment.ppt). Each icon is a beveled square with a white inner square showing the file extension in blue, plus a white label below. Hold for 24 frames.

3. ROADMAP.EXE LOADING (~3s): A loading window opens on the teal desktop. Inside: "Loading Q3 2024 Roadmap..." / "Aligning stakeholders: X%". Progress bar advances from 0% to 74% (iterate in steps of 2, one frame per step). FREEZE at 74% — hold for 30 frames. The progress bar stopping short is the visual punchline setup.

4. ERROR CASCADE (~9-12s): The core comedy sequence. Start from the frozen loading screen. Stack error dialogs on top of each other, each offset by (+30, +25) from the previous. Each dialog holds for 28 frames. The errors escalate in absurdity:
   - "Roadmap.exe has encountered a problem. Reason: Too many priorities (found 847). Expected: 3-5 priorities."
   - "FATAL: Feature #421 scored 8.5 AND 3.2 depending on who you ask. Would you like to schedule a meeting?" [Yes] [Also Yes]
   - "Cannot align stakeholders. 12 people need to approve. 11 are in other meetings. 1 is 'thinking about it.'" [Wait] [Wait More]
   - "RICE Score calculation failed. Division by zero in Effort field." [Cry] [Resign]
   - "Stack overflow in Meeting.exe — This meeting is to plan the meeting that plans the planning meeting. Recursion depth: 47"
   - "WARNING: Confidence score is statistically indistinguishable from a random number generator."

   Then RAPID POPUPS: 9 more dialogs at random positions, 4 frames each, titles escalating: "Error", "Error (2)", "Error (3)", "Something Went Wrong", "Really Wrong", "So Wrong", "Help", "HELP", "PLEASE". Hold the chaos for 20 frames.

5. BLUE SCREEN OF DEATH (~4s): Full screen BSOD_BLUE. Monospace text starting from (80, 80):
   - "PM_OS v3.1" (larger font)
   - "A fatal exception has occurred in ROADMAP.EXE"
   - "The current prioritization framework has performed an illegal operation and will be shut down."
   - Error code: "RICE_SCORE_MEANINGLESS (0x00000000)"
   - Fake stack trace: "at PrioritizationEngine.score()" -> "at MeetingScheduler.align()" -> "at RoadmapBuilder.build()" -> "at QuarterlyPlanning.plan()" -> "at QuarterlyPlanning.planThePlan()" -> "at QuarterlyPlanning.planThePlanForThePlan()"
   - "* Press any key to install a better framework."
   - "* Or press CTRL+ALT+DEL to schedule another meeting."
   Hold 72 frames, then flicker: 6 cycles of (2 black frames, 2 BSOD frames), then 12 black frames.

6. BTTR OS INSTALL (~6s): Black background, green/red monospace text, line by line. "Installing BTTR OS v1.0..." then "Removing unnecessary frameworks:" with [-] lines in RED for RICE, WSJF, ICE, Stakeholder Alignment Bus. Then "Installing BTTR components:" with [+] lines in GREEN for Build Engine, Signal Reader, Trash Collector, Repeat Scheduler. Then "Configuration:" with DISABLED lines in RED for effort estimation ("AI builds everything"), meeting scheduler ("ship instead"), score calculator ("test instead"). Final line "BTTR OS ready." holds for 20 frames. Each [-] and [+] line holds for just 2 frames (fast install feel).

7. BTTR DESKTOP (~4-6s): Dark/black background (contrast with teal). Minimal dark taskbar with green accent line at top, "BTTR" in green at left. A single dark window with green border: "bttr-cycle.exe". Inside, show a 4-step cycle animating through states (1 second each): IDEA -> BUILD -> SIGNAL -> DECIDE. Each step shows as "> [label]" when active, with "[OK]" when done and "[...]" when active. Use green for completed/active items, dark grey for pending. After the cycle completes, show results: "Time elapsed: 1 afternoon" / "Meetings held: 0" / "Scores calculated: 0" / "Things learned: 1" (this last one in white, rest in green). Hold for 48 frames.

8. FINAL + FADE (~3-4s): Black background. Brand text fades in over 20 frames (multiply color RGB by t from 0 to 1). Tagline below. Hold 48 frames. Fade to black over 24 frames using Image.blend(). 12 black frames.

AUDIO DESIGN:
Generate a WAV file (44100Hz, mono, 16-bit). Retro computer sound design — discrete events, not continuous texture.

Sound primitives:
- `add_beep(time, freq, dur, vol)` — Sine wave with quick 5ms attack and 10ms release envelope. Short (50-150ms), clean.
- `add_click(time, vol)` — 5ms burst of random noise with exponential decay (tau = 1ms). Simulates HDD head seeking.
- `add_chord(time, freqs, dur, vol)` — Multiple sine waves summed, averaged, with exponential decay envelope (e^(-t*2)).
- `add_error_beep(time, vol)` — Two-tone: 440Hz for 100ms, then 330Hz for 150ms with a 20ms gap. The classic Windows error sound.

Timeline-keyed events:
- Boot (0-4s): Startup chime at 0.5s — C major chord [523, 659, 784] Hz, 0.8s duration, vol 0.12. HDD clicks every ~0.3s from 1-4s.
- Desktop (4-6s): Two-tone chime (880Hz then 1100Hz, each 100ms, vol 0.08).
- Loading (6-9s): Rapid HDD clicks every 0.15s at low volume. Faint progress ticks every 0.25s (600Hz, 20ms, vol 0.03).
- Error cascade (9-18s): Error beeps at each dialog appearance (~1.5s apart, vol 0.10). Rapid error beeps every 0.1s during the popup storm (vol 0.06).
- BSOD (18-22s): Dramatic low A minor chord [110, 138.59, 164.81] Hz, 2s duration, vol 0.20. Ominous.
- BTTR boot (22-28s): Clean ascending C major arpeggio [261, 329, 392, 523] Hz, one note every 0.2s, each 150ms at vol 0.10. Soft clicks during install.
- BTTR desktop (28-36s): Subtle confirmation beep (880Hz, 50ms, vol 0.06) at each cycle step completion.
- Final (36-40s): Warm C major chord [261, 329, 392, 523] Hz, 2.5s, vol 0.15.
- Fade: linear fade to zero over last 2 seconds.

IMPORTANT: Normalize to peak 0.35 (keep it restrained — the silence between sounds is as important as the sounds). The contrast between the chaotic error beep section and the clean BTTR boot arpeggio is the audio payoff.

TECHNICAL NOTES:
- 24fps for slightly cinematic feel
- No post-processing effects (no scanlines, no noise) — the clean pixel-art look IS the style
- The comedy is in the WRITING of the error messages — spend time making them funny and specific to PM culture
- The visual arc: teal+grey (old, broken) -> BSOD (crash) -> black+green (new, clean) mirrors the BTTR thesis
- The beveled rectangles must have DOUBLE lines (offset 0 and 1) to look authentic — single-pixel bevels look wrong
- Use random.seed(42) for reproducibility
- Error dialogs composite onto the PREVIOUS frame (not a fresh frame), creating the cascading pile-up effect
```

---

## Usage Notes

- All three styles use the same tech stack: Python 3, Pillow (PIL), numpy, and ffmpeg
- Each prompt is self-contained — give it to Claude (or any capable LLM) and it should produce a working script
- Swap out the content (text, narrative, messaging) while keeping the visual/audio specifications intact
- The prompts specify macOS system fonts (Helvetica, Menlo, Georgia) — adjust for other platforms
- Audio peak levels are calibrated: Style 1 is loudest (0.7), Style 2 is medium (0.55), Style 3 is quietest (0.35) — reflecting each style's energy level
