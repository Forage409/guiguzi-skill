<p align="center">
  <h1 align="center">GuiGuZi.skill</h1>
  <p align="center">
    <strong>Distill any domain's methodology into an actionable operating system</strong>
  </p>
  <p align="center">
    NuWa distills how people think. GuiGuZi distills how to master a craft.
  </p>
  <p align="center">
    <a href="#quick-start">Quick Start</a> · <a href="#how-it-works">How It Works</a> · <a href="README.md">中文</a>
  </p>
</p>

---

## What is this?

Learning a new skill is painful — not because it's hard, but because **you don't know what to learn first**.

One YouTuber says start with A. A course says B matters more. Reddit argues C is the real key. You waste 3 months going in circles.

**GuiGuZi.skill** fixes this.

It's a [Claude Code Skill](https://docs.anthropic.com/en/docs/claude-code) that takes any domain name (e.g., "short-form video", "indie hacking", "latte art") and automatically:

1. **Runs 6 parallel research agents** — classics, real cases, community consensus, tools, monetization, learning paths
2. **Triple-validates findings** — cross-source replication × actionability × counter-intuitiveness
3. **Generates a complete methodology** — core principles, deadly traps, staged roadmap, monetization map, honest boundaries

The output isn't "study notes." It's **a cognitive operating system for that domain**.

---

## Why not just ask ChatGPT?

| Regular AI chat | GuiGuZi.skill |
|----------------|---------------|
| Single-turn, off the top of its head | 6 agents researching in parallel across 6 dimensions |
| Based on training data | Real-time search + multi-source cross-validation |
| Vague advice ("be persistent", "it depends") | Specific steps ("do X daily for Y weeks") |
| No quality assurance | 4-round quality testing + dual-agent adversarial polish |
| One-shot reply | Complete file system output, iterable |

**The core difference: GuiGuZi uses 6 parallel agents for research — something web-based AI can't do.**

---

## Quick Start

### Install

```bash
npx skills add Forage409/guiguzi-skill
```

### Use

In Claude Code, just say:

```
Distill the methodology for "indie hacking"
```

Or:

```
I want to learn short-form video creation from scratch, distill this domain for me
```

GuiGuZi auto-detects intent and runs the full pipeline.

---

## How It Works

```
Phase 0: Entry Routing → full distill / supplement / quality check
     ↓
Phase 1: 6 Parallel Research Agents
     ├── Classics & authorities
     ├── Real-world cases
     ├── Community consensus
     ├── Tools & tech stack
     ├── Monetization paths
     └── Learning paths
     ↓
Phase 1.5: Research Quality Matrix
     ↓
Phase 2: Triple Validation
     ├── Cross-source (≥2 independent sources)
     ├── Actionability (converts to "when X, do Y")
     └── Counter-intuitive (newbie says "wait, really?")
     ↓
Phase 3: Skill Construction
     ↓
Phase 4: 4 Quality Tests (newbie / deep-water / anti-BS / timeliness)
     ↓
Phase 5: Dual-Agent Adversarial Polish (Red team + Blue team, 8-dim score ≥7)
```

### What's in the output?

- **Domain Portrait**: one-line definition, who it's for, who should avoid it, brutal truth
- **Core Principles** (3-7): triple-validated, with evidence and specific usage
- **Deadly Traps** (5-10): extracted from real failures, not guesses
- **Decision Heuristics**: quick judgment rules for common choices
- **Staged Roadmap**: Survive → Grow → Monetize → Scale, with graduation criteria
- **Monetization Map**: median income, startup conditions, zero-to-first-dollar steps
- **Resource Map**: must-read (free), worth paying, avoid (traps)
- **Domain Controversies**: disputed views presented without judgment
- **Honest Boundaries**: cutoff date, low-confidence areas, what this can't replace

---

## Inspiration

GuiGuZi.skill is inspired by [NuWa.skill](https://github.com/alchaincyf/nuwa-skill).

NuWa distills **people** — extracting someone's thinking patterns and expression DNA.
GuiGuZi distills **crafts** — extracting a domain's collective wisdom into executable methodology.

They complement each other: NuWa tells you "how this person thinks," GuiGuZi tells you "how to master this craft."

---

## Project Structure

```
guiguzi-skill/
├── SKILL.md                          # Core skill definition
├── README.md                         # Chinese docs
├── README_EN.md                      # English docs (you are here)
├── LICENSE                           # MIT
├── references/
│   ├── domain-skill-template.md      # Output template
│   └── extraction-framework.md       # Extraction methodology
└── scripts/
    ├── quality_check.py              # Quality checker
    └── merge_research.py             # Research data merger
```

---

## FAQ

**Q: How long does it take?**
A: Full pipeline takes ~10-20 minutes depending on domain complexity.

**Q: How accurate is it?**
A: Every core principle is triple-validated. GuiGuZi marks low-confidence areas in "Honest Boundaries." No AI is 100% accurate — the key is GuiGuZi tells you what it's uncertain about.

**Q: Can I edit the output?**
A: Absolutely. The output is a Markdown file you can modify based on your own experience.

---

## Contributing

Contributions welcome! You can:

1. **Submit domain Skills you've distilled**
2. **Improve the extraction framework**
3. **Report issues** — found BS or inaccuracies? Open an Issue
4. **Translate** — help bring this to more languages

---

## License

[MIT](LICENSE)

---

<p align="center">
  <strong>Made with GuiGuZi.skill</strong><br>
  NuWa distills how people think. GuiGuZi distills how to master a craft.
</p>
