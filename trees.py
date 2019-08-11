from __future__ import annotations
from typing import Optional, List, Tuple, Dict


class OutOfBoundsError(Exception):
    pass


class Tree:
    def __contains__(self, name: str) -> bool:
        """ Return True if a player named <name> is stored in this tree.

        Runtime: O(n)
        """
        raise NotImplementedError

    def contains_point(self, point: Tuple[int, int]) -> bool:
        """ Return True if a player at location <point> is stored in this tree.

        Runtime: O(log(n))
        """
        raise NotImplementedError

    def insert(self, name: str, point: Tuple[int, int]) -> None:
        """Insert a player named <name> into this tree at point <point>.

        Raise an OutOfBoundsError if <point> is out of bounds.

        Raise an OutOfBoundsError if moving the player would place the player at exactly the
        same coordinates of another player in the Tree (before moving the player).

        Runtime: O(log(n))
        """
        raise NotImplementedError

    def remove(self, name: str) -> None:
        """ Remove information about a player named <name> from this tree.

        Runtime: O(n)
        """
        raise NotImplementedError

    def remove_point(self, point: Tuple[int, int]) -> None:
        """ Remove information about a player at point <point> from this tree.

        Runtime: O(log(n))
        """
        raise NotImplementedError

    def move(self, name: str, direction: str, steps: int) -> Optional[
        Tuple[int, int]]:
        """ Return the new location of the player named <name> after moving it
        in the given <direction> by <steps> steps.

        Raise an OutOfBoundsError if this would move the player named
        <name> out of bounds (before moving the player).

        Raise an OutOfBoundsError if moving the player would place the player at exactly the
        same coordinates of another player in the Tree (before moving the player).

        Runtime: O(n)

        === precondition ===
        direction in ['N', 'S', 'E', 'W']
        """
        raise NotImplementedError

    def move_point(self, point: Tuple[int, int], direction: str, steps: int) -> \
            Optional[Tuple[int, int]]:
        """ Return the new location of the player at point <point> after moving it
        in the given <direction> by <steps> steps.

        Raise an OutOfBoundsError if this would move the player at point
        <point> out of bounds (before moving the player).

        Raise an OutOfBoundsError if moving the player would place the player at exactly the
        same coordinates of another player in the Tree (before moving the player).

        Moving a point may require the tree to be reorganized. This method should do
        the minimum amount of tree reorganization possible to move the given point properly.

        Runtime: O(log(n))

        === precondition ===
        direction in ['N', 'S', 'E', 'W']

        """
        raise NotImplementedError

    def names_in_range(self, point: Tuple[int, int], direction: str,
                       distance: int) -> List[str]:
        """ Return a list of names of players whose location is in the <direction>
        relative to <point> and whose location is within <distance> along both the x and y axis.

        For example: names_in_range((100, 100), 'SE', 10) should return the names of all
        the players south east of (100, 100) and within 10 steps in either direction.
        In other words, find all players whose location is in the box with corners at:
        (100, 100) (110, 100) (100, 110) (110, 110)

        Runtime: faster than O(n) when distance is small

        === precondition ===
        direction in ['NE', 'SE', 'NE', 'SW']
        """
        raise NotImplementedError

    def size(self) -> int:
        """ Return the number of nodes in <self>

        Runtime: O(n)
        """
        raise NotImplementedError

    def height(self) -> int:
        """ Return the height of <self>

        Height is measured as the number of nodes in the path from the root of this
        tree to the node at the greatest depth in this tree.

        Runtime: O(n)
        """
        raise NotImplementedError

    def depth(self, tree: Tree) -> Optional[int]:
        """ Return the depth of the subtree <tree> relative to <self>. Return None
        if <tree> is not a descendant of <self>

        Runtime: O(log(n))
        """

    def is_leaf(self) -> bool:
        """ Return True if <self> has no children

        Runtime: O(1)
        """
        raise NotImplementedError

    def is_empty(self) -> bool:
        """ Return True if <self> does not store any information about the location
        of any players.

        Runtime: O(1)
        """
        raise NotImplementedError


def directions(centre: Tuple[int, int], point: Tuple[int, int]) -> int:
    if point[0] > centre[0] and point[1] > centre[1]:
        return 4
    elif point[0] >= centre[0] and point[1] <= centre[1]:
        return 1
    elif point[0] <= centre[0] and point[1] >= centre[1]:
        return 3
    else:
        return 2


def checksub(tre: QuadTree) -> int:
    if tre._ne is not None:
        return 1
    elif tre._nw is not None:
        return 2
    elif tre._sw is not None:
        return 3
    else:
        return 4


insertcount = 0
insert1 = 0
insert2 = 0
checkheight = 0


class QuadTree(Tree):
    _centre: Tuple[int, int]
    _name: Optional[str]
    _point: Optional[Tuple[int, int]]
    _ne: Optional[QuadTree]
    _nw: Optional[QuadTree]
    _se: Optional[QuadTree]
    _sw: Optional[QuadTree]

    def __init__(self, centre: Tuple[int, int]) -> None:
        """Initialize a new QuadTree instance
        Runtime: O(1)
        """
        self._centre = centre
        self._se = None
        self._ne = None
        self._point = None
        self._nw = None
        self._sw = None
        self._name = None

    def countsub(self) -> int:
        count = 0
        if self._se is not None:
            count += 1
        if self._ne is not None:
            count += 1
        if self._sw is not None:
            count += 1
        if self._nw is not None:
            count += 1
        return count

    def __contains__(self, name: str) -> bool:
        """ Return True if a player named <name> is stored in this tree.
        Runtime: O(n)
        >>> q = QuadTree((50, 50))
        >>> q._name = "Eric"
        >>> q.__contains__("Eric")
        True
        """
        if self.is_empty():
            return False
        elif self._name == name:
            return True
        else:
            if self._se is not None:
                if self._se.__contains__(name):
                    return True
            if self._ne is not None:
                if self._ne.__contains__(name):
                    return True
            if self._sw is not None:
                if self._sw.__contains__(name):
                    return True
            if self._nw is not None:
                if self._nw.__contains__(name):
                    return True
        return False

    def contains_point(self, point: Tuple[int, int]) -> bool:
        """ Return True if a player at location <point> is stored in this tree.
        Runtime: O(log(n))
        >>> q = QuadTree((50, 50))
        >>> q._point = (60, 60)
        >>> q.contains_point((60, 60))
        True
        """
        if self.is_empty():
            return False
        elif self._point == point:
            return True
        else:
            if self._se is not None:
                if point[0] >= self._centre[0] and point[1] >= self._centre[1]:
                    return self._se.contains_point(point)
            if self._ne is not None:
                if point[0] >= self._centre[0] and point[1] <= self._centre[1]:
                    return self._ne.contains_point(point)
            if self._sw is not None:
                if point[0] <= self._centre[0] and point[1] >= self._centre[1]:
                    return self._sw.contains_point(point)
            if self._nw is not None:
                if point[0] <= self._centre[0] and point[1] <= self._centre[1]:
                    return self._nw.contains_point(point)
        return False

    def getpoint(self, name: str) -> Tuple[int, int]:
        if self.is_empty():
            pass
        elif self._name == name:
            return self._point
        else:
            a = None
            b = None
            c = None
            d = None
            if self._ne is not None:
                a = self._ne.getpoint(name)
            if self._se is not None:
                b = self._se.getpoint(name)
            if self._nw is not None:
                c = self._nw.getpoint(name)
            if self._sw is not None:
                d = self._sw.getpoint(name)
            if a is not None:
                return a
            elif b is not None:
                return b
            elif c is not None:
                return c
            elif d is not None:
                return d
            else:
                pass

    def getname(self, point: Tuple[int, int]) -> str:
        if self.is_empty():
            return None
        elif self._point == point:
            return self._name
        elif point[0] > self._point[0] and point[1] > self._point[1]:
            return self._se.getname(point)
        elif point[0] > self._point[0] and point[1] < self._point[1]:
            return self._ne.getname(point)
        elif point[0] < self._point[0] and point[1] > self._point[1]:
            return self._sw.getname(point)
        elif point[0] < self._point[0] and point[1] < self._point[1]:
            return self._nw.getname(point)
        return None

    def insert(self, name: str, point: Tuple[int, int]) -> None:
        """Insert a player named <name> into this tree at point <point>.
        Raise an OutOfBoundsError if <point> is out of bounds.
        Raise an OutOfBoundsError if moving the player would place the player at exactly the
        same coordinates of another player in the Tree (before moving the player).
        Runtime: O(log(n))
        >>> q = QuadTree((100, 100))
        >>> q.insert("Eric", (150, 150))
        >>> q.contains_point((150, 150))
        True
        """
        global insertcount
        global insert2
        global insert1
        checkup = insertcount
        if checkup == 0:
            insertcount += 1
            insert1 = self._centre[0]
            insert2 = self._centre[1]
        if checkup == 0:
            step = self._centre[0] // 2
        else:
            step = min(self._centre[0] - insert1, self._centre[1] - insert2)
            step = step // 2
        if point[0] > self._centre[0] * 2 or point[1] > self._centre[1] * 2:
            raise OutOfBoundsError
        if self.contains_point(point):
            raise OutOfBoundsError
        if self._nw is None and self._sw is None and self._se is None \
                and self._ne is None and self._point is None:
            self._point = point
            self._name = name
        elif self._nw is None and self._sw is None and self._se is None \
                and self._ne is None and directions(self._centre, self._point) \
                != directions(self._centre, point):
            if directions(self._centre, point) == 4:
                newquad = QuadTree(
                    (self._centre[0] + step, self._centre[1] + step))
                self._se = newquad
                newquad._name = name
                newquad._point = point
            elif directions(self._centre, point) == 1:
                newquad = QuadTree(
                    (self._centre[0] + step, self._centre[1] - step))
                self._ne = newquad
                newquad._point = point
                newquad._name = name
            elif directions(self._centre, point) == 2:
                newquad = QuadTree(
                    (self._centre[0] - step, self._centre[1] - step))
                self._nw = newquad
                newquad._name = name
                newquad._point = point
            elif directions(self._centre, point) == 3:
                newquad = QuadTree(
                    (self._centre[0] - step, self._centre[1] + step))
                self._sw = newquad
                newquad._name = name
                newquad._point = point
            if directions(self._centre, self._point) == 4:
                newquad = QuadTree(
                    (self._centre[0] + step, self._centre[1] + step))
                self._se = newquad
                newquad._name = name
                newquad._point = point
            elif directions(self._centre, self._point) == 1:
                newquad = QuadTree(
                    (self._centre[0] + step, self._centre[1] - step))
                self._ne = newquad
                newquad._point = point
                newquad._name = name
            elif directions(self._centre, self._point) == 2:
                newquad = QuadTree(
                    (self._centre[0] - step, self._centre[1] - step))
                self._nw = newquad
                newquad._name = name
                newquad._point = point
            elif directions(self._centre, self._point) == 3:
                newquad = QuadTree(
                    (self._centre[0] - step, self._centre[1] + step))
                self._sw = newquad
                newquad._name = name
                newquad._point = point
        else:
            if directions(self._centre, self._point) == 4:
                newquad = QuadTree(
                    (self._centre[0] + step, self._centre[1] + step))
                self._se = newquad
                newquad._name = name
                newquad._point = point
                a=self._se
            elif directions(self._centre, self._point) == 1:
                newquad = QuadTree(
                    (self._centre[0] + step, self._centre[1] - step))
                self._ne = newquad
                newquad._point = point
                newquad._name = name
                a = self._ne
            elif directions(self._centre, self._point) == 2:
                newquad = QuadTree(
                    (self._centre[0] - step, self._centre[1] - step))
                self._nw = newquad
                newquad._name = name
                newquad._point = point
                a = self._nw
            else:
                newquad = QuadTree(
                    (self._centre[0] - step, self._centre[1] + step))
                self._sw = newquad
                newquad._name = name
                newquad._point = point
                a = self._sw
            if directions(a._centre, point) == 4:
                if a.is_empty() or a._se is None:
                    newquad = QuadTree(
                        (a._centre[0] + step, a._centre[1] + step))
                    a._se = newquad
                    newquad._name = name
                    newquad._point = point
                    insertcount = 0
                else:
                    a._se.insert(name, point)
            elif directions(a._centre, point) == 1:
                if a.is_empty() or a._ne is None:
                    newquad = QuadTree(
                        (a._centre[0] + step, a._centre[1] - step))
                    a._ne = newquad
                    newquad._point = point
                    newquad._name = name
                else:
                    a._ne.insert(name, point)
            elif directions(a._centre, point) == 2:
                if a.is_empty() or a._nw is None:
                    newquad = QuadTree(
                        (a._centre[0] - step, a._centre[1] - step))
                    a._nw = newquad
                    newquad._name = name
                    newquad._point = point
                else:
                    a._nw.insert(name, point)
            elif directions(a._centre, point) == 3:
                if a.is_empty() or a._sw is None:
                    newquad = QuadTree(
                        (a._centre[0] - step, a._centre[1] + step))
                    a._sw = newquad
                    newquad._name = name
                    newquad._point = point
                else:
                    a._sw.insert(name, point)

    def remove(self, name: str) -> None:
        """ Remove information about a player named <name> from this tree.
        Runtime: O(n)
        >>> q = QuadTree((100, 100))
        >>> q.insert("Eric", (150, 150))
        >>> q.__contains__("Eric")
        True
        >>> q.remove("Eric")
        >>> q.__contains__("Eric")
        False
        """
        if self._name == '' and self.countsub() == 0:
            pass
        elif self._name == name:
            count = self.countsub()
            if count >= 2:
                self._name = None
                self._point = None
            elif count == 1:
                if self._ne is not None:
                    if self._ne.countsub() == 0:
                        self._name = self._ne._name
                        self._point = self._ne._point
                    else:
                        self._name = None
                        self._point = None
                if self._se is not None:
                    if self._se.countsub() == 0:
                        self._name = self._se._name
                        self._point = self._se._point
                    else:
                        self._name = None
                        self._point = None
                if self._nw is not None:
                    if self._nw.countsub() == 0:
                        self._name = self._nw._name
                        self._point = self._nw._point
                    else:
                        self._name = None
                        self._point = None
                if self._sw is not None:
                    if self._sw.countsub() == 0:
                        self._name = self._sw._name
                        self._point = self._sw._point
                    else:
                        self._name = None
                        self._point = None
            else:
                self._name = None
                self._point = None
        else:
            if self._se is not None:
                self._se.remove(name)
            if self._sw is not None:
                self._sw.remove(name)
            if self._ne is not None:
                self._ne.remove(name)
            if self._nw is not None:
                self._nw.remove(name)

    def remove_point(self, point: Tuple[int, int]) -> None:
        """ Remove information about a player at point <point> from this tree.
        Runtime: O(log(n))
        >>> q = QuadTree((100, 100))
        >>> q.insert("Eric", (150, 150))
        >>> q.contains_point((150, 150))
        True
        >>> q.remove_point((150, 150))
        >>> q.contains_point((150, 150))
        False
        """
        direction = directions(self._centre, point)
        a = 0
        if self._point is not None:
            if self._point == point and a == 0:
                count = self.countsub()
                if count >= 2:
                    self._name = None
                    self._point = None
                elif count == 1:
                    if self._ne is not None:
                        if self._ne.countsub() == 0:
                            self._name = self._ne._name
                            self._point = self._ne._point
                        else:
                            self._name = None
                            self._point = None
                    if self._se is not None:
                        if self._se.countsub() == 0:
                            self._name = self._se._name
                            self._point = self._se._point
                        else:
                            self._name = None
                            self._point = None
                    if self._nw is not None:
                        if self._nw.countsub() == 0:
                            self._name = self._nw._name
                            self._point = self._nw._point
                        else:
                            self._name = None
                            self._point = None
                    if self._sw is not None:
                        if self._sw.countsub() == 0:
                            self._name = self._sw._name
                            self._point = self._sw._point
                        else:
                            self._name = None
                            self._point = None
                else:
                    self._name = None
                    self._point = None
        else:
            if direction == 4 and self._se is not None:
                self._se.remove_point(point)
            elif direction == 3 and self._sw is not None:
                self._sw.remove_point(point)
            elif direction == 1 and self._ne is not None:
                self._ne.remove_point(point)
            elif direction == 2 and self._nw is not None:
                self._nw.remove_point(point)

    def move(self, name: str, direction: str, steps: int) -> Optional[
        Tuple[int, int]]:
        """ Return the new location of the player named <name> after moving it
        in the given <direction> by <steps> steps.
        Raise an OutOfBoundsError if this would move the player named
        <name> out of bounds (before moving the player).
        Raise an OutOfBoundsError if moving the player would place the player at exactly the
        same coordinates of another player in the Tree (before moving the player).
        Runtime: O(n)
        === precondition ===
        direction in ['N', 'S', 'E', 'W']
        >>> q = QuadTree((100, 100))
        >>> q.insert("Eric", (150, 150))
        >>> q.move("Eric", "N", 10)
        (150, 140)
        """
        tempcord = (0, 0)
        tempname = name
        point = self.getpoint(name)
        if direction == 'N':
            tempcord = (point[0], point[1] - steps)
        elif direction == 'S':
            tempcord = (point[0], point[1] + steps)
        elif direction == 'E':
            tempcord = (point[0] + steps, point[1])
        elif direction == 'W':
            tempcord = (point[0] - steps, point[1])
        if tempcord[0] > self._centre[0] * 2 or tempcord[1] > self._centre[
            1] * 2:
            raise OutOfBoundsError
        if self.contains_point(tempcord):
            raise OutOfBoundsError
        self.remove(name)
        self.insert(tempname, tempcord)
        return tempcord

    def move_point(self, point: Tuple[int, int], direction: str, steps: int) -> \
            Optional[Tuple[int, int]]:
        """ Return the new location of the player at point <point> after moving it
        in the given <direction> by <steps> steps.
        Raise an OutOfBoundsError if this would move the player at point
        <point> out of bounds (before moving the player).
        Raise an OutOfBoundsError if moving the player would place the player at exactly the
        same coordinates of another player in the Tree (before moving the player).
        Moving a point may require the tree to be reorganized. This method should do
        the minimum amount of tree reorganization possible to move the given point properly.
        Runtime: O(log(n))
        === precondition ===
        direction in ['N', 'S', 'E', 'W']
        >>> q = QuadTree((100, 100))
        >>> q._point = (150, 150)
        >>> q.move_point((150, 150), "N", 10)
        (150, 140)
        """
        tempcord = (0, 0)
        tempname = self.getname(point)
        if direction == 'N':
            tempcord = (point[0], point[1] - steps)
        elif direction == 'S':
            tempcord = (point[0], point[1] + steps)
        elif direction == 'E':
            tempcord = (point[0] + steps, point[1])
        elif direction == 'W':
            tempcord = (point[0] - steps, point[1])
        if tempcord[0] > self._centre[0] * 2 or tempcord[1] > self._centre[
            1] * 2:
            raise OutOfBoundsError
        if self.contains_point(tempcord):
            raise OutOfBoundsError
        self.remove(tempname)
        self.insert(tempname, tempcord)
        return tempcord

    def names_in_range(self, point: Tuple[int, int], direction: str,
                       distance: int) -> List[str]:
        """ Return a list of names of players whose location is in the <direction>
        relative to <point> and whose location is within <distance> along both the x and y axis.
        For example: names_in_range((100, 100), 'SE', 10) should return the names of all
        the players south east of (100, 100) and within 10 steps in either direction.
        In other words, find all players whose location is in the box with corners at:
        (100, 100) (110, 100) (100, 110) (110, 110)
        Runtime: faster than O(n) when distance is small
        === precondition ===
        direction in ['NE', 'SE', 'NE', 'SW']
        >>> q = QuadTree((100, 100))
        >>> q.insert('Eric', (105, 105))
        >>> q.insert('Joe', (110, 110))
        >>> q.insert('Jack', (109, 109))
        >>> q.names_in_range((100, 100), 'SE', 10)
        ['Eric', 'Joe', 'Jack']
        """
        lst = []
        endpoint = ()
        if direction == 'NE':
            endpoint = (point[0] + distance, point[1] - distance)
        elif direction == 'SE':
            endpoint = (point[0] + distance, point[1] + distance)
        elif direction == 'SW':
            endpoint = (point[0] - distance, point[1] + distance)
        elif direction == 'NW':
            endpoint = (point[0] - distance, point[1] - distance)

        upl = (min(point[0], endpoint[0]), min(point[1], endpoint[1]))
        downr = (max(point[0], endpoint[0]), max(point[1], endpoint[1]))
        downl = (min(point[0], endpoint[0]), max(point[1], endpoint[1]))
        if self._point is not None:
            if downl[0] <= self._point[0] <= downr[0] and upl[1] <= self._point[
                1] <= \
                    downl[1]:
                lst.append(self._name)
        if self._se is not None:
            a = self._se.names_in_range(point, direction, distance)
            lst = lst + a
        if self._sw is not None:
            a = self._sw.names_in_range(point, direction, distance)
            lst = lst + a
        if self._ne is not None:
            a = self._ne.names_in_range(point, direction, distance)
            lst = lst + a
        if self._nw is not None:
            a = self._nw.names_in_range(point, direction, distance)
            lst = lst + a
        return lst

    def size(self) -> int:
        """ Return the number of nodes in <self>
        Runtime: O(n)
        >>> q = QuadTree((100, 100))
        >>> q._point = (150, 150)
        >>> q.size()
        1
        """
        if self._name is None and self._point is None:
            return 0
        elif countsub(self) == 0:
            return 1
        else:
            a = self._ne.size()
            b = self._nw.size()
            c = self._se.size()
            d = self._sw.size()
            total = a + b + c + d
            return total

    def height(self) -> int:
        """ Return the height of <self>
        Height is measured as the number of nodes in the path from the root of this
        tree to the node at the greatest depth in this tree.
        Runtime: O(n)
        >>> q = QuadTree((100, 100))
        >>> q._point = (150, 150)
        >>> q.height()
        1
        """
        if self._centre is not None and self._se is None and self._ne is None \
                and self._sw is None and self._nw is None:
            return 1
        elif self.is_empty():
            return 0
        elif self.is_leaf():
            return 1
        else:
            a = 0
            b = 0
            c = 0
            d = 0
            if self._ne is not None:
                a = self._ne.height()
            if self._nw is not None:
                b = self._nw.height()
            if self._se is not None:
                c = self._se.height()
            if self._sw is not None:
                d = self._sw.height()
            return max(a, b, c, d) + 1

    def same(self, tree) -> bool:
        if self._point != tree._point:
            return False
        if self._centre != tree._centre:
            return False
        if self._se is None:
            if tree._se is not None:
                return False
        if self._se is not None:
            if tree._se is None:
                return False
        if self._ne is None:
            if tree._ne is not None:
                return False
        if self._ne is not None:
            if tree._ne is None:
                return False
        if self._sw is None:
            if tree._sw is not None:
                return False
        if self._sw is not None:
            if tree._sw is None:
                return False
        if self._nw is None:
            if tree._nw is not None:
                return False
        if self._nw is not None:
            if tree._nw is None:
                return False
        if self._name != tree._name:
            return False
        if self._se is not None and tree._se is not None:
            return self._se.same(tree)
        if self._ne is not None and tree._ne is not None:
            return self._ne.same(tree)
        if self._sw is not None and tree._sw is not None:
            return self._sew.same(tree)
        if self._nw is not None and tree._nw is not None:
            return self._nw.same(tree)
        return True

    def depth(self, tree: Tree) -> Optional[int]:
        """ Return the depth of the subtree <tree> relative to <self>. Return None
        if <tree> is not a descendant of <self>
        Runtime: O(log(n))
        >>> q = QuadTree((100, 100))
        >>> q.depth(tree._ne)
        1
        """
        directions = (self._centre, tree._point)
        if self._point == tree._point:
            if self.same(tree):
                return 1
            else:
                return None
        elif directions == 1:
            if self._ne is not None:
                a = self._ne.depth(tree)
                if a is not None:
                    return a + 1
                else:
                    return None
        elif directions == 2:
            if self._nw is not None:
                a = self._nw.depth(tree)
                if a is not None:
                    return a + 1
                else:
                    return None
        elif directions == 3:
            if self._sw is not None:
                a = self._sw.depth(tree)
                if a is not None:
                    return a + 1
                else:
                    return None
        else:
            if self._se is not None:
                a = self._se.depth(tree)
                if a is not None:
                    return a + 1
                else:
                    return None

    def is_leaf(self) -> bool:
        """ Return True if <self> has no children
        Runtime: O(1)
        >>> q = QuadTree((100, 100))
        >>> q.is_leaf()
        True
        >>> q.insert("Eric", (150, 150))
        >>> q.is_leaf()
        False
        """
        if self._se is None and self._ne is None \
                and self._sw is None and self._nw is None:
            return True
        else:
            return False

    def is_empty(self) -> bool:
        """ Return True if <self> does not store any information about the location
        of any players.
        Runtime: O(1)
        >>> q = QuadTree((100, 100))
        >>> q.is_empty()
        True
        >>> q.insert("Eric", (150, 150))
        >>> q.is_empty()
        False
        """
        if self._se is not None:
            return False
        elif self._ne is not None:
            return False
        elif self._nw is not None:
            return False
        elif self._sw is not None:
            return False
        elif self._name is not None:
            return False
        elif self._point is not None:
            return False
        return True


splitt = 'x'


class TwoDTree(Tree):
    _name: Optional[str]
    _point: Optional[Tuple[int, int]]
    _nw: Optional[Tuple[int, int]]
    _se: Optional[Tuple[int, int]]
    _lt: Optional[TwoDTree]
    _gt: Optional[TwoDTree]
    _split_type: str

    def __init__(self, nw: Optional[Tuple[int, int]],
                 se: Optional[Tuple[int, int]]) -> None:
        """Initialize a new Tree instance
        Runtime: O(1)
        """
        self._nw = nw
        self._se = se
        self._name = None
        self._lt = None
        self._gt = None
        self._split_type = 'x'
        self._point = None

    def __contains__(self, name: str) -> bool:
        """ Return True if a player named <name> is stored in this tree.
        Runtime: O(n)
        >>> t = TwoDTree((0, 0), (100, 100))
        >>> t._name = "Eric"
        >>> t.__contains__("Eric")
        True
        """
        if self.is_empty():
            return False
        elif self._name == name:
            return True
        else:
            if self._lt is not None:
                if self._lt.__contains__(name) :
                    return True
            if self._gt is not None:
                if self._gt.__contains__(name):
                    return True
        return False

    def contains_point(self, point: Tuple[int, int]) -> bool:
        """ Return True if a player at location <point> is stored in this tree.
        Runtime: O(log(n))
        >>> t = TwoDTree((0, 0), (100, 100))
        >>> t._point = (50, 50)
        >>> t.contains_point((50, 50))
        True
        """
        if self.is_empty():
            return False
        elif self._point == point:
            return True
        elif self._point is None:
            return False
        elif self._split_type == 'x':
            if point[0] <= self._point[0]:
                if self._lt is not None:
                    return self._lt.contains_point(point)
            else:
                if self._gt is not None:
                    return self._gt.contains_point(point)
        elif self._split_type == 'y':
            if point[1] <= self._point[1]:
                if self._lt is not None:
                    return self._lt.contains_point(point)
            else:
                if self._gt is not None:
                    return self._gt.contains_point(point)
        return False

    def insert(self, name: str, point: Tuple[int, int]) -> None:
        """Insert a player named <name> into this tree at point <point>.
        Raise an OutOfBoundsError if <point> is out of bounds.
        Raise an OutOfBoundsError if moving the player would place the player at exactly the
        same coordinates of another player in the Tree (before moving the player).
        Runtime: O(log(n))
        >>> t = TwoDTree((0, 0), (100, 100))
        >>> t.insert("Eric", (50, 50))
        >>> t.contains_point((50, 50))
        True
        """
        global splitt
        if point[0] > self._se[0] or point[1] > self._se[1] or point[0] < \
                self._nw[0] or point[1] < self._nw[1]:
            raise OutOfBoundsError
        if self.__contains__(name):
            raise OutOfBoundsError
        if self._point is None:
            self._point = point
            self._name = name
            if splitt == 'x':
                self._split_type = 'x'
            elif splitt == 'y':
                self._split_type = 'y'
        elif self._split_type == 'x':
            splitt = 'y'
            if point[0] <= self._point[0]:
                if self._lt is not None:
                    self._lt.insert(name, point)
                else:
                    newquad=TwoDTree(self._nw, self._se)
                    newquad._point = point
                    newquad._name = name
                    self._lt=newquad
            else:
                if self._gt is not None:
                    self._gt.insert(name, point)
                else:
                    newquad = TwoDTree(self._nw, self._se)
                    newquad._point = point
                    newquad._name = name
                    self._gt = newquad
        elif self._split_type == 'y':
            splitt = 'x'
            if point[1] <= self._point[1]:
                if self._lt is not None:
                    self._lt.insert(name, point)
                else:
                    newquad = TwoDTree(self._nw, self._se)
                    newquad._point = point
                    newquad._name = name
                    self._lt = newquad
            else:
                if self._gt is not None:
                    self._gt.insert(name, point)
                else:
                    newquad = TwoDTree(self._nw, self._se)
                    newquad._point = point
                    newquad._name = name
                    self._gt = newquad

    def bigswitch(self) -> None:
        if self._split_type == 'x':
            self._split_type = 'y'
        elif self._split_type == 'y':
            self._split_type = 'x'
        if self._lt is not None:
            self._lt.bigswitch()
        if self._gt is not None:
            self._gt.bigswitch()

    def remove(self, name: str) -> None:
        """ Remove information about a player named <name> from this tree.
        Runtime: O(n)
        >>> t = TwoDTree((0, 0), (100, 100))
        >>> t.insert("Eric", (50, 50))
        >>> t.__contains__("Eric")
        True
        >>> t.remove("Eric")
        >>> t.__contains__("Eric")
        False
        """
        if self._name == name:
            if self._lt is None and self._gt is None:
                self._name = None
                self._point = None
            elif self._lt is not None:
                if self._lt._gt is not None:
                    self._name = self._lt._name
                    self._point = self._lt._point
                    a = self._lt._gt
                    self._lt = self._lt._lt
                    self._lt._gt = a
                    self.bigswitch()
                else:
                    self._name = self._lt._name
                    self._point = self._lt._point
                    self._lt = self._lt._lt
                    self.bigswitch()
            else:
                if self._lt is not None:
                    if self._lt._gt is not None:
                        self._name = self._gt._name
                        self._point = self._gt._point
                        self.bigswitch()
                    else:
                        self._name = None
                        self._point = None
                        self._split_type = None
        else:
            if self._lt is not None:
                self._lt.remove(name)
            if self._gt is not None:
                self._gt.remove(name)

    def remove_point(self, point: Tuple[int, int]) -> None:
        """ Remove information about a player at point <point> from this tree.
        Runtime: O(log(n))
        >>> t = TwoDTree((0, 0), (100, 100))
        >>> t.insert("Eric", (50, 50))
        >>> t.contains_point((50, 50))
        True
        >>> t.remove_point((50, 50))
        >>> t.contains_point((50, 50))
        False
        """
        if self._point == point:
            if self._lt is None and self._gt is None:
                self._name = None
                self._point = None
            elif self._lt is not None:
                if self._lt._gt is not None:
                    self._name = self._lt._name
                    self._point = self._lt._point
                    a = self._lt._gt
                    self._lt = self._lt._lt
                    self._lt._gt = a
                    self.bigswitch()
                else:
                    self._name = self._lt._name
                    self._point = self._lt._point
                    self._lt = self._lt._lt
                    self.bigswitch()
            else:
                if self._lt._gt is not None:
                    self._name = self._gt._name
                    self._point = self._gt._point
                    self.bigswitch()
                else:
                    self._name = None
                    self._point = None
                    self._split_type = None
        elif self._split_type == 'x':
            if point[0] <= self._point[0]:
                if self._lt is not None:
                    self._lt.remove_point(point)
            else:
                if self._gt is not None:
                    self._gt.remove_point(point)
        elif self._split_type == 'y':
            if point[1] <= self._point[1]:
                if self._lt is not None:
                    self._lt.remove_point(point)
            else:
                if self._gt is not None:
                    self._gt.remove_point(point)

    def getpoint(self, name: str) -> Tuple[int, int]:
        if self._name == name:
            return self._point
        else:
            if self._gt is not None:
                return self._gt.getpoint(name)
            if self._lt is not None:
                return self._lt.getpoint(name)
        return None

    def move(self, name: str, direction: str, steps: int) -> Optional[
        Tuple[int, int]]:
        """ Return the new location of the player named <name> after moving it
        in the given <direction> by <steps> steps.
        Raise an OutOfBoundsError if this would move the player named
        <name> out of bounds (before moving the player).
        Raise an OutOfBoundsError if moving the player would place the player at exactly the
        same coordinates of another player in the Tree (before moving the player).
        Runtime: O(n)
        === precondition ===
        direction in ['N', 'S', 'E', 'W']
        """
        tempcord = (0, 0)
        tempname = name
        point = self.getpoint(name)
        if direction == 'N':
            tempcord = (point[0], point[1] - steps)
        elif direction == 'S':
            tempcord = (point[0], point[1] + steps)
        elif direction == 'E':
            tempcord = (point[0] + steps, point[1])
        elif direction == 'W':
            tempcord = (point[0] - steps, point[1])
        if tempcord[0] > self._se[0] or tempcord[1] > self._se[1] or tempcord[0] < \
                self._nw[0] or tempcord[1] < self._nw[1]:
            raise OutOfBoundsError
        if self.contains_point(tempcord):
            raise OutOfBoundsError
        self.remove(name)
        self.insert(tempname, tempcord)
        return tempcord

    def getname(self, point) -> str:
        if self._point == point:
            return self._name
        elif self._split_type == 'x':
            if point[0] <= self._point[0]:
                return self._lt.getname(point)
            else:
                return self._gt.getname(point)
        elif self._split_type == 'y':
            if point[1] <= self._point[1]:
                return self._lt.getname(point)
            else:
                return self._gt.getname(point)
        return None

    def move_point(self, point: Tuple[int, int], direction: str, steps: int) -> \
            Optional[Tuple[int, int]]:
        """ Return the new location of the player at point <point> after moving it
        in the given <direction> by <steps> steps.
        Raise an OutOfBoundsError if this would move the player at point
        <point> out of bounds (before moving the player).
        Raise an OutOfBoundsError if moving the player would place the player at exactly the
        same coordinates of another player in the Tree (before moving the player).
        Moving a point may require the tree to be reorganized. This method should do
        the minimum amount of tree reorganization possible to move the given point properly.
        Runtime: O(log(n))
        === precondition ===
        direction in ['N', 'S', 'E', 'W']
        """
        tempcord = (0, 0)
        tempname = self.getname(point)
        if direction == 'N':
            tempcord = (point[0], point[1] - steps)
        elif direction == 'S':
            tempcord = (point[0], point[1] + steps)
        elif direction == 'E':
            tempcord = (point[0] + steps, point[1])
        elif direction == 'W':
            tempcord = (point[0] - steps, point[1])
        if point[0] > self._se[0] or point[1] > self._se[1] or point[0] < \
                self._nw[0] or point[1] < self._nw[1]:
            raise OutOfBoundsError
        if self.contains_point(tempcord):
            raise OutOfBoundsError
        self.remove(tempname)
        self.insert(tempname, tempcord)
        return tempcord

    def names_in_range(self, point: Tuple[int, int], direction: str,
                       distance: int) -> List[str]:
        """ Return a list of names of players whose location is in the <direction>
        relative to <point> and whose location is within <distance> along both the x and y axis.
        For example: names_in_range((100, 100), 'SE', 10) should return the names of all
        the players south east of (100, 100) and within 10 steps in either direction.
        In other words, find all players whose location is in the box with corners at:
        (100, 100) (110, 100) (100, 110) (110, 110)
        Runtime: faster than O(n) when distance is small
        === precondition ===
        direction in ['NE', 'SE', 'NE', 'SW']
        """
        lst = []
        endpoint = ()
        if direction == 'NE':
            endpoint = (point[0] + distance, point[1] - distance)
        elif direction == 'SE':
            endpoint = (point[0] + distance, point[1] + distance)
        elif direction == 'SW':
            endpoint = (point[0] - distance, point[1] + distance)
        elif direction == 'NW':
            endpoint = (point[0] - distance, point[1] - distance)
        upl = (min(point[0], endpoint[0]), min(point[1], endpoint[1]))
        downr = (max(point[0], endpoint[0]), max(point[1], endpoint[1]))
        downl = (min(point[0], endpoint[0]), max(point[1], endpoint[1]))
        if downl[0] <= self._point[0] <= downr[0] and upl[1] \
                <= self._point[1] <=downl[1]:
            lst.append(self._name)
        if self._lt is not None:
            a = self._lt.names_in_range(point, direction, distance)
            lst = lst + a
        if self._gt is not None:
            a = self._gt.names_in_range(point, direction, distance)
            lst = lst + a
        return lst

    def size(self) -> int:
        """ Return the number of nodes in <self>
        Runtime: O(n)
        >>> t = TwoDTree((0, 0), (100, 100))
        >>> t.size()
        0
        >>> t.insert("Eric", (50, 50))
        >>> t.size()
        1
        """
        if self._name is None and self._point is None:
            return 0
        else:
            if self._lt is not None:
                a = self._lt.size()
            if self._gt is not None:
                b = self._gt.size()
            total = a + b
            return total

    def height(self) -> int:
        """ Return the height of <self>
        Height is measured as the number of nodes in the path from the root of this
        tree to the node at the greatest depth in this tree.
        Runtime: O(n)
        >>> t = TwoDTree((0, 0), (100, 100))
        >>> t.height()
        0
        >>> t.insert("Eric", (50, 50))
        >>> t.height()
        1
        """
        if self._lt is None and self._gt is None and self._point is None:
            return 1
        elif self.is_empty():
            return 0
        elif self.is_leaf():
            return 1
        else:
            a=0
            b=0
            if self._lt is not None:
                a = self._lt.height()
            if self._gt is not None:
                b = self._gt.height()
            total = max(a,b)
            return total + 1

    def depth(self, tree: Tree) -> Optional[int]:
        """ Return the depth of the subtree <tree> relative to <self>. Return None
        if <tree> is not a descendant of <self>
        Runtime: O(log(n))
        >>> t = TwoDTree((0, 0), (100, 100))
        >>> t.depth(tree)
        0
        """
        if self._point == tree._point:
            return 1
        elif self._split_type == 'x':
            if not self._lt.is_empty():
                if self._lt._point[0] <= self._point[0]:
                    return self._lt.depth(tree) + 1
            elif not self._gt.is_empty():
                return self._gt.depth(tree) + 1
        elif self._split_type == 'y':
            if not self._lt.is_empty():
                if self._lt.point[1] <= self._point[1]:
                    return self._lt.depth(tree) + 1
            elif not self._gt.is_empty():
                return self._gt.depth(tree) + 1

    def is_leaf(self) -> bool:
        """ Return True if <self> has no children
        Runtime: O(1)
        """
        if self._lt is None and self._gt is None:
            return True
        return False

    def is_empty(self) -> bool:
        """ Return True if <self> does not store any information about the location
        of any players.
        Runtime: O(1)
        """
        if self._name is not None:
            return False
        elif self._point is not None:
            return False
        return True

    def balance(self) -> None:
        """ Balance <self> so that there is at most a difference of 1 between the
        size of the _lt subtree and the size of the _gt subtree for all trees in
        <self>.
        """
        pass


if __name__ == '__main__':
    """import python_ta

    python_ta.check_all(config={'extra-imports': ['typing']})"""
