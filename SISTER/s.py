import threading
import socket

#menentukan host, port
host = '192.168.56.1'
port = 8080
# Inisialisasi server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#membuat socket
server.bind((host, port))
#mendengarkan koneksi masuk
server.listen()

#membuat list client dan panggilan
clients = []
aliases = []

global password


def broadcast(message):
    #mengirim pesan ke semua client
    for client in clients:
        client.send(message)

def handle_client(client):
    #menghandle pesan masuk dari client
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)
            parting = message.split(':')
            if parting[1].strip() == "Password ditemukan":
                broadcast("stop".encode('utf-8'))
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left!\n'.encode('utf-8'))
            aliases.remove(alias)
            break


def bagi(clients):
    #membagi tugas para client

    # Jumlah total clients
    total_clients = len(clients)

    # Rentang karakter dari AAA hingga ZZZ
    start_range = 'AAA'
    end_range = 'ZZZ'

    # Menghitung jumlah kombinasi karakter
    total_combinations = (ord(end_range[0]) - ord(start_range[0]) + 1) * 26 * 26

    # Jumlah kombinasi karakter per client
    combinations_per_client = total_combinations // total_clients

    # Loop untuk setiap client
    for i, client in enumerate(clients):
        # Menghitung kombinasi karakter awal dan akhir untuk client saat ini
        start_combination = i * combinations_per_client
        end_combination = (i + 1) * combinations_per_client - 1

        # Mengonversi kombinasi karakter menjadi string
        start_str = ''
        end_str = ''

        for j in range(2, -1, -1):
            start_str += chr(ord('A') + start_combination // (26 ** j))
            start_combination %= (26 ** j)

            end_str += chr(ord('A') + end_combination // (26 ** j))
            end_combination %= (26 ** j)

        # untuk memastikan sampai ZZZ 'ZZZ'
        if end_str == 'ZZY':
            end_str = 'ZZZ'
        elif end_str == 'ZZX':
            end_str = 'ZZZ'

        # Mengirim awalan dan akhiran ke client
        message = f"{start_str},{end_str},{password}"
        client.send(message.encode('utf-8'))

def receive():
    #main function

    while True:
        print('Server is running and listening ...')
        #menerima koneksi dari client
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
        #meminta nama panggilan client
        client.send('alias?'.encode('utf-8'))
        #membaca nama panggilan client dan dimasukan kedalam list
        alias = client.recv(1024).decode('utf-8')
        aliases.append(alias)
        clients.append(client)
        print(f'The alias of this client is {alias}')
        print(f'{alias} has connected to')
        #mengirim pemberitahuan kepada client karena sudah terhubung dengan server
        client.send('you are now connected!'.encode('utf-8'))
        #membuat dan memulai thread baru untuk menangani koneksi dari klien
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()
        #menampilkan berapa client yang terhubung
        print(f'jumlah client yang terhubung: {len(clients)}')
        #meminta konfirmasi untuk membroadcast job untuk client memulai bruteforce
        user_input = input("Broadcast to all clients? (y/n): ")
        if user_input.lower() == "y":
            bagi(clients)
            break




if __name__ == "__main__":
    password = input("input pass: ")
    receive()