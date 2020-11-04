cmake_minimum_required(VERSION 3.15)

project(
	nngm
	LANGUAGES CXX C
)

# Cmake settings
set(CMAKE_VERBOSE_MAKEFILE false)
set(CMAKE_BUILD_RPATH_USE_ORIGIN true)

set(CMAKE_C_COMPILER /usr/bin/gcc)
set(CMAKE_CXX_COMPILER /usr/bin/g++)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY build/bin)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY build/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY build/lib)

set(VHASH_MODE "permissive" CACHE STRING "Valid choices: bootstrap/permissive/enforcing")
set(NO_STRIP false CACHE BOOL "Do not strip final binary at linkage")

# Cmake includes
include(cmake/all.cmake)

# Vhash mode
set(_cmb_t00 ${VHASH_MODE})
cmb_ctx_set(vhash_mode ${_cmb_t00})
unset(_cmb_t00)

# Include dirs (normal)
cmb_ctx_set(normal_include_dirs ".;include")

# Compiler flags (normal)
cmb_ctx_set(normal_compiler_flags "-std=c++14;-fPIC;-ffile-prefix-map=${CMAKE_SOURCE_DIR}=ROOT")

cmb_ctx_add(normal_compiler_flags "-fstack-protector-strong;-D_FORTIFY_SOURCE=1")

cmb_ctx_add(normal_compiler_flags "-O2;-s")

cmb_ctx_add(normal_compiler_flags "-w")

# Cmb includes
cmb_map_set(ns_to_dir "ROOT" ".")
cmb_include("ROOT" "normal")

# Set up linker flags
cmb_ctx_set(normal_linker_flags "-pie;-static-libstdc++")
cmb_ctx_set(normal_linker_shared "-Wl,-Bdynamic")
cmb_ctx_add(normal_linker_shared "-lpthread")
cmb_ctx_add(normal_linker_shared "-ldl")

# Combine linker flags
cmb_ctx_merge(normal_linker_flags normal_linker_shared)

# Print linker flags
cmb_ctx_get(_cmb_t00 normal_linker_flags)
message("Linker flags:")
message("  >>>  ${_cmb_t00}  <<<  ")
unset(_cmb_t00)

# Target output_exec
cmb_ctx_get(_cmb_t00 normal_linker_flags)
cmb_reg_exec(output_exec "lib;lib_s" "${_cmb_t00}")
unset(_cmb_t00)

cmb_execs(output_exec
	${_cmb_obj_dep__ROOT}
)

# Strip output_exec
if(NOT ${NO_STRIP})
	add_custom_target(output_exec_strip ALL
		COMMAND strip --strip-unneeded $<TARGET_FILE:output_exec>
		DEPENDS output_exec
	)
	add_dependencies(output_exec_vhash output_exec_strip)
endif()
