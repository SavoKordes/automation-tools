import socket


while True:
    host = input("Enter name of host (or 'done'): ")
    if host.lower() == "done":
        break
    try:
        port = int(input("Enter port number: "))
        timeout = int(input("Enter timeout value: "))
#socket is created
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((host, port))
        print(f"Connection to {host}:{port} successful")
        s.close()

    except ValueError:
        print("Port and timeout must be numbers")
    except socket.error:
        print(f"Connection to {host}:{port} failed")