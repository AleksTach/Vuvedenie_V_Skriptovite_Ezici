import turtle
import random

screen = turtle.Screen()
screen.title("Snowman")
screen.bgcolor("#87CEEB")
screen.setup(800, 600)
screen.tracer(0)

t = turtle.Turtle()
t.hideturtle()
t.speed(0)

def draw_filled_circle(x, y, radius, color, outline_color="black", outline_width=1):
    t.penup()
    t.goto(x, y - radius)
    t.pendown()
    t.color(outline_color, color)
    t.pensize(outline_width)
    t.begin_fill()
    t.circle(radius)
    t.end_fill()

def draw_tree(x, y, width, height):
    trunk_w = width / 3
    trunk_h = height / 4
    t.penup()
    t.goto(x - trunk_w/2, y)
    t.pendown()
    t.color("#5D4037", "#8D6E63")
    t.begin_fill()
    for _ in range(2):
        t.forward(trunk_w)
        t.left(90)
        t.forward(trunk_h)
        t.left(90)
    t.end_fill()
    
    t.color("#1B5E20", "#2E7D32")
    layers = 3
    layer_h = (height - trunk_h) / layers
    current_y = y + trunk_h
    current_w = width
    
    for i in range(layers):
        t.penup()
        t.goto(x - current_w/2, current_y)
        t.pendown()
        t.begin_fill()
        t.setheading(0)
        t.forward(current_w)
        t.goto(x, current_y + layer_h * 1.5)
        t.goto(x - current_w/2, current_y)
        t.end_fill()
        current_y += layer_h * 0.8
        current_w *= 0.7

def draw_forest():
    positions = [-350, -275, -200, 200, 275, 350]
    for x in positions:
        w = random.randint(70, 90)
        h = random.randint(120, 160)
        draw_tree(x, -250, w, h)

def draw_snowflakes():
    t.color("white")
    for _ in range(50):
        x = random.randint(-400, 400)
        y = random.randint(-300, 300)
        size = random.randint(5, 10)
        t.penup()
        t.goto(x, y)
        t.pendown()
        t.begin_fill()
        for _ in range(5):
            t.forward(size)
            t.right(144)
        t.end_fill()

def draw_snowman_body():
    draw_filled_circle(0, -180, 70, "white", "#E0E0E0")
    draw_filled_circle(0, -70, 50, "white", "#E0E0E0")
    draw_filled_circle(0, 10, 35, "white", "#E0E0E0")

def draw_face():
    draw_filled_circle(-12, 25, 4, "black")
    draw_filled_circle(12, 25, 4, "black")
    draw_filled_circle(-10, 27, 1.5, "white", "white")
    draw_filled_circle(14, 27, 1.5, "white", "white")
    
    t.penup()
    t.goto(0, 20)
    t.pendown()
    t.color("#E65100", "orange")
    t.begin_fill()
    t.goto(0, 10)
    t.goto(25, 15)
    t.goto(0, 20)
    t.end_fill()
    
    t.color("black")
    for i in range(5):
        mx = -16 + (i * 8)
        my = 0 + (mx**2 / 50)
        draw_filled_circle(mx, my, 2.5, "black")

def draw_hat():
    t.penup()
    t.goto(-40, 35)
    t.setheading(0)
    t.pendown()
    t.color("black", "black")

    # Brim
    t.begin_fill()
    t.forward(80)
    t.left(90)
    t.forward(10)
    t.left(90)
    t.forward(80)
    t.left(90)
    t.forward(10)
    t.end_fill()

    # Top part
    t.penup()
    t.goto(-25, 45)
    t.setheading(0)
    t.pendown()
    t.begin_fill()
    t.forward(50)
    t.left(90)
    t.forward(40) 
    t.left(90)
    t.forward(50)
    t.left(90) 
    t.forward(40) 
    t.end_fill()

    # Ribbon
    t.penup()
    t.goto(-25, 50)
    t.setheading(0)
    t.pendown()
    t.color("red")
    t.width(5)
    t.forward(50)
    t.width(1)

def draw_arms():
    t.color("#5D4037")
    t.pensize(4)
    
    t.penup()
    t.goto(-45, -50)
    t.pendown()
    t.setheading(160)
    t.forward(50)
    t.left(30)
    t.forward(15)
    t.backward(15)
    t.right(60)
    t.forward(15)
    t.backward(15)
    
    t.penup()
    t.goto(45, -50)
    t.pendown()
    t.setheading(20)
    t.forward(50)
    t.left(30)
    t.forward(15)
    t.backward(15)
    t.right(60)
    t.forward(15)
    t.backward(15)

def draw_buttons():
    for y in [-50, -80, -110]:
        draw_filled_circle(0, y, 4, "black")

def draw_scarf():
    t.penup()
    t.goto(-30, -20)
    t.setheading(0)
    t.pendown()
    t.color("#D32F2F")
    t.pensize(10)
    
    t.forward(60)
    
    t.penup()
    t.goto(20, -20)
    t.setheading(270)
    t.pendown()
    t.forward(30)
    t.pensize(1)

def main():
    draw_forest()
    draw_snowflakes()
    draw_snowman_body()
    draw_buttons()
    draw_arms()
    draw_scarf()
    draw_face()
    draw_hat()
    screen.update()
    turtle.done()

if __name__ == "__main__":
    main()