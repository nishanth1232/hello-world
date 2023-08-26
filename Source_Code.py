import turtle as t
from random import randint
from time import sleep, perf_counter
from itertools import combinations
from datetime import datetime
from sys import exit
import webbrowser
import pickle
import threading
import math
import pygame
import os
from flask import Flask
app = Flask(__name__)


t.speed(0)
current_level = 1
current_score = 0
current_health = 5
turtles = []
player_turtle = t.Turtle()
laser_turtle = t.Turtle()
laser_turtle.ht()
laser_turtle.speed(0)
t.ht()
t.color("white")
key_pressed = 0
running = 1

win = t.Screen()
win.setup(1000, 500) #1000x500 Size
win.delay(3)
win.tracer(0, 0)
pygame.mixer.init()

try:
    win.bgpic("space.gif")
    win.addshape("spaceship.gif")
    win.addshape("asteroid.gif")
    win.addshape("score.gif")
    win.addshape("laser.gif")
    win.addshape("space_key.gif")
    win.addshape("arrow_keys.gif")
    win.addshape("esc_key.gif")
    win.addshape("asteroid_hit.gif")
    win.addshape("space_asteroid.gif")
    win.addshape("space_score.gif")
    wave_object = pygame.mixer.Sound("bga.wav")
    score_pickup_object = pygame.mixer.Sound("score_pickup.wav")
    asteroid_pickup_object = pygame.mixer.Sound("asteroid_pickup.wav")
    asteroid_hit_object = pygame.mixer.Sound("asteroid_hit.wav")
    laser_object = pygame.mixer.Sound("laser.wav")
    spacecraft_movement_object = pygame.mixer.Sound("spacecraft_movement.wav")
    with open("scores.html", "r") as f:
        pass
except:
    t.write("Source Files Not Found!", align = "center", font = ("Arial", 25, "bold"))
    win.update()
    sleep(3)
    win.bye()
    exit()

score_turtle = t.Turtle()
health_turtle = t.Turtle()

score_turtle.ht()
score_turtle.up()
score_turtle.color("white")
score_turtle.setposition(-475, 200) #Co-ordinates of Score
score_turtle.down()

health_turtle.ht()
health_turtle.up()
health_turtle.color("white")
health_turtle.setposition(475, 200) #Co-ordinates of Health
health_turtle.down()

active_turtles = []
gen_values = []

def level_screen():
    global current_level, current_score, current_health, checker
    t.onkey(None, "Return")
    t.clear()
    t.write("Level " + str(current_level), align = "center", font = ("Arial", 30, "bold"))
    win.update()
    sleep(3)
    t.clear()
    level_screen_generate(current_level)
    t.clear()
    t.write("Start!", align = "center", font = ("Arial", 30, "bold"))
    win.update()
    sleep(3)
    t.clear()
    player_control()
    deployer()
    t.write("Score: " + str(current_score), align = "center", font = ("Arial", 20, "bold"))
    win.update()
    sleep(3)
    t.clear()
    return

class Movables:
    def __init__(self, i):
        global current_level
        self.__turtle = t.Turtle()
        self.__name = ""
        self.__turtle.ht()
        self.__turtle.up()
        self.__turtle.speed(0)
        self.__turtle.right(180)
        self.__turtle.setposition(400, randint(-150, 150))
        self.__angle = randint(-5, 5)
        if(i<current_level):
            self.__turtle.shape("asteroid.gif")
            self.name = "Asteroid"
            #if(i%2 == 0):
                #self.__turtle.right(randint(0, 15))
            #else:
                #self.__turtle.left(randint(0,15))
        else:
            self.name = "Score"
            self.__turtle.shape("score.gif")
        return
    def clear_turtle(self, i):
        global active_turtles, turtles
        if(i in active_turtles):
            active_turtles.remove(i)
        self.__turtle.ht()
        return
    def check(self, i):
        global turtles, current_health, current_level, current_score, player_turtle, active_turtles, laser_turtle
        if (self.__turtle.distance(player_turtle.xcor(), player_turtle.ycor())<55 and self.__turtle.isvisible()):
            if(self.name == "Asteroid"):
                self.__turtle.ht()
                t.setposition(self.__turtle.xcor(), self.__turtle.ycor())
                t.shape("asteroid_hit.gif")
                t.stamp()
                win.bgpic("space_asteroid.gif")
                (threading.Thread(target = lambda: asteroid_pickup_object.play())).start()
                self.clear_turtle(i)
                current_health -= 1
                health_turtle.clear()
                health_turtle.write("Health: " + str(current_health), align = "right", font = ("Arial", 20, "bold"))
                t.ontimer(lambda: t.clearstamps(), 100)
                t.setposition(0,0)
                t.ontimer(lambda: win.bgpic("space.gif"), 100)
            else:
                self.__turtle.ht()
                win.bgpic("space_score.gif")
                (threading.Thread(target = lambda: score_pickup_object.play())).start()
                self.clear_turtle(i)
                current_score += 100*current_level
                score_turtle.clear()
                score_turtle.write("Score: " + str(current_score), align = "left", font = ("Arial", 20, "bold"))
                t.ontimer(lambda: win.bgpic("space.gif"), 100)
        if(((self.__turtle.distance(laser_turtle.xcor(), laser_turtle.ycor())<35)) and self.__turtle.isvisible() and self.name == "Asteroid"):
                laser_turtle.ht()
                t.setposition(self.__turtle.xcor(), self.__turtle.ycor())
                t.shape("asteroid_hit.gif")
                t.stamp()
                (threading.Thread(target = lambda: asteroid_hit_object.play())).start()
                self.clear_turtle(i)
                current_score += 50*current_level
                score_turtle.clear()
                t.ontimer(lambda: t.clearstamps(), 100)
                t.setposition(0,0)
                score_turtle.write("Score: " + str(current_score), align = "left", font = ("Arial", 20, "bold"))
        return
    def bounds_check(self, i):
        if((self.__turtle.isvisible() and (self.__turtle.xcor()<-600 or self.__turtle.ycor()>350 or self.__turtle.ycor()<-350))):
                self.clear_turtle(i)
        return
    def move(self, i):
        global turtles, current_level, active_turtles, laser_turtle, checker
        #self.__turtle.forward(3*(current_level))
        self.__turtle.setposition(self.__turtle.xcor()-2*current_level, self.__turtle.ycor()+0.5*math.sin(self.__angle)) 
        if(laser_turtle.isvisible()):
            laser_turtle.setposition(laser_turtle.xcor()+7, laser_turtle.ycor())
        return
    def reset(self, i):
        self.clear_turtle(i)
        self.__turtle.ht()
        self.__turtle.seth(0)
        self.__turtle.right(180)
        self.__turtle.setposition(400, randint(-150, 150))
        if(i<1+current_level):
            if(i%2 == 0):
                self.__turtle.right(randint(0, 15))
            else:
                self.__turtle.left(randint(0,15))
        return
    def show(self, i):
        self.__turtle.st()
        return
    def get_heading(self):
        return self.__turtle.heading()
            
def level_screen_generate(n):
    global turtles, current_health, player_turtle, health_turtle, score_turtle, current_score, gen_values, current_level, laser_turtle
    score_turtle.write("Score: " + str(current_score), align = "left", font = ("Arial", 20, "bold"))
    player_turtle.up()
    laser_turtle.up()
    player_turtle.setposition(-450, 0)#Starting Position
    laser_turtle.setposition(-450, 0)
    player_turtle.shape("spaceship.gif")
    laser_turtle.shape("laser.gif")
    if(n==1):
        health_turtle.clear()
        current_health = 3
        health_turtle.write("Health: " + str(current_health), align = "right", font = ("Arial", 20, "bold"))
    elif(n==2):
        current_health = 2
        health_turtle.clear()
        health_turtle.write("Health: " + str(current_health), align = "right", font = ("Arial", 20, "bold"))
    elif(n==3):
        current_health = 1
        health_turtle.clear()
        health_turtle.write("Health: " + str(current_health), align = "right", font = ("Arial", 20, "bold"))
    turtles = list(map(lambda x: Movables(x), range(n+1)))
    gen_values = list(combinations(range(len(turtles)), len(turtles)))
    win.update()
    return True

def deactivate():
    global key_pressed
    key_pressed = 0
    return

def u():
    global key_pressed
    key_pressed = 1
    player_control_rem()
    (threading.Thread(target = lambda: spacecraft_movement_object.play(-1))).start()
    while(key_pressed):
        win.onkeyrelease(deactivate, "Up")
        player_turtle.setposition(player_turtle.xcor(), player_turtle.ycor()+5)
        if (laser_turtle.isvisible() == False):
            laser_turtle.setposition(laser_turtle.xcor(), laser_turtle.ycor()+5)
        if(player_turtle.xcor()>500 or player_turtle.ycor()>250 or player_turtle.ycor()<-250 or player_turtle.xcor()<-500):
            player_turtle.setposition(-450, 0)
        if(laser_turtle.xcor()>550 or laser_turtle.ycor()>300 or laser_turtle.ycor()<-300):
            laser_turtle.ht()
    spacecraft_movement_object.stop()
    win.onkeyrelease(None, "Up")
    return player_control()

def d():
    global key_pressed
    key_pressed = 1
    player_control_rem()
    (threading.Thread(target = lambda: spacecraft_movement_object.play(-1))).start()
    while(key_pressed):
        win.onkeyrelease(deactivate, "Down")
        player_turtle.setposition(player_turtle.xcor(), player_turtle.ycor()-5)
        if (laser_turtle.isvisible() == False):
            laser_turtle.setposition(laser_turtle.xcor(), laser_turtle.ycor()-5)
        if(player_turtle.xcor()>500 or player_turtle.ycor()>250 or player_turtle.ycor()<-250 or player_turtle.xcor()<-500):
            player_turtle.setposition(-450, 0)
        if(laser_turtle.xcor()>550 or laser_turtle.ycor()>300 or laser_turtle.ycor()<-300):
            laser_turtle.ht()
    spacecraft_movement_object.stop()
    win.onkeyrelease(None, "Down")
    return player_control()

def l():
    global key_pressed
    key_pressed = 1
    player_control_rem()
    (threading.Thread(target = lambda: spacecraft_movement_object.play(-1))).start()
    while(key_pressed):
        win.onkeyrelease(deactivate, "Left")
        player_turtle.setposition(player_turtle.xcor()-5, player_turtle.ycor())
        if (laser_turtle.isvisible() == False):
            laser_turtle.setposition(laser_turtle.xcor()-5, laser_turtle.ycor())
        if(player_turtle.xcor()>500 or player_turtle.ycor()>250 or player_turtle.ycor()<-250 or player_turtle.xcor()<-500):
            player_turtle.setposition(-450, 0)
        if(laser_turtle.xcor()>550 or laser_turtle.ycor()>300 or laser_turtle.ycor()<-300):
            laser_turtle.ht()
    spacecraft_movement_object.stop()
    win.onkeyrelease(None, "Left")
    return player_control()

def r():
    global key_pressed
    key_pressed = 1
    player_control_rem()
    (threading.Thread(target = lambda: spacecraft_movement_object.play(-1))).start()
    while(key_pressed):
        win.onkeyrelease(deactivate, "Right")
        player_turtle.setposition(player_turtle.xcor()+5, player_turtle.ycor())
        if (laser_turtle.isvisible() == False):
            laser_turtle.setposition(laser_turtle.xcor()+5, laser_turtle.ycor())
        if(player_turtle.xcor()>500 or player_turtle.ycor()>250 or player_turtle.ycor()<-250 or player_turtle.xcor()<-500):
            player_turtle.setposition(-450, 0)
        if(laser_turtle.xcor()>550 or laser_turtle.ycor()>300 or laser_turtle.ycor()<-300):
            laser_turtle.ht()
    spacecraft_movement_object.stop()
    win.onkeyrelease(None, "Right")
    return player_control()

def shoot():
    global laser_turtle
    laser_turtle.st()
    (threading.Thread(target = lambda: laser_object.play())).start()
    win.onkey(None, "space")
    return

def player_control():
    win.onkeypress(lambda: (threading.Thread(target = u)).start(), "Up")
    win.onkeypress(lambda: (threading.Thread(target = d)).start(), "Down")
    win.onkeypress(lambda: (threading.Thread(target = l)).start(), "Left")
    win.onkeypress(lambda: (threading.Thread(target = r)).start(), "Right")
    win.onkeypress(lambda: (threading.Thread(target = shoot)).start(), "space")
    return

def player_control_rem():
    win.onkeypress(None, "Up")
    win.onkeypress(None, "Down")
    win.onkeypress(None, "Left")
    win.onkeypress(None, "Right")
    win.onkeypress(None, "space")
    return

def deployer():
    win.onkey(None, "Return")
    global current_health, active_turtles, turtles, current_level, gen_values, player_turtle, checker
    win.tracer(0,0)
    active_turtles = list(gen_values[randint(0, len(gen_values)-1)])
    for i in active_turtles:
        turtles[i].show(i)
    win.update()
    for j in range(2*current_level):
        for i in active_turtles:
            turtles[i].show(i)
        win.update()
        count = len(active_turtles)
        start = perf_counter()
        player_control()
        while(len(active_turtles)>0 and current_health>0):
            for i in active_turtles:
                if (perf_counter()-start)>0.01:
                    win.update()
                    start = perf_counter()
                (threading.Thread(target = lambda: turtles[i].move(i))).start()
                (threading.Thread(target = lambda: turtles[i].bounds_check(i))).start()
                (threading.Thread(target = lambda: turtles[i].check(i))).start()
            """for i in range(len(active_turtles), count+1):
                (threading.Thread(target = lambda: True)).start()
                (threading.Thread(target = lambda: True)).start()
                (threading.Thread(target = lambda: True)).start()"""
        deactivate()
        player_control_rem()
        win.update()
        if(current_health<=0):
            for i in active_turtles:
                turtles[i].reset(i)
            win.update()
            break
        for i in range(len(turtles)):
            turtles[i].reset(i)
            win.update()
        active_turtles = list(gen_values[randint(0, len(gen_values)-1)])
        laser_turtle.ht()
        laser_turtle.setposition(player_turtle.xcor(), player_turtle.ycor())
        win.onkey(shoot, "space")
        win.update()
    for i in active_turtles:
        turtles[i].reset(i)
        win.update()
    player_control_rem()
    player_turtle.setposition(-450, 0)
    laser_turtle.setposition(-450, 0)
    win.update()
    return
    
def write_score():
    global current_score, player_name
    #[score, name, date, time]
    current_time = str((datetime.today()).strftime("%H:%M:%S"))
    current_date = str((datetime.today()).strftime("%d/%m/%Y"))
    if(player_name == None):
        player_name = "[N/A]"
    with open("scores.html", "r") as f, open("scores.bin", "rb") as p:
        s = f.readlines()
        score_list = pickle.load(p)
    start = s[:35]
    cont = s[35:-3]
    end = list(reversed(s[-1:-4:-1]))
    score_list.append([current_score, player_name, current_date, current_time])
    score_list = list(sorted(score_list, reverse = True))
    max_score = max(score_list)
    with open("scores.html", "w") as f, open("scores.bin", "wb") as p:
        f.writelines(start)
        pickle.dump(score_list, p)
        f.write("\n<tr>\n<td style=\"background-color:rgba(255, 215, 0, 0.6)\">"+str(max_score[1])+\
                "</td>\n<td style=\"text-align:center;background-color:rgba(255, 215, 0, 0.6)\">"\
            +str(max_score[0])+"</td>\n<td style=\"text-align:center;background-color:rgba(255, 215, 0, 0.6)\">"+str(max_score[2])+\
            "</td>\n<td style=\"text-align:center;background-color:rgba(255, 215, 0, 0.6)\">"+str(max_score[3])+\
            "</td>\n</tr>\n")
        for i in score_list:
            f.write("\n<tr>\n<td>"+str(i[1])+"</td>\n<td style=\"text-align:center\">"\
                +str(i[0])+"</td>\n<td style=\"text-align:center\">"+str(i[2])+\
                "</td>\n<td style=\"text-align:center\">"+str(i[3])+\
                "</td>\n</tr>\n")
        f.writelines(end)
        
def start():
    global current_level, current_health, current_score, intro
    intro[0].clear()
    intro[0].ht()
    intro[1].clear()
    intro[1].ht()
    intro[2].clear()
    intro[2].ht()
    win.update()
    del intro
    t.setposition(0,0)
    t.clear()
    level_screen()
    sleep(1)
    current_level += 1
    if(current_health<=0):
        t.write("Game Over!\nFinal Score: " + str(current_score), align = "center", font = ("Arial", 20, "bold"))
        win.update()
        sleep(3)
        t.bye()
        write_score()
        webbrowser.open("scores.html")
        os.system("taskkill /f /im pythonw.exe")
    else:
        level_screen()
        current_level += 1
        if(current_health<=0):
            t.write("Game Over!\nFinal Score: " + str(current_score), align = "center", font = ("Arial", 20, "bold"))
            win.update()
            sleep(3)
            t.bye()
            write_score()
            webbrowser.open("scores.html")
            os.system("taskkill /f /im pythonw.exe")
        else:
            level_screen()
            current_level += 1
            if(current_health<=0):
                t.write("Game Over!\nFinal Score: " + str(current_score), align = "center", font = ("Arial", 20, "bold"))
                win.update()
                sleep(3)
                t.bye()
                write_score()
                webbrowser.open("scores.html")
                os.system("taskkill /f /im pythonw.exe")
            else:
                t.write("Congratulations!\nFinal Score: " + str(current_score), align = "center", font = ("Arial", 20, "bold"))
                win.update()
                sleep(3)
                t.bye()
                write_score()
                webbrowser.open("scores.html")
                os.system("taskkill /f /im pythonw.exe")
        
win.listen()
player_name = win.textinput("Name", "Enter Player Name:")
t.color("white")
intro = [t.Turtle(), t.Turtle(), t.Turtle()]
t.up()
t.setposition(0, 200)
intro[0].up()
intro[1].up()
t.write("Instructions", align = "center", font = ("Arial", 20, "bold"))
win.update()
for i in range(len(intro)):
    if(i==0):
        intro[0].ht()
        intro[0].shape("arrow_keys.gif")
        intro[0].setposition(-200, 140)
        t.setposition(-200, 40)
        t.write("SpaceCraft Movement", align = "center", font = ("Arial", 20, "bold"))
        intro[0].st()
        win.update()
    if(i==1):
        intro[1].ht()
        intro[1].shape("space_key.gif")
        intro[1].setposition(200, 140)
        t.setposition(200, 40)
        t.write("Shoot Laser", align = "center", font = ("Arial", 20, "bold"))
        intro[1].st()
        win.update()
    if(i==2):
        intro[2].ht()
        intro[2].shape("esc_key.gif")
        intro[2].setposition(-75, -100)
        t.setposition(50, -115)
        t.write("Exit Game", align = "center", font = ("Arial", 20, "bold"))
        intro[2].st()
        win.update()

threading.Thread(target = lambda: wave_object.play(-1), daemon = True).start()
win.onkey(lambda: os.system("taskkill /f /im pythonw.exe"), "Escape")
t.setposition(0, -200)
t.write("Press Enter To Continue", align = "center", font = ("Arial", 20, "bold"))
win.update()
sleep(3)

win.listen()
win.onkey(start, "Return")
t.mainloop()
