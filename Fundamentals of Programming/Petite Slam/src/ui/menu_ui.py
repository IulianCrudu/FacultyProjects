class UI:
    def __init__(self, player_service):
        self._service = player_service
        pass

    @property
    def service(self):
        return self._service

    def print_players(self):
        players = self.service.get_sorted_players()
        for idx, player in enumerate(players[::-1]):
            print(f"{idx+1}. {player}")

    def qualifying_round_ui(self):
        print("Qualifying round starting...")
        players = self.service.players_for_qualifications()
        grouped_players = self.service.get_random_groups(players)
        for group in grouped_players:
            print("Player 1", group[0])
            print("Player 2", group[1])
            done = False
            while not done:
                winner_input = input("Who is the winner?: ")
                done = True
                if winner_input == "1":
                    winner = group[0]
                    loser = group[1]
                elif winner_input == "2":
                    winner = group[1]
                    loser = group[0]
                else:
                    done = False
                    print("Wrong input. Please type again")
                if done:
                    self.service.mark_loser(loser.id)
                    self.service.increase_strength(winner)

    def tournament_ui(self):
        print("Tournament starting...")
        while len(self.service.current_players) != 1:
            players = self.service.current_players
            grouped_players = self.service.get_random_groups(players)
            print(f"Last {len(players)}...")
            for group in grouped_players:
                print("Player 1", group[0])
                print("Player 2", group[1])
                done = False
                while not done:
                    winner_input = input("Who is the winner?: ")
                    done = True
                    if winner_input == "1":
                        winner = group[0]
                        loser = group[1]
                    elif winner_input == "2":
                        winner = group[1]
                        loser = group[0]
                    else:
                        done = False
                        print("Wrong input. Please type again")
                    if done:
                        self.service.mark_loser(loser.id)
                        self.service.increase_strength(winner)
        print(f"Winner is {self.service.current_players[0]}")

    def start(self):
        self.print_players()
        if self.service.is_qualifying_round_needed():
            self.qualifying_round_ui()
        self.tournament_ui()
