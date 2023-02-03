from PIL import Image
import random

# Nachfragen wie viele Startkeime es geben soll
print("Gib an wie viele Keime du haben willst.")
anzahlkeime = int(input())
#Aufforderung für jeden Startkeim folgende Parameter zu übergeben
print("Gib für jeden Keim folgende Werte in der richtigen Reihenfolge an: (PositionX, PositionY, Enstehungszeitpunkt, vN, vO, vS, vW)")
#Abspeichern der Parameter in der Liste parameter
parameter = []
parameter=[[] for i in range (anzahlkeime)]
for i in range (anzahlkeime):
    parameter[i] = input()
#Die Eingabe muss wie verlangt erfolgen: 7 Werte in einer Zeile, durch Kommas getrennt.
#Trennen der Zeilen in Listen von einzelnen Werte und Abspeichern in der Liste newparameter.
newparameter = []
newparameter=[[] for i in range (anzahlkeime)]
for i in range (len(parameter)):
    newparameter[i].extend(parameter[i].split(","))
#Alle Werte der Liste newparameter als int-Werte konvertieren
for i in range(len(newparameter)):
    for j in range(len(newparameter[i])):
        newparameter[i][j]=int(newparameter[i][j])
#Überprüfung, ob es auch wirklich genau 7 Parameter gibt
for i in range(len(newparameter)):
    if len(newparameter[i]) != 7:
        print("Starte das Programm neu. Die Parameter wurden nicht passend übergeben.")
        quit()
        
#Für jeden Keim eine Farbe hinzufügen. Zunächst erlaube ich alle Farben. Erst am Ende werden Farben im Sinne der
#Aufgabenstellung in Grautöne umgewandelt.        
#Liste mit allen verwendeten Farben. Zunächst enthält sie nur die Farbe weiß (255, 255, 255) für die noch leere Fläche. 
farbliste=[[255, 255, 255]]
#Funktion zum Erstellen einer Zufallsfarbe
def farbeerstellen():
    return random.sample(range(255), 3)
for i in range(len(newparameter)):
    zufallsfarbe= farbeerstellen()
    #Überprüfen, ob es die Farbe in der Liste farbliste schon gibt 
    while(zufallsfarbe in farbliste):
        zufallsfarbe= farbeerstellen()
    #Wenn nicht wird die neu erstellte Farbe zur Liste farbliste hinzugefügt
    farbliste.append(zufallsfarbe)
    newparameter[i].append((zufallsfarbe[0], zufallsfarbe[1], zufallsfarbe[2]))

hoehe= 300
breite=300

#Erstellen eines neuen Bildes mit den Maßen breite, hoehe, das nur weiß ist
bild = Image.new(mode = "RGB",size = (breite,hoehe),color = (255, 255, 255))

returnwert = True
#Variable für den aktuellen Durchlauf vom Bild
aktuellerschritt= 1
#Dauerschleife, die solange alle Bildpixel immer wieder von vorne durchläuft, bis keiner mehr weiß gefärbt ist
while(returnwert==True):
    #zweidimensinale Liste time für jeden einzelnen Pixel im Bild.
    #Bedeutung: Das ist für neu eingefärbte Pixel die verstrichene Zeit vom Beginn des aktuellen Durchlaufs der while-Schleife bis zur Einfärbung.
    time=[[] for x in range(breite)]
    #jeder Platz in der liste bekommt den Wert 0
    for h in range(breite):
        time[h]=[0 for x in range(hoehe)]
    returnwert = False
    #Überprüfen, ob einer der Keime im aktuellen Durchgang seinen Entstehungszeitpunkt hat.
    #Falls ja und der Enstehungspunkt noch weiß ist, wird der entsprechende Pixel mit der Farbe des Kristalls eingefärbt
    for i in range(len(newparameter)):
        if newparameter[i][2]==aktuellerschritt:
            if bild.getpixel((newparameter[i][0],newparameter[i][1])) == (255, 255, 255):
                bild.putpixel((newparameter[i][0],newparameter[i][1]),newparameter[i][7])
                returnwert = True
    
    #Variable für Wachstum der Kristalle. Das Wachstum wird in smooth Schritte geteilt, um ein glatteres Ergebnis zu erhalten.
    smooth=6
    for k in range(1,1+smooth):
        #Durchlaufen aller Pixel des Bildes
        for y in range(hoehe):
            for x in range(breite):
                #Pixel finden, der nicht weiß ist
                if bild.getpixel((x,y))!=(255, 255, 255):
                    #zugehörigen Keim finden
                    for i in range(len(newparameter)):
                        if bild.getpixel((x,y))== newparameter[i][7]:
                            aktuellerkeim = i
                    #Ausbreitung des Keims in alle Richtungen in Abhängigkeit von der Wachstumsgeschwindigkeit
                    #Wachstum nach oben
                    streckeO = newparameter[aktuellerkeim][3]*((k/smooth)-time[x][y])
                    if streckeO + 0.000000001 >= 1:
                        if y>0:
                            if bild.getpixel((x,y-1))==(255, 255, 255):
                                bild.putpixel((x,y-1), newparameter[aktuellerkeim][7])
                                time[x][y-1]= time[x][y]+(1/newparameter[aktuellerkeim][3])
                                returnwert = True

                    #Wachstum nach rechts
                    streckeR = newparameter[aktuellerkeim][4]*((k/smooth)-time[x][y])
                    if streckeR + 0.000000001 >= 1:
                        if x+1<=breite-1: 
                            if bild.getpixel((x+1,y))==(255, 255, 255):
                                bild.putpixel((x+1,y), newparameter[aktuellerkeim][7])
                                time[x+1][y]= time[x][y]+(1/newparameter[aktuellerkeim][4])
                                returnwert = True

                    #Wachstum nach unten
                    streckeU = newparameter[aktuellerkeim][5]*((k/smooth)-time[x][y])
                    if streckeU + 0.000000001 >= 1:
                        if y+1<=hoehe-1: 
                            if bild.getpixel((x,y+1))==(255, 255, 255):
                                bild.putpixel((x,y+1), newparameter[aktuellerkeim][7])
                                time[x][y+1]= time[x][y]+(1/newparameter[aktuellerkeim][5])
                                returnwert = True

                    #Wachstum nach links
                    streckeL = newparameter[aktuellerkeim][6]*((k/smooth)-time[x][y])
                    if streckeL + 0.000000001 >= 1:
                        if x>0: 
                            if bild.getpixel((x-1,y))==(255, 255, 255):
                                bild.putpixel((x-1,y), newparameter[aktuellerkeim][7])
                                time[x-1][y]= time[x][y]+(1/newparameter[aktuellerkeim][6])
                                returnwert = True
                            
    aktuellerschritt = aktuellerschritt+1
 
    
#Alle Farben in Grauwerte konvertieren und Ausgabe des schwarz-weiß Bildes
graubild= bild.convert('L')
graubild.show()

        
    



