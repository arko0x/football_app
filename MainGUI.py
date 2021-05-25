from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
import football_api_requests as far
from TeamInfoGUI import *


class MainGUI:
    STANDINGS_INFO_LENGTH = 10
    HEADING_SIZE = 15
    STANDINGS_ELEM_SIZE = 11
    PLAYER_INFO_ELEM_SIZE = 10

    def __init__(self, root):
        self.current_standings = []
        self.current_top_scorers = []
        self.teams_sort_info = [False for i in range(self.STANDINGS_INFO_LENGTH)]

        self.root = root
        self.main_frame = Frame(self.root, bg="#ADEFD1")
        self.main_frame.pack(fill=BOTH, expand=1)
        self.right_frame = Frame(self.main_frame, bg="#ADEFD1")
        self.right_frame.grid(row=0, column=1, sticky="n")
        self.__initialize_countries_scrollbar_with_buttons(far.get_all_countries())
        self.__initialize_leagues_and_seasons_frame()
        self.__initialize_league_table_frame()
        self.__set_default_values_for_combobox_widgets()

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
        self.countries_buttons = []
        for i in range(len(countries)):
            self.countries_buttons.append(
                Button(self.countries_inner_frame, text=countries[i], height=1, width=10, bg="#00203F", fg="#ADEFD1",
                       command=lambda j=i: self.define_league_table(countries[j])))
            self.countries_buttons[i].grid(
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
                                                                command=lambda:
                                                                self.update_standings_for_league_and_season(
                                                                    far.get_league_id(self.league_combobox.get()),
                                                                    self.season_combobox.get()))
        self.search_league_and_season_standings_button.grid(row=0, column=5)

    def __set_default_values_for_combobox_widgets(self):
        self.league_combobox["values"] = far.get_leagues_for_country("England")
        self.league_combobox.current(0)
        self.season_combobox["values"] = far.get_seasons()
        self.season_combobox.current(12)

    def __initialize_league_table_frame(self):
        self.league_table_frame = Frame(self.right_frame, bg="#00203F")
        self.league_table_frame.grid(row=1, column=1, sticky="n")
        self.create_league_table()

    def define_league_table(self, country_name):
        self.league_combobox.grid_forget()
        self.league_combobox = Combobox(self.leagues_seasons_frame, value=far.get_leagues_for_country(country_name),
                                        state="readonly")
        self.league_combobox.grid(row=0, column=2)

    def create_league_table(self):
        Label(self.league_table_frame, text="League table", font=("Verdana", MainGUI.HEADING_SIZE, "bold"),
              bg="#00203F",
              fg="#ADEFD1").grid(row=2, column=1, columnspan=10)
        Label(self.league_table_frame, text="Top scorers", font=("Verdana", MainGUI.HEADING_SIZE, "bold"), bg="#00203F",
              fg="#ADEFD1").grid(row=2, column=12, columnspan=3)
        Button(self.league_table_frame, font=("Verdana", MainGUI.STANDINGS_ELEM_SIZE, "bold"), height=1, width=5,
               bg="#00203F", fg="#ADEFD1",
               text="Pos.", command=lambda: self.sort_league_table(0)).grid(row=3, column=1, sticky="nsew")
        Button(self.league_table_frame, font=("Verdana", MainGUI.STANDINGS_ELEM_SIZE, "bold"), height=1, width=5,
               bg="#00203F", fg="#ADEFD1",
               text="Team", command=lambda: self.sort_league_table(1)).grid(row=3, column=2)
        Button(self.league_table_frame, font=("Verdana", MainGUI.STANDINGS_ELEM_SIZE, "bold"), height=1, width=5,
               bg="#00203F", fg="#ADEFD1",
               text="Pts", command=lambda: self.sort_league_table(2)).grid(row=3, column=3)
        Button(self.league_table_frame, font=("Verdana", MainGUI.STANDINGS_ELEM_SIZE, "bold"), height=1, width=5,
               bg="#00203F", fg="#ADEFD1",
               text="Games", command=lambda: self.sort_league_table(3)).grid(row=3, column=4)
        Button(self.league_table_frame, font=("Verdana", MainGUI.STANDINGS_ELEM_SIZE, "bold"), height=1, width=5,
               bg="#00203F", fg="#ADEFD1",
               text="W", command=lambda: self.sort_league_table(4)).grid(row=3, column=5)
        Button(self.league_table_frame, font=("Verdana", MainGUI.STANDINGS_ELEM_SIZE, "bold"), height=1, width=5,
               bg="#00203F", fg="#ADEFD1",
               text="D", command=lambda: self.sort_league_table(5)).grid(row=3, column=6)
        Button(self.league_table_frame, font=("Verdana", MainGUI.STANDINGS_ELEM_SIZE, "bold"), height=1, width=5,
               bg="#00203F", fg="#ADEFD1",
               text="L", command=lambda: self.sort_league_table(6)).grid(row=3, column=7)
        Button(self.league_table_frame, font=("Verdana", MainGUI.STANDINGS_ELEM_SIZE, "bold"), height=1, width=5,
               bg="#00203F", fg="#ADEFD1",
               text="Gs.", command=lambda: self.sort_league_table(7)).grid(row=3, column=8)
        Button(self.league_table_frame, font=("Verdana", MainGUI.STANDINGS_ELEM_SIZE, "bold"), height=1, width=5,
               bg="#00203F", fg="#ADEFD1",
               text="Gc.", command=lambda: self.sort_league_table(8)).grid(row=3, column=9)
        Button(self.league_table_frame, font=("Verdana", MainGUI.STANDINGS_ELEM_SIZE, "bold"), height=1, width=5,
               bg="#00203F", fg="#ADEFD1",
               text="Gd.", command=lambda: self.sort_league_table(9)).grid(row=3, column=10)
        Button(self.league_table_frame, font=("Verdana", MainGUI.STANDINGS_ELEM_SIZE, "bold"), height=1, width=5,
               bg="#00203F", fg="#ADEFD1",
               text="Player").grid(row=3, column=12)
        Button(self.league_table_frame, font=("Verdana", MainGUI.STANDINGS_ELEM_SIZE, "bold"), height=1, width=5,
               bg="#00203F", fg="#ADEFD1",
               text="Team").grid(row=3, column=13)
        Button(self.league_table_frame, font=("Verdana", MainGUI.STANDINGS_ELEM_SIZE, "bold"), height=1, width=5,
               bg="#00203F", fg="#ADEFD1",
               text="Goals").grid(row=3, column=14)

        standings = far.get_standings_for_league_and_season("39", "2020")
        self.__update_standings(standings)

        self.create_top_scorers_table("39", "2020")

    def update_standings_for_league_and_season(self, league, season):
        standings = far.get_standings_for_league_and_season(league, season)
        if not standings:
            messagebox.showerror("No data found", "No data found for given league and season.")
        else:
            self.__update_standings(standings)
            self.create_top_scorers_table(league, season)

    def __update_standings(self, standings):
        self.__forget_standings()
        self.__show_new_standings(standings)

    def create_top_scorers_table(self, league, season):
        for item in self.current_top_scorers:
            item.grid_forget()
        self.current_top_scorers = []

        top_scorers = far.get_scorers_for_league_and_season(league, season)
        for i in range(len(top_scorers)):
            for j in range(len(top_scorers[i])):
                label_to_add = Label(self.league_table_frame, font=("Arial", MainGUI.STANDINGS_ELEM_SIZE),
                                     bg="#00203F", fg="#D6ED17",
                                     text=top_scorers[i][j])
                label_to_add.grid(row=i + 4, column=j + 12)
                self.current_top_scorers.append(label_to_add)

    def sort_league_table(self, index):
        _list = []
        list_to_add = []
        for i in range(len(self.current_standings)):
            if i % MainGUI.STANDINGS_INFO_LENGTH != 0 or i == 0:
                list_to_add.append(self.current_standings[i]["text"])
                if i == len(self.current_standings) - 1:
                    _list.append(list_to_add)
            else:
                _list.append(list_to_add)
                list_to_add = [self.current_standings[i]["text"]]

        if index != 1:
            _list.sort(key=lambda e: int(e[index]), reverse=self.teams_sort_info[index])
        else:
            _list.sort(key=lambda e: e[index], reverse=self.teams_sort_info[index])

        was_reversed = self.teams_sort_info[index]
        self.teams_sort_info = [False for i in range(self.STANDINGS_INFO_LENGTH)]
        self.teams_sort_info[index] = False if was_reversed else True

        self.__forget_standings()
        self.__show_new_standings(_list)

    def __forget_standings(self):
        for item in self.current_standings:
            item.grid_forget()

        self.current_standings = []

    def __show_new_standings(self, standings):
        for i in range(len(standings)):
            for j in range(len(standings[i])):
                label_to_add = Label(self.league_table_frame, font=("Arial", MainGUI.STANDINGS_ELEM_SIZE), bg="#00203F",
                                     fg="#ADEFD1",
                                     text=standings[i][j])
                label_to_add.grid(row=i + 4, column=j + 1)
                self.current_standings.append(label_to_add)
                if j % 10 == 1:
                    label_to_add.bind("<Button-1>", lambda x, team_name=self.current_standings[-1].cget("text"): self.__show_team_info_window(team_name, self.season_combobox.get()))
                    label_to_add["cursor"] = "hand2"

    def __show_team_info_window(self, team_name, season):
        TeamInfoGUI(self.root, team_name, season)



if __name__ == '__main__':
    root = Tk()
    root.title("Football app")
    root.geometry("1300x700")
    root.configure(bg="#ADEFD1")
    root.resizable(False, False)
    MainGUI(root)
    root.mainloop()
