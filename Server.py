import socket, threading, os

#conns = set() # armazenar conxoes aqui
conns = [] # armazenar conxoes aqui
host, port = ('localhost', 9999)




def opc():
    print('[xd] Sair do server')
    print('[li] Listar conexões')
    print('[sd] Enviar mensagem')


def li():
    i=0
    if len(conns)>0:
        for c in conns:  # enviar mensagem para todos os outros clientes
            i+=1
            print('CONN:{}, USER:{}, ADDR:{}'.format(i, c[1], c[2] ))
    else:
        print('Nenhum cliente conctado...')

def menu(n):
    opc()
    o = input()
    while o!='xd':
        if o=='li':
            li()
            print('')
        if o=='sd':
            send()
            print('')

        opc()
        o = input()

    print('Finalizando serviços no servidor...')
    os._exit(0)

m = threading.Thread(target=menu, args=["o"])
m.start()

def send():
    li()
    print('Número da conexão')
    i = input()
    j = int(i)-1

    for index, item in enumerate(conns):
        if index==j:
            print('Cliente slecionado [{}], Digite a sua mensagem'.format(item[1]))
            msg = 'Server diz: ' + input()
            item[0].send(msg.encode())
        else:
            print('Conexão não encontrada')


def run(conn):
    while True:
        try:
            data = conn.recv(1024) # receber informacao
            if not data or 'x1' in data.decode(): # se o cliente tiver desligado
                for c in conns:
                    if c[0]==conn:
                        conns.remove(c)
                break
            for c in conns: # enviar mensagem para todos os outros clientes
                if c[0] is not conn: # excepto para o que a enviou
                    c[0].send('{}'.format(data.decode()).encode('utf-8'))
                    #c.send('{}: {}'.format(conn.getpeername(), data.decode()).encode('utf-8'))
        except ConnectionAbortedError:
            print('')
            #conns.remove(conn)
        except ConnectionResetError:
            print('')
            #conns.remove(conn)

with socket.socket() as sock: # ligacao TCP
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # reutilizar endereco logo a seguir a fechar o servidor
    sock.bind((host, port))
    sock.listen(5) # servidor ativo
    print('Server iniciado em..: {}:{}\n'.format(host, port))
    while True:
        conn, addr = sock.accept() # esperar que alguem se conect
        user = conn.recv(1024)  # receber informacao
        conn.send('Ola {}, você esta conectado em...: {}\n'.format(user,addr).encode())
        conn.send('Digite suas mensagens, elas serão visiveis a todos os usuários...\n'.encode())
        conns.append([conn, user.decode('utf-8'), addr]) # adicionar conexao ao nosso set de coneccoes
        threading.Thread(target=run, args=(conn,)).start() # esta coneccao vai ser independente das outra a partir de agora, vamos correr a thread na funcao run