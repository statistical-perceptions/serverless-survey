:py:mod:`ssbuilder.utils`
=========================

.. py:module:: ssbuilder.utils

.. autodoc2-docstring:: ssbuilder.utils
   :allowtitles:

Module Contents
---------------

Functions
~~~~~~~~~

.. list-table::
   :class: autosummary longtable
   :align: left

   * - :py:obj:`md_params <ssbuilder.utils.md_params>`
     - .. autodoc2-docstring:: ssbuilder.utils.md_params
          :summary:
   * - :py:obj:`check_query_length <ssbuilder.utils.check_query_length>`
     - .. autodoc2-docstring:: ssbuilder.utils.check_query_length
          :summary:
   * - :py:obj:`calculate_query_length <ssbuilder.utils.calculate_query_length>`
     - .. autodoc2-docstring:: ssbuilder.utils.calculate_query_length
          :summary:
   * - :py:obj:`cmd_merge_dir_csvs <ssbuilder.utils.cmd_merge_dir_csvs>`
     - .. autodoc2-docstring:: ssbuilder.utils.cmd_merge_dir_csvs
          :summary:
   * - :py:obj:`merge_dir_csvs <ssbuilder.utils.merge_dir_csvs>`
     - .. autodoc2-docstring:: ssbuilder.utils.merge_dir_csvs
          :summary:

API
~~~

.. py:function:: md_params(function)
   :canonical: ssbuilder.utils.md_params

   .. autodoc2-docstring:: ssbuilder.utils.md_params

.. py:function:: check_query_length(filename, vars_only=False, id_length=10, value_length=3, exclude_base=False)
   :canonical: ssbuilder.utils.check_query_length

   .. autodoc2-docstring:: ssbuilder.utils.check_query_length

.. py:function:: calculate_query_length(filename, vars_only=False, id_length=10, value_length=3, exclude_base=False)
   :canonical: ssbuilder.utils.calculate_query_length

   .. autodoc2-docstring:: ssbuilder.utils.calculate_query_length

.. py:function:: cmd_merge_dir_csvs(folder, merge_on, out_name, header, verbose, skip_row, complete_only)
   :canonical: ssbuilder.utils.cmd_merge_dir_csvs

   .. autodoc2-docstring:: ssbuilder.utils.cmd_merge_dir_csvs

.. py:function:: merge_dir_csvs(folder, merge_on='id', out_name=None, header=0, verbose=False, skip_row=None, complete_only=False)
   :canonical: ssbuilder.utils.merge_dir_csvs

   .. autodoc2-docstring:: ssbuilder.utils.merge_dir_csvs
