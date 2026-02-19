from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import unquote_plus
import socket
from http.server import BaseHTTPRequestHandler

white_mime = {
    ".html": "text/html",
    ".htm": "text/html",
    ".css": "text/css",
    ".js": "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon",
    ".txt": "text/plain",
    ".pdf": "application/pdf",
    ".zip": "application/zip",
    ".rar": "application/x-rar-compressed",
    ".mp3": "audio/mpeg",
    ".mp4": "video/mp4",
    ".avi": "video/x-msvideo",
    ".mpeg": "video/mpeg",
    ".webm": "video/webm",
    ".ogg": "audio/ogg",
    ".wav": "audio/wav",
    ".flac": "audio/flac",
    ".woff": "font/woff",
    ".woff2": "font/woff2",
}


class AccessManagerRequestHandler(BaseHTTPRequestHandler):
    """
    BaseHTTPRequestHandler не має окремої централізованої
    точки доступу, через яку проходять усі запити.

    Перевизначення handle_one_request() дозволяє
    реалізувати власну логіку перевірки доступу,
    логування або фільтрації перед викликом
    відповідного HTTP-методу (do_GET, do_POST тощо).
    """

    def handle_one_request(self):
        #original: githab
        try:
            # Читаємо перший рядок HTTP-запиту
            self.raw_requestline = self.rfile.readline(65537)

            # Перевірка занадто довгого запиту
            if len(self.raw_requestline) > 65536:
                self.requestline = ''
                self.request_version = ''
                self.command = ''
                self.send_error(414)
                return

            # Якщо запит порожній — закриваємо з'єднання
            if not self.raw_requestline:
                self.close_connection = 1
                return

            # Парсимо запит
            if not self.parse_request():
                # Помилка вже відправлена
                return

            # Формуємо назву методу (do_GET, do_POST і т.д.)
            mname = 'access_manager' 

            # Якщо метод не реалізований
            if not hasattr(self, mname):
                        self.send_error(501, "Method not implemented: (%r)" % mname)
                        return

            # Викликаємо відповідний метод
            method = getattr(self, mname)
            method()

            # Примусово відправляємо відповідь
            self.wfile.flush()

        except socket.timeout as e:
            # Якщо тайм-аут читання або запису
            self.log_error("Request timed out: %r", e)
            self.close_connection = 1
            return
        
    def access_manager(self):
        mname = 'do_' + self.command
        if not hasattr(self, mname):
            self.send_error(501, "Unsupported method (%r)" % self.command)
            return
        method = getattr(self, mname)
        method()

class MainHandler(AccessManagerRequestHandler):
    def access_manager(self):
        """ НД ТЗІ 1.1-002-99:
        Головна мета диспетчера доступу — забезпечення відомої точки
        проходження всіх запитів всередині КС і досягнення гарантії того,
        що потоки інформації між об'єктами-користувачами, об'єктами-процесами
        і пасивними об'єктами відповідають вимогам політики безпеки.
        """
        # перевірити чи не є self.path існуючим файлом
        # якщо запит — не каталог, пробуємо віддати файл
        if not self.path.endswith('/') and not '../' in self.path:
            try:
                dot_index = self.path.rindex('.')
                ext = self.path[dot_index:]
                mime_type = white_mime[ext]

                fname = "./http/assets" + self.path

                with open(fname, "rb") as file:
                    self.send_response(200, "OK")
                    self.send_header("Content-Type", mime_type)
                    self.end_headers()
                    self.wfile.write(file.read())
                    return

            except Exception as err:
                print(err)

        return super().access_manager()

    def do_GET(self):

        # -------- Розділяємо шлях і query --------
        parts = self.path.split('?', 1)
        path = parts[0]
        query_string = parts[1] if len(parts) > 1 else None

        base_path = path

        # -------- Controller / Action / ID --------
        parts = path.split('/', 3)
        controller = parts[1].lower() if len(parts) > 1 and len(parts[1]) > 0 else None
        action = parts[2].lower() if len(parts) > 2 and len(parts[2]) > 0 else None
        id = parts[3] if len(parts) > 3 and len(parts[3]) > 0 else None

        # -------- Service / Service Param --------
        parts2 = path.split('/', 2)
        service = parts2[1].lower() if len(parts2) > 1 and len(parts2[1]) > 0 else None
        service_param = parts2[2] if len(parts2) > 2 and len(parts2[2]) > 0 else None

        # -------- Query Params --------
        query_params = {}

        if query_string is not None:
            for key, value in (
                map(lambda x: None if x is None else unquote_plus(x),
                    item.split('=', 1) if '=' in item else [item, None])
                for item in query_string.split('&') if len(item) > 0
            ):
                query_params[key] = value if key not in query_params else [
                    *(
                        query_params[key] if isinstance(query_params[key], (list, tuple))
                        else [query_params[key]]
                    ),
                    value
                ]

        # -------- Response --------
        self.send_response(200, "OK")
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

        rows = [
            ("Full Path", self.path),
            ("Base Path", base_path),
            ("Controller", controller),
            ("Action", action),
            ("ID", id),
            ("Query String", query_string),
            ("Query Params", query_params),
            ("Service", service),
            ("Service Param", service_param),
        ]

        table_rows = ""
        for name, value in rows:
            table_rows += f"""
            <tr>
                <td>{name}</td>
                <td>{value}</td>
            </tr>
            """

        html = f"""
        <html>
        <head>
            <link rel="icon" href="Python.png" type="image/png">
            <meta charset="utf-8">
            <title>HTTP Server</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 30px;
                }}

                table {{
                    border-collapse: collapse;
                    width: 60%;
                    margin-top: 15px;
                }}

                th, td {{
                    border: 1px solid #ccc;
                    padding: 8px;
                }}

                th {{
                    background-color: #f4f4f4;
                }}

                .links {{
                    margin-bottom: 20px;
                }}

                .links a {{
                    display: inline-block;
                    padding: 8px 14px;
                    margin-right: 10px;
                    margin-bottom: 8px;
                    text-decoration: none;
                    border: 1px solid #4a90e2;
                    border-radius: 6px;
                    color: #4a90e2;
                    background-color: #f0f7ff;
                    font-size: 14px;
                }}

                .links a:hover {{
                    background-color: #4a90e2;
                    color: white;
                }}

                button {{
                    margin-top: 20px;
                    padding: 8px 14px;
                    border-radius: 6px;
                    border: 1px solid #444;
                    cursor: pointer;
                }}
            </style>
           
        </head>
        <body>

            <h1>HTTP</h1>

            <div class="links">
                <a href="/">Без параметрів</a>

                <a href="/?x=10&x=20">
                    Масив параметрів (x=10, x=20)
                </a>

                <a href="/?q=it+step%20%D0%B0%D0%BA%D0%B0%D0%B4%D0%B5%D0%BC%D1%96%D1%8F">
                    URL-кодовані параметри
                </a>
            </div>

            <table>
                <tr>
                    <th>Назва</th>
                    <th>Значення</th>
                </tr>
                {table_rows}
            </table>

            <hr/>

            <button onclick="sendLink()">Send LINK Request</button>
            <p id="out"></p>

            <script>
                function sendLink() {{
                    fetch('/', {{
                        method: 'LINK'
                    }})
                    .then(r => r.text())
                    .then(t => document.getElementById('out').innerText = t);
                }}
            </script>

        </body>
        </html>
        """



        self.wfile.write(html.encode())


    # -------- Обробка методу LINK --------
    def do_LINK(self):
        self.send_response(200, "OK")
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write("LINK response text".encode())


def main():
    port = 88
    http_server = HTTPServer(('127.0.0.1', port), MainHandler)
    try:
        print(f"Server starting on port {port}...")
        print(f"http://localhost:{port}")
        http_server.serve_forever()
    except:
        print("Server stopped")


if __name__ == "__main__":
    main()
