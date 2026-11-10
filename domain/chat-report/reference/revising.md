# Revising a report

Everything a report is made of stays in `results/<chat-name>/` — `stats.json`,
`content.html`, `report.html`. Revising means editing the content and running
the builder again. Same folder, same file, same URL if it was published.

Three kinds of revision, in rising order of how much you rewrite.

---

## 1. More detail on the same material

They've read it and want a section opened up, or something you skipped.

- Go back to the chat. **Never expand a section by writing more sentences about
  what you already found** — that's padding, and it dilutes the report's only
  real asset, which is that everything in it is sourced. Find new evidence or
  don't lengthen the section.
- Keep the length rules. If a section outgrows 400 words, split it and give the
  new half its own heading.
- Rebuild. Nothing else changes.

If the ask is big enough to need its own argument — "go deeper on the money
thing" — that's not a revision, it's a deep dive. See `deep-dive.md`.

---

## 2. A new export added

More of the same chat (a later export), or a second thread with the same
people.

1. Re-run the numbers over **all** the exports at once — never patch the old
   `stats.json`:

   ```
   python3 scripts/chatstats.py old.txt new.txt --people
   python3 scripts/chatstats.py old.txt new.txt \
     --alias "…" --label "…" --json "results/<name>/stats.json"
   ```

   Repeats are dropped, so an overlapping re-export is safe. Read
   `combining.md` before you do this — the alias step is not optional.

2. **Every number in the prose is now stale.** Message shares, question counts,
   silence rankings, "he never once…" claims — all of them move. Go through
   `content.html` and re-check each one against the new digest. The charts
   update themselves; the sentences don't.

3. Read the new material properly, then ask the honest question: *does this
   change the argument, or just extend it?* Both answers are fine. Saying
   "nothing here changed my read, and here's why" is a real finding.

4. Rebuild with a note saying what's new:

   ```
   python3 scripts/build_report.py … \
     --updated "Updated 2 March — now includes the group chat (1,900 more messages)."
   ```

---

## 3. The argument itself changed

New material contradicted the first report, or a closer read did.

**Lead with it.** Put a revision block at the top of The Read, before the
opening — the first thing the reader sees is what you got wrong.

```html
<div class="revision">
  <b>What changed in this version</b>
  <p>The group chat says the silence in October wasn't her withdrawing. She was moving house.</p>
  <ul>
    <li>I said she went quiet for nine days for no stated reason. There was a reason, and she told two other people.</li>
    <li>That makes the "she never asks for anything" line wrong. She asks — just never here.</li>
  </ul>
</div>
```

Rules for it:

- Say what you claimed, and what's true now. Both, plainly. Don't write "some
  nuance has emerged."
- Two or three items. If more than three claims collapsed, the first report was
  guessing and you should rewrite it rather than annotate it.
- Then fix the actual sections. A correction at the top does not license leaving
  the wrong sentence in place further down.
- Don't apologise. Correct it and move on.

**Never quietly delete a claim the reader has already read.** They will notice,
and it costs you the thing the whole report runs on.

---

## Keeping versions

Overwrite `report.html` — the folder is the current version, not an archive.
If they want the old one kept, copy it to `report-<date>.html` first and say
you've done it. If the report was published, update that page in place at the
same URL, so a revision reaches whoever already has the link.
