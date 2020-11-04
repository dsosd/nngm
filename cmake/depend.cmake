include_guard()

include(cmake/f_escape.cmake)

#l0 macro
macro(cmb_depend _parent_ns _child_ns)
	cmb_f_escape_ns(_cmb_t000 "${_parent_ns}")
	cmb_f_escape_ns(_cmb_t001 "${_child_ns}")

	list(APPEND "_cmb_obj_dep__${_cmb_t000}" ${_cmb_obj_dep__${_cmb_t001}})

	unset(_cmb_t001)
	unset(_cmb_t000)
endmacro()
