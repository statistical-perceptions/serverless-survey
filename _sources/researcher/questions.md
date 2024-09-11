---
jupytext:
  formats: md:myst,ipynb
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.4
kernelspec:
  display_name: Python 3 (ipykernel)
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
:tags: [remove-input]

import ssbuilder
# import markdown
from IPython.display import display, Markdown
```

## Normal Curve Questions

This question has two normal curves, one moves and one does not. 

### Example

````{margin}
```{note}
All example figures on this page are done with defaults which are visible on the [developer page](../dev/questions.md)
```
````

```{code-cell} ipython3
:tags: [remove-input]

ssbuilder.NormalCurveSlider().generate_figure()
```

### Settings 

Use `figure_type: NormalCurveSlider` with the following parameters in `figure_values`

```{code-cell} ipython3
:tags: [remove-input]

Markdown(ssbuilder.md_params(ssbuilder.NormalCurveSlider().generate_figure))
```

## Tradeoff Questions

this question type trades off between two two extremes over a number of models in the middle

Both formats accept the same dataset files, where each  row represents one bar heigh for one slider location. 
The values should be compatible with deisplay in the figures, for example converting .74 to 75 to display percentages. There may be extra columns that are not used. 

An example (that is used in the example plots):

```{code-cell} ipython3
:tags: [remove-input]

import pandas as pd
df = pd.read_csv('../_examples/tall_pretty.csv')
df.head()
```

### Line Graph Tradeoff 

This uses lines to show all metrics on one set of axes. 

#### Example

```{code-cell} ipython3
:tags: [remove-input]

ssbuilder.TradeoffLine().generate_figure(pretty_data_file='../_examples/tall_pretty.csv',default_selection=40)
```

#### Settings
Use `figure_type: TradeoffLine` with the following parameters for use in `figure_values`:

```{code-cell} ipython3
:tags: [remove-input]

Markdown(ssbuilder.md_params(ssbuilder.TradeoffLine().generate_figure))
```

<!-- edit in docstring -->
### Bar Graph Tradeoff 

This uses a set of bar graphs.

#### Example

```{code-cell} ipython3
:tags: [remove-input]

ssbuilder.TradeoffBar().generate_figure(pretty_data_file='../_examples/tall_pretty.csv',default_selection=18)
```

#### Settings
Use `figure_type: TradeoffBar` with the following parameters for use in `figure_values`

```{code-cell} ipython3
:tags: [remove-input]

Markdown(ssbuilder.md_params(ssbuilder.TradeoffBar().generate_figure))
```

```{code-cell} ipython3

```

```{code-cell} ipython3

```
