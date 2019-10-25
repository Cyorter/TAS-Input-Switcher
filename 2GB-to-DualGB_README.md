# 2GB to DualGB joiner

This tool copies 2 Game Boy (Gambatte and possibly GBHawk) input files to a Dual Game Boy input file for DualGambatte in BizHawk.
This is my first Python script and probably this may be written better, but it's not bad at all, works perfectly.
Hope this script is useful for what you want to do.

WARNING:
Be sure that both input files length the same in frames, otherwise it'll finish sooner than expected.
	For avoiding the above, you may add some frames (|.........|) to the file that needs it until they length the same, it's easy.
Be sure that there's not Input Log.txt while joining or the file it's empty.

Instructions:
1. Extract the Input Log.txt from the first bk2 you'll use with this tool and assign it a simple name (gb1.txt, left, a).
2. Repeat for the second bk2 you'll use.
3. Open the tool with Python 3 and type filenames of both files (including the .txt if has).
4. You'll see the progress in the interactive window, that's what it's writing in the new file.
5. While joining, record a new bk2 in BizHawk with the DualGambatte core, and them stop recording (you can step frames before stopping for being sure).
6. After join is finished press "any" key and place the new Input Log.txt into the bk2 you recently created.
	Taking advantage you have still bk2 opened as zip, you may also edit the rerecord count in Header file (obviously, left + right or right + left).
7. Enjoy the joined input!
