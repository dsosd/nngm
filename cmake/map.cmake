include_guard()

macro(cmb_map_set _name _key _val)
	set_property(GLOBAL PROPERTY "_ctx_map__${_name}__${_key}" "${_val}")
endmacro()

macro(cmb_map_get _ret _name _key)
	get_property(${_ret} GLOBAL PROPERTY "_ctx_map__${_name}__${_key}")
endmacro()
