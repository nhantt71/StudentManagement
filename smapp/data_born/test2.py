import random, json

def generate_student():
    last_name = random.choice(["Nguyễn", "Trần", "Lê", "Hoàng", "Phạm",
        "Tô", "Đinh", "Phan", "Huỳnh", "Đỗ", "Phùng", "Hồ", "Dương",
        "Bùi", "Đặng", "Võ"])
    first_name = random.choice(["Khang", "Phúc", "Huy", "Bảo", "Minh",
        "Anh", "Long", "Thịnh", "Quân", "Hưng", "Hoàng", "Phương", "Huyền",
        "Nga", "Hạnh"])
    ten_lot = random.choice(["Thị", "Văn", "Cao", "Phát", "Trí", "Tài",
     "Quang", "Ngọc", "Quỳnh", "Anh", "Trúc"])
    gender = random.choice(["MALE", "FEMALE"])

    birth1 = random.choice(["1", "2"])

    if (birth1 == "1"):
        birth1 += random.choice(["98", "99"])

    if (birth1 == "2"):
        birth1 += "00"

    for i in range(1):
        birth1 += str(random.randint(0, 9))

    birth = birth1 + "-01-01"
    address = "Số 123 đường ABC, phường XYZ, quận DEF, thành phố Hồ Chí Minh"
    phone_number = "0"


    for i in range(9):
        phone_number += str(random.randint(0, 9))

    email = "student@example.com"
    class_type = random.choice(['K10', 'K11', 'K12'])

    last_name = last_name + " " + ten_lot

    return {
        "class_type": class_type,
        "acceptation": "IDLE",
        "first_name": first_name,
        "last_name": last_name,
        "gender": gender,
        "birth": birth,
        "address": address,
        "phone_number": phone_number,
        "email": email
    }

reception_students = []
for i in range(100):
    reception_students.append(generate_student())

with open("../data/reception_students.json", "a") as file:
    file.write(json.dumps(reception_students))


if __name__ == '__main__':
    __name__.run(debug=True)
