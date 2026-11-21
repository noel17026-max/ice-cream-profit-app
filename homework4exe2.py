import sys
from pathlib import Path

import numpy as np
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFileDialog, QDialog, QTextBrowser,
)
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure


class AboutWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About")
        self.setMinimumSize(460, 260)

        layout = QVBoxLayout(self)
        browser = QTextBrowser(self)
        browser.setOpenExternalLinks(True)
        browser.setHtml(
            """
            <h3>נואל חנוכייב</h3>
            <p><b>Email:</b> noel17026@gmail.com</p>
            <p><b>LinkedIn:</b> <a href="https://www.linkedin.com/in/noel-hanukayev-07b19831b/">LinkedIn Profile</a></p>
            <p><b>GitHub Repository:</b> <a href="https://github.com/noel17026-max/ice-cream-profit-app">GitHub Repository</a></p>
            """
        )
        layout.addWidget(browser)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ice Cream Profit")
        self.resize(900, 650)

        self.temperatures = []
        self.revenues = []

        central = QWidget()
        layout = QVBoxLayout(central)

        title = QLabel("Ice Cream Revenue by Temperature")
        title.setObjectName("titleLabel")
        layout.addWidget(title)

        buttons = QHBoxLayout()
        self.select_button = QPushButton("Select File")
        self.select_button.clicked.connect(self.load_file)
        buttons.addWidget(self.select_button)

        self.about_button = QPushButton("About")
        self.about_button.setObjectName("secondaryButton")
        self.about_button.clicked.connect(self.open_about_window)
        buttons.addWidget(self.about_button)
        buttons.addStretch()
        layout.addLayout(buttons)

        self.figure = Figure(figsize=(8, 5))
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        self.setCentralWidget(central)
        self.plot_sample()

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "CSV Files (*.csv)")
        if file_path:
            x_values = []
            y_values = []
            with open(file_path, 'r') as f:
                next(f)
                for line in f:
                    x, y = line.strip().split(',')
                    x_values.append(float(x))
                    y_values.append(float(y))
            self.temperatures = x_values
            self.revenues = y_values
            self.plot_data()

    def plot_data(self):
        data_x = np.array(self.temperatures)
        data_y = np.array(self.revenues)

        coefficients = np.polyfit(data_x, data_y, 1)

        line_function = np.poly1d(coefficients)
        line_x = np.linspace(data_x.min(), data_x.max(), 100)
        line_y = line_function(line_x)

        self.figure.clear()
        ax = self.figure.add_subplot(1, 1, 1)
        ax.scatter(data_x, data_y, label='Data', s=10,
                   color='blue', marker='x')
        ax.plot(line_x, line_y, color='red', label='Trend Line')
        ax.text(data_x.min(), data_y.max(),
                f'y = {coefficients[0]:.2f}x + {coefficients[1]:.2f}',
                color='red')
        ax.set_xlabel('Temperature')
        ax.set_ylabel('Revenue')
        ax.set_title('Ice Cream Revenue vs Temperature')
        ax.legend()
        self.canvas.draw()

    def open_about_window(self):
        about_dialog = AboutWindow(self)
        about_dialog.exec()

    def plot_sample(self):
        time = np.arange(0, 24, 1)
        values = 20 + 5 * np.sin(time / 24 * 2 * np.pi)

        ax = self.figure.add_subplot(111)
        ax.plot(time, values, marker="o", color="#F06C9B")
        ax.set_xlabel("Time [hours]")
        ax.set_ylabel("Value")
        ax.set_title("Sample Time Graph")
        ax.grid(True, alpha=0.3)
        self.canvas.draw()


def main():
    app = QApplication(sys.argv)

    qss_path = Path(__file__).parent / "style2.qss"
    if qss_path.exists():
        app.setStyleSheet(qss_path.read_text(encoding="utf-8"))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
