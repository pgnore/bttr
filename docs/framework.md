# BTTR Framework — v0.5

## The One-Liner

BTTR is a product decision framework that replaces prioritization with evidence. Stop scoring what to build — build it, test it, and let reality decide.

**BTTR** stands for **Build, Test, Trash, Repeat** — and it's pronounced "better," because that's the point.

---

## The Core Claim: Prioritization Is Dead

Every PM framework invented before 2024 exists for one reason: building was expensive, so you had to choose carefully.

RICE weights Effort. WSJF weights Cost of Delay vs. Duration. ICE weights Ease. They're all solving the same problem: *"We can only build 3 things this quarter, so which 3?"*

That constraint is gone.

AI doesn't just speed up development — it collapses the cost of being wrong. When you can prototype in hours, the expensive thing isn't building. It's *deciding without data*.

The RICE formula is `(Reach x Impact x Confidence) / Effort`. When Effort approaches zero, the formula breaks — division by zero. And Confidence? It's a guess — an admission that you don't actually know. Why sit in a room estimating your confidence level when you can just *find out*?

**BTTR's argument is not "test your ideas."** Everyone already knows that. BTTR's argument is that the entire prioritization layer — the scoring, the stack-ranking, the roadmap negotiations, the quarterly planning theater — is now waste. You don't need to predict which ideas will work when you can *test all of them* in the time it used to take to debate one.

The question shifts from *"What should we build?"* to *"What did we learn?"*

---

## What BTTR Is Not

BTTR borrows from existing methodologies. It also fundamentally differs from them. If you're thinking "this sounds like X," here's where BTTR draws the line.

### BTTR is not A/B Testing

**A/B testing** is a measurement method. You show variant A to one group and variant B to another, then compare results. It answers: *"Which of these two options performs better?"*

BTTR *uses* A/B testing (among other methods) in the TEST phase. But A/B testing is a tool, not a framework. It doesn't tell you:
- Which problems to test in the first place
- When to kill a direction entirely vs. iterate
- How to structure your team's cadence around rapid experimentation
- What to do when neither A nor B works

A/B testing optimizes *between options*. BTTR decides *whether to keep playing*.

You can A/B test button colors for six months and still be working on the wrong feature. BTTR asks: should this feature exist at all?

### BTTR is not Lean Startup

**Lean Startup** (Eric Ries, 2011) introduced Build-Measure-Learn — the idea that startups should validate assumptions before scaling. BTTR owes a debt to Lean Startup. The DNA is visible.

But Lean Startup was written when building an MVP took months and tens of thousands of dollars. Its advice reflects that cost: validate before you build. Talk to customers. Build the *minimum* viable product. The word "minimum" is doing heavy lifting — it's there because building is expensive, so build as little as possible.

**BTTR operates in a world where building is essentially free.** That changes the math:

| | Lean Startup (2011) | BTTR (2024+) |
|---|---|---|
| **Building costs** | Significant (weeks/months for MVP) | Near-zero (hours with AI) |
| **Core advice** | Validate before you build | Build to validate |
| **"Minimum" in MVP** | Critical constraint — build the least you can | Irrelevant — build the full thing, it costs the same |
| **Pivot decision** | High-stakes (you invested months) | Low-stakes (you invested hours) |
| **Number of experiments** | Few, carefully chosen | Many, run in parallel |
| **Target audience** | Startups finding product-market fit | Any product team making decisions |
| **What it replaces** | "Just build the whole thing and pray" | RICE, WSJF, ICE — the prioritization layer |

Lean Startup says: *"Don't build until you've validated the idea."*
BTTR says: *"Building IS the validation."*

The key difference is that AI collapses the cost structure Lean Startup was designed around. When building is near-free, the entire "validate before you build" premise inverts. You don't need to be careful about which experiments to run. You run them all.

### BTTR is not User Testing

**User testing** is the practice of watching real people interact with your product. It's invaluable. Every product team should do it.

But user testing is a *research activity*, not a *decision framework*. It tells you what's happening. It doesn't tell you:
- When to stop iterating and move on
- How to structure your team around rapid experimentation
- What to do with the 80% of insights that are ambiguous
- When sunk cost is real vs. when you're fooling yourself

Most critically: user testing usually happens *after* a team has already committed to building something. The roadmap is set, the sprint is planned, the feature is scoped. User testing validates or refines the implementation — it doesn't question whether the feature should exist.

BTTR questions everything. Every cycle starts from "should this exist?" and earns its way to "yes" through signal. Nothing gets a free pass onto the roadmap because a stakeholder championed it or a competitor shipped it.

### BTTR is not Design Thinking

**Design Thinking** (IDEO, Stanford d.school) follows Empathize → Define → Ideate → Prototype → Test. It's a powerful approach to understanding problems deeply.

BTTR shares the "prototype and test" DNA. But Design Thinking front-loads the process with empathy research, problem definition, and ideation *before* building anything. That made sense when prototyping was expensive.

BTTR collapses the first three stages into one: **start with the idea and build.** If you're wrong about the problem, you'll find out fast — not after months of research. The research happens *through* shipping, not *before* it.

Design Thinking asks: *"Do we understand the problem well enough to solve it?"*
BTTR asks: *"Can we find out faster by shipping than by researching?"*

### So what IS BTTR?

BTTR is the **decision layer** — the part that sits above all of these methodologies and answers: *"What should our team be working on, and how do we know when to stop?"*

It replaces RICE, WSJF, ICE, and roadmap negotiation. It's compatible with (and often uses) A/B testing, user testing, Lean experiments, and Design Thinking techniques as tools within the cycle. But BTTR itself operates at the level of *team decision-making*: what ideas are we testing, how fast are we getting signal, and are we being honest about the results?

```
TRADITIONAL STACK:           BTTR STACK:

Strategy                     Strategy
    ↓                            ↓
Prioritization (RICE/WSJF)  BTTR (idea → build → signal)
    ↓                            ↓
Planning (sprints/quarters)  The cycle (you define the cadence)
    ↓                            ↓
Building                     Building (AI-assisted)
    ↓                            ↓
Measuring                    Measuring (A/B tests, analytics, user testing)
    ↓                            ↓
Learning (post-ship)         Learning (per cycle)
```

BTTR doesn't replace your measurement tools. It replaces the *decision process* that determines what gets measured in the first place.

---

## Key Concepts

Before diving into the phases, let's get the language straight.

### The Cycle

A **cycle** is one complete pass through Build → Test → Trash → Repeat. It's the atomic unit of BTTR. How long a cycle takes depends on the complexity of the idea — a simple idea might resolve in days, a complex one in weeks. The point isn't a specific cadence. The point is that every cycle has a clear idea, a scoped build, an honest signal, and a decisive outcome. AI-native teams will naturally run faster cycles, but the framework works at any speed.

### Iterate vs. Pivot

Every cycle ends with a decision. That decision has exactly two outcomes:

- **Iterate** — The problem is right, the solution needs refinement. You run another cycle on the *same problem* with a *refined approach*. You carry forward what you learned.
- **Pivot** — The problem was wrong, or a better one emerged. You run a new cycle on a *different problem*. You carry forward the insight, not the solution.

Both paths start a new cycle. The difference is what you keep and what you throw away.

**The rule:** If you can articulate *exactly* what you'd change in 5 minutes, that's an iteration. If the next build would be fundamentally different, that's a pivot — and that's fine.

### The Idea

Every cycle starts with an **idea** — a concrete concept for delivering value. Not a vague problem statement. Not a hypothesis wrapped in academic language. An idea: "I want to build X because Y." Some ideas pay off. Most don't. The goal isn't to be right every time — it's to find out fast so you can move to the next idea.

---

## The Four Phases

### 1. BUILD

Ship a working version. Not a spec, not a wireframe, not a "lo-fi prototype" — a *working thing*. AI builds, PM directs. The goal is a testable artifact as fast as possible — not weeks, not months.

**What BUILD looks like in practice:**

1. **Start with the idea** (2-3 sentences max):
   - What are you building and why?
   - For whom?
   - What does success look like?

2. **Direct AI to build it.** Give it the problem, the constraints, and your judgment on what matters. Review what it produces. Adjust. Ship.

3. **Set a time box.** Define a build deadline and hold yourself to it. Cut scope ruthlessly — build what's needed for signal, nothing more. The prototype is the proposal — not the product.

**What BUILD does NOT mean:**
- Pixel-perfect design (ugly and functional beats beautiful and theoretical)
- Full production architecture (you'll throw this away if the idea doesn't pan out)
- Stakeholder alignment (ship first, let results create alignment)
- A PRD (the idea *is* the PRD)

> **Example:** Your team suspects that users abandon onboarding because they don't see value fast enough. The idea: "Show users their first insight within 60 seconds of signup." BUILD: You direct AI to create a new onboarding flow that generates a sample insight using the user's industry as input. It's not pretty. The data is partially hardcoded. But it works, and a user can experience it. Shipped in one afternoon.

---

### 2. TEST

Put the build in front of real signals. Not opinions — *signals*.

The difference between an opinion and a signal: opinions are what people *say* in a conference room. Signals are what people *do* with a live product.

**Valid test signals (ranked by strength):**

| Signal | Why it's strong | Example |
|--------|----------------|---------|
| Revenue / willingness to pay | Money is the strongest signal | "3 users asked about pricing unprompted" |
| Retention / return usage | They came back without being asked | "40% of test users returned within 48 hours" |
| Conversion / activation | They completed the thing you wanted them to | "28% reached the aha moment vs. 12% baseline" |
| User behavior (observed) | What they actually did, not what they said | "Users spent 4 min on the insight page, 8 sec on the old one" |
| Direct feedback + behavior | What they say, cross-referenced with what they did | "Said 'this is cool' AND shared it with a teammate" |
| Speed to value | How fast they got the point | "Median time to first insight: 47 seconds" |

**Invalid test signals:**

| Signal | Why it's weak |
|--------|--------------|
| Stakeholder opinions | They're not your users |
| "I think users would..." | Thinking is not knowing |
| NPS on a prototype | Sample too small, context too artificial |
| Competitor has it | Their users aren't your users |
| Internal team excitement | Builders are biased toward what they built |
| Thumbs up in Slack | Encouragement is not engagement |

**How to test — pick the right method for the signal you need:**

| Method | Best for | Speed | Signal strength |
|--------|----------|-------|----------------|
| A/B test (traffic split) | Comparing a change against baseline | 3-7 days | High — quantitative, statistical |
| Feature flag rollout | Measuring adoption and engagement | 2-5 days | High — real usage data |
| Landing page / fake door | Testing demand before building | 1-3 days | Medium — intent, not commitment |
| Wizard of Oz (manual backend) | Testing UX when full automation is overkill | 1-2 days | Medium — real interaction, artificial scale |
| Concierge (1:1 manual delivery) | Deep understanding of value prop | 1-3 days | Medium — rich but small sample |
| User interview + live prototype | Understanding the "why" behind behavior | 1 day | Low-Medium — qualitative, biased |

Most BTTR tests should resolve fast. If you need months of data, you're not testing — you're stalling.

**Designing a good test:**

Before you build, answer these three questions:

1. **What signal would prove this idea right?** Be specific. "Users like it" is not a signal. "At least 20% of users who see the new onboarding complete it" is a signal.
2. **What signal would prove this idea wrong?** Equally important. Define failure before you ship.
3. **How fast can we get that signal?** Optimize for speed.

> **Example (continuing):** You define success as: "Activation rate (users who complete onboarding and perform one core action) increases from 12% to 20%+ in the test group." You define failure as: "Activation stays flat or the new flow has a higher drop-off rate than the old one." You roll it out to 15% of new signups via feature flag. You'll have enough data in 4 days.

---

### 3. TRASH

This is where most teams fail — not because trashing is hard, but because *not trashing* feels productive. Iterating on something broken gives you the illusion of progress. It's the most expensive kind of waste: effort that looks like work.

If the signals say no, kill it. No post-mortems. No "let's iterate one more time." No sunk cost theater.

**When to TRASH:**

- **Signals are flat or negative.** You tested it fairly and the needle didn't move. The idea didn't work.
- **The problem was wrong.** Users don't actually have this problem, or it's not painful enough to change behavior.
- **A better direction emerged.** Something you learned during testing reveals a more promising direction. Pursue that instead.
- **You can't articulate the next iteration.** If you stare at the results for 5 minutes and can't say "the specific thing I'd change is X," there's nothing to iterate on. Trash it.

**When to ITERATE (not trash):**

- **Right problem, wrong shape.** Users clearly have the problem and engaged with your solution, but the UX is tripping them up. The *what* is right; the *how* needs work.
- **Fixable friction.** Users are engaging but dropping off at a specific, identifiable point. You can see exactly what to fix.
- **Value lands, packaging doesn't.** Users who "get it" love it, but too many don't "get it." That's a messaging/positioning problem, not a value problem.

**The emotional test:** Are you iterating because the *data* suggests refinement, or because *you* don't want to let go? If you can't honestly answer that question, you're not ready to make the call. Show the data to someone who wasn't involved in the build and ask them.

> **Example (continuing):** After 4 days, the data comes in: activation rate in the test group is 14%, up from 12%. That's movement, but it's not the 20%+ you defined as success. However, you notice something: users who completed the AI-generated insight had a 38% activation rate. The problem is that 60% of users *skipped the insight entirely* — the UI buried it. This is "right problem, wrong shape." You iterate. The next cycle focuses entirely on making the insight un-skippable.

---

### 4. REPEAT

This is not a phase — it's a decision point. Every REPEAT is a fork:

**Path A: Iterate**
You're running another cycle on the same problem. The idea evolves.

What carries forward:
- Everything you learned about the user and the problem
- Specific signals about what worked and what didn't
- Code that's worth keeping (but be honest — most isn't)

What does NOT carry forward:
- Attachment to the previous solution
- The assumption that you're "close"
- Sunk cost logic ("we already built half of it")

**Path B: Pivot**
You're running a new cycle on a different problem. The idea changes entirely.

What carries forward:
- Problem understanding (what you now know users *don't* need)
- Pattern recognition (what kinds of signals were strongest)
- Speed (you'll be faster this time)

What does NOT carry forward:
- Code from the previous build
- The problem framing
- Hope that the old idea will "eventually" work

**How many iterations before you trash?**

There's no universal number, but here's a heuristic: **3 cycles max on the same problem.** If three honest cycles of build-test haven't produced a clear upward trajectory in your target signal, the problem isn't your solution — it's the idea. Pivot.

> **Example (conclusion):** Cycle 2: You rebuild the onboarding with the insight front-and-center — users literally can't proceed without seeing it. Four days later: activation rate hits 26%. That's above your 20% threshold. The bet paid off. Now you have a decision: do you iterate further to push it higher (path A), or take this win and pivot to the next highest-value problem (path B)? Your PM judgment says: the activation problem is meaningfully solved. Time to place a new bet. You pivot to retention.

---

## The Cycle Format

Every BTTR cycle has three moves. The idea creates the process — not the other way around.

```
IDEA:    [What you want to build and why — the insight, the hunch, the value proposition.]
BUILD:   [What you shipped and how fast — the working prototype, not a spec.]
SIGNAL:  [What you observed — real data, real behavior, real outcomes.]
```

**Sharp cycle:**
```
IDEA:    Show new users a personalized insight within 60 seconds of signup —
         onboarding should deliver value, not explain features.
BUILD:   AI-generated onboarding flow that imports sample data and surfaces
         a personalized insight. Shipped in an afternoon.
SIGNAL:  Rolled out to 15% of signups. Activation went from 12% to 14%.
         But insight-completers hit 38%. Right idea, wrong shape.
```

**Vague cycle:**
```
IDEA:    Make onboarding better.
BUILD:   Redesign the onboarding screens. Took 3 sprints.
SIGNAL:  Users said it "feels nicer." No metric moved.
```

The difference: the sharp cycle starts with a concrete idea, ships a working prototype fast, and produces a clear signal you can act on. The vague cycle starts with nothing specific, over-builds, and produces nothing measurable — a zombie feature that'll walk your roadmap forever.

---

## A Full BTTR Story: Three Cycles

Here's what BTTR looks like across multiple cycles on a real-ish product. Meet **Pulse**, a B2B analytics tool.

### Cycle 1: Activation

**Idea:** Replace the feature tour with an auto-generated insight using the user's own data — show value in the first 60 seconds instead of explaining features.

| Phase | What happened | Duration |
|-------|--------------|----------|
| BUILD | AI built a new onboarding flow that imports sample data and generates a personalized insight. Rough around the edges. | 1 day |
| TEST | Rolled out to 15% of new signups. Measured activation rate over 4 days. | 4 days |
| DECISION | Activation went from 12% → 14%. Not enough. But insight-completers activated at 38%. Most users skipped the insight — it was buried. | — |
| OUTCOME | **Iterate.** Right problem, wrong shape. | — |

### Cycle 2: Activation, Refined

**Idea:** Make the personalized insight un-skippable — it's step 1 in onboarding, not an optional sidebar.

| Phase | What happened | Duration |
|-------|--------------|----------|
| BUILD | Rebuilt onboarding so the insight is step 1, not optional sidebar. AI refactored the flow in half a day. | 0.5 days |
| TEST | Same 15% holdout. 4 more days of data. | 4 days |
| DECISION | Activation hit 26%. Clear win. | — |
| OUTCOME | **Pivot.** Activation solved. Move to next problem. | — |

### Cycle 3: Retention

**Idea:** Users who don't return within 72 hours never come back. Send a "your data changed" email with a specific insight at hour 48 to pull them back.

| Phase | What happened | Duration |
|-------|--------------|----------|
| BUILD | AI built an automated email pipeline: detect data change → generate insight → send personalized email. | 1.5 days |
| TEST | Triggered for all users who hadn't returned by hour 48. Measured 7-day retention. | 7 days |
| DECISION | 7-day retention went from 31% → 33%. The email open rate was high (52%) but click-through was low (4%). Users saw it but didn't care enough to come back. | — |
| OUTCOME | **Trash.** The email isn't the right lever for retention. The insight in the email wasn't compelling enough to pull someone back. Time to rethink the retention problem entirely. | — |

**Three cycles. Three weeks. One clear win, one clear loss, one refined into success.** In the old world, these would have been three items on a roadmap debated for a quarter before any of them shipped.

---

## The PM's Role in BTTR

BTTR doesn't eliminate the PM — it redefines the job.

The PM is no longer the person who decides *what to build* through analysis. The PM is the person who:

1. **Identifies problems worth solving.** The one input AI can't generate. Taste, judgment, customer intimacy — the ability to look at data and a market and say "this is the problem that matters." This is the job now.

2. **Shapes the idea.** Translating a hunch into a concrete, buildable concept with clear success criteria. This is the skill that separates PMs who thrive in BTTR from PMs who flounder.

3. **Defines what signal to look for.** What will tell us this worked? How do we get that signal fast? Looking for the wrong signal wastes an entire cycle.

4. **Reads the signal.** Interpreting data, separating noise from insight, seeing the story in the numbers. Not every result is clean. The PM's job is to make the call when the data is ambiguous.

5. **Makes the trash/iterate/pivot decision.** The hardest part. Requires ego death and intellectual honesty. The best PMs in BTTR are the ones who can kill their own ideas fastest.

6. **Directs AI.** Translating problem understanding into build instructions. Clear problem statements, sharp constraints, good judgment about what matters. This is the new core skill.

**What PMs stop doing:**

- Writing PRDs (replaced by the idea itself)
- Estimating effort (irrelevant when effort approaches zero)
- Negotiating scope (build the whole thing, test it, trash what doesn't work)
- Running prioritization ceremonies (replaced by the cycle itself)
- Building consensus before shipping (ship, then let results build consensus)
- Guessing confidence levels (you'll *know* after the test)

---

## How Teams Adopt BTTR

You don't reorganize your company to adopt BTTR. You run one cycle and let the results speak.

### Week 1: Pick one idea

Choose one problem your team believes in. Don't score it. Don't compare it. Just pick the one where you have the strongest conviction AND the clearest signal you could test against.

Write the cycle. Three lines: idea, build, signal.

### Run the first cycle

Build it. Test it. Make the call: iterate, pivot, or trash.

The first cycle will feel uncomfortable. You'll want to plan more. You'll want to polish. You'll want to "align stakeholders." Resist. Ship it ugly and let the signal tell you if it matters.

### Scale: Run cycles in parallel

Now you have muscle memory. Run concurrent BTTR cycles. Different problems, different tests. You'll start to notice: the bottleneck isn't building. It's not testing. It's *deciding*. The trash/iterate decision is where teams get stuck. Get faster at that.

### BTTR as operating rhythm

The team's cadence becomes the cycle, not the sprint. Work is organized around bets and signals, not tickets and story points. Standups become: "What did we learn? What are we testing next?"

### What about the existing roadmap?

BTTR doesn't require burning your roadmap on day one. Start by running BTTR cycles alongside your existing process. When BTTR consistently outperforms your prioritization framework at finding the right thing to build, the framework dies on its own. You won't need to argue for it. The results argue for themselves.

---

## Handling Competing Ideas

*"If we can build everything, how do we choose what to build first?"*

You don't choose — you race.

**The BTTR approach to multiple ideas:**

1. List the *problems* (not solutions) you could tackle
2. For each, write the cycle in 3 lines (idea, build plan, signal to watch)
3. For each idea, ask: "What's the fastest build that would produce a signal?"
4. Start with the idea where the build is fastest and the signal is clearest
5. Run multiple cycles in parallel when capacity allows

**What you're optimizing for:** Learning velocity. Not output. Not throughput. Not features shipped. How fast can you go from *"we think this matters"* to *"we know whether this matters."*

The team that learns fastest wins. Not the team that ships the most, or plans the best, or has the prettiest roadmap. The team that resolves uncertainty fastest.

---

## BTTR vs. Everything

| | RICE / WSJF / ICE | Lean Startup | A/B Testing | Design Thinking | BTTR |
|---|---|---|---|---|---|
| **What it is** | Prioritization framework | Startup methodology | Measurement method | Problem-solving process | Decision framework |
| **Core question** | "What should we build?" | "Should we build this?" | "Which option is better?" | "Do we understand the problem?" | "What did we learn?" |
| **Assumes building is** | Expensive (choose carefully) | Moderately expensive (minimize) | Already done (compare options) | Expensive (research first) | Near-free (build to learn) |
| **Decision made by** | Spreadsheet scores | Validated learning | Statistical significance | Empathy research | Observed signal |
| **Decision speed** | Slow (committee-driven) | Moderate (validated learning) | Fast (statistical) | Slow (research-first) | Fast (evidence-driven) |
| **Key innovation** | Structured comparison | Validate before scaling | Rigorous measurement | User empathy | Kill the prioritization layer |
| **Era** | Pre-AI (2000s) | Early startup era (2011) | Web optimization (2000s+) | Design era (2000s) | AI era (2024+) |
| **Failure mode** | Build the wrong thing confidently | Validate too slowly in fast markets | Optimize locally, miss the big picture | Research paralysis | Trash good ideas too early* |

*BTTR's failure mode is real. Mitigation: define clear test criteria BEFORE building, so you're evaluating against signal, not feeling. And give iterations a fair shot — up to 3 cycles before trashing.

**How BTTR relates to each:**
- **RICE/WSJF/ICE:** BTTR *replaces* these. They're the prioritization layer that AI made obsolete.
- **Lean Startup:** BTTR is the *spiritual successor* — same philosophy (validate through shipping), updated for a world where AI makes building near-free. If Lean Startup were written today, it would look a lot like BTTR.
- **A/B Testing:** BTTR *uses* this. A/B tests are one of several tools in the TEST phase. They're a great method; they're not a framework.
- **Design Thinking:** BTTR *complements* this. Use Design Thinking techniques when you need deeper problem understanding, but don't let research become a substitute for shipping.

---

## Common Objections

**"Not everything can be prototyped in a day."**
Most things can be tested faster than you think. The question isn't "can we build the full feature in a day?" — it's "can we build *enough* to get a signal?" A landing page tests demand. A Wizard-of-Oz flow tests UX. A hardcoded prototype tests value. You don't need the engine to test the car's shape.

**"What about infrastructure / platform work?"**
BTTR is for product decisions — features, experiences, and user-facing changes. Infrastructure work has its own constraints (reliability, scalability, security) that don't map to user signal. That said: if you're building infrastructure "in case we need it," BTTR's question still applies — can you prove the need before building the solution?

**"My company requires stakeholder buy-in before shipping."**
Ship the prototype to a small group first. Bring the *results* to stakeholders, not the *proposal*. "We tested this with 200 users and activation increased 14%" is a fundamentally different conversation than "We think this might work and here's a deck."

**"What if we trash something that would have worked with more iteration?"**
Possible. That's BTTR's failure mode. The mitigation is twofold: (1) define success criteria before you build, so you're not judging on vibes, and (2) give yourself up to 3 cycles on a problem before calling it. If 3 cycles don't show a trajectory, it's not iteration you need — it's a different idea.

**"How is this different from just... being agile?"**
Agile optimizes the *process* of building. BTTR optimizes the *decision* of what to build. Agile says "ship in 2-week sprints." BTTR says "ship in 2 days and find out if it matters." Agile is compatible with BTTR — it's just not sufficient. You can run perfect sprints and still build the wrong thing for 6 months.

**"Isn't this just user testing with a brand name?"**
No. User testing is a research method — you watch people use your product and gather qualitative insights. BTTR is a decision framework — it determines what your team works on, how long they spend on it, and when to kill it. User testing might be one input in a BTTR test phase, but BTTR also uses quantitative signals (conversion rates, retention, revenue) that user testing doesn't capture. More importantly, user testing doesn't have a "trash" phase. BTTR does, and that's the hardest, most valuable part.

---

## Quick Reference

### The Cycle
```
BUILD  →  TEST  →  TRASH  →  REPEAT
 ship fast    get signal   be honest    iterate or pivot
```

### The Cycle Format
```
IDEA:    [What you want to build and why.]
BUILD:   [What you shipped and how fast.]
SIGNAL:  [What you observed — data, behavior, outcomes.]
```

### The Decision Framework
```
Signals positive + clear next step    →  ITERATE
Signals negative + problem is wrong   →  PIVOT (new idea)
Signals negative + 3 cycles spent     →  TRASH (move on)
Signals ambiguous                     →  Refine the test, not the build
```

### The 5-Minute Rule
If you can't articulate exactly what you'd change in the next iteration within 5 minutes of seeing the test results, trash it. If the next build would be fundamentally different from the last one, that's not iteration — that's a new idea.

---

## Why This Works: The Philosophical Grounding

BTTR's epistemology isn't new. It echoes a 200-year-old debate in philosophy.

**Immanuel Kant** argued that we can never directly access the *noumenon* — the thing-in-itself. All we have are *phenomena* — things as they appear to us through perception and reasoning. We're trapped behind a veil. We can build models, but we can never truly know the underlying reality.

This is how traditional PM frameworks operate. RICE, WSJF, ICE — they're all Kantian. They assume user behavior is fundamentally unknowable before you ship, so you build elaborate scoring systems to *approximate* what might work. Confidence levels are literally an admission that you're guessing. The entire framework is a model of a reality you can't access.

**Georg Wilhelm Friedrich Hegel** rejected Kant's split. He argued that truth isn't hidden behind an inaccessible curtain — it *unfolds through a dialectical process*: thesis → antithesis → synthesis. You don't access truth by theorizing harder. You access it through contradiction, action, and resolution. Each pass reveals more of the real.

This is BTTR.

| | Kantian (RICE) | Hegelian (BTTR) |
|---|---|---|
| **How you find truth** | Reason about it abstractly | Act and observe what happens |
| **The model** | Score → Rank → Predict | Build → Test → Learn |
| **Confidence** | Estimated before the fact | Earned through evidence |
| **Failure** | "Our model was wrong" | "We learned something" |

The BTTR cycle *is* dialectical: **Build** (thesis) → **Test** (antithesis — reality contradicts your assumptions) → **Trash/Repeat** (synthesis — a new understanding emerges). Each cycle resolves a contradiction and moves closer to the truth.

Every major scientific breakthrough follows this pattern, not the Kantian one. Einstein didn't score relativity in a prioritization framework. He daydreamed an idea, then designed experiments to prove or disprove it. Newton didn't run a committee to evaluate gravity. Darwin didn't A/B test evolution. The idea came first — then the process existed to validate it.

BTTR formalizes this. The idea creates the process, not the other way around.

**The distilled version:** Truth isn't predicted. It's revealed through action. RICE tries to theorize about what users want. BTTR lets reality speak for itself.

---

*BTTR v0.5. This document was built, tested, and iterated using BTTR itself.*
