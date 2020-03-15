import numpy as np

def game_core_v3(number, min_number, max_number):
    '''На каждой итерации уменьшаем интервал, в котором находится угадываемое число, вдвое.
       Определяем, в каком из подинтервалов находится загаданное число.
       Функция принимает загаданное число и возвращает число попыток'''
    count = 0
    predict = (min_number+max_number)//2 #находим середину интервала
    while number != predict:
        count+=1
        if number > predict: 
            min_number = predict + 1 #сдвигаем нижнюю границу интервала
        elif number < predict: 
            max_number = predict - 1 #сдвигаем верхнюю границу интервала
        predict = (min_number+max_number)//2
    return(count+1) # выход из цикла, если угадали

def score_game(game_core_v, iterations = 1000, min_number = 0, max_number = 100):
    '''Запускаем игру несколько раз (в зависимости от значения параметра iterations), 
        чтобы узнать, как быстро игра угадывает число в диапазоне, заданном в параметрах min_number, max_number'''
    count_ls = []
    np.random.seed(1)  # фиксируем RANDOM SEED, чтобы ваш эксперимент был воспроизводим!
    random_array = np.random.randint(min_number, max_number, size=(iterations))
    for number in random_array:
        count_ls.append(game_core_v(number, min_number, max_number))
    score = int(np.mean(count_ls))
    print(f"Ваш алгоритм угадывает число в среднем за {score} попыток")
    return(score)

# Проверяем
score_game(game_core_v3)