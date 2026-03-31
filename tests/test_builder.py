"""
test_builder.py — basic tests for builder.py
"""
import pytest

from ssbuilder.builder import (
    get_file_name,
    expand_shared_params,
    set_pass_through,
    make_question_page,
)


# get_file_name

class TestGetFileName:

    def test_returns_html_extension(self):
        assert get_file_name(question_id="q1").endswith(".html")

    def test_output_is_lowercase(self):
        result = get_file_name(question_id="MyQuestion")
        assert result == result.lower()

    def test_spaces_replaced_with_dashes(self):
        result = get_file_name(out_html_file="my file.html", question_id="x")
        assert " " not in result

    def test_strips_slashes(self):
        result = get_file_name(question_id="a/b")
        assert "/" not in result


# expand_shared_params

class TestExpandSharedParams:

    def _cfg(self, shared, unique):
        return {"shared": shared, "unique": unique}

    def test_shared_key_appears_in_every_question(self):
        cfg = self._cfg(
            shared={"figure_type": "NormalCurveSlider"},
            unique=[{"question_id": "q1"}, {"question_id": "q2"}],
        )
        result = expand_shared_params(cfg)
        assert all(r["figure_type"] == "NormalCurveSlider" for r in result)

    def test_unique_overrides_shared(self):
        cfg = self._cfg(
            shared={"figure_type": "NormalCurveSlider"},
            unique=[{"question_id": "q1", "figure_type": "TradeoffBar"}],
        )
        assert expand_shared_params(cfg)[0]["figure_type"] == "TradeoffBar"

    def test_empty_unique_returns_empty_list(self):
        cfg = self._cfg(shared={"figure_type": "NormalCurveSlider"}, unique=[])
        assert expand_shared_params(cfg) == []


# set_pass_through

class TestSetPassThrough:

    def _q(self, qid, next_url=None):
        q = {
            "question_id": qid,
            "figure_type": "NormalCurveSlider",
            "logging_vars": {"location_var_name": "loc", "overlap_var_name": "ov"},
            "confirm_var_name": "confirm",
        }
        if next_url:
            q["next_question_url"] = next_url
        return q

    def test_id_always_in_pass_through(self):
        result = set_pass_through([self._q("q1", next_url="https://qualtrics.com/done")])
        assert "id" in result[0]["pass_through_vars"]

    def test_internal_forward_type(self):
        config = [self._q("q1", next_url="q2"), self._q("q2", next_url="https://qualtrics.com/done")]
        result = set_pass_through(config)
        assert result[0]["forward_type"] == "internal"

    def test_external_forward_type(self):
        result = set_pass_through([self._q("q1", next_url="https://qualtrics.com/done")])
        assert result[0]["forward_type"] == "external"

    def test_vars_accumulate_across_chain(self):
        config = [
            self._q("q1", next_url="q2"),
            self._q("q2", next_url="https://qualtrics.com/done"),
        ]
        result = set_pass_through(config)
        q2_ptv = result[1]["pass_through_vars"]
        assert any("q1" in v for v in q2_ptv)

    def test_missing_next_url_defaults_to_end_html(self):
        result = set_pass_through([self._q("q1")])
        assert result[0]["next_question_url"] == "end.html"


# make_question_page

class TestMakeQuestionPage:

    def test_html_file_created(self, tmp_output_dir):
        make_question_page(
            question_id="q1",
            figure_type="InstructionQuestion",
            question_text="Hello.",
            out_rel_path=str(tmp_output_dir),
            next_question_url="end.html",
            out_url="https://example.com",
        )
        assert (tmp_output_dir / "q1.html").exists()

    def test_output_contains_html_tag(self, tmp_output_dir):
        make_question_page(
            question_id="q2",
            figure_type="InstructionQuestion",
            question_text="Hello.",
            out_rel_path=str(tmp_output_dir),
            next_question_url="end.html",
            out_url="https://example.com",
        )
        html = (tmp_output_dir / "q2.html").read_text()
        assert "<html" in html.lower()

    def test_question_text_in_output(self, tmp_output_dir):
        make_question_page(
            question_id="q3",
            figure_type="InstructionQuestion",
            question_text="UniqueTextXYZ",
            out_rel_path=str(tmp_output_dir),
            next_question_url="end.html",
            out_url="https://example.com",
        )
        assert "UniqueTextXYZ" in (tmp_output_dir / "q3.html").read_text()

    def test_chart_page_includes_plotly(self, tmp_output_dir):
        make_question_page(
            question_id="q4",
            figure_type="NormalCurveSlider",
            out_rel_path=str(tmp_output_dir),
            next_question_url="end.html",
            out_url="https://example.com",
        )
        assert "plotly" in (tmp_output_dir / "q4.html").read_text().lower()
