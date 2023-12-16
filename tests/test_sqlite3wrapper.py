#!/usr/bin/env python
"""Tests for `sqlite3wrapper` package."""
# pylint: disable=redefined-outer-name

import os
import pytest
from sqlite3wrapper.sqlite3wrapper import DatabaseManager

@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
    del response

def test_database():
    os.remove('test.db')
    db = DatabaseManager('test.db')
    db.create_table('SCORES', {
        'name': 'text not null PRIMARY KEY',
        'number': 'text not null',
        'math': 'integer not null',
        'science': 'integer not null',
        }
    )
    data = {
        'name': 'smith',
        'number': '1',
        'math': 100,
        'science': 100,
    }
    db.add(table_name='SCORES', data=data)

    smith = db.select(table_name='SCORES').fetchall()[0]
    print(smith)
    assert smith[0] == 'smith'
    assert smith[1] == '1'
    assert smith[2] == 100
    assert smith[3] == 100