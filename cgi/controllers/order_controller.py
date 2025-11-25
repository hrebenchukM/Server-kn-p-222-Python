from models.cgi_request import CgiRequest
import json, sys

class OrderController :

    def __init__(self, cgi_request:CgiRequest, dev_mode:bool=False):
        self.cgi_request = cgi_request
        self.dev_mode = dev_mode


    def service(self) :
        action_name = "do_" + self.cgi_request.method.lower()
        try :
            action = getattr(self, action_name)
            action()
        except Exception as err :
            print("Status: 405 Method Not Allowed\n")
            if self.dev_mode :
                print(err)


    def do_get(self) :
        test_data = {
            "method": "GET",
            "info": "Перелік замовлень",
            "orders": [
                {
                    "id": 1,
                    "customer": "Марія",
                    "total": 1234.56,
                    "status": "new"
                },
                {
                    "id": 2,
                    "customer": "Маша",
                    "total": 789.00,
                    "status": "done"
                }
            ]
        }
        print("Content-Type: application/json; charset=utf-8")
        print()
        print(json.dumps(test_data, ensure_ascii=False))


    def do_post(self) :
        body = json.load(sys.stdin)
        test_data = {
            "method": "POST",
            "info": "Створення нового замовлення",
            "body": body
        }
        print("Content-Type: application/json; charset=utf-8")
        print()
        print(json.dumps(test_data, ensure_ascii=False))


    def do_put(self) :
        body = json.load(sys.stdin)
        test_data = {
            "method": "PUT",
            "info": "Повне оновлення замовлення",
            "body": body
        }
        print("Content-Type: application/json; charset=utf-8")
        print()
        print(json.dumps(test_data, ensure_ascii=False))


    def do_patch(self) :
        body = json.load(sys.stdin)
        test_data = {
            "method": "PATCH",
            "info": "Часткове оновлення замовлення ",
            "body": body
        }
        print("Content-Type: application/json; charset=utf-8")
        print()
        print(json.dumps(test_data, ensure_ascii=False))


    def do_delete(self) :
        test_data = {
            "method": "DELETE",
            "info": "Видалення замовлення ",
            "result": "ok"
        }
        print("Content-Type: application/json; charset=utf-8")
        print()
        print(json.dumps(test_data, ensure_ascii=False))
