import socket
import os
import struct

#Informações das Constantes
port = 7000
bufferSize = 1024
hostname = 'SpotiFail'
diretorio = '/Users/Public/Music/{}/Server'.format(hostname)

#Inicializar o Socket
h = socket.gethostname()
ip = socket.gethostbyname(h)
print('IP do Servidor: {}'.format(ip))
socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socketServer.bind((ip, port))
socketServer.listen(5)

#Criar Diretório para armazenar as músicas
try:
    os.makedirs(diretorio)
except:
    ()

#Funções dos Comandos

def baixar():
    with connection:
        musica = str(connection.recv(bufferSize))
        with open('{}/{}.wav'.format(diretorio, musica[2:-1]), 'rb') as bytes:
            connection.send(struct.pack('i', os.path.getsize('{}/{}.wav'.format(diretorio, musica[2:-1]))))
            data = bytes.read(bufferSize)
            while data:
                connection.send(data)
                data = bytes.read(bufferSize)
    return

def enviar():
    with connection:
        musica = str(connection.recv(bufferSize))
        with open('{}/{}.wav'.format(diretorio, musica[2:-1]), 'wb') as arquivoMusica:
            fileSize = struct.unpack('i', connection.recv(4))[0]
            bytesReceived = 0
            while bytesReceived < fileSize:
                data = connection.recv(bufferSize)
                arquivoMusica.write(data)
                bytesReceived += bufferSize
        arquivoMusica.close()
        response = 'Upload Concluido'
        connection.send(response.encode('utf-8'))
    return

def listarComandos():
    response = str("Lista de Comandos:;" +
                   "enviar: Enviar Uma Musica;" +
                   "baixar: Baixar Uma Musica;" +
                   "tocar: Tocar Uma Musica;" +
                   "listar: Listar as Musicas Disponiveis;" +
                   "?: Listar Comandos Disponiveis;" +
                   "sair: Sair"
                   )
    connection.send(response.encode('utf-8'))
    return

def listarMusicas():
    musicas = str(os.listdir('{}/'.format(diretorio)))
    musicas = musicas[1:-1]
    musicas = musicas.replace(', ', ';')
    musicas = musicas.replace("'", '')
    response = 'Lista de Musicas:;' + musicas
    connection.send(response.encode('utf-8'))
    return

def sair():
    response = 'Obrigado e Volte Sempre!'
    connection.send(response.encode('utf-8'))
    print('Conexão Com o Cliente {} Finalizada'.format(address))
    connection.close()
    return

#Loop Principal do Servidor
while True:
    try:
        print('Aguardando Conexão...')
        connection, address = socketServer.accept()
        print('Conexão Realizada com o Cliente: {}'.format(address))
        confirm = str('Bem Vindo ao {}!;'.format(hostname) + 'Digite "?" para Solicitar a Lista de Comandos Disponiveis.')
        connection.send(confirm.encode('utf-8'))
        while True:
            print('Aguardando Comando...')
            request = str(connection.recv(bufferSize))
            request = request[2:-1]
            print('O Cliente {} Solicitou o Comando: {}'.format(address, request))
            if request == 'baixar' or request == 'tocar':
                baixar()
                connection, address = socketServer.accept()
            elif request == 'enviar':
                enviar()
                connection, address = socketServer.accept()
            elif request == '?':
                listarComandos()
            elif request == 'listar':
                listarMusicas()
            elif request == 'sair':
                sair()
                break
            request = None
    except:
            print('Conexão Com o Cliente {} Finalizada'.format(address))