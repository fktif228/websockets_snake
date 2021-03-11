import asyncio
import random
import time
import websockets

STATE = {"value": 0}

USERS = set()


async def register(websocket):
    USERS.add(websocket)


async def unregister(websocket):
    USERS.remove(websocket)


async def notify_state(message):
    if USERS:
        await asyncio.wait([user.send(message) for user in USERS])


async def server(websocket, path):
    await register(websocket)  # добовляем сокет в массив

    # while True:
    #     await asyncio.sleep(2)

    try:
        print("try")
        async for message in websocket:
            print("for")
            await asyncio.sleep(2)

    finally:
        print("finally")
        print(websocket)
        await unregister(websocket)



async def giop():
    """модуль игры змейка"""

    def eat_tail(head, arr):
        """
        Если змейка укусила себя
        :param head: обьект координаты головы змейки
        :param arr: список обьектов координаты тела змейки
        """
        for arr_i in arr:
            if (head["x"] == arr_i["x"]) and (head["y"] == arr_i["y"]):
                pass
                # проигрыш
                # clearInterval(game)

    # x, y = 15, 15
    # array = [[0 for j in range(y)] for i in range(x)]

    # Размер одной клетки в px.
    box = 32

    # Счет.
    score = 0

    # Объект еды.
    # food = {
    #     "x": random.randint(1, 15) * box,
    #     "y": random.randint(1, 15) * box
    # }
    food = {
        "x": 10 * box,
        "y": 10 * box
    }

    # Змейка. Представляет собой список объектов - координат.
    snake = [{}]
    snake[0] = {
        "x": 10 * box,
        "y": 10 * box
    }

    # Направление змейки.
    direction = ""

    snake_text = '{"x": 32, "y": 64}'
    while True:

        print(snake)
        print(direction)

        # Новый ход змейки(Программный код пользователя)
        if (snake[0]["x"] == 320) and (snake[0]["y"] == 320):
            direction = "up"
        elif (snake[0]["x"] == 320) and (snake[0]["y"] == 160):
            direction = "left"
        elif (snake[0]["x"] == 96) and (snake[0]["y"] == 160):
            direction = "down"
        elif (snake[0]["x"] == 96) and (snake[0]["y"] == 320):
            direction = "right"

        # Координаты головы змейки.
        snake_x = snake[0]["x"]
        snake_y = snake[0]["y"]

        # Если змейка съела еду.
        if (snake_x == food["x"]) and (snake_y == food["y"]):
            score += 1
            # food = {
            #     "x": random.randint(1, 15) * box,
            #     "y": random.randint(1, 15) * box
            # }
            food = {
                "x": 10 * box,
                "y": 10 * box
            }
        else:
            snake.pop()

        # Если змейка врезалась в стену.
        if (snake_x < box) or (snake_x > box * 17) or (snake_y < 3 * box) or (snake_y > box * 17):
            # проигрыш
            # clearInterval(game)
            pass

        # Изменяем координаты головы, т.е. двигаем змейку.
        if direction == "left":
            snake_x -= box
        if direction == "right":
            snake_x += box
        if direction == "up":
            snake_y -= box
        if direction == "down":
            snake_y += box

        # Новая голова.
        new_head = {
            "x": snake_x,
            "y": snake_y
        }

        # Проверка не укусила ли себя змейка.
        eat_tail(new_head, snake)

        # Добавляем новую голову в начало.
        snake.insert(0, new_head)

        # Подготавливаем данные для передачи на клиент
        shipping_customer = [snake, [food]]

        # Преобразуем обьект в строку
        snake_text = ""
        for i in str(shipping_customer):
            if i == '\'':
                snake_text += '\"'
            else:
                snake_text += i

        # Отправка значений на клиент
        try:
            await notify_state(snake_text)
            # print(snake_text)
            await asyncio.sleep(0.05)
        except:
            print("!")


futer = giop()

start_server = websockets.serve(server, "localhost", 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_until_complete(futer)

asyncio.get_event_loop().run_forever()