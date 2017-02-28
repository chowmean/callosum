import yaml
from ProjectConfig import RANDOM_MULTIPLIER, RANDOM_ADD


def get_hashables(database):
	f = open(database+'.yml')
	dataMap = yaml.safe_load(f)
	f.close()
	to_hash = dataMap['pii']
	to_numerical = dataMap['numerical_hash']
	return to_hash, to_numerical

def random_algo(number):
	return int(number * RANDOM_MULTIPLIER) + RANDOM_ADD