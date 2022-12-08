# SPDX-License-Identifier: Apache-2.0

cmake_minimum_required(VERSION 3.20.0)

set(ZEPHYR_EXTRA_MODULES ${CMAKE_CURRENT_SOURCE_DIR}/../modules/tinyframe)
#set(MODULE_EXT_ROOT ${CMAKE_CURRENT_SOURCE_DIR}/..)


set(ENV{PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION} python)
message(STATUS "env: $ENV{PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION}")
find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(protobuf_uart)

# Note that here, we're adding CMAKE_SOURCE_DIR to the include path for nanopb.
# This is needed because the below call to nanopb_generate_cpp() is using
# 'RELPATH .'
set(NANOPB_OPTIONS "-I${CMAKE_SOURCE_DIR}")
nanopb_generate_cpp(proto_sources proto_headers RELPATH .
    src/simple.proto
)
# we need to be able to include generated header files
zephyr_library_include_directories(${CMAKE_CURRENT_BINARY_DIR})

FILE(GLOB app_sources src/*.c)
target_sources(app PRIVATE
${proto_sources}
${app_sources}
)