from cx_Freeze import setup, Executable

setup(name = "SlytherClaw Vector", version = "1", description = "SlytherClaw Vector Server",
    #executables = [Executable("new_gui.py"), Executable("gui_sidebar.py"), Executable("engine.py")])
    executables = [Executable("vector_server_select.py")])

#import compileall
#compileall.compile_dir(".", force =1)