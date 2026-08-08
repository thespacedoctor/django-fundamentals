import datetime

from django_fundamentals.__version__ import __version__

project = "django-fundamentals"
copyright = f"{datetime.date.today().year}, David R. Young"
author = "David R. Young"
release = __version__
version = __version__

extensions = [
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_inline_tabs",
]

myst_enable_extensions = ["colon_fence", "deflist"]
source_suffix = {".md": "markdown", ".rst": "restructuredtext"}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "furo"
html_static_path = ["_static"]
