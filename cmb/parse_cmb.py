import os
import re

def list_dir(root):
	dirs = []
	files = []

	ls_output = os.listdir(root)
	for str in ls_output:
		path = "/".join([root, str])

		if os.path.isfile(path):
			files.append(str)
		elif os.path.isdir(path):
			dirs.append(str)
		else:
			#unknown file type, neither file nor directory
			print(" ?? {}".format(path))

	return sorted(dirs), sorted(files)

def process_dir(root, target_filename, processed_dirs, bound_dirs, bound_files):
	dirs, files = list_dir(root)
	unbound_dirs = []
	unbound_files = []

	is_binding_dir = target_filename in files
	curr_dir = root.split("/")[-1]

	if is_binding_dir:
		if root not in bound_dirs:
			bound_dirs[root] = []
		if root not in bound_files:
			bound_files[root] = []

	for file in files:
		#TODO have a more generic check for source files
		if file.endswith(".cpp") or file.endswith(".c"):
			if is_binding_dir:
				bound_files[root].append(file)
			else:
				unbound_files.append("/".join([curr_dir, file]))

	for dir in dirs:
		dir_dirs, dir_files, dir_bound = process_dir(
			"/".join([root, dir]),
			target_filename,
			processed_dirs,
			bound_dirs,
			bound_files
		)

		if is_binding_dir:
			if dir_bound:
				bound_dirs[root].append(dir)
			else:
				for dir_file in dir_files:
					bound_files[root].append(dir_file)
		else:
			unbound_dirs += list(map(lambda x: "/".join([curr_dir, x]), dir_dirs))
			unbound_files += list(map(lambda x: "/".join([curr_dir, x]), dir_files))

	if is_binding_dir:
		processed_dirs.append(root)
	else:
		unbound_dirs.append(curr_dir)

	return unbound_dirs, unbound_files, is_binding_dir

def strip_path_beginning(data: dict):
	keys = list(data.keys())
	for key in keys:
		if key.startswith("./"):
			#MAGIC skip "./"
			new_key = key[2:]
			data[new_key] = data[key]
			del data[key]
		elif key == ".":
			#MAGIC skip "."
			new_key = key[1:]
			data[new_key] = data[key]
			del data[key]

def filter_regexes(regexes, strs):
	compiled = [re.compile("^" + x + "$") for x in regexes]
	str_matching = {x: any([y.match(x) for y in compiled]) for x in strs}
	safe_strs = [k for k, v in str_matching.items() if not v]

	return safe_strs

def macro_expand_file(in_fd, template_fd, out_fd, ctx):
	#ensure that template file starts with "template" and skip until a blank line is reached
	if template_fd.readline()[:-1] != "template":
		raise Exception()
	while template_fd.readline()[:-1] != "":
		pass

	exclude_regexes = []
	#process in file for template settings
	while True:
		line = in_fd.readline()
		#break on EOF
		if line == "":
			break

		line = line[:-1]
		if line == "exclude":
			while True:
				regex = in_fd.readline()[:-1]
				if regex == "":
					break

				exclude_regexes.append(regex)
		elif line == "":
			pass
		else:
			raise Exception()

	found_macro = False
	macro_token = ""
	special_tokens = []
	macro = ""

	for line in template_fd:
		if not found_macro:
			if line.startswith("%%__start"):
				found_macro = True
				#MAGIC skip "%%__start"
				tokens = line[9:].strip().split(" ")
				macro_token = tokens[0]
				special_tokens = tokens[1:]
			else:
				out_fd.write(line)
		else:
			if line[:-1] == "%%__end":
				if macro_token not in ctx:
					raise Exception()

				for it in filter_regexes(exclude_regexes, ctx[macro_token]):
					data = macro.replace(
						"%%{}%%".format(macro_token),
						it
					)
					for token in special_tokens:
						data = data.replace(
							"%%{}%%".format(token),
							ctx[token][it]
						)
					out_fd.write(data)

				#reset macro data
				found_macro = False
				macro_token = ""
				special_tokens = []
				macro = ""
			else:
				macro += line

def process_cmb_file(in_file: str, out_file: str, ctx: dict):
	with open(in_file) as in_:
		directive = in_.readline().strip()
		if directive.startswith("auto"):
			#MAGIC skip "auto"
			template_file = directive[4:].strip()
			with open(out_file, "w") as out:
				if not os.path.isfile(template_file):
					print("~~~ ERROR ~~~")
					raise Exception("Template file d.n.e.")
				with open(template_file) as template:
					macro_expand_file(in_, template, out, ctx)
		elif directive == "template":
			print("Unimplemented")
			raise Exception()
		else:
			raise Exception()

def get_namespace(dir):
	#MAGIC ".cmb_namespace" will store the namespace for the dir it's in
	if os.path.isfile("/".join([dir, ".cmb_namespace"])):
		with open("/".join([dir, ".cmb_namespace"])) as file:
			return file.readline().strip()
	else:
		return dir

def main():
	target_filename = "main.cmb"
	processed_dirs = []
	bound_dirs = {}
	bound_files = {}
	process_dir(".", target_filename, processed_dirs, bound_dirs, bound_files)

	#MAGIC trim off "./"
	processed_dirs = [x[2:] for x in processed_dirs]
	strip_path_beginning(bound_dirs)
	strip_path_beginning(bound_files)

	print(processed_dirs)
	print(bound_dirs)

	for dir in processed_dirs:
		if dir == "":
			process_cmb_file(
				"main.cmb",
				"main.cmake",
				{
					"DIR": bound_dirs[dir],
					"FILE": bound_files[dir],
					"NS": {x: get_namespace(x) for x in bound_dirs[dir]}
				}
			)
			continue
		dir_list = ["/".join([dir, x]) for x in bound_dirs[dir]]
		process_cmb_file(
			"{}/main.cmb".format(dir),
			"{}/main.cmake".format(dir),
			{
				"DIR": dir_list,
				"FILE": bound_files[dir],
				"NS": {x: get_namespace(x) for x in dir_list}
			}
		)
	print("~ ~DONE~ ~")

if __name__ == "__main__":
	main()
