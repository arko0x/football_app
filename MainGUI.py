from tkinter import *
from tkinter.ttk import Combobox
from tkinter.ttk import Separator
import football_api_requests as far


class MainGUI:
    def __initialize_countries_scrollbar_with_buttons(self, countries):
        self.countries_frame = Frame(self.main_frame)
        self.countries_frame.grid(row=0, column=0)
        self.countries_canvas = Canvas(self.countries_frame, width=80, height=700)
        self.countries_canvas.pack(side=LEFT, fill=BOTH, expand=1)
        self.countries_scrollbar = Scrollbar(self.countries_frame, orient=VERTICAL, command=self.countries_canvas.yview)
        self.countries_scrollbar.pack(side=RIGHT, fill=Y)
        self.countries_canvas.configure(yscrollcommand=self.countries_scrollbar.set)
        self.countries_canvas.bind("<Configure>", lambda e: self.countries_canvas.configure(
            scrollregion=self.countries_canvas.bbox("all")))
        self.countries_inner_frame = Frame(self.countries_canvas, bg="red")
        self.countries_canvas.create_window((0, 0), window=self.countries_inner_frame, anchor="nw")

        for i in range(len(countries)):
            Button(self.countries_inner_frame, text=countries[i], height=1, width=10, bg="#00203F", fg="#ADEFD1",
                   command=lambda: self.define_league_table(countries[i])).grid(
                row=i, column=0, sticky="nsew")

    def __initialize_leagues_and_seasons_frame(self):
        self.leagues_seasons_frame = Frame(self.right_frame, bg="#ADEFD1", pady=10)
        self.leagues_seasons_frame.grid(row=0, column=1, sticky="nw")
        self.league_combobox_label = Label(self.leagues_seasons_frame, text="League: ", bg="#ADEFD1", fg="#00203F")
        self.league_combobox_label.grid(row=0, column=1)
        self.league_combobox = Combobox(self.leagues_seasons_frame, value=far.get_leagues_for_country("england"),
                                        state="readonly")
        self.league_combobox.grid(row=0, column=2)
        self.season_combobox_label = Label(self.leagues_seasons_frame, text="Season: ", bg="#ADEFD1", fg="#00203F")
        self.season_combobox_label.grid(row=0, column=3)
        self.season_combobox = Combobox(self.leagues_seasons_frame, value=far.get_seasons())
        self.season_combobox.grid(row=0, column=4)
        self.search_league_and_season_standings_button = Button(self.leagues_seasons_frame, text="Search", height=1,
                                                                width=10,
                                                                bg="#00203F", fg="#ADEFD1",
                                                                command=lambda: self.update_standings_for_league_and_season(
                                                                    far.get_league_id(self.league_combobox.get()),
                                                                    self.season_combobox.get()))
        self.search_league_and_season_standings_button.grid(row=0, column=5)

    def __initialize_league_table_frame(self):
        self.league_table_frame = Frame(self.right_frame, bg="#00203F")
        self.league_table_frame.grid(row=1, column=1, sticky="n")
        self.create_league_table()

    def __init__(self, root):
        self.current_standings = []
        self.current_top_scorers = []

        self.root = root
        self.main_frame = Frame(self.root, bg="#ADEFD1")
        self.main_frame.pack(fill=BOTH, expand=1)
        self.right_frame = Frame(self.main_frame, bg="#ADEFD1")
        self.right_frame.grid(row=0, column=1, sticky="n")
        self.__initialize_countries_scrollbar_with_buttons(far.get_all_countries())
        self.__initialize_leagues_and_seasons_frame()
        self.__initialize_league_table_frame()
        self.england_button = None
        self.germany_button = None
        self.italy_button = None
        self.spain_button = None

    #
    # def init_gui(self):
    #     # self.england_button = Button(self.main_frame, text="England", height=1, width=10, bg="#00203F", fg="#ADEFD1",
    #     #                              command=lambda: self.define_league_table("england")).grid(
    #     #     row=0, column=0, sticky="nsew")
    #     # self.germany_button = Button(self.main_frame, text="Germany", height=1, width=10, bg="#00203F", fg="#ADEFD1",
    #     #                              command=lambda: self.define_league_table("germany")).grid(
    #     #     row=1, column=0, sticky="nsew")
    #     # self.italy_button = Button(self.main_frame, text="Italy", height=1, width=10, bg="#00203F", fg="#ADEFD1",
    #     #                            command=lambda: self.define_league_table("italy")).grid(row=2,
    #     #                                                                                    column=0, sticky="nsew")
    #     # self.spain_button = Button(self.main_frame, text="Spain", height=1, width=10, bg="#00203F", fg="#ADEFD1",
    #     #                            command=lambda: self.define_league_table("spain")).grid(row=3,
    #     #                                                                                    column=0, sticky="nsew")
    #     # Separator(self.main_frame, orient=VERTICAL).grid(column=0, row=0, rowspan=20, sticky="nse")
    #     # Separator(self.main_frame, orient=HORIZONTAL).grid(column=1, row=0, columnspan=20, sticky="esw")

    def define_league_table(self, country_name):
        self.league_combobox.grid_forget()
        self.league_combobox = Combobox(self.leagues_seasons_frame, value=far.get_leagues_for_country(country_name),
                                        state="readonly")
        self.league_combobox.grid(row=0, column=2)

    def create_league_table(self):
        Button(self.league_table_frame, font=("Verdana", 11, "bold"), height=1, width=5, bg="#00203F", fg="#ADEFD1",
               text="Pos.").grid(row=2, column=1, sticky="nsew")
        Button(self.league_table_frame, font=("Verdana", 11, "bold"), height=1, width=5, bg="#00203F", fg="#ADEFD1",
               text="Team").grid(row=2, column=2)
        Button(self.league_table_frame, font=("Verdana", 11, "bold"), height=1, width=5, bg="#00203F", fg="#ADEFD1",
               text="Pts").grid(row=2, column=3)
        Button(self.league_table_frame, font=("Verdana", 11, "bold"), height=1, width=5, bg="#00203F", fg="#ADEFD1",
               text="Games").grid(row=2, column=4)
        Button(self.league_table_frame, font=("Verdana", 11, "bold"), height=1, width=5, bg="#00203F", fg="#ADEFD1",
               text="W").grid(row=2, column=5)
        Button(self.league_table_frame, font=("Verdana", 11, "bold"), height=1, width=5, bg="#00203F", fg="#ADEFD1",
               text="D").grid(row=2, column=6)
        Button(self.league_table_frame, font=("Verdana", 11, "bold"), height=1, width=5, bg="#00203F", fg="#ADEFD1",
               text="L").grid(row=2, column=7)
        Button(self.league_table_frame, font=("Verdana", 11, "bold"), height=1, width=5, bg="#00203F", fg="#ADEFD1",
               text="Gs.").grid(row=2, column=8)
        Button(self.league_table_frame, font=("Verdana", 11, "bold"), height=1, width=5, bg="#00203F", fg="#ADEFD1",
               text="Gc.").grid(row=2, column=9)
        Button(self.league_table_frame, font=("Verdana", 11, "bold"), height=1, width=5, bg="#00203F", fg="#ADEFD1",
               text="Gd.").grid(row=2, column=10)
        Button(self.league_table_frame, font=("Verdana", 11, "bold"), height=1, width=5, bg="#00203F", fg="#ADEFD1",
               text="Player").grid(row=2, column=12)
        Button(self.league_table_frame, font=("Verdana", 11, "bold"), height=1, width=5, bg="#00203F", fg="#ADEFD1",
               text="Team").grid(row=2, column=13)
        Button(self.league_table_frame, font=("Verdana", 11, "bold"), height=1, width=5, bg="#00203F", fg="#ADEFD1",
               text="Goals").grid(row=2, column=14)

        for item in self.current_standings:
            item.grid_forget()
        self.current_standings = []

        standings = far.get_standings_for_league_and_season("39", "2020")
        for i in range(len(standings)):
            for j in range(len(standings[i])):
                label_to_add = Label(self.league_table_frame, font=("Arial", 13), bg="#00203F", fg="#ADEFD1",
                                     text=standings[i][j])
                label_to_add.grid(row=i + 3, column=j + 1)
                self.current_standings.append(label_to_add)

        self.create_top_scorers_table("39", "2020")

    def update_standings_for_league_and_season(self, league, season):
        standings = far.get_standings_for_league_and_season(league, season)
        for item in self.current_standings:
            item.grid_forget()
        self.current_standings = []

        for i in range(len(standings)):
            for j in range(len(standings[i])):
                label_to_add = Entry(self.countries_frame, font=("Arial", 13), bg="#00203F", fg="#ADEFD1",
                                     text=standings[i][j])
                label_to_add.grid(row=i + 2, column=j + 1)
                self.current_standings.append(label_to_add)

        self.create_top_scorers_table(league, season)

    def create_top_scorers_table(self, league, season):
        for item in self.current_top_scorers:
            item.grid_forget()
        self.current_top_scorers = []

        top_scorers = far.get_scorers_for_league_and_season(league, season)
        for i in range(len(top_scorers)):
            for j in range(len(top_scorers[i])):
                label_to_add = Label(self.main_frame, font=("Arial", 13), bg="#ADEFD1", fg="#00203F",
                                     text=top_scorers[i][j])
                label_to_add.grid(row=i + 2, column=j + 12)
                self.current_top_scorers.append(label_to_add)
        far.get_scorers_for_league_and_season(league, season)


if __name__ == '__main__':
    root = Tk()
    root.title("Football app")
    root.geometry("1300x700")
    root.configure(bg="#ADEFD1")
    root.resizable(False, False)
    MainGUI(root)
    root.mainloop()
