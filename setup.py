import sys
import os
from cx_Freeze import setup, Executable

#setup
python_dir = r'C:¥Python35' 
includes = []
include_files = [python_dir + r'¥DLLs¥tcl86t.dll',python_dir + r'¥DLLs¥tk86t.dll']
packages = ['os', 'sys', 'tkinter']
excludes = ['email', 'html', 'http', 'urlib','logging', 'ctypes', 'distutils','multiprocessing', 'pydoc_data','test', 'unittest','xml', 'xmlrpc']
build_exe_options = {'includes': includes,
                     'include_files': include_files,
                     'packages': packages,
                     'excludes': excludes,
                     'optimize': 2}
base = None

if sys.platform == 'win32':
    base = 'Win32GUI'
    
os.environ['TCL_LIBRARY'] = python_dir + r'¥tcl¥tcl8.6'
os.environ['TK_LIBRARY'] = python_dir + r'¥tcl¥tk8.6'
#exeを指定
exe = [
    Executable('Main.py', base=base, targetName='Main.exe', icon='sample.ico')
]

#description
setup( name = 'FIVE AI',
       version = '1.0',
       description = 'AI',
       options = {'build_exe': build_exe_options},
       executables = exe )
