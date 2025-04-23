import psycopg2
import csv
import os
conn =psycopg2.connect(
    dbname = "lab10",
    user = "postgres",
    password = "vilence1985",
    host = "127.0.0.1",
    port = "5432"
)

curr = conn.cursor()

menu = '''
1. Inserting data from file
2. Entering user name, phone from console
3. Update
4. Search   
5. Delete
'''
print(menu)
n = int(input("Номер запроса: "))
if n == 1:
    filepath = "C:/Users/almas/Desktop/Laba1-main/lab10/contact.csv" 
    with open(filepath, 'r') as f:
        rd = csv.DictReader(f)
        for row in rd:
            try:
                curr.execute(
                    "INSERT INTO phonebook (first_name,last_name, phone) VALUES (%s, %s,%s)",
                    (row['first_name'],row['last_name'], row['phone'])
                )
                conn.commit()
            except Exception as m:
                print(f"Ошибка: {m}")

elif n == 2:
    name = input("Enter first name: ")
    last= input("Enter last name: ")
    phone = input("Enter phone number: ")
    try:
        curr.execute(
            "INSERT INTO phonebook (first_name,last_name , phone) VALUES (%s , %s , %s)",
            (name,last, phone)
        )
        conn.commit()
        print("OK!!!")
    except Exception as m:
        print(f"Ошибка: {m}")
elif n == 3:
    choice = '''
        1. Имя по номеру телефона
        2. Номер телефона по имени
    '''
    print(choice)
    q = int(input("Введите номер запроса: "))
    if q == 1:
        ph = input("Ваш номер телефона: ")
        n_name = input("Новое имя: ")
        curr.execute(
            "UPDATE phonebook SET first_name = %s WHERE phone = %s", (n_name, ph)
        )
    elif q == 2:
        name = input("Введите имя: ")
        ph = input("Введите новый номер телефона: ")
        curr.execute(
            "UPDATE phonebook SET phone = %s WHERE first_name = %s", (ph, name)
        )
    else:
        print("Ошибка!")
    conn.commit()
elif n == 4:
    pt = input("Введите какую то информацию: ")
    curr.execute(
        "SELECT * FROM phonebook WHERE first_name ILIKE %s OR phone ILIKE %s", (f"%{pt}%", f"%{pt}%")
    )
    rw = curr.fetchall()
    if rw:
        for row in rw:
            print(row)
    else:
        print("Ничего не найдено")
elif n == 5:
    choice = '''
        1. Удалить по имени
        2. Удалить по номеру телефонa
    '''
    print(choice)
    q = int(input("Введите свой выбор: "))
    if q == 1:
        name = input("Введите имя: ")
        curr.execute(
            "DELETE FROM phonebook WHERE first_name = %s", (name,)
        )
    elif q == 2:
        ph = input("Введите номер телефона: ")
        curr.execute(
            "DELETE FROM phonebook WHERE phone = %s", (ph,)
        )
    conn.commit()
    print("OK!")
curr.close()
conn.close()