#!C:\Users\Michael\Documents\Development\helloworld\flask\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'sqlalchemy-migrate==0.9.2','console_scripts','migrate-repository'
__requires__ = 'sqlalchemy-migrate==0.9.2'
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('sqlalchemy-migrate==0.9.2', 'console_scripts', 'migrate-repository')()
    )
