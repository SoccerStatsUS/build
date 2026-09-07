import importlib

from build import mongo
from fakedb import FakeDB


def test_load_runs_enabled_loaders_once_in_order(monkeypatch):
    monkeypatch.setattr(mongo, 'soccer_db', FakeDB())
    load = importlib.import_module('load')

    calls = []
    expected = [
        'check_for_name_loops',
        'check_for_team_loops',
        'clear_all',
        'load_metadata',
        'load_alpf',
        'load_asl',
        'load_nasl',
        'load_mls',
        'load_women_domestic',
        'load_us_cups',
        'load_scraped_us_cups',
        'load_canada',
        'load_scraped_canada',
        'load_concacaf',
        'load_scraped_concacaf',
        'load_usmnt',
    ]

    for name in expected:
        monkeypatch.setattr(load, name, lambda name=name: calls.append(name))

    load.load()

    assert calls == expected
