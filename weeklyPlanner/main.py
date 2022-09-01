from weeklyPlanner.employee import Employee
from weeklyPlanner.week import Week

Mahid = Employee("Mahid Miah")
Majeed = Employee("Majeed Miah")
week = Week("21/09/2022", "../files/positions.txt")
week.add_shift("till 1", "monday", Majeed, 17.5, 23.0, 7.0)
week.add_shift("till 1", "monday", Mahid, 10.5, 17.0, 7.5)


print(week)
# print(week.shift_receipts)

# week.remove_shift('grillmondayMahid Miah10:30 - 17:00')

print(week)
# print(week.shift_receipts)

week.to_table()
