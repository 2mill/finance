import argparse, os, sys
from re import S
from typing import Optional
import csv
from enum import Enum

parser = argparse.ArgumentParser('finance', 'finance [record] NAME AMOUNT SOURCE type?', 'Tool for recording your financial spending.')
parser.add_argument('--record', nargs=4) 



args = parser.parse_args()
print(args)
class State:
	workdir: str
	directories: list[str]
	config: dict[str, str] = {
		'directories': {
			'config': '.config',
			'data': '.data'
		},
	}
	data_path: str
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

		self.data_path = "{}/{}".format(self.workdir, self.config['directories']['data'])
	def init_data(self, name: str, force: bool = False) -> bool:
		"""Generates a new data file in the data directory. Returns False if it fails."""
		files = os.listdir('{}/{}'.format(self.workdir, self.config['directories']['data']))
		files = [file.split('.')[0] for file in files if file.endswith('.fin')]

		if name in files and not force: return False
		else: open(
			'{}/{}/{}'.format(
				self.workdir,
				self.config['directories']['data'],
				"{}.fin".format(name)
			), 'w'
		)

		# TODO apply hash and path to cache
		return True

	def find(self, name: str) -> str:
		name = "{}.fin".format(name) if not name.endswith('.fin') else name
		if name in os.listdir(self.data_path):
			return '{}/{}'.format(self.data_path, name)

		return None

	def check_integrity(exclude: Optional[list[str]] = None) -> bool:
		"""Checks the state's folders for file integrity. If the cache file does not match checksums on file, return False"""
		return NotImplementedError

state = State()



class LineItemType(Enum):
	unknown= {
		'id': -1,
		'description': 'unkown',
	}
	variable={
		'id': 0,
		'description': 'variable',
	}
	fixed={
		'id': 1,
		'description': 'fixed',
	}
	intermittent={
		'id': 2,
		'description': 'intermittent',
	}
	discretionary={
		'id':3,
		'description':'discretionary'
	}

		


resolver: dict[str, LineItemType] = {
	'variable': LineItemType.variable,
	'fixed': LineItemType.fixed,
	'intermittent': LineItemType.intermittent,
	'discretionary': LineItemType.discretionary
}

category_line_item_map: dict[str, LineItemType] = {
	'groceries': resolver['variable'],
	'rent': resolver['fixed']
}

class LineItem:
	name: str
	amount: float
	category: str
	line_item_type: LineItemType
	def __init__(self, name: str, amount: float, category: str, line_type: Optional[LineItemType]):
		self.name = name
		self.amount = amount
		self.category = category
		self.line_item_type = line_type

	def __str__(self) -> str:
		return '{},{},{},{}'.format(
			self.name,
			self.amount,
			self.category,
			self.line_item_type.value['description']
		)


if args.record:
	name = args.record[0]
	amount = args.record[1]
	source = args.record[2]
	line_type = args.record[3]


	line_type = resolver.get(line_type)
	line_type = LineItemType.unknown if not line_type else line_type

	line_item = LineItem(
		name,
		amount,
		source,
		line_type
	)


	state.init_data('spending')
	state.find('spending')
	with open(state.find('spending'), 'a') as f:
		print(str(line_item), file=f)
	f.close()