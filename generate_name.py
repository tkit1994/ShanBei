import os 
word_list_downloaded = [os.path.basename(i).split(".")[0] for i in os.listdir("./download")]

# sorted(filenamelist, key=lambda x:os.path.getmtime("./download/{}".format(x)))
with open("word.txt", 'r') as f:
    word_list = f.read().splitlines()
word_list_ordered = [i for i in word_list if i in word_list_downloaded]
sorted_filenamelist = [f"{i}.mp3" for i in word_list_ordered]
with open("./filenamelist.txt", 'w') as f:
	for filename in sorted_filenamelist:
		f.write("file './download/{}'\n".format(filename))
		f.write("file './space.mp3'\n")
		f.write("file './download/{}'\n".format(filename))
		f.write("file './space.mp3'\n")
