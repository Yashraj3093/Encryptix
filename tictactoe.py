import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.current_player = 'X'
        self.board = ['' for _ in range(9)]
        self.buttons = []

        for i in range(9):
            button = tk.Button(root, text='', font='normal 20 bold', height=3, width=6, 
                               command=lambda i=i: self.on_click(i))
            button.grid(row=i // 3, column=i % 3)
            self.buttons.append(button)

        self.reset_button = tk.Button(root, text='Reset', command=self.reset_board)
        self.reset_button.grid(row=3, column=0, columnspan=3)

    def on_click(self, index):
        if self.board[index] == '' and self.current_player == 'X':
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)
            if self.check_winner():
                return
            self.current_player = 'O'
            self.root.after(500, self.computer_move)

    def computer_move(self):
        best_move = self.find_best_move()
        self.board[best_move] = self.current_player
        self.buttons[best_move].config(text=self.current_player)
        if self.check_winner():
            return
        self.current_player = 'X'

    def find_best_move(self):
        best_val = -float('inf')
        best_move = -1

        for i in range(9):
            if self.board[i] == '':
                self.board[i] = self.current_player
                move_val = self.minimax(0, False)
                self.board[i] = ''
                if move_val > best_val:
                    best_val = move_val
                    best_move = i

        return best_move

    def minimax(self, depth, is_maximizing):
        score = self.evaluate()

        if score == 10:
            return score - depth
        if score == -10:
            return score + depth
        if '' not in self.board:
            return 0

        if is_maximizing:
            best = -float('inf')
            for i in range(9):
                if self.board[i] == '':
                    self.board[i] = 'O'
                    best = max(best, self.minimax(depth + 1, not is_maximizing))
                    self.board[i] = ''
            return best
        else:
            best = float('inf')
            for i in range(9):
                if self.board[i] == '':
                    self.board[i] = 'X'
                    best = min(best, self.minimax(depth + 1, not is_maximizing))
                    self.board[i] = ''
            return best

    def evaluate(self):
        winning_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]

        for condition in winning_conditions:
            a, b, c = condition
            if self.board[a] == self.board[b] == self.board[c]:
                if self.board[a] == 'O':
                    return 10
                elif self.board[a] == 'X':
                    return -10

        return 0

    def check_winner(self):
        score = self.evaluate()
        if score == 10:
            messagebox.showinfo("Tic Tac Toe", "Computer wins!")
            self.reset_board()
            return True
        elif score == -10:
            messagebox.showinfo("Tic Tac Toe", "Player wins!")
            self.reset_board()
            return True
        elif '' not in self.board:
            messagebox.showinfo("Tic Tac Toe", "It's a draw!")
            self.reset_board()
            return True
        return False

    def reset_board(self):
        self.board = ['' for _ in range(9)]
        for button in self.buttons:
            button.config(text='')
        self.current_player = 'X'

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
