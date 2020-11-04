include_guard()

macro(cmb_ctx_set _name) # _vals
	set_property(GLOBAL PROPERTY "_ctx_var__${_name}" ${ARGN})
endmacro()

macro(cmb_ctx_get _ret _name)
	get_property(${_ret} GLOBAL PROPERTY "_ctx_var__${_name}")
endmacro()

macro(cmb_ctx_add _name _val)
	set_property(GLOBAL APPEND PROPERTY "_ctx_var__${_name}" "${_val}")
endmacro()

#l0 macro
macro(cmb_ctx_merge _lhs _rhs)
	cmb_ctx_get(_cmb_t000 "${_lhs}")
	cmb_ctx_get(_cmb_t001 "${_rhs}")

	list(APPEND _cmb_t000 ${_cmb_t001})
	cmb_ctx_set(${_lhs} "${_cmb_t000}")

	unset(_cmb_t001)
	unset(_cmb_t000)
endmacro()
