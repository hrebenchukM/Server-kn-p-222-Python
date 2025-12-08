from controllers.controller_rest import RestController, RestStatus
import json, sys


class OrderController(RestController):

    def __init__(self, cgi_request, dev_mode=False):
        super().__init__(cgi_request, dev_mode)
        self.rest_response.meta.serviceName += "Order"


    def do_get(self):
        auth_header = self.cgi_request.headers.get("Authorization", None)

        if auth_header:
            scheme = "Bearer "
            if not auth_header.startswith(scheme):
                self.rest_response.status = RestStatus.status401
                return "Invalid 'Authorization' scheme (Expected 'Bearer')"
            else:

                token = auth_header[len(scheme):]

                if len(token) == 0:
                    self.rest_response.status = RestStatus.status401
                    return "Empty Bearer token"

                return {
                    "method": "GET",
                    "info": "Перелік замовлень",
                    "token": token,
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

        else:
            self.rest_response.status = RestStatus.status401
            return "No 'Authorization' header in request"



    def do_post(self):
        body = json.load(sys.stdin)

        test_data = {
            "method": "POST",
            "info": "Створення нового замовлення",
            "body": body,
            "headers": self.cgi_request.headers
        }

        return test_data
