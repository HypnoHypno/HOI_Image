use std::env::args; // Will let us use args() to get all arguments sent.

fn main() {
	// args() gets all arguments sent to the file in it's own data type.
	// We then run .collect() on it to gather it's elements.
	// Using Vec<_> specifies we want a Vector.
	let vec_args: Vec<_> = args().collect();
	match vec_args.len()-1 { // By default there's always 1 argument, we don't consider this when counting here.
		1 => {
			println!("{:?}", vec_args[1])
		},
		_ => {
			help()
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