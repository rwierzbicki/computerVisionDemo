import bluetooth

bdCarAddr = "car address"
bdBaseAddr = "groundstation address"

def serverconnect(port, addr, protocol):
    
    serverSock = bluetooth.BluetoothSocket(protocol)
    serverSock.bind((addr, port))
    serverSock.listen(1)
    clientSock, address = serverSock.accept()

    return (serverSock, clientSock)

def clientconnect(port, addr, protocol):

    sock = bluetooth.BluetoothSocket(protocol)
    sock.connect((addr, port))

    return sock

