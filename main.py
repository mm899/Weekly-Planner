from wtforms import Form, StringField, SubmitField, SelectField
from flask import Flask, render_template, request
from flask.views import MethodView
from os.path import exists
import pickle

from weeklyPlanner.employee import Employee
from weeklyPlanner.week import Week

app = Flask(__name__)


class HomePage(MethodView):

    def get(self):
        return render_template('index.html')


class PlannerPage(MethodView):

    def __init__(self):
        self.week = None
        self.load_week()

    def load_week(self):
        if not exists("files/week.pkl"):
            print("Week.pkl does not exist, creating file...")
            self.week = Week("21/09/2022", "files/positions.txt")
            self.save_week()
        else:
            with open("files/week.pkl", "rb") as input:
                self.week = pickle.load(input)
                print("Week.pkl has successfully been loaded!")

    def save_week(self):
        with open("files/week.pkl", "wb") as output:
            pickle.dump(self.week, output, pickle.HIGHEST_PROTOCOL)
            print("Week.pkl has successfully been saved!")

    def get(self):
        headings, data = self.week.to_table()

        # Converts the cell back into a list object from a string.
        for row in data:
            for cell in row:
                if cell != "None":
                    items_list = cell.split("\n")
                    row_index = data.index(row)
                    cell_index = data[row_index].index(cell)
                    data[row_index][cell_index] = items_list

        shift_form = AddShiftForm()
        remove_form = RemoveShiftForm()
        remove_form.shift_id.choices = self.week.shift_receipts

        return render_template('planner.html', headings=headings, data=data, shiftform=shift_form,
                               removeform=remove_form)

    def post(self):
        # Initialising the week object and employees.
        file = open("files/employees.txt", "r")
        raw_contents = file.readlines()
        employees_dict = {}
        for content in raw_contents:
            name = content.replace("\n", "")
            employees_dict[name] = Employee(name)

        print(f"Length of the requests.form: {len(request.form)}")

        if len(request.form) == 7:
            shift_form = AddShiftForm(request.form)
            self.week.add_shift(shift_form.position_title.data,
                                shift_form.day_of_Week.data.lower(),
                                employees_dict[shift_form.employee.data],
                                float(shift_form.start_time.data),
                                float(shift_form.end_time.data),
                                float(shift_form.pay_rate.data))
            self.save_week()
            # print(self.week.shift_receipts)
        elif len(request.form) == 2:
            remove_form = RemoveShiftForm(request.form)
            self.week.remove_shift(remove_form.shift_id.data)
            self.save_week()

        # if shift_form.shift_id.data != None:
        #     self.week.remove_shift(shift_form.shift_id.data)

        headings, data = self.week.to_table()

        # Converts the cell back into a list object from a string.
        for row in data:
            for cell in row:
                if cell != "None":
                    items_list = cell.split("\n")
                    row_index = data.index(row)
                    cell_index = data[row_index].index(cell)
                    data[row_index][cell_index] = items_list

        shift_form = AddShiftForm()
        remove_form = RemoveShiftForm()
        remove_form.shift_id.choices = self.week.shift_receipts

        return render_template('planner.html', headings=headings, data=data, shiftform=shift_form,
                               removeform=remove_form)


class AddShiftForm(Form):
    time_list = [
        10.0,
        10.5,
        11.0,
        11.5,
        12.0,
        12.5,
        13.0,
        13.5,
        14.0,
        14.5,
        15.0,
        15.5,
        16.0,
        16.5,
        17.0,
        17.5,
        18.0,
        18.5,
        19.0,
        19.5,
        20.0,
        20.5,
        21.0,
        21.5,
        22.0,
        22.5,
        23.0
    ]

    # Gets list of positions for dropdown list.
    file = open("files/positions.txt", "r")
    _raw_contents = file.readlines()
    _positions_list = []
    for content in _raw_contents:
        _positions_list.append(content.lower().replace("\n", ""))

    # Gets list of employees for dropdown list.
    file = open("files/employees.txt", "r")
    _raw_contents = file.readlines()
    _employees_list = []
    for content in _raw_contents:
        _employees_list.append(content.replace("\n", ""))

    _days_of_week = [
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday'
    ]

    # position_title, day_of_week, employee, start_time, end_time, pay_rate
    position_title = SelectField(label="Position: ", choices=_positions_list)
    day_of_Week = SelectField(label="Day: ", choices=_days_of_week)
    employee = SelectField(label="Employee: ", choices=_employees_list)
    start_time = SelectField(label="Start Time: ", choices=time_list)
    end_time = SelectField(label="End Time: ", choices=time_list)
    pay_rate = StringField(label="Pay Rate: ")
    button = SubmitField("Submit")


class RemoveShiftForm(Form):
    shift_id = SelectField(label="Shift ID: ", choices=[])
    button = SubmitField("Remove")


app.add_url_rule('/', view_func=HomePage.as_view('home_page'))
app.add_url_rule('/planner', view_func=PlannerPage.as_view('planner_page'))

app.run(debug=True)
