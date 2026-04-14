import sys
from PyQt6.QtWidgets import QApplication
from src.app import App

def load_styles(style):
    """
        Download styles
        :param style:
        :return:
    """
    try:
        with open("src/UI/style/style.qss", "r", encoding="utf-8") as style_file:
            style_content = style_file.read()
            style.setStyleSheet(style_content)
    except FileNotFoundError:
        print("⚠️ Файл стилів style.qss не знайдено! Використовується стандартна тема.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    load_styles(app)

    aplication = App()
    aplication.run()
    sys.exit(app.exec())