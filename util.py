class Group(object):
    """Represents a group of connected stones on the board.
    Attributes:
        stones (set): list of all coordinates where the group has a stone
        border (set): list of all fields that are adjacent to the group
                      For a new group empty fields must be added manually
                      since the group does not know about the field size
        color (bool): color of the group
    Property:
        size (int): equal to len(self.stones), the number of stones in
                    the group.
    """

    def __init__(self, stones=None, color=None):
        """
        Initialise group
        """
        if stones is not None:
            self.stones = set(stones)
        else:
            self.stones = set()

        self.border = set()
        self.color = color

    def __add__(self, other):
        """To add two groups of the same color
        The new group contains all the stones of the previous groups and
        the border will be updated correctly.
        Raises:
            TypeError: The colours of the groups do not match
        """
        if self.color != other.color:
            raise ValueError('Only groups of same colour can be added!')
        grp = Group(stones=self.stones.union(other.stones))
        grp.color = self.color
        grp.border = self.border.union(other.border).difference(grp.stones)
        return grp

    @property
    def size(self):
        """Size of the group"""
        return len(self.stones)
