class Shift:
    """
    Represents shifts for a given position, contains the employee, hours, and pay rate.
    """

    _time_dictionary = {
        10.0: "10:00am",
        10.5: "10:30am",
        11.0: "11:00am",
        11.5: "11:30am",
        12.0: "12:00pm",
        12.5: "12:30pm",
        13.0: "1:00pm",
        13.5: "1:30pm",
        14.0: "2:00pm",
        14.5: "2:30pm",
        15.0: "3:00pm",
        15.5: "3:30pm",
        16.0: "4:00pm",
        16.5: "4:30pm",
        17.0: "5:00pm",
        17.5: "5:30pm",
        18.0: "6:00pm",
        18.5: "6:30pm",
        19.0: "7:00pm",
        19.5: "7:30pm",
        20.0: "8:00pm",
        20.5: "8:30pm",
        21.0: "9:00pm",
        21.5: "9:30pm",
        22.0: "10:00pm",
        22.5: "10:30pm",
        23.0: "11:00pm"
    }

    def __init__(self, position_title, day_of_week, employee, start_time, end_time, pay_rate):
        self.position_title = position_title
        self.day_of_week = day_of_week
        self.employee = employee
        self.start_time = start_time
        self.end_time = end_time
        self.pay_rate = pay_rate
        self.id = position_title + " "+ day_of_week + " " + employee.name + " " + str(start_time) + " " + str(end_time)

    def __str__(self):
        # return f"[{self.employee.name} - hours: {self._time_dictionary[self.start_time]} : " \
        #        f"{self._time_dictionary[self.end_time]} - rate: {self.pay_rate}]"
        return f"[{self.employee.name} - {self._time_dictionary[self.start_time]} : " \
               f"{self._time_dictionary[self.end_time]} - £{self.pay_rate}/h]"
