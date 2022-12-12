from tkinter import *
import sqlite3

# Okno aplikacji
root = Tk()
root.title('Baza danych przychodni lekarskiej')
root.geometry("360x450")



conn = sqlite3.connect('C:/Users/Hubert/Desktop/Testy/baza.db')

c = conn.cursor()



c.execute("""CREATE TABLE IF NOT EXISTS pacjenci (
            imie text,
            nazwisko text,
            rok_urodzenia integrer,
            pesel integrer 
            )""")



# Tworzę funkcję edytowania
def update():
    conn = sqlite3.connect('C:/Users/Hubert/Desktop/Testy/baza.db')
    c = conn.cursor()

    record_id = delete_box.get()

    c.execute("""UPDATE pacjenci SET
		imie = :imie,
		nazwisko = :nazwisko,
		rok_urodzenia = :rok_urodzenia,
		pesel = :pesel
		WHERE oid = :oid """,
              {
                  'imie': imie_editor.get(),
                  'nazwisko': nazwisko_editor.get(),
                  'rok_urodzenia': rok_urodzenia_editor.get(),
                  'pesel': pesel_editor.get(),
                  'oid': record_id
              })


    conn.commit()


    conn.close()

    editor.destroy()
    root.deiconify()


# Funkcja edytowania rekordów
def edit():
    root.withdraw()
    global editor
    editor = Tk()
    editor.title('Edycja')
    editor.geometry("400x150")
    conn = sqlite3.connect('C:/Users/Hubert/Desktop/Testy/baza.db')
    c = conn.cursor()

    record_id = delete_box.get()
    c.execute("SELECT * FROM pacjenci WHERE oid = " + record_id)
    records = c.fetchall()

    # Zmienne
    global imie_editor
    global nazwisko_editor
    global rok_urodzenia_editor
    global pesel_editor

    # wprowadzenia textu
    imie_editor = Entry(editor, width=30)
    imie_editor.grid(row=0, column=1, padx=20)
    nazwisko_editor = Entry(editor, width=30)
    nazwisko_editor.grid(row=1, column=1)
    rok_urodzenia_editor = Entry(editor, width=30)
    rok_urodzenia_editor.grid(row=2, column=1)
    pesel_editor = Entry(editor, width=30)
    pesel_editor.grid(row=3, column=1)

    # Etykiety
    imie_label = Label(editor, text="Imie")
    imie_label.grid(row=0, column=0)
    nazwisko_label = Label(editor, text="Nazwisko")
    nazwisko_label.grid(row=1, column=0)
    rok_urodzenia_label = Label(editor, text="Rok urodzenia")
    rok_urodzenia_label.grid(row=2, column=0)
    pesel_label = Label(editor, text="Numer pesel")
    pesel_label.grid(row=3, column=0)

    # wyniki
    for record in records:
        imie_editor.insert(0, record[0])
        nazwisko_editor.insert(0, record[1])
        rok_urodzenia_editor.insert(0, record[2])
        pesel_editor.insert(0, record[3])

    # Przycisk zapisywania/edytowania
    edit_btn = Button(editor, text="Zapisz", command=update)
    edit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=145)


# Funkcja usuwania rekordów
def delete():
    conn = sqlite3.connect('C:/Users/Hubert/Desktop/Testy/baza.db')
    c = conn.cursor()

    c.execute("DELETE from pacjenci WHERE oid = " + delete_box.get())

    delete_box.delete(0, END)

    conn.commit()

    conn.close()


# Funkcja dodawania rekordów
def submit():
    conn = sqlite3.connect('C:/Users/Hubert/Desktop/Testy/baza.db')
    c = conn.cursor()

    c.execute("INSERT INTO pacjenci VALUES (:imie, :nazwisko, :rok_urodzenia, :pesel)",
              {
                  'imie': imie.get(),
                  'nazwisko': nazwisko.get(),
                  'rok_urodzenia': rok_urodzenia.get(),
                  'pesel': pesel.get()
              })

    conn.commit()

    conn.close()

    # Usuwanie zawartości wpisanych w okna do wprowadzania textu
    imie.delete(0, END)
    nazwisko.delete(0, END)
    rok_urodzenia.delete(0, END)
    pesel.delete(0, END)


# Funkcja wyświetlania wyników
def query():
    conn = sqlite3.connect('C:/Users/Hubert/Desktop/Testy/baza.db')
    c = conn.cursor()

    c.execute("SELECT *, oid FROM pacjenci")
    records = c.fetchall()

    # Wyświetlanie listy pacjentów
    print_records = ''
    for record in records:
        print_records += str(record[4])+ " " + str(record[0]) + " " + str(record[1]) + " " + str(record[2]) + " " + str(record[3]) + "\n"
    else:
        print('brak pacjenta z takim ID')

    query_label = Label(root, text=print_records)
    query_label.grid(row=12, column=0, columnspan=2)

    conn.commit()

    conn.close()


# Tworzenie pól do wprowadzania textu
imie = Entry(root, width=30)
imie.grid(row=0, column=1, padx=20)
nazwisko = Entry(root, width=30)
nazwisko.grid(row=1, column=1)
rok_urodzenia = Entry(root, width=30)
rok_urodzenia.grid(row=2, column=1)
pesel = Entry(root, width=30)
pesel.grid(row=3, column=1)
delete_box = Entry(root, width=30)
delete_box.grid(row=9, column=1, pady=5)

# Etykiety
imie_label = Label(root, text="Imie")
imie_label.grid(row=0, column=0)
nazwisko_label = Label(root, text="Nazwisko")
nazwisko_label.grid(row=1, column=0)
rok_urodzenia_label = Label(root, text="Rok urodzenia")
rok_urodzenia_label.grid(row=2, column=0)
pesel_label = Label(root, text="Numer pesel")
pesel_label.grid(row=3, column=0)
delete_box_label = Label(root, text="Wybierz ID")
delete_box_label.grid(row=9, column=0, pady=5)

# Przycisk dodawania pacjentów
submit_btn = Button(root, text="Dodaj pacjenta", command=submit)
submit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

# Przycisk wyświetlania pacjentów
query_btn = Button(root, text="Wyświetl pacjentów", command=query)
query_btn.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=85)

# Przycisk usuwania pacjenta
delete_btn = Button(root, text="Usuń wybranego pacjenta", command=delete)
delete_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=70)

# Przycisk edycji
edit_btn = Button(root, text="Edytuj pacjenta", command=edit)
edit_btn.grid(row=11, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

conn.commit()

conn.close()

root.mainloop()
