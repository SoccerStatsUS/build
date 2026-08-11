# ROADMAP.md — Development Roadmap

Open work only; completed items are removed as they land (see git history).

The build order is load -> normalize -> lift -> transform -> merge -> generate ->
denormalize (see `README.md`). Items below are grouped by the stage they affect.

---

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

## Build Setup

- [ ] The tests only run on a machine listed in `settings.py`. `ROOT_DIR = roots[host]`
  (`settings.py:20`) is a bare dict lookup on hostname, so an unlisted machine raises
  `KeyError` on import. `merge`, `lift`, `normalize` and `transform` all import
  `settings`, so everything except `tests/test_check.py` fails to collect — 68 of the
  85 tests. `metadata/settings.py` has the same pattern. A fallback (env var, or
  derive the root from the repo location) would make the suite portable and open the
  door to CI. Not urgent while the build is one-machine and local.

## Error Detection

- [ ] Bad data signals itself with `pdb.set_trace()` — 119 live sites across
  `parse`, `build` and `metadata`, plus ~100 bare `except:`. In a batch run
  `make/__main__.py` stubs `set_trace` out to a print of file and line, which
  says where the code was standing and never which row was bad. The sites need to
  become explicit rejects that record the offending row. Note that `parse` is
  otherwise standalone and must not import from `build`, so its sites should
  return rejects or take a collector rather than call a global sink.
  A recorder that captured this by monkeypatching `set_trace` was built and
  reverted (`git show d2c1531`) — it worked, but its payoff only arrives when a
  disabled source is switched back on, and until then it makes 119 call sites
  mean something other than what they say.
- [ ] Fix two loaded standings whose records do not add up, found by `check_standings`
  once `check_games` stopped crashing. Both are off by three games:
  - Sporting Kansas City, MLS 2011 — `games=34` but 16-9-12 sums to 37.
  - FC Dallas, MLS 2003 — `games=30` but 6-16-5 sums to 27.

  `check_games` reports nothing against the current database, so every game row
  has its seven required fields.

- [ ] Expand checking beyond standings validity and game fields (`make/check.py`).
  The comment at `make/generate.py:6` sketches the intended next step: generate
  standings from games, then check those against the loaded standings. Build the
  season table from the rolling `Standing` in `make/generate.py:470`, which is
  what actually produces standings today. (A second, unused table builder lived
  in `make/standings.py` until it was deleted — `git log -- make/standings.py`.)

- [ ] Act on what `make/reconcile.py` found. It compares two independent scrapes of
  the same competition against each other — espn vs mlssoccer for MLS (2024-2026),
  espn vs nwslsoccer for NWSL (2016-2026) — and reports unmatched games and
  field-level disagreements. It is standalone: it reads the `*_data/parsed/*.jsonl`
  archives directly, is not called from `build()` or `check()`, and deliberately does
  not reuse `metadata.alias.get_team`, which imports `build.mongo` and would drag a
  live database in behind it. Folding it into `check()` only makes sense once the
  build actually loads these sources. Open findings, worst first:
  - nwslsoccer's 2022 goal lists are broken — 58 of 137 games carry the correct score
    but an incomplete goal list (Portland 6-0 Orlando on 2022-06-19 lists one goal of
    six). 2018 has 25 more. espn's NWSL events are fine where they exist.
  - espn has NWSL 2017-06-18 FC Kansas City vs Seattle Reign as 1-1 with no goals
    recorded; nwslsoccer has 2-2 with four named scorers. espn is wrong.
  - espn carries ghost fixtures: each 2015-2016 Western New York Flash game appears
    twice under two game ids, once as a real result under the franchise's *later*
    name (North Carolina Courage) and once as an unplayed 0-0 under the name it
    actually played under. `reconcile.py` drops the unplayed copies, but this is a
    warning about trusting espn team names on historical seasons at all.
  - nwslsoccer cannot distinguish playoffs from regular season — every row is
    competition `NWSL` with a null `round`. This is why a few games a season show up
    as nwslsoccer-only.
  - mlssoccer's goal lists come up short of the score on 3 MLS 2025 games.
  - Attendance (499) and venue (389) disagree constantly and are counted, not listed;
    neither source looks authoritative and no one has picked a winner.

- [ ] Widen the verification surface. `reconcile.py` compares two external scrapes to
  each other; checking the build's own hand-edited data against an external source is
  the thing that would let a competition be called canonical, and today it is barely
  possible at all.
  - MLS has *no* overlap. The build loads games for 1996-2016 (`make/load.py:942`),
    `mlssoccer_data` starts at 2017 and `espn_data` at 2020. The archives begin the
    year the build stops. The espn scraper already reaches back to 2013 for NWSL, so
    pointing it at MLS before 2020 is a scraper config change, not a data problem.
  - NWSL overlaps on 2013-2014 only, because `make/load.py:870-871` hardcodes those
    two seasons — `nwsl_data/games/usa/nwsl/` has 2015, 2016, 2017, 2018 and 2019
    sitting on disk unloaded. Loading them takes the surface from two seasons to
    seven, which is the cheapest unblock available here.
  - Watch out for false corroboration: the hand-edited NWSL files carry
    `BlockSource: http://www.nwslsoccer.com/...`, so `nwsl_data` and
    `nwslsoccer_data` were transcribed from the same upstream. Agreement between them
    is common origin, not independent confirmation. espn is the only genuinely
    independent NWSL witness we hold.
  - Note also that external sources can only ever verify the thin slice they share
    with the hand-edited data — scores, dates, sometimes attendance. Nothing external
    verifies the lineups, assists and misconduct that make `nwsl_data` worth having.
- [ ] Run `check()` as part of the build. It is not in `build()`, so the checks only
  run if invoked by hand, which is why the two standings above went unnoticed.
- [ ] Draw a graph of seasons — a visualization to surface gaps and overlaps in the
  season/competition structure.

## Data Notes

Known deliberate inaccuracies in the source data, to be corrected when real dates are
found. Games moved a day for convenience:

- Dallas - Apollon, 1971-07-08 (moved forward one day)
- Hapoel, 1970-06-30
- Veracruz, 1973-07-11 (Dallas/Atlanta)
- Hapoel / St. Louis / Washington, 1970-06-28
