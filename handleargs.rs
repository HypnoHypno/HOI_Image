mod converttohoi;
mod convertfromhoi;

use std::{
	path::Path,
	ffi::OsStr
};

pub fn handle_args(vec_args: Vec<String>, vec_args_length: usize) {
	let show = vec_args_length == 2 && vec_args[2].to_lowercase() == "true"; // Keep in mind usize is one lower than our actual size.
	let ext = Path::new(&vec_args[1]).extension().and_then(OsStr::to_str);
	match ext {
		Some("hoi") | Some("hoif") => {
			convertfromhoi::convert(vec_args[1], show);
		},
		_ => {
			converttohoi::convert(vec_args[1]);
		}
	}
}
