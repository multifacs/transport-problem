import os
import psutil
import copy
import random
import tracemalloc

# inner psutil function
def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss

def northwest_corner(g, s, d):
    # делаем копии данных, чтобы не изменять изначальные
    grid = copy.deepcopy(g)
    supply = list(s)
    demand = list(d)

    startR = 0  # стартовая строка
    startC = 0  # стартовая колонка
    ans = 0
    # цикл выполняется до тех пор, пока не достигнет правого нижнего угла
    counter = 0

    tracemalloc.start()

    while (startR != len(grid) and startC != len(grid[0])):
        counter += 1
        # если спрос превышает предложение
        if (supply[startR] <= demand[startC]):
            ans += supply[startR] * grid[startR][startC]
            # вычесть величину предложения из величины спроса
            demand[startC] -= supply[startR]
            startR += 1
        # если предложение превышает спрос
        else:
            ans += demand[startC] * grid[startR][startC]
            # вычесть величину спроса из величины предложения
            supply[startR] -= demand[startC]
            startC += 1

    max_mem = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    return max_mem

def least_cost_cell(g, s, d):
    # делаем копии данных, чтобы не изменять изначальные
    grid = copy.deepcopy(g)
    supply = list(s)
    demand = list(d)

    # вычеркнутые строки и столбцы
    visited_rows = []
    visited_cols = []

    ans = 0

    # переменные для нахождения минимальной ячейки
    least_row = 0
    least_col = 0
    least_cell = grid[0][0]
    counter = 0
    loop_counter = 0
    # в цикле пока спрос и предлодение не станут равны 0

    tracemalloc.start()

    while (sum(supply) + sum(demand) != 0):
        counter += 1
        loop_counter += 1
        if counter > 1000:
            ans = 0
            break
        # проходим по таблице и ищем минимальную ячейку
        for i in range(len(grid)):
            loop_counter += 1
            # исключая вычеркнутые строки
            if i in visited_rows:
                continue
            for j in range(len(grid[0])):
                loop_counter += 1
                # и столбцы
                if j in visited_cols:
                    continue

                cell = grid[i][j]
                if cell < least_cell:
                    least_cell = cell
                    least_row = i
                    least_col = j

        # записываем данные минимальной ячейки
        supply_val = supply[least_row]
        demand_val = demand[least_col]
        min_val = min(supply_val, demand_val)

        # сразу прибавляем в ответ
        ans += grid[least_row][least_col] * min_val

        # записываем данные в таблицу
        grid[least_row][least_col] = min_val
        supply[least_row] -= min_val
        demand[least_col] -= min_val

        # вычеркиваем строку или столбец если предложение или спрос занулились
        if supply[least_row] == 0:
            visited_rows.append(least_row)
        else:
            visited_cols.append(least_col)

        least_cell = min_val

    max_mem = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    return max_mem

def vogels_approximation(g, s, d):
    grid = copy.deepcopy(g)
    supply = list(s)
    demand = list(d)

    INF = 10**3
    n = len(grid)
    m = len(grid[0])
    ans = 0

    loop_counter = 0

    # вспомогательная функция для нахождения разности строк и разности столбцов
    def findDiff(grid):
        t = 0
        rowDiff = []
        colDiff = []
        for i in range(len(grid)):
            t += 1

            arr = grid[i][:]
            arr.sort()
            rowDiff.append(arr[1]-arr[0])
        col = 0
        while col < len(grid[0]):
            t += 1

            arr = []
            for i in range(len(grid)):
                t += 1
                arr.append(grid[i][col])
            arr.sort()
            col += 1
            colDiff.append(arr[1]-arr[0])
        return rowDiff, colDiff, t

    # цикл выполняется до тех пор, пока спрос и предложение не будут исчерпаны
    counter = 0

    tracemalloc.start()

    while max(supply) != 0 or max(demand) != 0:
        counter += 1
        loop_counter += 1
        if counter > 500:
            return 0, 0
        # нахождение разности строк и столбцов
        row, col, t = findDiff(grid)
        loop_counter += t
        # нахождение максимального элемента в массиве разности строк
        maxi1 = max(row)
        # нахождение максимального элемента в массиве разностей столбцов
        maxi2 = max(col)

        # если элемент row diff max больше или равен элементу col diff max
        if (maxi1 >= maxi2):
            for ind, val in enumerate(row):
                loop_counter += 1
                if (val == maxi1):
                    # нахождение минимального элемента в индексе таблицы, где был найден максимум в разности строк
                    mini1 = min(grid[ind])
                    for ind2, val2 in enumerate(grid[ind]):
                        loop_counter += 1
                        if (val2 == mini1):
                            # вычисление минимума спроса и предложения в данной строке и столбце
                            mini2 = min(supply[ind], demand[ind2])
                            ans += mini2 * mini1
                            # вычитание минимума из спроса и предложения
                            supply[ind] -= mini2
                            demand[ind2] -= mini2
                            # если спрос меньше, то всему столбцу присваивается максимальное значение, так что столбец исключается для следующей итерации
                            if (demand[ind2] == 0):
                                for r in range(n):
                                    loop_counter += 1
                                    grid[r][ind2] = INF
                            # если предложение меньше, то всему ряду присваивается максимальное значение, так что ряд исключается для следующей итерации
                            else:
                                grid[ind] = [INF for i in range(m)]
                            break
                    break
        # если элемент row diff max больше элемента col diff max
        else:
            for ind, val in enumerate(col):
                loop_counter += 1
                if (val == maxi2):
                    # нахождение минимального элемента в индексе таблицы, где максимум был найден в разности столбцов
                    mini1 = INF
                    for j in range(n):
                        loop_counter += 1
                        mini1 = min(mini1, grid[j][ind])

                    for ind2 in range(n):
                        loop_counter += 1
                        val2 = grid[ind2][ind]
                        if val2 == mini1:
                            # вычисление минимума спроса и предложения в данной строке и столбце
                            mini2 = min(supply[ind2], demand[ind])
                            ans += mini2 * mini1
                            # вычитание минимума из спроса и предложения
                            supply[ind2] -= mini2
                            demand[ind] -= mini2
                            # если спрос меньше, то всему столбцу присваивается максимальное значение, так что столбец исключается для следующей итерации
                            if (demand[ind] == 0):
                                for r in range(n):
                                    loop_counter += 1
                                    grid[r][ind] = INF
                            # если предложение меньше, то всей строке присваивается максимальное значение, так что строка исключается для следующей итерации
                            else:
                                grid[ind2] = [INF for i in range(m)]
                            break
                    break

    max_mem = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    return max_mem


def generate_transport_problem(n, m, cost_lim=15):
    grid = []
    supply = []
    demand = []

    # заполняем массивы спроса и предложения случайными числами
    for i in range(n):
        supply.append(int(random.random() * 20) * 50 + 50)
    for i in range(m):
        demand.append(int(random.random() * 15) * 50 + 50)

    # находим суммы
    sum_supply = sum(supply)
    sum_demand = sum(demand)

    # если сумма спроса получилась больше суммы предложения
    if (sum_demand > sum_supply):
        # находим разницу, которую нужно прибавить
        diff = sum_demand - sum_supply
        part = int(diff / n)
        rem = diff - part * n
        # и прибавляем в цикле
        for i in range(n):
            supply[i] += part
        supply[0] += rem
    # аналогично, если предложение больше спроса
    else:
        diff = sum_supply - sum_demand
        part = int(diff / m)
        rem = diff - part * m

        for i in range(m):
            demand[i] += part
        demand[0] += rem

    # print(supply, sum(supply))
    # print(demand, sum(demand))

    # заполняем таблицу случайными стоимостями
    for i in range(n):
        grid.append([])
        for j in range(m):
            grid[i].append(int(random.random() * cost_lim + 1))
    # print(grid)
    return grid, supply, demand

 

n = 4
m = 5
grid, supply, demand = generate_transport_problem(n, m, cost_lim=15)

r1 = northwest_corner(grid, supply, demand)
r2 = least_cost_cell(grid, supply, demand)
r3 = vogels_approximation(grid, supply, demand)

print(r1)
print(r2)
print(r3)