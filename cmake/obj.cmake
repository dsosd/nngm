include_guard()

include(cmake/f_escape.cmake)
include(cmake/vhash.cmake)

#l1 macro
macro(cmb_reg_obj _ns _include_dirs _compile_flags)
	cmb_f_escape_ns(_cmb_t100 "${_ns}")

	add_library("_cmb_obj__${_cmb_t100}" OBJECT)

	target_include_directories("_cmb_obj__${_cmb_t100}" PRIVATE ${_include_dirs})
	target_compile_options("_cmb_obj__${_cmb_t100}" PRIVATE ${_compile_flags})

	cmb_multi_vhash("_cmb_obj__${_cmb_t100}")
	#add this target to its list of upstream dependencies
	list(APPEND "_cmb_obj_dep__${_cmb_t100}" "${_ns}")

	unset(_cmb_t100)
endmacro()

#l0 macro
macro(cmb_object _ns _src_name)
	cmb_f_escape_ns(_cmb_t000 "${_ns}")
	target_sources("_cmb_obj__${_cmb_t000}" PRIVATE "${_src_name}")
	unset(_cmb_t000)
endmacro()

#l1 macro
macro(cmb_objects _ns) # _src_names
	list(APPEND _cmb_t100 ${ARGN})

	foreach(_cmb_t101 IN ITEMS ${_cmb_t100})
		cmb_object("${_ns}" "${_cmb_t101}")
	endforeach()

	#in case no sources are provided, we need to add at least one source
	#MAGIC use "null.cpp" as dummy source
	list(LENGTH _cmb_t100 _cmb_t102)
	if(_cmb_t102 EQUAL 0)
		cmb_object("${_ns}" "null.cpp")
	endif()

	unset(_cmb_t102)
	unset(_cmb_t101)
	unset(_cmb_t100)
endmacro()
