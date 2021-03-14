let data_from_server = '[[{"x": 320, "y": 320}], [{"x": 320, "y": 320}]]';

const socket = new WebSocket('ws://localhost:5000');

// Connection opened
socket.addEventListener('open', function (event) {
  console.log('Connected to the WS Server!')
});

// Connection closed
socket.addEventListener('close', function (event) {
  console.log('Disconnected from the WS Server!')
});

// Listen for messages
socket.addEventListener('message', function (event) {
  console.log('Message from server ', event.data);
  data_from_server = event.data;
});


// Игровое поле и тип игры (2D).
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

// Текстура поля.
const ground = new Image();
ground.src = "img/ground.png";

// Текстура еды.
const foodImg = new Image();
foodImg.src = "img/food.png";

// Размер одной клетки в px.
let box = 32;

// Счет.
let score = 0;

// Объект еды.
let food = {x: 10 * box,
            y: 10 * box};

// Змейка. Представляет собой список объектов-координат.
let snake = [];
snake[0] = {
  x: 10 * box,
  y: 10 * box
};


// Функция отрисовки игры.
function drawGame() {

  let json_line = JSON.parse(data_from_server)
  snake = json_line[0]
  food = json_line[1][0]

  // Отрисовка поля и еды.
  ctx.drawImage(ground, 0, 0);
  ctx.drawImage(foodImg, food.x, food.y);

  // Отрисовка змейки.
  ctx.fillStyle = "red";
  ctx.fillRect(snake[0].x, snake[0].y, box, box);
  for(let i = 1; i < snake.length; i++) {
    ctx.fillStyle = "green";
    ctx.fillRect(snake[i].x, snake[i].y, box, box);
  }
  // Отрисовка счета.
  ctx.fillStyle = "white";
  ctx.font = "50px Arial";
  ctx.fillText(score, box * 2.5, box * 1.7);
}

let game = setInterval(drawGame, 100);