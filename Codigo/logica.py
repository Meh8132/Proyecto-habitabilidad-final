import math
from pythermalcomfort.models import athb
from pythermalcomfort.utilities import v_relative, clo_dynamic

adj_matrix = [
    [0, 0.9, 0, 1, 0, 1.1, 0, 0, 0, 0, 0.9, 1, 0.95, 0, 0, 0, 0, 0, 0],
    [0.9, 0, 0.95, 0.95, 0, 0, 1.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0.95, 0, 0, 0, 0, 1, 1.1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0.95, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 1, 1, 1, 1.1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [1.1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1.1, 0, 0, 1, 0, 0, 0, 0],
    [0, 1.1, 1, 0, 1, 1, 0, 0, 1, 1.1, 0, 0, 0, 1, 0, 1, 0, 0, 0],
    [0, 0, 1.1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0.95, 0, 1.1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1.1, 0, 0, 0],
    [0, 0, 1, 0, 1, 0, 1.1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0.9, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1.1, 0, 0, 0, 0, 1, 0, 0],
    [1, 0, 0, 0, 1.1, 1.1, 0, 0, 0, 0, 1.1, 0, 1, 0, 0, 0, 0, 1, 0],
    [0.95, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1.1],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1.1, 0, 0, 0, 0, 0, 0, 0, 1.1, 0, 1.1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1.1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.1, 0, 0, 0, 1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0]
]

# Indice, Area (m2), X, Y

zone_dictionary = {
    "Garaje": [0, 85, 467, 461],
    "Pasillo": [1, 15, 298, 460],
    "Lobby entrada": [2, 30, 123, 454],
    "Escalera segundo piso": [3, 10, 364, 369],
    "Lobby segundo piso": [4, 20, 336, 284],
    "Cocina": [5, 20, 382, 217],
    "Salón social": [6, 30, 268, 226],
    "Habitación 201": [7, 10, 31, 280],
    "Habitación 202": [8, 10, 88, 245],
    "Habitación 203": [9, 10, 156, 210],
    "Habitación 204": [10, 10, 472, 224],
    "Habitación 205": [11, 10, 520, 257],
    "Habitación 206": [12, 10, 567, 293],
    "Escalera tercer piso": [13, 10, 294, 156],
    "Lobby tercer piso": [14, 25, 285, 46],
    "Terraza": [15, 45, 151, 58],
    "Habitación 301": [16, 20, 393, 38],
    "Habitación 302": [17, 20, 480, 60],
    "Habitación 303": [18, 20, 554, 107]
}

# Calculo de la temperatura radiante

def calc_tr(temp, zone):

    adj_temp_sum = 0
    adj_zones = 0
    avg_temp = 0
    zone_area = zone_dictionary.get(zone)[1]
    index = zone_dictionary.get(zone)[0]

    for i in adj_matrix[index]:
        
        if i != 0:
            adj_zones += 1
            adj_temp_sum += i*temp
    
    avg_temp = adj_temp_sum/adj_zones

    return avg_temp*(math.log(zone_area, 0.001)+1.5)


def calc_athb(temp, wind_v, r_hum, met_r, zone):
    
    v_r = v_relative(v=wind_v, met=met_r)

    athb_result = athb(
        tdb = temp, 
        tr = calc_tr(temp, zone),
        vr = v_r,
        rh = r_hum,
        met = met_r,
        t_running_mean = temp
    )

    return athb_result



    

