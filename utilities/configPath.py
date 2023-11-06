import os

class configpath:
    def config_path(self):
        self.absolutePath = str(os.path.dirname(__file__))
       # print(self.absolutepath)
        return self.absolutePath