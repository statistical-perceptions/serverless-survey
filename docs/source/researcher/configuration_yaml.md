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


## YAML Format

There are two supported formats for the configuration file:
- [no shared parameters](#noshare) where all settings for the question are set individually for every question
- [shared parameters](#shared), where some settings are set once for all questions and applied to all questions. 


All yaml files are like: 

```
key: value
```
where:
- the `key` will be an option name for either building or question type sepecific
- `value` is your chosen value. 
- The keys need to be unique. 
- keys should not have spaces in them, but values can be more complex

Yaml creates lists by starting a line with `- ` an then tabbing over all items that are related. In `ss` our lists have the same structure so each group that starts with `- ` woud have the same keys in it. 

```
- id: identifier_q1
  property: val for property in q1 
- id: identifier_q2
  property: val for property in q2 
```
not that in each group of lines with a `-` the keys are unique but they can repeat in the list. 


items can be nested
```
item_with_subparts:
  subpart1: val sub 1
  subpart2: val sub 2
```

and long values can go on a new line for readability
```
key_with_long_value: |
  long value first line
  long value second line
  long value third line
```

(noshare)=
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
- any variables not specified will get the default value as stated in the documentation
- `figure_values` is a special variable that takes more variables.  the names of the fig variables are defined for each question
- the variables can be in any order
- `question_id` must be stated, there is no default value for it 
- only the first variable for each question gets a `-`
- `name_of_var3_for_q2` is an example of how to format a long value if you do not leave it on a single line. 

Some come from the question and others are for the pate

(shared)=
### Shared parameters 

To share values across question it can be set up so that the top level is a single entry with two keys (`shared` and `unique`) where the `shared` key includes the parameter values that are to be applied to all questiona and `unique` includes a list defining individiual questions as above.  Any values defined in both, the `unique` will overwrite the `shared` value.  


For example: 
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

This is equivalent to (but, for large number of questions,  more compact than):

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

## Configuration Options

::::{attention} Prerequisite
To configure the study you will need the urls to each follow-up survey. They do not have to be fully configured, but you need to create them so that you can get the URL for each.  
::::::

Each question is a single page with a figure on it. There are some configurations to the overall page and some for the plot itself. 

### Page level  Settings

These settings control the rest of the question page, other than the figure. 

```{code-cell} ipython3
:tags: ["remove-input"]
import ssbuilder
# import markdown
from IPython.display import Markdown

Markdown(ssbuilder.md_params(ssbuilder.builder.make_question_page))
```

:::{warning}
You cannot use `end` as a question ID, or `end.html` as an output file name
::::

### Question Text

Questions' text goes in the page level parameter `question_text`. It may include markdown formatting to be rendered.  

Some key examples:
- `**bold**`
- `*italic*`
- `- bulleted text`
- `[link display text](url/for/link)`
- a blank space at the end of aline will make a new paragraph


### Figure specific Settings

These settings vary by question type and the options are detailed on [](questions.md)

## Build Level Options

Serverless Survey has some settings that are for a whole study or about how to process the configuration file. 

These are set as CLI arguments if you build offline.  If you use our template repo, you will have a set of options for these controls in your actions tab.  

This is where the path to save the output html files are set as well as the url of the hosted site for generating the instructions. There is also the option to generate only a fragment or to put all questions on a single page (eg for IRB review or paper supplemental materials). 

```{code-cell} ipython3
%%bash
ssgeneratehtml --help
```

