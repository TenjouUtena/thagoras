


ff = open("logging.txt","w+")

def log(line):
	ff.write(line)
	ff.write("\n")
	ff.flush()
