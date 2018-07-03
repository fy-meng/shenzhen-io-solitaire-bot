class Game:
    """
    A abstract class of game states.
    """

    def is_goal(self):
        return False

    def get_actions(self):
        return []

    def get_next_state(self, action):
        return self
