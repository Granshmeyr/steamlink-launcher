#Steamlink Launcher for Xbian
from pathlib import Path
import fileinput
import inspect
import os
import stat
import subprocess
import sys
import xbmc
import xbmcaddon
import xbmcgui
import xml.etree.ElementTree as et

__plugin__ = "steamlink"
__author__ = "Granshmeyr"
__url__ = "https://github.com/Granshmeyr/steamlink-launcher"
__git_url__ = "https://github.com/Granshmeyr/steamlink-launcher"
__credits__ = "toast"
__version__ = "0.0.12"

dialog = xbmcgui.Dialog()
addon = xbmcaddon.Addon(id="plugin.program.steamlink")

#Main operations of this plugin
def main():
    create_files()
    sudo_set()
    sudo_check()
    settings("update")
    subprocess.Popen(["sh", "/tmp/steamlink-launcher.sh"])
    dialog.ok("Starting Steamlink", "Please wait...")

#Settings checks and management
def settings(option):
    #Check if settings file exists
    settings = Path("/home/xbian/.kodi/userdata/addon_data/plugin.program.steamlink/settings.xml")
    if not settings.is_file():
        dialog.ok("Cannot start Steamlink", "Settings not configured." + "\n" + "Please navigate to Steamlink " +
        "Launcher > Settings > Credentials, and enter the password for user \"xbian\".")
        sys.exit()
    #Make settings only readable by user "xbian"
    sts = os.stat("/home/xbian/.kodi/userdata/addon_data/plugin.program.steamlink/settings.xml")
    oct_perm = oct(sts.st_mode)
    if oct_perm != 0o100600:
        os.chmod("/home/xbian/.kodi/userdata/addon_data/plugin.program.steamlink/settings.xml", 0o100600)
    #Store or update setting values
    tree = et.parse("/home/xbian/.kodi/userdata/addon_data/plugin.program.steamlink/settings.xml")
    root = tree.getroot()
    if option == "which":
        selected = [0,0,0]
        if root[1].text == "true":
            selected[0] = 1
        if root[2].text == "true":
            selected[1] = 1
        if root[3].text == "true":
            selected[2] = 1
        return selected
    elif option == "update":
        root[1].text = "false"
        root[2].text = "false"
        tree.write("/home/xbian/.kodi/userdata/addon_data/plugin.program.steamlink/settings.xml")
    elif option == "sudo":
        return root[0].text

#Set the $STEAM_SUDO environment variable
def sudo_set():
    os.environ["STEAM_SUDO"] = settings("sudo")

#Test sudo with saved password
def sudo_check():
    check = subprocess.run(["sudo", "-S", "-v"], stderr=subprocess.PIPE, input=os.environ["STEAM_SUDO"], encoding="utf-8")
    err = check.stderr
    if err.find("incorrect") != -1:
        dialog.ok("Cannot start Steamlink", "Password for user \"xbian\" is incorrectly set." + "\n" +
        "Please update the password in Steamlink Launcher > Settings > Credentials.")
        sys.exit()

#Creates bash files to be used for this plugin
def create_files():
    #First script; launches watchdog
    with open("/tmp/steamlink-launcher.sh", "w") as outfile:
        outfile.write(inspect.cleandoc("""
        #!/bin/bash
        chmod 755 /tmp/steamlink-watchdog.sh
        echo "$STEAM_SUDO" | sudo -S openvt -c 7 -s -f clear
        echo "$STEAM_SUDO" | sudo -S --preserve-env=STEAM_SUDO nohup openvt -c 7 -s -f -l /tmp/steamlink-watchdog.sh >/dev/null 2>&1 &
        """)
        )
        outfile.close()

    #Settings which insert into watchdog if set
    setting_repository = ""
    setting_dependency = ""
    setting_wol = ""
    selected = [0,0,0]
    selected = settings("which")
    if selected[0] == 1:
        setting_repository = "sudo apt-get update" + "\n"
    if selected[1] == 1:
        setting_dependency = inspect.cleandoc("""
        if [ ! "$(dpkg --list | grep -w gnupg)" ]; then
        kodi-send.py --action="Notification(Steamlink dependencies,Installing gnupg...)"
        sudo apt-get install gnupg -y
        fi
        if [ ! "$(dpkg --list | grep -w curl)" ]; then
            kodi-send.py --action="Notification(Steamlink dependencies,Installing curl...)"
            sudo apt-get install curl -y
        fi
        if [ ! "$(dpkg --list | grep -w libgles2)" ]; then
            kodi-send.py --action="Notification(Steamlink dependencies,Installing libgles2...)"
            sudo apt-get install libgles2 -y
        fi
        if [ ! "$(dpkg --list | grep -w libegl1)" ]; then
            kodi-send.py --action="Notification(Steamlink dependencies,Installing libegl1...)"
            sudo apt-get install libegl1 -y
        fi
        if [ ! "$(dpkg --list | grep -w libgl1-mesa-dri)" ]; then
            kodi-send.py --action="Notification(Steamlink dependencies,Installing libgl1-mesa-dri...)"
            sudo apt-get install libgl1-mesa-dri -y
        fi
        if [ "$(which steamlink)" = "" ]; then
            kodi-send.py --action="Notification(Installing Steamlink,Please wait...)"
            wget https://github.com/Granshmeyr/steamlink-launcher/raw/master/steamlink.deb -P /tmp/
            sudo dpkg -i /tmp/steamlink.deb
            rm -f /tmp/steamlink.deb
        fi
        """) + "\n"
    if selected[2] == 1:
        setting_wol = inspect.cleandoc("""
        if [ -f "/home/xbian/.wakeup" ]; then
        /usr/bin/wakeonlan "$(cat "/home/xbian/.wakeup")"
        else sudo apt-get install wakeonlan -y; /usr/bin/wakeonlan "$(cat "/home/xbian/.wakeup")" 
        fi
        """) + "\n"

    #Second script, enacts settings & pauses Kodi startup until Steamlink closed
    with open("/tmp/steamlink-watchdog.sh", "w") as outfile:
        outfile.write(
        "#!/bin/bash" + "\n" +
        setting_repository +
        setting_dependency +
        setting_wol +
        inspect.cleandoc("""
        sudo stop xbmc
        sudo -u xbian --preserve-env=STEAM_SUDO steamlink
        openvt -c 7 -s -f clear
        sudo start xbmc
        """)
        )
        outfile.close()

main()
