from dotenv import load_dotenv
import os
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


DEVICENAME=os.getenv('DEVICENAME')
PLATFORMNAME=os.getenv('PLATFORMNAME')
AUTOMATIONNAME=os.getenv('AUTOMATIONNAME')
PLATFORMVERSION=os.getenv('PLATFORMVERSION')
APPPACKAGE=os.getenv('APPPACKAGE')
APPACTIVITY=os.getenv('APPACTIVITY')
APP=os.getenv('APP')
AUTOGRANTPERMISSIONS=True
TARGET_BASE_URL = os.getenv('TARGET_BASE_URL')
WIREMOCK_URL = os.getenv('WIREMOCK_URL')
PHONE_NUMBER=os.getenv('PHONE_NUMBER')

WD_URL = os.getenv('WD_URL')