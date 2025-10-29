import json
from datetime import datetime

data1 = '''{
    "x": 10,
    "y": 0.123,
    "w": 1.2e-2,
    "t": true,
    "f": false,
    "n": null,
    "arr": [1, 2, "3"],
    "o": {
        "s": "The string",
        "date": "2025-10-29"
    },
    "b": 12345678901234567890123456789012345678901234567890,
    "c": "Вітання усім",
    "p": 0.1234567890123456789012345678901234567890
}'''

data2 = '''[10, 1.23, "String", {"x": 10}]'''


data3 = '''{
    "program": "exec logger",
    "execMoments": []
}'''


def main():

    


    print("---------ДЗ-----------")
    try:
        with open("log.json", "r", encoding="utf-8") as fp:
            jlog = json.load(fp)

    except FileNotFoundError:
        print("Файл не знайдено!")
        jlog = json.loads(data3)

    except OSError as err:
        print("Помилка читання файлу :", err)
  
    except json.decoder.JSONDecodeError as err:
        print("Помилка декодування файлу:", err)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    jlog["execMoments"].append(now)

    with open("log.json", "w", encoding="utf-8") as fp:
        json.dump(jlog, fp, ensure_ascii=False, indent=4)

    count = len(jlog["execMoments"]) - 1
    if count == 0:
        print("програма запущена вперше.")
    else:
        print(f"програма запускалась попередньо {count} раз(и) о:")
        for m in jlog["execMoments"][:-1]:
            print(" ", m)

    print("новий запуск програми:", now)
    print("----------------------")



    # j = json.loads(data1)
    # print(type(j), j)
    # print("----------------------")
    
    # j2 = json.loads(data2)
    # print(type(j2), j2)
    # print("----------------------")
    
    # j_str = json.dumps(j)
    # print(j_str)
    # print("----------------------")
    
    # j_str = json.dumps(j, ensure_ascii=False, indent=4)
    # print(type(j_str), j_str)
    # print("----------------------")
    

    # with open("07_json.json", mode="w", encoding="utf-8") as fp:
    #     json.dump(j, fp, ensure_ascii=False, indent=4)

    # print("----------------------")
    # with open("07_json.json", encoding="utf-8") as fp:
    #     j3 = json.load(fp)
    # print(type(j3), j3)
    # print("----------------------")


# try:
#     with open("07_json_err.json", "r", encoding="utf-8") as fp:
#         j3 = json.load(fp)
# except OSError as err:
#     print("Помилка читання файлу:", err)
# except json.decoder.JSONDecodeError as err:
#     print("Помилка декодування файлу:", err)
# except FileNotFoundError:
#     print("Файл не знайдено!")
# else:
#     print(type(j3), j3)


if __name__ == "__main__":
    main()
