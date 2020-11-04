include_guard()

macro(cmb_stack_push _name _val)
	list(PREPEND "_ctx_stack__${_name}" "${_val}")
endmacro()

macro(cmb_stack_pop _name)
	list(POP_FRONT "_ctx_stack__${_name}")
endmacro()

macro(cmb_stack_get _ret _name)
	list(GET "_ctx_stack__${_name}" 0 ${_ret})
endmacro()
