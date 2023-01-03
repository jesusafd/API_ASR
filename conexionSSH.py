import paramiko
import time
class Enrrutamiento():
    def __init__(self,user,password,espera):
        '''
        Las clase Enrrutamiento se encarga activar y desactivar
        los tres diferentes tipos de enrrutamineto para este proyecto 
        (rip, eigrp, ospf) el constructor de este objeto recibe 3 
        argumentos.
        user: es el nombre de usuario del router del dispositivo
        password: es la contraseña del router
        espera: es el tiempo de espera para que los comandos se ejecuten
        '''
        self._user=user
        self._password=password
        self._espera=espera

    def activar_rip(self,ip,port,interfaces):
        '''
        activar_rip es el metodo encargado de activar el protocolo de
        enrrutamiento rip en el router especificado, este metodo recibe
        3 argumentos:
        ip: la direccion ip de la interface del router que desamos configurar
        port: el puerto a conectar
        interfaces: es una lista de las interfaces conectadas al router
        '''
        # Creamos el comando a ejecutar en el router
        comando = 'configure terminal\n'
        comando += 'router rip\n'
        # Agregamos las redes al comando
        for interface in interfaces:
            comando += f'network {interface.ip}\n'
        comando += 'version 2\n'
        comando += 'no auto-summary\n'
        comando += 'end\n'
        comando += 'wr\n'

        # Inicia un cliente SSH
        ssh_client = paramiko.SSHClient()
        # Establecer política por defecto para localizar la llave del host localmente
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Conectarse
        ssh_client.connect(ip, port, self._user, self._password)
        # Ejecutar un comando de forma remota capturando entrada, salida y error estándar
        entrada, salida, error = ssh_client.exec_command(comando)
        # Esperamos 2 segundos para que se termine la ejecucion de los comandos
        time.sleep(self._espera)
        # Mostrar la salida estándar en pantalla
        print (salida.read())
        # Cerrar la conexión
        ssh_client.close()

    def desactivar_rip(self,ip,port):
        '''
        desactivar_rip es el metodo encargado de desactivar el protocolo de
        enrrutamiento rip en el router especificado, este metodo recibe
        dos parametros:
        ip: la direccion ip de la interface del router que desamos configurar
        port: el puerto a conectar
        '''
        # Creamos el comando a ejecutar en el router
        comando = 'configure terminal\n'
        comando += 'no router rip\n'
        comando += 'end\n'
        comando += 'wr\n'
        # Inicia un cliente SSH
        ssh_client = paramiko.SSHClient()
        # Establecer política por defecto para localizar la llave del host localmente
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Conectarse
        ssh_client.connect(ip, port, self._user, self._password)
        # Ejecutar un comando de forma remota capturando entrada, salida y error estándar
        entrada, salida, error = ssh_client.exec_command(comando)
        # Esperamos 2 segundos para que se termine la ejecucion de los comandos
        time.sleep(self._espera)
        # Mostrar la salida estándar en pantalla
        print (salida.read())
        # Cerrar la conexión
        ssh_client.close()

    def activar_ospf(self,ip,port,interfaces):
        '''
        activar_ospf es el metodo encargado de activar el protocolo de
        enrrutamiento ospf en el router especificado, este metodo recibe
        3 argumentos:
        ip: la direccion ip de la interface del router que desamos configurar
        port: el puerto a conectar
        interfaces: es una lista de las interfaces conectadas al router
        '''
        # Creamos el comando a ejecutar en el router
        comando = 'configure terminal\n'
        comando += 'router ospf 1\n'
        # Agregamos las redes al comando
        for interface in interfaces:
            comando += f'network {interface.ip} 0.0.0.255 area 0\n'
        comando += 'end\n'
        comando += 'wr\n'

        # Inicia un cliente SSH
        ssh_client = paramiko.SSHClient()
        # Establecer política por defecto para localizar la llave del host localmente
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Conectarse
        ssh_client.connect(ip, port, self._user, self._password)
        # Ejecutar un comando de forma remota capturando entrada, salida y error estándar
        entrada, salida, error = ssh_client.exec_command(comando)
        # Esperamos 2 segundos para que se termine la ejecucion de los comandos
        time.sleep(self._espera)
        # Mostrar la salida estándar en pantalla
        print (salida.read())
        # Cerrar la conexión
        ssh_client.close()

    def desactivar_ospf(self,ip,port):
        '''
        desactivar_ospf es el metodo encargado de desactivar el protocolo de
        enrrutamiento ospf en el router especificado, este metodo recibe
        dos parametros:
        ip: la direccion ip de la interface del router que desamos configurar
        port: el puerto a conectar
        '''
        # Creamos el comando a ejecutar en el router
        comando = 'configure terminal\n'
        comando += 'no router ospf 1\n'
        comando += 'end\n'
        comando += 'wr\n'
        # Inicia un cliente SSH
        ssh_client = paramiko.SSHClient()
        # Establecer política por defecto para localizar la llave del host localmente
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Conectarse
        ssh_client.connect(ip, port, self._user, self._password)
        # Ejecutar un comando de forma remota capturando entrada, salida y error estándar
        entrada, salida, error = ssh_client.exec_command(comando)
        # Esperamos 2 segundos para que se termine la ejecucion de los comandos
        time.sleep(self._espera)
        # Mostrar la salida estándar en pantalla
        print (salida.read())
        # Cerrar la conexión
        ssh_client.close()

    def activar_eigrp(self,ip,port,interfaces):
        '''
        activar_eigrp es el metodo encargado de activar el protocolo de
        enrrutamiento eigrp en el router especificado, este metodo recibe
        3 argumentos:
        ip: la direccion ip de la interface del router que desamos configurar
        port: el puerto a conectar
        interfaces: es una lista de las interfaces conectadas al router
        '''
        # Creamos el comando a ejecutar en el router
        comando = 'configure terminal\n'
        comando += 'router eigrp 22\n'
        # Agregamos las redes al comando
        for interface in interfaces:
            comando += f'network {interface.ip} 0.0.0.255\n'
        comando += 'end\n'
        comando += 'wr\n'

        # Inicia un cliente SSH
        ssh_client = paramiko.SSHClient()
        # Establecer política por defecto para localizar la llave del host localmente
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Conectarse
        ssh_client.connect(ip, port, self._user, self._password)
        # Ejecutar un comando de forma remota capturando entrada, salida y error estándar
        entrada, salida, error = ssh_client.exec_command(comando)
        # Esperamos 2 segundos para que se termine la ejecucion de los comandos
        time.sleep(self._espera)
        # Mostrar la salida estándar en pantalla
        print (salida.read())
        # Cerrar la conexión
        ssh_client.close()

    def desactivar_eigrp(self,ip,port):
        '''
        desactivar_eigrp es el metodo encargado de desactivar el protocolo de
        enrrutamiento eigrp en el router especificado, este metodo recibe
        dos parametros:
        ip: la direccion ip de la interface del router que desamos configurar
        port: el puerto a conectar
        '''
        # Creamos el comando a ejecutar en el router
        comando = 'configure terminal\n'
        comando += 'no router eigrp 22\n'
        comando += 'end\n'
        comando += 'wr\n'
        # Inicia un cliente SSH
        ssh_client = paramiko.SSHClient()
        # Establecer política por defecto para localizar la llave del host localmente
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Conectarse
        ssh_client.connect(ip, port, self._user, self._password)
        # Ejecutar un comando de forma remota capturando entrada, salida y error estándar
        entrada, salida, error = ssh_client.exec_command(comando)
        # Esperamos 2 segundos para que se termine la ejecucion de los comandos
        time.sleep(self._espera)
        # Mostrar la salida estándar en pantalla
        print (salida.read())
        # Cerrar la conexión
        ssh_client.close()




