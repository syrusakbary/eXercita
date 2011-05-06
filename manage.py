import os
import sys
ROOT_PATH = os.path.dirname(__file__)

sys.path.append(ROOT_PATH)
sys.path.append(os.path.join(ROOT_PATH,'website/'))

import website.settings as settings
from django.core.management import execute_manager

execute_manager(settings)
