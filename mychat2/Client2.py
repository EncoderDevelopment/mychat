import socket as sockerl, sys, select, platform
from socket import *
from threading import Thread

serverHost = 'localhost'
serverPort = 9999

def menu():
    print('[x1] Para sair')
    print('[mn] Ver menu')
    print('[soma][SOMA] Teste de soma no server')
    print('[subtrai][SUBTRAI] Teste de subtração no server')
    print('')

def linux(s, nome):
    s.connect((serverHost, serverPort))
    s.send(nome.encode('utf-8'))
    while True:
        io_list = [sys.stdin, s]
        ready_to_read, ready_to_write, in_error = select.select(io_list, [], [])
        for io in ready_to_read:
            if io is s:  # se tivermos recebido mensagem
                resp = s.recv(1024)
                if not resp:
                    print('Servidor fechado...')
                    sys.exit()
                print('{}'.format(resp.decode()))
            else:
                #msg = input()
                # msg = nome+': ' + sys.stdin.readline() # vamos enviar mensagem
                msg = nome + ': ' + input()  # vamos enviar mensagem
                if msg == 'mn':
                    menu()
                else:
                    s.send(msg.encode())
                    sys.stdout.flush()


def recebew(socket_):
    while True:
        try:
            msg = socket_.recv(1024)
            if not(len(msg)):
                break
            print(msg.decode("utf-8"))
        except ConnectionAbortedError:
            sys.exit(0)
        except ConnectionResetError:
            sys.exit(0)

    print("Conexão com o servidor encerrada")


def enviaw(socket_,nome):
    menu()
    while True:
        try:
            #msg = nome + ': ' + input()
            msg = input()
            if msg=='mn':
                menu()
            else:
                socket_.sendall(msg.encode("utf-8"))

            if msg == 'x1':
                socket_.close()
                sys.exit(0)
        except Exception:
            print("Finalizando aplicação")
            sys.exit(0)



def windows(nome):
    w = socket(AF_INET, SOCK_STREAM)
    w.connect((serverHost, serverPort))
    w.send(nome.encode('utf-8'))
    envia = Thread(target=enviaw, args=(w,nome,))
    recebe = Thread(target=recebew, args=(w,))

    envia.start()
    recebe.start()

with sockerl.socket() as s:
    print('Informe um nome para conexão')
    nome = input()
    while nome == '':
        print('Informe um nome para conexão')
        nome = input()

    if 'Windows' in platform.system():
        windows(nome)
    else:
        linux(s, nome)
