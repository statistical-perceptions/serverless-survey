"""
test_utils.py — basic tests for utils.py
"""
import os
import pytest
import pandas as pd

from ssbuilder.utils import calculate_query_length, merge_dir_csvs, md_params


# calculate_query_length

class TestCalculateQueryLength:

    def test_returns_integer(self, sample_instructions_file):
        assert isinstance(calculate_query_length(sample_instructions_file), int)

    def test_result_is_positive(self, sample_instructions_file):
        assert calculate_query_length(sample_instructions_file) > 0

    def test_longer_id_increases_estimate(self, sample_instructions_file):
        short = calculate_query_length(sample_instructions_file, id_length=5)
        long_ = calculate_query_length(sample_instructions_file, id_length=20)
        assert long_ > short

    def test_base_url_increases_estimate(self, sample_instructions_file):
        with_base = calculate_query_length(sample_instructions_file, exclude_base=False)
        without_base = calculate_query_length(sample_instructions_file, exclude_base=True)
        assert with_base > without_base


# merge_dir_csvs

class TestMergeDirCsvs:

    def _write_csv(self, folder, name, data):
        path = os.path.join(folder, name)
        pd.DataFrame(data).to_csv(path, index=False)

    def test_output_file_written(self, tmp_path):
        folder = str(tmp_path / "csvs")
        os.makedirs(folder)
        self._write_csv(folder, "a.csv", {"id": [1, 2], "val_a": [10, 20]})
        self._write_csv(folder, "b.csv", {"id": [1, 2], "val_b": [30, 40]})
        out = str(tmp_path / "merged.csv")
        merge_dir_csvs(folder, merge_on="id", out_name=out, skip_row=[])
        assert os.path.isfile(out)

    def test_outer_merge_keeps_all_rows(self, tmp_path):
        folder = str(tmp_path / "csvs")
        os.makedirs(folder)
        self._write_csv(folder, "a.csv", {"id": [1, 2, 3], "val_a": [1, 2, 3]})
        self._write_csv(folder, "b.csv", {"id": [1, 2, 4], "val_b": [4, 5, 6]})
        out = str(tmp_path / "merged.csv")
        merge_dir_csvs(folder, merge_on="id", out_name=out, skip_row=[])
        result = pd.read_csv(out)
        assert len(result) == 4

    def test_inner_merge_keeps_shared_rows_only(self, tmp_path):
        folder = str(tmp_path / "csvs")
        os.makedirs(folder)
        self._write_csv(folder, "a.csv", {"id": [1, 2, 3], "val_a": [1, 2, 3]})
        self._write_csv(folder, "b.csv", {"id": [2, 3, 4], "val_b": [4, 5, 6]})
        out = str(tmp_path / "merged.csv")
        merge_dir_csvs(folder, merge_on="id", out_name=out, skip_row=[], complete_only=True)
        result = pd.read_csv(out)
        assert len(result) == 2


# md_params — module-level function needed so numpydoc can parse it

def _dummy_func_with_params():
    """
    Dummy function.

    Parameters
    ----------
    alpha : float
        First param
    beta : int
        Second param

    Returns
    -------
    result : str
        Something
    """
    pass


class TestMdParams:

    def test_returns_string(self):
        assert isinstance(md_params(_dummy_func_with_params), str)

    def test_param_names_in_output(self):
        result = md_params(_dummy_func_with_params)
        assert "alpha" in result
        assert "beta" in result

    def test_params_in_backticks(self):
        result = md_params(_dummy_func_with_params)
        assert "`alpha`" in result
