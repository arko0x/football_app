from tkinter import *
from tkinter.ttk import Combobox
from tkinter.ttk import Separator
import football_api_requests as far


class MainGUI:
    def __init__(self, root):
        self.root = root
        self.england_button = None
        self.germany_button = None
        self.italy_button = None
        self.spain_button = None
        self.league_combobox_label = None
        self.league_combobox = None
        self.season_combobox_label = None
        self.season_combobox = None
        self.init_gui()

    def init_gui(self):
        self.england_button = Button(self.root, text="England", height=1, width=10,
                                     command=lambda: self.define_league_table("england")).grid(
            row=0, column=0, padx=10)
        self.germany_button = Button(self.root, text="Germany", height=1, width=10,
                                     command=lambda: self.define_league_table("germany")).grid(
            row=1, column=0)
        self.italy_button = Button(self.root, text="Italy", height=1, width=10,
                                   command=lambda: self.define_league_table("italy")).grid(row=2,
                                                                                           column=0)
        self.spain_button = Button(self.root, text="Spain", height=1, width=10,
                                   command=lambda: self.define_league_table("spain")).grid(row=3,
                                                                                           column=0)
        Separator(self.root, orient=VERTICAL).grid(column=0, row=0, rowspan=20, sticky="nse")
        Separator(self.root, orient=HORIZONTAL).grid(column=1, row=0, columnspan=20, sticky="esw")
        self.league_combobox_label = Label(root, text="Liga: ")
        self.league_combobox_label.grid(row=0, column=1)
        self.league_combobox = Combobox(root, value=far.get_leagues_for_country("england"), state="readonly")
        self.league_combobox.grid(row=0, column=2)
        self.season_combobox_label = Label(self.root, text="Season: ")
        self.season_combobox_label.grid(row=0, column=3)
        self.season_combobox = Combobox(root, value=far.get_seasons())
        self.season_combobox.grid(row=0, column=4)
        self.create_league_table()

    def define_league_table(self, country_name):
        self.league_combobox.grid_forget()
        self.league_combobox = Combobox(self.root, value=far.get_leagues_for_country(country_name), state="readonly")
        self.league_combobox.grid(row=0, column=2)

    def create_league_table(self):
        sample_data = [(1, "Manchester United", 60, 20, 20, 0, 0, 54, 22, 32),
                       (2, "Manchester United", 60, 20, 20, 0, 0, 54, 22, 32),
                       (3, "Manchester United", 60, 20, 20, 0, 0, 54, 22, 32),
                       (4, "Manchester United", 60, 20, 20, 0, 0, 54, 22, 32),
                       (5, "Manchester United", 60, 20, 20, 0, 0, 54, 22, 32),
                       (6, "Manchester United", 60, 20, 20, 0, 0, 54, 22, 32),
                       (7, "Manchester United", 60, 20, 20, 0, 0, 54, 22, 32),
                       (8, "Manchester United", 60, 20, 20, 0, 0, 54, 22, 32),
                       (9, "Manchester United", 60, 20, 20, 0, 0, 54, 22, 32),
                       (10, "Manchester United", 60, 20, 20, 0, 0, 54, 22, 32)]

        Label(self.root, font=("Verdana", 13, "bold"), text="Pos.").grid(row=1, column=1)
        Label(self.root, font=("Verdana", 13, "bold"), text="Team").grid(row=1, column=2)
        Label(self.root, font=("Verdana", 13, "bold"), text="Pts").grid(row=1, column=3)
        Label(self.root, font=("Verdana", 13, "bold"), text="Games").grid(row=1, column=4)
        Label(self.root, font=("Verdana", 13, "bold"), text="W").grid(row=1, column=5)
        Label(self.root, font=("Verdana", 13, "bold"), text="D").grid(row=1, column=6)
        Label(self.root, font=("Verdana", 13, "bold"), text="L").grid(row=1, column=7)
        Label(self.root, font=("Verdana", 13, "bold"), text="Gs.").grid(row=1, column=8)
        Label(self.root, font=("Verdana", 13, "bold"), text="Gc.").grid(row=1, column=9)
        Label(self.root, font=("Verdana", 13, "bold"), text="Gd.").grid(row=1, column=10)
        for i in range(10):
            for j in range(10):
                Label(self.root, font=("Arial", 13), text=sample_data[i][j]).grid(row=i+2, column=j+1)


if __name__ == '__main__':
    root = Tk()
    root.title("Football app")
    root.geometry("1000x700")
    root.resizable(False, False)
    MainGUI(root)
    root.mainloop()
