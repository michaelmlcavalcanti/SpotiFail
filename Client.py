#enconding: utf-8
import socket
import playsound
import struct
import os
import time

#Informações das Constantes
hostname = 'SpotiFail'
port = 7000
bufferSize = 1024
diretorio = '/Users/Public/Music/{}/Downloads'.format(hostname)
diretorio2 = '/Users/Public/Music/{}/Uploads'.format(hostname)
diretorio3 = '/Users/Public/Music/{}/Temp'.format(hostname)

# Inicializando o Socket
ipServer = input('Digite o IP do Servidor: ')
socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Conectando com o servidor
while True:
    try:
        socketClient.connect((ipServer, port))
        confirm = str(socketClient.recv(bufferSize))
        confirm = confirm[2:-1].split(';')
        for conf in confirm:
            print(conf)
        break
    except:
        print('Não foi possível se conectar ao servidor. Verifique se o servidor está online')
        ipServer = input('Digite o IP do Servidor: ')


# Criar Diretórios para armazenar as músicas
try:
    os.makedirs(diretorio)
except OSError:
    ()
try:
    os.makedirs(diretorio2)
except OSError:
    ()
try:
    os.makedirs(diretorio3)
except OSError:
    ()

# Funções dos Comandos

def enviar (musica):
    with socketClient:
        with open('{}/{}'.format(diretorio2, '{}.wav'.format(musica)), 'rb') as bytes:
            socketClient.send(musica.encode('utf-8'))
            socketClient.send(struct.pack('i', os.path.getsize('{}/{}'.format(diretorio2, '{}.wav'.format(musica)))))
            data = bytes.read(bufferSize)
            while data:
                socketClient.send(data)
                data = bytes.read(bufferSize)
        response = str(socketClient.recv(bufferSize))
    print(response[2:-1])
    return

def baixar(musica):
    with socketClient:
        with open('{}/{}'.format(diretorio, '{}.wav'.format(musica)), 'wb') as arquivoMusica:
            socketClient.send(musica.encode('utf-8'))
            fileSize = struct.unpack('i', socketClient.recv(4))[0]
            bytesReceived = 0
            while bytesReceived < fileSize:
                data = socketClient.recv(bufferSize)
                arquivoMusica.write(data)
                bytesReceived += bufferSize
    arquivoMusica.close()
    print('Download Concluído')

def tocar(musica):
    with socketClient:
        with open('{}/{}'.format(diretorio3, '{}.wav'.format(musica)), 'wb') as arquivoMusica:
            socketClient.send(musica.encode('utf-8'))
            fileSize = struct.unpack('i', socketClient.recv(4))[0]
            bytesReceived = 0
            while bytesReceived < fileSize:
                data = socketClient.recv(bufferSize)
                arquivoMusica.write(data)
                bytesReceived += bufferSize
    arquivoMusica.close()
    print('Musica Tocando...')
    playsound.playsound('{}/{}'.format(diretorio3, '{}.wav'.format(musica)))
    return

def listar():
    socketClient.send(request.encode('utf-8'))
    respost = str(socketClient.recv(bufferSize))
    respost = respost[2:-1].split(';')
    for resp in respost:
        print(resp)
    return

def listarMusicasUpload():
    listaMusicas = str(os.listdir('{}/'.format(diretorio2)))
    listaMusicas = listaMusicas[1:-1]
    listaMusicas = listaMusicas.replace("'", '')
    listaMusicas = listaMusicas.split(', ')
    print('Lista de Musicas Disponiveis Para Enviar:')
    for mus in listaMusicas:
        print(mus)

def limparMusicasTemporarias():
    listaMusicas = str(os.listdir('{}/'.format(diretorio3)))
    listaMusicas = listaMusicas[1:-1]
    listaMusicas = listaMusicas.replace("'", '')
    listaMusicas = listaMusicas.split(', ')
    for mus in listaMusicas:
        os.remove('{}/{}'.format(diretorio3,mus))

def sair():
    socketClient.send(request.encode('utf-8'))
    confirm = str(socketClient.recv(bufferSize))
    print(confirm[2:-1])
    socketClient.close()
    return

#Loop principal onde ficam as solicitações do cliente
while True:
    request = input('{}: '.format(hostname))
    if request == 'enviar':
        listarMusicasUpload()
        musica = input('Musica: ')
        if (os.path.exists('{}/{}'.format(diretorio2, '{}.wav'.format(musica))) == True):
            socketClient.send(request.encode('utf-8'))
            time.sleep(1)
            enviar(musica)
            socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socketClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            socketClient.connect((ipServer, port))
        else:
            print('Musica Não Encontrada')
    elif request == 'baixar':
        socketClient.send(request.encode('utf-8'))
        musica = input('Musica: ')
        baixar(musica)
        socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socketClient.connect((ipServer, port))
    elif request == 'tocar':
        socketClient.send(request.encode('utf-8'))
        musica = input('Musica: ')
        tocar(musica)
        socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socketClient.connect((ipServer, port))
    elif request == '?' or request == 'listar':
        listar()
    elif request == 'sair':
        sair()
        break
    else:
        print('Comando Inválido! Digite "?" para Solicitar a Lista de Comandos Disponiveis.')