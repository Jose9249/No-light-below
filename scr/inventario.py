class Inventory:
    def __init__(self) -> None:
        self.objetos = {}
        #self.MAX_OBJECTS = 10
    
    def add(self, object, quantity):
        if object in self.objetos:
            self.objetos[object] += quantity
        else:
            self.objetos[object] = quantity

    def remove(self, object, quantity):
        if object in self.objetos:
            self.objetos[object] -= quantity
            if self.objetos[object] <= 0:
                del self.objetos[object]
    
    def get_item_list(self):
        return [f"{nombre} x{cantidad}" for nombre, cantidad in self.objetos.items()]
