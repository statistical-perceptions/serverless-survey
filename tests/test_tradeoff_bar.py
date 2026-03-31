"""
test_tradeoff_bar.py — basic tests for TradeoffBar
"""
import pytest
import pandas as pd
import plotly.graph_objects as go

from ssbuilder.tradeoff_questions import TradeoffBar


class TestTradeoffBar:

    def test_returns_plotly_figure(self, sample_tradeoff_csv):
        fig = TradeoffBar().generate_figure(
            pretty_data_file=sample_tradeoff_csv, default_selection=5
        )
        assert isinstance(fig, go.Figure)

    def test_frame_count_matches_models(self, sample_tradeoff_csv):
        df = pd.read_csv(sample_tradeoff_csv)
        fig = TradeoffBar().generate_figure(
            pretty_data_file=sample_tradeoff_csv, default_selection=5
        )
        assert len(fig.frames) == df["model_number"].nunique()

    def test_slider_present(self, sample_tradeoff_csv):
        fig = TradeoffBar().generate_figure(
            pretty_data_file=sample_tradeoff_csv, default_selection=5
        )
        assert len(fig.layout.sliders) >= 1

    def test_slider_active_matches_selection(self, sample_tradeoff_csv):
        fig = TradeoffBar().generate_figure(
            pretty_data_file=sample_tradeoff_csv, default_selection=7
        )
        assert fig.layout.sliders[0].active == 7

    def test_play_button_removed(self, sample_tradeoff_csv):
        fig = TradeoffBar().generate_figure(
            pretty_data_file=sample_tradeoff_csv, default_selection=5
        )
        assert not fig.layout.updatemenus

    def test_explicit_y_axis_range(self, sample_tradeoff_csv):
        fig = TradeoffBar().generate_figure(
            pretty_data_file=sample_tradeoff_csv,
            y_min=0, y_max=100, default_selection=5
        )
        assert list(fig.layout.yaxis.range) == [0, 100]

    def test_disable_zoom_fixes_axes(self, sample_tradeoff_csv):
        fig = TradeoffBar().generate_figure(
            pretty_data_file=sample_tradeoff_csv,
            disable_zoom=True, default_selection=5
        )
        assert fig.layout.xaxis.fixedrange is True
        assert fig.layout.yaxis.fixedrange is True

    def test_all_csv_groups_appear_as_traces(self, sample_tradeoff_csv):
        """Every group in the CSV should be a named trace in the figure."""
        df = pd.read_csv(sample_tradeoff_csv)
        expected_groups = set(df["group"].unique())
        fig = TradeoffBar().generate_figure(
            pretty_data_file=sample_tradeoff_csv, default_selection=0
        )
        trace_names = {t.name for t in fig.frames[0].data}
        assert expected_groups == trace_names

    def test_bar_heights_within_csv_range(self, sample_tradeoff_csv):
        """Bar heights must fall within the actual data range from the CSV."""
        df = pd.read_csv(sample_tradeoff_csv)
        fig = TradeoffBar().generate_figure(
            pretty_data_file=sample_tradeoff_csv, default_selection=0
        )
        for bar in fig.frames[0].data:
            for y_val in bar.y:
                assert df["percent"].min() <= y_val <= df["percent"].max()

    def test_default_logging_vars(self):
        assert TradeoffBar().logging_vars["location_var_name"] == "model_number"
