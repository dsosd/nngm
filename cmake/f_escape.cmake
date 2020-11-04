include_guard()

function(cmb_f_escape_ns _ret _ns)
	string(REPLACE "/" "--" _cmb_t00 "${_ns}")
	set(${_ret} "${_cmb_t00}" PARENT_SCOPE)
endfunction()
