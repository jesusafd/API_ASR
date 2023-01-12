from Enrrutamiento import Enrrutamiento
import socket
import time


def enrrutamineto_telnet(cliente_telnet,router,ruta,network,enrrutamiento):
    '''
    enrrutamineto_telnet recibe el id del router a enrrutar, la para 
    llegar a el por medio de conexiones telnet y redes ip que se van a 
    configurar en ese router
    '''
    # bloque de logeo de sesion telnet
    time.sleep(3)
    cliente_telnet.recv(1024)
    cliente_telnet.send("admin\n".encode())
    cliente_telnet.recv(1024)
    cliente_telnet.send("admin\n".encode())
    cliente_telnet.recv(1024)
    cliente_telnet.send("enable\n".encode())
    cliente_telnet.recv(1024)
    cliente_telnet.send("admin\n".encode())
    
    if len(ruta) > 0:
        # si el largo de ruta no es igual a 0, aun tenemos saltos que
        # hacer para llegar al router a enrrutar
        cliente_telnet.send(f'telnet {ruta[0]}\n'.encode())
        enrrutamineto_telnet(cliente_telnet,router,ruta[1:],network,enrrutamiento)
    else:
        # Una vez que el arreglo ruta este vacio quiere decir que llegamos
        # al router a enrrutar, por lo que llamaremos a la funcion del 
        # respectivo enrrutamiento

        # Geramos el comando para el enrrutamineto solicitado
        if enrrutamiento == 'RIP':
            comando = Enrrutamiento.activar_rip(network)
        elif enrrutamiento == 'OSPF':
            comando = Enrrutamiento.activar_ospf(network)
        elif enrrutamiento == 'EIGRP':
            comando = Enrrutamiento.activar_eigrp(network)
        cliente_telnet.recv(1024).decode()
        cliente_telnet.send(comando.encode())
        time.sleep(3)
        res = cliente_telnet.recv(2048).decode()
        print(str(res).replace("\\n","\n").replace("\\r","\r"))
    cliente_telnet.send("exit".encode())
    res=cliente_telnet.recv(1024)

    
