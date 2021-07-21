import pandas
import math

dir_dist = pandas.read_csv('dir_dist.csv', header=None)
real_dist = pandas.read_csv('real_dist.csv', header=None)
lines = pandas.read_csv('lines.csv', header=None)


def dist_km_to_minutes(dist):
    for i in range(14):
        for j in range(14):    
            # a velocidade média de um trem é de 30km/h -> 1km/2min
            dist[i][j] = dist[i][j]*2
            
    # print(dist)
    return dist


def valid_station(str_station):
    if str_station[0] == "E" and str_station[1:].isnumeric():
        if int(str_station[1:]) >= 1 and int(str_station[1:]) <= 14:
            return str_station, True
    
    print("Estação invalida")
    return str_station, False
    
    
def get_connected_stations(station):
    connected_stations=[]
    for con, dist in enumerate(real_dist[station]):
        if not math.isnan(dist):
            # connected_stations.append((con,dist))
            connected_stations.append(con)
    
    # print(connected_stations)
    return(connected_stations)


def get_station(req_station):
    is_valid = False
    while not is_valid:
        print("Estações: E1 - E2 - E3 - E4 - E5 - E6 - E7 - E8 - E9 - E10 - E12 - E13 - E14")
        print(req_station)
        str_station = input()

        str_station, is_valid = valid_station(str_station)
    
    return str_station
    
    
# print(dir_dist)
dir_dist = dist_km_to_minutes(dir_dist)
# print(real_dist)
real_dist = dist_km_to_minutes(real_dist)
#print(lines)

str_s_station = get_station("Em qual estação você se encontra?")
str_d_station = get_station("Qual a estação de destino?")

# Convertendo a estação pra indice pra facilitar consulta
s_station = int(str_s_station[1:]) - 1
d_station = int(str_d_station[1:]) - 1
# print(s_station, d_station)

# h
def estimate_dist(target, destiny):
    if target == destiny:
        return 0
    return dir_dist[target][destiny]


# g
def covered_dist(current, target, covered_path):
    #print(covered_path)
    c_dist = 0
    line = lines[current][target]
    for edge in covered_path:
        c_dist += real_dist[edge[0]][edge[1]]
        newline = lines[edge[0]][edge[1]]
        #print(newline, edge[0], edge[1])
        if newline != line:
            line = newline
            # o tempo gasto para trocar de linha dentro de mesma estação (fazer baldeação) é de 4 minutos
            c_dist += 4
    c_dist += real_dist[current][target]
    #print(current, target, line)
    return c_dist, line

def expand_border(current, destiny, covered_path, border, marked_stations):
    connected_stations = get_connected_stations(current)
    connected_stations = list(filter(lambda station: station not in marked_stations, connected_stations))
    if len(connected_stations) == 0 and len(covered_path) > 0:
        covered_path.pop()
    newborder = border
    for station in connected_stations:
        c_dist, curline = covered_dist(current, station, covered_path)
        e_dist = estimate_dist(station, destiny)
        newborder.append([station, curline, c_dist+e_dist, c_dist, e_dist])

    newborder = sorted(newborder, key=lambda x: x[2])
    return newborder

    
def astar(destiny, border, covered_path, marked_stations):
    if border[0][0] != destiny:
        if len(covered_path) == 0:
            current = border[0][0]
        else:
            current = covered_path[-1][1]
        border = border[1:]
        
        border = expand_border(current, destiny, covered_path, border, marked_stations)
        it_border = ""
        for e in border:
            it_border+="(E"+ str(e[0]+1) + " " + e[1] + " " + str(e[2]) + " " + str(e[3]) + " " + str(e[4]) + ") "
        #print(it_border)
        if(len(covered_path) == 0):
            covered_path=[[current, border[0][0]]]
        else:
            covered_path.append([covered_path[-1][1], border[0][0]])
        marked_stations.add(current)
        astar(destiny, border, covered_path, marked_stations)
    else:
        print("Trajeto mais rápido")
        fast_path = ""
        for ride in covered_path:
            fast_path+="E"+str(ride[0]+1)+" - "
            # print("from E"+ str(ride[0]+1), "to E"+ str(ride[1]+1))
        fast_path += "E"+str(covered_path[-1][1]+1)
        
        print(fast_path)
        #print("GG")

# get_connected_stations(s_station)

border = [[s_station, "", dir_dist[s_station][d_station], 0, dir_dist[s_station][d_station]]]   
covered_path = [] 
marked_stations = set()
astar(d_station, border, covered_path, marked_stations)