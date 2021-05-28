from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from tkinter import filedialog
import football_api_requests as far
import utils
from TeamInfoGUI import *


class MainGUI:
    STANDINGS_INFO_LENGTH = 10
    HEADING_SIZE = 15
    STANDINGS_ELEM_SIZE = 11
    PLAYER_INFO_ELEM_SIZE = 10
    DEFAULT_SEASON = "2020"
    DEFAULT_COUNTRY = "England"
    DEFAULT_LEAGUE = "39"
    APP_GREEN_COLOR = "#ADEFD1"
    APP_BLUE_COLOR = "#00203F"
    APP_PLAYER_INFO_COLOR = "#D6ED17"
    DEFAULT_APP_FONT = "Verdana"

    def __init__(self, root):
        self.current_standings = []
        self.current_top_scorers = []
        self.teams_sort_info = [False for _ in range(self.STANDINGS_INFO_LENGTH)]
        self.current_season = MainGUI.DEFAULT_SEASON

        self.root = root
        self.main_frame = Frame(self.root, bg=MainGUI.APP_GREEN_COLOR)
        self.main_frame.pack(fill=BOTH, expand=1)
        self.right_frame = Frame(self.main_frame, bg=MainGUI.APP_GREEN_COLOR)
        self.right_frame.grid(row=0, column=1, sticky="n")
        self.__initialize_menu_bar()
        self.__initialize_countries_scrollbar_with_buttons(far.get_all_countries())
        self.__initialize_leagues_and_seasons_frame()
        self.__initialize_league_table_frame()
        self.__set_default_values_for_combobox_widgets()

    def __initialize_menu_bar(self):
        self.menu = Menu(self.root)
        self.filemenu = Menu(self.menu, tearoff=0)
        self.filemenu.add_command(label="Export league table as excel file", command=self.__export_xlsx)
        self.filemenu.add_command(label="Export league table as .txt file", command=self.__export_txt)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        root.config(menu=self.menu)

    def __initialize_countries_scrollbar_with_buttons(self, countries):
        self.countries_frame = Frame(self.main_frame)
        self.countries_frame.grid(row=0, column=0)
        self.countries_canvas = Canvas(self.countries_frame, width=80, height=565)
        self.countries_canvas.pack(side=LEFT, fill=BOTH, expand=1)
        self.countries_scrollbar = Scrollbar(self.countries_frame, orient=VERTICAL, command=self.countries_canvas.yview)
        self.countries_scrollbar.pack(side=RIGHT, fill=Y)
        self.countries_canvas.configure(yscrollcommand=self.countries_scrollbar.set)
        self.countries_canvas.bind("<Configure>", lambda e: self.countries_canvas.configure(
            scrollregion=self.countries_canvas.bbox("all")))
        self.countries_inner_frame = Frame(self.countries_canvas)
        self.countries_canvas.create_window((0, 0), window=self.countries_inner_frame, anchor="nw")
        self.countries_buttons = []
        for i in range(len(countries)):
            self.countries_buttons.append(
                Button(self.countries_inner_frame, text=countries[i], height=1, width=10, bg=MainGUI.APP_BLUE_COLOR,
                       fg=MainGUI.APP_GREEN_COLOR,
                       command=lambda j=i: self.__update_league_combobox(countries[j])))
            self.countries_buttons[i].grid(
                row=i, column=0, sticky="nsew")

    def __initialize_leagues_and_seasons_frame(self):
        self.leagues_seasons_frame = Frame(self.right_frame, bg=MainGUI.APP_GREEN_COLOR, pady=10)
        self.leagues_seasons_frame.grid(row=0, column=1, sticky="nw")
        self.league_combobox_label = Label(self.leagues_seasons_frame, text="League: ", bg=MainGUI.APP_GREEN_COLOR,
                                           fg=MainGUI.APP_BLUE_COLOR)
        self.league_combobox_label.grid(row=0, column=1)
        self.league_combobox = Combobox(self.leagues_seasons_frame, value=far.get_leagues_for_country(MainGUI.DEFAULT_COUNTRY),
                                        state="readonly")
        self.league_combobox.grid(row=0, column=2)
        self.season_combobox_label = Label(self.leagues_seasons_frame, text="Season: ", bg=MainGUI.APP_GREEN_COLOR, fg=MainGUI.APP_BLUE_COLOR)
        self.season_combobox_label.grid(row=0, column=3)
        self.season_combobox = Combobox(self.leagues_seasons_frame, value=far.get_seasons())
        self.season_combobox.grid(row=0, column=4)
        self.search_league_and_season_standings_button = Button(self.leagues_seasons_frame, text="Search", height=1,
                                                                width=10,
                                                                bg=MainGUI.APP_BLUE_COLOR, fg=MainGUI.APP_GREEN_COLOR,
                                                                command=lambda:
                                                                self.update_standings_for_league_and_season(
                                                                    far.get_league_id(self.league_combobox.get()),
                                                                    self.season_combobox.get()))
        self.search_league_and_season_standings_button.grid(row=0, column=5)

    def __initialize_league_table_frame(self):
        self.league_table_frame = Frame(self.right_frame, bg=MainGUI.APP_BLUE_COLOR)
        self.league_table_frame.grid(row=1, column=1, sticky="n")
        self.__create_league_table()

    def __set_default_values_for_combobox_widgets(self):
        self.league_combobox["values"] = far.get_leagues_for_country(MainGUI.DEFAULT_COUNTRY)
        self.league_combobox.current(0)
        self.season_combobox["values"] = far.get_seasons()
        self.season_combobox.current(12)

    def __update_league_combobox(self, country_name):
        self.league_combobox.grid_forget()
        self.league_combobox = Combobox(self.leagues_seasons_frame, value=far.get_leagues_for_country(country_name),
                                        state="readonly")
        self.league_combobox.grid(row=0, column=2)

    def __create_league_table(self):
        Label(self.league_table_frame, text="League table", font=(MainGUI.DEFAULT_APP_FONT, MainGUI.HEADING_SIZE, "bold"),
              bg=MainGUI.APP_BLUE_COLOR, fg=MainGUI.APP_GREEN_COLOR).grid(row=2, column=1, columnspan=10)
        Label(self.league_table_frame, text="Top scorers", font=(MainGUI.DEFAULT_APP_FONT, MainGUI.HEADING_SIZE, "bold"),
              bg=MainGUI.APP_BLUE_COLOR, fg=MainGUI.APP_GREEN_COLOR).grid(row=2, column=12, columnspan=3)
        Button(self.league_table_frame, font=(MainGUI.DEFAULT_APP_FONT, MainGUI.STANDINGS_ELEM_SIZE, "bold"), height=1, width=5,
               bg=MainGUI.APP_BLUE_COLOR, fg=MainGUI.APP_GREEN_COLOR,
               text="Pos.", command=lambda: self.__sort_league_table(0)).grid(row=3, column=1, sticky="nsew")
        Button(self.league_table_frame, font=(MainGUI.DEFAULT_APP_FONT, MainGUI.STANDINGS_ELEM_SIZE, "bold"), height=1, width=5,
               bg=MainGUI.APP_BLUE_COLOR, fg=MainGUI.APP_GREEN_COLOR,
               text="Team", command=lambda: self.__sort_league_table(1)).grid(row=3, column=2)
        Button(self.league_table_frame, font=(MainGUI.DEFAULT_APP_FONT, MainGUI.STANDINGS_ELEM_SIZE, "bold"), height=1, width=5,
               bg=MainGUI.APP_BLUE_COLOR, fg=MainGUI.APP_GREEN_COLOR,
               text="Pts", command=lambda: self.__sort_league_table(2)).grid(row=3, column=3)
        Button(self.league_table_frame, font=(MainGUI.DEFAULT_APP_FONT, MainGUI.STANDINGS_ELEM_SIZE, "bold"), height=1, width=5,
               bg=MainGUI.APP_BLUE_COLOR, fg=MainGUI.APP_GREEN_COLOR,
               text="Games", command=lambda: self.__sort_league_table(3)).grid(row=3, column=4)
        Button(self.league_table_frame, font=(MainGUI.DEFAULT_APP_FONT, MainGUI.STANDINGS_ELEM_SIZE, "bold"), height=1, width=5,
               bg=MainGUI.APP_BLUE_COLOR, fg=MainGUI.APP_GREEN_COLOR,
               text="W", command=lambda: self.__sort_league_table(4)).grid(row=3, column=5)
        Button(self.league_table_frame, font=(MainGUI.DEFAULT_APP_FONT, MainGUI.STANDINGS_ELEM_SIZE, "bold"), height=1, width=5,
               bg=MainGUI.APP_BLUE_COLOR, fg=MainGUI.APP_GREEN_COLOR,
               text="D", command=lambda: self.__sort_league_table(5)).grid(row=3, column=6)
        Button(self.league_table_frame, font=(MainGUI.DEFAULT_APP_FONT, MainGUI.STANDINGS_ELEM_SIZE, "bold"), height=1, width=5,
               bg=MainGUI.APP_BLUE_COLOR, fg=MainGUI.APP_GREEN_COLOR,
               text="L", command=lambda: self.__sort_league_table(6)).grid(row=3, column=7)
        Button(self.league_table_frame, font=(MainGUI.DEFAULT_APP_FONT, MainGUI.STANDINGS_ELEM_SIZE, "bold"), height=1, width=5,
               bg=MainGUI.APP_BLUE_COLOR, fg=MainGUI.APP_GREEN_COLOR,
               text="Gs.", command=lambda: self.__sort_league_table(7)).grid(row=3, column=8)
        Button(self.league_table_frame, font=(MainGUI.DEFAULT_APP_FONT, MainGUI.STANDINGS_ELEM_SIZE, "bold"), height=1, width=5,
               bg=MainGUI.APP_BLUE_COLOR, fg=MainGUI.APP_GREEN_COLOR,
               text="Gc.", command=lambda: self.__sort_league_table(8)).grid(row=3, column=9)
        Button(self.league_table_frame, font=(MainGUI.DEFAULT_APP_FONT, MainGUI.STANDINGS_ELEM_SIZE, "bold"), height=1, width=5,
               bg=MainGUI.APP_BLUE_COLOR, fg=MainGUI.APP_GREEN_COLOR,
               text="Gd.", command=lambda: self.__sort_league_table(9)).grid(row=3, column=10)
        Button(self.league_table_frame, font=(MainGUI.DEFAULT_APP_FONT, MainGUI.STANDINGS_ELEM_SIZE, "bold"), height=1, width=5,
               bg=MainGUI.APP_BLUE_COLOR, fg=MainGUI.APP_GREEN_COLOR,
               text="Player").grid(row=3, column=12)
        Button(self.league_table_frame, font=(MainGUI.DEFAULT_APP_FONT, MainGUI.STANDINGS_ELEM_SIZE, "bold"), height=1, width=5,
               bg=MainGUI.APP_BLUE_COLOR, fg=MainGUI.APP_GREEN_COLOR,
               text="Team").grid(row=3, column=13)
        Button(self.league_table_frame, font=(MainGUI.DEFAULT_APP_FONT, MainGUI.STANDINGS_ELEM_SIZE, "bold"), height=1, width=5,
               bg=MainGUI.APP_BLUE_COLOR, fg=MainGUI.APP_GREEN_COLOR,
               text="Goals").grid(row=3, column=14)

        standings = far.get_standings_for_league_and_season(MainGUI.DEFAULT_LEAGUE, MainGUI.DEFAULT_SEASON)
        self.__update_standings(standings)

        self.__create_top_scorers_table(MainGUI.DEFAULT_LEAGUE, MainGUI.DEFAULT_SEASON)

    def update_standings_for_league_and_season(self, league, season):
        standings = far.get_standings_for_league_and_season(league, season)
        if not standings:
            messagebox.showerror("No data found", "No data found for given league and season.")
        else:
            self.current_season = season
            self.__update_standings(standings)
            self.__create_top_scorers_table(league, season)

    def __update_standings(self, standings):
        self.__forget_standings()
        self.__show_new_standings(standings)

    def __create_top_scorers_table(self, league, season):
        for item in self.current_top_scorers:
            item.grid_forget()
        self.current_top_scorers = []

        top_scorers = far.get_scorers_for_league_and_season(league, season)
        for i in range(len(top_scorers)):
            for j in range(len(top_scorers[i])):
                label_to_add = Label(self.league_table_frame, font=("Arial", MainGUI.STANDINGS_ELEM_SIZE),
                                     bg=MainGUI.APP_BLUE_COLOR, fg=MainGUI.APP_PLAYER_INFO_COLOR,
                                     text=top_scorers[i][j])
                label_to_add.grid(row=i + 4, column=j + 12)
                self.current_top_scorers.append(label_to_add)

    def __sort_league_table(self, index):
        _list = self.__get_standings_as_list_of_lists()

        if index != 1:
            _list.sort(key=lambda e: int(e[index]), reverse=self.teams_sort_info[index])
        else:
            _list.sort(key=lambda e: e[index], reverse=self.teams_sort_info[index])

        was_reversed = self.teams_sort_info[index]
        self.teams_sort_info = [False for _ in range(self.STANDINGS_INFO_LENGTH)]
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
                label_to_add = Label(self.league_table_frame, font=("Arial", MainGUI.STANDINGS_ELEM_SIZE), bg=MainGUI.APP_BLUE_COLOR,
                                     fg=MainGUI.APP_GREEN_COLOR,
                                     text=standings[i][j])
                label_to_add.grid(row=i + 4, column=j + 1)
                self.current_standings.append(label_to_add)
                if j % 10 == 1:
                    label_to_add.bind("<Button-1>", lambda x, team_name=self.current_standings[-1].cget(
                        "text"): self.__show_team_info_window(team_name))
                    label_to_add["cursor"] = "hand2"

    def __show_team_info_window(self, team_name):
        TeamInfoGUI(self.root, team_name, self.current_season)

    def __export_xlsx(self):
        filepath = filedialog.asksaveasfilename(filetypes=(
            ("Excel files", "*.xlsx"),
        ))
        data = self.__get_standings_as_list_of_lists()
        utils.export_xlsx(filepath, data)

    def __export_txt(self):
        filepath = filedialog.asksaveasfilename(filetypes=(
            ("txt files", "*.txt"),
        ))
        data = self.__get_standings_as_list_of_lists()
        utils.export_txt(filepath, data)

    def __get_standings_as_list_of_lists(self):
        data = []
        list_to_add = []
        for i in range(len(self.current_standings)):
            if i % MainGUI.STANDINGS_INFO_LENGTH != 0 or i == 0:
                list_to_add.append(self.current_standings[i]["text"])
                if i == len(self.current_standings) - 1:
                    data.append(list_to_add)
            else:
                data.append(list_to_add)
                list_to_add = [self.current_standings[i]["text"]]

        return data


if __name__ == '__main__':
    root = Tk()
    root.title("Football app")
    root.geometry("1300x700")
    root.configure(bg=MainGUI.APP_GREEN_COLOR)
    root.resizable(False, False)
    MainGUI(root)
    root.mainloop()
