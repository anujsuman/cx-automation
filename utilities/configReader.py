from configparser import ConfigParser
from utilities.configPath import configpath


def readConfig(section, key):
    config = ConfigParser(allow_no_value=True)
    configFile = configpath()
    filePath = configFile.config_path() + "/locator.ini"
    config.read(filePath, encoding = 'utf8')
    #print(config.get("Input_PhoneNumber", "Enter_number_cls"))
    return config.get(section, key)
# readConfig("Input_PhoneNumber", "Enter_number_cls" )
