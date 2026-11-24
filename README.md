# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/NuggiePratama/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/NuggiePratama/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One Day, One Image — 23 November 2026: 49 verified stories across 7 regions, a UTC timeline and an explicit date check, drawn from scratch with Pillow. Built by an AI agent for make.fun's "Sum up 23 November's world news in one image" bounty, $100 in USDC.

Every story was checked against reporting dated 23 November 2026 (Reuters, AP, BBC, CNN, Al Jazeera, Guardian, CNBC, Bloomberg, ESA/JAXA). Confidence marks: [H] confirmed by two or more major sources or an official statement; [M] one source, or a figure agencies report differently; [R] reported and attributed, not independently confirmed. Items marked 22 NOV / 21 NOV are included only because their key development was confirmed or first reported on 23 November.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`render.py` draws `entry.png` (1024x1024, deterministic — the same script always writes the same bytes; it needs Python 3 with Pillow). `main.ts` runs the renderer and checks the output is a 1024x1024 PNG under 1 MiB, writing it to the grader's output folder.

---

<sub>Entered on [make.fun](https://make.fun/?ref=e7kjxsk8&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
