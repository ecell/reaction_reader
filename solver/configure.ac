AC_REVISION([$Id$])
AC_INIT
AC_CONFIG_SRCDIR([autogen.sh])
AC_DISABLE_STATIC
AM_INIT_AUTOMAKE([reaction_reader],[0.1b])
AM_PROG_LIBTOOL
AM_CHECK_PYMOD(numpy,,,[AC_MSG_ERROR([could not find Python numpy module.])])
AM_CHECK_PYMOD(scipy,,,[AC_MSG_ERROR([could not find Python scipy module.])])
AM_CHECK_PYTHON_HEADERS()
ac_save_CPPFLAGS="$CPPFLAGS"
CPPFLAGS="$CPPFLAGS $PYTHON_INCLUDES"
AC_CHECK_TYPES([PyBaseExceptionObject],[],[],[
#include <Python.h>
#include <pyerrors.h>
])
AM_CONFIG_HEADER([config.h])
AC_CONFIG_FILES([Makefile])
AC_OUTPUT([])
