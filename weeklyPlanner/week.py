from multipledispatch import dispatch
from tabulate import tabulate

from weeklyPlanner.shift import Shift
from weeklyPlanner.day import Day
from weeklyPlanner.employee import Employee


class Week:
    """
    Represents a week object, a Week object consists of several Day objects from Monday to Friday.
    """

    _days_of_week = [
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday'
    ]

    def __init__(self, date, positions_path):
        self.shift_receipts = []
        self._position_titles = []
        self.date = date

        self._add_positions(positions_path)

        self.days = {}
        for day in self._days_of_week:
            d = day.lower()
            self.days[d] = Day(d, self._position_titles)

    def _add_positions(self, path):
        file = open(path, "r")
        raw_contents = file.readlines()
        for content in raw_contents:
            self._position_titles.append(content.lower().replace("\n", ""))

    def add_shift(self, position_title, day_of_week, employee, start_time, end_time, pay_rate):
        shift = Shift(position_title=position_title,
                      day_of_week=day_of_week,
                      employee=employee,
                      start_time=start_time,
                      end_time=end_time,
                      pay_rate=pay_rate)
        self.days[day_of_week].positions[position_title][shift.id] = shift
        self.shift_receipts.append(shift.id)

    @dispatch(str, str, Employee, float, float)
    def remove_shift(self, position_title, day_of_week, employee, start_time, end_time):
        shift_id = position_title + " " + day_of_week + " " + employee.name + " " + str(start_time) + " " + str(end_time)
        if shift_id in self.shift_receipts:
            self.shift_receipts.remove(shift_id)
            del (self.days[day_of_week].positions[position_title][shift_id])

    @dispatch(str)
    def remove_shift(self, shift_id):
        if shift_id in self.shift_receipts:
            self.shift_receipts.remove(shift_id)
            for day in self._days_of_week:
                for position in self.days[day.lower()].positions:
                    for shift in self.days[day.lower()].positions[position].keys():
                        if shift_id == shift:
                            del (self.days[day.lower()].positions[position][shift])
                            print(f"Successfully removed Shift ID: {shift_id}")
                            break

    def to_table(self):
        table = [["" for _ in self._days_of_week] for _ in self._position_titles]

        headings = self._days_of_week.copy()
        headings.insert(0, "Positions")

        for position_index in range(len(self._position_titles)):
            table[position_index].insert(0, self._position_titles[position_index])

        for day in self._days_of_week:
            for position in self.days[day.lower()].positions:
                if len(self.days[day.lower()].positions[position]) > 0:

                    unordered_list = []

                    for key in self.days[day.lower()].positions[position].keys():
                        unordered_list.append(self.days[day.lower()].positions[position][key])

                    unordered_list.sort(key=lambda x: x.start_time)

                    for item in unordered_list:
                        position_title = item.position_title
                        row = self._position_titles.index(position_title)
                        day_of_week = item.day_of_week
                        column = self._days_of_week.index(str(day_of_week).capitalize()) + 1

                        if table[row][column] == "":
                            table[row][column] = str(item)
                        else:
                            table[row][column] = table[row][column] + "\n" + str(item)

        print(tabulate(table, headers=headings, tablefmt='grid'))

        return headings, table

    def __str__(self):
        print("\n" + "#" * 85)
        print((" " * 29) + f"Week commencing: {self.date}")
        print("#" * 85)
        for day in self._days_of_week:
            print(f"\nDay of week: {day}")
            for position in self.days[day.lower()].positions:
                print((" " * 13) + f"Position: {position}")
                for shift in self.days[day.lower()].positions[position]:
                    print((" " * 22) + f"- {self.days[day.lower()].positions[position][shift]}")
        print("\n" + ("#" * 85) + "\n")

        return ""
