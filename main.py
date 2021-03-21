import os
import time
import json
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'C:/Users/ACER/OneDrive/Рабочий стол/2-семестр/ввпд/file_upload/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'py'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'jsbcfsbfjefebw237u3gdbdc'
socketio = SocketIO(app)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def snake_game_module(filename):
    """модуль игры змейка"""

    def eat_tail(head, arr):
        """Если змейка укусила себя"""
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

        # Новый ход змейки(Программный код пользователя)
        pm_name = 'uploads.' + filename
        uploads = __import__(pm_name)
        # import uploads.main
        direction = uploads.main.user_algorithm(snake, direction)

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
            socketio.emit('my response', shipping_customer_text, callback=messageRecived)
            # print(snake_text)
            time.sleep(0.1)
        except:
            print("!")


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('broadcast_game', filename=filename))
    return render_template('upload_file.html')


@app.route('/broadcast_game')
def broadcast_game():
    """ggg"""
    data = dict(filename=request.args.get('filename'))
    return render_template('broadcast_game.html', data=data)


@app.route('/game', methods=['POST', 'GET'])
def game():
    """Запуск трансляции"""
    if request.method == "POST":
        filename = request.form['filename'][0:-3]
        snake_game_module(filename)
    else:
        return render_template('game.html')


def messageRecived():
    print('message was received!!!')


@socketio.on('my event')
def handle_my_custom_event(json):
    print('recived my event: ' + str(json))
    socketio.emit('my response', json, callback=messageRecived)


if __name__ == '__main__':
    socketio.run(app, debug=True)

