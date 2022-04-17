import tkinter as tk
from scrapper import Scrapper


class Window(tk.Frame):
    def __init__(self, cargar, listar, titulo, fecha, genero, master=None) -> None:
        tk.Frame.__init__(self, master)
        self.master = master

        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        fileMenu = tk.Menu(menu)
        fileMenu.add_command(label="Cargar", command=cargar)
        fileMenu.add_command(label="Listar", command=listar)
        fileMenu.add_command(label="Salir", command=exit)
        menu.add_cascade(label="Datos", menu=fileMenu)

        editMenu = tk.Menu(menu)
        editMenu.add_command(label="Título", command=titulo)
        editMenu.add_command(label="Fecha", command=fecha)
        editMenu.add_command(label="Género", command=genero)
        menu.add_cascade(label="Buscar", menu=editMenu)


class GUI(Window):
    scrapper: Scrapper

    def upload(self) -> None:
        number = self.scrapper.update_database()
        number_window = tk.Toplevel(self)
        number_window.title("Number of elements")
        display = tk.Label(number_window, text=f"There are {number} elements")
        display.grid(row=0, column=0, columnspan=3)
        number_window.geometry("200x100")

    def show(self) -> None:
        movies = self.scrapper.show_movies()

        movies_window = tk.Toplevel(self)
        movies_window.title("List with all the films")
        movies_window.geometry("400x350")

        scrollbar = tk.Scrollbar(movies_window)
        scrollbar.pack(side="right", fill="y")
        listbox = tk.Text(movies_window)

        for title, info in movies.items():
            formatted_line = f"{title}:\nCountries:\t{' '.join(info[0])}\nDirectors:\t{' '.join(info[1])}\n\n"
            print(formatted_line)
            listbox.insert("end", formatted_line)
        listbox.pack(fill="both")

    def search_title(self) -> None:
        # TODO
        return

    def search_date(self) -> None:
        # TODO
        return

    def search_genre(self) -> None:
        # TODO
        return

    def __init__(self, scrapper, master=None) -> None:
        self.scrapper = scrapper
        super().__init__(
            self.upload,
            self.show,
            self.search_title,
            self.search_date,
            self.search_genre,
            master,
        )


movies_scrapper = Scrapper("https://www.elseptimoarte.net/estrenos/", "movies.db")

root = tk.Tk()
app = GUI(movies_scrapper, root)
# app = Window(root)
root.wm_title("Buscador de peliculas")

root.mainloop()
