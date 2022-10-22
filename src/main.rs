extern crate argparse;
use std::path;
use argparse::{ArgumentParser};
use argparse::{
	Store,
	StoreTrue,
};
use finance::Config;
use csv;
fn main() {
	let mut item = String::from("undefined");
	let config = Config::new(
		String::from("~/.config"), 
		String::from(".data")
	);
	let data_path = config.dataPath();
	{
		let mut ap = ArgumentParser::new();
		ap.set_description("A simple finance tracking tool.");
		ap.refer(&mut item).add_option(&["-r", "--record"], Store, "Record a line item");
		ap.parse_args_or_exit()
	}
	let reader = csv::Reader::from_path(config.dataPath());



	println!("{} item", item)

}