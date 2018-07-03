from game import Game


class Solitaire(Game):
    """
    A game state of solitaire in Shenzhen I/O.
    """

    SUITS = ('Red', 'Green', 'Black', 'Flower')

    class Card:
        """
        A mahjong card in the solitaire game in Shenzhen I/O.

        """

        def __init__(self, suit, number):
            assert suit in Solitaire.SUITS
            assert number in tuple(range(1, 10)) + ('Dragon', 'Flower', 'Stack')

            self.suit = suit
            self.number = number

        def __eq__(self, other):
            return isinstance(other, Solitaire.Card) \
                   and self.suit == other.suit and self.number == other.number

        def __repr__(self):
            return self.suit[0] + (str(self.number) if isinstance(self.number, int) else self.suit[0])

    def __init__(self, piles):
        """
        Init game state with a given piles of cards.
        self.piles: the stacks of cards on the bottom;
        self.temps: the temporary spaces on the upper left;
        self.goals: the goal spaces on the upper right;
        self.flower: the space for the flower card.
        """
        assert len(piles) == 8
        assert all([len(pile) == 5 for pile in piles])
        assert all([all([isinstance(card, Solitaire.Card) for card in pile]) for pile in piles])

        self.piles = piles
        self.temps = [None, None, None]
        self.goals = {'Red': 0, 'Green': 0, 'Black': 0}
        self.flower = None

    def __copy__(self):
        copy = Solitaire(self.piles)
        copy.temps = self.temps
        copy.goals = self.goals
        copy.flower = self.flower
        return copy

    def is_goal(self):
        """
        Return True if the game is in goal state, which is equal to there are
        no cards left in the bottom.
        """
        return not any(self.piles)

    def _can_stack_dragons(self, suit):
        """
        Returns True if it is possible to remove the dragons of the given SUIT
        and to pile them up in an empty temporary space.
        """
        target = Solitaire.Card(suit, 'Dragon')
        if all(self.temps) and target not in self.temps:
            return False

        count = 0
        for card in self.temps:
            if card == target:
                count += 1
        for pile in self.piles:
            if pile[-1] == target:
                count += 1

        return count == 4

    def _stack_dragons(self, suit):
        """
        Remove the dragons of the given SUIT and stack them up in an empty
        temporary space. Assumes the action is possible.
        """
        target = Solitaire.Card(suit, 'Dragon')
        for i in range(len(self.temps)):
            if self.temps[i] == target:
                self.temps[i] = None
        for i in range(len(self.piles)):
            if self.piles[i] and self.piles[i][-1] == target:
                self.piles[i] = self.piles[i][:-1]

        for i in range(len(self.temps)):
            if self.temps[i] is None:
                self.temps[i] = Solitaire.Card(suit, 'Stack')

    def _can_move_to_goal(self, card):
        return card.number == self.goals[card.suit] + 1 and self.goals[card.suit] == min(self.goals.values())

    def _refresh(self):
        """
        Continuously moving possible cards to goal or flower space.
        """
        flag = False
        while flag:
            flag = False
            for i in range(len(self.temps)):
                card = self.temps[i]
                if self._can_move_to_goal(card):
                    self.goals[card.suit] += 1
                    self.piles[i] = self.piles[i][:-1]
                    flag = True
            for i in range(len(self.piles)):
                card = self.piles[i][-1]
                if card.suit == 'Flower':
                    self.flower = card
                    self.piles[i] = self.piles[i][:-1]
                    flag = True
                elif self._can_move_to_goal(card):
                    self.goals[card.suit] += 1
                    self.piles[i] = self.piles[i][:-1]
                    flag = True

    @staticmethod
    def _stackable(top, bottom):
        """
        Returns TRUE if the card BOTTOM can be stacked under the card TOP, or
        FALSE otherwise.
        """
        return top.suit != bottom.suit and top.number == bottom.number + 1

    def _get_stack_in_pile(self, index):
        """
        Reverses and returns the bottom largest movable stack in the pile given by the
        INDEX. Reverse is for easy counting.
        """
        pile = self.piles[index]
        if not pile:
            return []
        i = len(pile) - 1
        while Solitaire._stackable(pile[i - 1], pile[i]):
            i -= 1
        return pile[i:][::-1]

    class LOCATION:
        def __init__(self, source, location):

    class Action:
        """
        Actions allowed in the Solitaire game.
        """

        LOCATIONS = ('piles', 'temps', 'goals')

        def __init__(self, src, src_loc, src_size, target, target_loc):
            assert src in self.LOCATIONS
            assert target in self.LOCATIONS
            self.src = src
            self.src_loc = src_loc
            self.src_size = src_size
            self.target = target
            self.target_loc = target_loc

    def _get_actions_by_card(self, card):
        actions = []
        for i in range(len(self.piles)):
            if Solitaire._stackable(self.piles[j][-1], card):
                actions += [Solitaire.Action('piles', i, num + 1, 'piles', card)]


    def get_actions(self):
        actions = []

        for i in range(len(self.piles)):
            stack = self._get_stack_in_pile(i)
            # Move to another stack
            for num, card in enumerate(stack):
                for j in range(len(self.piles)):
                    if Solitaire._stackable(self.piles[j][-1], card):
                        actions += [Solitaire.Action('piles', i, num + 1, 'piles', j)]



    def _remove_cards(self, src, src_loc, src_size):
        """
        Removes and returns a stack of cards.
        :param src: The source location of removal. Either 'piles' or 'temps'.
        :param src_loc: The index in the source location.
        :param src_size: The size of the stack of cards to be removed. Only
        applied when SRC == 'piles'.
        :return: A list of cards in stacks.
        """
        if src == 'piles':
            result = self.piles[src_loc][-src_size:]
            self.piles[src_loc] = self.piles[src_loc][:-src_size]
        elif src == 'temps':
            result = [self.temps[src_loc]]
            self.temps = None
        return result

    def get_next_state(self, action):
        """
        Returns the next state given the next ACTION, including the automatic
        goal-moves made by the board.
        """

        assert isinstance(action, Solitaire.Action)

        next_state = self.__copy__()

        stack = next_state._remove_cards(action.src, action.src_loc, action.src_size)
        if action.target == 'piles':
            next_state.piles[action.target_loc] += stack
            assert len(next_state._get_stack_in_pile(action.target_loc)) > len(stack)
        elif action.target == 'temps':
            assert len(stack) == 1
            assert self.temps[action.target_loc] is None
            self.temps[action.target_loc] = stack[0]
        elif action.target == 'goals':
            assert len(stack) == 1
            assert self.goals[stack[0].suit] == stack[0].number - 1
            self.goals[stack[0].suit] += 1

        next_state._refresh()

        return next_state
