
import pickle

def Save(worlds, prefs=None):
	f = open('thagoras.wld', 'wb')
	pickle.dump(worlds, f)
	pickle.dump(prefs, f)
	f.close()


def Load():
	worlds = []
	prefs = {}
	f = open('thagoras.wld', 'rb')
	worlds = pickle.load(f)
	try:
		prefs = pickle.load(f)
	except EOFError:
		pass  ## Just means this isn't the correct version
	f.close()

	return [worlds,prefs]

def LoadSafe():
	try:
		return Load()
	except IOError:
		return None
















