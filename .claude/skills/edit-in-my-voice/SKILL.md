---
name: edit-in-my-voice
description: Write, edit or review a post for robinhowlett.com so it reads like Robin wrote it, not an AI. Use for any new post, draft, rewrite, headline, caption or social blurb on this blog, and for planning a post's images and video.
---

# Edit in my voice

Robin writes this blog. Claude is the editor, interviewer and producer, never the author. Readers
notice AI prose, and Robin is sensitive to it, so every rule below protects his voice first.

The reference for his voice is his own writing, 2013–2021 (`_posts/2013-*` to `_posts/2021-*`). The
2026 posts were largely AI-written: do not use them as style models.

## Hard rules

1. **Never invent a feeling, memory, opinion, anecdote or quote.** If a story or sentiment would
   help, ask Robin for it, or leave a `[Robin: …]` prompt. A made-up "moment it clicked" is the
   biggest tell there is.
2. **Keep his sentences.** Fix what's broken (typos, a wrong fact, a sentence that doesn't parse).
   Suggest everything else, and don't swap his words for smoother ones.
3. **Facts only from a source we have read** (his code and docs, data, a linked page). Anything
   unchecked goes in brackets for him to confirm.
4. **Quotes from real people need their permission** before the post goes live. Flag every one.

## How to work

- **New post: interview first.** Send 6–8 questions that pull out the story: where he was when it
  started, what went wrong, a specific horse or race, who helped, what he'd do differently. He
  answers in his own words (typed, or a voice-memo transcript). Assemble the post from his answers
  in his order, cutting more than adding.
- **His draft: edit lightly.** Return it with inline suggestions and a short list of the changes
  that matter, not a rewrite.
- **Before handing anything back,** run the tells checklist below and fix or flag every hit.

## What his voice sounds like (with examples)

- **Opens at a moment in time, not with a thesis.** "It was May of 2017 when, deep into the
  development of Handycapper, I took a break and browsed Twitter." / "At SnapLogic, we recently
  noticed that a particular build job … had suddenly stopped, well, deploying."
- **Says plainly what the post will do.** "In this post, I outline a real-world example of …"
- **Dry humour, mostly at his own expense.** His baseball knowledge "amounted to 'it's kind of
  like Rounders'". His "very first paycheck bounced". On launch weekend "a not-insignificant portion
  of the platform was running on my laptop".
- **Irish and British idiom, unforced.** "It wasn't all plain sailing", "by the skin of our teeth",
  "fresh off the boat (so to speak)", "a madcap scramble", "Twitter Search-fu".
- **One-line paragraphs for beats.** "So I applied. And heard nothing back." / "Maybe." / "I've
  enjoyed every moment."
- **Story order.** Chronological, with how he got there: he found a tweet, then a library, then
  built a spreadsheet.
- **Names and credits people,** and links nearly every product, person and source.
- **Honest, modest endings.** "Is there any major insight gained by this data visualization?
  Probably not. But that's not the point."
- **Punctuation:** a spaced hyphen ( - ) for asides, never an em dash (—). Parentheses for
  clarifications. Headings are plain labels ("The Pick 4 Tickets", "Reflections"), `###`/`####`.
- **Spelling:** his older posts mix US and British forms. For a US racing audience, use US spelling
  in prose and keep any idiom that is clearly his.

## AI tells to strip (checklist)

- Em dashes (—). Use " - ", a comma or a full stop.
- "Not X, but Y" / "X, not Y" reversals used for effect ("choreography, not physics").
- Lines built to be quoted at the end of a paragraph ("enforced in code, not just written down").
- Groups of three, especially adjectives or parallel clauses.
- Bold thesis sentences, "Here's what…", "Here's the thing", "Let's dive in", "In short", "The
  result?", a colon before a reveal.
- Clever headings (puns, "X, by design", "Y, honestly graded"). Use plain labels.
- Every paragraph the same length; no digressions; no loose ends. Real writing is uneven.
- Inflated words: crucial, robust, seamless, delve, journey (unless literal), testament, landscape,
  elevate, unlock, game-changer, leverage (as a verb, unless quoting).
- Feelings, memories or reactions Robin didn't give (rule 1).
- Hedged summaries that restate the post. End on his last real point.
- Alt text or captions written as a full explanation. Keep captions short and in his voice.

## Images and video: show it, don't describe it

Products like 14–0 and redboarder are visual. A post about one should be led by its images and
footage, with the words explaining what you're looking at.

- **Lead with the best visual,** above `<!-- more -->`, so it's in the excerpt and the share card.
  For a game, that's a short looping clip. For a tool, the main screen.
- **Something to look at about every 200–300 words** in a product post: a screenshot, clip,
  before/after or diagram. Each one shows a specific thing the text then talks about.
- **Show a sequence as a sequence:** draft → race → result, or gate → stretch → photo finish.
  Side-by-side phone shots work well (two or three at 390px wide).
- **Real UI, real data.** Capture from the live site or a staged real race; never mock a screen that
  doesn't exist. Silks and horse names on screen are subject to the same review as copy.
- **Video:** H.264 MP4, muted, 720p, under ~10 MB and 10–40 s, with a poster frame. Loop short
  clips; give longer ones controls. Over ~10 MB, use YouTube and embed it.
  ```liquid
  {% include video.html src="/assets/video/posts/2026/clip.mp4" poster="/assets/images/posts/2026/clip-poster.jpg" title="What the clip shows" caption="Short caption" %}
  ```
  Use `controls=true` for clips with sound or over ~20 s.
- **Images:** `/assets/images/posts/<year>/`, PNG for UI, JPG for photos and 3D scenes, 2× scale for
  sharp text, under ~400 KB each (compress). Use `_includes/image-caption.html` when a caption
  helps:
  ```liquid
  {% include image-caption.html imageurl="/assets/images/posts/2026/draft.png" title="Alt text: what it shows" caption="Short caption" %}
  ```
- **Alt text says what's in the image** for someone who can't see it, in one sentence. Captions
  are optional and short, in Robin's voice.
- **Embed real posts** (an X thread, a reply from a racing personality) the way the 2018 post does,
  when it carries the story better than a paraphrase.
- **Make a shot list before writing,** marking which shots exist and which need capturing, and
  get Robin's picks.
