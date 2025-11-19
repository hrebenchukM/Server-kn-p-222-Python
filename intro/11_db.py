# Робота з БД. Основи. Підключення. Команди

# Підготовчий етап: створюємо окрему БД та користувача для неї
# (орієнтуємось на СУБД MySQL)
# CREATE DATABASE server_222;

# CREATE USER 'user_222'@'localhost' IDENTIFIED BY 'pass_222';

# GRANT ALL PRIVILEGES ON server_222.* TO 'user_222'@'localhost';

# FLUSH PRIVILEGES;

# pip install mysql-connector-python

import mysql.connector
from datetime import datetime

# Параметри підключення до MySQL
db_ini = {
    "host": "localhost",
    "port": 3306,  
    "user": "user_222",
    "password": "pass_222",
    "database": "server_222",
    "charset": "utf8mb4",
    "collation": "utf8mb4_unicode_ci",
    "use_unicode": True
}
db_connection = None     # підключення бажано перевикористовувати, тому робити загальнодоступним

def connect() :
    global db_connection
    try :
        db_connection = mysql.connector.connect(**db_ini)
    except mysql.connector.Error as err :
        print(err)
    else :
        print("Connection Ok")


        
def demo1() :
    sql = "select current_timestamp union all select current_timestamp"
    try :
        cursor = db_connection.cursor()    # ~Statement - контекст (оточення) виконання запиту
        cursor.execute(sql)                # поділу за типом команд - немає 
    except mysql.connector.Error as err :  # Результати виконання запиту (за замовчанням)
        print(err)                         # розподіляються на два кортежі - 
    else :                                 # окремо імена колонок:
        print(cursor.column_names)         # ('current_timestamp',)
        row = next(cursor)                 # окремо самі дані:
        print(row)                         # (datetime.datetime(2025, 11, 6, 13, 8, 58),)
    finally :                              # Закриття курсора звільняє ресурс-генератор відповіді БД
        try: cursor.close()                # Дані, що не зчитані, призводять до помилки "Unread result found"
        except: pass                       # Для примусового закриття потрібен ще один try


def demo2() :
    global db_connection
    sql = "select uuid() union select uuid()"
    try :                                           # Рекомендована схема - блок з авто-закриттям (with) 
        with db_connection.cursor(dictionary=True   # Додатковий параметр dictionary
                                  ) as cursor :     # дозволяє формувати результати з іменами (як dict)
            cursor.execute(sql)                     #                     
            for row in cursor :                     # Цикл-ітератор гарантує повну вибірку результатів,    
                print(row)                          # а також захищає від їх відсутності
    except mysql.connector.Error as err :           # {'uuid()': 'b941845a-bb07-11f0-83b6-62517600596c'}                      
        print(err)


def demo3() :
    global db_connection
    sql = "select uuid(), uuid() union select uuid(), uuid()"
    try :                                           # ?? Що трапиться якщо у запиті будуть однакові імена полів? 
        with db_connection.cursor(dictionary=True   # Зворотний бік параметра dictionary полягає у тому, що 
                                  ) as cursor :     # дані для полів з однаковими іменами перезаписуються
            cursor.execute(sql)                     # 
            print(cursor.column_names)              # ('uuid()', 'uuid()')
            for row in cursor :                     # {'uuid()': '50d9da76-bb08-11f0-83b6-62517600596c'}   
                print(row)                          # {'uuid()': '50d9db9a-bb08-11f0-83b6-62517600596c'}
    except mysql.connector.Error as err :           # !! Слід дотримуватись традиції іменування полів БД                  
        print(err)                                  # коли імена полів збігаються, то значення теж повинні


def demo_par() :                                    # Параметризовані запити - у яких розділяється
    global db_connection                            # текст команди та її параметри.
    sql = "select datediff(current_date, %s) Days"  # До SQL додаються плейсхолдери (%s), а до 
    try :                                           # execute - другий аргумент з переліком підстановки
        with db_connection.cursor(dictionary=True   # 
                                  ) as cursor :     # 
            cursor.execute(sql, ('2025-01-01',))    # кома потрібна коли кортеж складається з одного 
            for row in cursor :                     # елемента, іншакше дужки сприймаються як група
                print(row)                          # 
    except mysql.connector.Error as err :           # 
        print(err)                                  # 


def demo_prep() :                                   # Підготовлені запити (prepared) - виконуються у
    global db_connection                            # два етапи: підготовка та виконання.
    sql = "select datediff(current_date, ?) Days"   # У якості плейсхолдера - "?"
    try :                                           # Такий тип запитів краще підходить для однакових
        with db_connection.cursor(dictionary=True,  # запитів, які відрізняються тільки значенням 
                                  prepared=True     # аргументів, наприклад, отримання щоденної 
                                  ) as cursor :     # статистики за тиждень чи місяць, коли в запиті
            cursor.execute(sql, ('2025-01-01',))    # змінються тільки номер дня чи дата.
            print(next(cursor))                     # 
            cursor.execute(sql, ('2025-10-01',))    # Технічно - у СУБД створюється тимчасова процедура
            print(next(cursor))                     # яка викликається декілька разів з різними даними
    except mysql.connector.Error as err :           # (один раз компілюється і кілька разів виконується)
        print(err)                                  # 


def demo_date():
    global db_connection
    u_input = input("Введіть дату YYYY-MM-DD:").strip()

    try:
        datetime.strptime(u_input, "%Y-%m-%d")
    except ValueError:
        print("Невірний формат. Треба YYYY-MM-DD")
        return

    sql = "select datediff(current_date, %s) as Days"

    try:
        with db_connection.cursor(dictionary=True) as cursor:
            cursor.execute(sql, (u_input,))
            row = next(cursor, None)
            if row:
                diff = row["Days"]
                if diff == 0:
                    print("Дата є сьогодні")
                elif diff > 0:
                    print(f"Дата у минулому  {diff} дні потому")
                else:
                    print(f"Дата у майбутньому  через {abs(diff)} дні")
    except mysql.connector.Error as err:
        print(err)



def main():
    
    if db_connection is None :
        connect()

    if db_connection :
    #     #demo1()
    #     demo2()
    #     print("------------------------------------------------------------")
    #     demo3()
    #     print("------------------------------------------------------------")
    #     demo_par()
    #     print("------------------------------------------------------------")
    #     demo_prep()
          demo_date()


if __name__ == '__main__':
    main()