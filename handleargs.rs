pub fn handle_args(vec_args: Vec<String>, vec_args_length: usize) {
	let show = vec_args_length == 2 && vec_args[2].to_lowercase() == "true"; // Keep in mind usize is one lower than our actual size.
	print!("{:?}", show)
}
