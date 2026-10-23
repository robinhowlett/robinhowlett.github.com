---
layout: post
title: "14–0: a Breeders' Cup game you can ride"
comments: true
tags: horseracing 14-0 games
---

<!-- DRAFT. Robin's sections are his interview answers with dictation fixed. Sections marked "Claude-drafted" are plain
     descriptions of the game for Robin to rewrite in his own words or cut. Notes in HTML comments don't render.
     Before publishing: OK from Ed DeRosa and Andrew Champagne to be named and quoted (and to embed Andrew's post);
     check with your wife about her photo; then move this file to _posts/YYYY-MM-DD-14-0-a-breeders-cup-game-you-can-ride.markdown
     and run python3 tag_generator.py (new tags: 14-0, games). -->

{% include video.html src="/assets/video/posts/2026/14-0-flightline-ride.mp4" poster="/assets/images/posts/2026/14-0/flightline-ride-poster.jpg" title="Riding Flightline down the stretch at Keeneland in 14–0, chase camera behind the field" caption="Riding Flightline at Keeneland" %}

<!-- Claude-drafted -->
The 2026 Breeders' Cup is at Keeneland on [October 30 and 31](https://lex18.com/news/covering-kentucky/breeders-cup-world-championship-returns-to-keeneland-in-2026). [14–0](https://14-0.net) is a free game where you draft a horse for each of the 14 Breeders' Cup races from every running since 1984, then sim the card, watch each race, or ride it yourself, on the track where that year's race was run. In this post, I go through where it came from, how it works, and how it was built.

<!-- more -->

### Churchill Downs, 2010

I had built a very simple and frankly unimpressive fantasy sports type game for the Breeders' Cup back in the year [Blame beat Zenyatta](https://en.wikipedia.org/wiki/2010_Breeders%27_Cup_Classic). I was part of the Breeders' Cup Fan Advisory Council - they found a few of us by a social media way back then - and they had a draw to determine who would go to the track from the council. I have a feeling they rigged it in my favor. It actually turned out to be my honeymoon. I had gotten married a few days beforehand, we traveled to Churchill Downs and attended the races for the two days.

<div style="display:flex;gap:8px;flex-wrap:wrap;align-items:flex-start">
<img src="/assets/images/posts/2026/14-0/bc-2010-credential.jpg" alt="A Breeders' Cup World Championships 2010 Churchill Downs credential, November 5th-6th" style="flex:1 1 260px;min-width:0;border-radius:6px">
<img src="/assets/images/posts/2026/14-0/churchill-2010-honeymoon.jpg" alt="Robin and his wife on a balcony high above the track at Churchill Downs at night, the infield lit up behind them" style="flex:1 1 260px;min-width:0;border-radius:6px">
</div>
<p class="caption-text" style="text-align:center">Churchill Downs, November 5-6, 2010<!-- Robin: your caption if you'd like one --></p>

What was funny was the original version of that game relied on you picking the winner to stay alive in the competition, and I think it was race three or four on day one, a huge outsider won and everyone was knocked out. I stayed up all night and rewrote the game to be more points budget based. I launched the game that Saturday morning and it worked a lot better. The morning-line odds determined how costly a horse was to purchase from a limited bank balance, and so you had to trade off who to pick and who to go wide and spread in certain legs.

<div style="display:flex;gap:8px;flex-wrap:wrap;align-items:flex-start">
<img src="/assets/images/posts/2026/14-0/louisville-2010-hotel-rewrite.jpg" alt="Robin at a hotel-room desk in Louisville, typing on a laptop by the window" style="flex:1 1 260px;min-width:0;border-radius:6px">
<img src="/assets/images/posts/2026/14-0/churchill-2010-laptop.jpg" alt="Robin in a suit at the track, working on a laptop" style="flex:1 1 260px;min-width:0;border-radius:6px">
</div>
<p class="caption-text" style="text-align:center">Louisville, that weekend<!-- Robin: a caption in your words, e.g. which one is the all-nighter --></p>

What was hilarious was my father, who's not much of a racing fan, entered the competition in support of me, and I remember going into the last race he was either first or second and I was dreading him winning and me being accused of rigging it on his behalf. Luckily someone else came through and won.

Toby Keith performed a concert on either the Thursday or Friday night of that Churchill Downs Breeders' Cup, and it involved a lot of gyrating in tight jeans, surrounded by Ford pick-up trucks, since he was sponsored by them. I think I saw him in the box that I was invited to watch the races from the next day. I have nothing against the guy. He's an entertainer and that's part of the business.

And I remember Zenyatta prancing around the paddock, the huge interest in her, and then the collective groan when she was beaten.

(I mentioned that [small social app for the 2010 Breeders' Cup]({% post_url 2015-08-06-farewell-sportslabs %}) in an earlier post.)<!-- Claude-drafted; rewrite or cut -->

### From 82–0 to 14–0

I initially created a clone of the viral basketball app [82–0](https://aftermath.site/82-0-free-basketball-game-browser) for horse racing. I needed something in the sport that could act like a tournament, and the Breeders' Cup was what came to mind. I iterated on several variations of the roster-picking game and ended up with two: Weekend Warrior (originally called Claimer) and Railbird.

<!-- Claude-drafted: how the draft works -->
Each of the 14 races starts with a spin that lands on a year. You pick one horse from that year's field, and you can't use the same year twice. Once all 14 are in, the card runs against rivals drawn from across the eras. The archive covers 422 Breeders' Cup races from 1984 to 2025: 1,266 starts by 1,097 different horses. Every horse is rated against its own field on how good it really was, not on one day's number, because a turf router and a dirt sprinter can't share a scale. Weekend Warrior shows you the ratings. Railbird hides them and lists each field A to Z, so it's your memory against the field.

<div style="display:flex;gap:8px;flex-wrap:wrap;justify-content:center">
<img src="/assets/images/posts/2026/14-0/phone-2-draft.jpg" alt="The 14–0 draft on a phone: spin a year, pick a horse for each race" style="flex:1 1 200px;max-width:260px;min-width:0;border-radius:6px">
<img src="/assets/images/posts/2026/14-0/share-card.jpg" alt="A finished 14–0 card: a 5–9 record with each race's horse, silks and finish" style="flex:1 1 200px;max-width:260px;min-width:0;border-radius:6px">
</div>
<p class="caption-text" style="text-align:center">The draft, and a finished card</p>

I messaged a few people about 14–0, and [Ed DeRosa](https://x.com/EJXD2) was the one who probably amplified it the most. The handicapper [Andrew Champagne](https://x.com/AndrewChampagne) was the most enthusiastic user, and in fact actually achieved a 14–0, something which I have never achieved. I think I actually increased the difficulty of the game once that happened.

<!-- Quotes from Andrew's post, verified on the page. With his OK, embed his X post instead of or beside this:
     https://x.com/AndrewChampagne/status/2073138333052744066 -->
<blockquote style="margin:1.5em 0">
It's an addictive game fans of the sport's champions will love. … I believe I posted the first 14-0 mark in the game's history Thursday night.
<span style="display:block;margin-top:.5em;font-size:.85em">Andrew Champagne, in his <a href="https://andrewchampagne.com/2026/07/02/saratoga-race-course-analysis-selections-and-bankroll-for-saturday-july-4th/">Saratoga analysis for July 4th</a></span>
</blockquote>

<!-- Claude-drafted, from the repo's traction notes (STATE.md, 2026-07-10) -->
In its first ten days there were 143 plays, and 91% of them finished all 14 picks.

It had a little bit of interest, but it petered out.

### Making it a game

I had always wanted to experiment with generating a game. I had seen some developers on X build simple graphical games - there was an [airplane game](https://404media.co/this-game-created-by-ai-vibe-coding-makes-50-000-a-month-yours-probably-wont) created by [levelsio](https://x.com/levelsio) - and I realized I could join a simple game with 14–0 and make it very easy to go in and out of that game, while still relying on the depth of the content - something recognizable to a fan of the sport.

<!-- I wrote "Claude" where you said the model's name; put it back if you want it. -->
It was actually one of those one-shot experiences where I asked for a game, and the very first version Claude produced was very similar to the game it looks like now, albeit it was from the side on. But I saw immediately that there was something I could build here that was exciting.

<div style="display:flex;gap:8px;flex-wrap:wrap;align-items:flex-start">
<img src="/assets/images/posts/2026/14-0/flatirons-park-v1.jpg" alt="Flatirons Park, the first version: a side-on view of eight horses on a dirt track, with a gas tank and Hold, Rate, Cruise, Press and Drive controls" style="flex:1 1 300px;min-width:0;border-radius:6px">
<img src="/assets/images/posts/2026/14-0/chase-today.jpg" alt="14–0 today: a chase camera behind the field at Keeneland, with the race board, clock and ride controls" style="flex:1 1 300px;min-width:0;border-radius:6px">
</div>
<p class="caption-text" style="text-align:center">Flatirons Park, the first version, 14 minutes after I asked for it, and the chase camera today</p>

### Watching a race

<!-- Claude-drafted: what watch mode does -->
Watching a race works like a TV broadcast. A camera director cuts between a wide shot at the gate, side-on down the backstretch, high and wide into the far turn, head-on down the stretch and side-on at the wire. A race caller calls the break, the turns and the finish, the fractions go up in one corner, and the running order sits in another, with a morning line and the favorite marked. The race you watch always lands exactly on the simulated result, margins and all. Horses drift, bump and steady along the way, but nobody is ever hurt.

<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:8px">
<img src="/assets/images/posts/2026/14-0/cam-gate.jpg" alt="At the gate at Keeneland: the field loaded, the grandstand behind" style="width:100%;border-radius:6px">
<img src="/assets/images/posts/2026/14-0/cam-back.jpg" alt="Side-on down the backstretch with the running order and fractions" style="width:100%;border-radius:6px">
<img src="/assets/images/posts/2026/14-0/cam-turn.jpg" alt="High and wide as the field turns for home, with the race call" style="width:100%;border-radius:6px">
<img src="/assets/images/posts/2026/14-0/cam-stretch.jpg" alt="Head-on down the stretch as two horses lock up in the final sixteenth" style="width:100%;border-radius:6px">
</div>
<p class="caption-text" style="text-align:center">One race, four camera shots: the 2022 Classic field at Keeneland</p>

When the top two finish within half a length, the camera cuts to the finish line, the race slows down and the PHOTO sign goes up. This one is Zenyatta and Blame again, at Churchill, in a Classic staged with them and five other Classic horses from 2007 to 2012, set up to finish close. It's a new race, not a replay of the real one, and Blame got there by a nose again.<!-- Claude staged this race for the clip (the two rated level, so it would be a photo); say so or cut -->

{% include video.html src="/assets/video/posts/2026/14-0-photo-finish-churchill.mp4" poster="/assets/images/posts/2026/14-0/photo-finish-poster.jpg" title="A photo finish in 14–0 at Churchill Downs: Zenyatta and Blame, slowed down at the wire, with the PHOTO sign" caption="Zenyatta and Blame, at Churchill again" controls=true %}

Every race is run at the track where that year's Breeders' Cup was held, and all 12 host tracks are modelled from their real dimensions, with a landmark or two: the twin spires at Churchill, the San Gabriels behind Santa Anita, the ocean behind Del Mar.

<img src="/assets/images/posts/2026/14-0/tracks.jpg" alt="Six host tracks in 14–0: Del Mar, Santa Anita, Churchill Downs, Belmont Park, Gulfstream Park and Keeneland" style="width:100%;border-radius:6px">
<p class="caption-text" style="text-align:center">Del Mar, Santa Anita, Churchill Downs, Belmont Park, Gulfstream Park and Keeneland</p>

### Riding a race

I tried to model the controller inputs after reading [*Winning Ways: Raceriding Insights*](https://www.theirishfield.ie/retired-jockey-and-coach-mick-kennedy-passes-away-425136) by Mick Kennedy, an Irish jockey who wrote it in the early 2000s, and it just didn't feel right, especially things regarding rhythm, where you had to keep a tempo. So really the point where I was most despondent was iterating on the controls, trying to do something more complicated than a mobile-first game should be doing. In my testing, I was spending all of the race just looking at the controls rather than the horses, and I questioned if I could invent something different than other people had tried with racing games before.

<figure style="max-width:340px;margin:1.5em auto"><img src="/assets/images/posts/2026/14-0/winning-ways-cover.jpg" alt="The cover of Winning Ways: Raceriding Insights by M. Kennedy" style="border-radius:4px"><figcaption class="caption-text">My copy</figcaption></figure>

The controls got unstuck by just simplifying it, so that you have both a balance control and an effort control and you didn't have to be fiddling with them too much.

<!-- Claude: the chart and the timeline come straight from the commit history and the session log. -->
<figure style="margin:1.5em 0">
{% include 14-0-commits-chart.svg %}
</figure>

1. **Tue 20 Oct, 8:00am:** I asked for "a very simple top down but slightly at an angle horse racing game". Flatirons Park was up 14 minutes later. Five minutes after that: "The side-on view doesn't work, it needs to be from behind."
2. **12:30pm:** the idea to merge it with 14–0. The first watch-mode commit landed at 12:49pm.
3. **6:33pm:** the first ride mode, one stick and a whip.
4. **Wed 21 Oct, 9:11am:** ride mode rebuilt around *Winning Ways*, rhythm taps and all.
5. **3:32pm:** two sticks, balance and reins. Rhythm became "soft hands".
6. **6:44pm:** one stamina pool with a ghost line, then the whip three ways in 40 minutes: a swipe, a press, then its own button.
7. **10:22pm:** copy approved and the device check passed. That's 88 commits, about 38 hours after the first prompt.

<!-- Claude-drafted: what riding is like now -->
Before each ride, a paddock briefing gives you the plan for your horse, the pace to expect and who to watch. In the race, the left stick is the reins and your line, the right stick keeps you balanced, and the whip has its own button for the stretch. A stamina ring shows the tank, with a ghost line for the ideal spend on that horse and trip. Your horse runs against what a top jockey would get from it, so a great ride can gain up to 1.6 rating points and a bad one can cost you, but it can't turn the wrong horse into a winner. After the race, a report card grades the ride.

<div style="display:flex;gap:8px;flex-wrap:wrap;justify-content:center">
<img src="/assets/images/posts/2026/14-0/phone-6-paddock.jpg" alt="The paddock briefing before a ridden race: the plan, the pace, and the field with morning-line odds" style="flex:1 1 200px;max-width:260px;min-width:0;border-radius:6px">
<img src="/assets/images/posts/2026/14-0/phone-8-report.jpg" alt="The ride report after a race: a ride rating and the finishing order" style="flex:1 1 200px;max-width:260px;min-width:0;border-radius:6px">
</div>
<p class="caption-text" style="text-align:center">The paddock briefing, and the report card after</p>

### The horses

My best roster? Well, as a developer I actually know statistically what is the best roster, but there are some horses from my history that I've always loved: Banks Hill, Cigar, Arazi, High Chaparral. And I remember tipping the 2010 Breeders' Cup Turf winner, [Dangerous Midge](https://en.wikipedia.org/wiki/Dangerous_Midge), who won at 5 to 1, to somebody in person, and they thought I was a genius. I like seeing that horse's name pop up.

<!-- I'd remembered 10 to 1; Wikipedia says 5/1. -->

<!-- Claude-drafted -->
Most of them run in their real colors: more than 1,100 sets of silks, redrawn from the race records.

### Try it

For the video game version, I just released it myself and created a [new X account](https://x.com/FourteenAndOApp) for the game. So far I haven't got as much attention as I was initially expecting, but it's early days and we'll see what happens.

Like most of the things I build, I primarily build it for me, then I share it to see who else likes it, and then I write about it so people can learn how I did it.

Really, I'd love for people to share it. I think there's a lot of maybe less technical folks, especially those who have seen most if not all of the over 40 years of the Breeders' Cup. I'd love for them to be able to try it, because it's not that difficult an experience in my opinion, and it might bring back some fun memories of great horses over the years. It's free, it doesn't have ads, I'm not asking anyone for anything. So yeah, if I could encourage people to try it out with an open mind, and to share it with those that they think might get at least a few minutes of entertainment out of it, that would be great.

<div style="display:flex;gap:8px;flex-wrap:wrap;justify-content:center">
<img src="/assets/images/posts/2026/14-0/lang-en.jpg" alt="The paddock briefing for High Chaparral in English" style="flex:1 1 160px;max-width:220px;min-width:0;border-radius:6px">
<img src="/assets/images/posts/2026/14-0/lang-ja.jpg" alt="The same paddock briefing in Japanese" style="flex:1 1 160px;max-width:220px;min-width:0;border-radius:6px">
<img src="/assets/images/posts/2026/14-0/lang-zh-HK.jpg" alt="The same paddock briefing in Traditional Chinese (Hong Kong)" style="flex:1 1 160px;max-width:220px;min-width:0;border-radius:6px">
</div>
<p class="caption-text" style="text-align:center">It also plays in Spanish, French, German, Japanese and Hong Kong Chinese</p>

**[Draft your 14 at 14-0.net](https://14-0.net)**, or jump straight into a [Quick Race](https://14-0.net/race) on a random horse. Follow [@FourteenAndOApp](https://x.com/FourteenAndOApp) on X.

<!-- "near 40 years" became "over 40 years": the game covers 1984-2025. -->
