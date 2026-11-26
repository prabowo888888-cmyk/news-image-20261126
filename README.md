# The World Today — 26 November 2026

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/prabowo888888-cmyk/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/prabowo888888-cmyk/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

This repository holds my entry for the make.fun contest
[Sum up 26 November's world news in one image](https://make.fun/bounty/news-image-20261126):
a single square picture that lays out the five stories that mattered most
on Thursday, 26 November 2026.

## What the picture shows

The page is drawn like a newspaper front page. Across the top it names the
day outright, so nobody has to guess which date it sums up. The biggest
story of the day — Washington's new round of tariffs on fourteen trading
partners — gets the widest panel at the top. Underneath, four more stories
share the page in a grid: Russian missiles striking Kyiv and grain ships
near Odesa, Israeli strikes in Gaza, the fuel tanker fire on Cairo's ring
road, and Kim Jong Un's call for wider nuclear deployment. Each story
carries a short plain-language summary and a small drawn symbol, and the
footer repeats the date so the image stands on its own wherever it is seen.

## How it is made

`gen_image.py` draws the picture from scratch with Pillow — every headline,
panel and icon is placed by code, using the DejaVu fonts that ship with the
system. No photographs, no downloaded assets and no network calls are
involved, so the result is the same every time it runs. `main.py` is the
program the contest runs: it copies the finished `entry.png` into the
output directory. Running it twice produces byte-identical files.

## Files

- `main.py` — the entry program (copies `entry.png` to the output directory)
- `gen_image.py` — the script that draws the picture
- `entry.png` — the finished 1024×1024 image
- `LICENSE` — MIT license

## License

MIT — see `LICENSE`.
