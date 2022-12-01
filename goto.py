import os
from colorama import Fore 

class Goto:
    def __init__(self) -> None:
        self.mainpath=self.get_mainpath()
        pass
    
    def cd(self,pth) -> None: # change directory
        os.chdir(pth)

    def get_mainpath(self) -> None:
        return os.path.abspath(os.curdir)

    def mainpath(self) -> None: # go to main folder
        self.cd(self.mainpath)

    def printcolor(self,text):
        return f"{Fore.CYAN}{text}{Fore.RESET}"

    def subf(self,*subfolders) -> str: # go to given fold(s) in parameter
        pth=self.mainpath
        for subfolder in subfolders:
            pth = os.path.join(pth,subfolder)
        self.cd(pth)
        return pth

    def _file(self,filename) -> any:
        abspath = self.get_mainpath() + f"\\{filename}"
        return abspath
        
    def cwd(self) -> str: # get current folder only
        curr = f"└─ ... ─ {self.printcolor(os.path.split(os.getcwd())[1])}"
        print(curr)
        return curr
    
    def abspath(self,print_=False) -> str: # get abspath of current folder
        abspath=os.getcwd()
        if print_:
            abspath=f"└─ {self.printcolor(os.getcwd())}"
            print(abspath)
        return abspath
    
    def fwardf(self,*subfolders):
        fwardf = self.abspath(print_=False)
        for subfolder in subfolders:
            fwardf = os.path.join(fwardf,subfolder)
        self.cd(fwardf)
        return fwardf
    
    def bwardf(self, repeat: int = 1):
        for item in range(0,repeat):
            self.cd('..')
        return self.abspath(print_=False)

    def trees(self) -> None: # print trees of current folder
        dirs=os.path.abspath(os.curdir).split('\\')
        spacing=''
        for d in dirs:
            print(spacing,'└─',f"{self.printcolor(d)}")
            spacing+='  '
    