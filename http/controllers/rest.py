from http.server import BaseHTTPRequestHandler

from urllib.parse import unquote_plus

class RestStatus :
    def __init__(self, is_ok:bool=True, code:int=200, phrase:str="OK"):
        self.is_ok  = is_ok
        self.code   = code
        self.phrase = phrase

    def __json__(self) :
        return {
            "isOk": self.is_ok,
            "code": self.code,
            "phrase": self.phrase,
        }
RestStatus.ok_200 = RestStatus(
    is_ok=True,
    code=200,
    phrase="OK"
)

RestStatus.created_201 = RestStatus(
    is_ok=True,
    code=201,
    phrase="Created"
)

RestStatus.no_content_204 = RestStatus(
    is_ok=True,
    code=204,
    phrase="No Content"
)

RestStatus.bad_request_400 = RestStatus(
    is_ok=False,
    code=400,
    phrase="Bad Request"
)

RestStatus.unauthorized_401 = RestStatus(
    is_ok=False,
    code=401,
    phrase="Unauthorized"
)

RestStatus.forbidden_403 = RestStatus(
    is_ok=False,
    code=403,
    phrase="Forbidden"
)

RestStatus.not_found_404 = RestStatus(
    is_ok=False,
    code=404,
    phrase="Not Found"
)

RestStatus.method_not_allowed_405 = RestStatus(
    is_ok=False,
    code=405,
    phrase="Method Not Allowed"
)

RestStatus.conflict_409 = RestStatus(
    is_ok=False,
    code=409,
    phrase="Conflict"
)

RestStatus.internal_500 = RestStatus(
    is_ok=False,
    code=500,
    phrase="Internal Server Error"
)

RestStatus.not_implemented_501 = RestStatus(
    is_ok=False,
    code=501,
    phrase="Not Implemented"
)

RestStatus.bad_gateway_502 = RestStatus(
    is_ok=False,
    code=502,
    phrase="Bad Gateway"
)

RestStatus.service_unavailable_503 = RestStatus(
    is_ok=False,
    code=503,
    phrase="Service Unavailable"
)
'''
Створити статичні поля RestStatus під стандартні коди HTTP статусів (з описами)
'''


class RestError(Exception): 
    
    def __init__(self, code:int=500, phrase:str="Internal Error", data:any=None, status:RestStatus|None=None): 
        self.code   = code 
        self.phrase = phrase 
        self.data   = data 
        self.status = status 
  
    def __str__(self): 
        return "RestError(%d, '%s', %r)" % (self.code, self.phrase, self.data)
    
    def __json__(self):
        return { "code": self.code, "phrase": self.phrase, "data": self.data }
    
    def __iter__(self):
        for k,v in self.__json__().items() :
            yield k,v 
  



class RestResponse :
    def __init__(self, status:RestStatus|None=None, data:any=None):
        self.status = status if status != None else RestStatus()
        self.meta = {}
        self.data = data

    def __json__(self) :
        return {
            "status": self.status,
            "meta": self.meta,
            "data": self.data,
        }



class ControllerRest :

    def __init__(self, handler:BaseHTTPRequestHandler):
        self.handler = handler
        query_params = {}
        if handler.query_string != None:
            for key, value in (map(lambda x : None if x is None else unquote_plus(x) , 
                                   item.split('=', 1) if '=' in item else [item, None] )
                for item in handler.query_string.split('&') if len(item) > 0) :
                    query_params[key] = value if not key in query_params else [
                        *(  query_params[key] if isinstance(query_params[key], (list,tuple)) 
                            else [query_params[key]] ), 
                        value
                    ]
        self.query_params = query_params
        self.rest_response = RestResponse()


    def serve(self):
        mname = 'do_' + self.handler.command
        if not hasattr(self, mname):
            self.rest_response.status = RestStatus(
                is_ok  = False,     
                code   = 405,      
                phrase = "Unsupported method (%r) for controller (%r)" % 
                            (self.handler.command, self.handler.service)
            )
        else :
            try :    
                method = getattr(self, mname)
                method()
                self.on_success()
                return
            except RestError as err :
                self.rest_response.status = RestStatus(
                    is_ok  = False,     
                    code   = err.code,
                    phrase = err.phrase
                )
                self.rest_response.data = err.data
            except Exception as err :
                self.rest_response.status = RestStatus(
                    is_ok  = False,     
                    code   = 500,      
                    phrase = "Internal Error " + str(err)
                )
        self.on_error()

                
    def on_success(self) :
        self.handler.send_rest(self.rest_response)


    def on_error(self) :
        self.handler.send_rest(self.rest_response)