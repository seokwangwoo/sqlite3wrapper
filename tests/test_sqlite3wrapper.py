#!/usr/bin/env python
"""Tests for `sqlite3wrapper` package."""
# pylint: disable=redefined-outer-name

import os

import pytest

from sqlite3wrapper.sqlite3wrapper import DatabaseManager


@pytest.fixture
def database():
    """Pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    database_path = os.path.join(os.getcwd(), "test.db")
    os.remove(database_path)
    db = DatabaseManager(database_path)
    db.create_table(
        "SCORES",
        {
            "number": "text not null",
            "name": "text not null PRIMARY KEY",
            "math": "integer not null",
            "science": "integer not null",
        },
    )
    data = {
        "number": "1",
        "name": "smith",
        "math": 100,
        "science": 100,
    }
    db.add(table_name="SCORES", data=data)
    data = {
        "number": "2",
        "name": "alex",
        "math": 80,
        "science": 50,
    }
    db.add(table_name="SCORES", data=data)
    return db


def test_select(database):
    smith = database.select(table_name="SCORES").fetchall()[0]
    print(smith)
    assert smith[0] == "1"
    assert smith[1] == "smith"
    assert smith[2] == 100
    assert smith[3] == 100


def test_select_criteria(database):
    criteria = {"name": "alex"}
    alex = database.select(table_name="SCORES", criteria=criteria).fetchall()[0]
    print(alex)
    assert alex[0] == "2"
    assert alex[1] == "alex"
    assert alex[2] == 80
    assert alex[3] == 50


def test_get_primary_key(database):
    key = database.get_primary_key(table_name="SCORES")
    assert key == "name"


def test_delete(database):
    criteria = {"name": "smith"}
    database.delete(table_name="SCORES", criteria=criteria)
    smith = database.select(table_name="SCORES", criteria=criteria).fetchall()
    assert smith == []


def test_update(database):
    data = {"number": "2", "name": "alex", "math": 100, "science": 80}
    database.update(table_name="SCORES", data=data)
    alex = database.select(table_name="SCORES", criteria={"name": "alex"}).fetchall()[0]
    print(alex)
    assert alex[2] == 100
    assert alex[3] == 80
