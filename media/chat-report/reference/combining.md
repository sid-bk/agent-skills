# Reading several exports as one story

Four reasons to combine, and each changes what the report is about.

| What you're handed | What the report becomes |
|---|---|
| The same friendship across two apps (WhatsApp then Signal, iMessage then WhatsApp) | One continuous relationship. The app change is invisible to the people; treat it that way. |
| A group chat plus the one-on-ones inside it | The real story: what gets said in the room versus what gets said about the room. |
| One chat exported twice, months apart | An updated report. See `revising.md`. |
| Several different friendships, same person in all of them | A report about that one person, seen from four angles. |

## Get the names straight first

Nothing matters more. The same human is written differently in every export —
"Alex", "Alex Morgan", a phone number, a nickname the group uses.
Merge them or every count in the report is wrong.

```
python3 scripts/chatstats.py A.txt B.txt --people
```

That prints the senders in each file with counts, and stops. Build the alias
map from it, then run for real:

```
python3 scripts/chatstats.py A.txt B.txt \
  --alias "Alex Morgan=Alex" \
  --alias "+447700900123=Sam" \
  --label "A.txt=The group" --label "B.txt=Alex & Sam" \
  --json "results/<name>/stats.json"
```

Labels become the source names on the page, so make them read like English —
"The group", "Just us two", "Before the fallout" — not filenames.

Exact repeats (same moment, same sender, same words) are dropped automatically,
so overlapping exports don't inflate anything.

## Reading a merged set

`--source "The group"` limits any read to one thread, which is how you compare:

```
python3 scripts/chatstats.py A.txt B.txt --source "The group" --grep "money"
python3 scripts/chatstats.py A.txt B.txt --source "Just us two" --grep "money"
```

That comparison is the whole point of combining. Do it deliberately for the
three or four subjects that matter — money, a specific person, plans, the
fight — and note where the two rooms disagree.

## What the report gains

Two sections earn their place when there's more than one source. Put them in
The Read, not The Numbers.

**What each room is for.** Every thread has a job. One is where plans get made,
one is where feelings go, one is where two people talk about a third. Name each
one's job in a sentence and prove it — the subject that appears in one and
never the other is the proof.

**The difference between rooms.** This is the sharpest thing a combined report
can do, and it must be handled straight. If someone is warm in the group and
cold in the DM, say so with both quotes and the dates. If they're the same in
both, say that too — it's rarer and it's a compliment.

Two rules on this section, and they're not optional:

- **Different is not dishonest.** Everyone talks differently in different
  rooms. Only call it a contradiction when the two statements cannot both be
  true, and quote both.
- **Watch whose side you're on.** The person who handed you four exports is in
  all four and everyone else is in one. That asymmetry will make them look like
  the reasonable one in every room. Correct for it out loud.

## Charts

`sources` (who talked where) and `sourceTimeline` (which thread was alive when)
appear automatically once there's more than one export. `sourceTimeline` is
often the best chart in the whole report: it shows one conversation dying
exactly as another starts.

## When not to combine

Don't merge chats with different casts into one continuous timeline and then
write about "the group" — there is no group. If the people barely overlap, it's
two reports, and say so rather than forcing one.
