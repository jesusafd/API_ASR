import paramiko
import time
class Enrrutamiento():
    @classmethod
    def activar_rip(cls,network):
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
        for ip in network:
            comando += f'network {ip}\n'
        comando += 'version 2\n'
        comando += 'no auto-summary\n'
        comando += 'end\n'
        comando += 'wr\n'
        return comando

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
        return comando

    @classmethod
    def activar_ospf(cls,network):
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
        for ip in network:
            comando += f'network {ip} 0.0.0.255 area 0\n'
        comando += 'end\n'
        comando += 'wr\n'
        return comando

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
        return comando

    @classmethod
    def activar_eigrp(cls,network):
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
        for ip in network:
            comando += f'network {ip} 0.0.0.255\n'
        comando += 'end\n'
        comando += 'wr\n'
        return comando

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
        return comando




