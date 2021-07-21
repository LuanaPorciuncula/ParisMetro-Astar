import pandas

dir_dist = pandas.read_csv('dir_dist.csv', header=None)
real_dist = pandas.read_csv('real_dist.csv', header=None)
lines = pandas.read_csv('lines.csv', header=None)


def dist_km_to_minutes(dist):
    for i in range(14):
        for j in range(14):
            
            dist[i][j] = dist[i][j]*2
    # print(dist)
    return dist


def valid_station(str_station):
    if str_station[0] == "E" and str_station[1:].isnumeric():
        if int(str_station[1:]) >= 1 and int(str_station[1:]) <= 14:
            return str_station, True
    
    print("Estação invalida")
    return str_station, False
    
    
# print(dir_dist)
dir_dist = dist_km_to_minutes(dir_dist)

print(real_dist)
real_dist = dist_km_to_minutes(real_dist)     

# print (lines)

is_valid = False
while not is_valid:
    print("Estações: E1 - E2 - E3 - E4 - E5 - E6 - E7 - E8 - E9 - E10 - E12 - E13 - E14")
    print("Em qual estação você se encontra?")
    str_s_station = input()

    str_s_station, is_valid = valid_station(str_s_station)

is_valid = False
while not is_valid:
    print("Estações: E1 - E2 - E3 - E4 - E5 - E6 - E7 - E8 - E9 - E10 - E12 - E13 - E14")
    print("Qual a estação de destino?")
    str_d_station = input()

    str_d_station, is_valid = valid_station(str_d_station)
    
s_station = int(str_s_station[1:]) - 1
d_station = int(str_d_station[1:]) - 1

print(s_station, d_station)