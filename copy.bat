rmdir /S /Q windist
mkdir windist
xcopy /Q /E c:\tempbuild\quinter.dist windist /Y
xcopy /Q /E docs windist /Y
xcopy /Q *.dll windist /Y
xcopy /Q /E ..\quinterfiles windist /S /Y
mkdir windist\sounds
xcopy /Q /E sounds windist\sounds /Y
rmdir /S /Q c:\tempbuild
del windist\t*86t.dll
pause