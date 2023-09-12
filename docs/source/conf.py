# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../../sparrow'))

# -- Project information -----------------------------------------------------

project = 'GBT Docs'
copyright = '2023, A. Schmiedeke'
author = 'A. Schmiedeke'

# The full version, including alpha/beta/rc tags
release = '0.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.todo',
              'sphinx.ext.autodoc',
              'sphinx.ext.coverage',
              'sphinx.ext.napoleon',
              'sphinx.ext.autosummary',
              'sphinx.ext.mathjax', 
              'sphinx.ext.intersphinx', 
              'sphinx_design',
              'sphinx_copybutton',
              'sphinx_inline_tabs',
              'hoverxref.extension',
              #'sphinx_idl.domain', 
              #'sphinx_idl.auto'
]

autosummary_generate = False
add_module_names=False
toc_object_entries_show_parents = 'hide'

todo_include_todos = True

intersphinx_mapping = {
        'dysh': ("https://dysh.readthedocs.io/en/latest", None)
}

# We recommend adding the following config value.
# Sphinx defaults to automatically resolve *unresolved* labels using all your Intersphinx mappings.
# This behavior has unintended side-effects, namely that documentations local references can
# suddenly resolve to an external location.
# See also:
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#confval-intersphinx_disabled_reftypes
intersphinx_disabled_reftypes = ["*"]


hoverxref_api_host = 'https://readthedocs.org'
hoverxref_auto_ref = True
hoverxref_domains = ["py"]
hoverxref_roles = [
    "option",
    # Documentation pages
    # Not supported yet: https://github.com/readthedocs/sphinx-hoverxref/issues/18
    "doc",
    # Glossary terms
    "term",
]
hoverxref_role_types = {
    "mod": "modal",  # for Python Sphinx Domain
    "doc": "modal",  # for whole docs
    "class": "tooltip",  # for Python Sphinx Domain
    "ref": "tooltip",  # for hoverxref_auto_ref config
    "confval": "tooltip",  # for custom object
    "term": "tooltip",  # for glossaries
}

hoverxref_intersphinx = [
        "dysh"
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


#I was trying to get the color part working, but it is not.
rst_prolog = """
.. include:: <s5defs.txt>

"""




# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'
html_theme = 'furo'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static', '_assets']

html_css_files = [
    'css/custom.css',
]

html_theme_options = {
        "announcement": "The GBT is currently offline for maintenance and expected to return to full operations by the end of September.",
        "dark_css_variables": {"color-announcement-background": "darkred"},
        "light_css_variables": {"color-announcement-background": "darkred"},

    }



# -- Options for latexpdf output ---------------------------------------------

latex_use_parts=True

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, document class [howto/manual]).
#latex_documents = [
#  ('tutorials', 'Tutorials.tex', ur'GBTdocs Tutorials', ur'The GBTdocs Team', 'manual', False),
#  ]
#
#  ('how-tos', 'HowToGuides.tex', ur'GBTdocs How-To Guides', ur'The GBTdocs Team', 'manual', False),
#  ('references', 'ReferenceGuides.tex', ur'GBTdocs Reference Guides', ur'The GBTdocs Team', 'manual', False),
#  ('explanations', 'ExplanationGuides.tex', ur'GBTdocs Explanation Guides', ur'The GBTdocs Team', 'manual', False),
#]
