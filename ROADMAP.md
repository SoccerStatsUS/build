# ROADMAP.md — Development Roadmap

Open work only; completed items are removed as they land (see git history).

The build order is load -> normalize -> lift -> transform -> merge -> generate ->
denormalize (see `README.md`). Items below are grouped by the stage they affect.

---

## Remove the pdb monkeypatch (do this first)

`rejects.install()` reassigns `pdb.set_trace`, so a call site that reads as
"drop into the debugger" instead writes a JSON record. That is deliberate and it
is scaffolding, not a design. It buys one thing: an inventory of which of the
119 `set_trace` sites across `parse`, `build` and `metadata` actually fire,
without editing 119 call sites across three repos to find out. The payoff only
arrives when a new source is switched on; until then it is a documented wart
with no benefit, and reverting it costs one commit.

The inventory does not need a full build, and should not wait for one. Today's
MLS-only build already runs every `build/make` stage, all of `parse`, and
`load_metadata`, and produces zero records — so those sites are quiet at least
for MLS-shaped input. The 119 break down as: 20 in always-run build stages, 39
in `parse`, 40 in `metadata` (19 of them in the competition-specific
`cmp/copaamerica.py`, `cmp/pdl.py` and `cmp/asl.py`, which only run behind
disabled loaders), and 20 in `s2/build`, which uses its own stub that raises.

- [ ] Collect the inventory incrementally: each time a source is enabled in
  `load.py`, read `logs/rejects.jsonl` before committing. That is the same rhythm
  the loaders already came back on in, it scopes each batch of records to one
  source, and it never requires a big run.
- [ ] Convert the sites that fire to explicit `rejects.record(...)` calls, source
  by source, as they turn up.
- [ ] Backstop, so this cannot linger: the patch is earning nothing while
  `rejects.jsonl` is empty. If no source has been enabled by the next time this
  repo's loaders are touched, revert it — `rejects.record()` can stay as a plain
  function, and the `set_trace` stub goes back to the print it replaced.
- [ ] Give `parse` its own answer. It is otherwise standalone — only
  `parse/rosters.py` reaches into `metadata`, which is its own layering wart — so
  it must not import `build.rejects`. Its sites should return rejects or take a
  collector.
- [ ] Delete `install()` and `_record_set_trace`, and restore whatever
  `pdb.set_trace` should mean in a batch run (probably: raise, as `s2/build`
  already does).

Until that last box is ticked, `pdb.set_trace()` in this codebase does not mean
what it says. The patch also depends on every live site being spelled exactly
`import pdb; pdb.set_trace()`; nothing enforces that, and a miss would be silent.

## Name Mapping

- [ ] Giant ASL team name bug — described in the old README as "easy but producing a
  lot of errors," which makes it the highest-value item here. The competition- and
  season-scoped splits live in `make/separate.py`.
- [ ] Fix the Brooklyn Hakoah name mapping — `Brooklyn Hakoah` (`make/separate.py:658`)
  and `Hakoah` (`make/separate.py:913`) are the bad entries, and `notes/timelines:27`
  records the underlying history: Hakoah All-Stars renamed New York Hakoah c. 1929,
  then Brooklyn Hakoah merged with New York Hakoah in Spring 1930. Accurate names for
  each period still need to be established.
- [ ] Audit the remaining ASL name mappings — the same merge/rename pattern likely
  affects other clubs of the era.

## Data Formats

- [ ] Parser and data formats are not properly specified — the text formats consumed by
  `make/load.py` are defined only by what the parser happens to accept.
- [ ] Convert bios to YAML — bios are currently loaded per-source and merged in
  `make/merge.py:265` (`merge_bios`), normalized as a group in `make/normalize.py:37`.
- [ ] Consider moving aliases into the data repos — aliases live in `metadata.alias`
  and are imported across `make/load.py`, `make/normalize.py`, `make/separate.py`,
  `make/transform.py`, `make/generate.py`, and `make/denormalize.py`.

## Data Gaps

Missing or thin source data. Roughly ordered by how much is missing.

- [ ] PDL — everything
- [ ] Copa America — everything; available at RSSSF
- [ ] APSL — everything pre-1993; 1994-1995 is spotty
- [ ] ASL2 — entirely terrible
- [ ] ASL — game locations and referees; lineups and goals
- [ ] CCC — very weak
- [ ] CCL — lineup/goal info very weak
- [ ] ISL — incomplete (loading was wired up in `make/load.py`; the data itself is short)
- [ ] Open Cup — spotty; watch for release of new Open Cup data
- [ ] NASL — lineup and goal info
- [ ] USL-1 / USL-2 — 2001-2003 and 2008-2009 lineups/goals
- [ ] SuperLiga — non-US goals/lineups
- [ ] Gold Cup — champions; non-US results/goals/lineups
- [ ] United States — game locations; scattered unknown-opponent lineups
- [ ] MLS 2012 season data
- [ ] 2010 World Cup

## Error Detection

- [ ] Expand checking beyond standings validity and game fields (`make/check.py`).
- [ ] Draw a graph of seasons — a visualization to surface gaps and overlaps in the
  season/competition structure.

## Data Notes

Known deliberate inaccuracies in the source data, to be corrected when real dates are
found. Games moved a day for convenience:

- Dallas - Apollon, 1971-07-08 (moved forward one day)
- Hapoel, 1970-06-30
- Veracruz, 1973-07-11 (Dallas/Atlanta)
- Hapoel / St. Louis / Washington, 1970-06-28
