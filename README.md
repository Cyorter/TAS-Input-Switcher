# TAS Input Switcher

This is a Python script (obviously, at first this may be seen as lua).

This is a script for converting a TAS input between some formats for easily watch it in another emulator. This script (obviously) will not guarantee you can watch the movie from start to end with no problems, emulation differences can affect sync, but as this does not always happen, you can try.

This will work for example, if you want to watch a movie made in BizHawk but NesHawk is too slow for your computer (like me), you have probabilities of that movie will sync in Mesen or if you are really lucky, in FCEUX (yes, that's possible of sync between FCEUX and NesHawk). But there are probably other uses of this script.

# Why did you started this?

I was making a vboy TAS in BizHawk and I was curious to see if an actual ("actual" for those times) TAS made with VBjin would sync in BizHawk, but bad news, the movie importer in BizHawk can convert MC2, but only for PCE, so I said "LET'S PYTHON!".

After finishing the VBjin MC2 -> BizHawk BK2 converting, I played it in BizHawk and the result was perfect! And what is as cool as converting MC2 -> BK2 in a short time? MC2 <- BK2! Why not?! And after that I published that version of the script here, on GitHub.

With some free time and nothing to do I (bit by bit) filled the program with more formats and improvements.

Snes9X Movies support was always planned, because as Snes9X is the performance core in BizHawk and lately you can now record using Snes9X, I saw a big probability for watching these movies in the native emulator. Also, even if Snes9X and BSNES have accuracy differences is not as big to being impossible to watch between them, like case of FCEUX and NesHawk. From/To Snes9X code are complex and the hardest work, but hey, I got it to work! Thanks to the SMV documentations in TASVideos.

# Why is not there x format?

There is a reason(s) depending of the format but what I am thinking is because at least one of this:

* I do not know the format.
* The format is from an emulator that can make input recordings but not TAS recordings.
* I was not able to make a function for the format, this would be understandable, I was able to give support for SMV because I read documentations that teaches me how the format works.
* And the most probably, the support for it may be the most stupid thing I can do. For example, if I give Mupen64 <-> BizHawk N64 support, will be really unuseful and will never sync. Other examples are PSXjin, Yabause, ZSNES, Famtasia, VBA, etc.

# Why "to BizHawk" if there is already an importer?

You are probably right, but I did it anyways, to be more "complete" (I think...), I wanted to see something like "Emu 1 <-> Emu 2" and I do not want BizHawk as a exception, being like "Emu 1 <- BizHawk" or "BizHawk -> Emu 2" which are the same but you got it right? I still know and recognize the movie importer in BizHawk is better than this script.

# Why some controllers and not all?

Well, a few of them are because the emulator does not support it, I really wanted to work in Power Pad in FCEUX, but I discovered it does not support it for movies...

The rest are because they will be unuseful (e.g Mouse, Super Scope, Four Score, Justifier, Arkanoid or any Famicom expansion), if I see some TASes using them *maybe* I can work on them (issue it if you see it necessary). (Fun fact: an Arkanoid TAS exists but I am not convinced to use it, as is the only game I know to use that controller).

# How to use (copypastes)

* __FCEUX__
	* From ~: Only Standard controllers and Zapper supported. Power Pad is not supported in FCEUX movies and Zapper must be in Port 2. Do not edit the file, I implemented a search for the beginning of the input. In cases of errors are because you are using a controller that is not Std or Zapper, if you are not using other controllers you have to open the FM2 file with a text editor (e.g Notepad++) and search in the movie info (above the first frame of input) "|0|", if there are matches delete them and try again.
	* To ~: Only Standard controllers supported, Zapper is not because has (weird) emulator code after the Fire button (the last two numbers that can be 0-AVeryHighNumber). While converting, you have to record a movie in FCEUX using the correct controller settings and stop it after some frames. After conversion, copy all the contents (Ctrl+A then Ctrl+C) to the file you created with FCEUX.

* __Mesen__
	* From ~: Standard, Zapper and Power Pad supported. Open the MMO file with an archive manager (e.g 7-Zip) and extract a file called "Input.txt", do not edit the file.
	* To ~: Standard, Zapper and Power Pad supported. While converting, record a short movie in Mesen with the correct game and controller settings and stop it after some frames. After conversion open it with an archive manager (e.g 7-Zip) and Drag'n'Drop the file into the MMO.

* __Snes9X__
	* From ~: Standard controllers 1-5 and Super Multitap is supported. Do not modify the file. Movies starting from savestate will never be supported, as you will get a warning, you can continue, but it will not sync.
	* To ~: You will need basic Hex Editing knowledges. Standard controllers 1-5 and Super Multitap is supported. While converting, record a short movie in Snes9X with the controller settings and stop it after some frames. After conversion copy all the contents with the Hex Editor (e.g XVI32) and paste it in the file you created with Snes9X, to know where to paste, look at byte 1C-1F (it is 4-byte little-endian) and the value means the byte where the input starts, it commonly is "5001" which means 0150 (because it is little-endian) so the input starts at byte 336 (0x150). Remove all bytes after the value you got at byte 1C-1F and paste the new content in the clipboard.

* __Lsnes__
	* From ~: Standard controllers 1-5, Super Multitap and Game Boy is supported. Open the LSMV file with an archive manager (e.g 7-Zip) and extract a file called "input", do not edit the file and filename.
	* To ~: Standard controllers 1-5, Super Multitap and Game Boy is supported. While converting, record a short movie in Lsnes with the controller settings and stop it after some frames. After conversion open the LSMV file with an archive manager (e.g 7-Zip) and Drag'n'Drop the file into the LSMV.

* __PCEjin/VBjin__
	* From ~: All 1-5 controllers supported. Do not modify the file, I implemented a search for the beginning of the input. In cases of errors you have to open the MC2 file with a text editor (e.g Notepad++) and search in the movie info (above the first frame of input) "|0|", if there are matches delete them and try again. For Vboy you will get a warning if your movie file has 2-5 players, but you can continue. 
	* To ~: All 1-5 controllers supported. While converting, you have to record a movie in PCEjin/VBjin using the correct controller settings and stop it after some frames. After conversion, copy all the contents (Ctrl+A then Ctrl+C) to the file you created with PCEjin/VBjin.

* __BizHawk__
	* From ~: All controllers mentioned above supported. Open the BK2 file with an archive manager (e.g 7-Zip) and extract a file called "Input Log.txt", do not edit the file.
	* To ~: All controllers mentioned above supported. While converting, record a short movie in BizHawk with the correct game and settings and stop it after some frames. After conversion open it with an archive manager (e.g 7-Zip) and Drag'n'Drop the file into the BK2.

After all this copypaste, hope you understand all this and this script being useful for you.
