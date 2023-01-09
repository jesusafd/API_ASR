import socket
import paramiko
import time

class SSH():
    @classmethod
    def generar_configuracion(cls,username,password):
        configuracion = "configure terminal\n"
        configuracion += "ip domain-name asr.escom.ipn.mx\n"
        configuracion += "ip ssh rsa keypair-name sshkey\n"
        configuracion += "crypto key generate rsa usage-keys label sshkey modulus 1024\n"
        configuracion += "ip ssh v 2\n"
        configuracion += "ip ssh time-out 30\n"
        configuracion += "ip ssh authentication-retries 3\n"
        configuracion += "line vty 0 15\n"
        configuracion += f'password {password}\n'
        configuracion += "login local\n"
        configuracion += "exit\n"
        configuracion += f'username {username} privilege 15 password {password}\n'
        configuracion += "end\n"
        configuracion += "wr\n"
        return configuracion


    @classmethod
    def desactivar_telnet(cls):
        comando = 'configure terminal\n'
        comando += 'line vty 0 4\n'
        comando += 'no transport input\n'
        comando += 'transport input ssh\n'
        comando += 'end\n'
        comando += 'wr\n'
        return comando

    @classmethod
    def levantar_ssh(cls,ip,username,password):
        '''
        levantar_ssh realiza la configuracion ssh para el router con la direccion ip recibida
        recibe tambien el nombre de usario a definir en el configuracion asi mismo la contraseña
        '''
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
        comando = SSH.generar_configuracion(username,password)
        cliente_telnet.send(comando.encode())
        time.sleep(2)
        res = cliente_telnet.recv(2048)
        print(str(res).replace("\\n","\n").replace("\\r","\r"))
        cliente_telnet.close()

        # Nos conectamos por ssh para dar de baja telnet
        # Inicia un cliente SSH
        ssh_client = paramiko.SSHClient()
        # Establecer política por defecto para localizar la llave del host localmente
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Conectarse
        ssh_client.connect(ip, 22, username, password)
        # Generamos el comando dar de baja telnet
        comando = SSH.desactivar_telnet()
        entrada, salida, error = ssh_client.exec_command(comando)
        print (salida.read())
        # Cerrar la conexión
        ssh_client.close()
        # En caso de que todo salira bien devolvemos verdadero
        return True
