import telnetlib

def comprobar_conexion(HOST):
    '''
    comprobar_conexion realiza una conexion telnet al HOST, en caso de dar un error quiere decir
    que no existe una configuracion telnet en el router
    '''
    try:
        # Conexion a al dispositivo con la libreria telnet 
        conexion = telnetlib.Telnet(HOST)
        conexion.close()
        return True
    except:
        return False

def levantar_SSH(HOST):
    user='admin'
    password='admin'
    # El bloque try-except permite solo realizar la configuracion ssh si previamente existe una 
    # conexion telnet
    try:
        # Conexion a al dispositivo con la libreria telnet 
        conexion = telnetlib.Telnet(HOST)
        print("Conexion telnet")
        # Leemos la pantalla hasta encontra que aparsca la linea Username
        conexion.read_until(b"Username: ")
        conexion.write(user.encode('ascii') + b"\n")
        # Ingresamos la contraseña
        conexion.read_until(b"Password: ")
        conexion.write(password.encode('ascii') + b"\n")
        # Comandos a ejecutar en el equipo via telnet
        conexion.write(b"enable\n")
        conexion.write(password.encode('ascii') + b"\n")
        

        # Damos de baja la conexion telnet
        conexion.write(b"conf t\n")
        conexion.write(b"line vty 0 4\n")
        conexion.write(b"no transport input\n")
        conexion.write(b"transport input ssh\n")
        conexion.write(b"end\n")
        conexion.write(b"wr\n")

        # Configuramos ssh
        conexion.write(b"configure terminal\n")
        conexion.write(b"ip domain-name asr.escom.ipn.mx\n")
        conexion.write(b"ip ssh rsa keypair-name sshkey\n")
        conexion.write(b"crypto key generate rsa usage-keys label sshkey modulus 1024\n")
        conexion.write(b"ip ssh v 2\n")
        # conexion.write(b"ip ssh time-out 30\n")
        conexion.write(b"ip ssh authentication-retries 3\n")
        conexion.write(b"line vty 0 15\n")
        conexion.write(b"password admin\n")
        conexion.write(b"login local\n")
        conexion.write(b"transport input ssh\n")
        conexion.write(b"exit\n")
        conexion.write(b"username admin privilege 15 password admin\n")
        conexion.write(b"exit\n")
        conexion.write(b"wr\n")

        # Salimos de la sesion
        conexion.write(b"exit\n")
        # Cerramos la conexion
        conexion.close()
        return
    except:
        return

    