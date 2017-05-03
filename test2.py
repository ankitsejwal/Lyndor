import install
import os

if install.check_os() == 'macos':
        os.chdir(os.path.expanduser('~/Desktop'))
        print os.getcwd()
