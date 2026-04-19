# Knowledge Base

A curated, searchable Obsidian vault of **143 essays** by [Justin Scott](https://cypherj.substack.com) — organized by theme, tagged for cross-cutting discovery, and cross-linked around his recurring conceptual frameworks.

## Getting Started

### 1. Install Obsidian

Download and install [Obsidian](https://obsidian.md) for your platform (macOS, Windows, or Linux). It's free for personal use.

### 2. Clone this repository

Open a terminal and run:

```bash
git clone https://github.com/NatoDoyle/cypherj-knowledge-base.git
```

If you don't have `git` installed:
- **macOS** — open Terminal and run `xcode-select --install`
- **Windows** — download from [git-scm.com](https://git-scm.com/downloads)
- **Linux** — run `sudo apt install git` (Debian/Ubuntu) or `sudo dnf install git` (Fedora)

Alternatively, download the ZIP from the [GitHub repo page](https://github.com/NatoDoyle/cypherj-knowledge-base) by clicking **Code > Download ZIP**, then unzip it.

### 3. Open the vault in Obsidian

1. Launch Obsidian
2. Click **Open folder as vault**
3. Navigate to the `cypherj-knowledge-base` folder you just cloned/unzipped
4. Select it and click **Open**

The vault will load with all folders, tags, and links ready to go. Start with any of the MOC pages in `_Meta/` to browse by theme, or use `Ctrl/Cmd + O` to quick-switch to any essay by title.

## Structure

```
knowledge_base/
├── Psychology/           48 essays — trauma, fear, healing, emotional patterns
├── Relationships/        29 essays — dating, intimacy, love, romantic dynamics
├── Politics/             31 essays — government, geopolitics, rights, capitalism
├── Spirituality/         15 essays — Christianity, theology, faith, metaphysics
├── Race & Culture/       11 essays — Black identity, systemic racism, cultural critique
├── Frameworks/            9 essays — concept-defining essays (theoretical backbone)
├── _Meta/                MOCs, concept pages, INDEX.md
├── _Tags/                15 tag pages with perspective summaries
└── .obsidian/            vault config
```

## How to Navigate

### Maps of Content (MOCs)

Each theme folder has a corresponding MOC page in `_Meta/` that lists every essay with a one-line summary:

- [[MOC - Psychology]]
- [[MOC - Relationships]]
- [[MOC - Politics]]
- [[MOC - Spirituality]]
- [[MOC - Race & Culture]]
- [[MOC - Frameworks]]

### Concept Pages

Seven concept pages in `_Meta/` provide synthesized summaries of Justin's recurring frameworks, plus links to every essay that references the concept:

| Concept | Description |
|---------|-------------|
| [[Entropy]] | Unprocessed collective trauma — the weight of what hasn't been healed |
| [[Proto-Fears]] | Eight primordial wounds that drive all behavior |
| [[Parallel Systems]] | Survival architectures (Maw, Keep, Flame, Thorn, Cog, Reverb, Prism, Pulse, Hearth) |
| [[Light-Identity Unified Theory]] | Consciousness as light focused through a metabolic lens |
| [[Narrative Warfare]] | Controlling the story before opponents frame it against you |
| [[Restructuring]] | Dismantling trauma-rooted survival behaviors toward wholeness |
| [[Self-Erasure]] | The adaptive disappearance of identity when survival replaces presence |

### Tag Pages

Fifteen tag pages in `_Tags/` let you explore essays by cross-cutting topic. Each page includes a summary of Justin's perspective on that topic and links to every tagged essay:

`trauma` · `fear` · `healing` · `relationships` · `identity` · `race` · `politics` · `geopolitics` · `faith` · `masculinity` · `femininity` · `dissociation` · `systems` · `narrative` · `capitalism`

### Obsidian Features

- **Tag pane** — filter by any of the 15 tags via Obsidian's built-in tag search
- **Graph view** — concept pages appear as connected hubs; tag pages show cross-cutting connections
- **Backlinks** — every essay shows which concept and tag pages reference it
- **Search** — full-text search across all essays via Obsidian's search (Cmd/Ctrl+Shift+F)

## Essay Format

Each essay has YAML frontmatter:

```yaml
---
title: "Essay Title"
subtitle: "Subtitle"
author: "Justin Scott"
date: YYYY-MM-DD
source: "https://cypherj.substack.com/p/slug"
word_count: NNN
primary_theme: "FolderName"
tags:
  - tag1
  - tag2
concepts:
  - "[[ConceptName]]"
---
```

## Source

All essays are by **Justin Scott**, published at [cypherj.substack.com](https://cypherj.substack.com). This vault is a personal archive for reference and study. Content spans April 2025 through March 2026.
