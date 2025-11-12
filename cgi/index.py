#!C:\Users\Lenovo\anaconda3\python.exe
import codecs, os, sys

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
sys.stdin = codecs.getreader("utf-8")(sys.stdin.detach())

# параметри від сервера передаються через змінні оточення,
# які доступні через пакет os

rows = "\n".join(
    f"<tr><td>{k}</td><td>{v}</td></tr>"
    for k, v in sorted(os.environ.items(), key=lambda item: item[0].lower())
)



envs = f"""
<table border="1" cellpadding="6" cellspacing="0">
    <thead>
        <tr>
            <th>Змінна</th>
            <th>Значення</th>
        </tr>
    </thead>
    <tbody>
        {rows}
    </tbody>
</table>
"""

# envs = "<ul>" + "\n".join(f"<li>{k} = {v}</li>" for k,v in os.environ.items()) + "</ul>"

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CGI-222</title>
    <link rel="icon" type="image/png" href="python.png" />
</head>
<body>
    <h1>Інтерфейс спільного шлюзу (CGI)</h1>
    {envs}
</body>
</html>'''



print("Content-Type: text/html; charset=utf-8")
print()  # порожній рядок відділяє заголовки та тіло
print(html)
