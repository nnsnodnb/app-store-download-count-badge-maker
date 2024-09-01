from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from maker.appstore import parse_tsv


@pytest.fixture()
def tsv_path(tmp_path) -> Path:
    apple_identifiers = np.array([1, 2, 3, 3, 1, 3])
    units = np.array([1, 2, 3, 4, 5, 6])
    df = pd.DataFrame(
        {
            "Apple Identifier": apple_identifiers,
            "Units": units,
        }
    )
    tsv_path = tmp_path / "test.tsv"
    df.to_csv(tsv_path, sep="\t", index=False)
    return tsv_path


@pytest.mark.parametrize(
    "apple_identifier, expected",
    [
        (1, 6),
        (2, 2),
        (3, 13),
    ],
    ids=["apple_identifier=1", "apple_identifier=2", "apple_identifier=3"],
)
def test_it(tsv_path, apple_identifier, expected):
    actual = parse_tsv(tsv_path=tsv_path, apple_identifier=apple_identifier)

    assert actual == expected
