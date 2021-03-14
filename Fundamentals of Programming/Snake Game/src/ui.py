from .board import Board


class UI:
    def __init__(self, dimension, apple_count):
        self._board = Board(dimension, apple_count)

    def read_command(self):
        command = input("Where next? >")

        command = command.strip()
        tokens = command.split(" ")

        if len(tokens) == 2:
            if tokens[0] != "move":
                raise Exception("Wrong command")
            if int(tokens[1]) < 1:
                raise Exception("Number of squares incorrect.")

        if len(tokens) == 1 and tokens[0] not in ["right", "up", "left", "down", "move"]:
            raise Exception("Wrong command")

        return tokens

    def start(self):
        finished = False

        while not finished:
            print(self._board)

            try:
                command = self.read_command()
                finished = not self._board.handle_command(command)
            except Exception as e:
                print("Error " + str(e))

        print("Game Over!")
