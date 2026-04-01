"""
conftest.py — shared pytest fixtures for the ssbuilder test suite
"""
import os
import pytest
import pandas as pd


@pytest.fixture
def tmp_output_dir(tmp_path):
    """A temporary directory for HTML output files."""
    out = tmp_path / "survey_output"
    out.mkdir()
    return out


@pytest.fixture
def sample_tradeoff_csv(tmp_path):
    """
    Minimal CSV suitable for TradeoffBar and TradeoffLine tests.
    Columns: model_number, metric, percent, group
    20 models x 2 groups x 2 metrics
    """
    rows = []
    groups = ["Group A", "Group B"]
    metrics = ["accuracy", "false_positive_rate"]
    for model in range(20):
        for group in groups:
            for metric in metrics:
                rows.append({
                    "model_number": model,
                    "metric": metric,
                    "percent": round(50 + model * 0.5 + (3 if metric == "accuracy" else 0), 1),
                    "group": group,
                })
    df = pd.DataFrame(rows)
    csv_path = tmp_path / "tradeoff_data.csv"
    df.to_csv(csv_path, index=False)
    return str(csv_path)


@pytest.fixture
def sample_instructions_file(tmp_path):
    """
    A fake *-instructions.md file mimicking the output of ssgeneratehtml.

    These are example URLs — calculate_query_length only cares about
    the line format (Sends, Forwards to, Created), not the actual domain.
    """
    content = """\
 ---------------------------
Created: [https://example.github.io/survey/q1.html](https://example.github.io/survey/q1.html)  
Forwards to: https://survey.qualtrics.com/jfe/form/SV_example?  
Sends: ['id', 'loc_q1', 'ov_q1', 'confirm_q1']  

 ---------------------------
Created: [https://example.github.io/survey/q2.html](https://example.github.io/survey/q2.html)  
Forwards to: https://survey.qualtrics.com/jfe/form/SV_example?  
Sends: ['id', 'loc_q1', 'ov_q1', 'confirm_q1', 'loc_q2', 'ov_q2', 'confirm_q2']  
"""
    instructions_path = tmp_path / "test-instructions.md"
    instructions_path.write_text(content)
    return str(instructions_path)


@pytest.fixture
def minimal_yaml_config(tmp_path):
    """
    Writes a minimal 2-question YAML config file and returns its path.
    Uses NormalCurveSlider (no CSV required).
    """
    content = """\
shared:
  figure_type: NormalCurveSlider
  logging_vars:
    location_var_name: loc
    overlap_var_name: ov
  confirm_var_name: confirm
unique:
  - question_id: q1
    next_question_url: q2
  - question_id: q2
    next_question_url: https://survey.qualtrics.com/jfe/form/SV_abc
"""
    config_path = tmp_path / "configuration.yml"
    config_path.write_text(content)
    return str(config_path)


@pytest.fixture
def simple_config_list(tmp_output_dir):
    """
    A plain Python list of 2 question dicts (no shared/unique split).
    """
    return [
        {
            "question_id": "q1",
            "figure_type": "NormalCurveSlider",
            "logging_vars": {"location_var_name": "loc", "overlap_var_name": "ov"},
            "confirm_var_name": "confirm",
            "next_question_url": "q2",
            "out_rel_path": str(tmp_output_dir),
            "out_url": "https://example.github.io/survey",
        },
        {
            "question_id": "q2",
            "figure_type": "NormalCurveSlider",
            "logging_vars": {"location_var_name": "loc", "overlap_var_name": "ov"},
            "confirm_var_name": "confirm",
            "next_question_url": "https://survey.qualtrics.com/jfe/form/SV_abc",
            "out_rel_path": str(tmp_output_dir),
            "out_url": "https://example.github.io/survey",
        },
    ]
