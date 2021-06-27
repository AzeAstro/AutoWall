import sys
import os
import time
import argparse
import re
import subprocess
import pathlib
import ctypes


#default walls
folder=f"{pathlib.Path(__file__).parent.resolve()}/Wallpapers"
sleep_time=3600

#Parser
parser=argparse.ArgumentParser(prog="AutoWall",description="Simple and light script that changes wallpaper automaticly each hour.")
parser.add_argument("--time","-t",help="Period for wallpaper changing.(seconds)",type=int)
parser.add_argument("--folder","-f",help="For specifying wallpapers folder.(full path)",type=str)
args=parser.parse_args()

if args.time:
    sleep_time=args.time

if args.folder:
    folder=args.folder


#image file formats.
imgFormats=[".png",".jpg",".jpeg",".tiff",".tif"]
wallpaper_list=[]
try:
    for file in os.listdir(folder):
        for imgFormat in imgFormats:
            if file.endswith(imgFormat):
                wallpaper_list.append(file)
except FileNotFoundError:
    print("Folder not found")
except Exception as e:
    print(f"Unknown error happened:\n{e}")

    

class DE:
    def getDE():
        if sys.platform in ["win32", "cygwin"]:
            return "windows"
        elif sys.platform == "darwin":
            return "mac"
        else:
            desktop_session = os.environ.get("DESKTOP_SESSION")
            if desktop_session is not None:
                desktop_session = desktop_session.lower()
                if desktop_session in ["gnome","unity", "cinnamon", "mate", "xfce4", "lxde", "fluxbox", 
                            "blackbox", "openbox", "icewm", "jwm", "afterstep","trinity", "kde","pop","pantheon"]:
                    return desktop_session
                elif "xfce" in desktop_session or desktop_session.startswith("xubuntu"):
                    return "xfce4"
                elif desktop_session.startswith("ubuntu"):
                    return "unity"       
                elif desktop_session.startswith("lubuntu"):
                    return "lxde" 
                elif desktop_session.startswith("kubuntu"): 
                    return "kde" 
                elif desktop_session.startswith("razor"): 
                    return "razor-qt"
                elif desktop_session.startswith("wmaker"):
                    return "windowmaker"
                elif desktop_session.startswith("pop"):
                    return "pop-gnome"
                elif desktop_session.startwith("pantheon"):
                    return "pantheon"
            if os.environ.get('KDE_FULL_SESSION') == 'true':
                return "kde"
            elif os.environ.get('GNOME_DESKTOP_SESSION_ID'):
                if not "deprecated" in os.environ.get('GNOME_DESKTOP_SESSION_ID'):
                    return "gnome2"
                elif "deprecated" in os.environ.get('GNOME_DESKTOP_SESSION_ID'):
                    return "gnome3"
                elif DE.is_running("xfce-mcs-manage"):
                    return "xfce4"
                elif DE.is_running("ksmserver"):
                    return "kde"
            return "unknown"

    def is_running(process):

        try:
            s = subprocess.Popen(["ps", "axw"],stdout=subprocess.PIPE)
        except:
            s = subprocess.Popen(["tasklist", "/v"],stdout=subprocess.PIPE)
        for x in s.stdout:
            x=x.decode("utf-8")
            if re.search(process, x):
                return True
        return False
#Special thanks to Martin Hansen
#https://stackoverflow.com/questions/2035657/what-is-my-current-desktop-environment



break_flag=False
de=DE.getDE()
if wallpaper_list==[]:
    print("Couldn't find any wallpapers. Exitting....")
else:
    while True:
        for imgname in wallpaper_list:
            if de=="unknown":
                print("Sorry,seems like this desktop enviroment is not available for this script.Please,report it to us in github. Thanks in advance.")
                input()
                break_flag=True
                break
            else:
                if de=="gnome3" or de=="pop" or de=="unity":
                    command=f"gsettings set org.gnome.desktop.background picture-uri 'file://{folder}/{imgname}'"
                elif de=="xfce4":
                    command=f"xfconf-query -c xfce4-desktop -p {imgname} -s {folder}"
                elif de=="pantheon":
                    command=f"io.elementary.contract.set-wallpaper {folder}/{imgname}"
                elif de=="mate":
                    command=f"gsettings set org.mate.background picture-filename '{folder}/{imgname}'"
                elif de=="lxde":
                    command=f"pcmanfm --set-wallpaper='{folder}/{imgname}'"
                elif de=="openbox":
                    command=f"feh --bg-scale {folder}/{imgname}"
                elif de=="icewm":
                    command=f"icewmbg --image='{folder}/{imgname}'"
                elif de=="jwm":
                    command=f"feh --no-fehbg --bg-fill '{folder}/{imgname}'"
                elif de=="afterstep":
                    command=f"fbsetbg {folder}/{imgname}"
                elif de=="trinity":
                    command=f"dcop kdesktop KBackgroundIface setWallpaper 1 '{folder}/{imgname}' 6"
                elif de=="mac":
                    command=f'osascript -e \'tell application "Finder" to set desktop picture to POSIX file "{folder}/{imgname}"'
                elif de=="windows":
                    pass
                else:
                    print("Sorry,we couldn't find a command line script that changes this DE's wallpaper. Please,report/say it to us in github.\nThanks in advance.")
                    input()
                    break_flag=True
                    break
                if de=="windows":
                    ctypes.windll.user32.SystemParametersInfoW(20, 0, f"{folder}/{imgname}" , 0)
                else:
                    os.system(command)
                time.sleep(sleep_time)
        if break_flag:
            break
