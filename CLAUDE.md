# CLAUDE.md — Vault Conventions

Obsidian vault of essays by Justin Scott (cypherj.substack.com), scraped and integrated in batches. **176 essays** through 2026-06-08 across six theme folders: Psychology, Relationships, Politics, Spirituality, Race & Culture, Frameworks. Navigation lives in `_Meta/` and `_Tags/` and is kept in **strict sync** with the essay files — never edit one side without the other.

## Essay file format

Filename `YYYY-MM-DD_<substack-slug>.md` in exactly one theme folder. Frontmatter keys, in this order (all double-quoted scalars; escape inner quotes as `\"` — invalid YAML breaks Obsidian's property parsing):

```yaml
title, aliases (the title, byte-identical scalar), [subtitle], author, date,
source, word_count, summary, primary_theme (== folder name), [series],
tags (2–4 lowercase from the 15 in _Tags/), [concepts ("[[Wikilink]]" list)]
```

- `summary` is the **canonical** one-liner; the bullet in the theme MOC must be the **identical string** (script-enforced mirror).
- `series` only on members of a series listed in `_Meta/Series.md`; membership is by explicit basename list, never title regex. A new series requires 2+ essays.
- Body is plain markdown from the scraper — no wikilinks in bodies.

## Integration batch workflow (recurring task: "scrape the new posts")

1. Find latest integrated date: `grep -rh '^date:' <theme folders> | sort | tail`. Fetch archive API `https://cypherj.substack.com/api/v1/archive?sort=new&limit=12&offset=N`; skip `audience: only_paid` (e.g. "The Observer Field" 2025-05-23 stays excluded). Reuse `scrape_substack.py` functions (`fetch_post_content`, `html_to_markdown`) via import — do **not** run its `main()`/`create_index()`; `_Meta/INDEX.md` is owned by the integration script.
2. Per essay decide: theme folder, tags, concepts, summary, MOC **cluster** (each MOC's `## Essays` is split into `###` clusters — assign each new essay to one), series membership.
3. One deterministic Python script updates everything from a single data structure:
   - `_Meta/INDEX.md` — entry at top (`- [Title](../Folder/file.md) (date)`), bump `**Total posts:**` and `**Scraped on:**`.
   - `_Meta/MOC - <Theme>.md` — bump `**N essays**`, insert bullet at top of the right `###` cluster: `- [[base|Title]] — <summary>.`
   - `_Tags/<Tag>.md` — bump `## Essays (N)`, same bullet at top.
   - `_Meta/<Concept>.md` — bullet under `## Essays Referencing This Concept` (short phrase note, no period).
   - `README.md` — total + per-folder counts.
   - `_Meta/Philosophy.md` — total essay count (line 9) is count-bearing too.
   - Regenerate `_Meta/Series.md` if series membership changed; extend the current phase in `_Meta/Timeline.md` (counts + landmark essays; open a new phase only if one clearly begins).
4. When a major new recurring framework emerges: create a `_Meta/` concept page (Summary / Defining Essays / Essays Referencing This Concept / Connected Concepts with reciprocal links), add to README concept table, Philosophy's concept-page list, and `_Meta/Glossary.md` terms.

**Not per-batch:** `_Meta/Reading Paths.md` and `_Meta/Glossary.md` are curated (touch only when a path-worthy essay or new concept lands). `_Meta/Essays.base` is property-driven and maintenance-free. `_Meta/Tensions.md` is a dated snapshot — its "152 essays" stays.

## Verification invariants (run after any integration)

- Theme-folder file count == INDEX `^- \[` entry count == README total == INDEX `**Total posts:**` == Philosophy count.
- Every MOC `**N essays**` == its bullet count == folder count; every essay in exactly one cluster; every tag page `## Essays (N)` == bullet count.
- Every essay: frontmatter parses as YAML; `aliases == [title]`; `summary` == its MOC bullet text; series keys ↔ `Series.md` bijection.
- All wikilinks/markdown links in `_Meta/` resolve (decode `%20`); `Essays.base` parses as YAML; `.obsidian/graph.json` parses with 8 colorGroups.

## Repo notes

- `.gitignore` covers `.DS_Store`, `.obsidian/workspace.json`, `__pycache__/` (run `git rm --cached .obsidian/workspace.json` once at commit time if still tracked).
- Don't commit unless asked. `_Meta/Psychological Analysis of Justin Scott.md` is an AI-written author profile, linked from README and Philosophy.
