# specfence-blog

A 24-part blog series on specfence: what it is, why exhaustive checking earns its keep next to testing, five worked examples, the landscape and trust point, three deep comparisons, the conversation, and an evaluation arc. Written in the style of the author's [ai4sgfinder](https://ashitpatel.github.io/ai4sgfinder/) and [lesson-scaffold-builder](https://ashitpatel.github.io/lesson-scaffold-builder/) series.

## Layout

- `blog/` — the Jekyll site (minima theme, `series` navigation). Posts in `_posts/`, in series order.
- `evidence/` — the primary sources for the worked examples, vendored so they stand alone:
  - `pool/` — the greenfield worked example: settled requirements, `Pool.tla`/`Pool.cfg`, `pool.als`, acceptance scenarios, answers file, `replay.py`.
  - `kombu/` — the structural story, regenerated for this series: the full Alloy model + run log, and the base/head trees with the golden model and the review verdict (`review.json`) behind the structural drift demo.
  - `engines/` — the second-engine spike reports.
  - `manual/` — the bot-teams guide.

  The benchmark and run records behind the evaluation posts are kept privately; ask the author for access.

## Preview

```bash
cd blog
bundle exec jekyll serve   # or: jekyll serve
```

## Publish

Push this directory as a GitHub repository with Pages enabled (Jekyll, `blog/` as the source or the repo root — adjust accordingly). If the repository is not named `specfence-blog`, update `baseurl` in `blog/_config.yml` (one line) to match.

## License

Apache 2.0 (`LICENSE`). Vendored evidence keeps its sources' provenance: code trees from the named upstream projects (kombu: BSD-3-Clause).
