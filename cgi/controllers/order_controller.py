from controllers.controller_rest import RestController, RestStatus, RestAuth
import json, sys, time
from data.helper import authorize_request


class OrderController(RestController):

    def __init__(self, cgi_request, dev_mode=False):
        super().__init__(cgi_request, dev_mode)
        self.rest_response.meta.serviceName += "Order"


    def do_get(self):
        try:
            payload = authorize_request(self.cgi_request)

            # часові поля JWT
            iat = payload.get("iat", None)
            exp = payload.get("exp", None)
            nbf = payload.get("nbf", None)

            # якщо немає жодного часового поля — токен невалідний
            if not any((iat, exp, nbf)):
                raise ValueError("Invalid token: missing time fields")

            now = time.time()

            # 1️⃣ nbf
            if nbf and nbf > now:
                raise ValueError("nbf")

            # 2️⃣ exp
            if exp and exp < now:
                raise ValueError("exp")

            # 3️⃣ iat (якщо нема nbf і exp)
            if not nbf and not exp and iat > now:
                raise ValueError("iat")

        except ValueError as err:
            self.rest_response.status = RestStatus.status401
            self.rest_response.meta.auth = RestAuth(False, str(err))
            return "Unauthorized"

        else:
            self.rest_response.meta.auth = RestAuth(True, payload.get("sub"))

        return {
            "method": "GET",
            "info": "Перелік замовлень",
            "orders": [
                {"id": 1, "customer": "Марія", "total": 1234.56, "status": "new"},
                {"id": 2, "customer": "Маша", "total": 789.00, "status": "done"}
            ]
        }


    def do_post(self):
        try:
            payload = authorize_request(self.cgi_request)
            self.rest_response.meta.auth = RestAuth(True, payload.get("sub"))
        except ValueError as err:
            self.rest_response.status = RestStatus.status401
            self.rest_response.meta.auth = RestAuth(False, str(err))
            return "Unauthorized"

        return {
            "method": "POST",
            "info": "Створення нового замовлення",
            "body": json.load(sys.stdin)
        }
