include_guard()

#l0 macro
macro(cmb_vhash _target)
	cmb_ctx_get(_cmb_t000 "vhash_mode")
	add_custom_target("${_target}_vhash" ALL
		COMMAND ./cmb/add_vhash.sh $<TARGET_FILE:${_target}> "${_cmb_t000}"
		DEPENDS "${_target}"
	)
	unset(_cmb_t000)
endmacro()

#l0 macro
macro(cmb_multi_vhash _target)
	cmb_ctx_get(_cmb_t000 "vhash_mode")
	add_custom_target("${_target}_vhash" ALL
		COMMAND ./cmb/add_multi_vhash.sh "$<JOIN:$<TARGET_OBJECTS:${_target}>, >" "${_cmb_t000}"
		DEPENDS "${_target}"
	)
	unset(_cmb_t000)
endmacro()
