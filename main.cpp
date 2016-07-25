#include "include.h"

PyMethodDef g_methods[] =
{
    {0, 0, 0, 0}
};

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#define STR_00(x) #x
#define STR_0(x) STR_00(x)
#define MODULE_STRING STR_0(MODULE_NAME)
#define MODULE_DOC MODULE_STRING
#define INIT_FUNCTION_00(x) PyInit_##x
#define INIT_FUNCTION_0(x) INIT_FUNCTION_00(x)
#define INIT_FUNCTION INIT_FUNCTION_0(MODULE_NAME)

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    MODULE_STRING,       /* m_name */
    MODULE_DOC,          /* m_doc */
    -1,                  /* m_size */
    g_methods,           /* m_methods */
    NULL,                /* m_reload */
    NULL,                /* m_traverse */
    NULL,                /* m_clear */
    NULL,                /* m_free */
};


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
PyMODINIT_FUNC
INIT_FUNCTION()
{
#ifdef _DEBUG
#if defined(WIN32) && defined(_MSC_VER)
    int tmpDbgFlag;
    tmpDbgFlag = _CrtSetDbgFlag(_CRTDBG_REPORT_FLAG);
    tmpDbgFlag |= _CRTDBG_LEAK_CHECK_DF;
    _CrtSetDbgFlag(tmpDbgFlag);
    //_CrtSetReportMode( _CRT_WARN, _CRTDBG_MODE_DEBUG | _CRTDBG_MODE_FILE );
    //_CrtSetReportFile( _CRT_WARN, _CRTDBG_FILE_STDERR );
#endif
#if !UNDERSCORE_D
    PyErr_Warn(PyExc_RuntimeWarning, "This is the debug build of " MODULE_STRING ".pyd");
#endif
#endif
    PyObject * module = PyModule_Create(&moduledef);
    return module;
}


