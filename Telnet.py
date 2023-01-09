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
        # Inicia un cliente SSH
        ssh_client = paramiko.SSHClient()
        # Establecer política por defecto para localizar la llave del host localmente
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Conectarse
        ssh_client.connect(ip, 22, username, password)
        # Generamos el comando de configuracion telnet
        comando = Telnet.generar_configuracion(username,password)
        entrada, salida, error = ssh_client.exec_command(comando)
        print (salida.read())

        # Generamos el comando dar de baja ssh
        comando = Telnet.desactivar_ssh()
        entrada, salida, error = ssh_client.exec_command(comando)
        print (salida.read())
        # Cerrar la conexión
        ssh_client.close()
