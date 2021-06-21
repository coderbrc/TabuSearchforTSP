import math
import random
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pylab import mpl
mpl.rcParams['font.sans-serif'] = ['Tahoma']
#Yol mesafesini hesapla yani değerlendirme fonksiyonu
def calFitness(line, dis_matrix):
    dis_sum = 0
    dis = 0
    for i in range(len(line)):
        if i < len(line) - 1:
            dis = dis_matrix.loc[line[i], line[i + 1]]  #Mesafe hesaplama
            dis_sum = dis_sum + dis
        else:
            dis = dis_matrix.loc[line[i], line[0]]
            dis_sum = dis_sum + dis
    return round(dis_sum, 1)
def traversal_search(line, dis_matrix, tabu_list):
    traversal = 0  #Arama
    traversal_list = []
    traversal_value = []
    while traversal <= traversalMax:
        pos1, pos2 = random.randint(0, len(line) - 1), random.randint(0, len(line) - 1)  #
        #Geçerli yolu kopyala ve oluşturulan yolu güncelle
        new_line = line.copy()
        new_line[pos1], new_line[pos2] = new_line[pos2], new_line[pos1]
        new_value = calFitness(new_line, dis_matrix)  #Geçerli yol mesafesi
        if (new_line not in traversal_list) & (new_line not in tabu_list):
            traversal_list.append(new_line)
            traversal_value.append(new_value)
            traversal += 1
    return min(traversal_value), traversal_list[traversal_value.index(min(traversal_value))]
def greedy(CityCoordinates, dis_matrix,num=15):
    '''Greedy strateji yapısı başlangıç çözümü'''
    #Dis_matrix
    dis_matrix = dis_matrix.astype('float64')
    for i in range(num): dis_matrix.loc[i, i] = math.pow(10, 10)
    line = []
    now_city = random.randint(0, num)  #Rastgele bir şehir oluştur
    line.append(now_city)  #Yola mevcut şehri ekle
    dis_matrix.loc[:, now_city] = math.pow(10, 10)  #Mesafe matrisi güncelle
    for i in range(len(CityCoordinates) - 1):
        next_city = dis_matrix.loc[now_city, :].idxmin()  #Mesafesi en yakın şehir seçilir
        line.append(next_city)  # Add into the path
        dis_matrix.loc[:, next_city] = math.pow(10, 10)  #Mesafe matrisi güncelle
        now_city = next_city  #Mevcut şehri güncelle
    return line
#Sonuç diagramını çizdirdik
def draw_path(line, CityCoordinates):
    x, y = [], []
    for i in line:
        Coordinate = CityCoordinates[i]
        x.append(Coordinate[0])
        y.append(Coordinate[1])
    x.append(x[0])
    y.append(y[0])
    plt.plot(x, y, marker='o')
    plt.show()
if __name__ == '__main__':
    #parametreler
    CityNum = 51  #City quantity
    path = "coord.txt"
    cityPoints = []
    #TSParameter
    tabu_limit = 100  #Tabu listesi uzunluğu
    iterMax = 50
    traversalMax = 20  #Her nesil için kısmi arama numarası
    tabu_list = []  #table
    tabu_time = []
    best_value = math.pow(10, 10)  #En iyi çözümü depola
    best_line = []
    with open(path, "r") as f:
        for line in f.readlines():
            line = [float(x.replace("\n", "")) for x in line.split(" ")]
            cityPoints.append(line)
    #Şehirler arası mesafeler hesaplanır
    dis_matrix = pd.DataFrame(data=None, columns=range(len(cityPoints)), index=range(len(cityPoints)))
    for i in range(len(cityPoints)):
        xi, yi = cityPoints[i][0], cityPoints[i][1]
        for j in range(len(cityPoints)):
            xj, yj = cityPoints[j][0], cityPoints[j][1]
            dis_matrix.iloc[i, j] = round(math.sqrt((xi - xj) ** 2 + (yi - yj) ** 2), 2)
    line = greedy(cityPoints, dis_matrix)
    value = calFitness(line, dis_matrix)
    best_value, best_line = value, line
    draw_path(best_line, cityPoints)
    best_value_list = []
    best_value_list.append(best_value)
    #Tabu tablosunu güncelle
    tabu_list.append(line)
    tabu_time.append(tabu_limit)
    iteration = 0
    while iteration <= iterMax:
        new_value, new_line = traversal_search(line, dis_matrix, tabu_list)
        if new_value < best_value:  #
            best_value, best_line = new_value, new_line  #En iyi çözümü güncelledik
            best_value_list.append(best_value)
        line, value = new_line, new_value  #Mevcut çözümü güncelledik
        #tabu tablasunu güncelle
        tabu_time = [x - 1 for x in tabu_time]
        if 0 in tabu_time:
            tabu_list.remove(tabu_list[tabu_time.index(0)])
            tabu_time.remove(0)
        tabu_list.append(line)
        tabu_time.append(tabu_limit)
        iteration += 1
    print(best_line)
    draw_path(best_line, cityPoints)
    plt.plot([i for i in range(len(best_line))], best_line)
    plt.ylabel("Fitness")
    plt.xlabel("Iteration")
    plt.show()
