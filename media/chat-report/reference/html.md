# Building the page

You write **one file**: `content.html` — just the sections, no `<html>`, no
`<head>`, no styles, no scripts. The builder wraps it in the shell, which
supplies the theme, the tab bar, the charts, tooltips, the light/dark toggle and
the print stylesheet.

```
python3 .../scripts/build_report.py \
  --content content.html \
  --stats stats.json \
  --out "Book Club report.html" \
  --title "Somebody Call First" \
  --standfirst "Two years, two cities, and the one trip nobody booked."
```

`--title` is the report's name — three or four words, taken from the report's
own argument, never "Chat Analysis". `--standfirst` is one sentence under it.

## Tabs

Every section is wrapped in a tab. Tabs appear in the order they first show up.

```html
<section data-tab="read" data-label="The Read" data-icon="EMOJI">
  …
</section>
```

Use these four, in this order:

| `data-tab` | Label | What goes in it |
|---|---|---|
| `read` | The Read | Opening, what this actually is, power, the loop, what's unsaid, what's missing, the moment it turned, where it's heading, what it gave you |
| `cast` | The Cast | One `.person` block per participant |
| `numbers` | The Numbers | The charts, each with a paragraph of reading underneath |
| `receipts` | Receipts | Quotes, the dictionary, the awards, the eras |

Split a tab into several `<section>` blocks with the same `data-tab` if that's
easier — they'll render as one. Every `<h2>` inside a tab automatically becomes
a jump chip at the top, so keep headings short.

Start each `<h2>` with one emoji wrapped in `<span class="e">` (`EMOJI` in
these examples stands for a single emoji character, as does `data-icon` above):

```html
<h2><span class="e">EMOJI</span> Two friends, one calendar</h2>
```

## Components

**Prose** is plain `<p>`. First paragraph of a section can be `<p class="lede">`.

**The blunt line** — the sentence in a section that has to land:

```html
<p class="verdict">You did the most talking and the least asking.</p>
```

**A quoted message.** `data-who` colours it to match that person everywhere else
in the report; use their name exactly as it appears in the stats.

```html
<div class="msg" data-who="Sam">
  <span class="who">Sam</span>
  <p>honestly i dont think you were listening</p>
  <time>9 May 2023, 23:48</time>
</div>
```

**An exchange** — two or more `.msg` blocks inside `<div class="exchange">`.
Use this two or three times in the whole report, where the back-and-forth
itself is the evidence.

**A pull quote**, for the single best line in the chat:

```html
<blockquote class="pull">this is me being supportive from a very safe distance
  <cite>Alex, 6 June 2022</cite></blockquote>
```

**An admission** — what you can't see from here:

```html
<p class="note"><b>What I can't tell:</b> whether he ever said it out loud.
  Nothing in here suggests he did.</p>
```

**The stinger** — an optional blur-until-tapped line, for the one sentence per
person that will hurt. Use it at most three times in a report, or it turns into
a gimmick:

```html
<p>And the thing you keep circling: <span class="sting">he has never once
  asked how the new job is going.</span></p>
```

**The revision block** — only on a report that's been updated, and only at the
very top of The Read. What you got wrong goes before anything else:

```html
<div class="revision">
  <b>What changed in this version</b>
  <p>The group chat says the October silence wasn't her withdrawing.</p>
  <ul><li>I said she went quiet for no stated reason. There was one, and she told two other people.</li></ul>
</div>
```

Pair it with `--updated "Updated 2 March — now includes the group chat."`
on the builder, which prints one line under the standfirst.

**A person block** (the Cast tab). `data-who` sets the colour and the initial:

```html
<article class="person" data-who="Alex">
  <div class="avatar"></div>
  <h2>Alex: the one who narrates so nobody asks</h2>
  <p class="role">54% of the messages, and the fewest questions.</p>
  <div class="miniStats">
    <span><b>2,418</b> messages</span>
    <span><b>3 min</b> to reply</span>
    <span><b>68%</b> of openings</span>
    <span><b>112</b> unanswered runs</span>
  </div>
  <p>…</p>
</article>
```

Pull the mini-stat numbers from the stats file. Four or five per person, and
they should be the ones that set up what you're about to say.

**The loop** — an ordered chain, auto-numbered:

```html
<ol class="chain">
  <li>Alex gives too much.</li>
  <li>The others feel crowded.</li>
  <li>They pull back gently.</li>
  <li>Alex reads it as abandonment.</li>
  <li>Alex gives more.</li>
</ol>
```

**Cards**, for short parallel points — what each person was given, three
unspoken things:

```html
<div class="cards">
  <div class="card"><h4>Sam</h4><p>You learned you could be relied on without being asked how you were.</p></div>
</div>
```

**The dictionary:** `<dl class="dict"><dt>Yikesville</dt><dd>…</dd></dl>`

**The awards:** `<ul class="awards"><li><b>Left on read</b><span>…</span></li></ul>`

**The eras:**
`<div class="era"><time>Mar 2022 – Aug 2022</time><div><b>The good year</b><p>…</p></div></div>`

## Charts

Drop a placeholder. The shell fills it from `stats.json` — you don't write any
numbers into it, and you can't get them wrong.

```html
<figure class="chart" data-chart="share"><figcaption></figcaption></figure>
```

| `data-chart` | Shows |
|---|---|
| `share` | Message share per person |
| `timeline` | Month by month, stacked by person |
| `speed` | How long each person takes to reply |
| `opens` | Who starts conversations, who has the last word |
| `hours` | Hour-of-day heatmap per person |
| `silences` | The longest gaps, coloured by who broke them |
| `runs` | Unanswered runs of three or more |
| `questions` | Who asks questions |
| `markers` | Sorry / love you / miss you / it's fine, per person |
| `pairs` | Who answers whom (groups only) |
| `sources` | Who spoke in which export (combined reports only) |
| `sourceTimeline` | Which thread was alive when (combined reports only) |

Every chart carries its own title, hover tooltips and a table view. Leave
`<figcaption>` empty for the default title, or write your own to point it at
your argument: `<figcaption>Ana starts nine conversations in ten</figcaption>`.

**A chart on its own says nothing.** Every one gets a paragraph underneath
saying what it means. That paragraph is the section; the chart is the evidence.

## Rules for the page

- Nothing in `content.html` but sections — no `<style>`, no `<script>`, no
  inline `style=` attributes. If you need a look that isn't here, the shell is
  wrong and should be edited, not worked around.
- Escape `&`, `<` and `>` inside quoted messages. Keep emoji as they are.
- Don't restate a number in prose and then chart it directly beneath. Pick one.
- The Numbers tab is the only place charts live, with one exception: one chart
  may appear inside a person's block in the Cast if it's about them.
- Check it renders. `open "the report.html"`, click every tab, hover a chart,
  hit the theme toggle, and read it once at phone width before you hand it over.
