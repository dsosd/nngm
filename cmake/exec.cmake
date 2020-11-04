include_guard()

include(cmake/f_escape.cmake)
include(cmake/vhash.cmake)

#l1 macro
macro(cmb_reg_exec _name _lib_dirs _link_flags)
	add_executable("${_name}")
	foreach(_cmb_t100 IN ITEMS ${_lib_dirs})
		target_link_directories("${_name}" PRIVATE "${_cmb_t100}")
	endforeach()

	target_link_options("${_name}" PRIVATE ${_link_flags})

	cmb_vhash("${_name}")
	unset(_cmb_t100)
endmacro()

#l0 macro
macro(cmb_exec _name _obj_ns)
	cmb_f_escape_ns(_cmb_t000 "${_obj_ns}")
	target_link_libraries(${_name} "_cmb_obj__${_cmb_t000}")
	unset(_cmb_t000)
endmacro()

#l1 macro
macro(cmb_execs _name) # _obj_nss
	list(APPEND _cmb_t100 ${ARGN})

	foreach(_cmb_t101 IN ITEMS ${_cmb_t100})
		cmb_exec("${_name}" "${_cmb_t101}")
	endforeach()

	unset(_cmb_t101)
	unset(_cmb_t100)
endmacro()
