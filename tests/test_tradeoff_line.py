"""
test_tradeoff_line.py — basic tests for TradeoffLine
"""
import pytest
import pandas as pd
import plotly.graph_objects as go

from ssbuilder.tradeoff_questions import TradeoffLine


class TestTradeoffLine:

    def test_returns_plotly_figure(self, sample_tradeoff_csv):
        fig = TradeoffLine().generate_figure(
            pretty_data_file=sample_tradeoff_csv, default_selection=5
        )
        assert isinstance(fig, go.Figure)

    def test_slider_present(self, sample_tradeoff_csv):
        fig = TradeoffLine().generate_figure(
            pretty_data_file=sample_tradeoff_csv, default_selection=5
        )
        assert len(fig.layout.sliders) >= 1

    def test_slider_steps_match_model_count(self, sample_tradeoff_csv):
        df = pd.read_csv(sample_tradeoff_csv)
        fig = TradeoffLine().generate_figure(
            pretty_data_file=sample_tradeoff_csv, default_selection=5
        )
        assert len(fig.layout.sliders[0].steps) == df["model_number"].nunique()

    def test_only_one_anchor_visible(self, sample_tradeoff_csv):
        fig = TradeoffLine().generate_figure(
            pretty_data_file=sample_tradeoff_csv, default_selection=5
        )
        visible_anchors = [
            t for t in fig.data
            if t.visible is True and t.name == "selected model"
        ]
        assert len(visible_anchors) == 1

    def test_explicit_y_axis_range(self, sample_tradeoff_csv):
        fig = TradeoffLine().generate_figure(
            pretty_data_file=sample_tradeoff_csv,
            y_min=0, y_max=100, default_selection=5
        )
        assert list(fig.layout.yaxis.range) == [0, 100]

    def test_x_axis_range_matches_data(self, sample_tradeoff_csv):
        df = pd.read_csv(sample_tradeoff_csv)
        fig = TradeoffLine().generate_figure(
            pretty_data_file=sample_tradeoff_csv, default_selection=5
        )
        assert fig.layout.xaxis.range[0] == df["model_number"].min()
        assert fig.layout.xaxis.range[1] == df["model_number"].max()

    def test_disable_zoom_fixes_x_axis(self, sample_tradeoff_csv):
        fig = TradeoffLine().generate_figure(
            pretty_data_file=sample_tradeoff_csv,
            disable_zoom=True, default_selection=5
        )
        assert fig.layout.xaxis.fixedrange is True

    def test_anchor_count_matches_model_count(self, sample_tradeoff_csv):
        """There must be exactly one anchor (vertical line) per model."""
        df = pd.read_csv(sample_tradeoff_csv)
        n_models = df["model_number"].nunique()
        fig = TradeoffLine().generate_figure(
            pretty_data_file=sample_tradeoff_csv, default_selection=5
        )
        anchor_count = sum(1 for t in fig.data if t.name == "selected model")
        assert anchor_count == n_models

    def test_anchor_meta_location_is_string(self, sample_tradeoff_csv):
        """JS reads location from meta — must be a string."""
        fig = TradeoffLine().generate_figure(
            pretty_data_file=sample_tradeoff_csv, default_selection=5
        )
        for trace in fig.data:
            if trace.name == "selected model" and trace.meta:
                assert isinstance(trace.meta.get("location"), str)

    def test_default_logging_vars(self):
        assert TradeoffLine().logging_vars["location_var_name"] == "model_number"
