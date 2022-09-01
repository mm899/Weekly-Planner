class Day:
    """
    Represents each day of the week, stores the shifts/positions for the day.
    """

    def __init__(self, day, position_titles):
        self.day_of_Week = day
        self.positions = {}
        for title in position_titles:
            self.positions[title] = dict()
