import pandas
import math

# Obtendo dados do problema
dir_dist = pandas.read_csv('dir_dist.csv', header=None)
real_dist = pandas.read_csv('real_dist.csv', header=None)
lines = pandas.read_csv('lines.csv', header=None)  
# print(dir_dist)
# print(real_dist)
# print(lines)


def dist_km_to_minutes(dist):
    for i in range(14):
        for j in range(14):    
            # a velocidade média de um trem é de 30km/h -> 1km/2min
            dist[i][j] = dist[i][j]*2.0
            
    return dist

# Convertendo dados do problema de km pra minutos 
dir_dist = dist_km_to_minutes(dir_dist)
real_dist = dist_km_to_minutes(real_dist)
# print(dir_dist)
# print(real_dist)


def valid_station(str_station):
    if str_station[0] == "E" and str_station[1:].isnumeric():
        if int(str_station[1:]) >= 1 and int(str_station[1:]) <= 14:
            return True
    
    print("Estação invalida")
    return False


def get_station(req_station):
    is_valid = False
    while not is_valid:
        print("Estações: E1 - E2 - E3 - E4 - E5 - E6 - E7",
              "- E8 - E9 - E10 - E11 - E12 - E13 - E14")
        print(req_station)
        str_station = input()

        is_valid = valid_station(str_station)
    
    return str_station
    

str_s_station = get_station("Em qual estação você se encontra?")
str_d_station = get_station("Qual a estação de destino?")

# Convertendo a estação pra indice pra facilitar consulta
s_station = int(str_s_station[1:]) - 1
d_station = int(str_d_station[1:]) - 1
    
    
def get_connected_stations(station, marked_stations):
    connected_stations=[]
    for con, dist in enumerate(real_dist[station]):
        if not math.isnan(dist):
            connected_stations.append(con)
    # Remove estações que já foram percorridas no caminho
    connected_stations = list(
            filter(lambda station: station not in marked_stations, 
                   connected_stations))
    return(connected_stations)


# h
def estimate_dist(target, destiny):
    if target == destiny:
        return 0
    return dir_dist[target][destiny]


# g
def covered_dist(current, target, covered_path):
    c_dist = 0
    line = ""
    if len(covered_path) > 0:
        line = lines[covered_path[0][0]][covered_path[0][1]]
    
    for edge in covered_path:
        c_dist += real_dist[edge[0]][edge[1]]
        newline = lines[edge[0]][edge[1]]
        
        if newline != line:
            line = newline
            # o tempo gasto para fazer baldeação é de 4 minutos
            c_dist += 4
            
    c_dist += real_dist[current][target]
    newline = lines[current][target]
    
    if newline != line and line != "":
        # o tempo gasto para fazer baldeação é de 4 minutos
        c_dist += 4
        
    line = newline
    return c_dist, line

def expand_border(current, destiny, border, covered_path, marked_stations):
    connected_stations = get_connected_stations(current, marked_stations)
    
    newborder = border
    for station in connected_stations:
        # Calcula a função de avaliação do A*
        c_dist, curline = covered_dist(current, station, covered_path)
        e_dist = estimate_dist(station, destiny)
        
        f = round(c_dist + e_dist, 1)
        g = round(c_dist, 1)
        h = round(e_dist, 1)
        
        # Adiciona o caminho e as estações visitadas para cada nó na fronteira
        new_path = covered_path + [[current, station]]
        new_m_stations = marked_stations
        new_m_stations.add(current)
        newborder.append([station, curline, f, g, h, new_path, new_m_stations])

    # Ordena pela função de avaliação
    newborder = sorted(newborder, key=lambda x: x[2])
    return newborder


def print_iter(border):
        it_border = ""
        for e in border:
            station = "E"+ str(e[0]+1)
            line = e[1]
            f = str(e[2])
            g = str(e[3])
            h = str(e[4])
            it_border+= "("+station+" "+line+" "+ f +" "+ g + " "+ h + "), "
            # print(e[5])
        print(it_border)
        

 
def astar(current, destiny, border):
    # Obtém o caminho que foi percorrido até a estação atual
    covered_path = border[0][5]
    
    if current != destiny:
        marked_stations = border[0][6]
        border = border[1:]
        
        border = expand_border(current, destiny, border, 
                                   covered_path, marked_stations)
        print_iter(border)
        
        current = border[0][0]
        astar(current, destiny, border)
    else:
        print("Trajeto mais rápido")
        fast_path = ""
        for ride in covered_path:
            fast_path+="E"+str(ride[0]+1)+" - "
        
        fast_path += "E"+str(covered_path[-1][1]+1)
        
        print(fast_path)

f = dir_dist[s_station][d_station]
g = 0
h = dir_dist[s_station][d_station]
covered_path = []
marked_stations = set()
border = [[s_station, "", f, g, h, covered_path, marked_stations]]
astar(s_station, d_station, border)