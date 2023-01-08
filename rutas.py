import networkx as  nx
def rutas(G,id):
    '''
    Rutas permite obtener la ruta a cada uno de los routers de la topoligia, partiendo del
    dispositivo especificado en el parametro id
    '''
    # Calculamos los caminos mas cortos de punto especificado al resto de los nodos
    camino_corto = nx.single_source_shortest_path(G,id)
    # Solo nos importan los caminos de la maquina virtual a los routers, por lo que excluimos
    # las llaves que contengan la subcadena PC
    rutas = {}
    for llave,valor in camino_corto.items():
        if llave[:2] != "PC":
            rutas[llave]=valor
    # Extraemos las direcciones ip entre cada par de nodos
    dir_ip = nx.get_edge_attributes(G, "IP")
    # cambiamos los valores del nombre de los nodos al valor de cada arista
    # cambiamos el ultimo octeto debido a que la interfaz de entrada llendo
    # de la PCMV al culaquier router siempre sera la primera direccion valida (.1)
    # y la de salida, llendo de la PCMV al router simepres sera la segundo (.2)
    tmp = []
    for llave,camino in rutas.items():
        aux = []
        for i in range(len(camino)-1):
            # El bloque try-except se agrego debido a que el programa busca especificamente
            # el mismo orden en que se ingresaron los nodos y en caso de no encotrar ese orden
            # ocacionara un error
            try:
                tmp = dir_ip[camino[i],camino[i+1]].split(".")
            except:
                tmp = dir_ip[camino[i+1],camino[i]].split(".")
            tmp[-1] = "1"
            aux.append(".".join(tmp))
        # Cambiamos los valores del diccionario 
        rutas[llave]=aux
    # Ahora rutas continene un lista con las direcciones 
    return rutas