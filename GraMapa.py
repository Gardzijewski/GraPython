import time
import os
import abc

class Drawable(abc.ABC):
    def __init__(self, kolor = 1, kolor_tla = 2, symbol = ' ') -> None:
        self.kolor = kolor
        self.kolor_tla = kolor_tla
        self.symbol = symbol
        
    @abc.abstractmethod
    def Rysuj(self, x,y ):
        pass

class Wektor3D:
    def __init__(self, x=0, y=0, z=0) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f'({self.x}, {self.y}, {self.z})'
    
    def __mul__(self, mnożnik):
        if type(mnożnik) == float:
            return Wektor3D(self.x*mnożnik, self.y*mnożnik, self.z*mnożnik)
        elif type(mnożnik) == Wektor3D:
            return Wektor3D(self.x*mnożnik.x, self.y*mnożnik.y, self.z*mnożnik.z)
        
    
    def __iadd__(self, dodana):
        self.x += dodana.x
        self.y += dodana.y
        self.z += dodana.z
        return self
    
    def __add__(self, dodana):
        return Wektor3D(self.x+dodana.x, self.y+dodana.y, self.z+dodana.z)

class Postać(Drawable):
    def __init__(self, nazwa: str, masa = 0.0, położenie_początkowe = Wektor3D(0,0,0), kolor = 0, tło = 0) -> None:
        super().__init__(kolor, tło)
        self.predkosc = Wektor3D()
        self.__położenie = położenie_początkowe
        self.nazwa = nazwa
        self.masa = masa
        @property
        def x(self):
            return self.__położenie.x
        @property
        def y(self):
            return self.__położenie.y
        @property
        def z(self):
            return self.__położenie.z
        @x.setter
        def x(self, v):
            if(v < 20):
                self.__położenie.x = v
            else:
                self.__położenie.x = 20
        @y.setter
        def y(self, v):
            if(v < 20):
                self.__położenie.y = v
            else:
                self.__położenie.y = 20
        @z.setter
        def z(self, v):
            self.__położenie.z = v
            

    def __str__(self) -> str:
        # return f'{self.nazwa} {self.położenie}'
        return f'\x1b[3;{30+self.kolor};{40+self.kolor_tla}m\x1b[{int(self.__położenie.x)};{int(self.__położenie.y)}H{self.nazwa}\x1b[0m'

    def przenieś(self, dt, przyspieszenie = Wektor3D(0,0,0)) -> None:
        self.predkosc += przyspieszenie*dt
        # self.położenie += self.predkosc*dt
        self.__położenie = self.__położenie + self.predkosc*dt
        
        
    def Rysuj(self):
        print(f'\x1b[3;{30+self.kolor};{40+self.kolor_tla  }m\x1b[{int(self.__położenie.x)};{int(self.__położenie.y)}H{self.nazwa}\x1b[0m') 



class Działka(Drawable):
    def __init__(self, x = 1, y = 1) -> None:
        super().__init__()
        self.x = x
        self.y = y
        self.kolor_tła = 10
        self.kolor_symbolu = 55
        self.symbol = ' '
        
    def Rysuj(self) -> None:
        print(f'\x1b[{self.x};{self.y}H\x1b[38;5;{self.kolor_symbolu}m\x1b[48;5;{self.kolor_tła}m{self.symbol}\x1b[0m')
     
     
class Trawa(Działka):
    def __init__(self, x=1, y=1) -> None:
        super().__init__(x, y)
        
        self.zapach = True
        
        self.kolor_tła = 49
        self.kolor_symbolu = 70
        self.symbol = '\u2591'
   
class Piasek(Działka):
    def __init__(self, x=1, y=1) -> None:
        super().__init__(x, y)
        
        self.wilgotność = 0.4
        
        self.kolor_tła = 120
        self.kolor_symbolu = 170
        self.symbol = '\u2591'
   
class Drzewo(Działka):
    def __init__(self, x=1, y=1) -> None:
        super().__init__(x, y)
        
        self.wysokość = 2.5
        
        self.kolor_tła = 13
        self.kolor_symbolu = 89
        self.symbol = '\u2591'
   
class Woda(Działka):
    def __init__(self, x=1, y=1) -> None:
        super().__init__(x, y)
        
        self.głębokość = 0.5
        
        self.kolor_tła = 77
        self.kolor_symbolu = 33
        self.symbol = '\u2591'
   
   
class Mapa:
    def __init__(self, pola) -> None:
        self.pola = []
        self.importuj(pola)
    
    def importuj(self, pola):
        self.pola=[]
        for x, wiersz in enumerate(pola):
            wiersz_obiektow = []
            for y, typ_pola in enumerate(wiersz):
                if typ_pola == 'T':
                    pole = Trawa(x,y)
                elif typ_pola == 'W':
                        pole = Woda(x,y)
                elif typ_pola == 'P':
                        pole = Piasek(x,y)
                elif typ_pola == 'D':
                        pole = Drzewo(x,y)
                wiersz_obiektow.append(pole)
            self.pola.append(wiersz_obiektow)
            
    def Rysuj(self):
        os.system('cls')
        for wiersz in self.pola:
            for pole in wiersz:
                pole.Rysuj()
                
        



pionek = Postać("X", kolor=3)
pionek.x=50

#ionek2 = Postać("Y", kolor=5)

pola = [
    ['T','W','W','P','P','T','D','D','T','T'],
    ['T','D','D','W','W','T','W','D','T','T'],
    ['W','W','D','W','W','T','D','D','T','T'],
    ['T','D','P','D','P','D','P','D','W','W'],
    ['P','P','W','P','P','W','P','P','W','W'],
    ['P','D','P','W','P','T','P','P','W','W'],
    ['W','T','W','D','P','T','P','P','W','D'],
    ['D','D','T','T','P','T','P','P','D','W'],
    ['T','T','W','P','P','T','D','D','D','P'],
]

m = Mapa(pola)
m.Rysuj()

pionek.Rysuj()


# poprzedni_czas = time.time()
# while True:
#     czas = time.time()
#     dt = czas - poprzedni_czas
#     poprzedni_czas = czas

#     os.system('cls')
#     pionek.przenieś(dt, Wektor3D(0.1, 0.5, 0))
#     pionek2.przenieś(dt, Wektor3D(0.15, 0.99, 0))
#     print(pionek)
print(pionek.x)