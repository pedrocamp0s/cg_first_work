import tkinter as tk
import math
import matplotlib.path as mplPath
from tkinter import StringVar, font
from tkinter.constants import CENTER, DISABLED, LEFT, NORMAL, RIGHT
import numpy as np

CANVAS_MAXWIDTH = 400
CANVAS_MAXHEIGHT = 400

'''
Criação do polígono definido pelos pontos escolhidos pelo usuário
'''

def create_polygon():
    global polygon, points
    polygon = canvas.create_polygon(points, fill="blue")

'''
Executa a rotação do polígono já criado
levando em conta o ângulo escolhido pelo usuário
na interface, transladando o objeto para a origem
antes de fazer a rotação e voltando pro seu centro anterior após a rotação
'''

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

'''
Faz a reflexão do polígono levando em conta a opção cartesiana
definida pelo usuário na interface. Para essa operação, primeiro
temos a transposta da matriz de pontos, de forma que cada linha tenha 
apenas X ou apenas Y, multiplicando a matriz de pontos pela matriz de transformação
de cada eixo. Ao fim da operação, é somado o valor do Width ou do Height do Canvas
para colocar o polígono sempre na tela, já que o Canvas não tem pixels negativos.
'''

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

'''
Realiza a operação de escala no polígono,
multiplicando o X e o Y pelos valores definidos
pelo usuário na interface.
'''

def scale(e):
    if(menu_open and polygon_exists):
        global points
        if(e.delta > 0):
            points = [[x*float(scale_factor_x.get()), y*float(scale_factor_y.get())] for x,y in points]
        else:
            points = [[x*(1/float(scale_factor_x.get())), y*(1/float(scale_factor_y.get()))] for x,y in points]
        canvas.delete(polygon)
        create_polygon()

'''
É executado automaticamente quando o usuário fecha o menu
configurando a interface para mostrar o botão de abrir menu novamente
e esconder o canvas.
'''

def on_closing():
    global menu_open
    menu_open = False
    menu_button.place(anchor=CENTER, relx=0.5, rely=0.5)
    canvas.pack_forget()
    menu_window.destroy()

'''
É executada automaticamente quando o usuário
começa a desenhar o polígono, setando a variável
de controle para saber quando finalizar o desenho.
'''

def start_to_draw():
    global is_drawing
    is_drawing = True
    start_polygon_button.configure(state=DISABLED)

'''
É executada automaticamente quando o usuário termina de desenhar o polígono,
unindo os pontos inseridos pelo usuário e criando o polígono a partir
desses pontos.
'''

def end_draw():
    global is_drawing, polygon_exists
    is_drawing = False
    polygon_exists = True
    end_polygon_button.configure(state=DISABLED)
    rotation_button.configure(state=NORMAL)
    reflection_button.configure(state=NORMAL)
    delete_polygon_button.configure(state=NORMAL)
    create_polygon()

'''
Remove o polígono desenhado anteriormente.
'''


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

'''
Executa o algoritmo de DDA para inserir 
a reta no Canvas, de acordo com os dois pontos
escolhidos pelo usuário.
'''

def dda_algorithm():
    global draw_line_dda, straight_points, lines
    if(draw_line_dda):
        draw_line_dda = False
        start_point = straight_points[0]
        end_point = straight_points[1]
        delta_x = end_point[0] - start_point[0]
        delta_y = end_point[1] - start_point[1]
        x_operator = 1 if delta_x > 0 else -1
        y_operator = 1 if delta_y > 0 else -1
        delta_x = abs(delta_x)
        delta_y = abs(delta_y)
        m = delta_y/delta_x
        if(m >= 1):
            x = start_point[0]
            y = start_point[1]
            straight_points = [[x, y]]
            while x != end_point[0] and y != end_point[1]:
                y += 1 * y_operator
                x += (1/m) * x_operator
                straight_points.append([x, y])
            straight_points = [[round(x), y] for x,y in straight_points]
        else:
            x = start_point[0]
            y = start_point[1]
            straight_points = [[x, y]]
            while x != end_point[0] and y != end_point[1]:
                y += m * y_operator
                x += 1 * x_operator
                straight_points.append([x, y])
            straight_points = [[x, round(y)] for x, y in straight_points]
        line = canvas.create_line(straight_points)
        lines.append(line)
    else:
        draw_line_dda = True
        straight_points = []
        

'''
Executa o algoritmo de bresenham para
desenhar a reta no canvas de acordo com os dois
pontos escolhidos pelo usuário.
'''

def bresenham_algorithm():
    global draw_line_bre, straight_points, lines
    if(draw_line_bre):
        draw_line_bre = False
        start_point = straight_points[0]
        end_point = straight_points[1]
        delta_x = end_point[0] - start_point[0]
        delta_y = end_point[1] - start_point[1]
        x_operator = 1 if delta_x > 0 else -1
        y_operator = 1 if delta_y > 0 else -1
        delta_x = abs(delta_x)
        delta_y = abs(delta_y)
        if(delta_x >= delta_y):
            p = 2 * delta_y - delta_x
            c1 = 2 * delta_y
            c2 = 2 * (delta_y - delta_x)
            x = start_point[0]
            y = start_point[1]
            while x != end_point[0] and y != end_point[1]:
                if(p < 0):
                    x += 1 * x_operator
                    p += c1
                else:
                    x += 1 * x_operator
                    y += 1 * y_operator
                    p += c2
                straight_points.append([x, y])
        else:
            p = 2 * delta_x - delta_y
            c1 = 2 * delta_x
            c2 = 2 * (delta_x - delta_y)
            x = start_point[0]
            y = start_point[1]
            while x != end_point[0] and y != end_point[1]:
                if(p < 0):
                    y += 1 * y_operator
                    p += c1
                else:
                    x += 1 * x_operator
                    y += 1 * y_operator
                    p += c2
                straight_points.append([x, y])
        line = canvas.create_line(straight_points)
        lines.append(line)
    else :
        draw_line_bre = True
        straight_points = []


'''
Remove a última linha inserida, seja pelo algoritmo de DDA
ou pelo de Bresenham.
'''

def remove_line():
    if(len(lines) > 0):
        canvas.delete(lines.pop())

'''
Define o menu na interface, inserindo todos os botões
necessários para utilizar o programa.
'''

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

    rasterization_frame = tk.LabelFrame(menu_window, text="Rasterização", font=("Arial", "12", "bold"))
    rasterization_frame.pack(pady=10)
    dda_button = tk.Button(rasterization_frame, text="Usar DDA", command=dda_algorithm)
    dda_button.pack()
    bresenham_button = tk.Button(rasterization_frame, text="Usar bresenham", command=bresenham_algorithm)
    bresenham_button.pack()
    delete_line_button = tk.Button(rasterization_frame, text="Deletar linha", command=remove_line)
    delete_line_button.pack()

    menu_window.protocol("WM_DELETE_WINDOW", on_closing)

'''
Função executada quando o usuário clica em algum ponto do Canvas,
utilizado em várias aplicações para pegar um ponto inicial
e um ponto final.
'''

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
        
'''
Função utilizada para finalizar o clique iniciado pelo usuário
em outra função, executado automaticamente assim que o usuário
solta o botão do mouse.
'''


def endmouse(position):
    global straight_points
    if(draw_line_dda):
        if(len(straight_points) == 1):
            straight_points.append([position.x, position.y])
            dda_algorithm()
        else:
            straight_points.append([position.x, position.y])
        return
    
    if(draw_line_bre):
        if(len(straight_points) == 1):
            straight_points.append([position.x, position.y])
            bresenham_algorithm()
        else:
            straight_points.append([position.x, position.y])
        return
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
draw_line_dda = False
draw_line_bre = False
rotation_angle = StringVar()
scale_factor_x = StringVar()
scale_factor_y = StringVar()
reflect_to = StringVar()
menu_open = False
points = []
straight_points = []
lines = []

root.bind('<Button-1>', startmouse)
root.bind('<ButtonRelease-1>', endmouse)
root.bind("<MouseWheel>", scale)
root.mainloop()