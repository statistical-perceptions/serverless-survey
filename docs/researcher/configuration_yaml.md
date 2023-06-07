# Working with Configuration Files

A configuration file is yaml


## Configuring your study 

To configure the study you will need the urls to each follow-up survey. They do not have to be fully configured first though. 

### Editing on GitHub.com

If you do not want to run the code locally you can instead edit configuration file here only. 

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
- `name_of_var3_for_q2` is an example of how to format a long variable if you do not leave it on a single line. 

Some come from the question and others are for the pate

## Page level  Settings

```{eval-rst}
.. autoclass:: ssbuilder.builder.make_question_page
  :members:
```

## Building from config

```{eval-rst}
.. autoclass:: ssbuilder.generate_from_configuration
  :members:
```

