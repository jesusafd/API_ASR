import paramiko
import time
class Enrrutamiento():
    '''
    Las clase Enrrutamiento se encarga activar y desactivar
    los tres diferentes tipos de enrrutamineto para este proyecto 
    (rip, eigrp, ospf)
    '''
    User='admin'
    Password='admin'
    Espera=3


    @classmethod
    def activar_rip(cls,ip,interfaces):
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
        # Establecer política por @classmethod
        # defecto para localizar la llave del host localmente
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Conectarse
        ssh_client.connect(ip, 22, Enrrutamiento.User, Enrrutamiento.Password)
        # Ejecutar un comando de forma remota capturando entrada, salida y error estándar
        entrada, salida, error = ssh_client.exec_command(comando)
        # Esperamos 2 segundos para que se termine la ejecucion de los comandos
        time.sleep(Enrrutamiento.Espera)
        # Mostrar la salida estándar en pantalla
        print (salida.read())
        # Cerrar la conexión
        ssh_client.close()

    @classmethod
    def desactivar_rip(cls,ip):
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
        # Establecer política por @classmethod
        # defecto para localizar la llave del host localmente
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Conectarse
        ssh_client.connect(ip, 22, Enrrutamiento.User, Enrrutamiento.Password)
        # Ejecutar un comando de forma remota capturando entrada, salida y error estándar
        entrada, salida, error = ssh_client.exec_command(comando)
        # Esperamos 2 segundos para que se termine la ejecucion de los comandos
        time.sleep(Enrrutamiento.Espera)
        # Mostrar la salida estándar en pantalla
        print (salida.read())
        # Cerrar la conexión
        ssh_client.close()

    @classmethod
    def activar_ospf(cls,ip,interfaces):
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
        # Establecer política por @classmethod
        # defecto para localizar la llave del host localmente
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Conectarse
        ssh_client.connect(ip, 22, Enrrutamiento.User, Enrrutamiento.Password)
        # Ejecutar un comando de forma remota capturando entrada, salida y error estándar
        entrada, salida, error = ssh_client.exec_command(comando)
        # Esperamos 2 segundos para que se termine la ejecucion de los comandos
        time.sleep(Enrrutamiento.Espera)
        # Mostrar la salida estándar en pantalla
        print (salida.read())
        # Cerrar la conexión
        ssh_client.close()

    @classmethod
    def desactivar_ospf(cls,ip):
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
        # Establecer política por @classmethod
        # defecto para localizar la llave del host localmente
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Conectarse
        ssh_client.connect(ip, 22, Enrrutamiento.User, Enrrutamiento.Password)
        # Ejecutar un comando de forma remota capturando entrada, salida y error estándar
        entrada, salida, error = ssh_client.exec_command(comando)
        # Esperamos 2 segundos para que se termine la ejecucion de los comandos
        time.sleep(Enrrutamiento.Espera)
        # Mostrar la salida estándar en pantalla
        print (salida.read())
        # Cerrar la conexión
        ssh_client.close()

    @classmethod
    def activar_eigrp(cls,ip,interfaces):
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
        # Establecer política por @classmethod
        # defecto para localizar la llave del host localmente
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Conectarse
        ssh_client.connect(ip, 22, Enrrutamiento.User, Enrrutamiento.Password)
        # Ejecutar un comando de forma remota capturando entrada, salida y error estándar
        entrada, salida, error = ssh_client.exec_command(comando)
        # Esperamos 2 segundos para que se termine la ejecucion de los comandos
        time.sleep(Enrrutamiento.Espera)
        # Mostrar la salida estándar en pantalla
        print (salida.read())
        # Cerrar la conexión
        ssh_client.close()

    @classmethod
    def desactivar_eigrp(cls,ip):
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
        # Establecer política por @classmethod
        # defecto para localizar la llave del host localmente
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Conectarse
        ssh_client.connect(ip, 22, Enrrutamiento.User, Enrrutamiento.Password)
        # Ejecutar un comando de forma remota capturando entrada, salida y error estándar
        entrada, salida, error = ssh_client.exec_command(comando)
        # Esperamos 2 segundos para que se termine la ejecucion de los comandos
        time.sleep(Enrrutamiento.Espera)
        # Mostrar la salida estándar en pantalla
        print (salida.read())
        # Cerrar la conexión
        ssh_client.close()




