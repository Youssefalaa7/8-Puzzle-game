import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox, 
                             QGridLayout, QInputDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import SearchInterface as si  # Assuming this wraps SearchService's methods
from Astar import a_star_algorithm  # Import the A* implementation

class PuzzleSolver(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("8-Puzzle Solver")
        self.setGeometry(100, 100, 600, 500)
        self.initUI()
        self.goal = (0, 1, 2, 3, 4, 5, 6, 7, 8)  # Set the goal state as a tuple

    def initUI(self):
        layout = QVBoxLayout()

        # File selection layout
        file_layout = QHBoxLayout()
        self.file_input = QLineEdit(self)
        file_button = QPushButton("Choose File", self)
        file_button.clicked.connect(self.load_file)
        file_layout.addWidget(self.file_input)
        file_layout.addWidget(file_button)
        layout.addLayout(file_layout)

        # Puzzle grid layout
        self.grid_layout = QGridLayout()
        self.grid_buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                button = QPushButton("", self)
                button.setFixedSize(100, 100)
                button.setFont(QFont("Arial", 20, QFont.Bold))
                self.grid_layout.addWidget(button, i, j)
                row.append(button)
            self.grid_buttons.append(row)
        layout.addLayout(self.grid_layout)

        # Search buttons layout
        button_layout = QHBoxLayout()
        dfs_button = QPushButton("DFS", self)
        bfs_button = QPushButton("BFS", self)
        ids_button = QPushButton("IDS", self)
        a_star_button = QPushButton("A*", self)

        dfs_button.clicked.connect(self.run_dfs)
        bfs_button.clicked.connect(self.run_bfs)
        ids_button.clicked.connect(self.run_ids)
        a_star_button.clicked.connect(self.run_a_star)

        button_layout.addWidget(dfs_button)
        button_layout.addWidget(bfs_button)
        button_layout.addWidget(ids_button)
        button_layout.addWidget(a_star_button)
        layout.addLayout(button_layout)

        # Solution details layout
        self.result_label = QLabel(self)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def load_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Choose Initial State File", "", 
                                                   "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            try:
                with open(file_name, 'r') as file:
                    # Read and validate the initial state from the file
                    self.initial_state = file.read().strip()
                    if len(self.initial_state) != 9 or not self.initial_state.isdigit():
                        raise ValueError("Invalid format. The file should contain 9 digits representing the initial state.")
                    
                    # Convert the initial state to a tuple of integers
                    self.initial_state = tuple(int(digit) for digit in self.initial_state)
                    self.file_input.setText(''.join(map(str, self.initial_state)))
                    self.update_grid(self.initial_state)

            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
                self.initial_state = None

    def update_grid(self, state):
        """Updates the 3x3 grid to display the current puzzle state."""
        for i in range(3):
            for j in range(3):
                value = state[i * 3 + j]
                self.grid_buttons[i][j].setText("" if value == 0 else str(value))

    def run_dfs(self):
        self.run_search(si.dfs)

    def run_bfs(self):
        self.run_search(si.bfs)

    def run_ids(self):
        # Prompt for maximum depth input for IDS
        self.run_search(si.ids)

    def run_a_star(self):
        # Prompt for heuristic type for A*
        heuristic_type, ok = QInputDialog.getInt(
            self, "Select Heuristic Type", 
            "Enter 1 for Manhattan or 2 for Euclidean:", 
            min=1, max=2
        )
        if ok:
            self.run_search(a_star_algorithm, heuristic_type=heuristic_type)

    def run_search(self, search_func, **kwargs):
        if not hasattr(self, 'initial_state') or self.initial_state is None:
            QMessageBox.warning(self, "Warning", "Please load a valid initial state from a file.")
            return

        initial_state = list(self.initial_state)
        goal_state = list(self.goal)

        # Convert the initial state tuple to an integer
        initial_state_int = int(''.join(map(str, initial_state)))
        goal_state_int = int(''.join(map(str, goal_state)))

        try:
            # Call the provided search function
            if search_func==si.ids:
                result = search_func(initial_state_int)
            elif 'heuristic_type' in kwargs:
                result = search_func(initial_state, goal_state, kwargs['heuristic_type'])
            else:
                result = search_func(initial_state_int)

            # Ensure result is not None
            if result is None:
                QMessageBox.warning(self, "Warning", "No solution found.")
                return

            # Unpack result
            success, max_depth, cost, expanded_nodes, path, exec_time = result

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred during search: {e}")
            return

        # Display results
        if not success:
            self.result_label.setText("No solution found.")
        else:
            self.result_label.setText(
                f"Path: {path}\n"
                f"Path Cost: {cost}\n"
                f"Max Depth: {max_depth}\n"
                f"Nodes Expanded: {expanded_nodes}\n"
                f"Execution Time: {exec_time:.4f} seconds"
            )
            # Update grid to show the goal state
            self.update_grid(list(goal_state))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PuzzleSolver()
    window.show()
    sys.exit(app.exec_())
