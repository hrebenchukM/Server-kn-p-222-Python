import base64
from models.cgi_request import CgiRequest
import json,sys
from data.accessor import DataAccessor


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
            # "ddf": {
            #     0: 1,
            #     1: 2,
            #     2: 3,
            #     3: 4,
            #     4: 5
            # },
            # "dfg": "Mary",
            "headers": self.cgi_request.headers

        }
        # перевіряємо автентифікацію
        auth_header = self.cgi_request.headers.get('Authorization', None)
        if auth_header :
            scheme = 'Basic '
            if not auth_header.startswith(scheme) :
                test_data['auth_message'] = "Invalid 'Authorization' scheme"
            else :
                try : credentials = base64.b64decode(auth_header[len(scheme):].encode()).decode("utf-8")
                except Exception as err : test_data['auth_message'] = str(err)
                else :
                    (login, password) = credentials.split(':')
                    data_accessor = DataAccessor()
                    test_data['auth_message'] = data_accessor.authenticate(login, password)

        else :
            test_data['auth_message'] = "No 'Authorization' header in request"

        sys.stdout.buffer.write(b"Content-Type: application/json; charset=utf-8\n\n")
        sys.stdout.buffer.write(json.JSONEncoder(ensure_ascii=False, default=str).encode(test_data).encode("utf-8"))

    def do_post(self) :
        
        test_data = {
            "cyrr": "Вітання усім!",
            "body": json.load(sys.stdin),
            "headers": self.cgi_request.headers

        }
        print("Content-Type: application/json; charset=utf-8")
        print()
        print(json.dumps(test_data, ensure_ascii=False))


