from flask import Flask,request,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from funcionesDatos import asignacion_direcciones_interfaz
from conexionTelnet import enrrutamineto_telnet
import rutas as r
import networkx as nx
import matplotlib.pyplot as plt
import time
import os
import socket


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

# -----------------------------------Usuarios-----------------------------------
class Conexion(db.Model):
    _tablename_='conexion'
    id = db.Column(db.String(64),primary_key=True)
    tipo = db.Column(db.String(64))

    def set_data(self,data):
        self.id=data['id']
        self.tipo=data['tipo']


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
    return '<h1>Enrrutado</h1>'

@app.route("/enrrutar/<protocolo>/<id>",methods=["DELETE"])
def desenrrutar(protocolo):
    '''
    Es el endpoint encargado de realizar la baja del enrrutamiento dinamico especificado
    comenzando desdesde el dispoositivo indicado
    '''
    pass