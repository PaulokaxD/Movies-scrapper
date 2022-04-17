import tkinter as tk
from scrapper import Scrapper


class Window(tk.Frame):
    def __init__(self, cargar, master=None) -> None:
        tk.Frame.__init__(self, master)
        self.master = master

        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        fileMenu = tk.Menu(menu)
        fileMenu.add_command(label="Cargar", command=cargar)
        fileMenu.add_command(label="Listar")
        fileMenu.add_command(label="Salir", command=exit)
        menu.add_cascade(label="Datos", menu=fileMenu)

        editMenu = tk.Menu(menu)
        editMenu.add_command(label="Título")
        editMenu.add_command(label="Fecha")
        editMenu.add_command(label="Género")
        menu.add_cascade(label="Buscar", menu=editMenu)


class GUI(Window):
    scrapper: Scrapper

    def upload(self) -> None:
        number = self.scrapper.update_database()
        number_window = tk.Toplevel(self)
        number_window.title("Number of elements")
        display = tk.Label(number_window, text=f"There are {number} elements")
        display.grid(row=0, column=0, columnspan=3)
        # Ponerla gonita

    def __init__(self, scrapper, master=None) -> None:
        self.scrapper = scrapper
        super().__init__(self.upload, master)


movies_scrapper = Scrapper("https://www.elseptimoarte.net/estrenos/", "movies.db")

root = tk.Tk()
app = GUI(movies_scrapper, root)
# app = Window(root)
root.wm_title("Buscador de peliculas")

root.mainloop()
