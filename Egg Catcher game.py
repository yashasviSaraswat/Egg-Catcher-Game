from itertools import cycle
from random import randrange, randint
from tkinter import Tk, Canvas, messagebox

canvas_width = 800
canvas_height = 400

win = Tk()
win.title("Egg Catcher Game")

c = Canvas(win, width=canvas_width, height=canvas_height, background='deep sky blue')
c.create_rectangle(-5, canvas_height - 100, canvas_width + 5, canvas_height + 5, fill='sea green', width=0)
c.create_oval(-80, -80, 120, 120, fill='orange', width=0)
c.pack()

color_cycle = cycle(['light blue', 'light pink', 'light yellow', 'light green', 'red', 'blue', 'green', 'black'])
egg_width = 45
egg_height = 55
egg_score = 10
egg_speed = 300
egg_interval = 3000
difficulty_factor = 0.95

catcher_color = 'blue'
catcher_width = 100
catcher_height = 100
catcher_start_x = canvas_width / 2 - catcher_width / 2
catcher_start_y = canvas_height - catcher_height - 20
catcher_start_x2 = catcher_start_x + catcher_width
catcher_start_y2 = catcher_start_y + catcher_height

catcher = c.create_arc(catcher_start_x, catcher_start_y, catcher_start_x2, catcher_start_y2,
                       start=200, extent=140, style='arc', outline=catcher_color, width=3)

score = 0
score_text = c.create_text(10, 10, anchor='nw', font=('Arial', 18, 'bold'),
                           fill='darkblue', text='Score : ' + str(score))

lives_remaining = 3
lives_text = c.create_text(canvas_width - 10, 10, anchor='ne', font=('Arial', 18, 'bold'),
                           fill='darkblue', text='Lives : ' + str(lives_remaining))

eggs = []

def create_eggs():
    x = randrange(10, canvas_width - egg_width)
    y = 40
    new_egg = c.create_oval(x, y, x + egg_width, y + egg_height, fill=next(color_cycle), width=0)
    eggs.append(new_egg)
    win.after(egg_interval, create_eggs)

def move_eggs():
    for egg in eggs[:]:
        (egg_x, egg_y, egg_x2, egg_y2) = c.coords(egg)
        c.move(egg, 0, 10)
        if egg_y2 > canvas_height - 20:
            egg_dropped(egg)
    win.after(egg_speed, move_eggs)

def create_splash_effect(x1, x2, y2):
    splash_x = (x1 + x2) / 2
    splash_y = min(y2, canvas_height - 30)
    splash_parts = []

    for _ in range(8):  # Simulate shell + yolk bursts
        dx = randint(-20, 20)
        dy = randint(-10, 10)
        size = randint(6, 14)
        color = 'yellow' if randint(0, 1) else 'white'
        part = c.create_oval(splash_x + dx, splash_y + dy,
                             splash_x + dx + size, splash_y + dy + size,
                             fill=color, width=0)
        splash_parts.append(part)

    # Clear the splash after 600ms
    win.after(600, lambda: [c.delete(p) for p in splash_parts])

def egg_dropped(egg):
    if egg in eggs:
        eggs.remove(egg)
        (x1, y1, x2, y2) = c.coords(egg)
        c.delete(egg)
        create_splash_effect(x1, x2, y2)
        lose_a_life()
        if lives_remaining == 0:
            messagebox.showinfo('GAME OVER!', 'Final Score: ' + str(score))
            win.destroy()

def lose_a_life():
    global lives_remaining
    lives_remaining -= 1
    c.itemconfigure(lives_text, text='Lives : ' + str(lives_remaining))

def catch_check():
    (catcher_x, catcher_y, catcher_x2, catcher_y2) = c.coords(catcher)
    for egg in eggs[:]:
        (egg_x, egg_y, egg_x2, egg_y2) = c.coords(egg)
        if catcher_x < egg_x and egg_x2 < catcher_x2 and catcher_y2 - egg_y2 < 40:
            eggs.remove(egg)
            c.delete(egg)
            increase_score(egg_score)
    win.after(100, catch_check)

def increase_score(points):
    global score, egg_speed, egg_interval
    score += points
    egg_speed = int(egg_speed * difficulty_factor)
    egg_interval = int(egg_interval * difficulty_factor)
    c.itemconfigure(score_text, text='Score : ' + str(score))

def move_left(event):
    (x1, y1, x2, y2) = c.coords(catcher)
    if x1 > 0:
        c.move(catcher, -20, 0)

def move_right(event):
    (x1, y1, x2, y2) = c.coords(catcher)
    if x2 < canvas_width:
        c.move(catcher, 20, 0)

c.bind('<Left>', move_left)
c.bind('<Right>', move_right)
c.focus_set()

win.after(1000, create_eggs)
win.after(1000, move_eggs)
win.after(1000, catch_check)

win.mainloop()

