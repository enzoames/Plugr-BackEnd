from .base import *

# == MUST COMMENT THIS SECTION IF GOING TO PRODUCTION =====

try:
	from .development import *
except:
	pass

# ======


try:
	from .production import *
except:
	pass

