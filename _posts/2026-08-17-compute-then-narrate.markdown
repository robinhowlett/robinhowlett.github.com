---
layout: post
title: "Compute, then narrate: putting your own data behind an LLM"
tags: ai llm cloudflare horseracing
---

When I added an AI partner to [redboarder](https://redboarder.com), [a place to practice the craft of handicapping]({% post_url 2026-08-17-introducing-redboarder %}), the obvious move was the one nearly everyone reaches for when they want to "chat with their data": point the model at the database, or embed everything and let retrieval feed it context, and let it answer. I did the opposite, and I've come to think the opposite is right far more often than the default suggests.

The AI in redboarder never touches the data directly. It can't query the database, it can't do the arithmetic, and it never sees a result it isn't supposed to. It's handed a finished, structured brief and asked only to *reason and talk* about it.

> The model is the narrator, not the analyst.

In this post I'll make the case for that split: why it's the right way to put *this kind* of data behind a model, and how it's the single decision that makes the AI convincing, cheap, correct, and impossible to trick into spoiling the game all at once. And, at the end, where it would be the wrong choice.

<!-- more -->

### The fork in the road

When you want to put your own data behind a language model, there are a few well-worn paths. **Retrieval-augmented generation (RAG)**: embed your data, search it by similarity at query time, and stuff the top hits into the prompt. **Tool or function calling**: hand the model live access to your database or API and let it fetch and compute. **Fine-tuning**: bake the data into the weights.

These are good tools. For *unstructured knowledge*, like documentation, support tickets, or a corpus of text you want searched and summarized, RAG in particular is often exactly right. The value there is the model synthesizing passages it retrieved, and approximate is fine.

redboarder's data is the opposite kind. It's **structured, quantitative, and correctness-critical**: performance ratings, win probabilities, pool sizes, payoffs, expected value. If I handed a model the raw rows and asked it to find the right ones and do the probability math, I'd be leaning on it for the two things language models are worst at, retrieval precision and arithmetic, and I'd get confident wrong numbers with no exactness and no control over what it saw. In a tool that's supposed to make you a *better* bettor, a hallucinated payoff isn't a glitch. It's a betrayal of the whole point.

So I don't do that. The hard, exact work happens first, in code, offline. The model only ever sees the finished product.

### The model is the narrator, not the analyst

The analytical engine behind redboarder is six repositories of deterministic code I've built over years: parsers, a race database, probability models, wagering math. It runs as an *offline build step* and turns raw data into a clean, structured brief for each race: running styles, a recency-weighted form read, pace scenarios, market comparison, bias signals, an opinion classification. Everything numeric is computed and verified in code.

The model's job starts where that ends. It's given the brief plus a tight persona, and its entire role is judgement and conversation: read the shape of the race, draw out what the user is seeing, push back, explain, structure an opinion into a bet. It never derives a number. It narrates the ones it's been handed.

That one boundary is the source of everything below. Convincing, cheap, correct, leak-proof: those aren't four features I built. They're four consequences of putting the model on the *narration* side of the line and the engine on the *analysis* side.

### Convincing

The first thing people assume makes an AI feature good is the model. It mostly isn't. It's what you feed it.

redboarder's partner sounds like a sharp horseplayer because it's *handed* a sharp horseplayer's homework: the pace projection is already done, the overlays already flagged, the trainer angle already surfaced. It isn't being clever on the fly; it's reasoning out loud over an expert-grade brief. A RAG pipeline would hand it a pile of rows and hope it assembled them into insight. Compute-then-narrate hands it the insight and asks it to *teach*.

![The AI partner's opening read: it reasons over a precomputed brief and suggests next actions, rather than deriving any of the numbers itself](/assets/images/posts/2026/ai-partner.png)

The persona does the rest. A short, strict prompt makes it behave like a partner rather than a tipster: it asks what you're seeing before it offers a view, states a structural opinion once and then builds what you ask for, and cites a specific number for every claim. None of that requires a frontier model, which matters a great deal for the next part.

### Cheap

Because the brief and the persona are *stable*, they cache. And prompt caching is the difference between this being a hobby I can afford and one I can't.

[Prompt caching](https://docs.claude.com/en/docs/build-with-claude/prompt-caching) is a prefix match: mark a stable chunk at the front of the prompt, and repeat requests that share it read it back at a fraction of the price instead of reprocessing it. The rule is that *any* byte change before the cache breakpoint invalidates everything after it, which is exactly why the volatile, per-race context goes *after* the stable system prompt, never woven into it:

``` js
const system = [
  { type: "text", text: SYSTEM_PROMPT, cache_control: { type: "ephemeral" } }, // ~13K tokens, cached
];
if (session_context) {
  system.push({ type: "text", text: "---\n\n" + session_context });            // volatile, uncached
}
```

The system prompt (the persona, the wagering doctrine, the data dictionary) runs about **13,000 tokens**, and it rides on every single turn. The multipliers are what make that survivable:

Operation | Cost (× base input)
---- | ----
Cache **write** (first turn, 5-min TTL) | 1.25×
Cache **read** (every turn after) | **0.1×**
Uncached | 1×

So after the first turn of a session, that 13K prompt bills at a tenth of its price, a **~90% saving on the biggest thing I send**, every turn. This is where compute-then-narrate pays off again: a RAG pipeline's context is *different every query* (you retrieved different chunks), so it can't cache the expensive part, and it adds a retrieval hop on top. A stable precomputed brief caches cleanly.

The model choice does the rest of the work. The live default is the cheapest current model, [Claude](https://claude.com/) Haiku ($1/$5 per million tokens in/out), because with the analysis already done the model only has to *talk*, and Haiku talks just fine. A turn lands at roughly **a cent**, which at my traffic is a couple of dollars a month. The expensive models are reserved for the one place quality compounds: precomputing each race's opening remarks, offline, once. That's a one-time build cost of a few dollars, not a per-conversation one. Worth guarding, that distinction, because conflating "spent once to build" with "spends every session" is how you talk yourself out of a project that's costing pennies.

> The inference turned out to be the *cheap* part of an AI app. The model you pick and the prefix you cache decide the bill; almost nothing else does.

### Correct, and hard to fool

The model is *forbidden* to do arithmetic. It doesn't compute what a bet costs, how many combinations it is, what it pays, or whether it won. A deterministic bet engine owns all of that and is the single source of truth. When a bet settles, the model is *told* the exact outcome and reflects on that; it never recomputes it.

This isn't caution for its own sake. Early on, the AI told a tester, with total conviction, that trifectas couldn't be played for 50¢. They can. That's the whole argument in one anecdote: a language model will state a wrong number without a flicker of doubt, so in any domain where the number has to be *right*, you don't ask it for the number. You compute it, and you let the model talk about it. The division of labour (engine reckons, model reasons) is legible, testable, and enforceable in a way "please be accurate" never is.

### Leak-proof where it matters

redboarder's core promise is that you commit to a bet before you're allowed to know how the race turned out. An AI partner threatens that promise in a way a static page doesn't: it could blurt the result, infer it, or be talked into it.

The defence isn't to *ask* the model nicely not to spoil things. It's that **the results are not in its context at all** until you commit. Each race is split into a "before" brief and an "after" file, and the model is only ever given the "before" half during handicapping. You can't leak what you were never handed.

That's the principle most people get backwards: **preventing leakage is an architecture problem, not a prompt problem.** If the sensitive data is in the context and you're relying on instructions to keep the model from repeating it, you've already lost. That's one clever user away from failure. Control what goes *into* the context and the guarantee holds by construction. (I still keep a belt-and-suspenders rule in the prompt forbidding the model from ever stating a result, but that's defence in depth, not the fence itself.)

### Knowing what it's doing

The last requirement is unglamorous: you have to be able to answer "what is this thing doing, and what is it costing me?" For a while, I couldn't.

A bar for the expensive model showed up on my billing dashboard and I froze: were real users somehow being routed to it? I had no way to tell, because I wasn't logging which model handled each request. The fix was a one-line structured log (model, and who, and how), and the mystery became a query. (It was my own overnight precompute batch. Of course it was.) The lesson is the oldest one in operations: you can't investigate what you didn't record, and the cost of turning on logging is trivial next to the cost of an unanswerable incident.

The other half of operability is a hard ceiling. Every model call routes through an [AI Gateway](https://developers.cloudflare.com/ai-gateway/) with a budget cap, the one control that *physically* stops spend if something runs away, plus a per-user rate limit as a pre-gateway guard. Cheap by design is good; cheap with a fuse is better.

### Did I do it the right way?

For this data: yes, and I'd defend it hard. Compute-then-narrate gives me correctness the model can't undermine, a bill dominated by a cache I control, and a leakage guarantee that holds by construction rather than by good behaviour. RAG or live queries would have handed me the opposite of all three.

The honest caveat is that this only works because my domain is *modelable in code*. I could put the model on the narration side of the line because I'd already spent years building the analysis side: the parsers, the database, the probability models. That's an enormous amount of up-front work, and RAG's whole appeal is that you skip it: point it at a pile of documents and have something useful by the afternoon.

So the rule isn't "RAG is bad." It's a question of what your data is:

- **Structured, quantitative, correctness matters, and you can build the engine** → compute the answers, hand the model a brief, let it narrate. redboarder is the poster child.
- **Unstructured knowledge, approximate is fine, and building an engine is absurd** → RAG, and don't overthink it.

Most "chat with your data" demos are the second kind wearing the first kind's clothes: a model doing retrieval and math it isn't good at, in a domain where being wrong is quiet and only shows up in production. If your numbers have to be right, move the numbers out of the model.

### The one decision

What I keep coming back to is how many separate-looking problems collapse into that single split. *How do I make it convincing?* Feed it computed insight. *How do I make it cheap?* A computed brief is a stable brief, and stable prefixes cache. *How do I keep it correct?* Don't let it near the math. *How do I stop it leaking the answer?* Don't put the answer in front of it.

Four questions, one answer: the model is the narrator, not the analyst. Decide that first, and most of the rest follows.
