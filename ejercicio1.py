import tkinter as tk


def getMovies():
    print("funciono")
    # connection.execute()
    return


class Window(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master

        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        fileMenu = tk.Menu(menu)
        fileMenu.add_command(label="Cargar", command=getMovies)
        fileMenu.add_command(label="Listar")
        fileMenu.add_command(label="Salir", command=exit)
        menu.add_cascade(label="Datos", menu=fileMenu)

        editMenu = tk.Menu(menu)
        editMenu.add_command(label="Título")
        editMenu.add_command(label="Fecha")
        editMenu.add_command(label="Género")
        menu.add_cascade(label="Buscar", menu=editMenu)


root = tk.Tk()
app = Window(root)
root.wm_title("Buscador de peliculas")

root.mainloop()

# Usa FastAPI
# Usa el ORM de FastAPI
