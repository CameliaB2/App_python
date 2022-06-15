from mlc_script_log import *
import platform

# Unico version check: 
if(platform.system() == "Windows"):
	from win32com.client import Dispatch
	
	logging.info("platform: ", platform.system())

	ver_parser = Dispatch('Scripting.FileSystemObject')
	mlc_app = "C:/Program Files (x86)/STMicroelectronics/Unico-GUI/unico.exe"  ## Windows

elif(platform.system() == "Darwin"): #Mac OS
	logging.info("platform: ", platform.system())

elif(platform.system() == "Linux"): #Linux
	logging.info("platform: ", platform.system())
else:
	logging.error("This application not available on this platform")


app_version = "0.0.0.0"
if os.path.isfile(mlc_app):
    app_version = ver_parser.GetFileVersion(mlc_app)
    logging.info("app version: " + app_version)
expected_version = "9.12.0.0"

if app_version != expected_version:
#    logging.error("\nERROR: wrong Unico version. Please download version " + expected_version + " from: https://www.st.com/en/development-tools/unico-gui.html")
    logging.error("\nERROR: wrong app version")