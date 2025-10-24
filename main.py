import customtkinter as ctk
from tkinter import filedialog
from modules.globalvar import GlobalVar
from modules.searchagent import bfs_steps, dfs_steps, set_start_end
from modules.utils import checkbox_event, print_logs_label, change_delay
import math

root = ctk.CTk()
global_object = GlobalVar()

root.geometry(f"{global_object.get_win_size()}")
root.title(global_object.window_name)
root.configure(fg_color = global_object.bg_color)
root.resizable(False, False)

main_frame = ctk.CTkFrame(root, width = global_object.get_attrs("main", "width"), height = global_object.get_attrs("main", "height"), fg_color = global_object.bg_color, corner_radius = global_object.corner_radius)
main_frame.pack(side = ctk.LEFT, padx = global_object.padding, pady = global_object.padding)

left_frame = ctk.CTkFrame(main_frame, width = global_object.get_attrs("left", "width"), height = global_object.get_attrs("left", "height"), fg_color = global_object.fg_color, corner_radius = 0, border_width = global_object.border_width, border_color = global_object.button_hover_color)
left_frame.pack(side = ctk.LEFT)
left_frame.pack_propagate(False)

right_frame = ctk.CTkFrame(main_frame, width = global_object.get_attrs("right", "width"), height = global_object.get_attrs("right", "height"), fg_color = global_object.bg_color)
right_frame.pack(side = ctk.RIGHT, anchor = "nw", padx = (global_object.gap, 0))
right_frame.pack_propagate(False)

option_label = ctk.CTkLabel(right_frame, text = "Algoritma Searching:", text_color = global_object.fg_color, font = global_object.font_style_1)
option_label.pack(anchor = "nw")

options_var = ctk.StringVar(value = "BFS")

options_frame = ctk.CTkFrame(right_frame, fg_color = global_object.bg_color, width = global_object.get_attrs("right", "width"))
options_frame.pack(anchor = "nw", pady = (global_object.gap / 2, 0))

options_left_frame = ctk.CTkFrame(options_frame, fg_color = global_object.bg_color, width = global_object.get_attrs("right", "width"))
options_left_frame.pack(side = ctk.LEFT, anchor = "nw")

options_right_frame = ctk.CTkFrame(options_frame, fg_color = global_object.bg_color, width = global_object.get_attrs("right", "width"))
options_right_frame.pack(side = ctk.RIGHT, anchor = "nw")

bfs_button = ctk.CTkCheckBox(options_left_frame, text = "BFS", command = lambda: checkbox_event(options_var, "BFS"), variable = options_var, onvalue = "BFS", offvalue = "DFS", fg_color = global_object.button_color, hover_color = global_object.button_hover_color, border_width = global_object.border_width, border_color = global_object.button_hover_color)
bfs_button.pack(side = ctk.LEFT)

dfs_button = ctk.CTkCheckBox(options_left_frame, text = "DFS", command = lambda: checkbox_event(options_var, "DFS"), variable = options_var, onvalue = "DFS", offvalue = "BFS", fg_color = global_object.button_color, hover_color = global_object.button_hover_color, border_width = global_object.border_width, border_color = global_object.button_hover_color)
dfs_button.pack(side = ctk.RIGHT)

delay_entry = ctk.CTkEntry(options_right_frame, placeholder_text = "Delay (ms) [contoh: 200]", width = global_object.get_attrs("right", "width") / 2, font = global_object.font_style_2, fg_color = global_object.button_color, text_color = global_object.fg_color, border_color = global_object.button_hover_color, border_width = global_object.border_width, corner_radius = global_object.corner_radius)
delay_entry.pack(anchor = "nw", padx = (global_object.gap / 2, 0))
delay_entry.delete(0, ctk.END)
delay_entry.insert(0, global_object.global_animation_delay)
delay_entry.bind("<Return>", lambda: change_delay(None, logs_label, delay_entry, ctk))

input_label = ctk.CTkLabel(right_frame, text = "Ukuran Maze:", text_color = global_object.fg_color, font = global_object.font_style_1)
input_label.pack(anchor = "nw", pady = (global_object.gap, 0))

def fill_frames(map_data: list[list[int]], map_size: tuple[int, int] = (0, 0), char_pos: tuple[int, int] = (0, 0), execute = False) -> None:
    if map_data == [[]] or map_size == (0, 0):
        return
    
    rows = len(map_data)
    cols = len(map_data[0]) if rows > 0 else 0

    if global_object.global_char_pos == (0, 0) or (global_object.global_char_pos[0] < 1 or global_object.global_char_pos[1] < 1) or (global_object.global_char_pos[0] > rows or global_object.global_char_pos[1] > cols):
        print_logs_label(logs_label, "Posisi Mr. Groovy tidak boleh berada diluar maze", log_type = "err")
        return

    if not global_object.global_cell_frames or len(global_object.global_cell_frames) != rows or len(global_object.global_cell_frames[0]) != cols:
        for widget in left_frame.winfo_children():
            widget.destroy()

        global_object.global_cell_frames = []
        cell_size = (math.floor(global_object.get_attrs("left", "width") / cols), math.floor(global_object.get_attrs("left", "height") / rows))

        for i in range(rows):
            row_cells = []

            for j in range(cols):
                frame = ctk.CTkFrame(left_frame, width = cell_size[0], height = cell_size[1], fg_color = global_object.fg_color, border_width = 1, border_color = global_object.bg_color, corner_radius = 0)
                frame.grid(row = i, column = j)
                frame.grid_propagate(False)

                emoji_label = ctk.CTkLabel(frame, text = "", font = (global_object.font_family, math.floor(cell_size[0] / 2)))
                emoji_label.place(relx = 0.5, rely = 0.5, anchor = "center")

                row_cells.append((frame, emoji_label))

            global_object.global_cell_frames.append(row_cells)

    char_pos = (int(char_pos[0]) - 1, int(char_pos[1]) - 1)
    char_pos = (0, 0) if char_pos[0] < 0 or char_pos[1] < 0 else char_pos
    char_pos_fill = False

    for i in range(rows):
        for j in range(cols):
            frame, emoji_label = global_object.global_cell_frames[i][j]
            is_groovy = False

            if (i, j) == char_pos and not char_pos_fill and not execute and map_data[i][j] != -1:
                char_pos_fill = True
                color = global_object.mr_groovy_color
                is_groovy = True
            elif map_data[i][j] == 2 and execute:
                char_pos_fill = True
                color = global_object.mr_groovy_color
                is_groovy = True
            elif map_data[i][j] == -1:
                color = global_object.wall_color
            elif map_data[i][j] == 1:
                color = global_object.passed_path_color
            elif map_data[i][j] == -2:
                color = global_object.stepped_path_color
            else:
                color = global_object.fg_color

            if is_groovy:
                emoji_label.configure(text = "\U0001F60A", text_color = global_object.fg_color)
            else:
                emoji_label.configure(text = "")

            frame.configure(fg_color = color)

def size_input(event: any = None) -> None:
    current_value: str = size_entry.get()
    maze_size = current_value.split(" ")

    try:
        if int(maze_size[0]) < 3 or int(maze_size[1]) < 3 or int(maze_size[0]) > 10 or int(maze_size[1]) > 10:
            print_logs_label(logs_label, "Ukuran maze harus >= 3 dan <= 10", log_type = "err")

            if global_object.global_maze_coor is not None or global_object.global_maze_coor != [[]] or len(global_object.global_maze_coor) >= 3:
                rows = len(global_object.global_maze_coor)
                cols = len(global_object.global_maze_coor[0]) if rows > 0 else 0

                global_object.global_maze_size = (rows, cols)
                maze_size_str = f"{rows} {cols}"
                size_entry.delete(0, ctk.END)
                size_entry.insert(0, maze_size_str)

            return

        if len(maze_size) != 2:
            maze_size = (0, 0)
            global_object.global_maze_size = maze_size
        else:
            global_object.global_maze_size = tuple(map(int, maze_size))

            fill_frames(global_object.global_maze_coor, global_object.global_maze_size, global_object.global_char_pos)
    except Exception:
        size_entry.delete(0, ctk.END)
        return

def coor_input(event: any = None) -> None:
    try:
        current_value: str = coor_textbox.get("0.0", ctk.END)
        lines = [line.strip() for line in current_value.splitlines() if line.strip()]
        maze_map = [list(map(int, line.split())) for line in lines] 

        if len(maze_map) > 0:
            rows = len(maze_map)
            cols = len(maze_map[0]) if rows > 0 else 0

            if rows < 3 or rows > 10 or cols < 3 or cols > 10:
                print_logs_label(logs_label, "Ukuran maze harus >= 3 dan <= 10", log_type = "err")
                return

            global_object.global_maze_size = (rows, cols)
            global_object.global_maze_coor = maze_map

            size_entry.delete(0, ctk.END)
            size_entry.insert(ctk.END, " ".join((str(rows), str(cols))))

            fill_frames(global_object.global_maze_coor, global_object.global_maze_size, global_object.global_char_pos)
    except Exception:
        coor_textbox.delete("0.0", ctk.END)
        return

def pos_input(event: any = None) -> None:
    current_value: str = pos_entry.get()
    char_pos = current_value.split(" ")

    try:
        if len(char_pos) != 2:
            char_pos = (0, 0)
            global_object.global_char_pos = char_pos
        else:
            global_object.global_char_pos = tuple(map(int, char_pos))

            fill_frames(global_object.global_maze_coor, global_object.global_maze_size, global_object.global_char_pos)
    except Exception:
        pos_entry.delete(0, ctk.END)
        return

size_entry = ctk.CTkEntry(right_frame, placeholder_text = "Ukuran maze (x, y) [contoh: 8 10]", width = global_object.get_attrs("right", "width"), font = global_object.font_style_2, fg_color = global_object.button_color, text_color = global_object.fg_color, border_color = global_object.button_hover_color, border_width = global_object.border_width, corner_radius = global_object.corner_radius)
size_entry.pack(anchor = "nw", pady = (global_object.gap / 2, 0))
size_entry.bind("<Return>", size_input)

coor_input_label = ctk.CTkLabel(right_frame, text = "Struktur Maze:", text_color = global_object.fg_color, font = global_object.font_style_1)
coor_input_label.pack(anchor = "nw", pady = (global_object.gap, 0))

coor_textbox = ctk.CTkTextbox(right_frame, width = global_object.get_attrs("right", "width"), height = global_object.get_attrs("right", "height") / 6, font = global_object.font_style_2, fg_color = global_object.button_color, text_color = global_object.fg_color, border_color = global_object.button_hover_color, border_width = global_object.border_width, corner_radius = global_object.corner_radius)
coor_textbox.pack(anchor = "nw", pady = (global_object.gap / 2, 0))
coor_textbox.bind("<Return>", coor_input)

pos_label = ctk.CTkLabel(right_frame, text = "Posisi Mr. Groovy:", text_color = global_object.fg_color, font = global_object.font_style_1)
pos_label.pack(anchor = "nw", pady = (global_object.gap, 0))

pos_entry = ctk.CTkEntry(right_frame, placeholder_text = "Posisi Mr. Groovy (x, y) [contoh: 7 5]", width = global_object.get_attrs("right", "width"), font = global_object.font_style_2, fg_color = global_object.button_color, text_color = global_object.fg_color, border_color = global_object.button_hover_color, border_width = global_object.border_width, corner_radius = global_object.corner_radius)
pos_entry.pack(anchor = "nw", pady = (global_object.gap / 2, 0))
pos_entry.bind("<Return>", pos_input)

other_label = ctk.CTkLabel(right_frame, text = "Input File Text (opsional):", text_color = global_object.fg_color, font = global_object.font_style_1)
other_label.pack(anchor = "nw", pady = (global_object.gap, 0))

def open_file(button_pressed: bool = True) -> None:
    file_path: str

    if button_pressed:
        file_path = filedialog.askopenfilename(title = "Pilih File Maze", filetypes = [("Text Files", "*.txt"), ("All Files", "*.*")])
    else:
        file_path = file_entry.get()
        file_path = file_path.strip()
    
    if file_path:
        if button_pressed:
            file_entry.delete(0, ctk.END)
            file_entry.insert(0, file_path)

        try:
            with open(file_path, "r") as file:
                content = file.read()

                lines = [line.strip() for line in content.splitlines() if line.strip()]
                maze_size = " ".join(lines[0].split())
                maze_map = [list(map(int, line.split())) for line in lines[1: -1]]
                maze_map_str = '\n'.join([" ".join(line.split()) for line in lines[1: -1]])
                rows = len(maze_map)
                cols = len(maze_map[0]) if rows > 0 else 0
                pos_list = lines[-1].split()

                if rows < 3 or rows > 10 or cols < 3 or cols > 10:
                    print_logs_label(logs_label, "Ukuran maze harus >= 3 dan <= 10", log_type = "err")

                    global_object.global_maze_size = (rows, cols)
                    maze_size_str = f"{rows} {cols}"
                    size_entry.delete(0, ctk.END)
                    size_entry.insert(0, maze_size_str)

                    return

                if len(maze_size.split(" ")) != 2:
                    maze_size = f"{rows} {cols}"

                if len(pos_list) != 2:
                    pos_list = ("0", "0")

                pos = " ".join(pos_list)

                size_entry.delete(0, ctk.END)
                size_entry.insert(ctk.END, maze_size)

                coor_textbox.delete("0.0", ctk.END)
                coor_textbox.insert(ctk.END, maze_map_str)

                pos_entry.delete(0, ctk.END)
                pos_entry.insert(ctk.END, pos)

                global_object.global_maze_size = (rows, cols)
                global_object.global_maze_coor = maze_map
                global_object.global_char_pos = tuple(map(int, pos_list))

                maze_size_list = maze_size.split(" ")

                fill_frames(maze_map, (int(maze_size_list[0]), int(maze_size_list[1])), lines[-1].split())
        except Exception:
            pass

def animate_bfs(maze_map: list[list[int]], goal: tuple[int, int]) -> tuple[int, str]:
    steps = list(bfs_steps(global_object.global_directions, maze_map, goal))
    step_index = 0

    def next_step():
        nonlocal step_index

        if step_index < len(steps):
            if not global_object.global_is_executing:
                global_object.global_is_executing = True

            fill_frames(steps[step_index], global_object.global_maze_size, execute = True)

            step_index += 1
            root.after(global_object.global_animation_delay, next_step)
        else:
            global_object.global_is_executing = False

    next_step()

    path_len = sum(val in (1, 2) for row in steps[-1] for val in row)
    
    return (len(steps), options_var.get(), path_len)

def animate_dfs(maze_map: list[list[int]], goal: tuple[int, int]) -> tuple[int, str]:
    steps = list(dfs_steps(global_object.global_directions, maze_map, goal))
    step_index = 0

    def next_step():
        nonlocal step_index

        if step_index < len(steps):
            if not global_object.global_is_executing:
                global_object.global_is_executing = True

            fill_frames(steps[step_index], global_object.global_maze_size, execute = True)

            step_index += 1
            root.after(global_object.global_animation_delay, next_step)
        else:
            global_object.global_is_executing = False

    next_step()

    path_len = sum(val in (1, 2) for row in steps[-1] for val in row)

    return (len(steps), options_var.get(), path_len)
            
def execute_maze(event: any = None) -> None:
    if global_object.global_is_executing:
        return

    current_maze_size: str = size_entry.get()
    current_maze_size = current_maze_size.strip()

    if current_maze_size == "" or current_maze_size is None:
        print_logs_label(logs_label, "Ukuran maze belum terisi", log_type = "err")
        return

    current_maze_coor: str = coor_textbox.get("0.0", ctk.END)
    current_maze_coor = current_maze_coor.strip()

    if current_maze_coor == "" or current_maze_coor is None:
        print_logs_label(logs_label, "Struktur maze belum terisi", log_type = "err")
        return

    current_char_pos: str = pos_entry.get()
    current_char_pos = current_char_pos.strip()

    if current_char_pos == "" or current_char_pos is None:
        print_logs_label(logs_label, "Posisi Mr. Groovy belum terisi", log_type = "err")
        return

    rows = len(global_object.global_maze_coor)
    cols = len(global_object.global_maze_coor[0]) if rows > 0 else 0

    if (global_object.global_maze_size[0] != rows or global_object.global_maze_size[1] != cols) and (rows > 0 and cols > 0):
        print_logs_label(logs_label, "Ukuran maze tidak sama dengan struktur maze", log_type = "err")

        global_object.global_maze_size = (rows, cols)
        maze_size_str = f"{rows} {cols}"
        size_entry.delete(0, ctk.END)
        size_entry.insert(0, maze_size_str)

        return
    
    option_value = options_var.get()

    global_object.global_goal = set_start_end(global_object.global_maze_coor, global_object.global_char_pos)

    steps, method = (0, option_value)
    path_len = 0

    if global_object.global_goal != []:
        if option_value == "BFS":
            steps, method, path_len = animate_bfs(global_object.global_maze_coor, global_object.global_goal)
        elif option_value == "DFS":
            steps, method, path_len = animate_dfs(global_object.global_maze_coor, global_object.global_goal)
    else:
        print_logs_label(logs_label, "Tidak ada tujuan (goal) yang ditemukan")
        return

    if steps == 0:
        print_logs_label(logs_label, f"Tidak ada solusi dengan algoritma {method}")
    else:
        print_logs_label(logs_label, f"Terdapat total {steps} langkah dan {path_len} langkah untuk jalur terpendak\ndengan algoritma {method}")

file_frame = ctk.CTkFrame(right_frame, width = global_object.get_attrs("right", "width"), fg_color = global_object.bg_color)
file_frame.pack(anchor = "nw", pady = (global_object.gap / 2, 0))

file_entry = ctk.CTkEntry(file_frame, placeholder_text = "Pilih file text", width = (global_object.get_attrs("right", "width") / 2) + global_object.padding * 2, font = global_object.font_style_2, fg_color = global_object.button_color, text_color = global_object.fg_color, border_color = global_object.button_hover_color, border_width = global_object.border_width, corner_radius = global_object.corner_radius)
file_entry.pack(side = ctk.LEFT)
file_entry.bind("<Return>", lambda event: open_file(False))

browse_button = ctk.CTkButton(file_frame, text = "Browse File", command = open_file, fg_color = global_object.button_color, hover_color = global_object.button_hover_color, text_color = global_object.fg_color, corner_radius = global_object.corner_radius)
browse_button.pack(side = ctk.RIGHT, padx = (global_object.gap / 2, 0))

buttons_frame = ctk.CTkFrame(right_frame, width = global_object.get_attrs("right", "width"), fg_color = global_object.bg_color)
buttons_frame.pack(anchor = "sw", pady = (global_object.gap / 2, 0))

execute_button = ctk.CTkButton(buttons_frame, command = execute_maze, text = "Eksekusi Program", width = global_object.get_attrs("right", "width"), fg_color = global_object.button_color, hover_color = global_object.button_hover_color, text_color = global_object.fg_color, corner_radius = global_object.corner_radius)
execute_button.pack(side = ctk.RIGHT, anchor = "sw", pady = (global_object.gap / 2, 0))

logs_frame = ctk.CTkFrame(right_frame, width = global_object.get_attrs("right", "width"), fg_color = global_object.button_color)
logs_frame.pack(anchor = "sw", pady = (global_object.gap, 0))
logs_frame.pack_propagate(False)

logs_label = ctk.CTkLabel(logs_frame, text = "Tidak ada log", text_color = global_object.fg_color, font = global_object.font_style_2, justify = "left")
logs_label.pack(anchor = "nw", padx = global_object.gap / 2, pady = global_object.gap / 4)

root.mainloop()