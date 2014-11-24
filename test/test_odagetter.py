import OdaGetter

getter = OdaGetter.OdaGetter()

def test_get_stemme():
	assert getter.get_stemme(5) == 