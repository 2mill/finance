use std::path;
pub mod config {
	pub struct Config {
		data_directory_path: String,
		config_directory_path: String,
	}
	impl Config {
		fn new(data_directory: String, config_directory: String) -> Self {
			Config {
				data_directory_path: data_directory,
				config_directory_path: config_directory,
			}
		}
	}

}