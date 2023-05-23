import uuid

class Layout:
    def __init__(self):
        self._map = {}

    def __getitem__(self, key):
        pass

    def __setitem__(self, key, value):
        if len(key)!=2:
            raise ValueError

        if key[0] not in self._elements:

            self._elements.append(zool.Element())

class Element:
    def __init__(self):
        self._child_elements = []
        self._parent_element = None


* Need to store hierarchical relationship.
* Nee



if __name__=="__main__":
    layout = Layout()
    layout['base','A1'] = Element()     # add 
    layout['base','B1'] = Element()
    layout['base',None] = Element()
    layout['base','C1'] = Element()
