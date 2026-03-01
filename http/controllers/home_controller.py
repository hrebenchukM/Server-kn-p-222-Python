from http.server import BaseHTTPRequestHandler
import json
import os

class HomeController :
    def __init__(self, handler:BaseHTTPRequestHandler):
        self.handler = handler


    def do_GET(self):
        fname = "./http/assets/home.html"
        with open(fname, "r", encoding="utf-8") as file:
            html_content = file.read()

            rest_file = "./http/assets/rest_structures.txt"
            rest_content = ""
            if os.path.exists(rest_file):
                with open(rest_file, "r", encoding="utf-8") as file:
                    rest_content = file.read()
                
        html_content = (html_content
            .replace("{self.handler.path}",          str(self.handler.path))    
            .replace("{self.handler.service_param}", str(self.handler.service_param))    
            .replace("{self.handler.service}",       str(self.handler.service))    
            .replace("{self.handler.query_params}",  str(self.handler.query_params))    
            .replace("{self.handler.query_string}",  str(self.handler.query_string)) 
            .replace("{rest_structures}", rest_content)   
        )
        # TODO: створити метод для успішного надсилання даних (HTML / JSON)
        self.handler.send_response(200, "OK")
        self.handler.send_header("Content-Type", "text/html; charset=utf-8")
        self.handler.end_headers()
        self.handler.wfile.write(html_content.encode())

'''
Реалізувати відображення на головній сторінці структур REST
 для об'єктів та масивів (як варіант: включити ТХТ файли до складу сторінки)
'''