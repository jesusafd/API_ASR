
def asignacion_direcciones_interfaz(routera,routerb,interfaz,ip):
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
    if interfaz == 'f0_0':
            routera.f0_0=direcciona
            routerb.f0_0=direccionb
    elif interfaz == 'f1_0':
        if routera.f0_0 == "" and routerb.f0_0 == "":
            routera.f1_0=direcciona
            routerb.f1_0=direccionb
    elif interfaz == 'f1_1':
        if routera.f0_0 == "" and routerb.f0_0 == "":
            routera.f1_1=direcciona
            routera.f1_1=direcciona
    elif interfaz == 'f2_0':
        if routera.f0_0 == "" and routerb.f0_0 == "":
            routera.f2_0=direcciona
            routerb.f2_0=direccionb
    elif interfaz == 'f2_1':
        if routera.f0_0 == "" and routerb.f0_0 == "":
            routera.f2_2=direcciona
            routerb.f2_2=direccionb
    elif interfaz == 'f3_0':
        if routera.f0_0 == "" and routerb.f0_0 == "":
            routera.f3_0=direcciona
            routerb.f3_0=direccionb
    elif interfaz == 'f3_1':
        if routera.f0_0 == "" and routerb.f0_0 == "":
            routera.f3_1=direcciona
            routerb.f3_1=direccionb
    elif interfaz == 'f4_0':
        if routera.f0_0 == "" and routerb.f0_0 == "":
            routera.f4_0=direcciona
            routerb.f4_0=direccionb
    elif interfaz == 'f4_1':
        if routera.f0_0 == "" and routerb.f0_0 == "":
            routera.f4_1=direcciona
            routerb.f4_1=direccionb
    elif interfaz == 'f5_0':
        if routera.f0_0 == "" and routerb.f0_0 == "":
            routera.f5_0=direcciona
            routerb.f5_0=direccionb
    elif interfaz == 'f5_1':
        if routera.f0_0 == "" and routerb.f0_0 == "":
            routera.f5_1=direcciona
            routerb.f5_1=direccionb
    elif interfaz == 'f6_0':
        if routera.f0_0 == "" and routerb.f0_0 == "":
            routera.f6_0=direcciona
            routerb.f6_0=direccionb
    elif interfaz == 'f6_1':
        if routera.f0_0 == "" and routerb.f0_0 == "":
            routera.f6_1=direcciona
            routerb.f6_1=direccionb