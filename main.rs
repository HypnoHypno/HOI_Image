mod handleargs; // Import handleargs.rs

use std::env::args; // Will let us use args() to get all arguments sent.

fn main() {
	// args() gets all arguments sent to the file in it's own data type.
	// We then run .collect() on it to gather it's elements.
	// Using Vec<_> specifies we want a Vector.
	let vec_args: Vec<_> = args().collect();
	let vec_args_length = vec_args.len() - 1; // By default there's always 1 argument, we don't consider this when counting here.
	match vec_args_length {
		1 | 2 => {
			handleargs::handle_args(vec_args, vec_args_length)
		},
		_ => { // If the amount of arguments passed is 0 or >2.
			help();
		}
	}
}

fn help() {
	println!("Usage:
#1: <path> (Required):
	File to convert to or from HOI.
#2: <bool> (Optional):
	If your first argument is a HOI file, do you want to save it as PNG or just view it?")
}
