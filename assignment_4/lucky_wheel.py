import random

from collections import defaultdict


class StreamersGameChooser:

    def __init__(self, donations_dict: dict[str: int] = None):
        """
        adding donations_dict dictionary to class initializer makes it
        possible to use existing dict to continue collecting donations
        with it as a base
        :param donations_dict: a dictionary of donations
        """
        if donations_dict is None:
            self._donations_dict = defaultdict(int)
        else:
            self._donations_dict = defaultdict(int, donations_dict)

    def __str__(self):
        """
        makes string representation of class objects equal to their
        donations_dict
        :return:
        """
        return str(self._donations_dict)

    def get_donations_dict(self):
        """
        getter for donations dict
        :return: donations dict
        """
        return self._donations_dict

    def add_game(self, game: str, donation: int):
        """
        method adds a game with its donation value to donations dict
        :param game: give game
        :param donation: given donation
        :return: None
        """
        self._donations_dict[game.lower()] += donation

    def get_game(self):
        """
        Method uses choices function of random module to get a weighted
        random value from donations dict
        :return: chosen value
        """
        games = list(self._donations_dict.keys())
        total_donations = sum(self._donations_dict.values())
        weights = [value / total_donations
                   for value in self._donations_dict.values()]
        chosen_game = random.choices(games, weights)[0]
        self._donations_dict.pop(chosen_game)
        return chosen_game


if __name__ == '__main__':
    wheel = StreamersGameChooser()
    print(wheel)
    wheel.add_game('Witcher 3', 200)
    wheel.add_game('witcher 3', 500)
    print(wheel)
    wheel.add_game('GTA 3', 200)
    wheel.add_game('GTA 5', 700)
    wheel.add_game('Tales of Zestiria', 400)
    wheel.add_game('Final Fantasy 8', 750)
    wheel.add_game('Final Fantasy 7', 900)
    wheel.add_game('Final Fantasy 10-2', 800)
    wheel.add_game('Gothic 2', 1000)
    print(wheel)
    print(wheel.get_game())
    print(wheel.get_game())

    wheel2 = StreamersGameChooser(wheel.get_donations_dict())
    print(wheel2)
