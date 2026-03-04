from controllers.controller_rest import ControllerRest, RestError

class UserController(ControllerRest) :

    def do_GET(self) :
        self.rest_response["data"] = {
            "Full Path": self.handler.path.split('?',1)[0],
            "Controller": "UserController",
            "Query String": self.handler.query_string,
            "Query Params": self.handler.query_params,
            "Service": self.handler.service,
            "Service Param": self.handler.service_param
        }

    def do_LINK(self) :
        raise RestError(
            code=400,
            phrase="LINK raised error",
            data={"LINK": "Помилка!"}
        )