from flask import Flask,request,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from fucionesDatos import asignacion_direcciones_interfaz
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
    _tablename_='router'
    id = db.Column(db.Integer,primary_key=True)
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
        self.f0_0=data['f0_0']
        self.f1_0=data['f1_0']
        self.f1_1=data['f1_1']
        self.f2_0=data['f2_0']
        self.f2_1=data['f2_1']
        self.f3_0=data['f3_0']
        self.f3_1=data['f3_1']
        self.f4_0=data['f4_0']
        self.f4_1=data['f4_1']
        self.f5_0=data['f5_0']
        self.f5_1=data['f5_1']
        self.f6_0=data['f6_0']
        self.f6_1=data['f6_1']

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
    routera=db.Column(db.Integer,db.ForeignKey('router.id'))
    routerb=db.Column(db.Integer,db.ForeignKey('router.id'))
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
    # Agragamos el objeto interface a la base de datos
    db.session.add(interface)
    # Agregamos las direcciones a cada extremo de la interfaes
    # Recuperamos los objetos router de cada uno de los extremos de la conexion
    routera=Router.query.get(interface.routera)
    routerb=Router.query.get(interface.routerb)
    # la funcion asignacion_direcciones_interfaz asigna las ip validas a la intefaz correspondiente
    asignacion_direcciones_interfaz(routera,routerb,interface.interfaz,interface.ip)
    # Hacemos el commit de los cambios
    db.session.commit()
    return f'<h1>Interface agregada</h1>'

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
@app.route("/interface/<int:ip>",methods=["DELETE"])
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

@app.route("/topologia",methods=['GET'])
def generar_topologia():
    G = nx.Graph()
    interfaces = Interface.query.all()
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
    plt.savefig("static/IMG/topologia.png")
    time.sleep(1)
    topologia = os.path.join(app.config['UPLOAD_FOLDER'], 'topologia.png')
    return render_template("topologia.html", image=topologia)

