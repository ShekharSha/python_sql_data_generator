from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker("en_IN")   # Indian style names, numbers

records = []
gatepass_no = 1001

for i in range(500):
    # Only YYYY-MM-DD
    date = fake.date_between(start_date="-60d", end_date="today")
    date_str = date.strftime("%Y-%m-%d")

    # Generate Indian-style vehicle numbers (e.g., MH12AB1234)
    states = ["AP", "AR", "AS", "BR", "CG", "GA", "GJ", "HR", "HP", "JH", "KA", "KL", "MP", "MH", "MN", "ML", "MZ", "NL", "OD", "PB", "RJ", "SK", "TN", "TS", "TR", "UP", "UK", "WB"]
    vehicle_number = f"{random.choice(states)}{random.randint(10,99)}{fake.random_uppercase_letter()}{fake.random_uppercase_letter()}{random.randint(1000,9999)}"
    driver_name = fake.name()
    driver_number = fake.msisdn()[:10]
    truck_type = random.choice(["Bullet","Pack"])
    lpg_qty = random.randint(500, 20000)

    # Security In
    records.append(
        f"INSERT INTO Security_In VALUES ({gatepass_no}, '{date_str}', '{vehicle_number}', '{driver_name}', '{driver_number}', '{truck_type}', {lpg_qty});"
    )

    # Security Out
    agency = fake.company()
    records.append(
        f"INSERT INTO Security_Out VALUES ({gatepass_no}, '{date_str}', '{vehicle_number}', '{agency}', '{driver_name}', '{driver_number}', '{truck_type}', {lpg_qty});"
    )

    # Weighbridge
    weight_in = lpg_qty + random.randint(1000, 5000)
    weight_out = weight_in - random.randint(100, 500)
    in_time = fake.date_time_between(start_date="-60d", end_date="now")
    out_time = in_time + timedelta(hours=random.randint(1, 5))
    in_time_str = in_time.strftime("%Y-%m-%d %H:%M")   # No seconds
    out_time_str = out_time.strftime("%Y-%m-%d %H:%M")

    records.append(
        f"INSERT INTO Weighbridge (Gatepass_No, Truck_Type, Weight_In, Weight_Out, In_Time, Out_Time) "
        f"VALUES ({gatepass_no}, '{truck_type}', {weight_in}, {weight_out}, '{in_time_str}', '{out_time_str}');"
    )

    # Loading / Unloading
    if truck_type == "Pack":
        cyl_type = random.choice(["14kg","19kg","47kg"])
        records.append(
            f"INSERT INTO Loading (Truck_Type, Cylinder_Type, Gatepass_No) VALUES ('{truck_type}', '{cyl_type}', {gatepass_no});"
        )
        records.append(
            f"INSERT INTO Unloading (Vehicle_Number, Truck_Type, Cylinder_Type, Capsule1_MT, Capsule2_MT, Capsule3_MT, Gatepass_No) "
            f"VALUES ('{vehicle_number}', '{truck_type}', '{cyl_type}', NULL, NULL, NULL, {gatepass_no});"
        )
    else:
        c1 = round(random.uniform(5, 10),2)
        c2 = round(random.uniform(5, 10),2)
        c3 = round(random.uniform(5, 10),2)
        records.append(
            f"INSERT INTO Unloading (Vehicle_Number, Truck_Type, Cylinder_Type, Capsule1_MT, Capsule2_MT, Capsule3_MT, Gatepass_No) "
            f"VALUES ('{vehicle_number}', '{truck_type}', NULL, {c1}, {c2}, {c3}, {gatepass_no});"
        )

    # Filling center
    cyl_fill = random.choice(["5kg","10kg","14.5kg","19kg","47kg"])
    leakage = random.choice([0,1])
    cap = random.choice([0,1])
    manual = random.choice([0,1])
    records.append(
        f"INSERT INTO Filling_Center (Cylinder_Type, Leakage_Test, Cap_Check, Manual_Test, Gatepass_No) "
        f"VALUES ('{cyl_fill}', {leakage}, {cap}, {manual}, {gatepass_no});"
    )

    gatepass_no += 1

# HR Department sample employees
for emp_id in range(1, 51):   # 50 staff
    ename = fake.name()
    sal = random.randint(20000, 60000)
    hdate = fake.date_between(start_date="-2y", end_date="today")
    hdate_str = hdate.strftime("%Y-%m-%d")  # Only YYYY-MM-DD
    dept = random.choice(["Filling","Security","Admin","Weighbridge","Maintenance"])
    desg = random.choice(["Manager","Supervisor","Operator","Helper","Clerk"])
    records.append(
        f"INSERT INTO HR_Department VALUES ({emp_id}, '{ename}', {sal}, '{hdate_str}', '{dept}', '{desg}');"
    )

# Write to SQL file
with open("lpg_bottling_data.sql", "w", encoding="utf-8") as f:
    f.write("\n".join(records))

print("✅ SQL script with 500+ records generated successfully!")
