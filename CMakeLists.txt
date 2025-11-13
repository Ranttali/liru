cmake_minimum_required(VERSION 3.25...3.30)
project(
    liru
    VERSION 0.1.0
    DESCRIPTION "High-performance Python wrapper for Spout 2.007 GPU texture sharing"
    LANGUAGES CXX
)

# C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Find Python (from scikit-build-core)
find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)

# Find pybind11
find_package(pybind11 CONFIG REQUIRED)

# Spout SDK paths (SDK binaries package structure)
set(SPOUT_SDK_DIR "${CMAKE_CURRENT_SOURCE_DIR}/external/Spout2/Spout-SDK-binaries/Libs_2-007-017")
set(SPOUT_INCLUDE_DIR "${SPOUT_SDK_DIR}/include")
set(SPOUT_LIB_DIR "${SPOUT_SDK_DIR}/MD/lib")
set(SPOUT_BIN_DIR "${SPOUT_SDK_DIR}/MD/bin")

# Verify Spout SDK exists
if(NOT EXISTS "${SPOUT_INCLUDE_DIR}/SpoutGL/Spout.h")
    message(FATAL_ERROR
        "Spout SDK not found at ${SPOUT_SDK_DIR}\n"
        "Please run: scripts/download_spout_sdk.bat\n"
        "Or download from: https://github.com/leadedge/Spout2/releases/tag/2.007.017\n"
    )
endif()

# Source files
set(LIRU_SOURCES
    src/bindings.cpp
    src/sender_wrapper.cpp
    src/receiver_wrapper.cpp
)

# Create Python module
pybind11_add_module(_liru_core MODULE ${LIRU_SOURCES})

# Include directories
target_include_directories(_liru_core PRIVATE
    ${SPOUT_INCLUDE_DIR}
    ${SPOUT_INCLUDE_DIR}/SpoutGL
    ${SPOUT_INCLUDE_DIR}/SpoutDX
)

# Link Spout library and system libraries
target_link_libraries(_liru_core PRIVATE
    "${SPOUT_LIB_DIR}/Spout.lib"
    opengl32
    gdi32
    user32
)

# Compiler flags
if(MSVC)
    target_compile_options(_liru_core PRIVATE
        /W4                  # Warning level 4
        /WX                  # Treat warnings as errors
        /permissive-         # Standards conformance
        /Zc:__cplusplus      # Enable __cplusplus macro
        /EHsc                # Exception handling
        /MP                  # Multi-processor compilation
    )
    target_compile_definitions(_liru_core PRIVATE
        _CRT_SECURE_NO_WARNINGS
        NOMINMAX
        WIN32_LEAN_AND_MEAN
    )
endif()

# Install target (wheel.install-dir in pyproject.toml already sets base to 'liru')
install(TARGETS _liru_core LIBRARY DESTINATION .)

# Install Spout DLL alongside the extension (required at runtime)
install(FILES "${SPOUT_BIN_DIR}/Spout.dll" DESTINATION .)

# Print configuration summary
message(STATUS "==========================================")
message(STATUS "liru Build Configuration")
message(STATUS "==========================================")
message(STATUS "CMake version:       ${CMAKE_VERSION}")
message(STATUS "C++ compiler:        ${CMAKE_CXX_COMPILER_ID} ${CMAKE_CXX_COMPILER_VERSION}")
message(STATUS "Python version:      ${Python_VERSION}")
message(STATUS "Spout SDK:           ${SPOUT_SDK_DIR}")
message(STATUS "Build type:          ${CMAKE_BUILD_TYPE}")
message(STATUS "==========================================")
