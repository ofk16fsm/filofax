# Titel: Filofax
# Författare: Ferhat Sevim
# Datum: 2018-08-26
#
# Det här är ett program för att skriva dagliga anteckningar.
# Programmet sparar anteckningarna i en textfil med namnet anteckning.txt


from datetime import datetime
from tkinter import *
from tkinter import messagebox

FILENAME = "anteckning.txt"


class MyFirstGui:
    def __init__(self, master, notes):
        self.master = master
        self.notes = notes
        master.title("En anteckning GUI")
        self.frame = Frame(master, relief=RAISED, borderwidth=1)
        self.frame.pack(fill=BOTH, expand=True)
        self.label = Label(self.frame, text="This is my first GUI!")
        self.label.pack()

        self.menuVar = StringVar()
        self.menu_label = Label(self.frame, text="Menu", textvariable=self.menuVar, justify=LEFT)
        self.menu_label.pack()
        self.menu_label.place(x=150, y=100)

        self.menu_button = Button(self.frame, text="Meny", command=self.menuNote)
        self.menu_button.pack(side=RIGHT, padx=15, pady=10)
        self.menu_button.place(x=5, y=20)

        self.add_button = Button(self.frame, text="Lägg till", command=self.addNote)
        self.add_button.pack(side=RIGHT, padx=10, pady=10)
        self.add_button.place(x=60, y=20)

        self.sort_button = Button(self.frame, text="Sortera", command=self.sortedNote)
        self.sort_button.pack(side=RIGHT, padx=5, pady=5)
        self.sort_button.place(x=125, y=20)

        self.forwardClicks = -1
        self.forward_button = Button(self.frame, text="Framåt", command=self.forwardNote)
        self.forward_button.pack(side=RIGHT, padx=20, pady=10)
        self.forward_button.place(x=185, y=20)

        self.backClicks = 0
        self.back_button = Button(self.frame, text="Bakåt", command=self.backNote)
        self.back_button.pack(side=RIGHT, padx=35, pady=10)
        self.back_button.place(x=245, y=20)

        self.save_button = Button(self.frame, text="Spara", command=self.saveNote)
        self.save_button.pack(side=RIGHT, padx=55, pady=10)
        self.save_button.place(x=300, y=20)

        self.remove_button = Button(self.frame, text="Ta bort", command=self.removeNote)
        self.remove_button.pack(side=RIGHT, padx=85, pady=10)
        self.remove_button.place(x=350, y=20)

        self.close_button = Button(self.frame, text="Stäng", command=self.master.quit)
        self.close_button.pack(side=RIGHT, padx=105, pady=10)
        self.close_button.place(x=405, y=20)

        self.date_label = Label(self.frame, text="Date", anchor=W)
        self.date_label.pack(side=LEFT)
        self.date_label.place(x=5, y=75)

        self.date_entry = Entry(self.frame)
        self.date_entry.pack(side=LEFT)
        self.date_entry.place(x=40, y=75)

        self.text_label = Label(self.frame, text="Text", anchor=W)
        self.text_label.pack(side=LEFT)
        self.text_label.place(x=170, y=75)

        self.text_entry = Entry(self.frame)
        self.text_entry.pack(side=LEFT)
        self.text_entry.place(x=200, y=75)

        self.noteVar = StringVar()
        self.note_label = Label(self.frame, textvariable=self.noteVar, justify=LEFT)
        self.note_label.pack()
        self.note_label.place(x=50, y=200)


    def sortedNote(self):
        self.noteVar.set("\n".join(str(i) for i in self.notes.notes_sorted))

    def addNote(self):
        date = "".join(date_control(self.date_entry.get()))
        text = self.text_entry.get()
        note = Note(date, text)
        self.notes.addNote(note)

    def menuNote(self):
        self.menuVar.set("\n".join(i for i in show_menu()))

    def forwardNote(self):
        self.forwardClicks += 1
        self.noteVar.set("".join(str(i) for i in self.notes.browse(int(self.forwardClicks))))

    def backNote(self):
        self.backClicks -= 1
        self.noteVar.set("".join(str(i) for i in self.notes.browse(int(self.backClicks))))

    def saveNote(self):
        global FILENAME
        self.notes.saveNote(FILENAME)

    def removeNote(self):
        self.noteVar.set("".join(str(i) for i in self.notes.removed))


# Klassen Notesides skapar en ny anteckning
class Note:
    def __init__(self, date, text):
        self.date = date
        self.text = text

    # Det används för att läsa ett objekt som en textsträng
    def __repr__(self):
        return "{}: {}".format(self.date, self.text)  # Returnerar som textsträng.
        # return f"{self.date}: {self.text}" #Det här är det nya sträng format i Python version 3.7.0.


# Klassen Note som bläddrar framåt, bakåt, lägger till en ny anteckning och raderar alla anteckningar.
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
            yield self.sides[sidenum]
        except IndexError as ie:  # Jag använder try except för att undvika avbrytningar.
            messagebox.showinfo('Index Error', ie)

    # Lägger till en ny anteckning
    def addNote(self, myNote):
        return self.sides.append(myNote)

    # Sparar alla anteckningar sorterade till filen anteckning.txt
    def saveNote(self, filename):
        with open(filename, "w") as w_file:
            for line in self.notes_sorted:
                w_file.write("".join(line.date) + ": " + "".join(line.text))
                w_file.write("\n")
        w_file.close()

    # Raderar en anteckning i filen anteckning.txt
    @property
    def removed(self):
        side = self.side
        self.sides.remove(side)
        return "Följande anteckning tas bort: {}".format(side)

    # Sorterar anteckningar med datum ordning
    @property
    def notes_sorted(self):
        sortedNotesides = sorted(self.sides, key=lambda line: line.date)
        return sortedNotesides  # Returnerar sorterade anteckningar med datum ordning mha metoden sorted och lambda.


# Jag skapar menyn som beskriver vad jag ska göra i programmet.
def show_menu():
    menu = ["Bläddra framåt", "Bläddra bakåt", "Lägg till en ny anteckning", "Ta bort denna anteckning",
            "Visa alla anteckningar", "Avsluta programmet"]
    return menu


# Jag ska kontrollera om datumet är i rätt ordning.
def date_control(correct_date):
    while True:
        try:
            # correct_date = input("Ange datum på följande sätt: ÅÅÅÅ-MM-DD\n")
            if datetime.strptime(correct_date, "%Y-%m-%d"):
                yield correct_date
                break
            else:
                continue

        except ValueError:  # Jag har undantag för att undvika värde fel om man matar in fel datum format.
            messagebox.showinfo('Value Error', 'Ange rätt datum, borde vara ÅÅÅÅ-MM-DD')
            break


# Huvud programmet
def main():
    global FILENAME
    notes = Notesides(FILENAME)
    root = Tk()
    root.geometry("500x400")
    MyFirstGui(root, notes)
    root.mainloop()
    '''
    # Semikolon gör att jag kan ha variablar och konstarter på samma rad.
    rotForward = 0
    rotBack = -1
    FORWARD = 1
    BACK = 2
    ADD = 3
    REMOVE = 4
    SORT = 5
    while True:
        # show_menu()
        # ny_rad()
        choice = int(input("Välj ett alternativ\n"))
        if choice == FORWARD:
            #textForward = notes.browse(rotForward)
            #print(textForward)
            #rotForward += 1
            ny_rad()
        elif choice == BACK:
            textBack = notes.browse(rotBack)
            print(textBack)
            rotBack -= 1
            ny_rad()
        elif choice == ADD:
            date = date_control()
            #date = my_gui.date_entry.get()
            text = input("Skriv in din text\n")
            #text = my_gui.text_entry.get()
            note = Note(str(date), str(text))
            notes.addNote(note)
            ny_rad()
        elif choice == REMOVE:
            removedNote = notes.removed()
            print("Följande anteckning tas bort: {}".format(removedNote))
            ny_rad()
        elif choice == SORT:
            for sortedLine in notes.notes_sorted():
                print(sortedLine)
            ny_rad()
        else:
            print("Avslutar programmet")
            break
    notes.saveNote(FILENAME)
    '''


main()
