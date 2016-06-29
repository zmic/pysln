
#if defined(_MSC_VER)
#	define _CRT_SECURE_NO_WARNINGS
#	define WIN32_LEAN_AND_MEAN
#	include <Windows.h>
#	ifdef _DEBUG
#		include <crtdbg.h>
#	endif
#endif

#ifdef _DEBUG
#define _DEBUG_WAS_DEFINED
#undef _DEBUG
#endif
#include <Python.h>
#include <structmember.h>
#ifdef _DEBUG_WAS_DEFINED
#define _DEBUG 1
#endif
