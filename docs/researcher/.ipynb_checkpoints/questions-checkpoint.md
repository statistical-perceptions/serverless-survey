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
import ssbuilder
```

```{code-cell} ipython3
ex_obj = ssbuilder.NormalCurveSlider()
```

```{code-cell} ipython3
ds_list = [l.strip() for l in ex_obj.generate_figure.__doc__.split('\n')]
param_start = ds_list.index('Parameters') +2

param_end = ds_list.index('Returns')
print('\n'.join(ds_list[param_start:param_end]))
```

## Normal Curve Questions

This question has two normal curves, one moves and one does not. 
```{eval-rst}
.. autoclass:: ssbuilder.a

  :members:
```

+++

## Trade Off Questions

this quesiton typ trades off between two two extremes over a number of models in the middle

<!-- example comment -->


```{eval-rst}
.. autoclass:: ssbuilder.TradeoffLine
  :members:
```

```{eval-rst}
.. autoclass:: ssbuilder.TradeoffBar
  :members:
```

##
