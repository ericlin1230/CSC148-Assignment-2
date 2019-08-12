from __future__ import annotations
from typing import List, Tuple, Optional, Set

def random_direction() -> List[str]:
    output = []
    directions = ['NE', 'NW', 'SW', 'SE']
    output.append(random.choice(directions))
    directions.remove(output[0])
    output.append(random.choice(directions))
    return output

def random_direction2() -> str:
    directions = ['N', 'S', 'W', 'E']
    return random.choice(directions)

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
        
    def assignd(self)->None:
        self._direction=random_direction2()
        
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

    def getname(self) -> str:
        return self.name
    def getcolor(self)->str:
        return self._colour
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
        s = set()
        random_dir = random_direction()

        northpoints = 0
        southpoints = 0
        eastpoints = 0
        westpoints = 0

        targets1 = []
        enemies1 = []

        targets2 = []
        enemies2 = []

        # Collects targets and names of first direction
        for name in self._game.field.names_in_range(self._location, random_dir[0],
                                                    self._vision):
            if name in self._targets:
                targets1.append(name)
            elif name in self._enemies:
                enemies1.append(name)

        # Collects targets and names of second direction
        for name in self._game.field.names_in_range(self._location, random_dir[1],
                                                     self._vision):
            if name in self._targets:
                targets2.append(name)
            elif name in self._enemies:
                enemies2.append(name)

        # Calculates all possibilities for NSEW points
        if 'NE' in random_dir and 'NW' in random_dir:
            if random_dir[0] == 'NE':
                northpoints = len(targets1) + len(targets2)
                southpoints = len(enemies1) + len(enemies2)
                eastpoints = len(targets1) + len(enemies2)
                westpoints = len(targets2) + len(enemies1)
            elif random_dir[0] == 'NW':
                northpoints = len(targets1) + len(targets2)
                southpoints = len(enemies1) + len(enemies2)
                eastpoints = len(targets2) + len(enemies1)
                westpoints = len(targets1) + len(enemies2)
        elif 'NE' in random_dir and 'SW' in random_dir:
            if random_dir[0] == 'NE':
                northpoints = len(targets1) + len(enemies2)
                southpoints = len(targets2) + len(enemies1)
                eastpoints = len(targets1) + len(enemies2)
                westpoints = len(targets2) + len(enemies1)
            elif random_dir[0] == 'SW':
                northpoints = len(targets2) + len(enemies1)
                southpoints = len(targets2) + len(enemies1)
                eastpoints = len(targets2) + len(enemies1)
                westpoints = len(targets1) + len(enemies2)
        elif 'NE' in random_dir and 'SE' in random_dir:
            if random_dir[0] == 'NE':
                northpoints = len(targets1) + len(enemies2)
                southpoints = len(targets2) + len(enemies1)
                eastpoints = len(targets1) + len(targets2)
                westpoints = len(enemies1) + len(enemies2)
            elif random_dir[0] == 'SE':
                northpoints = len(targets2) + len(enemies1)
                southpoints = len(targets1) + len(enemies2)
                eastpoints = len(targets1) + len(targets2)
                westpoints = len(enemies1) + len(enemies2)
        elif 'NW' in random_dir and 'SW' in random_dir:
            if random_dir[0] == 'NW':
                northpoints = len(targets1) + len(enemies2)
                southpoints = len(targets2) + len(enemies1)
                eastpoints = len(enemies1) + len(enemies2)
                westpoints = len(targets1) + len(targets2)
            elif random_dir[0] == 'SW':
                northpoints = len(targets2) + len(enemies1)
                southpoints = len(targets1) + len(enemies2)
                eastpoints = len(enemies1) + len(enemies2)
                westpoints = len(targets1) + len(targets2)
        elif 'NW' in random_dir and 'SE' in random_dir:
            if random_dir[0] == 'NW':
                northpoints = len(targets1) + len(enemies2)
                southpoints = len(targets2) + len(enemies1)
                eastpoints = len(targets2) + len(enemies1)
                westpoints = len(targets1) + len(enemies2)
            elif random_dir[0] == 'SE':
                northpoints = len(targets2) + len(enemies1)
                southpoints = len(targets1) + len(enemies2)
                eastpoints = len(targets1) + len(enemies2)
                westpoints = len(targets2) + len(enemies1)
        elif 'SW' in random_dir and 'SE' in random_dir:
            if random_dir[0] == 'SW':
                northpoints = len(enemies1) + len(enemies2)
                southpoints = len(targets1) + len(targets2)
                eastpoints = len(targets2) + len(enemies1)
                westpoints = len(targets1) + len(enemies2)
            elif random_dir[0] == 'SE':
                northpoints = len(enemies1) + len(enemies2)
                southpoints = len(targets1) + len(targets2)
                eastpoints = len(targets1) + len(enemies2)
                westpoints = len(targets2) + len(enemies1)

        # Calculates all possibilities of NSEW points to return best direction(s)
        if northpoints > (southpoints and eastpoints and westpoints):
            s.add('N')
            self._direction = 'N'
            return s
        elif southpoints > (northpoints and eastpoints and westpoints):
            s.add('S')
            self._direction = 'S'
            return s
        elif eastpoints > (southpoints and northpoints and westpoints):
            s.add('E')
            self._direction = 'E'
            return s
        elif westpoints > (northpoints and southpoints and eastpoints):
            s.add('W')
            self._direction = 'W'
            return s

        elif southpoints == eastpoints and southpoints == westpoints and northpoints < (southpoints and eastpoints and westpoints):
            s.add('S')
            s.add('E')
            s.add('W')
            return s
        elif northpoints == eastpoints and northpoints == westpoints and southpoints < (northpoints and eastpoints and westpoints):
            s.add('N')
            s.add('E')
            s.add('W')
            return s
        elif southpoints == northpoints and southpoints == westpoints and eastpoints < (southpoints and northpoints and westpoints):
            s.add('N')
            s.add('S')
            s.add('W')
            return s
        elif northpoints == southpoints and northpoints == eastpoints and westpoints < (northpoints and southpoints and eastpoints):
            s.add('N')
            s.add('S')
            s.add('E')
            return s

        elif northpoints == southpoints and northpoints > (eastpoints and westpoints):
            s.add('N')
            s.add('S')
            return s
        elif northpoints == westpoints and northpoints > (
                eastpoints and southpoints):
            s.add('N')
            s.add('W')
            return s
        elif northpoints == eastpoints and northpoints > (
                southpoints and westpoints):
            s.add('N')
            s.add('E')
            return s
        elif eastpoints == southpoints and eastpoints > (
                northpoints and westpoints):
            s.add('E')
            s.add('S')
        elif eastpoints == westpoints and eastpoints > (
                northpoints and southpoints):
            s.add('E')
            s.add('W')

        else:
            s.add(random_direction2())
            return s

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
