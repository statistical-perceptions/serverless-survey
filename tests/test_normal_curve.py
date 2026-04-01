"""
test_normal_curve.py — basic tests for NormalCurveSlider
"""
import pytest
import plotly.graph_objects as go

from ssbuilder.single_normal_curve import NormalCurveSlider


class TestNormalCurveSlider:

    def test_returns_plotly_figure(self):
        fig = NormalCurveSlider().generate_figure()
        assert isinstance(fig, go.Figure)

    def test_trace_count_matches_slider_locs(self):
        # 1 static trace + num_slider_locs dynamic traces
        fig = NormalCurveSlider().generate_figure(num_slider_locs=50)
        assert len(fig.data) == 1 + 50

    def test_slider_present(self):
        fig = NormalCurveSlider().generate_figure()
        assert len(fig.layout.sliders) >= 1

    def test_static_color_applied(self):
        fig = NormalCurveSlider().generate_figure(static_color="#FF0000")
        assert fig.data[0].line.color == "#FF0000"

    def test_dynamic_color_applied(self):
        fig = NormalCurveSlider().generate_figure(dynamic_color="#00FF00")
        assert all(t.line.color == "#00FF00" for t in fig.data[1:])

    def test_overlap_values_within_0_and_100(self):
        """Overlap percentage must be a valid probability (0-100)."""
        fig = NormalCurveSlider().generate_figure()
        for trace in fig.data[1:]:
            if trace.meta and "overlap" in trace.meta:
                assert 0.0 <= float(trace.meta["overlap"]) <= 100.0

    def test_overlap_meta_is_string(self):
        """JS reads overlap as a string — Python must encode it as one."""
        fig = NormalCurveSlider().generate_figure()
        for trace in fig.data[1:]:
            if trace.meta and "overlap" in trace.meta:
                assert isinstance(trace.meta["overlap"], str)

    def test_location_meta_is_string(self):
        """JS reads location as a string — Python must encode it as one."""
        fig = NormalCurveSlider().generate_figure()
        for trace in fig.data[1:]:
            if trace.meta and "location" in trace.meta:
                assert isinstance(trace.meta["location"], str)

    def test_overlap_higher_when_curves_are_close(self):
        """Core math check: overlap should be higher when means are similar."""
        static_mean = 50
        fig_close = NormalCurveSlider().generate_figure(
            static_mean=static_mean, dynamic_starting_mean=static_mean
        )
        fig_far = NormalCurveSlider().generate_figure(
            static_mean=static_mean, dynamic_starting_mean=0
        )
        # data[0] is static (no meta); dynamic traces start at data[1]
        overlap_close = float(fig_close.data[static_mean].meta["overlap"])
        overlap_far = float(fig_far.data[1].meta["overlap"])
        assert overlap_close > overlap_far

    def test_xaxis_title_applied(self):
        fig = NormalCurveSlider().generate_figure(xaxis_title="Income")
        assert fig.layout.xaxis.title.text == "Income"

    def test_default_logging_vars(self):
        ncs = NormalCurveSlider()
        assert ncs.logging_vars["location_var_name"] == "loc"
        assert ncs.logging_vars["overlap_var_name"] == "ov"
