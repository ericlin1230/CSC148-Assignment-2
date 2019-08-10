from __future__ import annotations
from typing import List, Tuple, Optional, Set

class Player:
    _name: str
    _location: Tuple[int, int]
    _colour: str
    _vision: int
    _speed: int
    _game: Game
    _points: int
    _targets: List[str]
    _enemies: List[str]
    _direction: str

    def __init__(self, name: str, vision: int, speed: int, game: Game,
                       colour: str, location: Tuple[int, int]) -> None:
        self._name = name
        self._vision = vision
        self._speed = speed
        self._game = game
        self._colour = colour
        self._location = location
        self._points = 0
        self._targets = []
        self._enemies = []
        self._direction = ""

    def set_colour(self, colour: str) -> None:
        """ Change the colour of self
        >>> p = Player(None, None, None, None, None, None)
        >>> p._colour = "green"
        >>> p._colour == "green"
        True
        """
        self._colour = colour

    def increase_points(self, points: int) -> None:
        """ Increase <self>'s points by <points>
        >>> p = Player(None, None, None, None, None, None)
        >>> p._points == 0
        True
        >>> p.increase_points(5)
        >>> p.get_points()
        5
        >>> p.increase_points(5)
        >>> p.get_points()
        10
        """
        self._points += points

    def get_points(self) -> int:
        """ Return the number of points <self> currently has
        >>> p = Player(None, None, None, None, None, None)
        >>> p.get_points()
        0
        """
        return self._points

    def select_target(self, name: str) -> None:
        """ Add a target to <self>'s target list
        >>> p = Player(None, None, None, None, None, None)
        >>> p.select_target("Eric")
        >>> p.select_target("Joe")
        >>> p.get_targets()
        ['Eric', 'Joe']
        """
        self._targets.append(name)

    def ignore_target(self, name: str) -> None:
        """ Remove a target from <self>'s target list
        >>> p = Player(None, None, None, None, None, None)
        >>> p.select_target("Eric")
        >>> p.select_target("Joe")
        >>> p.ignore_target("Joe")
        >>> p.get_targets()
        ['Eric']
        """
        self._targets.remove(name)

    def get_targets(self) -> List[str]:
        """ Return a copy of the list of target names
        >>> p = Player(None, None, None, None, None, None)
        >>> p.select_target("Eric")
        >>> p.select_target("Joe")
        >>> p.select_target("Jack")
        >>> p.get_targets()
        ['Eric', 'Joe', 'Jack']
        """
        return self._targets

    def select_enemy(self, name: str) -> None:
        """ Add an enemy to <self>'s target list
        >>> p = Player(None, None, None, None, None, None)
        >>> p.select_enemy("Eric")
        >>> p.select_enemy("Joe")
        >>> p.get_enemies()
        ['Eric', 'Joe']
        """
        self._enemies.append(name)

    def ignore_enemy(self, name: str) -> None:
        """ Remove an enemy from <self>'s enemy list
        >>> p = Player(None, None, None, None, None, None)
        >>> p.select_enemy("Eric")
        >>> p.select_enemy("Joe")
        >>> p.ignore_enemy("Joe")
        >>> p.get_enemies()
        ['Eric']
        """
        self._enemies.remove(name)

    def get_enemies(self) -> List[str]:
        """ Return a copy of the list of enemy names
        >>> p = Player(None, None, None, None, None, None)
        >>> p.select_enemy("Eric")
        >>> p.select_enemy("Joe")
        >>> p.select_enemy("Jack")
        >>> p.get_enemies()
        ['Eric', 'Joe', 'Jack']
        """
        return self._enemies

    def reverse_direction(self) -> None:
        """ Update the direction so that <self> will move in the opposite direction
        >>> p = Player(None, None, None, None, None, None)
        >>> p._direction = "N"
        >>> p.reverse_direction()
        >>> p._direction == "S"
        True
        """
        if self._direction == "N":
            self._direction = "S"
        elif self._direction == "S":
            self._direction = "N"
        elif self._direction == "E":
            self._direction = "W"
        else:
            self._direction = "E"

    def set_speed(self, speed: int) -> None:
        """ Update <self>'s speed to <speed>
        >>> p = Player(None, None, 1, None, None, None)
        >>> p._speed == 1
        True
        >>> p.set_speed(2)
        >>> p._speed == 2
        True
        """
        self._speed = speed

    def next_direction(self) -> Set[str]:
        """ Update the direction to move the next time self.move is called. This direction should be
        determined by the relative number of visible targets and enemies.

        Return a set of all equally good directions to move towards.

        This method should call the names_in_range Tree method exactly twice.

        This method should set self._direction to a subset of: ('N', 'S', 'E', 'W')
        """
        total_targets = []
        total_enemies = []
        t1 = []
        e1 = []
        t2 = []
        e2 = []
        t3 = []
        e3 = []
        t4 = []
        e4 = []
        for name in self._game.field.names_in_range(self._location, "NE", self._vision):
            if name in self._targets:
                t1.append(name)
            elif name in self._enemies:
                e1.append(name)
        for name in self._game.field.names_in_range(self._location, "NW",
                                                     self._vision):
            if name in self._targets:
                t2.append(name)
            elif name in self._enemies:
                e2.append(name)
        for name in self._game.field.names_in_range(self._location, "SW",
                                                     self._vision):
            if name in self._targets:
                t3.append(name)
            elif name in self._enemies:
                e3.append(name)
        for name in self._game.field.names_in_range(self._location, "SE",
                                                     self._vision):
            if name in self._targets:
                t4.append(name)
            elif name in self._enemies:
                e4.append(name)


    def move(self) -> None:
        """ Move <self> in the direction described by self._direction by the number of steps
        described by self._speed. Make sure to keep track of the updated location of self.

        If the movement would move self out of bounds, move self in the opposite direction instead.
        self should continue to move in this new direction until next_direction is called again.
        >>> p = Player(None, None, 1, None, None, (50, 50))
        >>> p._direction = "N"
        >>> p._speed == 1
        True
        >>> p._location == (50, 50)
        True
        >>> p.move()
        >>> p._location == (50, 49)
        True
        """
        if self._direction == "N" and self._location[1] - self._speed < 0:
            self.reverse_direction()
            # self._location[1] = self._game.field.move_point((self._location, "S", self._speed))
            lst = list(self._location)
            lst[1] = self._location[1] + self._speed
            self._location = tuple(lst)
        elif self._direction == "N" and self._location[1] - self._speed >= 0:
            # self._location[1] = self._game.field.move_point((self._location, "N", self._speed))
            lst = list(self._location)
            lst[1] = self._location[1] - self._speed
            self._location = tuple(lst)

        if self._direction == "S" and self._location[1] + self._speed > (2*(self._game.field._centre[1])):
            self.reverse_direction()
            # self._location = self._game.field.move_point((self._location, "N", self._speed))
            lst = list(self._location)
            lst[1] = self._location[1] - self._speed
            self._location = tuple(lst)
        elif self._direction == "S" and self._location[1] + self._speed <= (2*(self._game.field._centre[1])):
            # self._location[1] = self._game.field.move_point((self._location, "S", self._speed))
            lst = list(self._location)
            lst[1] = self._location[1] + self._speed
            self._location = tuple(lst)

        if self._direction == "W" and self._location[0] - self._speed < 0:
            self.reverse_direction()
            # self._location[0] = self._game.field.move_point(
            #     (self._location, "E", self._speed))
            lst = list(self._location)
            lst[0] = self._location[0] + self._speed
            self._location = tuple(lst)
        elif self._direction == "W" and self._location[0] - self._speed >= 0:
            # self._location[0] = self._game.field.move_point(
            #     (self._location, "W", self._speed))
            lst = list(self._location)
            lst[0] = self._location[0] - self._speed
            self._location = tuple(lst)

        if self._direction == "E" and self._location[0] + self._speed > (
                2 * (self._game.field._centre[0])):
            self.reverse_direction()
            # self._location = self._game.field.move_point(
            #     (self._location, "W", self._speed))
            lst = list(self._location)
            lst[0] = self._location[0] - self._speed
            self._location = tuple(lst)
        elif self._direction == "E" and self._location[0] + self._speed <= (
                2 * (self._game.field._centre[0])):
            # self._location[0] = self._game.field.move_point(
            #     (self._location, "E", self._speed))
            lst = list(self._location)
            lst[0] = self._location[0] + self._speed
            self._location = tuple(lst)

if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={'extra-imports': ['typing']})
    
