
def asignacion_direcciones_interfaz(dispositivoa,dispositivob,interfaz,ip):
    # Separamos los octetos de la direccion ip de la interface para poder asignar una ip a cada extremo del conexion
    octetos=ip.split(".")
    # La primera direccion valida la asiganmos al lado a de la conexion
    octetos[-1]=str(int(octetos[-1])+1)
    direcciona='.'.join(octetos)
    # La segunda direccion valida la asiganmos al lado b de la conexion
    octetos[-1]=str(int(octetos[-1])+1)
    direccionb='.'.join(octetos)
    # Dependiendo de la interfaz asiganmos la ip a la interface respectiva
    # Las interfaces se conectaran solo si no tiene una ip asignada
    if interfaz == "e":
        # interfaz ethernet
        if dispositivoa.f0_0 == "" and dispositivob.e == "":
            dispositivoa.f0_0=direcciona
            dispositivob.e=direccionb
            return True
        else:
            return False
    elif interfaz == 'f0_0':
        if dispositivoa.f0_0 == "" and dispositivob.f0_0 == "":
            dispositivoa.f0_0=direcciona
            dispositivob.f0_0=direccionb
            return True
        else:
            return False
    elif interfaz == 'f1_0':
        if dispositivoa.f1_0 == "" and dispositivob.f1_0 == "":
            dispositivoa.f1_0=direcciona
            dispositivob.f1_0=direccionb
            return True
        else:
            return False
    elif interfaz == 'f1_1':
        if dispositivoa.f1_1 == "" and dispositivob.f1_1 == "":
            dispositivoa.f1_1=direcciona
            dispositivob.f1_1=direccionb
            return True
        else:
            return False
    elif interfaz == 'f2_0':
        if dispositivoa.f2_0 == "" and dispositivob.f2_0 == "":
            dispositivoa.f2_0=direcciona
            dispositivob.f2_0=direccionb
            return True
        else:
            return False
    elif interfaz == 'f2_1':
        if dispositivoa.f2_1 == "" and dispositivob.f2_1 == "":
            dispositivoa.f2_1=direcciona
            dispositivob.f2_1=direccionb
            return True
        else:
            return False
    elif interfaz == 'f3_0':
        if dispositivoa.f3_0 == "" and dispositivob.f3_0 == "":
            dispositivoa.f3_0=direcciona
            dispositivob.f3_0=direccionb
            return True
        else:
            return False
    elif interfaz == 'f3_1':
        if dispositivoa.f3_1 == "" and dispositivob.f3_1 == "":
            dispositivoa.f3_1=direcciona
            dispositivob.f3_1=direccionb
            return True
        else:
            return False
    elif interfaz == 'f4_0':
        if dispositivoa.f4_0 == "" and dispositivob.f4_0 == "":
            dispositivoa.f4_0=direcciona
            dispositivob.f4_0=direccionb
            return True
        else:
            return False
    elif interfaz == 'f4_1':
        if dispositivoa.f4_1 == "" and dispositivob.f4_1 == "":
            dispositivoa.f4_1=direcciona
            dispositivob.f4_1=direccionb
            return True
        else:
            return False
    elif interfaz == 'f5_0':
        if dispositivoa.f5_0 == "" and dispositivob.f5_0 == "":
            dispositivoa.f5_0=direcciona
            dispositivob.f5_0=direccionb
            return True
        else:
            return False
    elif interfaz == 'f5_1':
        if dispositivoa.f5_1 == "" and dispositivob.f5_1 == "":
            dispositivoa.f5_1=direcciona
            dispositivob.f5_1=direccionb
            return True
        else:
            return False
    elif interfaz == 'f6_0':
        if dispositivoa.f6_0 == "" and dispositivob.f6_0 == "":
            dispositivoa.f6_0=direcciona
            dispositivob.f6_0=direccionb
            return True
        else:
            return False
    elif interfaz == 'f6_1':
        if dispositivoa.f6_1 == "" and dispositivob.f6_1 == "":
            dispositivoa.f6_1=direcciona
            dispositivob.f6_1=direccionb
            return True
        else:
            return False