# Vboy MC2 - BK2 TAS switcher

As BizHawk only imports mc2 files from PCEjin, I wanted to make again a Python script similar to my 2gb to dualgb converter.
This script as title says, will convert your mc2 input file made with VBjin to a BizHawk input file (bk2). BUT! Also converts from BizHawk (bk2) to VBjin (mc2).

WARNING: POWER BUTTON UNSUPPORTED FOR NOW.

This script will only do the hardest work for you, you have still to do the rest (the easy work), and as the use isn't too obvious, here's the instructions:

__Convert from MC2 to BK2:__

* Open your mc2 file with a Notepad (Gedit/Notepad++) of your choice and remove the metadata content inside it, keeping only the input in the file.
	* If you don't want to lose your rerecord count you may note it in another place (unless you can remember it in your mind).
	* You can also rename the file with a simple name, just make sure it has extension mc2 or ends with mc2 if hasn't extension.
* Open the script and type the filename and press ENTER, the convert process will begin.
* While converting, create a bk2 file with BizHawk, step a few frames and stop recording.
	* Optional: If you want to copy the rerecord count open bk2 as a zip file and edit the Header file with the actual rerecord count you have.
* After conversion finished, place the Input Log.txt in the bk2 file, and you'll have finished.

__Convert from BK2 to MC2:__

* Open your bk2 file as a zip file and extract the Input Log.txt (but don't modify that input file).
	* As above, you can rename the input file with a simple name, just make sure it has extension txt or ends with txt if hasn't extension.
* Open the script and type the filename and press ENTER, the convert process will begin. (copy-paste ftw).
* While converting, create a mc2 file with VBjin, step a few frames and stop recording.
	* Optional: If you want to copy the rerecord count open mc2 with a Notepad and edit rerecord count with the actual you have.
* After conversion finished, copy the input in converted file and paste it in the mc2 created in VBjin, so you'll have finished.
