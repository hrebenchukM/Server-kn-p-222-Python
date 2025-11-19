def write_file(filename: str = "file.txt") -> None:
    'Приклад без ресурсного блоку - звільнення ресурсу забезпечує код'
    file = None
    try:
        file = open(filename, mode="w", encoding="utf-8")
        file.write("Latin data\n")    # новий рядок не переводиться, символ потрібний у даних
        file.write("Кириличні дані")  # перевірка того, що необхідно зазначати encoding
        file.flush()
    except OSError as err:
        print("File write error:", err)
    else:
        print("File written successfully")
    finally:
        if file is not None:
            file.close()


def write_file_with(filename: str = "file_with.txt") -> None:
    'Приклад з ресурсним блоком - звільнення ресурсу забезпечує інтерпретатор'
    try:
        with open(filename, mode="w", encoding="utf-8") as file:
            file.write("Latin data\n")
            file.write("Букви кирилиці\n")
            file.flush()
    except OSError as err:
        print("File write error:", err)
    else:
        print("File written successfully")


def read_file(filename: str = "file.txt") -> None:
    'Приклад читання файлу з ресурсним блоком'
    try:
        with open(filename, mode="r", encoding="utf-8") as file:
            # print(file.read())  # зчитує весь контент файлу як рядок
            for line in file :    # ітерація файлу іде по рядках (\n)
                print(line)       # сам символ '\n' залишається у рядку
                print('---')
    except OSError as err:
        print("File read error:", err)
    else:
        print("File read successfully")



def read_ini(filename: str = "db.ini") -> dict:
    """Читает конфигурационный файл типа "ini".
    Игнорирует комментарии и возвращает словарь с парами "ключ": "значение".
    При ошибке передается ошибка в исключении OS.
    """
    res = {}
    try:
        with open(filename, encoding='utf-8') as file:
            for line in file:
                line = line.split('#')[0].split(';')[0] # удаление комментариев
                if not ':' in line: # пропуск некорректных строк
                    continue
                pair = line.split(':',1) # розділення на пару ключ-значення
                res[pair[0].strip()] = pair[1].strip()  # ~trim()   # [:-1]   # slice [start:end:step]
        return res
    except OSError as e:
        raise e



def read_ini2(filename:str="db.ini") -> dict :
    'Функциональный стиль'
    with open(filename, encoding='utf-8') as file :
      return {
            k.strip(): v.strip()
            for line in file
            if ':' in line.split('#')[0].split(';')[0]
            for k, v in [line.split('#')[0].split(';')[0].split(':', 1)]
        }



def main():
   # write_file()
   # write_file_with()
   # read_file()
    try:
        config = read_ini('db.ini')
        print(config)
        config2 = read_ini2('db.ini')
        print(config2)
    except OSError as err:
       print(f"Произошла ошибка: {err}")

if __name__ == "__main__":
    main()
