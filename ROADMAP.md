# ROADMAP.md — Development Roadmap

Open work only; completed items are removed as they land (see git history).

The build order is load -> normalize -> lift -> transform -> merge -> generate ->
denormalize (see `README.md`). Items below are grouped by the stage they affect.

---

## Name Mapping

- [ ] Review the player identity audit (`python -m build.identity`).
- [ ] **Contextual player identity.** `python -m build.identity` finds four NASL names
  with conflicting birth dates and 117 abbreviated ASL stat rows. Nationality supports
  13 NASL rows, while 10 NASL rows remain ambiguous; team history supports one ASL row,
  four more have a unique name-only candidate, and 112 remain unresolved. Apply the
  supported mappings without globally merging the homonyms, then research the remainder.
- [ ] Franchise renames the site still files under the old name: Sky Blue FC (Gotham FC
  since 2021), Montreal Impact (CF Montréal since 2021), Chicago Red Stars (Chicago Stars
  since 2025). The convention elsewhere is the current name as canonical with a
  `mappings/team_name` entry for the old period (Kansas City Wizards → Sporting Kansas
  City), but renaming these changes the team slugs, so s2 needs redirects first. Until
  then the new names are aliased to the old ones in `metadata/alias/teams/usa.py`;
  "Chicago Stars" goes through `separate.py` because the all-star alias claims it.
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
- [ ] Load the scraped bios — `mlssoccer_data/parsed/bios.jsonl` and
  `nwslsoccer_data/parsed/bios.jsonl` (3,861 rows) are read by nothing in `make/load.py`.
- [ ] Merge bios on stable ids — `merge_bios` (`make/merge.py:265`) keys on name only and
  over-merges by its own admission; the scraped bios carry `player_id`/`provider_id`,
  so key on those where present and fall back to name.
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
- [ ] NWSL 2015 loads 98 games against 93 in the feed, 2019 114 against 111: hand rows
  in `nwsl_data` that disagree with `nwslsoccer_data` on date or teams and so escape the
  merge. `merges == 0` (Error Detection below) would list them.
- [ ] 2010 World Cup

## Build Setup

- [ ] `load()` explicitly selects MLS, US women's leagues, US cups, ALPF, ASL,
  ASL2, NASL, Canada, CONCACAF, USMNT and indoor in `enabled_loaders`
  (`make/load.py`). Canada and CONCACAF currently load only selected
  competitions and seasons. Every other source — ISL, US minor leagues, other
  international data, drafts, jobs and salaries — is loaded by nothing, and
  production has the same shape. Decide, dataset by dataset, what else comes
  back.
- [ ] The tests only run on a machine listed in `settings.py`. `ROOT_DIR = roots[host]`
  (`settings.py:20`) is a bare dict lookup on hostname, so an unlisted machine raises
  `KeyError` on import. `merge`, `lift`, `normalize` and `transform` all import
  `settings`, so everything except `tests/test_check.py` fails to collect — 68 of the
  85 tests. `metadata/settings.py` has the same pattern. A fallback (env var, or
  derive the root from the repo location) would make the suite portable and open the
  door to CI. Not urgent while the build is one-machine and local.

## Error Detection

- [ ] Duplicate keys in dict literals silently discard the first value. An AST scan of
  `build`, `metadata` and `parse` finds 308 repeated string keys; 264 repeat the same
  value and are harmless, but **44 hold different values, so the earlier one is lost
  with no error**. `make/separate.py:873` was one: a second `'Fall River'` key seven
  lines below wiped out four season-scoped rules, leaving the 1922-1931 ASL games
  split between `Fall River` and `Fall River Marksmen`. That one is fixed; six remain
  in `separate.py`, three of which need a decision about which club is meant rather
  than a merge:
  - `Rapid` — the Liga I → `Rapid Bucureşti` rule is lost, so every "Rapid" resolves
    to Rapid Vienna.
  - `Victoria` — the Liga Nacional de Honduras → `CD Victoria` rule is lost, so
    "Victoria" resolves to `CDS Vida`, a different club.
  - `Springfield` — two rules for the same competition, `Shawsheen Indians` against
    `Springfield Babes`; one of them is simply wrong.
  - `Maryland` loses an NCAA rule; `Jenison` and `Ludlow` are benign (a typo fix and
    a superset).

  Two outside `separate.py` look like lost data rather than name confusion:
  `metadata/data/lists/awards/canada.py:111`, where `'Champion'` holds a list of
  winning teams overwritten by a list of players, and
  `metadata/data/lists/awards/ncaa.py:3840`, where a block of WCC Player of the Year
  winners is overwritten by another. The remaining 37 are alias maps whose two
  spellings disagree, several of them self-cancelling pairs that map a name in both
  directions.

  Once these are resolved, an AST duplicate-key check belongs in the test suite. It
  cannot be added first: it fails on every one of the 43 still open.

- [ ] Fill the six Fall River games no rule reaches, now that the block above runs:
  Lewis Cup 1928, 1930 and 1930 Fall (3 games), U.S. Open Cup 1931 (2), and ASL
  (1933-1983) 1958-1959 (1). The first five fall inside the Marksmen's run and the
  last is a hole in an otherwise continuous 1957-58 to 1963-64 list, but each needs a
  `from_seasons` clause naming its own competition, and which club is meant is a
  judgment about the record rather than a merge.

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

- [ ] **`nwslsoccer_data/stats/nwsl/*` is wrong.** The load is commented out in
  `make/load.py`; decide whether to fix the source or delete the files. The scraper
  (`scrapers/nwslsoccer/stats.py`) transcribes the SDP stats API faithfully — the API
  response itself is bad. Fetching the 2015 `BlockSource` gives:
  - `team` is the player's *most recent* club, not the club they played for that
    season. The 2015 response puts Christen Press at Angel City, Vanessa DiBernardo at
    Kansas City Current and Abby Erceg at Racing Louisville, while
    `nwsl_data/games/usa/nwsl/2015` has all three in one Chicago Red Stars lineup.
    Defunct clubs (Boston Breakers, Western New York Flash) survive only where the
    player's career ended there, and historic franchises get current branding back-
    applied (Sky Blue -> Gotham FC, Chicago Red Stars -> Chicago Stars). 191 of 212
    players land on a real 2015 club by coincidence of never having moved.
  - `minutes-played` is 0 for 128 of the 185 players with `games-played > 0` (69%),
    including a 20-game, 10-goal Allie Long.
  - The counting stats are season-scoped in 2015 (max GP 20, exactly the season
    length) but not in 2021 (max GP 49 against a 24-game season; top five
    27/30/46/48/49). The season id is not the culprit — `nwslsoccer_data/nwsl/2021`
    queries the same id and holds genuine 2021 fixtures, so the games endpoint is
    correctly scoped where the stats endpoint is not. Which years are inflated has
    not been surveyed.
  - One `teamId` comes back under two `officialName` strings in a single response
    (`Chicago Stars`/`Chicago Stars FC`, `Gotham FC`/`NJ/NY Gotham FC`); the alias map
    papers over this, which is why the parsed files show 16 teams against 18 names.

  Fixing it means finding a per-season, per-team attribution — check whether the API
  has a team-scoped stats endpoint — or picking a different source. Deleting costs
  little, since none of it was trustworthy. Note `nwsl_data/stats/nwsl/2013` is a
  separate hand-transcribed file and still loads.

- [ ] **An unrecognised venue silently becomes a city.** `location_normalizer`
  (`make/normalize.py`) matches a game's location against the stadium names in
  `soccer_db.stadiums`; on a miss the string falls through to `city_getter`
  (`s2/build/load.py:825-829`), which creates a `City` row for it. Nothing is
  logged. 567 of the 4,867 rows in `places.City` are venues rather than places
  — names carrying stadium, estadio, arena, bowl, oval, or a park/field that is
  nobody's birthplace and no club's home. 1,377 games hang off them.

  Two causes, and neither is a naming variant:
  - **In `team_stadium`, absent from the stadium list.**
    `team_stadium/nasl1` maps `Boston Rovers, Manning Bowl`,
    `Toronto Metros, Lamport Stadium` and `Washington Whips, D.C. Stadium`, and
    none of the three appears anywhere in `metadata/data/places/stadiums/`. The
    mapping mints a postgres `Stadium` row through `Stadium.objects.find()`
    while `normalize` — which reads the stadium list — has never heard of the
    name, so the games go to a `City` of the same name. Postgres holds 1,497
    stadium rows against 1,331 names in metadata; **139 of the 166 extra carry
    no games at all**, which is that signature.
  - **In the list only under a qualified name.** `Olympic Stadium` is in the
    stadium files five times and never bare — Montreal, Kiev, Amsterdam, Tokyo,
    Munich — so a game file writing it plain matches nothing.

  Montreal's Olympic Stadium is the worked example. It is defined once, at
  `metadata/data/places/stadiums/canada.py:171`, and 2 of its 72 games are
  attached to it: the Manic's 60 NASL and NASL-indoor games sit on a cityless
  `Olympic Stadium` row minted by `team_stadium/nasl:35` and `nasl1:136`, and
  the Impact's 10 MLS games sit on a *city* called Olympic Stadium.
  `metadata/alias/stadiums.py` already does this job for the others
  (`Olympisch Stadion`, `Tokyo Olympic Stadium`, `Oaca Spyro Louis`); the bare
  name has no entry, and claiming it for Montreal is a judgment about a name
  five cities share.

  The case-folded stadium lookup is in — `Stubhub Center` cost the venue
  sixteen 2015 MLS games — but that was only 4 of the 567. What is left:
  - Stop the build inventing places. A location matching no stadium, no city
    and no country deserves a line in the build log, not a new `City`. Smallest
    change, and it stops the list growing while the rest is worked.
  - Add the missing venues to `metadata/data/places/stadiums/`. The
    `team_stadium` mappings and a name-and-usage scan of `places.City` give the
    worklist; the scan is a few lines and worth re-running after each pass.
  - Decide the bare-name aliases, starting with `Olympic Stadium`.

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
  - NWSL now loads 2013-2019, but the seasons are nothing like equivalent. Parsing the
    files directly gives rows / rows-with-scores / goals / lineups:

        2013   92 / 91  / 246 / 2437      2017  123 / 123 /   7 /    0
        2014  112 / 111 / 356 / 3000      2018  110 / 105 / 145 / 1519
        2015   93 /  26 /  48 /  326      2019  108 /  11 /  28 /  246
        2016  103 / 103 / 188 / 1930

    2019 is about a tenth transcribed and 2015 about a quarter, so the surface roughly
    tripled rather than quintupling — 368 newly scored games against 202. 2017 is the
    odd one: every score present, seven goals, no lineups at all. Any per-source
    coverage descriptor has to be per season and per field; one attached to
    `nwsl_data` as a whole would be meaningless.
  - Watch out for false corroboration: the hand-edited NWSL files carry
    `BlockSource: http://www.nwslsoccer.com/...`, so `nwsl_data` and
    `nwslsoccer_data` were transcribed from the same upstream. Agreement between them
    is common origin, not independent confirmation. espn is the only genuinely
    independent NWSL witness we hold.
  - Note also that external sources can only ever verify the thin slice they share
    with the hand-edited data — scores, dates, sometimes attendance. Nothing external
    verifies the lineups, assists and misconduct that make `nwsl_data` worth having.
- [ ] Find strays by counting how many sources recorded a game. Most of this already
  exists and is simply not read: `merge_games` sets `d['merges'] = 0`
  (`make/merge.py:351`) and increments it on every merge (`:399`), so `merges == 0`
  already means "exactly one source record produced this game". Nothing consumes it
  outside `tests/test_merge.py:83,91`. A report of `merges == 0` grouped by
  competition and season needs no new data and is the cheapest version of the
  per-competition error list.

  Two things to sort out first, and both argue for starting with a read-only report
  rather than touching the merge:

  - `sources` counts but does not name. It accumulates at `make/merge.py:400-401`,
    but the parser fills it from the data files themselves — per-game `Source:` lines
    (`parse/parse/games.py:333`) and `BlockSource:` (`:344`). So it holds citation
    URLs a transcriber wrote down, not the identity of the contributing collection,
    and it stays empty for any source whose files carry no `Source:` line. Naming
    contributors is a small change — `merge_all_games` (`make/merge.py:79`) builds
    `['%s_games' % coll for coll in SOURCES]` and then passes only the cursors into
    `merge_games`, dropping the name — but see the warning below.
  - `merges == 0` will over-report. The keys at `make/merge.py:337-345` are
    `(teams, date, season, round)` and `(teams, competition, date)`. The comment at
    `:317` says the first is "teams, competition, season, round - no date", but the
    code puts `date` in it, so a game one source dated and another left undated
    matches on neither key and survives as two games, each claiming a single source.
    Given how much of `nwsl_data` is partially transcribed, this will fire a lot.
    Separately, a record with neither `round` nor `date` is discarded outright at
    `:347` — no counter, no message.

  Be careful here. `merge_games` produces every game in the database, so changing the
  keys or the record shape moves everything downstream with it. Read first, change
  second.

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

## Deferred

- WUSA 2001-2003 player statistics — StatsCrew has complete team-season tables with
  full names, appearances, starts, goals, assists, discipline, shooting and goalkeeper
  statistics; archived official WUSA team-stat pages can be used for verification.
  Defer ingestion because the current name-lifting problem can use existing lineup
  names, and StatsCrew does not publish an explicit open license for its soccer data.
