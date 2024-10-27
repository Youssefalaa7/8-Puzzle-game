import sys
import ast
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QFileDialog, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtCore import Qt

# Placeholder search algorithms
def dfs(puzzle):
    return "DFS Solution Steps"

def bfs(puzzle):
    return "BFS Solution Steps"

def ids(puzzle):
    return "IDS Solution Steps"

def a_star(puzzle):
    return "A* Solution Steps"

class EightPuzzle(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("8-Puzzle Solver")
        self.setGeometry(100, 100, 600, 600)
        self.initUI()

    def initUI(self):
        self.widget = QWidget(self)
        self.main_layout = QVBoxLayout(self.widget)
        self.grid_layout = QGridLayout()

        # Initial 8-puzzle board configuration
        self.puzzle = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                num = self.puzzle[i][j]
                btn = QPushButton(str(num) if num != 0 else '', self)
                btn.setFixedSize(100, 100)
                self.grid_layout.addWidget(btn, i, j)
                self.buttons[i][j] = btn

        self.main_layout.addLayout(self.grid_layout)

        # Add buttons for loading and solving
        self.load_button = QPushButton("Load Puzzle from File", self)
        self.load_button.clicked.connect(self.load_puzzle)
        self.main_layout.addWidget(self.load_button)

        self.dfs_button = QPushButton("Solve with DFS", self)
        self.dfs_button.clicked.connect(lambda: self.solve_puzzle(dfs))
        self.main_layout.addWidget(self.dfs_button)

        self.bfs_button = QPushButton("Solve with BFS", self)
        self.bfs_button.clicked.connect(lambda: self.solve_puzzle(bfs))
        self.main_layout.addWidget(self.bfs_button)

        self.ids_button = QPushButton("Solve with IDS", self)
        self.ids_button.clicked.connect(lambda: self.solve_puzzle(ids))
        self.main_layout.addWidget(self.ids_button)

        self.a_star_button = QPushButton("Solve with A*", self)
        self.a_star_button.clicked.connect(lambda: self.solve_puzzle(a_star))
        self.main_layout.addWidget(self.a_star_button)

        self.result_label = QLabel("", self)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.result_label)

        self.setCentralWidget(self.widget)

    def load_puzzle(self):
        """Load the initial puzzle configuration from a file."""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Puzzle File", "", "Text Files (*.txt);;All Files (*)", options=options)

        if file_name:
            try:
                with open(file_name, 'r') as file:
                    data = file.read()
                    puzzle = ast.literal_eval(data)  # Read the list from file
                    if self.validate_puzzle(puzzle):
                        self.puzzle = puzzle
                        self.update_buttons()
                    else:
                        QMessageBox.warning(self, "Invalid Puzzle", "The file contains an invalid puzzle format.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to load the puzzle: {e}")

    def validate_puzzle(self, puzzle):
        """Validate the puzzle format."""
        if isinstance(puzzle, list) and len(puzzle) == 3 and all(len(row) == 3 for row in puzzle):
            return True
        return False

    def update_buttons(self):
        for i in range(3):
            for j in range(3):
                num = self.puzzle[i][j]
                self.buttons[i][j].setText(str(num) if num != 0 else '')

    def solve_puzzle(self, algorithm):
        """Solve the puzzle using the selected algorithm."""
        solution_steps = algorithm(self.puzzle)
        self.result_label.setText(f"Solution: {solution_steps}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EightPuzzle()
    window.show()
    sys.exit(app.exec_())
