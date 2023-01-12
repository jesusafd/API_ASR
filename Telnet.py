import socket
import time
import paramiko

class Telnet():
    @classmethod
    def generar_configuracion(cls,username,password):
        configuracion = "configure terminal\n"
        configuracion += f"enable password {password}\n"
        configuracion += f"username {username} password 0 {password}\n"
        configuracion += "line vty 0 4\n"
        configuracion += "logging synchronous\n"
        configuracion += "login local\n"
        configuracion += "transport input telnet\n"
        configuracion += "end\n"
        configuracion += "wr\n"
        return configuracion

    @classmethod
    def desactivar_ssh(cls):
        comando = 'configure terminal\n'
        comando += 'line vty 0 15\n'
        comando += 'no transport input\n'
        comando += 'transport input telnet\n'
        comando += 'end\n'
        comando += 'wr\n'
        return comando

    @classmethod
    def levantar_telnet(cls,ip,username,password):
        # Creamos un socket telnet para realizar la configuracion por medio de telnet
        cliente_telnet = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        
        # Nos conectamos al ruoter
        cliente_telnet.connect((ip,23))
        # Accedemos a la cuenta telnet y nos logeamos
        cliente_telnet.recv(1024)
        cliente_telnet.send("admin\n".encode())
        cliente_telnet.recv(1024)
        cliente_telnet.send("admin\n".encode())
        cliente_telnet.recv(1024)
        cliente_telnet.send("enable\n".encode())
        cliente_telnet.recv(1024)
        cliente_telnet.send("admin\n".encode())
        cliente_telnet.recv(1024)
        time.sleep(1)
        # Creamos el comando para la configuracion y lo ejcutamos
        comando = Telnet.desactivar_ssh()
        cliente_telnet.send(comando.encode())
        time.sleep(2)
        res = cliente_telnet.recv(2048)
        print(str(res).replace("\\n","\n").replace("\\r","\r"))
        cliente_telnet.close()
        return True
