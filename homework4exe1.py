from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)


class AboutWindow(QDialog):
    def __init__(self):
        super().__init__()
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
            <p><b>GitHub Repository:</b> <a href="https://github.com/noel17026-max/grades-bonus-manager">GitHub Repository</a></p>
            """
        )
        layout.addWidget(browser)


class GradesMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grades Bonus Manager")
        self.setMinimumSize(780, 620)

        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []
        self.selected_file = ""

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        top_bar = QHBoxLayout()
        self.select_file_btn = QPushButton("Select Students File", self)
        self.select_file_btn.clicked.connect(self.open_file_dialog)
        self.file_label = QLabel("No file selected", self)
        self.about_btn = QPushButton("About", self)
        self.about_btn.clicked.connect(self.open_about_window)

        top_bar.addWidget(self.select_file_btn)
        top_bar.addWidget(self.file_label, stretch=1)
        top_bar.addWidget(self.about_btn)
        main_layout.addLayout(top_bar)

        self.table = QTableWidget(50, 3, self)
        self.table.setHorizontalHeaderLabels(["ID", "Original Grades", "Corrected Grades"])
        self.table.setAlternatingRowColors(True)
        for row in range(50):
            for col in range(3):
                self.table.setItem(row, col, QTableWidgetItem(""))
        main_layout.addWidget(self.table)

        bottom_bar = QHBoxLayout()
        bonus_label = QLabel("Bonus Points:", self)
        self.bonus_spinbox = QSpinBox(self)
        self.bonus_spinbox.setRange(-100, 100)
        self.bonus_spinbox.setValue(0)

        self.update_file_btn = QPushButton("Update File", self)
        self.update_file_btn.clicked.connect(self.apply_bonus)

        bottom_bar.addWidget(bonus_label)
        bottom_bar.addWidget(self.bonus_spinbox)
        bottom_bar.addStretch()
        bottom_bar.addWidget(self.update_file_btn)
        main_layout.addLayout(bottom_bar)

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Grades File",
            "",
            "CSV Files (*.csv);;All Files (*)",
        )
        if file_path:
            self.selected_file = file_path
            self.file_label.setText(Path(file_path).name)

            x_values = []
            y_values = []
            with open(self.selected_file, "r") as f:
                next(f)
                for line in f:
                    x, y = line.strip().split(",")
                    x_values.append(int(x))
                    y_values.append(int(y))
            self.student_ids = x_values
            self.original_grades = y_values
            self.corrected_grades = y_values.copy()
            self.populate_table()

    def apply_bonus(self):
        bonus = self.bonus_spinbox.value()
        new_grades = []
        for grade in self.original_grades:
            updated = grade + bonus
            if updated > 100:
                updated = 100
            new_grades.append(updated)
        self.corrected_grades = new_grades
        self.populate_table()
        if self.selected_file:
            with open(self.selected_file, "w") as f:
                f.write("ID,Grade\n")
                for i in range(len(self.student_ids)):
                    f.write(f"{self.student_ids[i]},{self.corrected_grades[i]}\n")

    def populate_table(self):
        for row in range(len(self.student_ids)):
            self.table.setItem(row, 0, QTableWidgetItem(str(self.student_ids[row])))
            self.table.setItem(row, 1, QTableWidgetItem(str(self.original_grades[row])))
            self.table.setItem(row, 2, QTableWidgetItem(str(self.corrected_grades[row])))

    def open_about_window(self):
        about_dialog = AboutWindow()
        about_dialog.exec()


def load_stylesheet(app: QApplication, qss_path: str = "style.qss"):
    path = Path(qss_path)
    if path.exists():
        app.setStyleSheet(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    app = QApplication([])
    app.setLayoutDirection(Qt.LeftToRight)
    load_stylesheet(app, "style.qss")
    window = GradesMainWindow()
    window.show()
    app.exec()