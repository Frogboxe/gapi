"""
Created on the 29th of September, 2017
(incorrect metadata because of renaming from contants.py to k.py)

[11/10] Contains a bunch of globals. Currently mostly for input.

"""
import json

class Key:
    keyToName = dict()
    nameToKey = dict()
    @staticmethod
    def to_string(keycode:int):
        return Key.keyToName[keycode]

    @staticmethod
    def to_key(name:str):
        return Key.nameToKey[name]
        
    @staticmethod
    def populate(pop):
        for char in range(26): # letters
            Key.add_definition(chr(char+97).upper(), char+97)
        for char in range(12): # f<n> keys
            Key.add_definition("F"+str(char+1), char+282)
        for char in range(10):
            Key.add_definition("N"+str(char), char+48)
        for char in range(10): # numpad numbers
            Key.add_definition("NUMPAD"+str(char), char+256)
        for key, val in pop.items():
            Key.add_definition(val, int(key))

    @staticmethod
    def add_definition(name, key):
        setattr(Key, name, key)
        Key.keyToName[key] = name
        Key.nameToKey[name] = key

class Mouse:
    L_CLICK = 1
    M_CLICK = 2
    R_CLICK = 3
    ROLL_UP = 4
    ROLL_DN = 5

class Colour:
    @staticmethod
    def populate(pop):
        for key, val in pop.items():
            setattr(Colour, key, Colour.deserialise(val))

    @staticmethod
    def serialise(col):
        _int = 0
        for i in range(4):
            assert col[i] < 2**8, "COL '{}' TOO LARGE! DOESN'T FIT IN 32 BITS".format(col)
            _int += col[i]*(256**(3-i))
        return _int

    @staticmethod
    def deserialise(_int):
        assert _int < 2**32, "INT '{}' TOO LARGE! DOESN'T FIT IN 32 BITS".format(_int)
        r = _int//(256**3)
        _int -= r*(256**3)
        g = _int//(256**2)
        _int -= g*(256**2)
        b = _int//(256)
        _int -= b*(256)
        a = _int
        return r, g, b, a

Key.populate(json.load(open("gapi/assets/keys.json", "r")))
Colour.populate(json.load(open("gapi/assets/colours.json", "r")))
