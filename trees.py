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
    elif point[0] > centre[0] and point[1] < centre[1]:
        return 1
    elif point[0] < centre[0] and point[1] > centre[1]:
        return 3
    else:
        return 2

def countsub(treee:QuadTree)->int:
    count = 0
    if treee._se != []:
        count += 1
    if treee._ne != []:
        count += 1
    if treee._sw != []:
        count += 1
    if treee._nw != []:
        count += 1

def checksub(tre:QuadTree)->int:
    if tre._ne!=[]:
        return 1
    elif tre._nw!=[]:
        return 2
    elif tre._sw!=[]:
        return 3
    else:
        return 4

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
        self._se = []
        self._ne = []
        self._nw = []
        self._sw = []
        self._name = ""
        self._point = ()

    def __contains__(self, name: str) -> bool:
        """ Return True if a player named <name> is stored in this tree.

        Runtime: O(n)
        """
        if self.is_empty():
            return False
        elif self._name == name:
            return True
        else:
            if self._ne.__contains__(name) or self._nw.__contains__(name) or \
                    self._se.__contains__(name) or self._sw.__contains__(name):
                return True
        return False

    def contains_point(self, point: Tuple[int, int]) -> bool:
        """ Return True if a player at location <point> is stored in this tree.

        Runtime: O(log(n))
        """
        if self.is_empty():
            return False
        elif self._point == point:
            return True
        elif point[0] > self._point[0] and point[1] > self._point[1]:
            return self._se.contains_point(point)
        elif point[0] > self._point[0] and point[1] < self._point[1]:
            return self._ne.contains_point(point)
        elif point[0] < self._point[0] and point[1] > self._point[1]:
            return self._sw.contains_point(point)
        elif point[0] < self._point[0] and point[1] < self._point[1]:
            return self._nw.contains_point(point)
        return False

    def insert(self, name: str, point: Tuple[int, int]) -> None:
        """Insert a player named <name> into this tree at point <point>.

        Raise an OutOfBoundsError if <point> is out of bounds.

        Raise an OutOfBoundsError if moving the player would place the player at exactly the
        same coordinates of another player in the Tree (before moving the player).

        Runtime: O(log(n))
        """
        if point[0] > self._centre[0] * 2 or point[1] > self._centre[1] * 2:
            raise OutOfBoundsError
        if self.contains_point(point):
            raise OutOfBoundsError
        step = int(self._centre[0] // 2)
        if directions(self._centre, point) == 4:
            if self.is_empty() or self._se == []:
                newquad = QuadTree(
                    (self._centre[0] + step, self._centre[1] + step))
                self._se = newquad
                newquad._name = name
            else:
                self._se.insert(name, point)
        elif directions(self._centre, point) == 1:
            if self.is_empty() or self._ne == []:
                newquad = QuadTree(
                    (self._centre[0] + step, self._centre[1] - step))
                self._ne = newquad
                newquad._name = name
            else:
                self._ne.insert(name, point)
        elif directions(self._centre, point) == 2:
            if self.is_empty() or self._nw == []:
                newquad = QuadTree(
                    (self._centre[0] - step, self._centre[1] - step))
                self._nw = newquad
                newquad._name = name
            else:
                self._nw.insert(name, point)
        elif directions(self._centre, point) == 3:
            if self.is_empty() or self._sw == []:
                newquad = QuadTree(
                    (self._centre[0] - step, self._centre[1] + step))
                self._sw = newquad
                newquad._name = name
            else:
                self._sw.insert(name, point)

    def remove(self, name: str) -> None:
        """ Remove information about a player named <name> from this tree.

        Runtime: O(n)
        """
        if self._name=='' and countsub(self)==0:
            pass
        elif self._name==name:
            count=countsub(self)
            if count>=2:
                self._name=''
                self._point=()
            elif count==1:
                if self._ne!=[]:
                    if countsub(self._ne)==0:
                        self._name=self._ne._name
                        self._point=self._ne._point
                    else:
                        self._name = ''
                        self._point = ()
                if self._se!=[]:
                    if countsub(self._se)==0:
                        self._name=self._se._name
                        self._point=self._se._point
                    else:
                        self._name = ''
                        self._point = ()
                if self._nw!=[]:
                    if countsub(self._nw)==0:
                        self._name=self._nw._name
                        self._point=self._nw._point
                    else:
                        self._name = ''
                        self._point = ()
                if self._sw!=[]:
                    if countsub(self._sw)==0:
                        self._name=self._sw._name
                        self._point=self._sw._point
                    else:
                        self._name = ''
                        self._point = ()
        else:
            self._se.remove(name)
            self._sw.remove(name)
            self._ne.remove(name)
            self._nw.remove(name)

    def remove_point(self, point: Tuple[int, int]) -> None:
        """ Remove information about a player at point <point> from this tree.

        Runtime: O(log(n))
        """
        direction=directions(self._centre, point)
        if self._point==() and countsub(self)==0:
            pass
        elif self._point==point:
            count = countsub(self)
            if count >= 2:
                self._name = ''
                self._point = ()
            elif count == 1:
                if self._ne != []:
                    if countsub(self._ne) == 0:
                        self._name = self._ne._name
                        self._point = self._ne._point
                    else:
                        self._name = ''
                        self._point = ()
                if self._se != []:
                    if countsub(self._se) == 0:
                        self._name = self._se._name
                        self._point = self._se._point
                    else:
                        self._name = ''
                        self._point = ()
                if self._nw != []:
                    if countsub(self._nw) == 0:
                        self._name = self._nw._name
                        self._point = self._nw._point
                    else:
                        self._name = ''
                        self._point = ()
                if self._sw != []:
                    if countsub(self._sw) == 0:
                        self._name = self._sw._name
                        self._point = self._sw._point
                    else:
                        self._name = ''
                        self._point = ()
        else:
            if direction==4:
                self._se.remove_point(point)
            elif direction==3:
                self._sw.remove_point(point)
            elif direction==1:
                self._ne.remove_point(point)
            else:
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
        if self._name=='' and self._point==():
            return 0
        elif countsub(self)==0:
            return 1
        else:
            a=self._ne.size()
            b = self._nw.size()
            c = self._se.size()
            d = self._sw.size()
            total=a+b+c+d
            return total

    def height(self) -> int:
        """ Return the height of <self>

        Height is measured as the number of nodes in the path from the root of this
        tree to the node at the greatest depth in this tree.

        Runtime: O(n)
        """
        if self.is_empty():
            return 0
        elif self.is_leaf():
            return 1
        else:
            a=self._ne.height()
            b = self._nw.height()
            c = self._se.height()
            d = self._sw.height()
            return max(a,b,c,d)+1

    def depth(self, tree: Tree) -> Optional[int]:
        """ Return the depth of the subtree <tree> relative to <self>. Return None
        if <tree> is not a descendant of <self>

        Runtime: O(log(n))
        """
        directions=(self._centre,tree._point)
        if self._point==tree._point:
            return 1
        elif directions==1:
            a=self._ne.depth(tree)
            if a is not None:
                return a+1
            else:
                return None
        elif directions==2:
            a = self._nw.depth(tree)
            if a is not None:
                return a + 1
            else:
                return None
        elif directions==3:
            a = self._sw.depth(tree)
            if a is not None:
                return a + 1
            else:
                return None
        else:
            a = self._se.depth(tree)
            if a is not None:
                return a + 1
            else:
                return None



    def is_leaf(self) -> bool:
        """ Return True if <self> has no children

        Runtime: O(1)
        """
        if self._se.is_empty() and self._ne.is_empty() \
                and self._sw.is_empty() and self._nw.is_empty():
            return True
        else:
            return False

    def is_empty(self) -> bool:
        """ Return True if <self> does not store any information about the location
        of any players.

        Runtime: O(1)
        """
        if self._se != []:
            return False
        elif self._ne != []:
            return False
        elif self._nw != []:
            return False
        elif self._sw != []:
            return False
        elif self._name != "":
            return False
        elif self._point != ():
            return False
        return True

def countsub_v2(treee:TwoDTree)->int:
    count = 0
    if treee._lt != []:
        count += 1
    if treee._gt != []:
        count += 1

def checksub_v2(tre:TwoDTree)->int:
    if tre._lt!=[]:
        return 1
    else:
        return 2
    
class TwoDTree(Tree):
    _name: Optional[str]
    _point: Optional[Tuple[int, int]]
    _nw: Tuple[int, int]
    _se: Tuple[int, int]
    _lt: Optional[TwoDTree]
    _gt: Optional[TwoDTree]
    _split_type: str

    def __init__(self, name: str) -> None:
        """Initialize a new Tree instance

        Runtime: O(1)
        """
        self._name = name
        self._point = ()
        self._nw = ()
        self._se = ()
        self._lt = []
        self._gt = []
        self._split_type = ""

    def __contains__(self, name: str) -> bool:
        """ Return True if a player named <name> is stored in this tree.

        Runtime: O(n)
        """
        if self.is_empty():
            return False
        elif name == self._name:
            return True
        else:
            if self._lt.__contains__(name) or self._gt.__contains__(name):
                return True
            return False

    def contains_point(self, point: Tuple[int, int]) -> bool:
        """ Return True if a player at location <point> is stored in this tree.

        Runtime: O(log(n))
        """
        if self.is_empty():
            return False
        elif self._point == point:
            return True
        elif point[0] > self._point[0] and point[1] > self._point[1]:
            return self._gt.contains_point(point)
        elif point[0] < self._point[0] and point[1] < self._point[1]:
            return self._lt.contains_point(point)
        return False

    def insert(self, name: str, point: Tuple[int, int]) -> None:
        """Insert a player named <name> into this tree at point <point>.

        Raise an OutOfBoundsError if <point> is out of bounds.

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

    def move(self, name: str, direction: str, steps: int) -> Optional[Tuple[int, int]]:
        """ Return the new location of the player named <name> after moving it
        in the given <direction> by <steps> steps.

        Raise an OutOfBoundsError if this would move the player named
        <name> out of bounds (before moving the player).

        Runtime: O(n)

        === precondition ===
        direction in ['N', 'S', 'E', 'W']
        """
        raise NotImplementedError

    def move_point(self, point: Tuple[int, int], direction: str, steps: int) -> Optional[Tuple[int, int]]:
        """ Return the new location of the player at point <point> after moving it
        in the given <direction> by <steps> steps.

        Raise an OutOfBoundsError if this would move the player at point
        <point> out of bounds (before moving the player).

        Moving a point may require the tree to be reorganized. This method should do
        the minimum amount of tree reorganization possible to move the given point properly.

        Runtime: O(log(n))

        === precondition ===
        direction in ['N', 'S', 'E', 'W']

        """
        raise NotImplementedError

    def names_in_range(self, point: Tuple[int, int], direction: str, distance: int) -> List[str]:
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
        if self._name == '' and self._point == ():
            return 0
        elif countsub_v2(self) == 0:
            return 1
        else:
            a = self._lt.size()
            b = self._gt.size()
            total = a + b
            return total

    def height(self) -> int:
        """ Return the height of <self>

        Runtime: O(n)
        """
        if self.is_empty():
            return 0
        elif self.is_leaf():
            return 1
        else:
            a = self._lt.height()
            b = self._gt.height()
            return max(a, b) + 1

    def depth(self, tree: Tree) -> Optional[int]:
        """ Return the depth of the subtree <tree> relative to <self>. Return None
        if <tree> is not a descendant of <self>

        Runtime: O(log(n))
        """
        raise NotImplementedError

    def is_leaf(self) -> bool:
        """ Return True if <self> has no children

        Runtime: O(1)
        """
        if self._lt.is_empty() and self._gt.is_empty():
            return True
        return False

    def is_empty(self) -> bool:
        """ Return True if <self> does not store any information about the location
        of any players.

        Runtime: O(1)
        """
        if self._lt != []:
            return False
        elif self._gt != []:
            return False
        elif self._name != "":
            return False
        elif self._point != ():
            return False
        return True

    def balance(self) -> None:
        """ Balance <self> so that there is at most a difference of 1 between the
        size of the _lt subtree and the size of the _gt subtree for all trees in
        <self>.
        """
        pass


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={'extra-imports': ['typing']})
