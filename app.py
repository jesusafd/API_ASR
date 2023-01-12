from flask import Flask,request,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from funcionesDatos import asignacion_direcciones_interfaz,extraccion_ip_interfaz,asignacion_posicion_enrrutamiento,reasignacion_posicion_enrrutamiento
from conexionTelnet import enrrutamineto_telnet
from Worker import Worker
from Monitoreo import Monitoreo
import Enrrutamiento as E
from SSH import SSH
from Telnet import Telnet
import rutas as r
import networkx as nx
import matplotlib.pyplot as plt
import time
import os
import socket

eunrrutamineto_activo = None
app = Flask(__name__)
IMG_FOLDER = os.path.join('static', 'IMG')
app.config['UPLOAD_FOLDER'] = IMG_FOLDER
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///dbApi.sqlite3'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)

migarte = Migrate(app,db)

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------Modelos-----------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

# -----------------------------------Usuario-----------------------------------

# -----------------------------------Routers-----------------------------------
class Router(db.Model):
    '''
    El modelo router 
    '''
    _tablename_='router'
    id = db.Column(db.String(64),primary_key=True)
    f0_0 = db.Column(db.String(64))
    f1_0 = db.Column(db.String(64))
    f1_1 = db.Column(db.String(64))
    f2_0 = db.Column(db.String(64))
    f2_1 = db.Column(db.String(64))
    f3_0 = db.Column(db.String(64))
    f3_1 = db.Column(db.String(64))
    f4_0 = db.Column(db.String(64))
    f4_1 = db.Column(db.String(64))
    f5_0 = db.Column(db.String(64))
    f5_1 = db.Column(db.String(64))
    f6_0 = db.Column(db.String(64))
    f6_1 = db.Column(db.String(64))

    def set_data(self,data):
        self.id=data['id']
        # La interfaz f0_0 de todos los routers simpres se usara para conectar pcs o switches
        self.f0_0=""
        self.f1_0=""
        self.f1_1=""
        self.f2_0=""
        self.f2_1=""
        self.f3_0=""
        self.f3_1=""
        self.f4_0=""
        self.f4_1=""
        self.f5_0=""
        self.f5_1=""
        self.f6_0=""
        self.f6_1=""

    def get_data(self):
        return{
            "id":self.id,
            "f0_0":self.f0_0,
            "f1_0":self.f1_0,
            "f1_1":self.f1_1,
            "f2_0":self.f2_0,
            "f2_1":self.f2_1,
            "f3_0":self.f3_0,
            "f3_1":self.f3_1,
            "f4_0":self.f4_0,
            "f4_1":self.f4_1,
            "f5_0":self.f5_0,
            "f5_1":self.f5_1,
            "f6_0":self.f6_0,
            "f6_1":self.f6_1,
        }
        
    
# --------------------------------------PCs--------------------------------------

class PC(db.Model):
    '''
    El modelo PC 
    '''
    _tablename_='pc'
    id = db.Column(db.String(64),primary_key=True)
    # e es la interfaz fasethernet
    e = db.Column(db.String(64))

    def set_data(self,data):
        self.id=data['id']
        self.e=""

    def get_data(self):
        return{
            "id":self.id,
            "e":self.e,
        }
        
    
# -----------------------------------Interface-----------------------------------
# El modelo interfaces
class Interface(db.Model):
    _tablename_='interface'
    ip = db.Column(db.String(64),primary_key=True)
    dispositivoa=db.Column(db.String(64))
    dispositivob=db.Column(db.String(64))
    interfaz=db.Column(db.String(64))

    def set_data(self,data):
        self.ip=data['ip']
        self.dispositivoa=data['dispositivoa']
        self.dispositivob=data['dispositivob']
        self.interfaz=data['interfaz']

    def get_data(self):
        return {
            'ip':self.ip,
            'dispositivoa':self.dispositivoa,
            'dispositivoa':self.dispositivob,
            'interfaz':self.interfaz
        }

# -----------------------------------Conexiones-----------------------------------
class Conexion(db.Model):
    _tablename_='conexion'
    id = db.Column(db.String(64),primary_key=True)
    tipo = db.Column(db.String(64))

    def set_data(self,data):
        self.id=data['id']
        self.tipo=data['tipo']


# -----------------------------------Enrrutamiento-----------------------------------
class Enrrutamiento(db.Model):
    _tablename_='enrrutamiento'
    id = db.Column(db.String(64),primary_key=True)
    primero = db.Column(db.String(64))
    segundo = db.Column(db.String(64))
    tercero = db.Column(db.String(64))



# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# -----------------------------------Endpoints-----------------------------------
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------



# -------------------------------------------------------------------------------
# -----------------------------Limpiar topologia---------------------------------
# -------------------------------------------------------------------------------

@app.route("/limpiar",methods=["GET"])
def limpiar():
    routers = Router.query.all()
    for router in routers:
        db.session.delete(router)
    interfaces = Interface.query.all()
    for interface in interfaces:
        db.session.delete(interface)
    pcs = PC.query.all()
    for pc in pcs:
        db.session.delete(pc)
    conexiones = Conexion.query.all()
    for conexion in conexiones:
        db.session.delete(conexion)
    enrrutamiento.query.get('1')
    db.session.delete(enrrutamiento)
    db.session.commit()
    return f'<h1>Topologia eliminada</h1>'


# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# -------------------------------------CRUDs-------------------------------------
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# -----------------------------------Routers-----------------------------------
# ------------------------------------------------------------------------------
# Agraegar router
@app.route("/router",methods=["POST"])
def agregar_routers():
    router = Router()
    data=request.json
    router.set_data(data)
    db.session.add(router)
    # Agregamos por defecto un usuario telnet
    conexion = Conexion()

    conexion.set_data({'id':router.id,'tipo':'telnet'})
    db.session.add(conexion)
    db.session.commit()
    return f'<h1>Router agregado</h1>'

# Listar todos los routers
@app.route("/router/<id>",methods=["GET"])
def ver_router(id):
    router=Router.query.get_or_404(id)
    return render_template("router.html",router=router)

# Ver router especifico
@app.route("/router",methods=["GET"])
def listar_routers():
    routers=Router.query.all()
    print(routers)
    return render_template("routers.html",routers=routers)

# Editar router
@app.route("/router",methods=['PUT'])
def editar_router():
    data=request.json
    router = Router.query.get_or_404(data['id'])
    router.set_data(data)
    db.session.commit()
    return f'<h1>Reouter editado</h1>'

# Eliminar router
@app.route("/router/<id>",methods=["DELETE"])
def eliminar_router(id):
    router=Router.query.get_or_404(id)
    db.session.delete(router)
    db.session.commit()
    # En caso de eliminar un router, eliminaremos las interfaces realicionadas a este
    # Extraemos los registros de la tabla de interfaces
    interfaces = Interface.query.all()
    for interface in interfaces:
        print(interface)
        if interface.routera == id or interface.routerb == id:
            eliminar_interface(interface.ip)
    return f'<h1>Rourter eliminado</h1>'

# Eliminar todos los routers
@app.route("/router",methods=["DELETE"])
def eliminar_todos_router():
    routers=Router.query.all()
    if len(routers)==0:
        return f'<h1>No hay routers</h1>'
    for router in routers:
        db.session.delete(router)
        # En caso de eliminar un router, eliminaremos las interfaces realicionadas a este
        # Extraemos los registros de la tabla de interfaces
        interfaces = Interface.query.all()
        for interface in interfaces:
            print(interface)
            if interface.dispositivoa == router.id or interface.dispositivob == router.id:
                eliminar_interface(interface.ip)
    db.session.commit()
    return f'<h1>Rourter eliminado</h1>'


# ------------------------------------------------------------------------------
# --------------------------------------PCs-------------------------------------
# ------------------------------------------------------------------------------
# Agraegar pc
@app.route("/pc",methods=["POST"])
def agregar_pc():
    pc = PC()
    data=request.json
    pc.set_data(data)
    db.session.add(pc)
    db.session.commit()
    return f'<h1>PC agregada</h1>'

# Listar todos las PCs
@app.route("/pc/<id>",methods=["GET"])
def ver_pc(id):
    pc=PC.query.get_or_404(id)
    return render_template("pc.html",pc=pc)

# Ver pc especifico
@app.route("/pc",methods=["GET"])
def listar_pcs():
    pcs=PC.query.all()
    print(pcs)
    return render_template("pcs.html",pcs=pcs)

# Editar pc
@app.route("/pc",methods=['PUT'])
def editar_pc():
    data=request.json
    pc = PC.query.get_or_404(data['id'])
    pc.set_data(data)
    db.session.commit()
    return f'<h1>PC editado</h1>'

# Eliminar router
@app.route("/pc/<id>",methods=["DELETE"])
def eliminar_pc(id):
    pc=PC.query.get_or_404(id)
    db.session.delete(pc)
    db.session.commit()
    # En caso de eliminar un router, eliminaremos las interfaces realicionadas a este
    # Extraemos los registros de la tabla de interfaces
    interfaces = Interface.query.all()
    for interface in interfaces:
        print(interface)
        if interface.dispositivoa == id or interface.dispositivob == id:
            eliminar_interface(interface.ip)
    return f'<h1>PC eliminada</h1>'

# Eliminar todos los routers
@app.route("/pc",methods=["DELETE"])
def eliminar_todos_pc():
    pcs=PC.query.all()
    if len(pcs)==0:
        return f'<h1>No hay routers</h1>'
    for pc in pcs:
        db.session.delete(pc)
        # En caso de eliminar un router, eliminaremos las interfaces realicionadas a este
        # Extraemos los registros de la tabla de interfaces
        interfaces = Interface.query.all()
        for interface in interfaces:
            print(interface)
            if interface.dispositivoa == pc.id or interface.dispositivob == pc.id:
                eliminar_interface(interface.ip)
    db.session.commit()
    return f'<h1>PCs eliminadas</h1>'

# ------------------------------------------------------------------------------
# -----------------------------------Interface----------------------------------
# ------------------------------------------------------------------------------

# Agraegar Intergace
@app.route("/interface",methods=["POST"])
def agregar_interface():
    interface = Interface()
    data=request.json
    interface.set_data(data)
    # Agregamos las direcciones a cada extremo de la interfaes
    # Recuperamos los objetos dispositivo de cada uno de los extremos de la conexion
    # en caso de que se conecte una pc al router esta siempre debera venir en el segundo dispositvo
    dispositivoa=Router.query.get(interface.dispositivoa)
    # Si la interfaz es una e quiere decir que conectaremos una pc de lo contrario sera un router
    if interface.interfaz == 'e':
        dispositivob=PC.query.get(interface.dispositivob)
    else:
        dispositivob=Router.query.get(interface.dispositivob)
    # la funcion asignacion_direcciones_interfaz asigna las ip validas a la intefaz correspondiente
    # Y devuelve una cadena con el estado de la asgignacion
    estado = asignacion_direcciones_interfaz(dispositivoa,dispositivob,interface.interfaz,interface.ip)
    # Hacemos el commit de los cambios
    if estado:
        # Agragamos el objeto interface a la base de datos en caso de que se pudiera asignar
        db.session.add(interface)
        db.session.commit()
        return f'<h1>Interface agregada</h1>'
    else:
        return f'<h1>Interface no agregada, puerto {interface.interfaz} ocupado</h1>'

# listar interfaces
@app.route("/interface",methods=["GET"])
def listar_interface():
    interfaces=Interface.query.all()
    return render_template("interfaces.html",interfaces=interfaces)

# Editar interface
@app.route("/interface",methods=['PUT'])
def editar_interface():
    data=request.json
    interface = Interface.query.get_or_404(data['ip'])
    interface.set_data(data)
    db.session.commit()
    return f'<h1>interface editada</h1>'

# Eliminar interface
@app.route("/interface/<ip>",methods=["DELETE"])
def eliminar_interface(ip):
    interface=Interface.query.get_or_404(ip)
    db.session.delete(interface)
    db.session.commit()
    return f'<h1>Interface eliminada</h1>'

# Eliminar todas las interface
@app.route("/interface",methods=["DELETE"])
def eliminar_todas_interfaces():
    interfaces=Interface.query.all()
    for interface in interfaces:
        db.session.delete(interface)
    db.session.commit()
    return f'<h1>Interfaces eliminadas</h1>'

# ------------------------------------------------------------------------------
# -----------------------------------Usuarios-----------------------------------
# ------------------------------------------------------------------------------
# Para los conexiones ya sea telnet o ssh lo unico que nos importa es ver la lista de estos
# Ver conexiones
@app.route("/conexiones",methods=["GET"])
def listar_conexiones():
    conexiones=Conexion.query.all()
    print(conexiones)
    return render_template("conexiones.html",conexiones=conexiones)

# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# -----------------------------------Funciones-----------------------------------
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------


# -----------------------------------Imagenes----------------------------------

@app.route("/topologia",methods=['GET'])
def generar_topologia():
    G = nx.Graph()
    interfaces = Interface.query.all()
    # Agregamos todas las conexiones al grafico
    for interface in interfaces:
        print(interfaces)
        G.add_edge(interface.dispositivoa,interface.dispositivob,weight=interface.ip)
    # Definimos la posicion del grafo
    pos = nx.layout.planar_layout(G)
    # Dibujamos los nodos
    nx.draw_networkx(G,pos)
    labels = nx.get_edge_attributes(G,"weight")
    # Dibujamos las aristas
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
    # Mostramos la grafica
    plt.title("Topologia")
    # Guardamos la imagen de la topologia
    plt.savefig("static/IMG/topologia.png")
    time.sleep(1)
    topologia = os.path.join(app.config['UPLOAD_FOLDER'], 'topologia.png')
    return render_template("topologia.html", image=topologia)

# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# -----------------------------------Enrrutamiento----------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------

# Levanetamos primer enrrutamiento
@app.route("/enrrutar",methods=["GET"])
@app.route("/enrrutar/<protocolo>",methods=["GET"])
@app.route("/enrrutar/<protocolo>/<id>",methods=["GET"])
def enrrutar(protocolo="RIP",id="PCMV"):
    '''
    El endpoint enrrutar puede puede recibiir dos parametros
    protocolo: el cual sera el protocolo de enrrutamineto dinamico por defecto es RIP
    id: el id del dispositivo desde el cual comenzaremos a enrrutar, en caso de que se 
        tengan mas maquinas virtuales conectadas, por defecto es PCMV
    '''

    # Verificamos que no este enrrutado posteriormento
    enrrutamiento = Enrrutamiento.query.all()
    if len(enrrutamiento) > 0:
        return '<h1>Ya se relizo un enrrutamiento posteriormento. Para cambiar de enrrutamiento favor de hacerlo mediante el endpoint enrrutamiento</h1>'

    G = nx.Graph()
    interfaces = Interface.query.all()
    # Generamos el grafico con todas las interfaces
    for interface in interfaces:
        G.add_edge(interface.dispositivoa,interface.dispositivob,IP=interface.ip)
    rutas = r.rutas(G,id)
    # Ahora obtenemos las direcciones ip (network) para el enrrutamiento de cada router
    network = {}
    for llave in rutas:
        aux = []
        for interfaz in interfaces:
            if interfaz.dispositivoa == llave or  interfaz.dispositivob == llave:
                aux.append(interfaz.ip)
        network[llave]=aux
    print(rutas)
    print(network)
    # Llamaremos a enrrutamineto_telnet para realizar un levantamiento de enrrutamiento
    # dinamico por medio de una sesion telnet
    for llave,ruta in rutas.items():
        # Creamos el socket que usaremos para conectarnos por telnet
        cliente = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # Nos conectamos a la direccion especificada
        cliente.connect((ruta[0],23))
        enrrutamineto_telnet(cliente,llave,ruta[1:],network[llave],protocolo)
    
    # reutilizamos la varible enrrutamiento ahora para crear un nuevo registro en la bd
    enrrutamiento = Enrrutamiento()
    # Al ser el primer enrutamietno todos los protocolos los colcamos vacios
    # para posteriormente solo ingresar el que se levanto
    
    enrrutamiento.id = '1'
    enrrutamiento.rip = None
    enrrutamiento.ospf = None
    enrrutamiento.eigrp = None
    # Se asiganra al respectivo enrrutamiento a la posicion unicial
    enrrutamiento.primero=protocolo
    # Guardamos el registro en la base de datos
    db.session.add(enrrutamiento)
    db.session.commit()
    return '<h1>Enrrutado</h1>'

@app.route("/enrrutamiento/<protocolo>",methods=["GET"])
def enrrutamiento(protocolo):
    # Extraemos el registro de enrrutamientos
    enrrutamiento = Enrrutamiento.query.get('1')
    # Verificamos si no ha sido enrrutado anteriormente
    if enrrutamiento.primero == protocolo or enrrutamiento.segundo == protocolo or enrrutamiento.tercero == protocolo:
        return f'<h1>{protocolo} ya configurado</h1>'


    routers = Router.query.all()
    interfaces = Interface.query.all()
    # levantamos el nuevo enrrutamiento
    for router in routers:
        # y tomamos la direccion ip de cualqueira de sus interfaces
        ip = extraccion_ip_interfaz(router)
        cliente_telnet = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        cliente_telnet.connect((ip,23))
        cliente_telnet.recv(1024)
        cliente_telnet.send("admin\n".encode())
        cliente_telnet.recv(1024)
        cliente_telnet.send("admin\n".encode())
        cliente_telnet.recv(1024)
        cliente_telnet.send("enable\n".encode())
        cliente_telnet.recv(1024)
        cliente_telnet.send("admin\n".encode())
        network = []
        # Extraemos las redes a configurar
        for interfaz in interfaces:
            if interfaz.dispositivoa == router.id or interfaz.dispositivob == router.id:
                network.append(interfaz.ip)

        if protocolo == 'RIP':
            comando = E.Enrrutamiento.activar_rip(network)
        elif protocolo == 'OSPF':
            comando = E.Enrrutamiento.activar_ospf(network)
        elif protocolo == 'EIGRP':
            comando = E.Enrrutamiento.activar_eigrp(network)

        cliente_telnet.recv(1024).decode()
        cliente_telnet.send(comando.encode())
        time.sleep(3)
        res = cliente_telnet.recv(2048).decode()
        print(str(res).replace("\\n","\n").replace("\\r","\r"))

        cliente_telnet.send("exit".encode())
        cliente_telnet.close()
    enrrutamiento = Enrrutamiento.query.get('1')
    #Agregamos el nuevo enrrutamiento con su respectivo nuemro
    enrrutamiento=asignacion_posicion_enrrutamiento(enrrutamiento,protocolo)
    db.session.commit()
    return f'<h1>{protocolo} levantado</h1>'


# --------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------

# Levantamos enrrutamiento
@app.route("/enrrutamiento/<protocolo>/baja",methods=["GET"])
def baja_enrrutamiento(protocolo):
    # Verificamos que el enrrutamiento este levantado y no sea el unico
    # ya que por defecto debe haber levantado uno siempre
    enrrutamiento = Enrrutamiento.query.get('1')
    # Verificamos que el protocolo este levantado en cualquier posicion
    if enrrutamiento.primero == protocolo or enrrutamiento.segundo == protocolo or enrrutamiento.tercero == protocolo:
        # Verificamos que exista pro lo menos un segundo enrrutamiento, de no existir retornamos un mensaje
        if enrrutamiento.segundo == None:
            return f'<h1>no se pudo desactivar el protocolo {protocolo} ya que es el unico</h1>'
    routers = Router.query.all()
    # Damos de baja el enrrutamiento    
    for router in routers:
        # y tomamos la direccion ip de cualqueira de sus interfaces
        ip = extraccion_ip_interfaz(router)
        cliente_telnet = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        cliente_telnet.connect((ip,23))
        cliente_telnet.recv(1024)
        cliente_telnet.send("admin\n".encode())
        cliente_telnet.recv(1024)
        cliente_telnet.send("admin\n".encode())
        cliente_telnet.recv(1024)
        cliente_telnet.send("enable\n".encode())
        cliente_telnet.recv(1024)
        cliente_telnet.send("admin\n".encode())
        
        cliente_telnet.recv(1024)
        if protocolo == 'RIP':
            comando = E.Enrrutamiento.desactivar_rip()
        elif protocolo == 'OSPF':
            comando = E.Enrrutamiento.desactivar_ospf()
        elif protocolo == 'EIGRP':
            comando = E.Enrrutamiento.desactivar_eigrp()
        
        cliente_telnet.send(comando.encode())
        time.sleep(3)
        res = cliente_telnet.recv(2048).decode()
        print(str(res).replace("\\n","\n").replace("\\r","\r"))

        cliente_telnet.send("exit".encode())
        cliente_telnet.recv(1024)
        cliente_telnet.close()
    #Cambiamos la posocion de los enrrutamientos en la bd
    enrrutamiento = reasignacion_posicion_enrrutamiento(enrrutamiento,protocolo)
    db.session.commit()
    return f'<h1>Se dio de baja el protocolo {protocolo}</h1>'


# --------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------

# Mostramos protocolos levantados
@app.route("/enrrutamiento",methods=["GET"])
def protocolo_enrrutamiento():
    enrrutamiento = Enrrutamiento.query.get('1')
    return render_template("enrrutamiento.html", enrrutamiento=enrrutamiento)

# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------SSH---------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------

@app.route("/ssh/<id>",methods=["GET"])
@app.route("/ssh/<id>/<username>/<password>",methods=["GET"])
def levantar_ssh(id,username="admin",password="admin"):
    '''
    levantar_ssh realiza el cambio de la configuracion telnet a una configuracion ssh
    recibe como parametros el id del router a configurar
    y opcinalmente el username y password que se desa configurar, por defecto estas dos
    son admin
    '''
    # Primero extraemos el router a configurar de la bd
    router = Router.query.get_or_404(id)
    # y tomamos la direccion ip de cualqueira de sus interfaces
    ip = extraccion_ip_interfaz(router)
    # En caso de que no encuentre una direccion ip valida, devolvera una cadena vacia
    # lo cual en python es un valor falso
    if not(ip):
        return '<h1>Configuracion ssh no realizada</h1>'
    # Mandamos a llamar al metodo estatico levantar ssh de la clase SSH
    if SSH.levantar_ssh(ip,username,password):
        # En caso de que todo sea correcto se hace el cambio del tipo de conexion
        conexion=Conexion.query.get_or_404(id)
        conexion.tipo="SSH"
        db.session.commit()
        return f'<h1>Configuracion ssh realizada</h1>'
    else:
        return '<h1>Configuracion ssh no realizada</h1>'


# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# --------------------------------------Telnet--------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------

@app.route("/telnet/<id>",methods=["GET"])
@app.route("/telnet/<id>/<username>/<password>",methods=["GET"])
def levantar_telnet(id,username="admin",password="admin"):
    '''
    levantar_telnet realiza el cambio de la configuracion ssh a una configuracion telnet
    recibe como parametros el id del router a configurar
    y opcinalmente el username y password que se desa configurar, por defecto estas dos
    son admin
    '''
    # Primero extraemos el router a configurar de la bd
    router = Router.query.get_or_404(id)
    # y tomamos la direccion ip de cualqueira de sus interfaces
    ip = extraccion_ip_interfaz(router)
    # En caso de que no encuentre una direccion ip valida, devolvera una cadena vacia
    # lo cual en python es un valor falso
    if not(ip):
        return '<h1>Configuracion telnet no realizada</h1>'
    # Mandamos a llamar al metodo estatico levantar ssh de la clase SSH
    if Telnet.levantar_telnet(ip,username,password):
        # En caso de que todo sea correcto se hace el cambio del tipo de conexion
        conexion=Conexion.query.get_or_404(id)
        conexion.tipo="telnet"
        db.session.commit()
        return f'<h1>Configuracion telnet realizada</h1>'
    else:
        return '<h1>Configuracion telnet no realizada</h1>'

# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------SNMP-------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------
@app.route("/snmp",methods=["GET"])
def snmp():
    routers = Router.query.all()
    interfaces = Interface.query.all()
    # levantamos snmp
    for router in routers:
        # y tomamos la direccion ip de cualqueira de sus interfaces
        ip = extraccion_ip_interfaz(router)
        cliente_telnet = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        cliente_telnet.connect((ip,23))
        cliente_telnet.recv(1024)
        cliente_telnet.send("admin\n".encode())
        cliente_telnet.recv(1024)
        cliente_telnet.send("admin\n".encode())
        cliente_telnet.recv(1024)
        cliente_telnet.send("enable\n".encode())
        cliente_telnet.recv(1024)
        cliente_telnet.send("admin\n".encode())
        network = []
        # Extraemos las redes a configurar
        for interfaz in interfaces:
            if interfaz.dispositivoa == router.id or interfaz.dispositivob == router.id:
                network.append(interfaz.ip)

        comando = "config t\n"
        comando += "snmp-server community public ro v2c\n"
        comando += "snmp-server enable traps\n"
        comando += "snmp-server host 10.0.1.2 public\n"
        comando += "end\n"
        comando += "wr\n"

        cliente_telnet.recv(1024).decode()
        cliente_telnet.send(comando.encode())
        time.sleep(3)
        res = cliente_telnet.recv(2048).decode()
        print(str(res).replace("\\n","\n").replace("\\r","\r"))

        cliente_telnet.send("exit".encode())
        cliente_telnet.close()
    return f'<h1>snmp levantado</h1>'



cmdGen = cmdgen.CommandGenerator()



community = 'public'

# Hostname OID
host_OID = '1.3.6.1.2.1.1.1.0'

# Interface OID
interface_OID = '1.3.6.1.2.1.2.2.1.11.1'

@app.route("/monitorear/<interface>",methods=['GET'])
@app.route("/monitorear/<interface>/<int:periodo>",methods=['GET'])
def monitorear(interface,periodo=30):
    os.remove("resultados.txt")
    hilo = Worker()
    hilo.start()
    while True:
        Monitoreo.grabar(interface,community,host_OID,interface_OID)
        time.sleep(periodo) 


@app.route("/graficar")
def graficar():
    x_time = []
    in_packets = []
    ant_in_packets = 0
    paquetes = 0    
    estado = True
    caidas = []
    with open('resultados.txt', 'r') as f:
        for line in f.readlines():
            line = eval(line)
            if (len(x_time) == 0):
                x_time.append(line['Tiempo'])
                ant_in_packets=float(line['Fa0-0_In_uPackets'])
                in_packets.append(10)
                estado = True
            else:   
                x_time.append(line['Tiempo'])
                if line['Fa0-0_In_uPackets'] is None :
                    in_packets.append(0)
                    #Si el estado anterior es True quiere decir que la
                    #la interface esta apagada o caida
                    if estado:
                        caidas.append(line['Tiempo'])
                        estado = False
                else:
                    
                    paquetes=float(line['Fa0-0_In_uPackets'])-ant_in_packets
                    if paquetes > 0:
                        in_packets.append(paquetes)
                        ant_in_packets=float(line['Fa0-0_In_uPackets'])
                    else:
                        in_packets.append(in_packets[-1])
                    if estado:
                        estado = True
                    else:
                        #si el estado anterior es falso esto quiere decir que
                        #que la interface fue encendida o leventada
                        estado = True
                        caidas.append(line['Tiempo'])
    
    plt.plot(x_time,in_packets)
    for i in caidas:
        plt.vlines(i,0,80)
    plt.savefig("static/IMG/grafica.png")
    time.sleep(1)
    grafica = os.path.join(app.config['UPLOAD_FOLDER'], 'grafica.png')
    return render_template("grafica.html", image=grafica)
