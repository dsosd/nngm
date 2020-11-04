include_guard()

include(cmake/ctx.cmake)
include(cmake/map.cmake)
include(cmake/stack.cmake)

#l0 macro
macro(cmb_include _ns _type)
	cmb_ctx_get(_cmb_t000 ns)

	cmb_stack_push(type "${_type}")

	string(COMPARE EQUAL "${_cmb_t000}" "" _cmb_t001)
	if(${_cmb_t001})
		cmb_stack_push(ns "${_ns}")
	else()
		cmb_stack_push(ns "${_cmb_t000}/${_ns}")
	endif()
	unset(_cmb_t001)

	cmb_map_get(_cmb_t002 "ns_to_dir" "${_ns}")
	#MAGIC use "main.cmake" as the cmake file for each directory
	include("${_cmb_t002}/main.cmake")
	unset(_cmb_t002)

	cmb_stack_pop(ns)
	cmb_stack_pop(type)

	unset(_cmb_t000)
endmacro()
