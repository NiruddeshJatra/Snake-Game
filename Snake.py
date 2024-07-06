import os
# Hide Pygame support prompt
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
import turtle
import time
import random
import pickle
import atexit



class Screen:
    def __init__(self):
        self.wn = turtle.Screen()
        self.wn.title("Snake Game by NJ Production")
        self.wn.setup(width=900, height=650)
        self.wn.bgcolor("#FFEC94")
        self.wn.tracer(0)
        self.level_turtle = self.create_turtle("#A91E4B", -400, 285)
        self.point_turtle = self.create_turtle("#2A4A1A", 0, 285)
    
    def create_turtle(self, color, x, y):
        t = turtle.Turtle()
        t.speed(0)
        t.hideturtle()
        t.penup()
        t.pencolor(color)
        t.goto(x, y)
        return t

    def update_score(self, score, high_score):
        self.point_turtle.clear()
        self.point_turtle.write(f"SCORE: {score}    HIGH SCORE: {high_score}", align="center", font=("ds-digital", 20, "normal"))

    def update_level(self, level):
        self.level_turtle.clear()
        self.level_turtle.write(f'LEVEL: {level}', align="left", font=("ds-digital", 20, "normal"))

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.load("sound\melody_bgm.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(.5)

    def play_sound(self, sound_file):
        sound = pygame.mixer.Sound(sound_file)
        sound.play()

    def stop_music(self):
        pygame.mixer.music.stop()

    def start_music(self):
        pygame.mixer.music.load("sound\melody_bgm.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(.5)

class ScoreManager:
    def __init__(self):
        self.score = 0
        self.high_score = self.load_high_score()

    def load_high_score(self):
        try:
            with open('high_score.pkl', 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            with open('high_score.pkl', 'wb') as f:
                pickle.dump(0, f)
            return 0

    def save_high_score(self):
        with open('high_score.pkl', 'wb') as f:
            pickle.dump(self.high_score, f)

    def update_score(self, points):
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score

class SnakeGame:
    def __init__(self):
        self.sound_manager = SoundManager()
        self.score_manager = ScoreManager()
        self.screen = Screen()
        self.screen.update_score(self.score_manager.score, self.score_manager.high_score)
        self.head = self.create_turtle("#101018", 0, 0, "square", 0.75)
        self.food = self.create_turtle("#470808", 0, 150, "circle", 0.75)
        self.body = []
        self.wall = []
        self.delay = 10
        self.level = 1
        self.end_time = time.time() + 3
        self.count = 1
        self.head.direction = "stop"
        self.bind_keys()
        self.generate_food()
        atexit.register(self.save_high_score)
        self.run_game()

    def create_turtle(self, color, x, y, shape, size):
        t = turtle.Turtle()
        t.speed(0)
        t.color(color)
        t.shape(shape)
        t.shapesize(size, size, 1)
        t.penup()
        t.goto(x, y)
        return t

    def bind_keys(self):
        self.screen.wn.listen()
        self.screen.wn.onkeypress(self.go_up, "Up")
        self.screen.wn.onkeypress(self.go_down, "Down")
        self.screen.wn.onkeypress(self.go_left, "Left")
        self.screen.wn.onkeypress(self.go_right, "Right")

    def go_up(self):
        if self.head.direction != "down":
            self.head.direction = "up"

    def go_down(self):
        if self.head.direction != "up":
            self.head.direction = "down"

    def go_left(self):
        if self.head.direction != "right":
            self.head.direction = "left"

    def go_right(self):
        if self.head.direction != "left":
            self.head.direction = "right"

    def move(self):
        if self.head.direction == "up":
            y = self.head.ycor()
            self.head.sety(y + 10)
        if self.head.direction == "down":
            y = self.head.ycor()
            self.head.sety(y - 10)
        if self.head.direction == "left":
            x = self.head.xcor()
            self.head.setx(x - 10)
        if self.head.direction == "right":
            x = self.head.xcor()
            self.head.setx(x + 10)

    def generate_food(self):
        x = random.randint(-435, 435)
        y = random.randint(-300, 265)
        self.food.goto(x, y)
        self.sound_manager.play_sound("sound\generating_food.wav")

    def create_block(self):
        block = turtle.Turtle()
        block.speed(0)
        block.shapesize(1.5, 1.5, 1)
        block.color("#2E3840")
        block.penup()
        block.shape("square")
        return block

    def create_wall(self):
        self.wall = []
        wall_coords = [
            (-180, 45), (-150, 45), (-120, 45), (-90, 45), (-60, 45), (-30, 45),
            (0, 45), (30, 45), (60, 45), (90, 45), (120, 45), (150, 45),
            (-180, -70), (-150, -70), (-120, -70), (-90, -70), (-60, -70),
            (-30, -70), (0, -70), (30, -70), (60, -70), (90, -70), (120, -70), (150, -70),
            (-300, 150), (-270, 150), (-240, 150), (-210, 150), (-180, 150), (-150, 150),
            (120, 150), (150, 150), (180, 150), (210, 150), (240, 150), (270, 150),
            (-300, 120), (-300, 90), (-300, 60), (-300, 30), (-300, 0),
            (270, 120), (270, 90), (270, 60), (270, 30), (270, 0),
            (-120, -175), (-90, -175), (-60, -175), (-30, -175),
            (120, -175), (150, -175), (180, -175), (210, -175),
            (-330, -205), (-300, -205), (-270, -205), (-240, -205), (-210, -205),
            (210, -205), (240, -205), (270, -205), (300, -205), (330, -205)
        ]
        for coord in wall_coords:
            block = self.create_block()
            block.goto(coord)
            self.wall.append(block)

    def game_over(self):
        self.score_manager.save_high_score()
        self.sound_manager.stop_music()
        self.sound_manager.play_sound("sound\lose_or_failure.wav")
        time.sleep(4)
        self.head.goto(0, 0)
        self.head.direction = "stop"
        self.screen.wn.bgcolor("#FFEC94")
        for part in self.body:
            part.goto(1000, 1000)
        self.body.clear()
        self.score_manager.score = 0
        self.delay = 10
        self.level = 1
        for block in self.wall:
            block.goto(1000, 1000)
        self.wall.clear()
        self.screen.update_score(self.score_manager.score, self.score_manager.high_score)
        self.generate_food()
        self.sound_manager.start_music()

    def border_collision(self):
        if self.head.xcor() > 435 or self.head.xcor() < -435 or self.head.ycor() > 275 or self.head.ycor() < -300:
            self.game_over()

    def body_collision(self):
        for part in self.body:
            if self.head.distance(part) < 10:
                self.game_over()

    def wall_collision(self):
        for block in self.wall:
            if self.head.distance(block) < 10:
                self.game_over()

    def eating_food(self):
        if self.head.distance(self.food) < 10:
            self.generate_food()
            part = self.create_turtle("#224E43", 0, 0, "square", 0.75)
            self.body.append(part)
            self.score_manager.update_score(10)
            self.screen.update_score(self.score_manager.score, self.score_manager.high_score)
            self.delay += 0.5

    def move_body(self):
        for index in range(len(self.body) - 1, 0, -1):
            x = self.body[index - 1].xcor()
            y = self.body[index - 1].ycor()
            self.body[index].goto(x, y)
        if len(self.body) > 0:
            x = self.head.xcor()
            y = self.head.ycor()
            self.body[0].goto(x, y)

    def save_high_score(self):
        self.score_manager.save_high_score()

    def run_game(self):
        while True:
            self.screen.wn.update()
            if self.score_manager.score < 200:
                self.border_collision()
                self.body_collision()
                self.eating_food()
                self.move_body()
                self.screen.update_level(self.level)
            elif 200 <= self.score_manager.score < 400:
                self.level = 2
                self.delay = 30
                if self.count == 1:
                    self.sound_manager.play_sound("sound\entered_next_level.wav")
                    self.count += 1
                self.screen.wn.bgcolor('#A3B8B1')
                self.border_collision()
                self.body_collision()
                self.eating_food()
                self.move_body()
                self.screen.update_level(self.level)
            elif 400 <= self.score_manager.score < 600:
                self.level = 3
                self.delay = 40
                if self.count == 2:
                    self.sound_manager.play_sound("sound\entered_next_level.wav")
                    self.count += 1
                self.screen.wn.bgcolor('#E1C4AB')
                self.border_collision()
                self.body_collision()
                self.eating_food()
                self.move_body()
                self.screen.update_level(self.level)
                if time.time() > self.end_time:
                    self.generate_food()
                    self.end_time = time.time() + 3
            elif 600 <= self.score_manager.score < 800:
                self.level = 4
                self.delay = 45
                if self.count == 3:
                    self.sound_manager.play_sound("sound\entered_next_level.wav")
                    self.create_wall()
                    self.count += 1
                self.screen.wn.bgcolor("#E6EFF6")
                self.border_collision()
                self.body_collision()
                self.wall_collision()
                self.eating_food()
                self.screen.update_level(self.level)
                for block in self.wall:
                    if self.food.distance(block) < 20:
                        self.generate_food()
                self.move_body()
            elif self.score_manager.score >= 800:
                self.level = 5
                self.delay = 50
                if self.count == 4:
                    self.sound_manager.play_sound("sound\entered_next_level.wav")
                    self.create_wall()
                    self.count += 1
                self.screen.wn.bgcolor("#C4D15B")
                self.border_collision()
                self.body_collision()
                self.wall_collision()
                self.eating_food()
                self.screen.update_level(self.level)
                for block in self.wall:
                    if self.food.distance(block) < 20:
                        self.generate_food()
                self.move_body()
                if time.time() > self.end_time:
                    self.generate_food()
                    self.end_time = time.time() + 3
            self.move()
            pygame.time.Clock().tick(self.delay)

if __name__ == "__main__":
    SnakeGame()
