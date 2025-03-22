"""
Отскакивающий от краев логотип DVD, (c) Эл Свейгарт al@inventwithpython.com
Анимация отскакивающего логотипа DVD. Оценить ее по достоинству могут
только люди "определенного возраста". Для останова нажмите Ctrl+C.
"""

import random
import time
import sys


try:
    import bext
except ImportError:
    print("""
    Эта программа использует модуль "bext", который вы можете установить выполнив команду "pip install bext"
    """)
    sys.exit()

# Задаем константы:
WIDTH, HEIGHT = bext.size()

# В Windows нельзя вывести символ в последний столбец без добавления
# автоматически символа новой строки, так что уменьшаем ширину на 1:

WIDTH -= 1

NUMBER_OF_LOGOS = 5
PAUSE_AMOUNT = 0.2
COLORS = ['red', 'green', 'orange', 'blue', 'yellow', 'white', 'cyan', 'magenta']

UP_RIGHT = 'ur'
UP_LEFT = 'lr'
DOWN_RIGHT = 'dr'
DOWN_LEFT = 'dl'
DIRECTIONS = (UP_RIGHT, UP_LEFT, DOWN_RIGHT, DOWN_LEFT)

# Названия ключей для ассоциативных масcивов логотипов.
COLOR = 'color'
X = 'x'
Y = 'y'
DIR = 'directions'


def main():
    bext.clear()
    # Генерация логотипов.
    logos = []
    for i in range(NUMBER_OF_LOGOS):
        logos.append({COLOR: random.choice(COLORS),
                      X: random.randint(1, WIDTH - 4),
                      Y: random.randint(1, HEIGHT - 4),
                      DIR: random.choice(DIRECTIONS)
                      })
        if logos[-1][X] % 2 == 1:
            # Гарантируем, что X четное число, для столкновения с углом.
            logos[-1][X] -= 1

    corner_bounces = 0  # считаем сколько раз логотип ударился об угол.
    while True:  # Основной цикл программы.
        for logo in logos:  # обрабатываем все виды логотипов.
            bext.goto(logo[X], logo[Y])  # Очищаем место где ранее был логотип.
            print('   ', end='')

            original_direction = logo[DIR]

            # Проверяем не отскакивает ли логотип от угла.
            if logo[X] == 0 and logo[Y] == 0:
                logo[DIR] = DOWN_RIGHT
                corner_bounces += 1
            elif logo[X] == 0 and logo[Y] == HEIGHT-1:
                logo[DIR] = UP_RIGHT
                corner_bounces += 1
            elif logo[X] == WIDTH-3 and logo[Y] == 0:
                logo[DIR] = DOWN_LEFT
                corner_bounces += 1
            elif logo[X] == WIDTH-3 and logo[Y] == HEIGHT-1:
                logo[DIR] = UP_LEFT
                corner_bounces += 1

            # Проверяем, не отскакивает ли логотип от левого края:
            elif logo[X] == 0 and logo[DIR] == UP_LEFT:
                logo[DIR] = UP_RIGHT
            elif logo[X] == 0 and logo[DIR] == DOWN_LEFT:
                logo[DIR] = DOWN_RIGHT

            # Проверяем, не отскакивает ли логотип от правого края:
            # (WIDTH - 3, поскольку 'DVD' состоит из трех букв.)
            elif logo[X] == WIDTH - 3 and logo[DIR] == UP_RIGHT:
                logo[DIR] = UP_LEFT
            elif logo[X] == WIDTH - 3 and logo[DIR] == DOWN_RIGHT:
                logo[DIR] = DOWN_LEFT

            # Проверяем, не отскакивает ли логотип от верхнего края:
            elif logo[Y] == 0 and logo[DIR] == UP_LEFT:
                logo[DIR] = DOWN_LEFT
            elif logo[Y] == 0 and logo[DIR] == UP_RIGHT:
                logo[DIR] = DOWN_RIGHT

            # Проверяем, не отскакивает ли логотип от нижнего края:
            elif logo[Y] == HEIGHT - 1 and logo[DIR] == DOWN_LEFT:
                logo[DIR] = UP_LEFT
            elif logo[Y] == HEIGHT - 1 and logo[DIR] == DOWN_RIGHT:
                logo[DIR] = UP_RIGHT

            if logo[DIR] != original_direction:
                # Меняем цвет при отскакивании логотипа:
                logo[COLOR] = random.choice(COLORS)

            # Перемещаем логотип (Координата X меняется на 2, поскольку
            # в терминале высота символов вдвое превышает ширину.)
            if logo[DIR] == UP_RIGHT:
                logo[X] += 2
                logo[Y] -= 1
            elif logo[DIR] == UP_LEFT:
                logo[X] -= 2
                logo[Y] -= 2
            elif logo[DIR] == DOWN_RIGHT:
                logo[X] += 2
                logo[Y] += 1
            elif logo[DIR] == DOWN_LEFT:
                logo[X] -= 2
                logo[Y] += 1

        # Отображает количество отскакиваний.
        bext.goto(5, 0)
        bext.fg('white')
        print(f'Отскакиваний от угла: {corner_bounces} раз(а)')

        for logo in logos:
            # Отрисовывает логотипы на новом месте:
            bext.goto(logo[X], logo[Y])
            bext.fg(logo[COLOR])
            print('DVD', end='')

        bext.goto(0, 0)
        sys.stdout.flush()
        time.sleep(PAUSE_AMOUNT)


if __name__ == '__main__':
    try:
        print('bugivugi')
        main()
    except KeyboardInterrupt:
        print()
        print('Bouncing DVD Logo, by Al Sweigart')
        sys.exit()
