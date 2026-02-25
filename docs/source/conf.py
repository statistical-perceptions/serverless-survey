# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Serverless Survey'
copyright = '2026,  Sarah M Brown'
author = ' Sarah M Brown'
release = '0.3.7'


import os
import sys
sys.path.insert(0, os.path.abspath('../../ssbuilder/'))

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    'autodoc2',
    'sphinx.ext.intersphinx',
    "sphinx_design",
    'sphinx.ext.napoleon',
    'sphinx_click'
]
#  "myst_nb",
    # 'sphinx.ext.autodoc',
autodoc2_packages = [
    "../my_package",
]

templates_path = ['_templates']
exclude_patterns = ["README.md", 'demobench/*', 'build/*',
                     '_build', 'Thumbs.db', "*import_posts*"]



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'

html_theme_options = {
  "show_nav_level": 2,
   "show_toc_level": 2,
  "header_links_before_dropdown": 6,
  "icon_links": [ 
        {
            "name": "GitHub",
            "url": "https://github.com/statistical-perceptions/serverless-survey",
            "icon": "fa-brands fa-github",
        }]
        ,
  "secondary_sidebar_items": {
        "**/*": ["page-toc", "edit-this-page", "sourcelink"],
    }
}


# MyST config
myst_enable_extensions = [
    # "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    # "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    # "tasklist",
]

# html_favicon = "_static/favicon.ico"
#  change this to change the site title
html_title = project

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
# html_extra_path = ["feed.xml"]
# map pages to which sidebar they should have
#  "page_file_name": ["list.html", "of.html", "sidebar.html", "files.html"]
html_sidebars = {
    "*": [],
    "**/*": ["sidebar-nav-bs",]
}
