import socket
import argparse

print(r"""
           ⡴⠚⣉⡙⠲⠦⠤⠤⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣴⠛⠉⠉⠀⣾⣷⣿⡆⠀⠀⠀⠐⠛⠿⢟⡲⢦⡀⠀⠀⠀⠀
⠀⠀⠀⠀⣠⢞⣭⠎⠀⠀⠀⠀⠘⠛⠛⠀⠀⢀⡀⠀⠀⠀⠀⠈⠓⠿⣄⠀⠀⠀
⠀⠀⠀⡜⣱⠋⠀⠀⣠⣤⢄⠀⠀⠀⠀⠀⠀⣿⡟⣆⠀⠀⠀⠀⠀⠀⠻⢷⡄⠀
⠀⢀⣜⠜⠁⠀⠀⠀⢿⣿⣷⣵⠀⠀⠀⠀⠀⠿⠿⠿⠀⠀⣴⣶⣦⡀⠀⠰⣹⡆
⢀⡞⠆⠀⣀⡀⠀⠀⠘⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣶⠇⠀⢠⢻⡇
⢸⠃⠘⣾⣏⡇⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⣠⣤⣤⡉⠁⠀⠀⠈⠫⣧
⡸⡄⠀⠘⠟⠀⠀⠀⠀⠀⠀⣰⣿⣟⢧⠀⠀⠀⠀⠰⡿⣿⣿⢿⠀⠀⣰⣷⢡⢸
⣿⡇⠀⠀⠀⣰⣿⡻⡆⠀⠀⠻⣿⣿⣟⠀⠀⠀⠀⠀⠉⠉⠉⠀⠀⠘⢿⡿⣸⡞
⠹⣽⣤⣤⣤⣹⣿⡿⠇⠀⠀⠀⠀⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡔⣽⠀
⠀⠙⢻⡙⠟⣹⠟⢷⣶⣄⢀⣴⣶⣄⠀⠀⠀⠀⠀⢀⣤⡦⣄⠀⠀⢠⣾⢸⠏⠀
⠀⠀⠘⠀⠀⠀⠀⠀⠈⢷⢼⣿⡿⡽⠀⠀⠀⠀⠀⠸⣿⣿⣾⠀⣼⡿⣣⠟⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢠⡾⣆⠑⠋⠀⢀⣀⠀⠀⠀⠀⠈⠈⢁⣴⢫⡿⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⣧⣄⡄⠴⣿⣶⣿⢀⣤⠶⣞⣋⣩⣵⠏⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢺⣿⢯⣭⣭⣯⣯⣥⡵⠿⠟⠛⠉⠉⠀⠀⠀⠀⠀⠀⠀

  ____      _    _    _
 / ___|___ | | _| | _(_) ___   _ __  _ __ _____  ___   _
| |   / _ \| |/ / |/ / |/ _ \ | '_ \| '__/ _ \ \/ / | | |
| |__| (_) |   <|   <| |  __/ | |_) | | | (_) >  <| |_| |
 \____\___/|_|\_\_|\_\_|\___| | .__/|_|  \___/_/\_\\__, |
                              |_|                  |___/
""")

def build_args():
    parser = argparse.ArgumentParser(
        prog="cokkie proxy",
        description="Cokkie Proxy intercept"
    )
    parser.add_argument(
        "-i", "--intercept",
        action="store_true",
        help="Enable interactive interception mode"
    )
    return parser.parse_args()

def interactive_edit(lines, title):
    print(f"\n--- {title} ---")
    print("Press enter on empty line to finish\n")

    new_lines = []
    for line in lines:
        print(line)

    print("\n--- edit ---")
    while True:
        line = input("> ")
        if line == "":
            break
        new_lines.append(line)

    return new_lines if new_lines else lines

args = build_args()

HOST = "127.0.0.1"
PORT = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(5)

print(f"proxy running on {HOST}:{PORT}")

while True:
    client, addr = server.accept()
    print(f"\nrequest from {addr}")

    request = client.recv(8192)
    if not request:
        client.close()
        continue

    request_text = request.decode("utf-8", errors="ignore")
    headers = request_text.split("\r\n")

    if args.intercept:
        headers = interactive_edit(headers, "original request")
        request_text = "\r\n".join(headers) + "\r\n\r\n"
        request = request_text.encode("utf-8")

    host = None
    for h in headers:
        if h.lower().startswith("host:"):
            host = h.split(":", 1)[1].strip()
            break

    if not host:
        print("host not found")
        client.close()
        continue

    try:
        remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote.connect((socket.gethostbyname(host), 80))
        remote.sendall(request)

        while True:
            data = remote.recv(4096)
            if not data:
                break

            if args.intercept:
                response_text = data.decode("utf-8", errors="ignore")
                resp_lines = response_text.split("\r\n")

                resp_lines = interactive_edit(resp_lines, "response")
                response_text = "\r\n".join(resp_lines) + "\r\n\r\n"
                client.sendall(response_text.encode("utf-8"))
            else:
                client.sendall(data)

    finally:
        remote.close()
        client.close()
