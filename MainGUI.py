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
        self.current_standings = []
        self.search_league_and_season_standings_button = Button(self.root, text="Search", height=1, width=10, command=lambda: self.update_standings_for_league_and_season(far.get_league_id(self.league_combobox.get()), self.season_combobox.get()))
        self.search_league_and_season_standings_button.grid(row=0, column=5)
        self.current_top_scorers = []
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
        Label(self.root, font=("Verdana", 13, "bold"), text="Player").grid(row=1, column=12)
        Label(self.root, font=("Verdana", 13, "bold"), text="Team").grid(row=1, column=13)
        Label(self.root, font=("Verdana", 13, "bold"), text="Goals").grid(row=1, column=14)

        for item in self.current_standings:
            item.grid_forget()
        self.current_standings = []

        standings = far.get_standings_for_league_and_season("39", "2020")
        for i in range(len(standings)):
            for j in range(len(standings[i])):
                label_to_add = Label(self.root, font=("Arial", 13), text=standings[i][j])
                label_to_add.grid(row=i+2, column=j+1)
                self.current_standings.append(label_to_add)

        self.create_top_scorers_table("39", "2020")



    def update_standings_for_league_and_season(self, league, season):
        standings = far.get_standings_for_league_and_season(league, season)
        for item in self.current_standings:
            item.grid_forget()
        self.current_standings = []

        for i in range(len(standings)):
            for j in range(len(standings[i])):
                label_to_add = Label(self.root, font=("Arial", 13), text=standings[i][j])
                label_to_add.grid(row=i+2, column=j+1)
                self.current_standings.append(label_to_add)

        self.create_top_scorers_table(league, season)

    def create_top_scorers_table(self, league, season):
        for item in self.current_top_scorers:
            item.grid_forget()
        self.current_top_scorers = []

        top_scorers = far.get_scorers_for_league_and_season(league, season)
        for i in range(len(top_scorers)):
            for j in range(len(top_scorers[i])):
                label_to_add = Label(self.root, font=("Arial", 13), text=top_scorers[i][j])
                label_to_add.grid(row=i+2, column=j+12)
                self.current_top_scorers.append(label_to_add)
        far.get_scorers_for_league_and_season(league, season)

if __name__ == '__main__':
    root = Tk()
    root.title("Football app")
    root.geometry("1300x700")
    root.resizable(False, False)
    MainGUI(root)
    root.mainloop()
