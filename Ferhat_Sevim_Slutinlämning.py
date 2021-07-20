# Titel: Filofax
# Författare: Ferhat Sevim
# Datum: 2018-08-26
#
# Det här är ett program för att skriva dagliga anteckningar.
# Programmet sparar anteckningarna i en textfil med namnet anteckning.txt


from datetime import datetime


# Klassen Note skapar en ny anteckning
class Note:
    def __init__(self, date, text):
        self.date = date
        self.text = text

    # Det används för att läsa ett objekt som en textsträng
    def __repr__(self):
        return "{}: {}".format(self.date, self.text)  # Returnerar som textsträng.
        # return f"{self.date}: {self.text}" #Det här är det nya sträng format i Python version 3.7.0.


# Klassen Notesides som bläddrar framåt, bakåt, lägger till en ny anteckning, raderar en anteckning och visar på sorterat sätt.
class Notesides:
    def __init__(self, filename):
        self.sides = []
        self.side = ""
        
        with open(filename, "r") as readFile:
            for line in readFile:
                parts = line.strip().split(": ")
                note = Note(parts[0], parts[1])
                self.addNote(note)
        readFile.close()

    # Bläddra framåt
    def browse(self, rotation):
        sidenum = self.sides.index(self.sides[0])
        try:
            if sidenum < len(self.sides) - 1:
                sidenum += rotation
            else:
                sidenum = 0
            self.side = self.sides[sidenum]
            return self.sides[sidenum]
        except IndexError as ie:  # Jag använder try except för att undvika avbrytningar.
            print(ie, "\n")
   
    # Lägger till en ny anteckning
    def addNote(self, myNote):
        return self.sides.append(myNote)

    # Sparar alla anteckningar sorterade till filen anteckning.txt
    def saveNote(self, filename):
        with open(filename, "w") as w_file:
            for line in self.notes_sorted():
                w_file.write(line.date + ": " + line.text)
                w_file.write("\n")
        w_file.close()

    # Raderar denna anteckning i filen anteckning.txt
    def removed(self):
        side = self.side
        self.sides.remove(side)
        return side

    # Sorterar anteckningar med datum ordning
    def notes_sorted(self):
        sortedNotesides = sorted(self.sides, key=lambda line: line.date)
        return sortedNotesides  # Returnerar sorterade anteckningar med datum ordning mha metoden sorted och lambda.


# Jag skapar menyn som beskriver vad jag ska göra i programmet.
def show_menu():
    menu = ["Bläddra framåt", "Bläddra bakåt", "Lägg till en ny anteckning", "Ta bort denna anteckning",
            "Visa alla anteckningar", "Avsluta programmet"]
    for num, choice in enumerate(menu, 1):
        print("{}. {}".format(num, choice))


# Jag ska kontrollera om datumet är i rätt ordning.
def date_control():
    while True:

        try:
            correct_date = input("Ange datum på följande sätt: ÅÅÅÅ-MM-DD\n")
            datetime.strptime(correct_date, "%Y-%m-%d")
            return correct_date
            # noinspection PyUnreachableCode
            break
        except ValueError:  # Jag har undantag för att undvika värde fel om man matar in fel datum format.
            print("Ange rätt datum")


# Här skaffar jag en tom rad med funktion.
def new_space():
    return print()


# Huvud programmet
def main():
    FILENAME = "anteckning.txt"
    notes = Notesides(FILENAME)

    # Semikolon gör att jag kan ha variablar och konstarter på samma rad.
    rotForward = 0; rotBack = -1
    FORWARD = 1; BACK = 2; ADD = 3; REMOVE = 4; SORT = 5; QUIT = 6
    
    while True:
        try:
            show_menu()
            new_space()
            choice = int(input("Välj ett alternativ\n"))
            if choice == FORWARD:
                textForward = notes.browse(rotForward)
                print(textForward)
                rotForward += 1
                new_space()
            elif choice == BACK:
                textBack = notes.browse(rotBack)
                print(textBack)
                rotBack -= 1
                new_space()
            elif choice == ADD:
                date = date_control()
                text = input("Skriv in din text\n")
                note = Note(date, text)
                notes.addNote(note)
                new_space()
            elif choice == REMOVE:
                removedNote = notes.removed()
                print("Följande anteckning tas bort: {}".format(removedNote))
                new_space()
            elif choice == SORT:
                for sortedLine in notes.notes_sorted():
                    print(sortedLine)
                new_space()
            elif choice == QUIT:
                print("Avslutar programmet")
                break
            else:
                print("Ange en siffra mellan 1 och 6\n")
        except ValueError:
            print("Du borde använda en siffra\n")
            
    notes.saveNote(FILENAME)


main()
