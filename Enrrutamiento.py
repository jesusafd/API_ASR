class Enrrutamiento():
    '''
    La clase Enrrutamiento es una clase con metodos statico, los cuales proporcionan los
    comandos necesarios para realizar la activacion o des activacion de 3 protocolos de 
    enrrutamiento dinamico (RIP, OSPF, EIGRP)
    '''
    @classmethod
    def activar_rip(cls,network):
        '''
        El metdo genera el comando necesario para levantar el enrruatamiento dinamico RIP
        en cualquier router

        Parametros

        network: es una lista de las direcciones ip que estaran conectadas al router
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
    def desactivar_rip(cls):
        # Creamos el comando a ejecutar en el router
        comando = 'configure terminal\n'
        comando += 'no router rip\n'
        comando += 'end\n'
        comando += 'wr\n'
        return comando

    @classmethod
    def activar_ospf(cls,network):
        '''
        El metdo genera el comando necesario para levantar el enrruatamiento dinamico OSPF
        en cualquier router

        Parametros

        network: es una lista de las direcciones ip que estaran conectadas al router
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
    def desactivar_ospf(cls):
        # Creamos el comando a ejecutar en el router
        comando = 'configure terminal\n'
        comando += 'no router ospf 1\n'
        comando += 'end\n'
        comando += 'wr\n'
        return comando

    @classmethod
    def activar_eigrp(cls,network):
        '''
        El metdo genera el comando necesario para levantar el enrruatamiento dinamico EIGRP
        en cualquier router

        Parametros

        network: es una lista de las direcciones ip que estaran conectadas al router
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
    def desactivar_eigrp(cls):
        # Creamos el comando a ejecutar en el router
        comando = 'configure terminal\n'
        comando += 'no router eigrp 22\n'
        comando += 'end\n'
        comando += 'wr\n'
        return comando




