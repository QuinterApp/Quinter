@echo off
nuitka --windows-company-name=Mellaquin --windows-product-name=Quinter --windows-file-version=0.62 --windows-product-version=0.62 --windows-file-description=Quinter --standalone --python-flag=no_site --include-data-file=keymap.keymap=keymap.keymap --windows-disable-console --output-dir=c:\tempbuild --remove-output quinter.pyw