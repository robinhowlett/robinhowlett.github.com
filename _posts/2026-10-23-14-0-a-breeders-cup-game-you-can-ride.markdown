---
layout: post
title: "14–0: a Breeders' Cup game you can ride"
description: "Draft one horse for every Breeders' Cup race since 1984, then watch or ride the races yourself. Where 14–0 came from, how it works, and how it was built in 38 hours."
image: /assets/images/posts/2026/14-0/chase-today.jpg
comments: true
tags: horseracing 14-0 games
---

{% include video.html src="/assets/video/posts/2026/14-0-flightline-ride.mp4" poster="/assets/images/posts/2026/14-0/flightline-ride-poster.jpg" title="Riding Flightline down the stretch at Keeneland in 14–0, chase camera behind the field" caption="Riding Flightline at Keeneland" %}

The 2026 Breeders' Cup is at Keeneland on [October 30 and 31](https://lex18.com/news/covering-kentucky/breeders-cup-world-championship-returns-to-keeneland-in-2026), and I've launched a game for it. [14–0](https://14-0.net) is free: you draft one horse for each of the 14 Breeders' Cup races from every running since 1984, then sim the card, watch each race, or ride it yourself, at the track where that year's race was run.

In this post, I explain where it came from, how it works, and how it was built.

<!-- more -->

### Churchill Downs, 2010

Back in 2010, the year [Blame beat Zenyatta](https://en.wikipedia.org/wiki/2010_Breeders%27_Cup_Classic), I built a very simple and frankly unimpressive fantasy game for the Breeders' Cup. I was on the Breeders' Cup Fan Advisory Council (they'd found a few of us through social media), and the council held a draw to decide who would go to the track. I have a feeling they rigged it in my favor.

It turned out to be my honeymoon. I'd gotten married a few days before, and we spent both days at Churchill Downs.

<div style="display:flex;gap:8px;flex-wrap:wrap;align-items:flex-start">
<img src="/assets/images/posts/2026/14-0/bc-2010-credential.jpg" alt="A Breeders' Cup World Championships 2010 Churchill Downs credential, November 5th-6th" style="flex:1 1 260px;min-width:0;border-radius:6px">
<img src="/assets/images/posts/2026/14-0/churchill-2010-honeymoon.jpg" alt="Robin and his wife on a balcony high above the track at Churchill Downs at night, the infield lit up behind them" style="flex:1 1 260px;min-width:0;border-radius:6px">
</div>
<p class="caption-text" style="text-align:center">Churchill Downs, November 2010</p>

The first version of the game had you pick a winner to stay alive. Around race three or four on day one, a huge outsider won and knocked everyone out. So I stayed up all night and rewrote it around a budget. Morning-line odds set each horse's price, you had a limited bank balance, and you had to decide where to single and where to spread. It launched that Saturday morning and worked a lot better.

<div style="display:flex;gap:8px;flex-wrap:wrap;align-items:flex-start">
<img src="/assets/images/posts/2026/14-0/louisville-2010-hotel-rewrite.jpg" alt="Robin at a hotel-room desk in Louisville, typing on a laptop by the window" style="flex:1 1 260px;min-width:0;border-radius:6px">
<img src="/assets/images/posts/2026/14-0/churchill-2010-laptop.jpg" alt="Robin in a suit at the track, working on a laptop" style="flex:1 1 260px;min-width:0;border-radius:6px">
</div>
<p class="caption-text" style="text-align:center">Louisville, that weekend</p>

My father, who's not much of a racing fan, entered to support me. Going into the last race he was first or second, and I was dreading him winning and me being accused of rigging it. Luckily someone else came through.

Toby Keith played a concert on the Thursday or Friday night, with a lot of gyrating in tight jeans and a stage surrounded by Ford pick-up trucks (his sponsor). I think I saw him in the box I watched the races from the next day. I have nothing against the guy - he's an entertainer, and that's part of the business.

And I remember Zenyatta prancing around the paddock, the crowd around her, and then the collective groan when she was beaten.

That game was the [small social app for the 2010 Breeders' Cup]({% post_url 2015-08-06-farewell-sportslabs %}) I mentioned when I left SportsLabs.

### From 82–0 to 14–0

This summer, I built a horse racing version of [82–0](https://aftermath.site/82-0-free-basketball-game-browser), the viral basketball game. I needed something in racing that worked like a tournament, and the Breeders' Cup was the obvious choice. After a few variations, I ended up with two modes: Weekend Warrior (originally called Claimer) and Railbird.

Each of the 14 races starts with a spin that lands on a year, and you pick one horse from that year's field. You can't use the same year twice. Once all 14 are in, each one runs against a field drawn from across the eras.

The archive covers 422 Breeders' Cup races from 1984 to 2025: 1,266 starts by 1,097 horses. Each horse is rated on how good it really was, relative to its own field, because a turf router and a dirt sprinter can't share one scale. Weekend Warrior shows you the ratings. Railbird hides them and lists each field A to Z, so it's your memory against the field.

<div style="display:flex;gap:8px;flex-wrap:wrap;justify-content:center">
<img src="/assets/images/posts/2026/14-0/phone-2-draft.jpg" alt="The 14–0 draft on a phone: spin a year, pick a horse for each race" style="flex:1 1 200px;max-width:260px;min-width:0;border-radius:6px">
<img src="/assets/images/posts/2026/14-0/share-card.jpg" alt="A finished 14–0 card: a 5–9 record with each race's horse, silks and finish" style="flex:1 1 200px;max-width:260px;min-width:0;border-radius:6px">
</div>
<p class="caption-text" style="text-align:center">The draft, and a finished card</p>

I messaged a few people about it. [Ed DeRosa](https://x.com/EJXD2) probably amplified it the most, and the handicapper [Andrew Champagne](https://x.com/AndrewChampagne), who heard about it from Ed, was the most enthusiastic player. He went 14–0, something I have never done. The next day, I made the game harder.

<blockquote style="margin:1.5em 0">
It's an addictive game fans of the sport's champions will love. … I believe I posted the first 14-0 mark in the game's history Thursday night.
<span style="display:block;margin-top:.5em;font-size:.85em">Andrew Champagne, in his <a href="https://andrewchampagne.com/2026/07/02/saratoga-race-course-analysis-selections-and-bankroll-for-saturday-july-4th/">Saratoga analysis for July 4th</a></span>
</blockquote>

In its first ten days, 14–0 was played 143 times, and 91% of those plays finished all 14 picks. Then the interest petered out.

### Making it a game

I'd always wanted to try generating a game. I'd seen developers on X build simple graphical games with AI - levelsio's [airplane game](https://404media.co/this-game-created-by-ai-vibe-coding-makes-50-000-a-month-yours-probably-wont) was the famous one - and I realized I could pair a simple game with 14–0. It would be easy to dip in and out of, but still backed by the depth of the data, and recognizable to a fan of the sport.

It was one of those one-shot experiences. I asked Claude for a horse racing game, and the very first version looked a lot like the game does today, except it was side-on. It was called Flatirons Park, and I saw immediately that there was something exciting I could build from it.

<div style="display:flex;gap:8px;flex-wrap:wrap;align-items:flex-start">
<img src="/assets/images/posts/2026/14-0/flatirons-park-v1.jpg" alt="Flatirons Park, the first version: a side-on view of eight horses on a dirt track, with a gas tank and Hold, Rate, Cruise, Press and Drive controls" style="flex:1 1 300px;min-width:0;border-radius:6px">
<img src="/assets/images/posts/2026/14-0/chase-today.jpg" alt="14–0 today: a chase camera behind the field at Keeneland, with the race board, clock and ride controls" style="flex:1 1 300px;min-width:0;border-radius:6px">
</div>
<p class="caption-text" style="text-align:center">Flatirons Park, 14 minutes after I asked for it, and the chase camera today</p>

### Watching a race

Watching a race is meant to feel like a TV broadcast. The camera cuts from the gate, to side-on down the backstretch, high and wide into the far turn, head-on down the stretch, and side-on at the wire. There's a race caller, fractions, and a running order with a morning line and the favorite marked. The race always lands exactly on the simulated result, margins included. Horses drift, bump and steady along the way, but none are ever hurt.

<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:8px">
<img src="/assets/images/posts/2026/14-0/cam-gate.jpg" alt="At the gate at Keeneland: the field loaded, the grandstand behind" style="width:100%;border-radius:6px">
<img src="/assets/images/posts/2026/14-0/cam-back.jpg" alt="Side-on down the backstretch with the running order and fractions" style="width:100%;border-radius:6px">
<img src="/assets/images/posts/2026/14-0/cam-turn.jpg" alt="High and wide as the field turns for home, with the race call" style="width:100%;border-radius:6px">
<img src="/assets/images/posts/2026/14-0/cam-stretch.jpg" alt="Head-on down the stretch as two horses lock up in the final sixteenth" style="width:100%;border-radius:6px">
</div>
<p class="caption-text" style="text-align:center">One race, four camera shots: a Classic at Keeneland</p>

If the top two are within half a length, the camera cuts to the finish line, the race slows down, and the PHOTO sign goes up. For the clip below, I set up Zenyatta and Blame to meet again at Churchill, with five other Classic horses from 2007 to 2012. It's a new race, not a replay. Blame still got there by a nose.

{% include video.html src="/assets/video/posts/2026/14-0-photo-finish-churchill.mp4" poster="/assets/images/posts/2026/14-0/photo-finish-poster.jpg" title="A photo finish in 14–0 at Churchill Downs: Zenyatta and Blame, slowed down at the wire, with the PHOTO sign" caption="Zenyatta and Blame, at Churchill again" controls=true %}

Each race runs at the track that hosted that year's Breeders' Cup. All 12 host tracks are modelled from their real dimensions, with a landmark or two: Churchill's twin spires, the San Gabriels behind Santa Anita, the ocean behind Del Mar.

<img src="/assets/images/posts/2026/14-0/tracks.jpg" alt="Six host tracks in 14–0: Del Mar, Santa Anita, Churchill Downs, Belmont Park, Gulfstream Park and Keeneland" style="width:100%;border-radius:6px">
<p class="caption-text" style="text-align:center">Del Mar, Santa Anita, Churchill Downs, Belmont Park, Gulfstream Park and Keeneland</p>

### Riding a race

Riding was the hard part. I tried to model the controls on [*Winning Ways: Raceriding Insights*](https://www.theirishfield.ie/retired-jockey-and-coach-mick-kennedy-passes-away-425136) by Mick Kennedy, an Irish jockey who went on to teach young riders, and it just didn't feel right, especially the rhythm, where you had to keep a tempo.

<figure style="max-width:340px;margin:1.5em auto"><img src="/assets/images/posts/2026/14-0/winning-ways-cover.jpg" alt="The cover of Winning Ways: Raceriding Insights by M. Kennedy" style="border-radius:4px"><figcaption class="caption-text">My copy</figcaption></figure>

Iterating on the controls was where I was most despondent. I was trying to do something more complicated than a mobile-first game should, and in testing I spent the whole race watching the controls instead of the horses. I started to wonder whether I could come up with anything different from what other racing games had tried.

What got it unstuck was simplifying: one control for balance, one for effort, and nothing you have to fiddle with too much. The commit history shows how long that took.

<figure style="margin:1.5em 0">
{% include 14-0-commits-chart.svg %}
</figure>

1. **Tue 20 Oct, 8:00am:** I asked for "a very simple top down but slightly at an angle horse racing game". Flatirons Park was up 14 minutes later. Five minutes after that, I wrote back: "The side-on view doesn't work, it needs to be from behind."
2. **12:30pm:** I decided to merge it with 14–0. The first commit landed at 12:49pm.
3. **6:33pm:** The first ride mode: one stick and a whip.
4. **Wed 21 Oct, 9:11am:** Ride mode rebuilt around *Winning Ways*, rhythm taps and all.
5. **3:32pm:** Two sticks, for balance and reins. Rhythm became "soft hands".
6. **6:44pm:** One stamina pool with a ghost line. Then the whip, three ways in 40 minutes: a swipe, a press, and finally its own button.
7. **10:22pm:** Copy approved and the device check passed. 88 commits, about 38 hours after the first prompt.

Before each ride, a paddock briefing gives you the plan, the pace to expect, and who to watch. In the race, the left stick is the reins and your line, the right stick is your balance, and the whip gets its own button for the stretch. A stamina ring shows what's left in the tank, with a ghost line marking the ideal spend for that horse and trip.

Your ride is measured against what a top jockey would get from the same horse. A great ride gains up to 1.6 rating points, a bad one costs you, and no ride turns the wrong horse into a winner. A report card grades it afterwards.

<div style="display:flex;gap:8px;flex-wrap:wrap;justify-content:center">
<img src="/assets/images/posts/2026/14-0/phone-6-paddock.jpg" alt="The paddock briefing before a ridden race: the plan, the pace, and the field with morning-line odds" style="flex:1 1 200px;max-width:260px;min-width:0;border-radius:6px">
<img src="/assets/images/posts/2026/14-0/phone-8-report.jpg" alt="The ride report after a race: a ride rating and the finishing order" style="flex:1 1 200px;max-width:260px;min-width:0;border-radius:6px">
</div>
<p class="caption-text" style="text-align:center">The paddock briefing, and the report card</p>

### The horses

As a developer, I actually know statistically what the best roster is. But there are horses from my history I've always loved: Banks Hill, Cigar, Arazi, High Chaparral. And [Dangerous Midge](https://en.wikipedia.org/wiki/Dangerous_Midge), who won the 2010 Turf at 5 to 1 after I'd tipped him to somebody in person. They thought I was a genius. I like seeing his name pop up.

Most of them run in their real colors, from more than 1,100 sets of silks redrawn from the race records.

### Try it

I released the game myself, with a [new X account](https://x.com/FourteenAndOApp) to go with it. So far it hasn't had the attention I was expecting, but it's early days.

Like most things I build, I built it for me first, then shared it to see who else liked it, and now I'm writing about it so people can see how I did it.

What I'd really love is for people to share it, especially people who aren't very technical but have watched most of the Breeders' Cup's 40-plus years. It's not hard to play, and it might bring back some fun memories of great horses. It's free, there are no ads, and I'm not asking anyone for anything. If you know someone who'd get a few minutes of fun out of it, send it their way.

<div style="display:flex;gap:8px;flex-wrap:wrap;justify-content:center">
<img src="/assets/images/posts/2026/14-0/lang-en.jpg" alt="The paddock briefing for High Chaparral in English" style="flex:1 1 160px;max-width:220px;min-width:0;border-radius:6px">
<img src="/assets/images/posts/2026/14-0/lang-ja.jpg" alt="The same paddock briefing in Japanese" style="flex:1 1 160px;max-width:220px;min-width:0;border-radius:6px">
<img src="/assets/images/posts/2026/14-0/lang-zh-HK.jpg" alt="The same paddock briefing in Traditional Chinese (Hong Kong)" style="flex:1 1 160px;max-width:220px;min-width:0;border-radius:6px">
</div>
<p class="caption-text" style="text-align:center">It plays in six languages, including Japanese and Hong Kong Chinese</p>

**[Draft your 14 at 14-0.net](https://14-0.net)**, or jump straight into a [Quick Race](https://14-0.net/race) on a random horse. Follow [@FourteenAndOApp](https://x.com/FourteenAndOApp) on X.
