---
layout: post
title: "14–0: a Breeders' Cup game you can ride"
comments: true
tags: horseracing 14-0 games
---

<!-- DRAFT, assembled from Robin's interview answers (dictation fixed). Notes for Robin are in HTML comments like this
     one; they don't render. Before publishing: permissions from Ed DeRosa and Andrew Champagne, confirm the
     Irish Field link for Mick Kennedy, check with your wife about her photo, then move this file to
     _posts/YYYY-MM-DD-14-0-a-breeders-cup-game-you-can-ride.markdown and run python3 tag_generator.py (new tags:
     14-0, games). -->

{% include video.html src="/assets/video/posts/2026/14-0-flightline-ride.mp4" poster="/assets/images/posts/2026/14-0/flightline-ride-poster.jpg" title="Riding Flightline down the stretch at Keeneland in 14–0, chase camera behind the field" caption="Riding Flightline at Keeneland" %}

<!-- Robin: one line in your words on what 14–0 is. e.g. "14–0 is a free game where you draft a horse for every
     Breeders' Cup race since 1984, then watch or ride the races yourself." -->
[14–0](https://14-0.net) is a free game where you draft a horse for every Breeders' Cup race since 1984, then watch or ride the races yourself.

<!-- more -->

### Churchill Downs, 2010

I had built a very simple and frankly unimpressive fantasy sports type game for the Breeders' Cup back in the year Blame beat Zenyatta. I was part of the Breeders' Cup Fan Advisory Council - they found a few of us by a social media way back then - and they had a draw to determine who would go to the track from the council. I have a feeling they rigged it in my favor. It actually turned out to be my honeymoon. I had gotten married a few days beforehand, we traveled to Churchill Downs and attended the races for the two days.

<div style="display:flex;gap:8px;flex-wrap:wrap;align-items:flex-start">
<img src="/assets/images/posts/2026/14-0/bc-2010-credential.jpg" alt="A Breeders' Cup World Championships 2010 Churchill Downs credential, November 5th-6th" style="flex:1 1 260px;min-width:0;border-radius:6px">
<img src="/assets/images/posts/2026/14-0/churchill-2010-honeymoon.jpg" alt="Robin and his wife on a balcony high above the track at Churchill Downs at night, the infield lit up behind them" style="flex:1 1 260px;min-width:0;border-radius:6px">
</div>
<p class="caption-text" style="text-align:center">Churchill Downs, November 5-6, 2010<!-- Robin: your caption if you'd like one, e.g. "Our honeymoon" --></p>

What was funny was the original version of that game relied on you picking the winner to stay alive in the competition, and I think it was race three or four on day one, a huge outsider won and everyone was knocked out. I stayed up all night and rewrote the game to be more points budget based. I launched the game that Saturday morning and it worked a lot better. The morning-line odds determined how costly a horse was to purchase from a limited bank balance, and so you had to trade off who to pick and who to go wide and spread in certain legs.

<div style="display:flex;gap:8px;flex-wrap:wrap;align-items:flex-start">
<img src="/assets/images/posts/2026/14-0/louisville-2010-hotel-rewrite.jpg" alt="Robin at a hotel-room desk in Louisville, typing on a laptop by the window" style="flex:1 1 260px;min-width:0;border-radius:6px">
<img src="/assets/images/posts/2026/14-0/churchill-2010-laptop.jpg" alt="Robin in a suit at the track, working on a laptop" style="flex:1 1 260px;min-width:0;border-radius:6px">
</div>
<p class="caption-text" style="text-align:center">Louisville, that weekend<!-- Robin: a caption in your words, e.g. which one is the all-nighter --></p>

What was hilarious was my father, who's not much of a racing fan, entered the competition in support of me, and I remember going into the last race he was either first or second and I was dreading him winning and me being accused of rigging it on his behalf. Luckily someone else came through and won.

Toby Keith performed a concert on either the Thursday or Friday night of that Churchill Downs Breeders' Cup, and it involved a lot of gyrating in tight jeans, surrounded by Ford pick-up trucks, since he was sponsored by them. I think I saw him in the box that I was invited to watch the races from the next day. I have nothing against the guy. He's an entertainer and that's part of the business.

And I remember Zenyatta prancing around the paddock, the huge interest in her, and then the collective groan when she was beaten.

### 14–0

I initially created a clone of the viral basketball app [82–0](https://aftermath.site/82-0-free-basketball-game-browser) for horse racing. I needed something in the sport that could act like a tournament, and the Breeders' Cup was what came to mind. I iterated on several variations of the roster-picking game and ended up with two: Weekend Warrior (originally called Claimer) and Railbird.

<div style="display:flex;gap:8px;flex-wrap:wrap;justify-content:center">
<img src="/assets/images/posts/2026/14-0/phone-2-draft.jpg" alt="The 14–0 draft on a phone: spin a year, pick a horse for each race" style="flex:1 1 200px;max-width:260px;min-width:0;border-radius:6px">
<img src="/assets/images/posts/2026/14-0/share-card.jpg" alt="A finished 14–0 card: a 5–9 record with each race's horse, silks and finish" style="flex:1 1 200px;max-width:260px;min-width:0;border-radius:6px">
</div>

I messaged a few people about 14–0, and [Ed DeRosa]() was the one who probably amplified it the most. The handicapper [Andrew Champagne]() was the most enthusiastic user, and in fact actually achieved a 14–0, something which I have never achieved. I think I actually increased the difficulty of the game once that happened.

<!-- Robin: with Andrew's OK, embed his 14–0 post from X here. Add both links above. -->

It had a little bit of interest, but it petered out.

### Making it a game

I had always wanted to experiment with generating a game. I had seen some developers on X build simple graphical games - there was an [airplane game](https://404media.co/this-game-created-by-ai-vibe-coding-makes-50-000-a-month-yours-probably-wont) created by [levelsio](https://x.com/levelsio) - and I realized I could join a simple game with 14–0 and make it very easy to go in and out of that game, while still relying on the depth of the content - something recognizable to a fan of the sport.

<!-- I wrote "Claude" where you said the model's name; put it back if you want it. -->
It was actually one of those one-shot experiences where I asked for a game, and the very first version Claude produced was very similar to the game it looks like now, albeit it was from the side on. <!-- Claude added the name; keep or cut: --> It was called Flatirons Park. But I saw immediately that there was something I could build here that was exciting.

{% include image-caption.html imageurl="/assets/images/posts/2026/14-0/flatirons-park-v1.jpg" title="Flatirons Park, the first version: a side-on view of eight horses on a dirt track, with a gas tank and Hold, Rate, Cruise, Press and Drive controls" caption="Flatirons Park, the first version, 14 minutes after I asked for it" %}

<!-- From the logs (UTC, 20-22 Oct 2026): the first prompt at 14:00; Flatirons Park up at 14:14; "the side-on view
     doesn't work, it needs to be from behind" at 14:19; the idea to merge it with 14–0 at 18:30; launch-ready about
     38 hours after the first prompt, across 88 commits. Use what helps. -->

I tried to model the controller inputs after reading [*Winning Ways: Raceriding Insights*](https://www.theirishfield.ie/retired-jockey-and-coach-mick-kennedy-passes-away-425136) by Mick Kennedy, an Irish jockey who wrote it in the early 2000s, and it just didn't feel right, especially things regarding rhythm, where you had to keep a tempo. So really the point where I was most despondent was iterating on the controls, trying to do something more complicated than a mobile-first game should be doing. In my testing, I was spending all of the race just looking at the controls rather than the horses, and I questioned if I could invent something different than other people had tried with racing games before.

<figure style="max-width:340px;margin:1.5em auto"><img src="/assets/images/posts/2026/14-0/winning-ways-cover.jpg" alt="The cover of Winning Ways: Raceriding Insights by M. Kennedy" style="border-radius:4px"><figcaption class="caption-text">My copy</figcaption></figure>

<!-- From the commits: the controls went through six versions in about 28 hours - one stick and a whip; rhythm taps
     from the book; two sticks ("rhythm is soft hands"); a stamina pool with a ghost line; then the whip three ways in
     40 minutes (a swipe, a press, its own button). -->

The controls got unstuck by just simplifying it, so that you have both a balance control and an effort control and you didn't have to be fiddling with them too much.

<div style="display:flex;gap:8px;flex-wrap:wrap;justify-content:center">
<img src="/assets/images/posts/2026/14-0/phone-6-paddock.jpg" alt="The paddock briefing before a ridden race: the plan, the pace, and the field with morning-line odds" style="flex:1 1 200px;max-width:260px;min-width:0;border-radius:6px">
<img src="/assets/images/posts/2026/14-0/phone-8-report.jpg" alt="The ride report after a race: a ride rating and the finishing order" style="flex:1 1 200px;max-width:260px;min-width:0;border-radius:6px">
</div>

### The horses

My best roster? Well, as a developer I actually know statistically what is the best roster, but there are some horses from my history that I've always loved: Banks Hill, Cigar, Arazi, High Chaparral. And I remember tipping the 2010 Breeders' Cup Turf winner, Dangerous Midge, who won at 5 to 1, to somebody in person, and they thought I was a genius. I like seeing that horse's name pop up.

<!-- I'd remembered 10 to 1; Wikipedia says 5/1 (https://en.wikipedia.org/wiki/Dangerous_Midge). -->

### Try it

For the video game version, I just released it myself and created a new X account for the game. So far I haven't got as much attention as I was initially expecting, but it's early days and we'll see what happens.

Like most of the things I build, I primarily build it for me, then I share it to see who else likes it, and then I write about it so people can learn how I did it.

Really, I'd love for people to share it. I think there's a lot of maybe less technical folks, especially those who have seen most if not all of the over 40 years of the Breeders' Cup. I'd love for them to be able to try it, because it's not that difficult an experience in my opinion, and it might bring back some fun memories of great horses over the years. It's free, it doesn't have ads, I'm not asking anyone for anything. So yeah, if I could encourage people to try it out with an open mind, and to share it with those that they think might get at least a few minutes of entertainment out of it, that would be great.

<!-- "near 40 years" became "over 40 years": the game covers 1984-2025. -->

Play it at [14-0.net](https://14-0.net), and follow [@FourteenAndOApp](https://x.com/FourteenAndOApp) on X.
