
#if defined(_MSC_VER)
#	define _CRT_SECURE_NO_WARNINGS
#	define WIN32_LEAN_AND_MEAN
#	include <Windows.h>
#	ifdef _DEBUG
#		include <crtdbg.h>
#	endif
#endif

#if !UNDERSCORE_D
#   ifdef _DEBUG
#   define DEBUG_WAS_DEFINED_00
#   undef _DEBUG
#   endif
#endif

#include <Python.h>
#include <structmember.h>

#if !UNDERSCORE_D
    #ifdef DEBUG_WAS_DEFINED_00
    #define _DEBUG 1
    #undef DEBUG_WAS_DEFINED_00
    #endif
#endif

