# Exports: what you'll be handed, and what to do with it

## WhatsApp

The common case. A `.txt` file, or a `.zip` containing `_chat.txt` plus media.
Unzip to the scratchpad, never into the user's folder.

Two header styles, both handled by the script:

```
[04/03/2023, 09:12:45] Alex: message text
04/03/2023, 09:12 - Alex: message text
```

Things to know:
- Day-first vs month-first varies by phone locale. The script detects it; if the
  chat spans a range that looks impossible, check this first.
- Media is stripped on export: `<Media omitted>`, `image omitted`, `sticker
  omitted`. Count them — who sends pictures is a real fact — but you can't see
  them.
- `This message was deleted` is worth noticing, especially who does it and when.
- System lines (added, removed, changed the subject, left) have no sender. The
  group's renamings and who left are useful; the script keeps them separately.
- Replies and reactions do not survive the export. Don't claim you know what a
  message was replying to unless it's obvious from the text.

## iMessage

Usually via `imessage-exporter` (txt or html) or a database dump. The txt output
puts the sender and timestamp on their own lines. Reactions ("Liked a
message") show up as messages — count them separately, they're not
conversation. Read receipts and edits may appear; ignore them.

## Telegram

`result.json` from Desktop → Export chat history. Messages are objects with
`from`, `date`, and `text` (which is either a string or a list of fragments —
join the fragments' `text` fields). `service` type messages are joins, pins and
calls.

## Instagram / Facebook

`message_1.json` (and `_2`, `_3`…) with `sender_name`, `timestamp_ms`,
`content`. **Order is newest-first** and must be reversed. Text is
double-encoded — `â\x80\x99` needs fixing (`content.encode('latin1').decode('utf8')`).
Unsent messages and reactions live in separate keys.

## Discord

Usually a CSV or JSON from DiscordChatExporter: `AuthorID, Author, Date,
Content, Reactions`. Channel context matters — check whether the export is one
channel or a whole server.

## Generic / unknown

If nothing matches, read the first 40 lines yourself and work out the shape.
The script's `--regex` flag takes a custom header pattern with named groups
`ts`, `who`, `msg`. Failing that, hand-count with grep — you do not need the
script to write the report, only to be accurate about numbers.

---

# The counting pass

```
python3 scripts/chatstats.py "<export>"                # the full digest
python3 scripts/chatstats.py "<export>" --grep "sorry" -C 2
python3 scripts/chatstats.py "<export>" --day 2023-05-14
python3 scripts/chatstats.py "<export>" --range 2023-05-10 2023-05-18
python3 scripts/chatstats.py "<export>" --sample 40
python3 scripts/chatstats.py "<export>" --person "Alex" --grep "?"
```

What the digest gives you, and what each thing is actually for:

| What it reports | What you use it for |
|---|---|
| Message share per person | The opening line of every cast section |
| Words per person, longest messages | Who explains and who declares |
| Who reaches first after a gap | Section 7, and who is holding this together |
| Who ends conversations | Power, and the exit |
| Median reply time per person | The single most revealing number in most chats |
| Longest silences, and who broke each | The fights nobody described as a fight |
| Monthly volume, per person | Eras, drift, the month it changed |
| Double-texting runs | Anxiety, and who is talking to a wall |
| Questions asked per person | One-way curiosity — often the whole report |
| Distinctive words per person | Voice, nicknames, tells |
| Repeated phrases | The dictionary, and the running jokes |
| First and last message | The opening and the ending of the report |

## Reading after counting

The numbers tell you where to point the reading. Always read, in full:

1. The first day and the last day.
2. The two busiest days in the whole chat.
3. Both sides of every silence longer than a week.
4. The month with the sharpest drop in volume.
5. Every hit for: each person's name, "sorry", "sad", "love", "hate", "miss",
   "fine", "whatever", "call", "why did you", "you never", "you always",
   money amounts, and whatever slang the phrase list surfaced.
6. Any late-night run of messages — after 1am, the mask comes off.

Keep the quotes as you find them, with dates, in a scratchpad file. You will
not find them again by memory in a 60,000-message export.

## When the export is enormous

Above roughly 30,000 messages, work month by month: run the digest, then read
each month's busiest week, and write a two-line note per month before you write
anything else. The notes become the timeline, and the timeline stops the report
from becoming a description of the last three weeks.
