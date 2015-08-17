
import pickle

def Save(worlds):
	f = open('thagoras.wld', 'wb')
	pickle.dump(worlds, f)
	f.close()


def Load():
	worlds = []
	f = open('thagoras.wld', 'rb')
	worlds = pickle.load(f)
	f.close()

	return [worlds,]

def LoadSafe():
	try:
		return Load()
	except IOError:
		return None
















