from tkinter import *
import football_api_requests as far
from MainGUI import *


class TeamInfoGUI:
    def __init__(self, master, team_name, season):
        self.parent = master
        self.pages = 0
        self.current_page = 1
        self.players_data = []
        self.team_window = Toplevel(master=self.parent, bg="#00203F")
        self.team_name = team_name
        self.season = season
        self.show_team_info_window(self.team_name, self.season)
        self.previous_page_button = Button(self.team_window, text="<<", bg="#ADEFD1", fg="#00203F", command=self.__previous_page)
        self.previous_page_button.grid(row=21, column=0, sticky="e")
        self.previous_page_button["state"] = "disabled"
        self.next_page_button = Button(self.team_window, text=">>", bg="#ADEFD1", fg="#00203F", command=self.__next_page)
        self.next_page_button.grid(row=21, column=1, sticky="w")

    def show_team_info_window(self, team_name, season):
        players, self.pages = far.get_players_and_pages_for_team_and_season(team_name, season)

        Label(master=self.team_window, text="Player", font=("Verdana", MainGUI.STANDINGS_ELEM_SIZE, "bold"),
              bg="#00203F", fg="#ADEFD1").grid(row=0, column=0)
        Label(master=self.team_window, text="Age", font=("Verdana", MainGUI.STANDINGS_ELEM_SIZE, "bold"),
              bg="#00203F", fg="#ADEFD1").grid(row=0, column=1)

        self.__show_players(players)


    def __next_page(self):
        if self.current_page < self.pages:
            for i in range(len(self.players_data)):
                self.players_data[i].grid_forget()

        players = far.get_players_and_pages_for_team_and_season(self.team_name, self.season, self.current_page+1)[0]
        self.current_page += 1
        self.__show_players(players)

        if self.current_page == self.pages:
            self.next_page_button["state"] = "disabled"
        if self.current_page == 2:
            self.previous_page_button["state"] = "normal"

    def __previous_page(self):
        if self.current_page > 1:
            for i in range(len(self.players_data)):
                self.players_data[i].grid_forget()

        players = far.get_players_and_pages_for_team_and_season(self.team_name, self.season, self.current_page-1)[0]
        self.current_page -= 1
        self.__show_players(players)

        if self.current_page == 1:
            self.previous_page_button["state"] = "disabled"
        if self.current_page == self.pages-1:
            self.next_page_button["state"] = "normal"


    def __show_players(self, players):
        for i in range(len(players)):
            name = Label(master=self.team_window, text=players[i][0], font=("Arial", MainGUI.PLAYER_INFO_ELEM_SIZE), bg="#00203F",
                  fg="#ADEFD1")
            name.grid(row=i + 1, column=0)
            age = Label(master=self.team_window, text=players[i][1], font=("Arial", MainGUI.PLAYER_INFO_ELEM_SIZE), bg="#00203F",
                  fg="#ADEFD1")
            age.grid(row=i + 1, column=1)
            self.players_data.append(name)
            self.players_data.append(age)


