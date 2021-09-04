import tkinter as tk
import math
import matplotlib.path as mplPath
from tkinter import StringVar, font
from tkinter.constants import CENTER, DISABLED, LEFT, NORMAL, RIGHT
import numpy as np

CANVAS_MAXWIDTH = 400
CANVAS_MAXHEIGHT = 400

def create_polygon():
    global polygon, points
    polygon = canvas.create_polygon(points, fill="blue", tags="openmenu")

def rotate():
    global points
    x_points = [point[0] for point in points]
    y_points = [point[1] for point in points]
    polygon_len = len(points)
    center = [sum(x_points)/polygon_len, sum(y_points)/polygon_len]
    angle = math.radians(int(rotation_angle.get()))
    cos = math.cos(angle)
    sin = math.sin(angle)
    new_points = [[x - center[0], y - center[1]] for x,y in points]
    points = [[(x*cos - y*sin) + center[0], (x*sin + y*cos) + center[1]] for x,y in new_points]
    canvas.delete(polygon)
    create_polygon()

def reflection():

    reflect_to_where = reflect_to.get()
    global points
    points_transposed = np.array(points).transpose()

    if(reflect_to_where == "X"):
        transformation_matrix = np.array([[1, 0], [0, -1]])
        reflected_matrix = np.dot(transformation_matrix, points_transposed)
        points = [[x, y + CANVAS_MAXHEIGHT] for x, y in reflected_matrix.transpose().tolist()]
    elif(reflect_to_where == "Y"):
        transformation_matrix = np.array([[-1, 0], [0, 1]])
        reflected_matrix = np.dot(transformation_matrix, points_transposed)
        points = [[x + CANVAS_MAXWIDTH, y] for x, y in reflected_matrix.transpose().tolist()]
    elif(reflect_to_where == "XY"):
        transformation_matrix = np.array([[0, 1], [1, 0]])
        reflected_matrix = np.dot(transformation_matrix, points_transposed)
        points = [[x, y] for x, y in reflected_matrix.transpose().tolist()]

    canvas.delete(polygon)
    create_polygon()

def scale(e):
    if(menu_open and polygon_exists):
        global points
        if(e.delta > 0):
            points = [[x*float(scale_factor_x.get()), y*float(scale_factor_y.get())] for x,y in points]
        else:
            points = [[x*(1/float(scale_factor_x.get())), y*(1/float(scale_factor_y.get()))] for x,y in points]
        canvas.delete(polygon)
        create_polygon()
def on_closing():
    global menu_open
    menu_open = False
    menu_button.place(anchor=CENTER, relx=0.5, rely=0.5)
    canvas.pack_forget()
    menu_window.destroy()

def start_to_draw():
    global is_drawing
    is_drawing = True
    start_polygon_button.configure(state=DISABLED)

def end_draw():
    global is_drawing, polygon_exists
    is_drawing = False
    polygon_exists = True
    end_polygon_button.configure(state=DISABLED)
    rotation_button.configure(state=NORMAL)
    reflection_button.configure(state=NORMAL)
    delete_polygon_button.configure(state=NORMAL)
    create_polygon()

def remove_polygon():
    global points
    canvas.delete(polygon)
    points = []
    start_polygon_button.configure(state=NORMAL)
    end_polygon_button.configure(state=NORMAL)
    rotation_button.configure(state=DISABLED)
    reflection_button.configure(state=DISABLED)
    global polygon_exists
    polygon_exists = False

def show_menu():
    global menu_open
    
    menu_open = True
    menu_button.place_forget()
    canvas.pack()

    canvas.create_polygon([[CANVAS_MAXHEIGHT/2, 0], [CANVAS_MAXHEIGHT/2, CANVAS_MAXHEIGHT]], outline="black", outlineoffset=3)
    canvas.create_polygon([[0, CANVAS_MAXWIDTH/2], [CANVAS_MAXWIDTH, CANVAS_MAXWIDTH/2]], outline="black", outlineoffset=3)
    global menu_window
    menu_window = tk.Toplevel(root)
    menu_window.geometry("200x800")


    draw_polygon_frame = tk.LabelFrame(menu_window, text="Desenhar", font=("Arial", "12", "bold"))
    draw_polygon_frame.pack(pady=10)
    global start_polygon_button, end_polygon_button
    start_polygon_button = tk.Button(draw_polygon_frame, text="Iniciar polígono", command=start_to_draw)
    start_polygon_button.pack(pady=10)
    end_polygon_button = tk.Button(draw_polygon_frame, text="Finalizar polígono", command=end_draw)
    end_polygon_button.pack(pady=10)
    global delete_polygon_button
    delete_polygon_button = tk.Button(draw_polygon_frame, text="Apagar polígono", command=remove_polygon, state=DISABLED)
    delete_polygon_button.pack(pady=10)

    scale_frame = tk.LabelFrame(menu_window, text="Escala", font=("Arial", "12", "bold"))
    scale_frame.pack(pady=10)
    tk.Label(scale_frame, text="X: ", font=("Arial", "10")).grid(row=0, column=0)
    scale_for_x = tk.Entry(scale_frame, textvariable=scale_factor_x)
    scale_for_x.grid(row=0, column=1)
    scale_for_x.insert(0, "1.1")
    tk.Label(scale_frame, text="Y: ", font=("Arial", "10")).grid(row=1, column=0)
    scale_for_y = tk.Entry(scale_frame, textvariable=scale_factor_y)
    scale_for_y.grid(row=1, column=1)
    scale_for_y.insert(0, "1.0")


    rotation_frame = tk.LabelFrame(menu_window, text="Rotação", font=("Arial", "12", "bold"))
    rotation_frame.pack(pady=10)
    global rotation_button
    rotation_button = tk.Button(rotation_frame, text="Rotacionar", command=rotate, state=DISABLED)
    rotation_button.pack(pady=10)
    tk.Label(rotation_frame, text="Ângulo", font=("Arial", "10")).pack(side=LEFT)
    angle_input = tk.Entry(rotation_frame, textvariable=rotation_angle)
    angle_input.pack(side=RIGHT)
    angle_input.insert(0, "45")


    reflection_frame = tk.LabelFrame(menu_window, text="Reflexão", font=("Arial", "12", "bold"))
    reflection_frame.pack(pady=10)
    default_option = tk.Radiobutton(reflection_frame, text="X", variable=reflect_to, value="X")
    default_option.pack()
    default_option.select()
    tk.Radiobutton(reflection_frame, text="Y", variable=reflect_to, value="Y").pack()
    tk.Radiobutton(reflection_frame, text="XY", variable=reflect_to, value="XY").pack()
    global reflection_button
    reflection_button = tk.Button(reflection_frame, text="Reflexão", command=reflection, state=DISABLED)
    reflection_button.pack()


    menu_window.protocol("WM_DELETE_WINDOW", on_closing)

def startmouse(position):
    if(menu_open and polygon_exists):
        if(mplPath.Path(points).contains_point((position.x, position.y))):
            global diff_points, is_moving
            is_moving = True
            diff_points = [
                [position.x - points[0][0], position.y - points[0][1]],
                [position.x - points[1][0], position.y - points[1][1]],
                [position.x - points[2][0], position.y - points[2][1]],
                [position.x - points[3][0], position.y - points[3][1]]
            ]
        

def endmouse(position):
    global points, is_moving
    if(menu_open and polygon_exists and is_moving):
        is_moving = False
        points = [[position.x - x, position.y - y] for x,y in diff_points]
        canvas.delete(polygon)
        create_polygon()
    elif(menu_open and is_drawing):
        points.append([position.x, position.y])



root = tk.Tk()
root.geometry("400x400")
menu_button = tk.Button(root, text="Abrir menu", command=show_menu)
menu_button.place(anchor=CENTER, relx=0.5, rely=0.5)
canvas = tk.Canvas(root, width=CANVAS_MAXWIDTH, height=CANVAS_MAXHEIGHT)

polygon_exists = False
is_moving = False
is_drawing = False
rotation_angle = StringVar()
scale_factor_x = StringVar()
scale_factor_y = StringVar()
reflect_to = StringVar()
menu_open = False
points = []

root.bind('<Button-1>', startmouse)
root.bind('<ButtonRelease-1>', endmouse)
root.bind("<MouseWheel>", scale)
root.mainloop()