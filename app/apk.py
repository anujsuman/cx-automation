import os

class APK:
    absolute_path = ''

    def CX_apk(self,version):
        self.absolute_path =  os.path.abspath(os.path.join(os.path.dirname(__file__), 'apps/CX.apk'))
        print(self.absolute_path)
        return self.absolute_path






