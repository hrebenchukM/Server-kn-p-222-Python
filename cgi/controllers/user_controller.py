from controllers.controller_rest import RestController, RestStatus
import json, sys, base64
from data.accessor import DataAccessor



class UserController(RestController):

    def __init__(self, cqi_request, dev_mode = False):
        super().__init__(cqi_request, dev_mode)
        self.rest_response.meta.serviceName += "User"

    def do_get(self):
        auth_header = self.cgi_request.headers.get('Authorization', None)
        
        if auth_header:
            scheme = 'Basic '
            if not auth_header.startswith(scheme):
                self.rest_response.status = RestStatus.status401
                return "Invalid 'Authorization' scheme (Expected 'Basic')"
            else:
                try: 
                    encoded_creds = auth_header[len(scheme):]
                    credentials = base64.b64decode(encoded_creds.encode()).decode("utf-8")
                except Exception as err: 
                    self.rest_response.status = RestStatus.status401
                    return str(err)
                
                try:
                    (login, password) = credentials.split(':')
                except ValueError:
                    self.rest_response.status = RestStatus.status401
                    return "Invalid credential format"

                data_accessor = DataAccessor()
                token = data_accessor.authenticate(login, password) 
                
                if token is None:
                    self.rest_response.status = RestStatus.status401
                    return "Invalid login or password"
                else:
                    return token
        else:
            self.rest_response.status = RestStatus.status401
            return "No 'Authorization' header in request"

    def do_post(self):
        test_data = {
            "cyrr": "Привет мир",
            "body": json.load(sys.stdin),
            "headers": self.cgi_request.headers,
        }
        return test_data