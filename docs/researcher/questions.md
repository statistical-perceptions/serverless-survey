---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.1
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Question Types 

```{admonition} Question Implementation
:class: developer, dropdown

Each question type is implemented as a class the class also specifies the HTML/js templates to use for that question type. The constructor documents the logging variables that can be passed.  See more on [](dev/questions)
```

All questions must have certain parameters:
- `question_text`
- `question_id`

the `question_text` can include markdown formatting which will be rendered with the [markdown](https://pypi.org/project/Markdown/) package

```{code-cell} ipython3
:tags: ["remove-input"]
import ssbuilder
# import markdown
from IPython.display import Markdown
```

## Normal Curve Questions

This question has two normal curves, one moves and one does not. 

Use `figure_type: NormalCurveSlider` with the following parameters in `figure_values`
```{code-cell} ipython3
:tags: ["remove-input"]
Markdown(ssbuilder.md_params(ssbuilder.NormalCurveSlider().generate_figure))
```

## Trade Off Questions



this question type trades off between two two extremes over a number of models in the middle

### Line Graph

Use `figure_type: TradeoffLine` with the following parameters for use in `figure_values`:
```{code-cell} ipython3
:tags: ["remove-input"]
Markdown(ssbuilder.md_params(ssbuilder.TradeoffLine().generate_figure))
```
<!-- edit in docstring -->
### Bar Graph

Use `figure_type: TradeoffBar` with the following parameters for use in `figure_values`

```{code-cell} ipython3
:tags: ["remove-input"]
Markdown(ssbuilder.md_params(ssbuilder.TradeoffBar().generate_figure))
```

