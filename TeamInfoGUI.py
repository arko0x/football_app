from MainGUI import *
import utils


class TeamInfoGUI:
    NUMBER_OF_PLAYER_INFO_COLUMNS = 10

    def __init__(self, master, team_name, season):
        self.parent = master
        self.pages = 0
        self.current_page = 1
        self.players_data = []
        self.team_window = Toplevel(master=self.parent, bg="#00203F")
        self.team_name = team_name
        self.season = season
        self.show_team_info_window(self.team_name, self.season)
        self.previous_page_button = Button(self.team_window, text="<<", bg="#ADEFD1", fg="#00203F",
                                           command=self.__previous_page)
        self.previous_page_button.grid(row=21, column=0, columnspan=5, sticky="e")
        self.previous_page_button["state"] = "disabled"
        self.next_page_button = Button(self.team_window, text=">>", bg="#ADEFD1", fg="#00203F",
                                       command=self.__next_page)
        self.next_page_button.grid(row=21, column=5, columnspan=5, sticky="w")

        self.sort_info = [False for _ in range(self.NUMBER_OF_PLAYER_INFO_COLUMNS)]

    def show_team_info_window(self, team_name, season):
        players, self.pages = far.get_players_and_pages_for_team_and_season(team_name, season)

        player_label = Label(master=self.team_window, text="Player",
                             font=("Verdana", MainGUI.STANDINGS_ELEM_SIZE, "bold"),
                             bg="#00203F", fg="#ADEFD1")
        player_label.grid(row=0, column=0)
        player_label.bind("<Button-1>", lambda x: self.__sort_players_info(0))
        player_label["cursor"] = "hand2"
        age_label = Label(master=self.team_window, text="Age", font=("Verdana", MainGUI.STANDINGS_ELEM_SIZE, "bold"),
                          bg="#00203F", fg="#ADEFD1")
        age_label.grid(row=0, column=1)
        age_label.bind("<Button-1>", lambda x: self.__sort_players_info(1))
        age_label["cursor"] = "hand2"
        nationality_label = Label(master=self.team_window, text="Nationality",
                                  font=("Verdana", MainGUI.STANDINGS_ELEM_SIZE, "bold"),
                                  bg="#00203F", fg="#ADEFD1")
        nationality_label.grid(row=0, column=2)
        nationality_label.bind("<Button-1>", lambda x: self.__sort_players_info(2))
        nationality_label["cursor"] = "hand2"
        height_label = Label(master=self.team_window, text="Height",
                             font=("Verdana", MainGUI.STANDINGS_ELEM_SIZE, "bold"),
                             bg="#00203F", fg="#ADEFD1")
        height_label.grid(row=0, column=3)
        height_label.bind("<Button-1>", lambda x: self.__sort_players_info(3))
        height_label["cursor"] = "hand2"
        weight_label = Label(master=self.team_window, text="Weight",
                             font=("Verdana", MainGUI.STANDINGS_ELEM_SIZE, "bold"),
                             bg="#00203F", fg="#ADEFD1")
        weight_label.grid(row=0, column=4)
        weight_label.bind("<Button-1>", lambda x: self.__sort_players_info(4))
        weight_label["cursor"] = "hand2"
        games_label = Label(master=self.team_window, text="Games",
                            font=("Verdana", MainGUI.STANDINGS_ELEM_SIZE, "bold"),
                            bg="#00203F", fg="#ADEFD1")
        games_label.grid(row=0, column=5)
        games_label.bind("<Button-1>", lambda x: self.__sort_players_info(5))
        games_label["cursor"] = "hand2"
        goals_label = Label(master=self.team_window, text="Goals",
                            font=("Verdana", MainGUI.STANDINGS_ELEM_SIZE, "bold"),
                            bg="#00203F", fg="#ADEFD1")
        goals_label.grid(row=0, column=6)
        goals_label.bind("<Button-1>", lambda x: self.__sort_players_info(6))
        goals_label["cursor"] = "hand2"
        assists_label = Label(master=self.team_window, text="Assists",
                              font=("Verdana", MainGUI.STANDINGS_ELEM_SIZE, "bold"),
                              bg="#00203F", fg="#ADEFD1")
        assists_label.grid(row=0, column=7)
        assists_label.bind("<Button-1>", lambda x: self.__sort_players_info(7))
        assists_label["cursor"] = "hand2"
        yellow_cards_label = Label(master=self.team_window, text="Yellow cards",
                                   font=("Verdana", MainGUI.STANDINGS_ELEM_SIZE, "bold"),
                                   bg="#00203F", fg="#ADEFD1")
        yellow_cards_label.grid(row=0, column=8)
        yellow_cards_label.bind("<Button-1>", lambda x: self.__sort_players_info(8))
        yellow_cards_label["cursor"] = "hand2"
        red_cards_label = Label(master=self.team_window, text="Red cards",
                                font=("Verdana", MainGUI.STANDINGS_ELEM_SIZE, "bold"),
                                bg="#00203F", fg="#ADEFD1")
        red_cards_label.grid(row=0, column=9)
        red_cards_label.bind("<Button-1>", lambda x: self.__sort_players_info(9))
        red_cards_label["cursor"] = "hand2"

        self.__show_players(players)

    def __next_page(self):
        if self.current_page < self.pages:
            self.__forget_players()

        players = far.get_players_and_pages_for_team_and_season(self.team_name, self.season, self.current_page + 1)[0]
        self.current_page += 1
        self.__show_players(players)

        if self.current_page == self.pages:
            self.next_page_button["state"] = "disabled"
        if self.current_page == 2:
            self.previous_page_button["state"] = "normal"

    def __previous_page(self):
        if self.current_page > 1:
            self.__forget_players()

        players = far.get_players_and_pages_for_team_and_season(self.team_name, self.season, self.current_page - 1)[0]
        self.current_page -= 1
        self.__show_players(players)

        if self.current_page == 1:
            self.previous_page_button["state"] = "disabled"
        if self.current_page == self.pages - 1:
            self.next_page_button["state"] = "normal"

    def __show_players(self, players):
        for i in range(len(players)):
            for j in range(len(players[i])):
                label_to_add = Label(self.team_window, text=players[i][j],
                                     font=("Arial", MainGUI.PLAYER_INFO_ELEM_SIZE), bg="#00203F",
                                     fg="#ADEFD1")
                label_to_add.grid(row=i + 1, column=j)
                self.players_data.append(label_to_add)

    def __forget_players(self):
        for elem in self.players_data:
            elem.grid_forget()

        self.players_data = []

    def __sort_players_info(self, index):
        list_of_lists = []
        list_to_add = []
        for i in range(len(self.players_data)):
            if i % TeamInfoGUI.NUMBER_OF_PLAYER_INFO_COLUMNS != 0 or i == 0:
                list_to_add.append(self.players_data[i]["text"])
                if i == len(self.players_data) - 1:
                    list_of_lists.append(list_to_add)
            else:
                list_of_lists.append(list_to_add)
                list_to_add = [self.players_data[i]["text"]]

        if index == 0 or index == 2:
            list_of_lists.sort(key=lambda e: e[index], reverse=self.sort_info[index])
        elif index != 0 and index != 2:
            list_of_lists.sort(key=lambda e: utils.extract_integer_from_string_or_return_zero(str(e[index])),
                               reverse=self.sort_info[index])

        was_reversed = self.sort_info[index]
        self.sort_info = [False for _ in range(TeamInfoGUI.NUMBER_OF_PLAYER_INFO_COLUMNS)]
        self.sort_info[index] = False if was_reversed else True

        self.__forget_players()
        self.__show_players(list_of_lists)
