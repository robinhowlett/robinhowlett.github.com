---
layout: post
title: "Introducing redboarder: practice the craft of handicapping, with an AI partner"
tags: redboarder horseracing ai llm
---

Becoming a successful horseplayer is extremely difficult. Interpreting form, pace, class, and the myriad of other variables that can affect the performance of a living creature, and turning that read into a wagering decision that reflects the value your opinion identified across [a host of different bet types]({% post_url 2018-08-12-visualizing-inefficient-multi-ticket-horizontal-wagering-tickets %}) - well, it's one of the last forms of betting where a sharp individual can still find an edge against both the "house" (takeout etc) and the crowd and profit handsomely when they are right.

Improving these skills, however, is more challenging than it should be, for a handful of reasons that pile on top of each other.

Start with the structure. Pari-mutuel wagering, the way it works in America, is zero-sum by definition: everyone bets into the same pool, so your edge comes straight out of someone else's payout. Which means nobody who's actually good at this has the slightest incentive to help you get better. The loudest voices in the space are tipsters, and their business model is keeping you dependent on their picks instead of building your own judgement.

Then there's where the attention goes. Winning at the races is, in the end, a *betting* problem. The edge is thin, and what little of it exists lives in the dry, objective side of the craft: value, pool dynamics, staking, discipline. That side is unglamorous and binary (you either had the value or you didn't), so it gets almost none of the airtime. What gets debated endlessly, on every handicapping show and in every tip sheet, is the *opinion*: who the best horse is. It's subjective, it's arguable, it's fun, and it's the part that matters least once you can already read a race. Newcomers pour their hours into the entertaining half and starve the half that decides whether they win.

And the cost of learning the hard way is brutal. Pari-mutuel takeout, the house's cut of every pool, dwarfs the vig at a sportsbook, so every bet you place while you're still bad is fighting a steep built-in edge before you've even been wrong. Put the takeout, the tipster noise, and a genuinely thin edge together, and a beginner betting live money mostly just watches the bankroll bleed away as tuition. Even if you're happy to pay that tuition, you can't practice efficiently. Live racing trickles out one race every thirty or forty minutes, most of them cards you don't care about, with no way to drill when you actually have a free hour.

So the problem was never a lack of information. Old races have known outcomes, so replaying them teaches you nothing your hindsight doesn't already know. Tipsters just hand you the pick, so following along tests nothing. You can read forever and still have no honest signal on whether you're any good.

I spent years building the raw material for this without quite admitting it was the gap I kept circling: [parsing Equibase chart data]({% post_url 2019-11-29-parsing-structured-data-complex-pdf-layouts %}), building [Handycapper](https://www.thoroughbreddailynews.com/getting-from-cease-and-desist-to-come-work-with-us/), and assembling a database of more than a million races. The industry has talked about technology for as long as I've been around it, and not much of it ever shipped. It turned out an independent with the data and a few ideas could just build. But data alone doesn't sharpen you; it's something you query, not something that makes you better. What I wanted was a place to make a real call and find out, honestly, whether I was right, and along the way to see what a bit of genuine product thinking could do in a corner of the world that hasn't seen much of it.

So I built it. It's called [redboarder](https://redboarder.com), and this post is a look at what it is: who it's for, how it works, what's in it, how it was built, and why I think it's interesting.

![redboarder: past performances on the left, an AI handicapping partner on the right](/assets/images/posts/2026/redboarder-hero.png)

<!-- more -->

### Real decisions, honestly graded

redboarder deals you a real historical card, race by race, and asks you to commit to a read and a bet before the results are revealed. That's the whole core of it. Your judgement is always on the line, and it's always graded, with no hindsight to lean on.

Not every historical card is fair game. Races have to clear a quality bar to qualify: 2005 or later, at least eight races on the card, at least eight runners per race, real wagering pools behind them, and no Grade 1 or Grade 2 stakes races, which are the most over-analyzed and least representative of the day-to-day grind of handicapping. The idea is to keep the cards genuinely bettable, the way an actual card at the track would be.

> The rule that shapes the whole experience is simple: you commit before you're allowed to know the answer.

### A partner, not a tipster

The key design decision behind redboarder was that the AI had to be a partner, not a tipster. A tipster defeats the entire point of the exercise: if it just hands you the pick, you're back to not practicing anything.

So the AI is built to behave differently. It opens by asking what you're seeing, drawing out your read before it offers its own. It pushes back on your reasoning instead of rubber-stamping it. It only leads if you ask it to. There's no mode selector for this, no toggle between "quiz me" and "just tell me." It works out what you need from how you're engaging with it. The distinction that matters is between a tool that makes you dependent and one built for deliberate practice with a real feedback loop. A tipster makes you faster today and no better tomorrow. A partner is only worth anything if it leaves you sharper than it found you.

### How it works, and what's in it

The interface is a split screen. Past performances live on the left, the AI conversation on the right.

The left panel has race tabs for the full card, a sortable runners table, full past-performance lines for each horse, a pace summary, pool information, and bias signals, with results appearing there only after you've made your call. The right panel is where the work of handicapping happens: the back-and-forth with the AI partner as you build your read.

What's in it, concretely:

- A qualifying card of real historical races, picked to be genuinely bettable rather than showcase stakes events
- A full per-race analysis suite covering form, pace, class, and pool signals
- An adaptive AI partner that asks before it tells, and leads only when asked
- A bet slip covering five bet types, with real profit-and-loss settlement against the pool payouts
- Precomputed instant openers, so a card is ready to work the moment you want it
- The reveal (results, payoffs, performance ratings, and chart footnotes), held back until you've committed

### How I built it

redboarder is the front door to a stack of racing infrastructure I've been building for years, not a project that started from scratch. Behind it sit six repos, each doing a specific job: **chartbase** for parsing and structuring race chart data; **race-explanation** for the per-horse narrative analysis; **racing-stats** for the underlying statistics, kept strictly point-in-time-correct so a day in 2016 only ever sees what was knowable *then*, with no leakage from the future (otherwise the whole exercise would be cheating); **wagering-analytics** for pool and payout logic, including Stern-Harville fair values for the exotics; **bet-calculator** for turning a read into a settled bet; and **race-day-sim** for reconstructing full historical cards to deal.

The modeling underneath draws on a Benter-style blend of model output with market odds, weighted at roughly 30% model trust; a recency-weighted form read with a five-start half-life; an ability multiplier built from a dataset of 1.8 million starters; and an actual-over-expected curve that catches where the market is mispricing a horse.

The architecture, by contrast, is boring on purpose. Because historical race data never changes, everything that can be precomputed offline is baked down to static JSON ahead of time; the whole thing runs behind a single [Cloudflare Worker](https://workers.cloudflare.com/) with no live database to maintain; and [Claude](https://claude.com/) sits in as the partner at a cost of roughly a cent per conversational turn. I'll get into [the cost mechanics]({% post_url 2026-08-17-compute-then-narrate %}), and [how the reveal stays hidden]({% post_url 2026-08-17-the-design-decisions-behind-redboarder %}), in later posts.

### What I think is interesting about it

A few things stand out to me. It rewards skill rather than luck, which is rare for anything built around betting. The partner-not-tipster design means it develops your skill instead of replacing it, which was the whole reason I built it. And it's the payoff for years of infrastructure work that never had a clear destination until this one. There's real engineering craft under a thing that, on the surface, just looks like a card and a chat window.

### Try it

redboarder is live at **[redboarder.com](https://redboarder.com)**. It's early, it's rough in places, and it's still changing week to week. Deal a card, commit before you look, and see what happens.

Then check the reveal and see how good your handicapping really is. I'd love to know whether this sharpens people's game, or whether it just turns out to be good fun. Either answer would tell me something.
