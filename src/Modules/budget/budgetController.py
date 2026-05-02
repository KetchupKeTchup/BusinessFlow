"""Керування логікою і інтерфейсом"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QDialog,QMenu, QMessageBox, QAbstractItemView, QTableWidgetItem
from PyQt6.QtGui import QCursor, QPainter
from PyQt6.QtCharts import QChart, QChartView, QPieSeries, QPieSlice
from src.Modules.budget.budgetService import BudgetService
from src.Modules.budget.budgetUi import BudgetWindow, EditBudgetDialog, AddTransactionDialog, TransactionHistoryDialog


class BudgetController(QWidget):
    def __init__(self):
        super().__init__()


        # Створюємо інтерфейс та сервіс даних
        self.ui = BudgetWindow()
        self.service = BudgetService()

        # Розміщуємо інтерфейс на екрані контролера
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # Прибираємо зайві відступи
        layout.addWidget(self.ui)
        # Зміна року
        self.ui.year_selector.currentTextChanged.connect(lambda :self.load_data())
        # Даємо команду завантажити дані
        self.load_data()
        # Прослуховування нажаття кнопки
        self.ui.table.customContextMenuRequested.connect(self.show_context_menu)
        self.ui.btn_add_payment.clicked.connect(self.open_add_transaction)
        self.ui.radio_plan.toggled.connect(lambda checked: self.update_chart())
        self.ui.radio_fact.toggled.connect(lambda checked: self.update_chart())
        self.ui.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.ui.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        # Відкриття історії при подвійному кліку на рядок таблиці
        self.ui.table.cellDoubleClicked.connect(self.open_history)

        # Підключаємо сигнал: коли користувач клікає на рядок
        self.ui.table.itemSelectionChanged.connect(self.on_table_selection_changed)


    def load_data(self):
        # Беремо рік який вибраний у випадаючому списку
        try:

            selected_year = int(self.ui.year_selector.currentText())

            # Звертаємося до сервісу (він дістає дані з бази)
            data = self.service.get_budget_stats(selected_year)

            # Передаємо дані в UI для малювання таблиці
            if data:
                self.ui.fill_table(data)
                self.current_data = data
                self.ui.fill_table(data)
                self.update_chart()

                # Рахуємо підсумок: сумуємо всі заплановані гроші
                total_planned = sum(row[1] for row in data)
                self.ui.lbl_total.setText(f" Presupuesto total para el año: {selected_year} - {total_planned:,.2f} €")
            else:
                self.ui.table.setRowCount(0)
                self.ui.lbl_total.setText("No hay datos para este año.")

                reply = QMessageBox.question(
                    self, "Año vacío",
                    f"На {selected_year} рік ще немає бюджету. Бажаєте скопіювати категорії та суми з {selected_year - 1} року?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.Yes
                )
                if reply == QMessageBox.StandardButton.Yes:
                    self.clone_budget_for_year(selected_year - 1, selected_year)
        except Exception as e:
            print(f"{e}Помилка призавантажені року")

    def clone_budget_for_year(self, old_year, new_year):
        # 1. Беремо дані за старий рік
        old_data = self.service.get_budget_stats(old_year)
        if not old_data:
            QMessageBox.warning(self, "Помилка", f"Немає даних за {old_year} рік для копіювання!")
            return

            # 2. Перебираємо старі дані і записуємо їх у новий рік
        for row in old_data:
            category_name = row[0]
            amount = row[1]
            self.service.db.set_budget(category_name, new_year, amount)

        # 3. Перезавантажуємо таблицю (вона вже буде заповнена!)
        self.load_data()

    def show_context_menu(self, position):

        row = self.ui.table.rowAt(position.y())

        # Якщо натиснули на пустий рядок нічого не робимо
        if row < 0:
            return

        # Створення меню
        menu = QMenu()
        edit_action = menu.addAction("✏️ Plan de edición")

        #delete_action = menu.addAction("🗑 Eliminar")

        # Показуємо меню прямо під курсором миші
        action = menu.exec(QCursor.pos())

        # Якщо натиснули редагування
        if action == edit_action:
            self.edit_record(row)

    def edit_record(self, row):
        # назва категорії в колонкі 0
        category_name = self.ui.table.item(row, 0).text()
        # дістаємо поточну суму в колонкі 1
        current_amount_str = self.ui.table.item(row, 1).text()


        dialog = EditBudgetDialog(category_name, current_amount_str, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # якщо натиснуто зберегти
            new_amount = dialog.amount_input.value()
            current_year = int(self.ui.year_selector.currentText())


            self.service.update_budget(category_name,current_year, new_amount)
            self.ui.table.setRowCount(0)
            self.load_data()

    def update_chart(self):
        """Оновлює кругову діаграму залежно від вибраного перемикача"""
        try:
            if not hasattr(self, 'current_data') or not self.current_data:
                return

            self.ui.chart.removeAllSeries()
            series = QPieSeries()

            is_plan = self.ui.radio_plan.isChecked()
            data_index = 1 if is_plan else 2

            valid_data = []
            for row in self.current_data:
                val = row[data_index]
                if val is not None and float(val) > 0:
                    valid_data.append((row[0], float(val)))

            total = sum(item[1] for item in valid_data)
            if total == 0:
                return

            for name, amount in valid_data:
                percentage = (amount / total) * 100
                label = f"{name} ({percentage:.1f}%)"

                slice_obj = series.append(label, amount)
                slice_obj.setLabelVisible(True)
                slice_obj.setLabelPosition(QPieSlice.LabelPosition.LabelOutside)

                # ВИПРАВЛЕНИЙ РЯДОК: використовуємо змінну name
                slice_obj.hovered.connect(
                    lambda is_hovered, s=slice_obj, cat_name=name:
                    self.on_slice_hovered(s, cat_name, is_hovered)
                )

            self.ui.chart.addSeries(series)

        except Exception as e:
            print(f"❌ ПОМИЛКА ГРАФІКА: {e}")
        except Exception as e:
            print(f"❌ КРИТИЧНА ПОМИЛКА ГРАФІКА: {e}")
            import traceback
            traceback.print_exc()  # Це покаже точний рядок, де сталася помилка


    def open_add_transaction(self):
        # 1. Збираємо список категорій з таблиці
        row_count = self.ui.table.rowCount()
        categories = [self.ui.table.item(i, 0).text() for i in range(row_count)]

        if not categories:
            QMessageBox.warning(self, "Увага", "Спочатку створіть бюджет на цей рік!")
            return

        # 2. Відкриваємо вікно
        dialog = AddTransactionDialog(categories, self)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            # 3. Забираємо дані
            category = dialog.category_cb.currentText()
            amount = dialog.amount_input.value()
            date_str = dialog.date_input.date().toString("yyyy-MM-dd")  # Формат для БД
            invoice = dialog.file_path_input.text()

            # 4. Зберігаємо
            self.service.add_payment(category, amount, date_str, invoice)

            # 5. Оновлюємо таблицю та графік!
            self.load_data()

    def on_slice_hovered(self, slice_obj, category_name, is_hovered):
        """Спрацьовує при наведенні на графік: підсвічує рядок у таблиці"""
        slice_obj.setExploded(is_hovered)

        # Тимчасово блокуємо сигнали таблиці, щоб не було нескінченного циклу
        self.ui.table.blockSignals(True)

        if is_hovered:
            # Шукаємо рядок за назвою категорії і виділяємо його
            for row in range(self.ui.table.rowCount()):
                if self.ui.table.item(row, 0).text() == category_name:
                    self.ui.table.selectRow(row)
                    break
        else:
            self.ui.table.clearSelection()  # Знімаємо виділення, коли мишка йде

        self.ui.table.blockSignals(False)

    def on_table_selection_changed(self):
        """Спрацьовує при кліку на таблицю: висуває шматочок графіка"""
        # Спочатку "ховаємо" всі шматочки графіка назад
        if self.ui.chart.series():
            series = self.ui.chart.series()[0]
            for slice_obj in series.slices():
                slice_obj.setExploded(False)

        selected_items = self.ui.table.selectedItems()
        if not selected_items:
            return

        # Беремо назву категорії з вибраного рядка (з колонки 0)
        row = selected_items[0].row()
        category_name = self.ui.table.item(row, 0).text()

        # Знаходимо потрібний шматочок графіка і "висуваємо" його
        if self.ui.chart.series():
            series = self.ui.chart.series()[0]
            for slice_obj in series.slices():
                # Перевіряємо чи назва шматка починається з назви категорії
                # (бо на графіку ще є відсотки, напр. "Agua (15%)")
                if slice_obj.label().startswith(category_name):
                    slice_obj.setExploded(True)
                    break

    def open_history(self, row, column):
        """Відкриває вікно з історією платежів для вибраної категорії"""
        # Беремо назву категорії з вибраного рядка
        category_name = self.ui.table.item(row, 0).text()
        year = int(self.ui.year_selector.currentText())

        # Беремо транзакції з бази
        transactions = self.service.get_category_transactions(category_name, year)

        if not transactions:
            QMessageBox.information(self, "Інфо", "Для цієї категорії ще немає витрат у цьому році.")
            return

        # Відкриваємо вікно
        dialog = TransactionHistoryDialog(category_name, self)

        # Заповнюємо таблицю у вікні
        # Заповнюємо таблицю у вікні
        dialog.table.setRowCount(len(transactions))
        for i, t in enumerate(transactions):
            t_id, date_str, amount, receipt_path = t  # Тепер розпаковуємо 4 змінні!

            short_date = date_str.split(" ")[0] if " " in date_str else date_str

            dialog.table.setItem(i, 0, QTableWidgetItem(str(t_id)))
            dialog.table.setItem(i, 1, QTableWidgetItem(short_date))
            dialog.table.setItem(i, 2, QTableWidgetItem(f"{amount:.2f}"))

            from PyQt6.QtWidgets import QPushButton

            # --- НОВА КНОПКА: ВІДКРИТИ ЧЕК ---
            btn_open = QPushButton("👁 Відкрити")
            if not receipt_path:  # Якщо при додаванні файл не вибрали
                btn_open.setEnabled(False)
                btn_open.setText("Немає файлу")
            else:
                # Використовуємо лямбду, щоб передати шлях
                btn_open.clicked.connect(lambda checked, path=receipt_path: self.open_receipt(path))
            dialog.table.setCellWidget(i, 3, btn_open)  # Ставимо в 4-ту колонку (індекс 3)

            # --- СТАРА КНОПКА: ВИДАЛИТИ ---
            btn_delete = QPushButton("🗑 Видалити")
            btn_delete.setStyleSheet("color: #ff4c4c; font-weight: bold;")
            btn_delete.clicked.connect(lambda checked, t_id=t_id: self.delete_and_refresh(t_id, dialog))
            dialog.table.setCellWidget(i, 4, btn_delete)  # Перемістили в 5-ту колонку (індекс 4)

        dialog.exec()

    def delete_and_refresh(self, t_id, dialog):
        """Видаляє платіж і оновлює головний інтерфейс"""
        reply = QMessageBox.question(self, "Підтвердження", "Ви дійсно хочете видалити цей платіж?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.service.delete_transaction(t_id)  # Видаляємо з БД
            dialog.accept()  # Закриваємо вікно історії
            self.load_data()  # Оновлюємо головну таблицю і графік

    def open_receipt(self, file_path):
        """Відкриває файл фактури у стандартній програмі ОС"""
        import os
        from PyQt6.QtGui import QDesktopServices
        from PyQt6.QtCore import QUrl

        # Перетворюємо відносний шлях в абсолютний (повний шлях на комп'ютері)
        abs_path = os.path.abspath(file_path)

        # Перевіряємо, чи файл досі фізично існує в папці
        if os.path.exists(abs_path):
            # Магія PyQt: відкриває будь-що як системне посилання
            QDesktopServices.openUrl(QUrl.fromLocalFile(abs_path))
        else:
            QMessageBox.warning(self, "Помилка", f"Файл не знайдено за шляхом:\n{abs_path}")