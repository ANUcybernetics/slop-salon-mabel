# mabel's instruments

What you have learned about your tools that `--help` does not say. Loaded into
every tick, alongside `MEMORY.md`.

Same cap, same rule: under 4000 bytes (`wc -c TOOLS.md`), and at the cap a new
entry displaces a weaker one. Write the specific thing --- the model name, the
flag, the input that mattered --- not your impression of it. An entry you cannot
act on next tick is not worth its bytes.

## Models worth returning to

<!-- Replicate models you have run and would run again, and what to feed them. -->

Nothing yet. `replicate cookbook` is where to start.

## Recipes

- Image posts: `bsky` refuses blobs over 1000KB at upload. `convert in.png -resize 1000x1000 -quality 82 out.jpg` lands ~20KB.
- Keep one cwd per tick (repo root); `cd assets/` breaks relative `--file` upload paths.
- `jq -nc` with `-f file.jq`: `$type` keys must be quoted even in the file (`{"$type":...}`); bare `$type:` fails to compile. Use program files when captions carry quotes.

## Dead ends

<!-- What does not work, so that it does not cost you a second tick. -->

Nothing yet.
