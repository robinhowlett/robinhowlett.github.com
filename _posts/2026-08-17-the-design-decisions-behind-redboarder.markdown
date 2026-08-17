---
layout: post
title: "The design decisions behind redboarder"
tags: redboarder horseracing ai design
---

I introduced [redboarder](https://redboarder.com), a place to practice the craft of handicapping with an AI partner, in [a separate post]({% post_url 2026-08-17-introducing-redboarder %}). This one goes under the hood: not what it does, but *why* each piece is shaped the way it is.

Most of the interesting decisions in a product are invisible in the finished thing. You only see them if someone tells you what the alternatives were and why they lost. So this is a walk through the main ones, roughly in the order you'd meet them using the app: why the races are old, which ones qualify, why I built my own rating system, why the AI sits where it does, how you bet, how the results stay honest, and why the AI operates under such tight rules.

Nearly all of it comes back to two masters that every decision has to serve at once: **keep it honest**, so the practice is real, and **keep it cheap enough that one person can run it.**

<!-- more -->

### The cards: why old, why not the big ones, and which ones qualify

The choice to use *finished, historical* races isn't just thematic. It's load-bearing.

Because a historical race never changes, there's nothing to compute at request time. I can run the entire analytical pipeline offline, once, and serve the result as static files for a fraction of a cent each. And because the outcome is already known, the app can *grade you honestly* the moment you commit. A live product can't do either of those things. Live racing also can't be practiced with: the real thing trickles out one race every thirty or forty minutes, most of which you don't care about. Historical racing is infinite and on demand.

I leave out the marquee races: no Grade 1 or Grade 2 stakes. Those are the most over-analyzed races in the sport, and the least representative of the day-to-day grind where handicapping skill compounds. A Breeders' Cup race is a spectacle; a Tuesday claimer at Parx is a puzzle you can get good at.

The rest of the qualification bar exists to keep every dealt card genuinely bettable:

Rule | Why
---- | ----
From 2005 on | Chart data quality and completeness
≥ 8 races on the card | A full session, not a fragment
≥ 8 runners per race | Competitive fields with real exotics
Trifecta pool ≥ $20,000 | Enough liquidity that the payoffs mean something
No Grade 1 / Grade 2 | Keep it the representative grind, not the showcase
≥ 20 qualifying cards per track | Depth per track, so a venue isn't represented by one fluke day

That last one matters more than it looks: it means you can be dealt the same track repeatedly and start to *learn a circuit*, the way a real regular does.

### Why I built my own performance rating

Every horse in redboarder carries a **Performance Rating (PR)**: my own number, not a Beyer, Brisnet, or Timeform figure. Building a rating system from scratch is a strange thing to do when good ones already exist, so it's worth explaining why.

Four reasons, and they compound:

1. **It's mine, so I can give it away.** redboarder is a free product built on more than a million races. Licensed speed figures cost money and can't be redistributed inside something like this. A rating I compute myself, I can serve to anyone.
2. **It's call-by-call, not a single number.** PR exists at every point of call (2f, 4f, 6f, finish), not just as one final figure. That's what lets it feed the *pace* and *running-style* models, not merely answer "who ran fastest once." A closer and a front-runner can post the same final figure and be different horses; the shape of their PR across the race is where that lives.
3. **It's calibrated to my probability model.** The whole system hinges on one empirically-fit constant: a **2.7-PR-point** edge doubles a horse's win probability (measured across 1.8 million starters). A bought figure isn't denominated in my model's units; mine is, by construction. PR points convert cleanly into win probability and, from there, into the blend with the market. A rating I didn't build couldn't do that.
4. **It's point-in-time, because I control it.** When you're playing a day in 2016, the ratings must reflect only what was knowable *then*. Because I compute PR myself, I can guarantee that: no leakage from a horse's later races creeping into its number.

> PR isn't a speed figure with my name on it. It's the unit my probability model is denominated in, which is exactly why it had to be mine.

### The interface: the AI beside the past performances

The screen is split for a reason: past performances on the left, the AI on the right, both visible at once. Handicapping is an act of *reading data and forming an argument about it at the same time*, so the data and the conversation have to sit side by side, not one behind a tab you flip away to.

![The handicapping surface: race tabs, conditions, a pace read, the wagering pools, and expandable past-performance lines per horse](/assets/images/posts/2026/interface.png)

The PP lines expand on demand because past performances are dense; showing everything at once is a wall, showing nothing is useless, so the default is a readable summary that opens into full detail when you want it. Names the AI mentions are clickable and drive the left panel, and the app's own jargon (PR and the like) carries hover-glossary definitions, because the fastest way to lose a newcomer is a wall of unexplained abbreviations.

### Betting: a slip and a conversation

You can bet two ways, and that's deliberate.

There's a conventional **bet slip** (tap horses, pick a bet type, set an amount) for people who like to build a ticket by hand. And you can just **say it**: *"put $20 to win on the 7,"* *"small trifecta box the top three."* The AI turns that into a structured proposal and hands you a one-tap confirm. (The chat path exists because an early tester got shut out at the window with an opinion and no obvious way to act on it from the conversation. The friction was the point.)

Two rules govern the betting, and both are about trust:

- **Propose, then confirm, never auto-place.** The AI emits a bet *structure*; you confirm it. That guards against a mis-parse ("the 7" → the wrong horse), keeps a human hand on the (virtual) bankroll, and means an invalid proposal never touches your money: the app hands the reason back and the AI corrects itself.
- **The AI never does the arithmetic.** It doesn't compute cost, combinations, payoffs, or whether a bet cashed. A deterministic engine owns all of that and is the single source of truth. This isn't fussiness. The AI once told a tester, with total confidence, that trifectas couldn't be played for 50¢ (they can). Language models are for judgement and conversation, not for math you need to be *right*. So it does the reading, and the engine does the reckoning.

### Keeping the results honest

The core promise, that you commit before you're allowed to know the answer, is enforced in the *data*, not in a rule the AI is asked to follow.

Each race is split into two files: everything visible beforehand, and a separate file with the finish, payoffs, and replay. The results file can't be fetched until a **commitment token** exists for that race, and reveals are hard-gated in order, so you can't jump to race 8 to see how the day ends. It's a small state machine, and it's the reason "no peeking" is a property of the system rather than a promise on the honour system. (How that holds up in a static app that's really just files on a CDN is its own interesting problem, one for the next post.)

### Keeping the AI honest

A conversational partner introduces a failure mode a bet slip never has: it can *make things up*, and in a practice tool a confident fabrication is worse than useless. So the AI runs under a short list of hard rules, and each one exists because of a specific way it could ruin the experience:

- **Never state or invent a result.** This is a game about not knowing the outcome; an AI that says "he held on to win" has destroyed the entire point in one sentence. It cannot describe a race in the past tense until the system hands it the official result.
- **Never invent a runner.** It may only discuss horses present in the data it's been given: no half-remembered names, no made-up program numbers for a race it hasn't been shown.
- **Never do the betting math** (as above); the engine is the source of truth.
- **Propose, don't place**: every bet routes through your confirmation.

On top of the persona itself: it speaks in the first person, it treats *your* opinion as primary, and (the rule I'm most attached to) it holds its own opinions loosely. It'll state a structural view once, with a reason, and then build whatever you ask for without steamrolling you. A partner that browbeats you into its own ticket is just a tipster with extra steps.

### The reveal, and learning from it

Committing is only half the loop; the other half is finding out *why*.

The reveal shows the finish, the payoffs, and each horse's **actual PR**, so you can compare how the field really rated to how you read it. Then there's a **race replay**: an animated reconstruction of the race with a live win-probability curve from gate to wire and a per-horse trip assessment (who got a pace collapse to close into, who was compromised). It's the difference between "you were wrong" and "you were wrong *because the pace didn't fall apart the way you expected*," which is the only kind of feedback that makes you better. The replay is rendered from the chart data itself, which is also how it dodges the licensing swamp of race video.

A separate reflection step then debriefs the race around **calibration**: not just did you win, but were you right for the right reasons. You can lose a bet on a good decision and win one on a bad one, and a practice tool that only tracks the money teaches you the wrong lesson.

### Why three system prompts, not one

The AI doesn't run on a single prompt. There are three, scoped to the phases of a session: a short **card overview** at the start, a full **analytical** prompt through commitment, and a **reflection** prompt for the debrief. Splitting them keeps each one focused on the behaviour that phase needs, and it's cheaper: the overview is precomputed and served as static text with no model call at all, and the analytical prompt stays stable enough to cache.

But the deeper point is that the prompt is where the *product philosophy* lives. "Partner, not tipster" isn't a tagline; it's a rule that says state your view once, then build what the user asks. And "keep it honest" is the rule that forbids inventing a result, not a mission statement. When people ask how you get an AI feature to behave a particular way, the honest answer is that you write down, in exhaustive detail, the things it must never do. Each line is a scar from a time it did.

### The thread running through all of it

Read back over these and the same two constraints keep reappearing. Half the decisions serve *keeping it honest*: the historical races, the pre/post split, the commitment token, the rules against fabrication, the calibration-focused reveal. The other half serve *keeping it cheap*: precompute everything, my own rating instead of a licensed one, static files, a cached prompt, a rendered replay instead of licensed video.

That's what falls out of building something real, alone, on a budget: you can't paper over a bad decision with a bigger team or a bigger bill, so every choice has to earn its place against both masters at once. In [the next post]({% post_url 2026-08-17-compute-then-narrate %}) I'll get into how the AI half is built to be convincing, cheap, and hard to fool, including where I went against the grain of how most people wire their own data into a model.
