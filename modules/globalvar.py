class GlobalVar:
    def __init__(self):
        self.window_name = "Mr. Groovy - Maze Solver"
        self.padding: int = 32
        self.gap: int = 24
        self.win_height: int = 720
        self.win_width: int = 1080
        self.corner_radius: int = 8
        self.border_width: int = 2
        self.font_family: str = "Arial"
        self.font_style_1: tuple[str, int] = (self.font_family, 16)
        self.font_style_2: tuple[str, int] = (self.font_family, 12)
        self.bg_color: str = "#333333"
        self.fg_color: str = "#fdfdfd"
        self.button_color: str = "#555555"
        self.button_hover_color: str = "#646464"
        self.mr_groovy_color: str = "#e14434"
        self.wall_color: str = "#ffc700"
        self.passed_path_color: str = "#ff6f5f"
        self.stepped_path_color: str = "#fff780"
        self.global_maze_size: tuple[int, int] = (0, 0)
        self.global_maze_coor: list[list[int]] = [[]]
        self.global_char_pos: tuple[int, int] = (0, 0)
        self.global_goal: list[tuple[int, int]] = []
        self.global_cell_frames: list[list[any]] = []
        self.global_animation_delay: int = 100
        self.global_directions: list[tuple[int, int]] = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        self.global_is_executing: bool = False
        self.main_frame_attrs = {
            "width": self.win_width - self.padding,
            "height": self.win_height - self.padding
        }
        self.left_frame_attrs = {
            "width": (self.win_width / 2) + (self.padding * 2),
            "height": self.main_frame_attrs.get("height")
        }
        self.right_frame_attrs = {
            "width": (self.main_frame_attrs.get("width") - self.left_frame_attrs.get("width")) - self.padding,
            "height": self.main_frame_attrs.get("height")
        }

    def get_win_size(self) -> str:
        return f"{self.win_width}x{self.win_height}"
    
    def get_attrs(self, var_name: str = None, attr_name: str = None) -> int | None:
        if var_name is None:
            print("Parameter 'var_name' cannot be empty")
            return
        
        if attr_name is None:
            print("Parameter 'attr_name' cannot be empty")
            return
        
        if attr_name != "width" and attr_name != "height":
            print(f"Attribute name '{attr_name}' is not defined")
            return
        
        if var_name == "main":
            return self.main_frame_attrs.get(attr_name)
        elif var_name == "left":
            return self.left_frame_attrs.get(attr_name)
        elif var_name == "right":
            return self.right_frame_attrs.get(attr_name)
        else:
            print(f"Variable nam '{var_name}' is not defined")
            return