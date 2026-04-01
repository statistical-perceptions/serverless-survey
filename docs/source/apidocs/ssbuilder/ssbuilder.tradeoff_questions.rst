:py:mod:`ssbuilder.tradeoff_questions`
======================================

.. py:module:: ssbuilder.tradeoff_questions

.. autodoc2-docstring:: ssbuilder.tradeoff_questions
   :allowtitles:

Module Contents
---------------

Classes
~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`TradeoffBar <ssbuilder.tradeoff_questions.TradeoffBar>`
     - .. autodoc2-docstring:: ssbuilder.tradeoff_questions.TradeoffBar
          :summary:
   * - :py:obj:`TradeoffLine <ssbuilder.tradeoff_questions.TradeoffLine>`
     - .. autodoc2-docstring:: ssbuilder.tradeoff_questions.TradeoffLine
          :summary:

API
~~~

.. py:class:: TradeoffBar(logging_vars={'location_var_name': 'model_number'})
   :canonical: ssbuilder.tradeoff_questions.TradeoffBar

   .. autodoc2-docstring:: ssbuilder.tradeoff_questions.TradeoffBar

   .. rubric:: Initialization

   .. autodoc2-docstring:: ssbuilder.tradeoff_questions.TradeoffBar.__init__

   .. py:method:: generate_figure(pretty_data_file, slider_column='model_number', slider_label='Model', x_col='metric', x_value1='accuracy', x_value1_hover='accurate', x_value2='false_positive_rate', x_value2_hover='false positives', y_col='percent', y_min=None, y_max=None, num_digits=1, color_col='group', color_hover='people', disable_zoom=True, default_selection=10)
      :canonical: ssbuilder.tradeoff_questions.TradeoffBar.generate_figure

      .. autodoc2-docstring:: ssbuilder.tradeoff_questions.TradeoffBar.generate_figure

.. py:class:: TradeoffLine(logging_vars={'location_var_name': 'model_number'})
   :canonical: ssbuilder.tradeoff_questions.TradeoffLine

   .. autodoc2-docstring:: ssbuilder.tradeoff_questions.TradeoffLine

   .. rubric:: Initialization

   .. autodoc2-docstring:: ssbuilder.tradeoff_questions.TradeoffLine.__init__

   .. py:method:: generate_figure(pretty_data_file, slider_label='Model', trace_col='metric', x_col='model_number', trace_value1='accuracy', trace1_hover='accurate', trace_value2='false_positive_rate', trace2_hover='false positives', y_col='percent', y_min=None, y_max=None, num_digits=2, color_col='group', color_hover='people', anchor_name='selected model', disable_zoom=True, default_selection=10)
      :canonical: ssbuilder.tradeoff_questions.TradeoffLine.generate_figure

      .. autodoc2-docstring:: ssbuilder.tradeoff_questions.TradeoffLine.generate_figure
