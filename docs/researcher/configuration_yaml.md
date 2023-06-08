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

# Working with Configuration Files

A configuration file is yaml


## How YAML works 


### No shared parameters 


This file is setup like: 
```
- question_id: unique_id_for_q1
  name_of_var1_for_q1: value_for_var1_q1
  name_of_var2_for_q1: value_for_var2_q1
  figure_values:
    name_of_fig_var1_for_q1: value_for_fig_var1_for_q1
- question_id: unique_id_for_q2
  name_of_var1_for_q2: value_for_var1_q2
  name_of_var3_for_q2: value_for_var3_q2
  name_of_var3_for_q2: |
        value_for_var3_q2_line_1
        value_for_var3_q2_line_3
        value_for_var3_q2_line_3
  figure_values:
    name_of_fig_var1_for_q2: value_for_fig_var1_for_q2
```

Notes: 
- Each `name_of_varX_for_qY` has to be a variable that the `make_question_page` function accepts
- reference for the functions is at the top of the notebook
- any variables not specified will get the default value as stated inthe documentation
- `figure_values` is a special variable that takes more variables.  the nams of the fig variables are the ones for the `normal_curve_slider` function
- the variables can be in any order
- `question_id` must be stated, there is no default value for it 
- only the first variable for each question gets a `-`
- `name_of_var3_for_q2` is an example of how to format a long value if you do not leave it on a single line. 

Some come from the question and others are for the pate

### No shared parameters 

To share values across question it can be set up like
```
shared: 
  name_of_var1_shared: value_for_var1_shared
  name_of_var2_shared: value_for_var2_shared
  figure_values:
    name_of_fig_var2_shared: value_for_fig_var2_shared
unique: 
- question_id: unique_id_for_q1
  name_of_var4_for_q1: value_for_var4_q1
  figure_values:
    name_of_fig_var1_for_q1: value_for_fig_var1_for_q1
- question_id: unique_id_for_q2
  name_of_var4_for_q2: value_for_var4_q2
  figure_values:
    name_of_fig_var1_for_q2: value_for_fig_var1_for_q2
```

This is equivalent to (but, for many questions,  more compact than)

```
- question_id: unique_id_for_q1
  name_of_var4_for_q1: value_for_var4_q1
  name_of_var1_shared: value_for_var1_shared
  name_of_var2_shared: value_for_var2_shared
  figure_values:
    name_of_fig_var2_shared: value_for_fig_var2_shared
    name_of_fig_var1_for_q1: value_for_fig_var1_for_q1
- question_id: unique_id_for_q2
  name_of_var4_for_q2: value_for_var4_q2
  name_of_var1_shared: value_for_var1_shared
  name_of_var2_shared: value_for_var2_shared
  figure_values:
    name_of_fig_var2_shared: value_for_fig_var2_shared
    name_of_fig_var1_for_q2: value_for_fig_var1_for_q2
```

## Configuring your study 

To configure the study you will need the urls to each follow-up survey. They do not have to be fully configured first though. 

### Page level  Settings

```{code-cell} ipython3
:tags: ["remove-input"]
import ssbuilder
# import markdown
from IPython.display import Markdown

Markdown(ssbuilder.md_params(ssbuilder.builder.make_question_page))
```

### Figure specific Settings

These settings vary by question type and the options are detailed on [](questions.md)

## Building Level Options

```{code-cell} ipython3
%%bash
ssgeneratehtml --help
```

