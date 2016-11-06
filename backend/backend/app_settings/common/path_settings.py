from unipath.path import Path

# Django root path where manage.py resides.
BASE_DIR = Path(__file__).ancestor(4)

# The project path which has BASE_DIR, .gitignore, and etc.
PROJECT_DIR = BASE_DIR.parent
