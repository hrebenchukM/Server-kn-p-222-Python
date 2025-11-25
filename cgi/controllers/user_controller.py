from models.cgi_request import CgiRequest
import json,sys

class UserController :

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


    def do_get(self):
        test_data = {
            "x": 10,
            "y": 20,
            "cyrr": "Вітання усім!",
            "ddf": {
                0: 1,
                1: 2,
                2: 3,
                3: 4,
                4: 5
            },
            "dfg": "Mary"
        }
        print("Content-Type: application/json; charset=utf-8")
        print()
        print(json.dumps(test_data, ensure_ascii=False))

    def do_post(self) :
        
        test_data = {
            "cyrr": "Вітання усім!",
            "body": json.load(sys.stdin)
        }
        print("Content-Type: application/json; charset=utf-8")
        print()
        print(json.dumps(test_data, ensure_ascii=False))


