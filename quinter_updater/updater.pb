RunProgram("taskkill.exe","-f -im Quinter.exe","",#PB_Program_Wait|#PB_Program_Hide)
RunProgram("unzip.exe","-o -qq Quinter.zip","",#PB_Program_Wait|#PB_Program_Hide)
RunProgram("Quinter.exe","","")
; IDE Options = PureBasic 5.73 LTS (Windows - x64)
; CursorPosition = 2
; EnableThread
; EnableXP
; EnableAdmin
; Executable = updater.exe
; EnableCompileCount = 3
; EnableBuildCount = 3