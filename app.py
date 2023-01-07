from flask import Flask,request,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from funcionesDatos import asignacion_direcciones_interfaz
from Enrrutamiento import Enrrutamiento
import networkx as nx
import matplotlib.pyplot as plt
import time
import os



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
        self.f0_0=None
        self.f1_0=None
        self.f1_1=None
        self.f2_0=None
        self.f2_1=None
        self.f3_0=None
        self.f3_1=None
        self.f4_0=None
        self.f4_1=None
        self.f5_0=None
        self.f5_1=None
        self.f6_0=None
        self.f6_1=None

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
        
# -----------------------------------Interface-----------------------------------
# El modelo interfaces
class Interface(db.Model):
    _tablename_='interface'
    ip = db.Column(db.String(64),primary_key=True)
    routera=db.Column(db.String(64),db.ForeignKey('router.id'))
    routerb=db.Column(db.String(64),db.ForeignKey('router.id'))
    interfaz=db.Column(db.String(64))

    def set_data(self,data):
        self.ip=data['ip']
        self.routera=data['routera']
        self.routerb=data['routerb']
        self.interfaz=data['interfaz']

    def get_data(self):
        return {
            'ip':self.ip,
            'routera':self.routera,
            'routerb':self.routerb,
            'interfaz':self.interfaz
        }

# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# -----------------------------------Endpoints-----------------------------------
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------



# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
# -------------------------------------CRUDs-------------------------------------
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# -----------------------------------Usuarios-----------------------------------
# ------------------------------------------------------------------------------


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
    db.session.commit()
    return f'<h1>Router agregado</h1>'

# Listar todos los routers
@app.route("/router/<int:id>",methods=["GET"])
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
@app.route("/router/<int:id>",methods=["DELETE"])
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
            if interface.routera == router.id or interface.routerb == router.id:
                eliminar_interface(interface.ip)
    db.session.commit()
    return f'<h1>Rourter eliminado</h1>'

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
    # Recuperamos los objetos router de cada uno de los extremos de la conexion
    routera=Router.query.get(interface.routera)
    routerb=Router.query.get(interface.routerb)
    # la funcion asignacion_direcciones_interfaz asigna las ip validas a la intefaz correspondiente
    # Y devuelve una cadena con el estado de la asgignacion
    estado = asignacion_direcciones_interfaz(routera,routerb,interface.interfaz,interface.ip)
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
        G.add_edge("R"+str(interface.routera),"R"+str(interface.routerb),weight=interface.ip)
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

# ----------------------------------------RIP---------------------------------------

@app.route("/activarRIP/<ip>/<int:id>",methods=['GET'])
def activar_rip(ip,id):
    '''
    Los argumetos recibidos son la direccion ip de la interface a la que nos conectareos
    por ssh para realizar la debida configuracion y el id del router a configurar
    '''
    # Extraemos todas las interfaces de la bd
    interfaces = Interface.query.all()
    interfacesIP = []
    for interface in interfaces:
        if interface.routera == id or interface.routerb == id:
            interfacesIP.append(interface)
    Enrrutamiento.activar_rip(ip,interfacesIP)
    return f'<h1>RIP activado en el router {id}</h1>'

@app.route("/desactivarRIP/<ip>",methods=['GET'])
def desactivar_rip(ip):
    '''
    El argumento recibido es la direccion ip de la interface del router que vamos a configurar
    por ssh
    '''
    Enrrutamiento.desactivar_rip(ip)
    return f'<h1>RIP desactivado en el router {id}</h1>'

# ---------------------------------------EIGRP--------------------------------------

@app.route("/activarEIGRP/<ip>/<int:id>",methods=['GET'])
def activar_eigrp(ip,id):
    '''
    Los argumetos recibidos son la direccion ip de la interface a la que nos conectareos
    por ssh para realizar la debida configuracion y el id del router a configurar
    '''
    # Extraemos todas las interfaces de la bd
    interfaces = Interface.query.all()
    interfacesIP = []
    for interface in interfaces:
        if interface.routera == id or interface.routerb == id:
            interfacesIP.append(interface)
    Enrrutamiento.activar_eigrp(ip,interfacesIP)
    return f'<h1>RIP activado en el router {id}</h1>'

@app.route("/desactivarEIGRP/<ip>",methods=['GET'])
def desactivar_eigrp(ip):
    '''
    El argumento recibido es la direccion ip de la interface del router que vamos a configurar
    por ssh
    '''
    Enrrutamiento.desactivar_eigrp(ip)
    return f'<h1>RIP desactivado en el router {id}</h1>'

# ---------------------------------------OSPF---------------------------------------

@app.route("/activarOSPF/<ip>/<int:id>",methods=['GET'])
def activar_ospf(ip,id):
    '''
    Los argumetos recibidos son la direccion ip de la interface a la que nos conectareos
    por ssh para realizar la debida configuracion y el id del router a configurar
    '''
    # Extraemos todas las interfaces de la bd
    interfaces = Interface.query.all()
    interfacesIP = []
    for interface in interfaces:
        if interface.routera == id or interface.routerb == id:
            interfacesIP.append(interface)
    Enrrutamiento.activar_ospf(ip,interfacesIP)
    return f'<h1>RIP activado en el router {id}</h1>'

@app.route("/desactivarOSPF/<ip>",methods=['GET'])
def desactivar_ospf(ip):
    '''
    El argumento recibido es la direccion ip de la interface del router que vamos a configurar
    por ssh
    '''
    Enrrutamiento.desactivar_ospf(ip)
    return f'<h1>RIP desactivado en el router {id}</h1>'