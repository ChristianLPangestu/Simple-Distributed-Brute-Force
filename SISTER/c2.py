import threading
import socket

#menentukan nama panggilan client
alias = "client2"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#menghubungkan ke server
client.connect(('192.168.56.1', 8080))


def client_receive():
    #untuk memproses pesan yang diterima
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "alias?":
                client.send(alias.encode('utf-8'))
            elif message == "stop":
                print("berhenti mencari")
                break
            elif message == "you are now connected!":
                print(message)
            else:
                print(message)
                parts = message.split(',')
                part0 = parts[0].strip()
                part1 = parts[1].strip()
                part2 = parts[2].strip()
                brute_force(part0,part1,part2)
        except:
            print('Quit')
            client.close()
            break


def brute_force(start, end, target_password):
    #fungsi bruteforce dimana mencoba kombinasi dari start hingga end untuk menebak target password
    def increment_combination(combination):
        chars = list(combination)
        index = len(chars) - 1

        while chars[index] <= 'Z':
            chars[index] = chr(ord(chars[index]) + 1)

            if chars[index] > 'Z':
                chars[index] = 'A'
                index -= 1
            else:
                break

        return ''.join(chars)

    current_combination = start
    password_found = False

    while current_combination <= end:
        #perulangan untuk mencoba kombinasi
        print(f"Trying combination: {current_combination}")
        #mengecek apakah kombinasi sama dengan password yang dicari
        if current_combination == target_password:
            password_found = True
            print(f'password ditemukan : {target_password}')
            send_thread = threading.Thread(target=client_send)
            send_thread.start()
            #mengirim pesan ke server bahwa password telah ditemukan
            client.send(f"{alias} : Password ditemukan : {current_combination}".encode('utf-8'))
            break
        if current_combination == end:
            break
        current_combination = increment_combination(current_combination)
    if not password_found:
        client.send(f"{alias} : Password tidak ditemukan".encode('utf-8'))
    return None

def client_send():
    #untuk mengirim pesan
    while True:
        message = f'{alias}: {input("")}'
        client.send(message.encode('utf-8'))

#membuat thread untuk menerima pesan dari client
receive_thread = threading.Thread(target=client_receive)
receive_thread.start()


#membuat thread untuk mengirim pesan ke client
send_thread = threading.Thread(target=client_send)
send_thread.start()