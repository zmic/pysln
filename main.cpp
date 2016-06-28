#include "include.h"

PyMethodDef g_methods[] =
{
    {0, 0, 0, 0}
};

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#define _STR(x) #x
#define STR(x) _STR(x)
#define MODULE_STRING STR(MODULE_NAME)
#define MODULE_DOC MODULE_STRING
#define __INIT_FUNCTION(x) PyInit_##x
#define _INIT_FUNCTION(x) __INIT_FUNCTION(x)
#define INIT_FUNCTION _INIT_FUNCTION(MODULE_NAME)

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
    PyErr_Warn(PyExc_RuntimeWarning, "This is the debug build of "MODULE_STRING".pyd");
#endif
    PyObject * module = PyModule_Create(&moduledef);
    return module;
}


