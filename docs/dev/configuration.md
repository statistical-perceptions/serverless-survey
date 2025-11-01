# Configuration Details

`builder.py` automates the building of configured HTML survey pages. The heart of the process being: 
1. **`make_question_page()`** which handles page generation, and 
2. **`generate_from_configuration()`** that handles reading the configuration. 
Pages are designed using preloaded templates via assets, and this is handled by `load_template_file`. 

The remainder of `builder.py` contain the following helper functions, 
3. `set_pass_through`, to handle passing of question parameters. 
4. `get_file_name`, for filename I/O.
5. `expand_shared_params`, for shared configuration of parameters expanded for all the questions, 
6. `question_csv`, for CSV output containing a summary of the whole process. 

See below a breakdown of the two main functions: 


## Page level 

```{eval-rst}
.. automodule:: ssbuilder.builder
   :members: make_question_page
```

## Building from config

```{eval-rst}
.. autoclass:: ssbuilder.generate_from_configuration
  :members:
```

```{eval-rst}
.. automodule:: ssbuilder.builder.generate_from_configuration
  :members:
```


