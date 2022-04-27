import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..')))
from main import add_question
import pandas as pd
from pandas.testing import assert_frame_equal
import pytest
from io import StringIO

def test_add_question(monkeypatch):
    test_df = pd.read_csv('./data/test_data.csv')
    df = pd.read_csv('./data/animals.csv')
    monkeypatch.setattr('sys.stdin', StringIO('Is it a carnivore?'))
    assert_frame_equal(add_question(df), test_df)
