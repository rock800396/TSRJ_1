import tkinter as tk
from tkinter import messagebox
import random

class Minesweeper:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("扫雷")
        self.window.resizable(False, False)
        
        self.size = 16  # 棋盘大小
        self.mines = 40  # 地雷数量
        self.buttons = {}  # 存储按钮
        self.is_game_over = False
        self.flags = set()  # 标记的位置
        self.mines_positions = set()  # 地雷位置
        
        # 创建菜单栏
        self.create_menu()
        
        # 创建游戏面板
        self.create_board()
        
        # 初始化游戏
        self.init_game()

    def create_menu(self):
        menubar = tk.Menu(self.window)
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="新游戏", command=self.reset_game)
        game_menu.add_separator()
        game_menu.add_command(label="退出", command=self.window.quit)
        menubar.add_cascade(label="游戏", menu=game_menu)
        self.window.config(menu=menubar)

    def create_board(self):
        # 创建主框架
        self.frame = tk.Frame(self.window)
        self.frame.pack()

        # 创建按钮网格
        for x in range(self.size):
            for y in range(self.size):
                button = tk.Button(self.frame,
                                 width=2,     # 设置按钮宽度
                                 height=1,    # 设置按钮高度
                                 font=('TkDefaultFont', 9),  # 设置字体大小
                                 padx=1,      # 设置水平内边距
                                 pady=1)      # 设置垂直内边距
                button.grid(row=x, 
                          column=y,
                          padx=0,    # 设置网格水平间距
                          pady=0)    # 设置网格垂直间距
                button.bind('<Button-1>', lambda e, x=x, y=y: self.click(x, y))
                button.bind('<Button-3>', lambda e, x=x, y=y: self.place_flag(x, y))
                self.buttons[(x, y)] = button

    def init_game(self):
        # 随机布置地雷
        self.mines_positions.clear()
        positions = [(x, y) for x in range(self.size) for y in range(self.size)]
        self.mines_positions = set(random.sample(positions, self.mines))

    def get_neighbors(self, x, y):
        neighbors = []
        for i in range(max(0, x-1), min(self.size, x+2)):
            for j in range(max(0, y-1), min(self.size, y+2)):
                if (i, j) != (x, y):
                    neighbors.append((i, j))
        return neighbors

    def count_surrounding_mines(self, x, y):
        count = 0
        for nx, ny in self.get_neighbors(x, y):
            if (nx, ny) in self.mines_positions:
                count += 1
        return count

    def click(self, x, y):
        if self.is_game_over or (x, y) in self.flags:
            return

        button = self.buttons[(x, y)]

        if (x, y) in self.mines_positions:
            # 点到地雷，游戏结束
            button.configure(text="💣", bg="red")
            self.show_all_mines()
            self.is_game_over = True
            messagebox.showinfo("游戏结束", "很遗憾，你踩到地雷了！")
            return

        # 显示数字
        self.show_cell(x, y)
        
        # 检查是否胜利
        self.check_win()

    def show_cell(self, x, y):
        if (x, y) not in self.buttons or \
           self.buttons[(x, y)]['state'] == 'disabled':
            return

        button = self.buttons[(x, y)]
        mines_count = self.count_surrounding_mines(x, y)
        
        if mines_count == 0:
            button.configure(text="", state="disabled", relief="sunken")
            # 递归显示周围的空白格子
            for nx, ny in self.get_neighbors(x, y):
                self.show_cell(nx, ny)
        else:
            button.configure(text=str(mines_count), state="disabled", 
                           relief="sunken", disabledforeground=self.get_number_color(mines_count))

    def get_number_color(self, number):
        colors = {
            1: "blue",
            2: "green",
            3: "red",
            4: "purple",
            5: "maroon",
            6: "turquoise",
            7: "black",
            8: "gray"
        }
        return colors.get(number, "black")

    def place_flag(self, x, y):
        if self.is_game_over:
            return

        if (x, y) in self.flags:
            self.buttons[(x, y)].configure(text="")
            self.flags.remove((x, y))
        else:
            self.buttons[(x, y)].configure(text="🚩")
            self.flags.add((x, y))
        
        self.check_win()

    def show_all_mines(self):
        for (x, y) in self.mines_positions:
            if (x, y) not in self.flags:
                self.buttons[(x, y)].configure(text="💣", bg="red")
        for (x, y) in self.flags:
            if (x, y) not in self.mines_positions:
                self.buttons[(x, y)].configure(text="❌", bg="orange")

    def check_win(self):
        # 检查是否胜利
        remaining_cells = self.size * self.size - len([b for b in self.buttons.values() 
                                                     if b['state'] == 'disabled'])
        if remaining_cells == self.mines and self.flags == self.mines_positions:
            self.is_game_over = True
            messagebox.showinfo("恭喜", "你赢了！")
            self.show_all_mines()

    def reset_game(self):
        # 重置游戏
        self.is_game_over = False
        self.flags.clear()
        self.mines_positions.clear()
        
        # 重置所有按钮
        for button in self.buttons.values():
            button.configure(text="", state="normal", relief="raised", bg="SystemButtonFace")
        
        # 重新初始化游戏
        self.init_game()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = Minesweeper()
    game.run()