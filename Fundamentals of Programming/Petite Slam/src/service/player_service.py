import math
import random


class PlayerService:
    def __init__(self, repo):
        self._repo = repo
        self._current_players = repo.items

    @property
    def repo(self):
        return self._repo

    @property
    def current_players(self):
        return self._current_players

    def get_sorted_players(self, reverse=False):
        self.repo.items.sort(key=lambda player: player.strength, reverse=reverse)
        self._current_players.sort(key=lambda player: player.strength, reverse=reverse)
        return self.repo.items

    @staticmethod
    def get_nearest_power_of_2(nr):
        return 2**math.floor(math.log2(nr))

    def is_qualifying_round_needed(self):
        players_len = len(self.repo.items)
        tournament_players = self.get_nearest_power_of_2(players_len)
        return players_len > tournament_players

    def players_for_qualifications(self):
        """
        Returns the last x needed players for qualifications. The players are sorted by strength
        X - If the number of players are 13, X will be 10 because we need to get rid of 5 players => from 10 games
        :return: The array of players
        """
        sorted_players = self.get_sorted_players(reverse=False)
        players_len = len(self.repo.items)
        nr_players = (players_len - self.get_nearest_power_of_2(players_len)) * 2
        return sorted_players[-nr_players:]

    @staticmethod
    def get_random_index(length, used_indexes):
        """
        Returns a random index between 0 and length-1. Checks if the resulted index is already in used_indexes.
        If yes, get a new random index
        :param length: The max number than the index can be
        :param used_indexes: The array of used indexes
        :return: A new unused index
        """
        while True:
            rand_index = random.randint(0, length-1)
            if rand_index not in used_indexes:
                return rand_index

    def get_random_groups(self, players):
        """
        Groups the players by 2 randomly
        :param players: The players that need to be grouped
        :return: An array of arrays consisting of 2 elements that are the players that need to play together
        """
        players_len = len(players)
        used_indexes = []
        grouped_players = []
        while len(used_indexes) < players_len:
            player_1_idx = self.get_random_index(players_len, used_indexes)
            used_indexes.append(player_1_idx)
            player_1 = self.current_players[player_1_idx]

            player_2_idx = self.get_random_index(players_len, used_indexes)
            used_indexes.append(player_2_idx)
            player_2 = self.current_players[player_2_idx]

            grouped_players.append([player_1, player_2])
        return grouped_players

    def mark_loser(self, player_id):
        """
        Deletes the losing player from the current_players array
        :param player_id: The id of the player that lost
        :return: None
        """
        self._current_players = [
            player for player in self._current_players
            if player.id != player_id
        ]

    def increase_strength(self, player):
        """
        Increases the strength by 1 of the given player
        :param player: The player that needs to have his strength increased
        :return: None
        """
        self.repo.update_strength(player.id, player.strength + 1)
