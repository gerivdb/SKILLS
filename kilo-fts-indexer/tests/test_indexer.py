import pytest
from kilo_fts_indexer import build_index, search
import os
import tempfile

TEST_DB = os.path.join(tempfile.gettempdir(), "test_kilo.db")
TEST_INDEX = os.path.join(tempfile.gettempdir(), "test_kilo_fts.db")


def setup_module(module):
    # Créer une base de test avec des messages
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    if os.path.exists(TEST_INDEX):
        os.remove(TEST_INDEX)
    conn = sqlite3.connect(TEST_DB)
    conn.execute("CREATE TABLE messages (id INTEGER PRIMARY KEY, content TEXT, session_id TEXT)")
    conn.executemany(
        "INSERT INTO messages (content, session_id) VALUES (?, ?)",
        [
            ("navigateur Chromium Profile 2 port 9222 CDP", "s1"),
            ("extraction DOM Google Keep Playwright", "s1"),
            ("doctrine navigateur attitré ENV2", "s2"),
            ("autre sujet sans rapport", "s3"),
        ],
    )
    conn.commit()
    conn.close()


def teardown_module(module):
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    if os.path.exists(TEST_INDEX):
        os.remove(TEST_INDEX)


def test_build_and_search():
    result = build_index(TEST_DB, TEST_INDEX)
    assert result["scanned"] == 4
    assert result["inserted"] == 4

    results = search(TEST_INDEX, "Chromium CDP")
    assert len(results) >= 1
    assert any("Chromium" in r["content"] for r in results)


def test_search_no_results():
    results = search(TEST_INDEX, "zzzqwxyznonexistent")
    assert len(results) == 0


import sqlite3
