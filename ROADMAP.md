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
- [ ] `check_games` can never report anything (`make/check.py:60`). Its warning is
  `print("% missing fields from game %s" % game)` — `%` where it needs `%s`, so the
  format raises `ValueError`, the bare `except` catches it, and the row drops into
  `pdb.set_trace()`. Every game with a missing field takes this path. Pinned by
  `tests/test_check.py::test_missing_field_falls_through_to_pdb`; the xfail beside
  it asserts what the check should say.

- [ ] Winless teams are dropped from generated standings (`make/standings.py:85`).
  `Standing.standings()` iterates `sorted(self.wins.keys())`, and `wins` only has
  teams that won at least once — so a team that went winless never appears, and a
  round where every game was drawn produces an empty table. Fixing it means
  iterating the union of teams instead; note this changes what the build emits.
  Pinned by the xfails in `tests/test_standings.py`.

- [ ] `Standing` re-walks `games` once per column (`make/standings.py:17-22`), eight
  times in all. Harmless for the lists `generate.py` passes, but the class comment
  says "Games is probably a cursor object!" — if one is ever passed it is exhausted
  after the first pass and the result is a `KeyError`. Compute the columns in one
  pass.

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
