import os
import imp

_config_file = os.environ.get('SBCSWEBSITE_CONFIG', None) or os.path.join(os.getcwd(), "sbcswebsite_config.py")
print _config_file
if not os.path.exists(_config_file):
	raise Exception("Cannot find config file at {0}".format(_config_file))

config = imp.load_source("sbcswebsite_config", _config_file)
