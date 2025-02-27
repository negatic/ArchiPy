# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'ArchiPy'
copyright = '2024, Mehdi Einali, Hossein Nejati'
author = 'Mehdi Einali, Hossein Nejati'
version = '0.1.0'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.coverage',
    'sphinx.ext.todo',
    'sphinx.ext.autosummary',

]

# AutoAPI settings for better code extraction
autoapi_type = 'python'
autoapi_dirs = ['../../archipy']
autoapi_options = [
    'members',
    'undoc-members',
    'private-members',
    'special-members',
    'inherited-members',
    'show-inheritance',
    'show-module-summary',
    'imported-members',
]
autoapi_python_class_content = 'both'
autoapi_member_order = 'groupwise'
autoapi_add_toctree_entry = False  # We'll handle this in our own index

templates_path = ['_templates']
exclude_patterns = []

# -- Options for autodoc -----------------------------------------------------
autodoc_member_order = 'bysource'
autodoc_typehints = 'description'
autoclass_content = 'both'
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    # 'special-members': True,
    # 'inherited-members': True,
    # 'show-inheritance': True,
    # 'undoc-members': True,

}

# Enable auto-summary generation
autosummary_generate = True

# Include __init__ method docstring in class docstring
autoclass_content = 'both'

# Enable todos
todo_include_todos = True

# Inheritance diagrams
inheritance_graph_attrs = dict(rankdir="TB", size='"12.0, 12.0"', fontsize=14, ratio='compress')
inheritance_node_attrs = dict(shape='rect', fontsize=14, height=0.75, margin='"0.08, 0.05"')

# Enable documenting typehints
autodoc_typehints = 'description'
typehints_fully_qualified = False
always_document_param_types = True

# -- Options for napoleon ----------------------------------------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_use_keyword = True
napoleon_custom_sections = None

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_logo = None
html_favicon = None
html_title = f"{project} {version} Documentation"
html_short_title = project

# -- Options for intersphinx -------------------------------------------------
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'sqlalchemy': ('https://docs.sqlalchemy.org/en/14/', None),
    'pydantic': ('https://docs.pydantic.dev/', None),
}

# -- Options for autosectionlabel --------------------------------------------
autosectionlabel_prefix_document = True

# -- Options for viewcode ----------------------------------------------------
viewcode_enable_epub = False

# -- Options for LaTeX output ------------------------------------------------
latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '11pt',
    'preamble': '',
    'figure_align': 'htbp',
}

# Define master_doc (the main document)
master_doc = 'index'

latex_documents = [
    (master_doc, 'ArchiPy.tex', 'ArchiPy Documentation',
     author, 'manual'),
]