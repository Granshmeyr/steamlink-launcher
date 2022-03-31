




# Steamlink Launcher for Xbian

Kodi add-on which creates a launcher for Steamlink. Only for Xbian systems. The launcher simply handles the shutdown/startup of Kodi and Steamlink. This repository is a fork of https://github.com/swetoast/steamlink-launcher, originally for OSMC.

## Installation

* Download the add-on zip file and install.
	* SSH into Xbian (default password is raspberry)
	* Exit from configuration if necessary
	* `cd ~`
	*  `wget https://github.com/Granshmeyr/steamlink-launcher-xbian/releases/download/0.0.12/plugin.program.steamlink-v0.0.12.zip`
	* Install .zip through Kodi interface (plugin zip will be located in Home)
* (Optional) If you want to send a wake-on-lan packet to your host PC on launch, navigate to Steamlink Launcher > Settings > System > Turn on "Wake-on-lan functionality"
	* Check *Notes* below for required configuration

## Security Notice
This add-on stores the password for the "xbian" user in its settings file, in plain-text. This is necessary because the "xbian" user does not have NOPASSWD set for the necessary directories, unlike on OSMC.
* The script makes the settings file read/writable only by user "xbian".
* **Your password will be visible to everyone on your local network unless you secure Xbian's Samba shares which allow guest browsing by default:**
	* SSH into Xbian (default password is raspberry)
	* Exit from configuration if necessary
	* `sudo nano /etc/samba/shares.conf`
		* Change every line that says `guest ok = yes` to `guest ok = no`
	* Create Samba password of your choice for user "xbian":
		* `sudo smbpasswd xbian`
	* Now when browsing the XBIAN Samba share from the local network, it will require you to provide the credentials you set for user "xbian"

The settings file is deleted if you select to remove it when uninstalling the Steamlink Launcher.

This add-on installs a modified `steamlink.deb` which removes the `python:any` dependency (it would cause `python2` to be needlessly installed). It also modifies the `steamlink` binary so it reads the password from the add-on settings. This allows the Steamlink scripts to run sudo commands without a user prompt. Typically this would only happen on the first run, but it requires user input on the command line.

## Notes
Startup will be quite slow on the first launch. Reasons for this below.

This add-on updates your repositories and checks for & installs Steamlink and its dependencies—only on the first run. If you need to re-run these functions, toggle on the respective options under Steamlink Launcher > Settings > System > ...on next run

Wake-on-lan functionality requires the creation of a `.wakeup` file in `/home/xbian/`
* SSH into Xbian (default password is raspberry)
* Exit from configuration if necessary
* `nano  /home/xbian/.wakeup`
* Input the MAC address of your host pc
	* Search up how to save & exit in "nano" if needed

Steamlink Launcher was tested on fresh install RPi3 with latest Xbian image as of 31/3/2022.

## Troubleshooting

* Do not report issues related to this launcher on official forums.
* You can file an issue and I will try to help.

Possible issues (copied from original repo):

If you are on RPi3+ especially, and your Steamlink immediately crashes on launch with a blurred/pixelated image:
* SSH into Xbian (default password is raspberry)
* Exit from configuration if necessary
* `sudo nano /boot/config.txt`
* Add a new line `gpu_mem=128` anywhere, or near the other similar lines for convenience.
	* Search up how to save & exit in "nano" if needed

RPi4 crashes in kernel with error message: `vc4_hdmi fef05700.hdmi: ASoC: error at snd_soc_dai_startup on fef05700.hdmi` (where's the fix?)

Source: https://steamcommunity.com/app/353380/discussions/6/3193611900710760046/#c4328520278444207948

## Credits

Full list of people that contributed to this project

* [Toast](https://github.com/swetoast) - original repository
	* [Ludeeus](https://github.com/ludeeus) - code clean up
	* [Valve/Slouken](https://github.com/swetoast/Steamlink-launcher/commits?author=slouken) - for additional code donations and for adding lib replacement for OSMC
	* [sgroen88](https://github.com/sgroen88) - adding shell execution to the script
	* [ninfur](https://github.com/ninfur) - fixing the watchdog

## Acknowledgement

© 2022 Valve Corporation. All rights reserved. Valve, Steam Link and Steam are trademarks and/or 
registered trademarks of Valve Corporation in the US and other countries. 
