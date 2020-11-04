import enum

class Vhash_mode(enum.Enum):
	none = 0
	bootstrap = 1
	permissive = 2
	enforcing = 3

class Vhash_status(enum.Enum):
	mismatch = 0
	ok_mismatch = 1
	ok = 2
	pass_ = 3

	def __str__(self):
		return ["MISMATCH", "ok", "OK+", "PASS"][self.value]

def compare_hash(curr_mode: Vhash_mode, ref_mode: Vhash_mode, equal: bool) \
		-> Vhash_status:
	if ref_mode == Vhash_mode.none:
		if curr_mode == Vhash_mode.none:
			raise Exception()
		elif curr_mode == Vhash_mode.bootstrap:
			return Vhash_status.pass_
		elif curr_mode == Vhash_mode.permissive:
			return Vhash_status.ok_mismatch
		else:
			return Vhash_status.mismatch

	elif ref_mode == Vhash_mode.bootstrap:
		if curr_mode == Vhash_mode.none:
			return Vhash_status.mismatch
		elif curr_mode == Vhash_mode.bootstrap:
			return Vhash_status.pass_ if equal else Vhash_status.mismatch
		elif curr_mode == Vhash_mode.permissive:
			return Vhash_status.pass_ if equal else Vhash_status.ok_mismatch
		else:
			return Vhash_status.pass_ if equal else Vhash_status.mismatch

	elif ref_mode == Vhash_mode.permissive:
		if curr_mode == Vhash_mode.none:
			return Vhash_status.ok_mismatch
		elif curr_mode == Vhash_mode.bootstrap:
			return Vhash_status.ok if equal else Vhash_status.ok_mismatch
		elif curr_mode == Vhash_mode.permissive:
			return Vhash_status.pass_ if equal else Vhash_status.ok_mismatch
		else:
			return Vhash_status.pass_ if equal else Vhash_status.mismatch

	else:
		if curr_mode == Vhash_mode.none:
			return Vhash_status.mismatch
		elif curr_mode == Vhash_mode.bootstrap:
			return Vhash_status.ok if equal else Vhash_status.mismatch
		elif curr_mode == Vhash_mode.permissive:
			return Vhash_status.ok if equal else Vhash_status.ok_mismatch
		else:
			return Vhash_status.pass_ if equal else Vhash_status.mismatch

def get_vhash_map(filename: str):
	ret = {}
	with open(filename, "a") as file:
		pass
	with open(filename, "r") as file:
		for line in file:
			mode = Vhash_mode.bootstrap
			if line.startswith("!"):
				mode = Vhash_mode.enforcing
				line = line[1:]
			elif line.startswith("?"):
				mode = Vhash_mode.permissive
				line = line[1:]

			key, hash = line.split(": ")
			ret[key] = (hash, mode)

	return ret

def compare_vhash_map(curr, ref_):
	ret = {}
	ref = ref_.copy()

	for key, val in curr.items():
		if key in ref:
			ret[key] = compare_hash(val[1], ref[key][1], val[0] == ref[key][0])
			del ref[key]
		else:
			ret[key] = compare_hash(val[1], Vhash_mode.none, False)

	for key, val in ref.items():
		ret[key] = compare_hash(Vhash_mode.none, val[1], False)

	return ret

def update_vhash_map(curr, ref, comp):
	for k, v in curr.items():
		if comp[k] == Vhash_status.pass_:
			ref[k] = v

def write_vhash_map(filename, data):
	with open(filename, "w") as file:
		for k, v in sorted(data.items()):
			prefix_sym = ["", "?", "!"][v[1].value - 1]
			file.write("{}{}: {}".format(prefix_sym, k, v[0]))

def main():
	ref = get_vhash_map("ref_hashes")
	curr = get_vhash_map("curr_hashes")

	stats = {x: 0 for x in Vhash_status}
	comp = compare_vhash_map(curr, ref)
	for k, v in sorted(comp.items()):
		stats[v] += 1
		if v != Vhash_status.pass_:
			print(v, k)

	update_vhash_map(curr, ref, comp)
	write_vhash_map("new_hashes", ref)

	print("{} / {}({}-{}) / {}".format(
		stats[Vhash_status.pass_],
		stats[Vhash_status.ok] + stats[Vhash_status.ok_mismatch],
		stats[Vhash_status.ok],
		stats[Vhash_status.ok_mismatch],
		stats[Vhash_status.mismatch]
	))

if __name__ == "__main__":
	main()
