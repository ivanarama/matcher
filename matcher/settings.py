INSTALLED_APPS = [
    ...
    "rest_framework",
    "api",
]

import os
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")