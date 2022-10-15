import argparse, os, sys
from re import S
from typing import Optional

class State:
	workdir: str
	directories: list[str]
	config: dict[str, str] = {
		'directories': {
			'config': '.config',
			'data': '.data'
		},
	}
	def __init__(self, workdir: Optional[str] = '.', config: Optional[dict[str, str]] = None):
		self.workdir = workdir

		if config: self.config = config
		desired_state = set(self.config['directories'].values())
		current_state = set(os.listdir(self.workdir))

		exists = current_state.intersection(desired_state)
		missing = desired_state.difference(exists)
		for missed in missing:
			path = r"{}/{}".format(self.workdir, missed)
			os.mkdir(path)

			# md5 file hashing to check for changes.
			open("{}/{}".format(path, 'cache.yml'), 'w')
	def init_data(self, name: str, force: bool = False) -> bool:
		"""Generates a new data file in the data directory. Returns False if it fails."""
		files = os.listdir('{}/{}'.format(self.workdir, self.config['directories']['data']))
		files = [file.split('.')[0] for file in files if file.endswith('.fin')]
	def check_integrity(exclude: Optional[list[str]] = None) -> bool:
		"""Checks the state's folders for file integrity. If the cache file does not match checksums on file, return False"""
		return NotImplementedError


state = State()

state.init_data('something')