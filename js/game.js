let gimi = '[[{"x": 320, "y": 320}], [{"x": 320, "y": 320}]]';

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
  gimi = event.data;
  //document.getElementsByTagName('div')[0].style.width = event.data + "%";
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
let food = {x: Math.floor((Math.random() * 17 + 1)) * box,
            y: Math.floor((Math.random() * 15 + 3)) * box};

// Змейка. Представляет собой список объектов-координат.
let snake = [];
snake[0] = {
  x: 10 * box,
  y: 10 * box
};

// Направление змейки.
let dir;

// Управление змейкой.
// document.addEventListener("keydown", function(event) {
//     if(event.keyCode == 37 && dir != "right")
//       dir = "left";
//     else if(event.keyCode == 38 && dir != "down")
//       dir = "up";
//     else if(event.keyCode == 39 && dir != "left")
//       dir = "right";
//     else if(event.keyCode == 40 && dir != "up")
//       dir = "down";
// });

// Если змейка укусила себя.
function eatTail(head, arr) {
  for(let i = 0; i < arr.length; i++) {
    if(head.x == arr[i].x && head.y == arr[i].y)
      clearInterval(game);
  }
}

// Функция отрисовки игры.
function drawGame() {

  let json_line = JSON.parse(gimi)
  // snakeX = json_line[0]['x']
  // snakeY = json_line[0]['y']




  // Отрисовка поля и еды.
  ctx.drawImage(ground, 0, 0);
  ctx.drawImage(foodImg, json_line[1][0]["x"], json_line[1][0]["y"]);

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

  // Координаты головы змейки.
  let snakeX = snake[0].x;
  let snakeY = snake[0].y;

  // Если змейка съела еду.
  if(snakeX == food.x && snakeY == food.y) {
    // score++;
    // food = {x: Math.floor((Math.random() * 17 + 1)) * box,
    //         y: Math.floor((Math.random() * 15 + 3)) * box};
  } 
  else {
    snake.pop();
  }

  snake = json_line[0]

  // // Если змейка врезалась в стену.
  // if (snakeX < box || snakeX > box * 17 || snakeY < 3 * box || snakeY > box * 17)
  //   clearInterval(game);



  // for (let i=0; i<gimi.length; i++){
  //   if (gimi[i] === "\'"){
  //     alert(gimi[i]);
  //     gimi[i] = "\""
  //   }
  //
  // }
  // let json_line = JSON.parse(gimi)
  // if (gimi[0] === "{")
  //   gimi = "[" + gimi.substring(1, gimi.length - 1) + "]"
  //alert(gimi);
    // Изменяем координаты головы, т.е. двигаем змейку.
  // var a = eval("({\'obj\':[" + gimi + "]})");
  // let object = eval("("+gimi+")");





  // alert(snakeX);
  // if (dir == "left") snakeX -= box;
  // if (dir == "right") snakeX += box;
  // if (dir == "up") snakeY -= box;
  // if (dir == "down") snakeY += box;

  //alert(snakeX);
  // Новая голова.
  // let newHead = {
  //   x: snakeX,
  //   y: snakeY
  // };
  //alert(newHead);

  // Проверка не укусила ли себя змейка.
  // eatTail(newHead, snake);

  // Добавляем новую голову в начало.
  //snake.unshift(newHead);
}

let game = setInterval(drawGame, 100);
