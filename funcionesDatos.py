
def asignacion_direcciones_interfaz(dispositivoa,dispositivob,interfaz,ip):
    '''
    asignacion_direcciones_interfaz Es la funcion que se encarga de asignar las direcciones ip a las interfaces de los routers
    en el caso de una conexion router-router se usara la misma interface en ambos routers, en el caso de conexion router-pc
    se usara la interface f0_0 en el router y en la pc la interface e
    '''
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

def extraccion_ip_interfaz(router):
    '''
    extraccion_ip_interfaz busca una direccion ip entre las interfaces del router que no sea valida (no vacia)
    y la devuelve, en caso de no encontrar devolvera una cadena vacia lo cual para python es un valor negativo
    '''
    if router.f0_0 != "":
        return router.f0_0
    elif router.f1_0 != "":
        return router.f1_0
    elif router.f1_1 != "":
        return router.f1_1
    elif router.f2_0 != "":
        return router.f2_0
    elif router.f2_1 != "":
        return router.f2_1
    elif router.f3_0 != "":
        return router.f3_0
    elif router.f3_1 != "":
        return router.f3_1
    elif router.f4_0 != "":
        return router.f4_0
    elif router.f4_1 != "":
        return router.f4_1
    elif router.f5_0 != "":
        return router.f5_0
    elif router.f5_1 != "":
        return router.f5_1
    elif router.f6_0 != "":
        return router.f6_0
    elif router.f6_1 != "":
        return router.f6_1
    else:
        return ""


def asignacion_posicion_enrrutamiento(enrrutamiento,protocolo):
    '''
    asignacion_posicion_enrrutamiento se encarga de asignar un posicion al nuevo enrrutamiento
    el sistema no permite dar de baja todos los enrruateintos por defecto uno debe seguir activo
    por lo que las posiciones  a asiganar siempre seran 2 y 3

    los objetos en python se pasan por referencia por lo que no es necesario retornar nada, ya que
    se modifico el objeto, pero por buenas practicas se hace
    '''
    print(enrrutamiento.primero)
    print(enrrutamiento.segundo)
    print(enrrutamiento.tercero)
    print(protocolo)
    if enrrutamiento.segundo == None:
        enrrutamiento.segundo = protocolo
    else:
        enrrutamiento.trecero = protocolo

    print(enrrutamiento.primero)
    print(enrrutamiento.segundo)
    print(enrrutamiento.tercero)

    return enrrutamiento

def reasignacion_posicion_enrrutamiento(enrrutamiento,protocolo):
    '''
    reasignacion_posicion_enrrutamiento se encarga de recorrer el orden de los protocolos enrrutados
    '''
    if enrrutamiento.primero == protocolo:
        enrrutamiento.primero = enrrutamiento.segundo
        enrrutamiento.segundo = enrrutamiento.tercero
        enrrutamiento.tercero = None
    elif enrrutamiento.segundo == protocolo:
        enrrutamiento.segundo = enrrutamiento.tercero
        enrrutamiento.tercero = None
    else:
        enrrutamiento.tercero = None
    
    print(enrrutamiento.primero)
    print(enrrutamiento.segundo)
    print(enrrutamiento.tercero)

    return enrrutamiento
