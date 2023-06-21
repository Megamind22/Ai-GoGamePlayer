from game.util import Group
WHITE=False
BLACK=True


class Model:
    def __init__(self):
        self.dead_group=[]
        self.size=19
        self.count=0
    # used for ko-rule
        self.ko = None
        self.turn=BLACK
        # game over flag
        self.game_over = False

        # the board is represented by a size x size - matrix.
        self.board = [[None for i in range(self.size)] for j in range(self.size)]

        # score from empty fields at the end of the game.
        self.score = [0, 0]

        # stones killed during the game
        self.captured = [0, 0]



    def _add(self, grp):
        """Adds a group of stones to the game
        Arguments:
            grp (Group): The group that shall be added

        Attributes updated by this function:
            self.board
        """
        for (x, y) in grp.stones:
            self.board[x][y] = grp

    def _remove(self, grp):
        """Removes a group of stones from the game
        Arguments:
            grp (Group): The group that shall be removed

        Attributes updated by this function:
            self.board
        """
        for (x, y) in grp.stones:
            self.board[x][y] = None


    def stone(self):
        # return coloropf each stone
        colors=[[None for i in range(self.size)] for j in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] is None:
                    colors[i][j] =None
                else:
                    colors[i][j]=self.board[i][j].color

        return colors



    def _kill(self, grp):
        """Removes a group of stones from the game and increases the
        counter of captured stones.
        grp (Group): The group that has been killed - needs to be removed  Attributes updated by this function: self.board
            self.captured self.group
        """
        # increase the caputured counter of the opposite color by the nr. of stones in the g

        self.captured[not grp.color] += grp.size
        print('succes',self.captured[not grp.color])
        # remove the group
        self._remove(grp)


    def _liberties(self, grp):
        """Counts the number of empty fields adjacent to the group.
        Arguments:
            grp (Group): a group of stones.
        Returns:
            (int): nr. of liberties of that group
        """
        return sum([1 for u, v in grp.border if self.board[u][v] is None])


    def add_scores(self):
        """Sums up the scores: adding empty fields + captured stones per player
        Returns:
            list (int): containing the scores of each player -self .reverse add
        """
        print("score player have black stone 1 : ", self.score[1] + self.captured[1])
        print("score player have white stone 2 : ", self.score[0] + self.captured[0] )
        return   [self.score[0] + self.captured[0], self.score[1] + self.captured[1]]


    def get_data(self):
        """Returns the data object containing all relevant information to the controller.
        Returns:
            data (dictionary): data object for the controller
        """
        data = {
            'size': self.size,
            'stones': self._stones(),
            'territory': self.territory,
            'game_over': self.game_over,
            'score': self.add_scores(),
            'color': self.turn
        }

        return data

        # Most Important Fun By Me
    def get_moves(self):
        lis=[]
        for i in range(19):
            for j in range(19):
                if self.board[i][j] is None:
                    lis.append((i,j))
        return lis


    def check_if_neigh(self, x, y):  # مفيش عمرها 4 حولياا ألا لو اننا حاككل
        flag = True
        flag2=True
        i = 0
        j = 4
        for (k,l) in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
             if k < 0 or l < 0 or k >= self.size or l >= self.size:
                 continue
             if self.board[k][l] is  None:
                 flag2=False
        if flag2:
            for (u, v) in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
                if u < 0 or v < 0 or u >= self.size or v >= self.size:
                    continue
                if self.turn == self.board[u][v].color:
                    i += 1
                if self.turn != self.board[u][v].color:
                    j -= 1
                    flag = False
            # if self.board[x][y]
            if i >= 1:
                flag = True
            if not j:  # 4 around me confirm i eat
                flag = True
        return flag  # Most #



    def place_stone(self, x, y):
        """Attempts to place a new stone.
           Validates the move and if valid, executes the respective action.
        Arguments
            x (int): x - coordinate of the new stone
            y (int): y - coordinate of the new stone
        Variables changed by this function
            self.has_passed
            self.blocked_field
            self.turn
            self.board - adds / removes / kills stones
        """
        # check if the game is finished
        if self.game_over:
            return False

        # check if the position is free
        if self.board[x][y] is not None:
            return False

        # check if the field is already blocked
        if self.ko == (x, y):
            return False

        # create new group with the given coordinates
        new_group = Group(stones=[(x, y)], color=self.turn)

        # create two lists to remember the groups to remove / kill
        groups_to_remove = []
        groups_to_kill = []
        is_valid = False

        # All direct neighbors of (x, y)
        for (u, v) in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:

            # Check if the neighbor is on the board because edges
            if u < 0 or v < 0 or u >= self.size or v >= self.size:
                continue

            # Add the neighbor to the border of the new group
            new_group.border.add((u, v))

            other_group = self.board[u][v]

            # check if neighbor is None igonre with continue nd do on fill
            if other_group is None:
                is_valid = True
                continue

            # same color

            if new_group.color == other_group.color:
                # merge the two groups
                new_group = new_group + other_group

                # remember to delte the old grp (other_group)
                groups_to_remove.append(other_group)

            # groups have different colors
            # check that there is only one free adjacent field to other_group

            elif self._liberties(other_group) == 1:
                is_valid = True

                # remember to kill the other_group
                if other_group not in groups_to_kill:
                    groups_to_kill.append(other_group)
                    self.dead_group = groups_to_kill[:]

        # new_group must have at least one free adjacent field
        if self._liberties(new_group) >= 1:
            is_valid = True

        ######################################
        # Move Execution (only if valid)
        ######################################

        # the move is valid
        if is_valid:
            # remove groups
            for grp in groups_to_remove:
                self._remove(grp)

            # kill groups
            for grp in groups_to_kill:
                self._kill(grp)




            # add the new group
            self._add(new_group)


        # the move is invalid
        else:
            return False

        ######################################
        # ko-rule: block the field where the stone has just been placed
        ######################################

        # 3 conditions for the ko-rule to apply
        # 1. the new group has only one stone
        # 2. only one group has been killed
        # 3. the killed group has only had one stone
        if new_group.size == 1 and len(groups_to_kill) == 1 and groups_to_kill[0].size == 1:
            for (x, y) in groups_to_kill[0].stones:
                self.ko = (x, y)

        else:
            self.ko = None

        ######################################
        # Turn End Actions: Change the current player
        ######################################

        # switch the color (turn)
        self.turn = WHITE if (self.turn == BLACK) else BLACK


        return True

