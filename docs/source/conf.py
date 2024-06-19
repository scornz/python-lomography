# Configuration file for the Sphinx documentation builder.

import os
import sys

sys.path.insert(0, os.path.abspath("../../lomography"))

# -- Project information

project = "python-lomography"
copyright = "2024, Mike Scornavacca"
author = "Mike Scornavacca"

release = "1.0.0"
version = "1.0.0"

# -- General configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = ["_templates"]

# -- Options for HTML output

html_theme = "sphinx_rtd_theme"

# -- Options for EPUB output
epub_show_urls = "footnote"

# -- Show both init function and class documentation
autoclass_content = "both"
