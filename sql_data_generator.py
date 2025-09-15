
from faker import Faker
import random
import string
from datetime import timedelta

fake = Faker("en_IN")   # Indian locale (names, phone numbers, etc.)

# ✅ Vehicle number generator
def generate_vehicle_number():
    state_code = random.choice(["MH","DL","GJ","RJ","KA","TN","UP","WB","PB","HR"])
    letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    return f"{state_code}{random.randint(10,99)}{letters}{random.randint(1000,9999)}"

records = []
gatepass_no = 1001

# 🔹 Generate 500 trucks passing through plant
for i in range(500):
    date = fake.date_between(start_date="-60d", end_date="today")
    vehicle_number = generate_vehicle_number()
    driver_name = fake.name()
    driver_number = fake.msisdn()[:10]
    truck_type = random.choice(["Bullet","Pack"])
    lpg_qty = random.randint(500, 20000)

    # Security In
    records.append(f"INSERT INTO Security_In VALUES ({gatepass_no}, '{date}', '{vehicle_number}', '{driver_name}', '{driver_number}', '{truck_type}', {lpg_qty});")

    # Security Out
    agency = fake.company()
    records.append(f"INSERT INTO Security_Out VALUES ({gatepass_no}, '{date}', '{vehicle_number}', '{agency}', '{driver_name}', '{driver_number}', '{truck_type}', {lpg_qty});")

    # Weighbridge
    weight_in = lpg_qty + random.randint(1000, 5000)
    weight_out = weight_in - random.randint(100, 500)
    in_time = fake.date_time_between(start_date="-60d", end_date="now")
    out_time = in_time + timedelta(hours=random.randint(1, 5))
    records.append(f"INSERT INTO Weighbridge (Gatepass_No, Truck_Type, Weight_In, Weight_Out, In_Time, Out_Time) VALUES ({gatepass_no}, '{truck_type}', {weight_in}, {weight_out}, '{in_time}', '{out_time}');")

    # Loading / Unloading
    if truck_type == "Pack":
        cyl_type = random.choice(["14kg", "19kg", "47kg"])
        records.append(f"INSERT INTO Loading (Truck_Type, Cylinder_Type, Gatepass_No) VALUES ('{truck_type}', '{cyl_type}', {gatepass_no});")
        records.append(f"INSERT INTO Unloading (Vehicle_Number, Truck_Type, Cylinder_Type, Capsule1_MT, Capsule2_MT, Capsule3_MT, Gatepass_No) VALUES ('{vehicle_number}', '{truck_type}', '{cyl_type}', NULL, NULL, NULL, {gatepass_no});")
    else:  # Bullet truck
        c1 = round(random.uniform(5, 10), 2)
        c2 = round(random.uniform(5, 10), 2)
        c3 = round(random.uniform(5, 10), 2)
        records.append(f"INSERT INTO Unloading (Vehicle_Number, Truck_Type, Cylinder_Type, Capsule1_MT, Capsule2_MT, Capsule3_MT, Gatepass_No) VALUES ('{vehicle_number}', '{truck_type}', NULL, {c1}, {c2}, {c3}, {gatepass_no});")

    # Filling center
    cyl_fill = random.choice(["5kg", "10kg", "14.5kg", "19kg", "47kg"])
    leakage = random.choice([0, 1])
    cap = random.choice([0, 1])
    manual = random.choice([0, 1])
    records.append(f"INSERT INTO Filling_Center (Cylinder_Type, Leakage_Test, Cap_Check, Manual_Test, Gatepass_No) VALUES ('{cyl_fill}', {leakage}, {cap}, {manual}, {gatepass_no});")

    gatepass_no += 1

# 🔹 HR Department – 50 employees
for emp_id in range(1, 51):
    ename = fake.name()
    sal = random.randint(20000, 60000)
    hdate = fake.date_between(start_date="-2y", end_date="today")
    dept = random.choice(["Filling", "Security", "Admin", "Weighbridge", "Maintenance"])
    desg = random.choice(["Manager", "Supervisor", "Operator", "Helper", "Clerk"])
    records.append(f"INSERT INTO HR_Department VALUES ({emp_id}, '{ename}', {sal}, '{hdate}', '{dept}', '{desg}');")

# 🔹 Save SQL file
with open("lpg_bottling_data.sql", "w", encoding="utf-8") as f:
    f.write("\n".join(records))

print("✅ SQL script with 500+ records generated successfully! File: lpg_bottling_data.sql")
