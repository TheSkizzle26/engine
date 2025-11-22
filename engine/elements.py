class Element:
    def __init__(self, singleton=False, custom_id=None):
        self._singleton = singleton
        self._name = self.__class__.__name__ if not custom_id else custom_id

        self.e = elems
        self.e.register(self)

    def delete(self):
        self.e.delete(self)

    def update(self):
        ...

    def  render(self):
        ...

class ElementSingleton(Element):
    def __init__(self, custom_id=None):
        super().__init__(singleton=True, custom_id=custom_id)

class Elements:
    def __init__(self):
        self.elems = {
            "groups": {},
            "singletons": {}
        }

    def delete(self, elem):
        if elem._singleton:
            return
        if elem._name not in self.elems["groups"]:
            return

        self.elems["groups"][elem._name].remove(elem)

    def register(self, elem):
        if elem._singleton:
            self.elems["singletons"][elem._name] = elem
        else:
            self.elems["groups"].setdefault(elem, []).append(elem)

    def __getitem__(self, key):
        return self.elems["singletons"][key]

    def group(self, key):
        if key in self.elems["groups"]:
            return self.elems["groups"][key]

        return []


elems = Elements()