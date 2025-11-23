from models.cgi_request import CgiRequest

class HomeController :

    def __init__(self, cgi_request:CgiRequest,dev_mode:bool=False):
        self.cgi_request = cgi_request
        self.dev_mode = dev_mode


    def service(self) :
        action_name = (self.cgi_request.path_parts[1].lower()             
            if len(self.cgi_request.path_parts) > 1 
                and len(self.cgi_request.path_parts[1]) > 0 
            else 'index')
        try :
            action = getattr(self, action_name)
            action()
        except Exception as err :
            print("Status: 404 Not Found\n")
            if self.dev_mode :
                print(err)
   
        
    def privacy(self) :
        html = self._layout().replace(
            "RenderBody", '''
            <h1>Політика конфіденційності</h1>
            '''
        )
        print("Content-Type: text/html; charset=utf-8")
        print()
        print(html)


    def _layout(self) :
        return '''<!DOCTYPE html>
            <html lang="en">
            <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width-width, initial-scale=1.0">
                    <title>CGI-2222</title>
                    <link rel="icon" href="/img/Python.png" />
                    <link rel="stylesheet" href="/css/site.css" />
            </head>
            <body>
                   RenderBody
                    <script src="/js/site.js"></script>
            </body>
            </html>'''



    def index(self) :
        envs = "<ul>" + "".join(f"<li>{k} = {v}</li>" for k,v in self.cgi_request.server.items() ) + "</ul>"
        qp   = "<ul>" + "".join(f"<li>{k} = {v}</li>" for k,v in self.cgi_request.query.items()  ) + "</ul>"
        hdrs = "<ul>" + "".join(f"<li>{k} = {v}</li>" for k,v in self.cgi_request.headers.items()) + "</ul>"

        html = self._layout().replace(
        "RenderBody", f'''
        <h1>Інтерфейс спільного шлюзу (CGI)</h1>
        <a href = "/home/privacy">Політика конфеденційності</a>

        <h2>ENV</h2>
        {envs}

        <h2>QUERY</h2>
        {qp}

        <h2>HEADERS</h2>
        {hdrs}

        <img src="/img/m13.jpg" />
        <hr>

        <h2>Зміст</h2>
        <ul>
            <li><a href="/home/params">Параметри CGI (ENV, QUERY, HEADERS)</a></li>
            <li><a href="/home/privacy">Політика конфіденційності</a></li>

            
            <li><a href="/wantsleep/index">Неправильний контролер</a></li>
            <li><a href="/home/wantsleep">Неправильний метод</a></li>
        </ul>

        <script src="/js/site.js"></script>
        '''
    )

        

        print("Content-Type: text/html; charset=utf-8")
        print()  
        print(html)

    def params(self):

        def table(d: dict):
            rows = "".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k,v in d.items())
            return f"<table border='1' cellpadding='4'>{rows}</table>"

        envs = table(self.cgi_request.server)
        qp   = table(self.cgi_request.query)
        hdrs = table(self.cgi_request.headers)

        html = self._layout().replace(
            "RenderBody", f'''
            <h1>Параметри CGI</h1>

            <h2>Змінні оточення (ENV)</h2>
            {envs}

            <h2>Параметри запиту (QUERY)</h2>
            {qp}

            <h2>Заголовки (HEADERS)</h2>
            {hdrs}

            <a href="/home/index">⬅ назад</a>
            '''
        )

        print("Content-Type: text/html; charset=utf-8")
        print()
        print(html)



