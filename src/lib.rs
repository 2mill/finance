use std::path;
use std::fs;
pub struct Config {
	data_directory_path: String,
	config_directory_path: String,
}
impl Config {
	pub fn new(data_directory: String, config_directory: String) -> Self {
		Config {
			data_directory_path: data_directory,
			config_directory_path: config_directory,
		}
	}
	pub fn dataPath(&self) -> &path::Path {
		path::Path::new(&self.data_directory_path)	
	} 

	pub fn configPath(&self) -> &path::Path {
		path::Path::new(&self.config_directory_path)
	}
}

struct LineItem {
	name: String,
	amount: f32,
	purpose: String,
	spending_category: SpendingCategory
}

struct Record {
	name: String,
	line_items: Vec<LineItem>,
	path: &path::Path,
}

impl Record {
	pub fn new(name: String, config: &Config) -> Self {
		let mut newPathString = format!("./{}.fin", name);
		if let Some(path) = config.dataPath().to_str() {
			newPathString = format!("{}/{}", path, name);
		};
		let path = path::Path::new(newPathString);
		if !path.exists() {
			fs::File::create(path)
		}
		Record {
			name,
			line_items: Vec::new(),
			path: path::Path::new(newPathString)
		}
	}
	pub fn pushLineItem(&mut self, line_item: LineItem) {
		self.line_items.push(line_item);
	}
}

impl LineItem {
	fn new(name: String, amount: f32, purpose: String, spending_category: SpendingCategory) -> Self {
		LineItem {
			name,
			amount,
			purpose,
			spending_category
		}
	}
}

enum SpendingCategory {
	Variable,
	Fixed,
	Intermittent,
	Discretionary,
}
