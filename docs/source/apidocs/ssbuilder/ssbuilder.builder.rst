:py:mod:`ssbuilder.builder`
===========================

.. py:module:: ssbuilder.builder

.. autodoc2-docstring:: ssbuilder.builder
   :allowtitles:

Module Contents
---------------

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`load_template_file <ssbuilder.builder.load_template_file>`
     - .. autodoc2-docstring:: ssbuilder.builder.load_template_file
          :summary:
   * - :py:obj:`make_question_page <ssbuilder.builder.make_question_page>`
     - .. autodoc2-docstring:: ssbuilder.builder.make_question_page
          :summary:
   * - :py:obj:`set_pass_through <ssbuilder.builder.set_pass_through>`
     - .. autodoc2-docstring:: ssbuilder.builder.set_pass_through
          :summary:
   * - :py:obj:`get_file_name <ssbuilder.builder.get_file_name>`
     - .. autodoc2-docstring:: ssbuilder.builder.get_file_name
          :summary:
   * - :py:obj:`expand_shared_params <ssbuilder.builder.expand_shared_params>`
     - .. autodoc2-docstring:: ssbuilder.builder.expand_shared_params
          :summary:
   * - :py:obj:`generate_from_configuration <ssbuilder.builder.generate_from_configuration>`
     - .. autodoc2-docstring:: ssbuilder.builder.generate_from_configuration
          :summary:
   * - :py:obj:`question_csv <ssbuilder.builder.question_csv>`
     - .. autodoc2-docstring:: ssbuilder.builder.question_csv
          :summary:

Data
~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`figure_classes <ssbuilder.builder.figure_classes>`
     - .. autodoc2-docstring:: ssbuilder.builder.figure_classes
          :summary:
   * - :py:obj:`instruction_template_log <ssbuilder.builder.instruction_template_log>`
     - .. autodoc2-docstring:: ssbuilder.builder.instruction_template_log
          :summary:
   * - :py:obj:`instruction_template_minimal <ssbuilder.builder.instruction_template_minimal>`
     - .. autodoc2-docstring:: ssbuilder.builder.instruction_template_minimal
          :summary:
   * - :py:obj:`instruction_template_forward <ssbuilder.builder.instruction_template_forward>`
     - .. autodoc2-docstring:: ssbuilder.builder.instruction_template_forward
          :summary:
   * - :py:obj:`instructions_template <ssbuilder.builder.instructions_template>`
     - .. autodoc2-docstring:: ssbuilder.builder.instructions_template
          :summary:

API
~~~

.. py:data:: figure_classes
   :canonical: ssbuilder.builder.figure_classes
   :value: None

   .. autodoc2-docstring:: ssbuilder.builder.figure_classes

.. py:function:: load_template_file(*args)
   :canonical: ssbuilder.builder.load_template_file

   .. autodoc2-docstring:: ssbuilder.builder.load_template_file

.. py:data:: instruction_template_log
   :canonical: ssbuilder.builder.instruction_template_log
   :value: <Multiline-String>

   .. autodoc2-docstring:: ssbuilder.builder.instruction_template_log

.. py:data:: instruction_template_minimal
   :canonical: ssbuilder.builder.instruction_template_minimal
   :value: <Multiline-String>

   .. autodoc2-docstring:: ssbuilder.builder.instruction_template_minimal

.. py:data:: instruction_template_forward
   :canonical: ssbuilder.builder.instruction_template_forward
   :value: <Multiline-String>

   .. autodoc2-docstring:: ssbuilder.builder.instruction_template_forward

.. py:data:: instructions_template
   :canonical: ssbuilder.builder.instructions_template
   :value: None

   .. autodoc2-docstring:: ssbuilder.builder.instructions_template

.. py:function:: make_question_page(question_id, figure_type='NormalCurveSlider', figure_values=None, page_title='Normal Curve Question', question_text='Move the slider', confirm_message='Confirm my answer', skip_message='Prefer not to answer', button_text='Submit', out_html_file=None, out_rel_path=None, logging_vars=None, confirm_var_name=None, var_name_suffix=True, pretty_url=False, pass_through_vars=['id'], out_url=None, next_question_url=None, debug=False, full_html=True, footer_type='confirm_submit', instructions_type='log', forward_type=None)
   :canonical: ssbuilder.builder.make_question_page

   .. autodoc2-docstring:: ssbuilder.builder.make_question_page

.. py:function:: set_pass_through(config_dict_list, study_default_pt_vars=['id'], debug=False)
   :canonical: ssbuilder.builder.set_pass_through

   .. autodoc2-docstring:: ssbuilder.builder.set_pass_through

.. py:function:: get_file_name(question_dict=None, out_html_file=None, question_id=None)
   :canonical: ssbuilder.builder.get_file_name

   .. autodoc2-docstring:: ssbuilder.builder.get_file_name

.. py:function:: expand_shared_params(loaded_config, debug=False)
   :canonical: ssbuilder.builder.expand_shared_params

   .. autodoc2-docstring:: ssbuilder.builder.expand_shared_params

.. py:function:: generate_from_configuration(config_file=None, repo_name=None, gh_org=None, out_url=None, debug=False, out_rel_path='', fragment=False, all_in_one=False, study_pass_through_vars=['id'], instructions_type='log')
   :canonical: ssbuilder.builder.generate_from_configuration

   .. autodoc2-docstring:: ssbuilder.builder.generate_from_configuration

.. py:function:: question_csv(config_file=None, metadata=None, debug=False)
   :canonical: ssbuilder.builder.question_csv

   .. autodoc2-docstring:: ssbuilder.builder.question_csv
