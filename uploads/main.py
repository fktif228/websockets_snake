def user_algorithm(snake, direction):
    if (snake[0]["x"] == 320) and (snake[0]["y"] == 320):
        direction = "up"
    elif (snake[0]["x"] == 320) and (snake[0]["y"] == 160):
        direction = "left"
    elif (snake[0]["x"] == 96) and (snake[0]["y"] == 160):
        direction = "down"
    elif (snake[0]["x"] == 96) and (snake[0]["y"] == 320):
        direction = "right"
    return direction
