from random import choice
from texttable import Texttable
from copy import deepcopy


class Board:
    def __init__(self, dimension, apple_count):
        self._dimension = dimension
        self._apple_count = apple_count
        self._direction = "up"
        self._head_pos = None
        self._body_positions = []
        self._apple_positions = []

        self.initial_snake_position()
        self.place_initial_apples()

    @property
    def dimension(self):
        return self._dimension

    @property
    def apple_count(self):
        return self._apple_count

    @property
    def direction(self):
        return self._direction

    @property
    def head_pos(self):
        return self._head_pos

    @property
    def body_positions(self):
        return self._body_positions

    def initial_snake_position(self):
        head_y_pos = self.dimension // 2
        head_x_pos = self.dimension // 2 - 1

        self._head_pos = [head_x_pos, head_y_pos]
        for i in range(1, 3):
            self._body_positions.append([head_x_pos+i, head_y_pos])

    def place_new_apple(self):
        empty_cells = self.get_empty_cells()
        valid = False
        apple_position = choice(empty_cells)

        while not valid:
            x, y = apple_position
            valid = True

            if not self.is_cell_free(apple_position):
                valid = False

            first_row = x == 0
            last_row = x == self.dimension - 1
            first_column = y == 0
            last_column = y == self.dimension - 1

            if not last_row and [x+1, y] in self._apple_positions:
                valid = False
            if not first_row and [x-1, y] in self._apple_positions:
                valid = False

            if not first_column and [x, y - 1] in self._apple_positions:
                valid = False
            if not last_column and [x, y + 1] in self._apple_positions:
                valid = False

            if not valid:
                new_empty_cells = []
                for empty_cell in empty_cells:
                    if empty_cell == apple_position:
                        continue
                    new_empty_cells.append(empty_cell)
                empty_cells = new_empty_cells
                if not empty_cells:
                    return None
                apple_position = choice(empty_cells)

        return apple_position

    def place_initial_apples(self):
        for apple in range(0, self.apple_count):
            apple_pos = self.place_new_apple()
            if apple_pos:
                self._apple_positions.append(apple_pos)
            else:
                return None

    def handle_command(self, command):
        if len(command) == 1:
            if command[0] != self._direction:
                if command[0] == "move":
                    return self.move(self._direction, 1)
                return self.move(command[0], 1)
            else:
                return True

        return self.move(self._direction, int(command[1]))

    def get_new_head_position(self, direction):
        new_head_x = self._head_pos[0]
        new_head_y = self._head_pos[1]

        if direction == "up":
            new_head_x -= 1
        if direction == "down":
            new_head_x += 1
        if direction == "left":
            new_head_y -= 1
        if direction == "right":
            new_head_y += 1

        return [new_head_x, new_head_y]

    def move(self, direction, nr):
        """
        Handles the movement of a snake in a given direction nr times
        :return: Whether the game is won or not
        """
        if {direction, self.direction} == {"up", "down"} or {direction, self.direction} == {"left", "right"}:
            raise Exception("Can't move 180 degrees.")

        for i in range(nr):
            is_lost = not self.move_1_position(direction)
            if is_lost:
                return False
        self._direction = direction

        return not self.is_game_lost()

    def move_1_position(self, direction):
        new_head_pos = self.get_new_head_position(direction)
        if new_head_pos in self._body_positions:
            return False
        ate_apple = self.will_eat_apple(new_head_pos)

        if ate_apple:
            # If we ate an apple, add a new body chunk where the head was
            self._body_positions.insert(0, self._head_pos)
            apple_pos = self.place_new_apple()
            self._apple_positions.append(apple_pos)
        else:
            body_positions = self.body_positions
            # The 2nd chunk will be on the 1st position, 3rd on the 2nd and so on
            for i in range(len(body_positions) - 1, 0, -1):
                body_positions[i] = body_positions[i - 1]

            # First body chunk is where the head was
            body_positions[0] = self._head_pos

        self._head_pos = new_head_pos
        return True

    def is_game_lost(self):
        x, y = self.head_pos
        if x < 0 or x >= self.dimension:
            return True
        if y < 0 or y >= self.dimension:
            return True
        return False

    def will_eat_apple(self, pos):
        for apple_pos in self._apple_positions:
            if apple_pos == pos:
                return True
        return False

    def get_empty_cells(self):
        """
        Gets all the empty, available cells
        :return: An array of tuples consisting of [row, column] of the empty cells
        """
        empty_cells = []
        for i in range(0, self.dimension):
            for j in range(0, self.dimension):
                # if self._data[i][j] is None:
                if self.is_cell_free([i, j]) and [i, j] not in self._apple_positions:
                    empty_cells.append([i, j])
        return empty_cells

    def is_cell_free(self, pos):
        if pos == self._head_pos:
            return False
        if pos in self._body_positions:
            return False

        return True

    def _is_board_full(self):
        """
        Checks whether the board is full or not
        :return: bool - True if the board is full, False otherwise
        """
        return not len(self.get_empty_cells())

    def __str__(self):
        """
        Returns a printable table that represents the board
        :return: The board
        """
        t = Texttable()
        table_headers = [''] * self.dimension
        t.header(table_headers)
        for i in range(self.dimension):
            row_data = []
            for j in range(self.dimension):
                if [i, j] == self.head_pos:
                    row_data.append("*")
                elif [i, j] in self.body_positions:
                    row_data.append("+")
                elif [i, j] in self._apple_positions:
                    row_data.append(".")
                else:
                    row_data.append(' ')
            t.add_row(row_data)

        return t.draw()
