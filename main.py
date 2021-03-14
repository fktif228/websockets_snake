import asyncio
import json
import random
import time
import websockets

USERS = set()


async def register(websocket):
    """Добавление вебсокета в массива"""
    USERS.add(websocket)


async def unregister(websocket):
    """Удаление вебсокета из массива"""
    USERS.remove(websocket)


async def notify_state(message):
    """Отправка данных на клиент"""
    if USERS:
        await asyncio.wait([user.send(message) for user in USERS])


async def server(websocket, path):
    await register(websocket)  # добовляем сокет в массив
    try:
        # print("try")
        async for message in websocket:
            await unregister(websocket)
            print(message)
            await asyncio.sleep(2)

    finally:
        # print("finally")
        # print(websocket)
        # await unregister(websocket)
        pass


async def snake_game_module():
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

    while True:
        # print(score)
        # print(snake)
        # print(direction)

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
        shipping_customer_text = json.dumps(shipping_customer)

        # Отправка значений на клиент
        try:
            await notify_state(shipping_customer_text)
            # print(snake_text)
            await asyncio.sleep(0.5)
        except:
            print("!")


plug_module = snake_game_module()

start_server = websockets.serve(server, "localhost", 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_until_complete(plug_module)

asyncio.get_event_loop().run_forever()
