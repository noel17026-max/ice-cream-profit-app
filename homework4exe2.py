# דוגמת קוד שנוצרה בעזרת AI (מותר לפי ההנחיות):
# גרף זמני בסיסי של matplotlib בתוך חלון PySide6, עם טעינת style2.qss.
# את ההתאמה לקובץ Ice Cream.csv ואת שאר הדרישות יש להשלים לבד (ראו TODO).

import sys
from pathlib import Path

import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sample Time Graph")
        self.resize(900, 600)

        central = QWidget()
        layout = QVBoxLayout(central)

        title = QLabel("Sample Time Graph")
        title.setObjectName("titleLabel")
        layout.addWidget(title)

        # Sample time-series graph
        self.figure = Figure(figsize=(8, 5))
        self.canvas = FigureCanvasQTAgg(self.figure)
        layout.addWidget(self.canvas)

        self.setCentralWidget(central)
        self.plot_sample()

        # TODO (לבד): כפתור שפותח חלון לבחירת קובץ
        # TODO (לבד): יכולת זום ושמירת הגרף כקובץ
        # TODO (לבד): כפתור About עם כתובת ה-GitHub של מאגר הקוד

    def plot_sample(self):
        time = np.arange(0, 24, 1)  # hours
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
