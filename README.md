# BusinessFlow

Цей проект — desktop-додаток на Python + PyQt6 для ведення фінансового/операційного обліку в стилі ERP/ERM. Основна мета — зберігати транзакції, бюджет, регулярні платежі, звернення (скарги/пропозиції) і мати просту навігацію між розділами.

## 1. Що це за проект

BusinessFlow — це GUI-додаток, який працює як одне вікно з боковою навігацією. Користувач може:

- дивитися дашборд з основною статистикою;
- вести транзакції;
- планувати бюджет;
- розглядати регулярні платежі;
- працювати з feedback/скаргами та пропозиціями;
- переглядати простий розділ inventory (склад/запаси), який поки що мінімальний.

## 2. Як запускати проект

### Встановлення залежностей

```bash
pip install -r requirements.txt
```

### Запуск

```bash
python main.py
```

Вихідна точка програми — [main.py](main.py).

## 3. Загальна архітектура

Проект побудований за схемою:

- UI/інтерфейс — PyQt6
- Контролери — зв’язують інтерфейс і бізнес-логіку
- Сервіси — працюють з даними
- База даних — SQLite

Ключові шари:

- [main.py](main.py) — точка входу
- [src/app.py](src/app.py) — створює головне вікно й підключає сторінки
- [src/core/main_window.py](src/core/main_window.py) — головне вікно з боковою панеллю та контейнером сторінок
- [src/Modules](src/Modules) — модулі програми
- [src/DataBase/db_manager.py](src/DataBase/db_manager.py) — робота з SQLite

## 4. Потік запуску програми

1. Запускається [main.py](main.py).
2. У [main.py](main.py) створюється QApplication.
3. Завантажується стиль з [src/UI/style/style.qss](src/UI/style/style.qss).
4. Створюється об’єкт [src/app.py](src/app.py) — App.
5. App створює головне вікно, ініціалізує модулі, реєструє сторінки й підключає навігацію.
6. Після цього відображається головне вікно.

## 5. Основні модулі

### 5.1 Dashboard

Розташування:
- [src/Modules/Dashboard/DashboardController.py](src/Modules/Dashboard/DashboardController.py)
- [src/Modules/Dashboard/DashboardServise.py](src/Modules/Dashboard/DashboardServise.py)
- [src/Modules/Dashboard/DashboardUi.py](src/Modules/Dashboard/DashboardUi.py)

Що робить:
- показує головну сторінку з основною статистикою;
- показує кількість відкритих завдань/скарг;
- показує залишок бюджету за поточний рік;
- будує кругову діаграму статусів звернень.

Ключові методи:
- load_statistics() — підвантажує дані з бази й оновлює UI
- showEvent() — викликається при показі сторінки, щоб оновити дані

### 5.2 Transactions

Розташування:
- [src/Modules/Transaction/Transactions.py](src/Modules/Transaction/Transactions.py)

Що робить:
- дозволяє додавати транзакції;
- показує список транзакцій у таблиці;
- дозволяє видаляти записи.

Основні функції:
- open_add_dialog() — відкриває діалог додавання транзакції
- load_data() — читає записи з бази й відображає їх у таблиці
- delete_record() — видаляє транзакцію з БД

### 5.3 Feedback

Розташування:
- [src/Modules/Feedback/FeedbackController.py](src/Modules/Feedback/FeedbackController.py)
- [src/Modules/Feedback/FeedbackServise.py](src/Modules/Feedback/FeedbackServise.py)
- [src/Modules/Feedback/feedbackUi.py](src/Modules/Feedback/feedbackUi.py)

Що робить:
- працює зі зверненнями типу “скарга/пропозиція”;
- дозволяє створювати нові записи;
- дозволяє змінювати статус;
- дозволяє редагувати записи;
- підтримує прикріплення файлів до запису.

Особливості:
- є контекстне меню правою кнопкою миші;
- є логіка збереження файлів у папку data/feedback_files.

### 5.4 Budget

Розташування:
- [src/Modules/budget/budgetController.py](src/Modules/budget/budgetController.py)
- [src/Modules/budget/budgetService.py](src/Modules/budget/budgetService.py)
- [src/Modules/budget/budgetUi.py](src/Modules/budget/budgetUi.py)

Що робить:
- показує бюджет по категоріях за рік;
- дозволяє редагувати планові суми;
- показує фактичні витрати;
- будує кругову діаграму;
- дозволяє додавати фактичні платежі з можливістю прикріпити чек/фактуру;
- дозволяє переглядати історію витрат для категорії.

Ключові сценарії:
- load_data() — завантажує бюджет за вибраний рік
- clone_budget_for_year() — копіює бюджет з попереднього року в новий
- open_add_transaction() — додає новий платіж
- open_history() — відкриває історію витрат

### 5.5 Regular Payments

Розташування:
- [src/Modules/RegularPayments/RegularPaymentsUi.py](src/Modules/RegularPayments/RegularPaymentsUi.py)
- [src/Modules/RegularPayments/controller.py](src/Modules/RegularPayments/controller.py)
- [src/Modules/RegularPayments/service.py](src/Modules/RegularPayments/service.py)

Що робить:
- дозволяє додавати регулярні платежі;
- зберігає назву, суму, категорію та день списання;
- виводить їх у таблицю.

### 5.6 Inventory

Розташування:
- [src/Modules/Inventory/InventoryUi.py](src/Modules/Inventory/InventoryUi.py)

Що робить:
- поки що є заглушкою/порожнім контейнером для майбутнього функціоналу складу.

## 6. Бокова навігація

Головне вікно створює бокову панель через [src/Modules/Sidebar/Sidebar.py](src/Modules/Sidebar/Sidebar.py).

На панелі є кнопки:
- Dashboard
- Транзакції
- Скарги/пропозиції
- Склад
- Регулярні платежі
- Бюджет
- Планування робіт

Перемикання між сторінками відбувається в [src/app.py](src/app.py).

## 7. База даних

Проект використовує SQLite. Основний менеджер БД — [src/DataBase/db_manager.py](src/DataBase/db_manager.py).

### Основні таблиці

- transactions
  - зберігає транзакції
  - поля: id, date, type, category, sum, status, json_datails, receipt_path

- feedback
  - зберігає звернення
  - поля: id, date, name, type, description, status, resolution_note, priority

- regular_payments
  - зберігає регулярні списання
  - поля: id, name, amount, category, day_of_month

- categories
  - категорії бюджетів

- budgets
  - план бюджету за роками

- users
  - заготовка для користувачів

Файл бази даних зберігається в папці data.

## 8. Де зберігаються файли

- [data/receipts](data/receipts) — скани/фактури для транзакцій
- [data/feedback_files](data/feedback_files) — прикріплені файли до feedback-записів
- [src/UI/style/style.qss](src/UI/style/style.qss) — стилі UI

## 9. Що варто знати перед продовженням роботи

- Проект вже має робочий каркас UI і базу даних.
- Більшість логіки розділена на три рівні: UI → Controller → Service/DB.
- Якщо хочеш змінити функціонал, найчастіше треба працювати в одному з таких місць:
  - UI: відповідний файл у папці Modules/*/*.ui або *.Ui.py
  - Логіка: Controller/Service
  - Збереження даних: db_manager.py
- У коді є кілька назв/спотворень (наприклад, DashboardServise, FeedbackServise), але це не впливає на базову роботу, якщо не змінювати їх назви без потреби.
- Існує частина коду, яка ще не повністю дороблена, наприклад розділ Inventory.

## 10. Якщо хочеш швидко орієнтуватися в коді

Рекомендований порядок перегляду:

1. [main.py](main.py)
2. [src/app.py](src/app.py)
3. [src/core/main_window.py](src/core/main_window.py)
4. [src/Modules/Sidebar/Sidebar.py](src/Modules/Sidebar/Sidebar.py)
5. [src/DataBase/db_manager.py](src/DataBase/db_manager.py)
6. Потім конкретний модуль, який потрібно змінювати: Dashboard, Transactions, Feedback або Budget

## 11. Коротко: що робить кожен важливий файл

- [main.py](main.py) — запуск додатку
- [src/app.py](src/app.py) — ініціалізація модулів і навігація
- [src/core/main_window.py](src/core/main_window.py) — базове головне вікно
- [src/Modules/Sidebar/Sidebar.py](src/Modules/Sidebar/Sidebar.py) — бічна панель
- [src/DataBase/db_manager.py](src/DataBase/db_manager.py) — доступ до бази даних SQLite
- [src/Modules/Transaction/Transactions.py](src/Modules/Transaction/Transactions.py) — транзакції
- [src/Modules/Feedback/FeedbackController.py](src/Modules/Feedback/FeedbackController.py) — логіка feedback
- [src/Modules/budget/budgetController.py](src/Modules/budget/budgetController.py) — логіка бюджету
- [src/Modules/Dashboard/DashboardController.py](src/Modules/Dashboard/DashboardController.py) — дашборд

## 12. Карта розвитку проекту

Нижче — практичний план розвитку, який можна виконувати поетапно.

### Етап 1. Стабілізація і чистота коду
- виправити помилки в назвах класів/файлів, якщо вони впливають на підтримку проекту;
- привести до єдиного стилю назви методів і файлів;
- прибрати дублювання логіки між контролерами і сервісами;
- додати базову обробку помилок для всіх діалогів і CRUD-операцій.

Чому це важливо:
- код стане простішим для розуміння після довгої перерви;
- зменшиться кількість багів при зміні функціоналу.

### Етап 2. Покращення UX/UI
- зробити єдину тему для всіх сторінок;
- покращити відступи, кольори, стилі таблиць і кнопок;
- додати підказки, валідацію полів і повідомлення про успішне збереження;
- зробити більш зрозумілий layout для Dashboard і Budget.

Чому це важливо:
- програма буде виглядати як повноцінний продукт, а не як прототип.

### Етап 3. Розширення функціоналу бюджету
- додати редагування і видалення транзакцій прямо з історії;
- додати фільтри по датах і категоріях;
- показувати звіт за місяць/квартал/рік;
- додати автоматичні підсумки і аналітику.

Чому це важливо:
- це один із найцінніших модулів для користувача.

### Етап 4. Розвиток модулів Transactions і Regular Payments
- додати редагування транзакцій, а не тільки видалення;
- додати фільтрацію за типом, датою, категорією;
- зробити синхронізацію регулярних платежів з транзакціями;
- додати можливість відмічати платежі як виконані/заплановані.

Чому це важливо:
- це підвищить практичність застосунку в повсякденному використанні.

### Етап 5. Feedback як реальна система роботи
- додати пошук і сортування звернень;
- додати фільтр по статусу/пріоритету;
- зберігати історію змін статусів;
- зробити окремий екран для “активних” і “вирішених” звернень.

Чому це важливо:
- модуль уже є, але може стати набагато більш корисним.

### Етап 6. Inventory
- реалізувати базову систему складу;
- додати товари, кількість, ціну, категорію;
- додати рух товарів (прибуток/витрата);
- показувати залишки на складі.

Чому це важливо:
- це наступний логічний блок після бюджету і транзакцій.

### Етап 7. Технічне вдосконалення
- перейти на більш чітку структуру: view/controller/service/repository;
- розділити UI та логіку ще сильніше;
- додати unit tests;
- підготувати збірку .exe.

Чому це важливо:
- це дозволить проекту рости без хаосу.

## 13. Порада для повернення до роботи

Якщо давно не працював із цим проєктом, почни з таких кроків:

1. запусти програму;
2. подивись, як працює навігація;
3. відкрий модуль, над яким хочеш працювати;
4. спочатку зрозумій UI, потім controller, і лише після цього — базу даних.

Це дасть швидше розуміння, де саме потрібно вносити зміни.
