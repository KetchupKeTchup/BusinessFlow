from PyQt6.QtWidgets import QMessageBox, QTableWidgetItem, QDialog, QMenu, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from src.Modules.Feedback.FeedbackServise import FeedbackServise
from src.Modules.Feedback.feedbackUi import FeedbackWindow, AddFeedbackDialog, EditFeedbackDialog
class FeedbackController(QWidget):

    def __init__(self):
        super().__init__()  # Обов'язкова ініціалізація віджета
        print("1. Старт ініціалізації Контролера Відгуків")

        self.ui = FeedbackWindow()
        self.service = FeedbackServise()

        # Розміщуємо інтерфейс на екрані контролера (ЯК У БЮДЖЕТІ)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ui)

        # Підключаємо сигнали
        self.ui.btn_add.clicked.connect(self.open_add_feedback)
        print("2. Кнопка 'Додати' підключена")

        self.ui.table.customContextMenuRequested.connect(self.show_context_menu)

        # Завантажуємо дані
        print("3. Виклик load_data()...")
        self.load_data()
        print("4. Ініціалізація завершена успішно!")

    def load_data(self):
        """Очищає таблицю і заповнює її даними з бази"""
        print("--- СТАРТ load_data ---")
        try:
            self.ui.table.setRowCount(0)
            feedbacks = self.service.get_all_feedbacks()
            print(f"Отримано даних з БД: {len(feedbacks)} записів")

            if not feedbacks:
                print("БД порожня (або повернула пустий список).")
                return

            for row_idx, row_data in enumerate(feedbacks):
                print(f"Обробка рядка {row_idx}: {row_data}")
                self.ui.table.insertRow(row_idx)
                id_feedback = row_data[0]
                date = row_data[1]

                col_date = QTableWidgetItem(date)
                col_date.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                col_date.setData(Qt.ItemDataRole.UserRole, id_feedback)
                self.ui.table.setItem(row_idx, 0, col_date)

                # ТУТ МОЖЕ БУТИ ПОМИЛКА, якщо структура таблиці в БД відрізняється від очікуваної
                mapping = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 7)]
                for ui_col, db_col in mapping:
                    try:
                        item_text = str(row_data[db_col]) if row_data[db_col] else ""
                        cell_widget = QTableWidgetItem(item_text)
                        cell_widget.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.ui.table.setItem(row_idx, ui_col, cell_widget)
                    except IndexError:
                        print(f"❌ ПОМИЛКА: Немає колонки {db_col} в даних з БД! Довжина рядка: {len(row_data)}")

            print("--- КІНЕЦЬ load_data ---")
        except Exception as e:
            print(f"❌ КРИТИЧНА ПОМИЛКА в load_data: {e}")

    def open_add_feedback(self):
        try:
            dialog = AddFeedbackDialog(self.ui)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                t_type = dialog.option.currentText()
                author_name = dialog.author_name.text().strip() or "Анонім"
                t_priority = dialog.priority.currentText()
                text_feedback = dialog.text_feedback.toPlainText()

                if not text_feedback.strip():
                    QMessageBox.warning(self.ui, "Увага", "Поле з описом не може бути порожнім!")
                    return

                self.service.add_feedback(author_name, t_type, text_feedback, t_priority)
                self.load_data()
            else:
                print("Додавання скасовано.")
        except Exception as e:
            print(f"❌ КРИТИЧНА ПОМИЛКА в open_add_feedback: {e}")

    def show_context_menu(self, position):
        """Відображає меню при кліку правою кнопкою миші по таблиці"""
        # Отримуємо рядок, по якому клікнули
        row = self.ui.table.rowAt(position.y())
        if row < 0:
            return  # Якщо клікнули на порожнє місце — нічого не робимо

        # Створюємо меню
        menu = QMenu(self.ui)

        # 1. Кнопка Редагування
        action_edit = menu.addAction("✏️ Редагувати")

        menu.addSeparator()  # Розділювач

        # 2. Підменю для статусів
        status_menu = menu.addMenu("🔄 Змінити статус")
        action_new = status_menu.addAction("Нове")
        action_progress = status_menu.addAction("В процесі")
        action_resolved = status_menu.addAction("Вирішено")

        menu.addSeparator()  # Розділювач

        # 3. Кнопка Видалення
        action_delete = menu.addAction("🗑 Видалити")

        # Показуємо меню під курсором і чекаємо вибору
        action = menu.exec(self.ui.table.viewport().mapToGlobal(position))

        # Якщо користувач клікнув повз меню
        if not action:
            return

        # Отримуємо прихований ID запису (з 0-ї колонки, як ти робив у load_data)
        record_id = self.ui.table.item(row, 0).data(Qt.ItemDataRole.UserRole)

        # Обробляємо вибір користувача
        if action == action_edit:
            self.edit_record(record_id)
        elif action == action_new:
            self.change_status(record_id, "Нове")
        elif action == action_progress:
            self.change_status(record_id, "В процесі")
        elif action == action_resolved:
            self.change_status(record_id, "Вирішено")
        elif action == action_delete:
            self.delete_record(record_id)

    def change_status(self, record_id, new_status):
        self.service.update_status(record_id, new_status)
        self.load_data()

    def delete_record(self, record_id):
        reply = QMessageBox.question(self.ui, 'Підтвердження', 'Ви дійсно хочете видалити цей запис?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.service.delete_record(record_id)
            self.load_data()

    def edit_record(self, record_id):
        # 1. Беремо всі поточні дані з БД
        current_data = self.service.get_feedback_by_id(record_id)
        if not current_data:
            return

        # 2. Відкриваємо вікно і передаємо туди старі дані
        dialog = EditFeedbackDialog(current_data, self.ui)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # 3. Якщо натиснуто Зберегти - збираємо нові дані з полів
            t_type = dialog.option.currentText()
            author_name = dialog.author_name.text().strip() or "Анонім"
            t_priority = dialog.priority.currentText()
            status = dialog.status_cb.currentText()
            text_feedback = dialog.text_feedback.toPlainText()
            file_path = dialog.file_path_input.text()

            if not text_feedback.strip():
                QMessageBox.warning(self.ui, "Увага", "Поле з описом не може бути порожнім!")
                return

            # 4. Передаємо в сервіс для збереження (і копіювання файлу)
            self.service.update_feedback_full(record_id, author_name, t_type, text_feedback, t_priority, status, file_path)

            # 5. Оновлюємо таблицю на екрані
            self.load_data()