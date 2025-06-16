import sys
import csv
import psycopg2
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QDialog, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
                             QMessageBox, QTabWidget, QTableWidget, QTableWidgetItem,
                             QComboBox, QHeaderView, QScrollArea, QFileDialog, QDateEdit, QCheckBox)
from PyQt5.QtCore import Qt, QDate, QTime, QSizeF
from PyQt5.QtGui import QPalette, QColor
import os
from datetime import datetime


# Стили приложения
APP_STYLE = """
QMainWindow, QDialog, QWidget {
    background-color: #F3E9DC;
    color: #5E3023;
    font-family: Arial;
    font-size: 14px;
}

QPushButton {
    background-color: #895737;
    color: #FFFFFF;
    border: 1px solid #5E3023;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
    min-width: 80px;
}

QPushButton:hover {
    background-color: #C08552;
}

QPushButton:pressed {
    background-color: #5E3023;
}

QLineEdit, QComboBox, QDateEdit {
    background-color: #FFFFFF;
    border: 1px solid #C08552;
    padding: 6px;
    border-radius: 4px;
    min-height: 25px;
}

QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
    border: 2px solid #895737;
}

QTabWidget::pane {
    border: 1px solid #C08552;
    background: #F3E9DC;
    margin-top: -1px;
}

QTabBar::tab {
    background: #E8D5C4;
    color: #5E3023;
    padding: 12px 25px;          /* Увеличили отступы */
    border: 1px solid #C08552;
    border-bottom: none;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}

QTabBar::tab:selected {
    background: #F3E9DC;
    color: #5E3023;
    font-weight: bold;
}

QTableWidget {
    background-color: #FFFFFF;
    border: 1px solid #C08552;
    gridline-color: #E8D5C4;
    selection-background-color: #895737;
    selection-color: white;
}

QHeaderView::section {
    background-color: #895737;
    color: white;
    padding: 6px;
    border: none;
    font-weight: bold;
}
"""


class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="School",
            user="postgres",
            password="katel",
            host="localhost"
        )
        self.cursor = self.conn.cursor()

    def execute(self, query, params=None, fetch=True):
        try:
            self.cursor.execute(query, params or ())
            if not fetch:
                self.conn.commit()
            return self.cursor.fetchall() if fetch else None
        except Exception as e:
            self.conn.rollback()
            raise e


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(APP_STYLE)
        self.setWindowTitle("Авторизация")
        self.setFixedSize(400, 250)
        self.db = Database()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 20, 30, 20)
        main_layout.setSpacing(15)

        title = QLabel("Вход в систему школы")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #5E3023;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)

        lbl_login = QLabel("Логин:")
        lbl_login.setStyleSheet("font-weight: bold;")
        form_layout.addWidget(lbl_login)

        self.edit_login = QLineEdit()
        self.edit_login.setPlaceholderText("Введите ваш логин")
        form_layout.addWidget(self.edit_login)

        lbl_pass = QLabel("Пароль:")
        lbl_pass.setStyleSheet("font-weight: bold;")
        form_layout.addWidget(lbl_pass)

        self.edit_pass = QLineEdit()
        self.edit_pass.setPlaceholderText("Введите ваш пароль")
        self.edit_pass.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(self.edit_pass)

        main_layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.btn_login = QPushButton("Войти")
        self.btn_exit = QPushButton("Выход")

        btn_layout.addWidget(self.btn_login)
        btn_layout.addWidget(self.btn_exit)
        main_layout.addLayout(btn_layout)

        self.btn_login.clicked.connect(self.auth)
        self.btn_exit.clicked.connect(self.close)

    def auth(self):
        login = self.edit_login.text()
        password = self.edit_pass.text()

        # Словарь пользователей: логин -> (пароль, роль, полное_имя)
        users = {
            "admin": ("admin", "admin", "Администратор системы"),
            "zavuch": ("zavuch", "zavuch", "Завуч школы"),
            #    "director": ("director", "zavuch", "Директор школы")
        }

        if login in users and users[login][0] == password:
            user_role = users[login][1]
            user_name = users[login][2]
            self.app = MainApp(self.db, user_role, user_name)
            self.app.show()
            self.close()
        else:
            QMessageBox.critical(self, "Ошибка", "Неверные учетные данные")



class MainApp(QMainWindow):
    def __init__(self, db, user_role='admin', user_name='Пользователь'):
        super().__init__()
        self.setStyleSheet(APP_STYLE)
        self.db = db
        self.user_role = user_role  # ДОБАВИТЬ
        self.user_name = user_name  # ДОБАВИТЬ

        self.setWindowTitle(f"Система управления школой - {user_name} ({self.get_role_name()})")
        self.setGeometry(100, 100, 1200, 800)

        # Создаем вкладки
        self.tabs = QTabWidget()

        # Инициализируем вкладки в зависимости от роли
        self.init_tabs_by_role()

        # Кнопки управления
        self.init_toolbar()

        main_layout = QVBoxLayout()
        main_layout.addLayout(self.toolbar_layout)
        main_layout.addWidget(self.tabs)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def get_role_name(self):
        """Возвращает русское название роли"""
        role_names = {
            'admin': 'Администратор',
            'zavuch': 'Завуч'
        }
        return role_names.get(self.user_role, 'Пользователь')

    def init_tabs_by_role(self):
        """Инициализация вкладок в зависимости от роли пользователя"""
        if self.user_role == 'admin':
            # Администратор видит все вкладки с полным функционалом
            self.init_students_tab()
            self.init_teachers_tab()
            self.init_classes_tab()
            self.init_subjects_tab()
            self.init_lessons_tab()
            self.init_grades_tab()
            self.init_progress_tab()
            self.init_reports_tab()
        elif self.user_role == 'zavuch':
            # Завуч видит только таблицы для просмотра и отчеты
            self.init_students_tab_readonly()
            self.init_teachers_tab_readonly()
            self.init_classes_tab_readonly()
            self.init_subjects_tab_readonly()
            self.init_lessons_tab_readonly()
            self.init_grades_tab_readonly()
            self.init_progress_tab_readonly()
            self.init_reports_tab()

    def init_toolbar(self):
        """Инициализация панели инструментов с учетом ролей"""
        self.toolbar_layout = QHBoxLayout()

        # Информация о пользователе
        user_info = QLabel(f"👤 {self.user_name} ({self.get_role_name()})")
        user_info.setStyleSheet("font-weight: bold; color: #5E3023; padding: 5px;")

        self.toolbar_layout.addWidget(user_info)
        self.toolbar_layout.addStretch()

        # Кнопки экспорта (доступны всем)
        self.btn_export_pdf = QPushButton("Экспорт PDF")
        self.btn_export_csv = QPushButton("Экспорт CSV")
        self.btn_logout = QPushButton("Выход")

        self.toolbar_layout.addWidget(self.btn_export_pdf)
        self.toolbar_layout.addWidget(self.btn_export_csv)
        self.toolbar_layout.addWidget(self.btn_logout)

        self.btn_export_csv.clicked.connect(self.export_current_tab_to_csv)
        self.btn_export_pdf.clicked.connect(self.export_current_tab_to_pdf)
        self.btn_logout.clicked.connect(self.logout)

    def init_students_tab_readonly(self):
        """Вкладка учеников только для чтения"""
        tab = QWidget()
        layout = QVBoxLayout()

        # Поиск
        search_layout = QHBoxLayout()
        self.student_search = QLineEdit()
        self.student_search.setPlaceholderText("Поиск учеников...")
        self.student_search.textChanged.connect(self.load_students)
        search_layout.addWidget(QLabel("Поиск:"))
        search_layout.addWidget(self.student_search)

        # Информационная панель для завуча
        info_label = QLabel("👁️ Режим просмотра (завуч)")
        info_label.setStyleSheet("background-color: #E8D5C4; padding: 8px; border-radius: 4px; font-weight: bold;")

        # Таблица
        self.students_table = QTableWidget()
        self.students_table.setColumnCount(6)
        self.students_table.setHorizontalHeaderLabels([
            "Фамилия", "Имя", "Отчество", "Дата рождения", "Пол", "Класс"
        ])
        self.students_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addLayout(search_layout)
        layout.addWidget(info_label)
        layout.addWidget(self.students_table)
        tab.setLayout(layout)

        self.tabs.addTab(tab, "Ученики")
        self.load_students()

    def init_teachers_tab_readonly(self):
        """Вкладка учителей только для чтения"""
        tab = QWidget()
        layout = QVBoxLayout()

        # Поиск
        search_layout = QHBoxLayout()
        self.teacher_search = QLineEdit()
        self.teacher_search.setPlaceholderText("Поиск учителей...")
        self.teacher_search.textChanged.connect(self.load_teachers)
        search_layout.addWidget(QLabel("Поиск:"))
        search_layout.addWidget(self.teacher_search)

        # Информационная панель для завуча
        info_label = QLabel("👁️ Режим просмотра (завуч)")
        info_label.setStyleSheet("background-color: #E8D5C4; padding: 8px; border-radius: 4px; font-weight: bold;")

        # Таблица
        self.teachers_table = QTableWidget()
        self.teachers_table.setColumnCount(5)
        self.teachers_table.setHorizontalHeaderLabels([
            "Фамилия", "Имя", "Отчество", "Зарплата", "Недельные часы"
        ])
        self.teachers_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addLayout(search_layout)
        layout.addWidget(info_label)
        layout.addWidget(self.teachers_table)
        tab.setLayout(layout)

        self.tabs.addTab(tab, "Учителя")
        self.load_teachers()

    def init_classes_tab_readonly(self):
        """Вкладка классов только для чтения"""
        tab = QWidget()
        layout = QVBoxLayout()

        # Поиск
        search_layout = QHBoxLayout()
        self.class_search = QLineEdit()
        self.class_search.setPlaceholderText("Поиск классов...")
        self.class_search.textChanged.connect(self.load_classes)
        search_layout.addWidget(QLabel("Поиск:"))
        search_layout.addWidget(self.class_search)

        # Информационная панель для завуча
        info_label = QLabel("👁️ Режим просмотра (завуч)")
        info_label.setStyleSheet("background-color: #E8D5C4; padding: 8px; border-radius: 4px; font-weight: bold;")

        # Таблица
        self.classes_table = QTableWidget()
        self.classes_table.setColumnCount(4)
        self.classes_table.setHorizontalHeaderLabels([
            "Номер класса", "Количество учеников", "Классный руководитель", "Кабинет"
        ])
        self.classes_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addLayout(search_layout)
        layout.addWidget(info_label)
        layout.addWidget(self.classes_table)
        tab.setLayout(layout)

        self.tabs.addTab(tab, "Классы")
        self.load_classes()

    def init_subjects_tab_readonly(self):
        """Вкладка предметов только для чтения"""
        tab = QWidget()
        layout = QVBoxLayout()

        # Поиск
        search_layout = QHBoxLayout()
        self.subject_search = QLineEdit()
        self.subject_search.setPlaceholderText("Поиск предметов...")
        self.subject_search.textChanged.connect(self.load_subjects)
        search_layout.addWidget(QLabel("Поиск:"))
        search_layout.addWidget(self.subject_search)

        # Информационная панель для завуча
        info_label = QLabel("👁️ Режим просмотра (завуч)")
        info_label.setStyleSheet("background-color: #E8D5C4; padding: 8px; border-radius: 4px; font-weight: bold;")

        # Таблица
        self.subjects_table = QTableWidget()
        self.subjects_table.setColumnCount(3)
        self.subjects_table.setHorizontalHeaderLabels([
            "Название предмета", "Учитель", "Недельные часы"
        ])
        self.subjects_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addLayout(search_layout)
        layout.addWidget(info_label)
        layout.addWidget(self.subjects_table)
        tab.setLayout(layout)

        self.tabs.addTab(tab, "Предметы")
        self.load_subjects()

    def init_lessons_tab_readonly(self):
        """Вкладка расписания только для чтения"""
        tab = QWidget()
        layout = QVBoxLayout()

        # Поиск и фильтры
        filter_layout = QHBoxLayout()

        self.lesson_search = QLineEdit()
        self.lesson_search.setPlaceholderText("Поиск уроков...")
        self.lesson_search.textChanged.connect(self.load_lessons)

        self.lesson_class_filter = QComboBox()
        self.load_classes_for_lessons()
        self.lesson_class_filter.currentIndexChanged.connect(self.load_lessons)

        self.lesson_day_filter = QComboBox()
        self.lesson_day_filter.addItem("Все дни", None)
        self.lesson_day_filter.addItems([
            "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"
        ])
        self.lesson_day_filter.currentIndexChanged.connect(self.load_lessons)

        filter_layout.addWidget(QLabel("Поиск:"))
        filter_layout.addWidget(self.lesson_search)
        filter_layout.addWidget(QLabel("Класс:"))
        filter_layout.addWidget(self.lesson_class_filter)
        filter_layout.addWidget(QLabel("День:"))
        filter_layout.addWidget(self.lesson_day_filter)

        # Информационная панель для завуча
        info_label = QLabel("👁️ Режим просмотра (завуч)")
        info_label.setStyleSheet("background-color: #E8D5C4; padding: 8px; border-radius: 4px; font-weight: bold;")

        # Таблица
        self.lessons_table = QTableWidget()
        self.lessons_table.setColumnCount(6)
        self.lessons_table.setHorizontalHeaderLabels([
            "Класс", "Предмет", "День недели", "Время", "Кабинет", "Учитель"
        ])
        self.lessons_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addLayout(filter_layout)
        layout.addWidget(info_label)
        layout.addWidget(self.lessons_table)
        tab.setLayout(layout)

        self.tabs.addTab(tab, "Расписание")
        self.load_lessons()

    def init_grades_tab_readonly(self):
        """Вкладка оценок только для чтения"""
        tab = QWidget()
        layout = QVBoxLayout()

        # Фильтры
        filter_layout = QVBoxLayout()

        # Первая строка фильтров - общий поиск
        search_layout = QHBoxLayout()
        self.grade_search = QLineEdit()
        self.grade_search.setPlaceholderText("Поиск по всем параметрам...")
        self.grade_search.textChanged.connect(self.load_grades)
        search_layout.addWidget(QLabel("Поиск:"))
        search_layout.addWidget(self.grade_search)

        # Вторая строка фильтров - специфичные фильтры
        specific_filters_layout = QHBoxLayout()

        self.grade_student_filter = QComboBox()
        self.load_students_for_grades()
        self.grade_student_filter.currentIndexChanged.connect(self.load_grades)

        self.grade_date_filter = QComboBox()
        self.load_dates_for_grades()
        self.grade_date_filter.currentIndexChanged.connect(self.load_grades)

        self.grade_subject_filter = QComboBox()
        self.load_subjects_for_grades()
        self.grade_subject_filter.currentIndexChanged.connect(self.load_grades)

        specific_filters_layout.addWidget(QLabel("Ученик:"))
        specific_filters_layout.addWidget(self.grade_student_filter)
        specific_filters_layout.addWidget(QLabel("Дата:"))
        specific_filters_layout.addWidget(self.grade_date_filter)
        specific_filters_layout.addWidget(QLabel("Предмет:"))
        specific_filters_layout.addWidget(self.grade_subject_filter)

        self.btn_reset_filters = QPushButton("Сбросить фильтры")
        self.btn_reset_filters.clicked.connect(self.reset_grade_filters)
        specific_filters_layout.addWidget(self.btn_reset_filters)

        filter_layout.addLayout(search_layout)
        filter_layout.addLayout(specific_filters_layout)

        # Информационная панель для завуча
        info_label = QLabel("👁️ Режим просмотра (завуч)")
        info_label.setStyleSheet("background-color: #E8D5C4; padding: 8px; border-radius: 4px; font-weight: bold;")

        # Таблица
        self.grades_table = QTableWidget()
        self.grades_table.setColumnCount(6)
        self.grades_table.setHorizontalHeaderLabels([
            "Ученик", "Предмет", "Оценка", "Дата", "Тип", "Комментарий"
        ])
        self.grades_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addLayout(filter_layout)
        layout.addWidget(info_label)
        layout.addWidget(self.grades_table)
        tab.setLayout(layout)

        self.tabs.addTab(tab, "Оценки")
        self.load_grades()

    def init_progress_tab_readonly(self):
        """Вкладка итоговых оценок только для чтения"""
        tab = QWidget()
        layout = QVBoxLayout()

        # Фильтры
        filter_layout = QVBoxLayout()

        # Первая строка - общий поиск
        search_layout = QHBoxLayout()
        self.progress_search = QLineEdit()
        self.progress_search.setPlaceholderText("Поиск по всем параметрам...")
        self.progress_search.textChanged.connect(self.load_progress)
        search_layout.addWidget(QLabel("Поиск:"))
        search_layout.addWidget(self.progress_search)

        # Вторая строка - специфичные фильтры
        specific_filters_layout = QHBoxLayout()

        self.progress_student_filter = QComboBox()
        self.load_students_for_progress()
        self.progress_student_filter.currentIndexChanged.connect(self.load_progress)

        self.progress_period_filter = QComboBox()
        self.progress_period_filter.addItem("Все периоды", None)
        self.progress_period_filter.addItem("четверть", "четверть")
        self.progress_period_filter.addItem("полугодие", "полугодие")
        self.progress_period_filter.addItem("год", "год")
        self.progress_period_filter.currentIndexChanged.connect(self.load_progress)

        self.progress_year_filter = QComboBox()
        self.load_years_for_progress()
        self.progress_year_filter.currentIndexChanged.connect(self.load_progress)

        self.progress_subject_filter = QComboBox()
        self.load_subjects_for_progress()
        self.progress_subject_filter.currentIndexChanged.connect(self.load_progress)

        specific_filters_layout.addWidget(QLabel("Ученик:"))
        specific_filters_layout.addWidget(self.progress_student_filter)
        specific_filters_layout.addWidget(QLabel("Период:"))
        specific_filters_layout.addWidget(self.progress_period_filter)
        specific_filters_layout.addWidget(QLabel("Учебный год:"))
        specific_filters_layout.addWidget(self.progress_year_filter)
        specific_filters_layout.addWidget(QLabel("Предмет:"))
        specific_filters_layout.addWidget(self.progress_subject_filter)

        self.btn_reset_progress_filters = QPushButton("Сбросить фильтры")
        self.btn_reset_progress_filters.clicked.connect(self.reset_progress_filters)
        specific_filters_layout.addWidget(self.btn_reset_progress_filters)

        filter_layout.addLayout(search_layout)
        filter_layout.addLayout(specific_filters_layout)

        # Информационная панель для завуча
        info_label = QLabel("👁️ Режим просмотра (завуч)")
        info_label.setStyleSheet("background-color: #E8D5C4; padding: 8px; border-radius: 4px; font-weight: bold;")

        # Таблица
        self.progress_table = QTableWidget()
        self.progress_table.setColumnCount(7)
        self.progress_table.setHorizontalHeaderLabels([
            "Ученик", "Предмет", "Период", "Номер периода", "Учебный год", "Средний балл", "Итоговая оценка"
        ])
        self.progress_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addLayout(filter_layout)
        layout.addWidget(info_label)
        layout.addWidget(self.progress_table)
        tab.setLayout(layout)

        self.tabs.addTab(tab, "Итоговые оценки")
        self.load_progress()



    def init_students_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Поиск
        search_layout = QHBoxLayout()
        self.student_search = QLineEdit()
        self.student_search.setPlaceholderText("Поиск учеников...")
        self.student_search.textChanged.connect(self.load_students)
        search_layout.addWidget(QLabel("Поиск:"))
        search_layout.addWidget(self.student_search)

        # Кнопки управления
        btn_layout = QHBoxLayout()
        self.btn_add_student = QPushButton("Добавить ученика")
        self.btn_edit_student = QPushButton("Редактировать")
        self.btn_delete_student = QPushButton("Удалить")

        btn_layout.addWidget(self.btn_add_student)
        btn_layout.addWidget(self.btn_edit_student)
        btn_layout.addWidget(self.btn_delete_student)
        btn_layout.addStretch()

        # Таблица
        self.students_table = QTableWidget()
        self.students_table.setColumnCount(6)
        self.students_table.setHorizontalHeaderLabels([
            "Фамилия", "Имя", "Отчество", "Дата рождения", "Пол", "Класс"
        ])
        self.students_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addLayout(search_layout)
        layout.addLayout(btn_layout)
        layout.addWidget(self.students_table)
        tab.setLayout(layout)

        self.tabs.addTab(tab, "Ученики")

        # Подключаем события
        self.btn_add_student.clicked.connect(self.add_student)
        self.btn_edit_student.clicked.connect(self.edit_student)
        self.btn_delete_student.clicked.connect(self.delete_student)

        self.load_students()

    def load_students(self):
        search_text = self.student_search.text()
        query = """
                SELECT s.student_id, \
                       s.last_name, \
                       s.first_name, \
                       s.middle_name,
                       s.birth_date, \
                       s.gender, \
                       c.class_number
                FROM students s
                         LEFT JOIN classes c ON s.class_id = c.class_id
                WHERE s.last_name ILIKE %s \
                   OR s.first_name ILIKE %s \
                   OR s.middle_name ILIKE %s
                   OR c.class_number ILIKE %s \
                   OR s.gender ILIKE %s
                   OR TO_CHAR(s.birth_date \
                    , 'DD.MM.YYYY') ILIKE %s
                ORDER BY s.last_name, s.first_name \
                """
        search_param = f"%{search_text}%"
        data = self.db.execute(query,
                               (search_param, search_param, search_param, search_param, search_param, search_param))

        self.students_table.setRowCount(len(data))
        for row_idx, row in enumerate(data):
            # Пропускаем student_id при отображении
            for col_idx in range(1, len(row)):
                value = row[col_idx]
                if col_idx == 4 and value:  # Дата рождения
                    value = value.strftime("%d.%m.%Y")
                item = QTableWidgetItem(str(value) if value else "")
                item.setData(Qt.UserRole, row[0])  # Сохраняем ID для операций
                self.students_table.setItem(row_idx, col_idx - 1, item)

    def add_student(self):
        dialog = StudentDialog(self.db)
        if dialog.exec_() == QDialog.Accepted:
            self.load_students()
            # Обновляем также таблицу классов, если она видима
            try:
                self.load_classes()
            except:
                pass  # Если метод еще не инициализирован, игнорируем


    def edit_student(self):
        current_row = self.students_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Выберите ученика для редактирования")
            return

        student_id = self.students_table.item(current_row, 0).data(Qt.UserRole)
        dialog = StudentDialog(self.db, student_id)
        if dialog.exec_() == QDialog.Accepted:
            self.load_students()
            try:
                self.load_classes()  # ДОБАВИЛ ЭТУ СТРОКУ
            except:
                pass

    def delete_student(self):
        current_row = self.students_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Выберите ученика для удаления")
            return

        student_id = self.students_table.item(current_row, 0).data(Qt.UserRole)

        reply = QMessageBox.question(self, "Подтверждение",
                                     "Вы уверены, что хотите удалить этого ученика?\n"
                                     "Все связанные оценки также будут удалены.",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                self.db.execute("DELETE FROM students WHERE student_id = %s", (student_id,), fetch=False)
                self.load_students()
                try:
                    self.load_classes()  # ДОБАВИЛ ЭТУ СТРОКУ
                except:
                    pass
                QMessageBox.information(self, "Успех", "Ученик удален")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить ученика:\n{str(e)}")


    def init_teachers_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Поиск
        search_layout = QHBoxLayout()
        self.teacher_search = QLineEdit()
        self.teacher_search.setPlaceholderText("Поиск учителей...")
        self.teacher_search.textChanged.connect(self.load_teachers)
        search_layout.addWidget(QLabel("Поиск:"))
        search_layout.addWidget(self.teacher_search)

        # Кнопки управления
        btn_layout = QHBoxLayout()
        self.btn_add_teacher = QPushButton("Добавить учителя")
        self.btn_edit_teacher = QPushButton("Редактировать")
        self.btn_delete_teacher = QPushButton("Удалить")  # ДОБАВИЛИ КНОПКУ УДАЛИТЬ

        btn_layout.addWidget(self.btn_add_teacher)
        btn_layout.addWidget(self.btn_edit_teacher)
        btn_layout.addWidget(self.btn_delete_teacher)  # ДОБАВИЛИ В ЛЕЙАУТ
        btn_layout.addStretch()

        # Таблица
        self.teachers_table = QTableWidget()
        self.teachers_table.setColumnCount(5)
        self.teachers_table.setHorizontalHeaderLabels([
            "Фамилия", "Имя", "Отчество", "Зарплата", "Недельные часы"
        ])
        self.teachers_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addLayout(search_layout)
        layout.addLayout(btn_layout)
        layout.addWidget(self.teachers_table)
        tab.setLayout(layout)

        self.tabs.addTab(tab, "Учителя")

        # Подключаем события
        self.btn_add_teacher.clicked.connect(self.add_teacher)
        self.btn_edit_teacher.clicked.connect(self.edit_teacher)
        self.btn_delete_teacher.clicked.connect(self.delete_teacher)  # ПОДКЛЮЧИЛИ СОБЫТИЕ

        self.load_teachers()




    def load_teachers(self):
        search_text = self.teacher_search.text()
        query = """
                SELECT teacher_id, last_name, first_name, middle_name, salary, weekly_hours
                FROM teachers
                WHERE last_name ILIKE %s \
                   OR first_name ILIKE %s
                ORDER BY last_name, first_name \
                """
        search_param = f"%{search_text}%"
        data = self.db.execute(query, (search_param, search_param))

        self.teachers_table.setRowCount(len(data))
        for row_idx, row in enumerate(data):
            # Пропускаем teacher_id при отображении
            for col_idx in range(1, len(row)):
                value = row[col_idx]
                item = QTableWidgetItem(str(value) if value else "")
                item.setData(Qt.UserRole, row[0])  # Сохраняем ID
                self.teachers_table.setItem(row_idx, col_idx - 1, item)

    def add_teacher(self):
        dialog = TeacherDialog(self.db)
        if dialog.exec_() == QDialog.Accepted:
            self.load_teachers()

    def edit_teacher(self):
        current_row = self.teachers_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Выберите учителя для редактирования")
            return

        teacher_id = self.teachers_table.item(current_row, 0).data(Qt.UserRole)
        dialog = TeacherDialog(self.db, teacher_id)
        if dialog.exec_() == QDialog.Accepted:
            self.load_teachers()


    def delete_teacher(self):
        """Удаление выбранного учителя"""
        current_row = self.teachers_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Выберите учителя для удаления")
            return

        teacher_id = self.teachers_table.item(current_row, 0).data(Qt.UserRole)

        # Получаем информацию об учителе для подтверждения
        teacher_info = self.db.execute(
            "SELECT last_name, first_name, middle_name FROM teachers WHERE teacher_id = %s",
            (teacher_id,)
        )

        if not teacher_info:
            QMessageBox.warning(self, "Ошибка", "Учитель не найден")
            return

        teacher_name = f"{teacher_info[0][0]} {teacher_info[0][1]} {teacher_info[0][2] or ''}".strip()

        # Проверяем, связан ли учитель с предметами или классами
        subjects_count = self.db.execute(
            "SELECT COUNT(*) FROM subjects WHERE teacher_id = %s", (teacher_id,)
        )[0][0]

        classes_count = self.db.execute(
            "SELECT COUNT(*) FROM classes WHERE homeroom_teacher_id = %s", (teacher_id,)
        )[0][0]

        # Формируем сообщение с предупреждениями
        warning_message = f"Вы уверены, что хотите удалить учителя {teacher_name}?"

        if subjects_count > 0:
            warning_message += f"\n\nВНИМАНИЕ: У этого учителя есть {subjects_count} предмет(ов)."
            warning_message += "\nПри удалении учителя, у этих предметов будет удален преподаватель."

        if classes_count > 0:
            warning_message += f"\n\nВНИМАНИЕ: Этот учитель является классным руководителем {classes_count} класса(ов)."
            warning_message += "\nПри удалении учителя, у этих классов будет удален классный руководитель."

        warning_message += "\n\nПродолжить удаление?"

        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            warning_message,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No  # По умолчанию "Нет"
        )

        if reply == QMessageBox.Yes:
            try:
                # Начинаем транзакцию
                self.db.cursor.execute("BEGIN")

                # Обновляем предметы - убираем ссылку на учителя
                if subjects_count > 0:
                    self.db.execute(
                        "UPDATE subjects SET teacher_id = NULL WHERE teacher_id = %s",
                        (teacher_id,),
                        fetch=False
                    )

                # Обновляем классы - убираем ссылку на классного руководителя
                if classes_count > 0:
                    self.db.execute(
                        "UPDATE classes SET homeroom_teacher_id = NULL WHERE homeroom_teacher_id = %s",
                        (teacher_id,),
                        fetch=False
                    )

                # Удаляем оценки, поставленные этим учителем
                self.db.execute(
                    "DELETE FROM grades WHERE teacher_id = %s",
                    (teacher_id,),
                    fetch=False
                )

                # Удаляем самого учителя
                self.db.execute(
                    "DELETE FROM teachers WHERE teacher_id = %s",
                    (teacher_id,),
                    fetch=False
                )

                # Подтверждаем транзакцию
                self.db.conn.commit()

                # Обновляем таблицы
                self.load_teachers()
                try:
                    self.load_subjects()  # Обновляем предметы
                    self.load_classes()  # Обновляем классы
                except:
                    pass  # Если методы еще не инициализированы, игнорируем

                QMessageBox.information(self, "Успех", f"Учитель {teacher_name} успешно удален")

            except Exception as e:
                # Откатываем транзакцию в случае ошибки
                self.db.conn.rollback()
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить учителя:\n{str(e)}")




    def init_classes_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Поиск
        search_layout = QHBoxLayout()
        self.class_search = QLineEdit()
        self.class_search.setPlaceholderText("Поиск классов...")
        self.class_search.textChanged.connect(self.load_classes)
        search_layout.addWidget(QLabel("Поиск:"))
        search_layout.addWidget(self.class_search)

        # Кнопки управления
        btn_layout = QHBoxLayout()
        self.btn_add_class = QPushButton("Добавить класс")
        self.btn_edit_class = QPushButton("Редактировать")
        self.btn_delete_class = QPushButton("Удалить")  # ДОБАВИЛИ КНОПКУ УДАЛИТЬ

        btn_layout.addWidget(self.btn_add_class)
        btn_layout.addWidget(self.btn_edit_class)
        btn_layout.addWidget(self.btn_delete_class)  # ДОБАВИЛИ В ЛЕЙАУТ
        btn_layout.addStretch()

        # Таблица
        self.classes_table = QTableWidget()
        self.classes_table.setColumnCount(4)
        self.classes_table.setHorizontalHeaderLabels([
            "Номер класса", "Количество учеников", "Классный руководитель", "Кабинет"
        ])
        self.classes_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addLayout(search_layout)
        layout.addLayout(btn_layout)
        layout.addWidget(self.classes_table)
        tab.setLayout(layout)

        self.tabs.addTab(tab, "Классы")

        # Подключаем события
        self.btn_add_class.clicked.connect(self.add_class)
        self.btn_edit_class.clicked.connect(self.edit_class)
        self.btn_delete_class.clicked.connect(self.delete_class)  # ПОДКЛЮЧИЛИ СОБЫТИЕ

        self.load_classes()

    def delete_class(self):
        """Удаление выбранного класса"""
        current_row = self.classes_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Выберите класс для удаления")
            return

        class_id = self.classes_table.item(current_row, 0).data(Qt.UserRole)

        # Получаем информацию о классе для подтверждения
        class_info = self.db.execute(
            "SELECT class_number, student_count FROM classes WHERE class_id = %s",
            (class_id,)
        )

        if not class_info:
            QMessageBox.warning(self, "Ошибка", "Класс не найден")
            return

        class_number = class_info[0][0]
        student_count = class_info[0][1] or 0

        # Проверяем, есть ли ученики в этом классе
        actual_students = self.db.execute(
            "SELECT COUNT(*) FROM students WHERE class_id = %s", (class_id,)
        )[0][0]

        # Получаем список учеников для отображения
        students_list = []
        if actual_students > 0:
            students = self.db.execute("""
                                       SELECT CONCAT(last_name, ' ', first_name, ' ', COALESCE(middle_name, '')) as full_name
                                       FROM students
                                       WHERE class_id = %s
                                       ORDER BY last_name, first_name LIMIT 10
                                       """, (class_id,))
            students_list = [student[0] for student in students]

        # Формируем сообщение с предупреждениями
        warning_message = f"Вы уверены, что хотите удалить класс {class_number}?"

        if actual_students > 0:
            warning_message += f"\n\nВНИМАНИЕ: В этом классе учится {actual_students} ученик(ов):"
            for i, student_name in enumerate(students_list):
                if i < 5:  # Показываем первых 5 учеников
                    warning_message += f"\n• {student_name}"
                elif i == 5:
                    warning_message += f"\n• ... и еще {actual_students - 5} ученик(ов)"
                    break

            warning_message += "\n\nПри удалении класса:"
            warning_message += "\n- Все ученики этого класса будут переведены в статус 'Без класса'"
            warning_message += "\n- Все связанные данные об успеваемости сохранятся"
        else:
            warning_message += f"\n\nКласс пустой (нет учеников), удаление безопасно."

        warning_message += "\n\nПродолжить удаление?"

        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            warning_message,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No  # По умолчанию "Нет"
        )

        if reply == QMessageBox.Yes:
            try:
                # Начинаем транзакцию
                self.db.cursor.execute("BEGIN")

                # Переводим всех учеников в статус "Без класса"
                if actual_students > 0:
                    self.db.execute(
                        "UPDATE students SET class_id = NULL WHERE class_id = %s",
                        (class_id,),
                        fetch=False
                    )

                # Удаляем класс
                self.db.execute(
                    "DELETE FROM classes WHERE class_id = %s",
                    (class_id,),
                    fetch=False
                )

                # Подтверждаем транзакцию
                self.db.conn.commit()

                # Обновляем таблицы
                self.load_classes()
                try:
                    self.load_students()  # Обновляем учеников
                except:
                    pass  # Если метод еще не инициализирован, игнорируем

                success_message = f"Класс {class_number} успешно удален"
                if actual_students > 0:
                    success_message += f"\n{actual_students} ученик(ов) переведены в статус 'Без класса'"

                QMessageBox.information(self, "Успех", success_message)

            except Exception as e:
                # Откатываем транзакцию в случае ошибки
                self.db.conn.rollback()
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить класс:\n{str(e)}")



    def load_classes(self):
        search_text = self.class_search.text()
        query = """
                SELECT c.class_id, \
                       c.class_number, \
                       c.student_count,
                       CONCAT(t.last_name, ' ', t.first_name, ' ', COALESCE(t.middle_name, '')) as teacher_name,
                       c.classroom
                FROM classes c
                         LEFT JOIN teachers t ON c.homeroom_teacher_id = t.teacher_id
                WHERE c.class_number ILIKE %s
                ORDER BY c.class_number \
                """
        search_param = f"%{search_text}%"
        data = self.db.execute(query, (search_param,))

        self.classes_table.setRowCount(len(data))
        for row_idx, row in enumerate(data):
            # Пропускаем class_id при отображении
            for col_idx in range(1, len(row)):
                value = row[col_idx]
                item = QTableWidgetItem(str(value) if value else "")
                item.setData(Qt.UserRole, row[0])  # Сохраняем ID
                self.classes_table.setItem(row_idx, col_idx - 1, item)

    def add_class(self):
        dialog = ClassDialog(self.db)
        if dialog.exec_() == QDialog.Accepted:
            self.load_classes()

    def edit_class(self):
        current_row = self.classes_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Выберите класс для редактирования")
            return

        class_id = self.classes_table.item(current_row, 0).data(Qt.UserRole)
        dialog = ClassDialog(self.db, class_id)
        if dialog.exec_() == QDialog.Accepted:
            self.load_classes()


    def init_subjects_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Поиск
        search_layout = QHBoxLayout()
        self.subject_search = QLineEdit()
        self.subject_search.setPlaceholderText("Поиск предметов...")
        self.subject_search.textChanged.connect(self.load_subjects)
        search_layout.addWidget(QLabel("Поиск:"))
        search_layout.addWidget(self.subject_search)

        # Кнопки управления
        btn_layout = QHBoxLayout()
        self.btn_add_subject = QPushButton("Добавить предмет")
        self.btn_edit_subject = QPushButton("Редактировать")
        self.btn_delete_subject = QPushButton("Удалить")  # ДОБАВИЛИ КНОПКУ УДАЛИТЬ

        btn_layout.addWidget(self.btn_add_subject)
        btn_layout.addWidget(self.btn_edit_subject)
        btn_layout.addWidget(self.btn_delete_subject)  # ДОБАВИЛИ В ЛЕЙАУТ
        btn_layout.addStretch()

        # Таблица
        self.subjects_table = QTableWidget()
        self.subjects_table.setColumnCount(3)
        self.subjects_table.setHorizontalHeaderLabels([
            "Название предмета", "Учитель", "Недельные часы"
        ])
        self.subjects_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addLayout(search_layout)
        layout.addLayout(btn_layout)
        layout.addWidget(self.subjects_table)
        tab.setLayout(layout)

        self.tabs.addTab(tab, "Предметы")

        # Подключаем события
        self.btn_add_subject.clicked.connect(self.add_subject)
        self.btn_edit_subject.clicked.connect(self.edit_subject)
        self.btn_delete_subject.clicked.connect(self.delete_subject)  # ПОДКЛЮЧИЛИ СОБЫТИЕ

        self.load_subjects()

    def delete_subject(self):
        """Удаление выбранного предмета"""
        current_row = self.subjects_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Выберите предмет для удаления")
            return

        subject_id = self.subjects_table.item(current_row, 0).data(Qt.UserRole)

        # Получаем информацию о предмете для подтверждения
        subject_info = self.db.execute(
            "SELECT subject_name, weekly_hours FROM subjects WHERE subject_id = %s",
            (subject_id,)
        )

        if not subject_info:
            QMessageBox.warning(self, "Ошибка", "Предмет не найден")
            return

        subject_name = subject_info[0][0]
        weekly_hours = subject_info[0][1]

        # Проверяем количество оценок по этому предмету
        grades_count = self.db.execute(
            "SELECT COUNT(*) FROM grades WHERE subject_id = %s", (subject_id,)
        )[0][0]

        # Проверяем количество записей в итоговых оценках
        progress_count = self.db.execute(
            "SELECT COUNT(*) FROM student_progress WHERE subject_id = %s", (subject_id,)
        )[0][0]

        # Получаем статистику по оценкам
        grades_stats = None
        if grades_count > 0:
            grades_stats = self.db.execute("""
                                           SELECT COUNT(DISTINCT student_id) as students_count,
                                                  MIN(grade_date)            as first_grade_date,
                                                  MAX(grade_date)            as last_grade_date,
                                                  AVG(grade)                 as avg_grade
                                           FROM grades
                                           WHERE subject_id = %s
                                           """, (subject_id,))[0]

        # Получаем информацию об учителе
        teacher_info = self.db.execute("""
                                       SELECT CONCAT(last_name, ' ', first_name, ' ', COALESCE(middle_name, ''))
                                       FROM teachers t
                                                JOIN subjects s ON t.teacher_id = s.teacher_id
                                       WHERE s.subject_id = %s
                                       """, (subject_id,))

        teacher_name = teacher_info[0][0] if teacher_info else "Не назначен"

        # Формируем сообщение с предупреждениями
        warning_message = f"Вы уверены, что хотите удалить предмет '{subject_name}'?"
        warning_message += f"\nПреподаватель: {teacher_name}"
        if weekly_hours:
            warning_message += f"\nНедельные часы: {weekly_hours}"

        if grades_count > 0:
            warning_message += f"\n\n🚨 ВНИМАНИЕ: По этому предмету есть {grades_count} оценок!"
            if grades_stats:
                warning_message += f"\n📊 Статистика:"
                warning_message += f"\n   • Учеников с оценками: {grades_stats[0]}"
                warning_message += f"\n   • Период оценок: с {grades_stats[1].strftime('%d.%m.%Y')} по {grades_stats[2].strftime('%d.%m.%Y')}"
                warning_message += f"\n   • Средний балл: {grades_stats[3]:.2f}"

        if progress_count > 0:
            warning_message += f"\n\n📈 ВНИМАНИЕ: По этому предмету есть {progress_count} итоговых оценок!"

        if grades_count > 0 or progress_count > 0:
            warning_message += "\n\n❌ При удалении предмета будут БЕЗВОЗВРАТНО удалены:"
            if grades_count > 0:
                warning_message += f"\n   • Все {grades_count} оценок"
            if progress_count > 0:
                warning_message += f"\n   • Все {progress_count} итоговых оценок"
            warning_message += "\n\n⚠️  ЭТО ДЕЙСТВИЕ НЕЛЬЗЯ ОТМЕНИТЬ!"
        else:
            warning_message += "\n\n✅ Предмет не имеет связанных оценок, удаление безопасно."

        warning_message += "\n\nПродолжить удаление?"

        # Используем более серьезное предупреждение, если есть оценки
        if grades_count > 0 or progress_count > 0:
            reply = QMessageBox.critical(
                self,
                "⚠️ ОПАСНОЕ УДАЛЕНИЕ",
                warning_message,
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No  # По умолчанию "Нет"
            )
        else:
            reply = QMessageBox.question(
                self,
                "Подтверждение удаления",
                warning_message,
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No  # По умолчанию "Нет"
            )

        if reply == QMessageBox.Yes:
            try:
                # Начинаем транзакцию
                self.db.cursor.execute("BEGIN")

                # Удаляем все связанные итоговые оценки
                if progress_count > 0:
                    self.db.execute(
                        "DELETE FROM student_progress WHERE subject_id = %s",
                        (subject_id,),
                        fetch=False
                    )

                # Удаляем все оценки по предмету
                if grades_count > 0:
                    self.db.execute(
                        "DELETE FROM grades WHERE subject_id = %s",
                        (subject_id,),
                        fetch=False
                    )

                # Удаляем сам предмет
                self.db.execute(
                    "DELETE FROM subjects WHERE subject_id = %s",
                    (subject_id,),
                    fetch=False
                )

                # Подтверждаем транзакцию
                self.db.conn.commit()

                # Обновляем таблицы
                self.load_subjects()
                try:
                    self.load_grades()  # Обновляем оценки
                    self.load_progress()  # Обновляем итоговые оценки
                except:
                    pass  # Если методы еще не инициализированы, игнорируем

                success_message = f"Предмет '{subject_name}' успешно удален"
                if grades_count > 0 or progress_count > 0:
                    success_message += "\n\nБыли удалены:"
                    if grades_count > 0:
                        success_message += f"\n• {grades_count} оценок"
                    if progress_count > 0:
                        success_message += f"\n• {progress_count} итоговых оценок"

                QMessageBox.information(self, "Успех", success_message)

            except Exception as e:
                # Откатываем транзакцию в случае ошибки
                self.db.conn.rollback()
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить предмет:\n{str(e)}")


    def load_subjects(self):
        search_text = self.subject_search.text()
        query = """
                SELECT s.subject_id, \
                       s.subject_name,
                       CONCAT(t.last_name, ' ', t.first_name, ' ', COALESCE(t.middle_name, '')) as teacher_name,
                       s.weekly_hours
                FROM subjects s
                         LEFT JOIN teachers t ON s.teacher_id = t.teacher_id
                WHERE s.subject_name ILIKE %s
                ORDER BY s.subject_name \
                """
        search_param = f"%{search_text}%"
        data = self.db.execute(query, (search_param,))

        self.subjects_table.setRowCount(len(data))
        for row_idx, row in enumerate(data):
            # Пропускаем subject_id при отображении
            for col_idx in range(1, len(row)):
                value = row[col_idx]
                item = QTableWidgetItem(str(value) if value else "")
                item.setData(Qt.UserRole, row[0])  # Сохраняем ID
                self.subjects_table.setItem(row_idx, col_idx - 1, item)

    def add_subject(self):
        dialog = SubjectDialog(self.db)
        if dialog.exec_() == QDialog.Accepted:
            self.load_subjects()

    def edit_subject(self):
        current_row = self.subjects_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Выберите предмет для редактирования")
            return

        subject_id = self.subjects_table.item(current_row, 0).data(Qt.UserRole)
        dialog = SubjectDialog(self.db, subject_id)
        if dialog.exec_() == QDialog.Accepted:
            self.load_subjects()

    def init_lessons_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Поиск и фильтры
        filter_layout = QHBoxLayout()

        self.lesson_search = QLineEdit()
        self.lesson_search.setPlaceholderText("Поиск уроков...")
        self.lesson_search.textChanged.connect(self.load_lessons)

        self.lesson_class_filter = QComboBox()
        self.load_classes_for_lessons()
        self.lesson_class_filter.currentIndexChanged.connect(self.load_lessons)

        self.lesson_day_filter = QComboBox()
        self.lesson_day_filter.addItem("Все дни", None)
        self.lesson_day_filter.addItems([
            "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"
        ])
        self.lesson_day_filter.currentIndexChanged.connect(self.load_lessons)

        filter_layout.addWidget(QLabel("Поиск:"))
        filter_layout.addWidget(self.lesson_search)
        filter_layout.addWidget(QLabel("Класс:"))
        filter_layout.addWidget(self.lesson_class_filter)
        filter_layout.addWidget(QLabel("День:"))
        filter_layout.addWidget(self.lesson_day_filter)

        # Кнопки управления
        btn_layout = QHBoxLayout()
        self.btn_add_lesson = QPushButton("Добавить урок")
        self.btn_edit_lesson = QPushButton("Редактировать")
        self.btn_delete_lesson = QPushButton("Удалить")

        btn_layout.addWidget(self.btn_add_lesson)
        btn_layout.addWidget(self.btn_edit_lesson)
        btn_layout.addWidget(self.btn_delete_lesson)
        btn_layout.addStretch()

        # Таблица
        self.lessons_table = QTableWidget()
        self.lessons_table.setColumnCount(6)
        self.lessons_table.setHorizontalHeaderLabels([
            "Класс", "Предмет", "День недели", "Время", "Кабинет", "Учитель"
        ])
        self.lessons_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addLayout(filter_layout)
        layout.addLayout(btn_layout)
        layout.addWidget(self.lessons_table)
        tab.setLayout(layout)

        self.tabs.addTab(tab, "Расписание")

        # Подключаем события
        self.btn_add_lesson.clicked.connect(self.add_lesson)
        self.btn_edit_lesson.clicked.connect(self.edit_lesson)
        self.btn_delete_lesson.clicked.connect(self.delete_lesson)

        self.load_lessons()

    def load_classes_for_lessons(self):
        self.lesson_class_filter.clear()
        self.lesson_class_filter.addItem("Все классы", None)

        classes = self.db.execute("""
                                  SELECT class_id, class_number
                                  FROM classes
                                  ORDER BY class_number
                                  """)

        for class_id, class_number in classes:
            self.lesson_class_filter.addItem(class_number, class_id)

    def load_lessons(self):
        search_text = self.lesson_search.text()
        class_id = self.lesson_class_filter.currentData()
        day_of_week = self.lesson_day_filter.currentText()

        query = """
                SELECT l.lesson_id,
                       c.class_number,
                       s.subject_name,
                       l.day_of_week,
                       l.lesson_time,
                       l.classroom,
                       CONCAT(t.last_name, ' ', t.first_name, ' ', COALESCE(t.middle_name, '')) as teacher_name
                FROM lessons l
                         JOIN classes c ON l.class_id = c.class_id
                         JOIN subjects s ON l.subject_id = s.subject_id
                         JOIN teachers t ON l.teacher_id = t.teacher_id
                WHERE 1 = 1 \
                """
        params = []

        if search_text:
            query += """ AND (
                c.class_number ILIKE %s OR
                s.subject_name ILIKE %s OR
                l.day_of_week ILIKE %s OR
                CONCAT(t.last_name, ' ', t.first_name, ' ', COALESCE(t.middle_name, '')) ILIKE %s OR
                l.classroom::text ILIKE %s
            )"""
            search_param = f"%{search_text}%"
            params.extend([search_param] * 5)

        if class_id:
            query += " AND l.class_id = %s"
            params.append(class_id)

        if day_of_week and day_of_week != "Все дни":
            query += " AND l.day_of_week = %s"
            params.append(day_of_week)

        query += """ ORDER BY 
            c.class_number,
            CASE l.day_of_week 
                WHEN 'Понедельник' THEN 1
                WHEN 'Вторник' THEN 2
                WHEN 'Среда' THEN 3
                WHEN 'Четверг' THEN 4
                WHEN 'Пятница' THEN 5
                WHEN 'Суббота' THEN 6
            END,
            l.lesson_time
        """

        data = self.db.execute(query, params)

        self.lessons_table.setRowCount(len(data))
        for row_idx, row in enumerate(data):
            # Пропускаем lesson_id при отображении
            for col_idx in range(1, len(row)):
                value = row[col_idx]
                # Форматируем время
                if col_idx == 4 and value:  # lesson_time
                    if hasattr(value, 'strftime'):
                        value = value.strftime("%H:%M")
                    else:
                        value = str(value)
                item = QTableWidgetItem(str(value) if value else "")
                item.setData(Qt.UserRole, row[0])  # Сохраняем lesson_id
                self.lessons_table.setItem(row_idx, col_idx - 1, item)

    def add_lesson(self):
        dialog = LessonDialog(self.db)
        if dialog.exec_() == QDialog.Accepted:
            self.load_lessons()

    def edit_lesson(self):
        current_row = self.lessons_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Выберите урок для редактирования")
            return

        lesson_id = self.lessons_table.item(current_row, 0).data(Qt.UserRole)
        dialog = LessonDialog(self.db, lesson_id)
        if dialog.exec_() == QDialog.Accepted:
            self.load_lessons()

    def delete_lesson(self):
        """Удаление выбранного урока"""
        current_row = self.lessons_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Выберите урок для удаления")
            return

        lesson_id = self.lessons_table.item(current_row, 0).data(Qt.UserRole)

        # Получаем информацию об уроке для подтверждения
        lesson_info = self.db.execute("""
                                      SELECT c.class_number,
                                             s.subject_name,
                                             l.day_of_week,
                                             l.lesson_time,
                                             l.classroom,
                                             CONCAT(t.last_name, ' ', t.first_name, ' ',
                                                    COALESCE(t.middle_name, '')) as teacher_name
                                      FROM lessons l
                                               JOIN classes c ON l.class_id = c.class_id
                                               JOIN subjects s ON l.subject_id = s.subject_id
                                               JOIN teachers t ON l.teacher_id = t.teacher_id
                                      WHERE l.lesson_id = %s
                                      """, (lesson_id,))

        if not lesson_info:
            QMessageBox.warning(self, "Ошибка", "Урок не найден")
            return

        class_number, subject_name, day_of_week, lesson_time, classroom, teacher_name = lesson_info[0]

        # Форматируем время для отображения
        if hasattr(lesson_time, 'strftime'):
            time_str = lesson_time.strftime("%H:%M")
        else:
            time_str = str(lesson_time)

        # Формируем сообщение с подтверждением
        warning_message = f"Вы уверены, что хотите удалить урок?"
        warning_message += f"\n\n📚 Детали урока:"
        warning_message += f"\n   • Класс: {class_number}"
        warning_message += f"\n   • Предмет: {subject_name}"
        warning_message += f"\n   • День: {day_of_week}"
        warning_message += f"\n   • Время: {time_str}"
        warning_message += f"\n   • Кабинет: {classroom or 'Не указан'}"
        warning_message += f"\n   • Учитель: {teacher_name}"

        warning_message += "\n\n⚠️  Удаление урока из расписания повлияет на:"
        warning_message += "\n   • Расписание класса"
        warning_message += "\n   • Нагрузку учителя"
        warning_message += "\n   • Использование кабинета"

        warning_message += "\n\nПродолжить удаление?"

        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            warning_message,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No  # По умолчанию "Нет"
        )

        if reply == QMessageBox.Yes:
            try:
                # Удаляем урок
                self.db.execute(
                    "DELETE FROM lessons WHERE lesson_id = %s",
                    (lesson_id,),
                    fetch=False
                )

                # Обновляем таблицу
                self.load_lessons()

                success_message = f"Урок успешно удален из расписания"
                success_message += f"\n\nУдаленный урок:"
                success_message += f"\n• {subject_name} ({class_number})"
                success_message += f"\n• {day_of_week} в {time_str}"
                success_message += f"\n• Учитель: {teacher_name}"

                QMessageBox.information(self, "Успех", success_message)

            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить урок:\n{str(e)}")


    def init_grades_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Фильтры
        filter_layout = QVBoxLayout()

        # Первая строка фильтров - общий поиск
        search_layout = QHBoxLayout()
        self.grade_search = QLineEdit()
        self.grade_search.setPlaceholderText("Поиск по всем параметрам (ученик, предмет, оценка, комментарий)...")
        self.grade_search.textChanged.connect(self.load_grades)
        search_layout.addWidget(QLabel("Поиск:"))
        search_layout.addWidget(self.grade_search)

        # Вторая строка фильтров - специфичные фильтры
        specific_filters_layout = QHBoxLayout()

        # Фильтр по ученику
        self.grade_student_filter = QComboBox()
        self.load_students_for_grades()
        self.grade_student_filter.currentIndexChanged.connect(self.load_grades)

        # Фильтр по дате
        self.grade_date_filter = QComboBox()
        self.load_dates_for_grades()
        self.grade_date_filter.currentIndexChanged.connect(self.load_grades)

        # Фильтр по предмету
        self.grade_subject_filter = QComboBox()
        self.load_subjects_for_grades()
        self.grade_subject_filter.currentIndexChanged.connect(self.load_grades)

        specific_filters_layout.addWidget(QLabel("Ученик:"))
        specific_filters_layout.addWidget(self.grade_student_filter)
        specific_filters_layout.addWidget(QLabel("Дата:"))
        specific_filters_layout.addWidget(self.grade_date_filter)
        specific_filters_layout.addWidget(QLabel("Предмет:"))
        specific_filters_layout.addWidget(self.grade_subject_filter)

        # Кнопка сброса фильтров
        self.btn_reset_filters = QPushButton("Сбросить фильтры")
        self.btn_reset_filters.clicked.connect(self.reset_grade_filters)
        specific_filters_layout.addWidget(self.btn_reset_filters)

        filter_layout.addLayout(search_layout)
        filter_layout.addLayout(specific_filters_layout)

        # Кнопки управления
        btn_layout = QHBoxLayout()
        self.btn_add_grade = QPushButton("Добавить оценку")
        self.btn_edit_grade = QPushButton("Редактировать")
        self.btn_delete_grade = QPushButton("Удалить")

        btn_layout.addWidget(self.btn_add_grade)
        btn_layout.addWidget(self.btn_edit_grade)
        btn_layout.addWidget(self.btn_delete_grade)
        btn_layout.addStretch()

        # Таблица
        self.grades_table = QTableWidget()
        self.grades_table.setColumnCount(6)
        self.grades_table.setHorizontalHeaderLabels([
            "Ученик", "Предмет", "Оценка", "Дата", "Тип", "Комментарий"
        ])
        self.grades_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addLayout(filter_layout)
        layout.addLayout(btn_layout)
        layout.addWidget(self.grades_table)
        tab.setLayout(layout)

        self.tabs.addTab(tab, "Оценки")

        # Подключаем события
        self.btn_add_grade.clicked.connect(self.add_grade)
        self.btn_edit_grade.clicked.connect(self.edit_grade)
        self.btn_delete_grade.clicked.connect(self.delete_grade)

        self.load_grades()

    def load_students_for_grades(self):
        self.grade_student_filter.clear()
        self.grade_student_filter.addItem("Все ученики", None)

        students = self.db.execute("""
                                   SELECT student_id,
                                          CONCAT(last_name, ' ', first_name, ' ', COALESCE(middle_name, '')) as full_name
                                   FROM students
                                   ORDER BY last_name, first_name
                                   """)

        for student_id, full_name in students:
            self.grade_student_filter.addItem(full_name, student_id)

    def load_subjects_for_grades(self):
        self.grade_subject_filter.clear()
        self.grade_subject_filter.addItem("Все предметы", None)

        subjects = self.db.execute("SELECT subject_id, subject_name FROM subjects ORDER BY subject_name")

        for subject_id, subject_name in subjects:
            self.grade_subject_filter.addItem(subject_name, subject_id)

    def load_dates_for_grades(self):
        self.grade_date_filter.clear()
        self.grade_date_filter.addItem("Все даты", None)

        # Получаем уникальные месяцы и годы из оценок
        dates = self.db.execute("""
                                SELECT DISTINCT TO_CHAR(grade_date, 'YYYY-MM')  as year_month,
                                                TO_CHAR(grade_date, 'Mon YYYY') as display_date
                                FROM grades
                                ORDER BY year_month DESC
                                """)

        for year_month, display_date in dates:
            self.grade_date_filter.addItem(display_date, year_month)

        # Добавляем опции для периодов
        self.grade_date_filter.addItem("─" * 20, "separator1")  # Разделитель
        self.grade_date_filter.addItem("Последние 30 дней", "last_30_days")
        self.grade_date_filter.addItem("Текущий месяц", "current_month")
        self.grade_date_filter.addItem("Прошлый месяц", "last_month")
        self.grade_date_filter.addItem("Текущий учебный год", "current_year")

    def reset_grade_filters(self):
        """Сброс всех фильтров"""
        self.grade_search.clear()
        self.grade_student_filter.setCurrentIndex(0)
        self.grade_date_filter.setCurrentIndex(0)
        self.grade_subject_filter.setCurrentIndex(0)
        self.load_grades()

    def load_grades(self):
        search_text = self.grade_search.text()
        student_id = self.grade_student_filter.currentData()
        subject_id = self.grade_subject_filter.currentData()
        date_filter = self.grade_date_filter.currentData()

        query = """
                SELECT g.grade_id,
                       CONCAT(s.last_name, ' ', s.first_name, ' ', COALESCE(s.middle_name, '')) as student_name,
                       sub.subject_name,
                       g.grade,
                       g.grade_date,
                       g.grade_type,
                       g.comment
                FROM grades g
                         JOIN students s ON g.student_id = s.student_id
                         JOIN subjects sub ON g.subject_id = sub.subject_id
                WHERE 1 = 1 \
                """
        params = []

        # Общий поиск по всем текстовым полям
        if search_text:
            query += """ AND (
                CONCAT(s.last_name, ' ', s.first_name, ' ', COALESCE(s.middle_name, '')) ILIKE %s OR
                sub.subject_name ILIKE %s OR
                g.grade::text ILIKE %s OR
                g.grade_type ILIKE %s OR
                g.comment ILIKE %s OR
                TO_CHAR(g.grade_date, 'DD.MM.YYYY') ILIKE %s
            )"""
            search_param = f"%{search_text}%"
            params.extend([search_param] * 6)

        # Фильтр по ученику
        if student_id:
            query += " AND g.student_id = %s"
            params.append(student_id)

        # Фильтр по предмету
        if subject_id:
            query += " AND g.subject_id = %s"
            params.append(subject_id)

        # Фильтр по дате
        if date_filter and date_filter not in ["separator1"]:
            if date_filter == "last_30_days":
                query += " AND g.grade_date >= CURRENT_DATE - INTERVAL '30 days'"
            elif date_filter == "current_month":
                query += " AND EXTRACT(YEAR FROM g.grade_date) = EXTRACT(YEAR FROM CURRENT_DATE) AND EXTRACT(MONTH FROM g.grade_date) = EXTRACT(MONTH FROM CURRENT_DATE)"
            elif date_filter == "last_month":
                query += """ AND g.grade_date >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month') 
                            AND g.grade_date < DATE_TRUNC('month', CURRENT_DATE)"""
            elif date_filter == "current_year":
                query += """ AND g.grade_date >= CASE 
                                WHEN EXTRACT(MONTH FROM CURRENT_DATE) >= 9 
                                THEN DATE_TRUNC('year', CURRENT_DATE) + INTERVAL '8 months'
                                ELSE DATE_TRUNC('year', CURRENT_DATE) - INTERVAL '4 months'
                            END
                            AND g.grade_date <= CASE 
                                WHEN EXTRACT(MONTH FROM CURRENT_DATE) >= 9 
                                THEN DATE_TRUNC('year', CURRENT_DATE) + INTERVAL '1 year' + INTERVAL '4 months'
                                ELSE DATE_TRUNC('year', CURRENT_DATE) + INTERVAL '4 months'
                            END"""
            elif len(date_filter) == 7 and '-' in date_filter:  # Формат YYYY-MM
                year, month = date_filter.split('-')
                query += " AND EXTRACT(YEAR FROM g.grade_date) = %s AND EXTRACT(MONTH FROM g.grade_date) = %s"
                params.extend([int(year), int(month)])

        query += " ORDER BY g.grade_date DESC, s.last_name, s.first_name"

        try:
            data = self.db.execute(query, params)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при загрузке оценок:\n{str(e)}")
            data = []

        self.grades_table.setRowCount(len(data))
        for row_idx, row in enumerate(data):
            # Пропускаем grade_id при отображении
            for col_idx in range(1, len(row)):
                value = row[col_idx]
                if col_idx == 4 and value:  # Дата
                    value = value.strftime("%d.%m.%Y")
                item = QTableWidgetItem(str(value) if value else "")
                item.setData(Qt.UserRole, row[0])  # Сохраняем ID
                self.grades_table.setItem(row_idx, col_idx - 1, item)



    def add_grade(self):
        dialog = GradeDialog(self.db)
        if dialog.exec_() == QDialog.Accepted:
            self.load_grades()

    def edit_grade(self):
        current_row = self.grades_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Выберите оценку для редактирования")
            return

        grade_id = self.grades_table.item(current_row, 0).data(Qt.UserRole)
        dialog = GradeDialog(self.db, grade_id)
        if dialog.exec_() == QDialog.Accepted:
            self.load_grades()

    def delete_grade(self):
        current_row = self.grades_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Выберите оценку для удаления")
            return

        grade_id = self.grades_table.item(current_row, 0).data(Qt.UserRole)

        reply = QMessageBox.question(self, "Подтверждение",
                                     "Вы уверены, что хотите удалить эту оценку?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                self.db.execute("DELETE FROM grades WHERE grade_id = %s", (grade_id,), fetch=False)
                self.load_grades()
                QMessageBox.information(self, "Успех", "Оценка удалена")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить оценку:\n{str(e)}")




    def init_progress_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Фильтры
        filter_layout = QVBoxLayout()

        # Первая строка - общий поиск
        search_layout = QHBoxLayout()
        self.progress_search = QLineEdit()
        self.progress_search.setPlaceholderText("Поиск по всем параметрам (ученик, предмет, период, год, оценка)...")
        self.progress_search.textChanged.connect(self.load_progress)
        search_layout.addWidget(QLabel("Поиск:"))
        search_layout.addWidget(self.progress_search)

        # Вторая строка - специфичные фильтры
        specific_filters_layout = QHBoxLayout()

        # Фильтр по ученику
        self.progress_student_filter = QComboBox()
        self.load_students_for_progress()
        self.progress_student_filter.currentIndexChanged.connect(self.load_progress)

        # Фильтр по периоду
        self.progress_period_filter = QComboBox()
        self.progress_period_filter.addItem("Все периоды", None)
        self.progress_period_filter.addItem("четверть", "четверть")
        self.progress_period_filter.addItem("полугодие", "полугодие")
        self.progress_period_filter.addItem("год", "год")
        self.progress_period_filter.currentIndexChanged.connect(self.load_progress)

        # Фильтр по учебному году
        self.progress_year_filter = QComboBox()
        self.load_years_for_progress()
        self.progress_year_filter.currentIndexChanged.connect(self.load_progress)

        # Фильтр по предмету
        self.progress_subject_filter = QComboBox()
        self.load_subjects_for_progress()
        self.progress_subject_filter.currentIndexChanged.connect(self.load_progress)

        specific_filters_layout.addWidget(QLabel("Ученик:"))
        specific_filters_layout.addWidget(self.progress_student_filter)
        specific_filters_layout.addWidget(QLabel("Период:"))
        specific_filters_layout.addWidget(self.progress_period_filter)
        specific_filters_layout.addWidget(QLabel("Учебный год:"))
        specific_filters_layout.addWidget(self.progress_year_filter)
        specific_filters_layout.addWidget(QLabel("Предмет:"))
        specific_filters_layout.addWidget(self.progress_subject_filter)

        # Кнопка сброса фильтров
        self.btn_reset_progress_filters = QPushButton("Сбросить фильтры")
        self.btn_reset_progress_filters.clicked.connect(self.reset_progress_filters)
        specific_filters_layout.addWidget(self.btn_reset_progress_filters)

        filter_layout.addLayout(search_layout)
        filter_layout.addLayout(specific_filters_layout)

        # Таблица
        self.progress_table = QTableWidget()
        self.progress_table.setColumnCount(7)
        self.progress_table.setHorizontalHeaderLabels([
            "Ученик", "Предмет", "Период", "Номер периода", "Учебный год", "Средний балл", "Итоговая оценка"
        ])
        self.progress_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addLayout(filter_layout)
        layout.addWidget(self.progress_table)
        tab.setLayout(layout)

        self.tabs.addTab(tab, "Итоговые оценки")

        self.load_progress()

    def load_students_for_progress(self):
        self.progress_student_filter.clear()
        self.progress_student_filter.addItem("Все ученики", None)

        students = self.db.execute("""
                                   SELECT student_id,
                                          CONCAT(last_name, ' ', first_name, ' ', COALESCE(middle_name, '')) as full_name
                                   FROM students
                                   ORDER BY last_name, first_name
                                   """)

        for student_id, full_name in students:
            self.progress_student_filter.addItem(full_name, student_id)

    def load_subjects_for_progress(self):
        self.progress_subject_filter.clear()
        self.progress_subject_filter.addItem("Все предметы", None)

        subjects = self.db.execute("""
                                   SELECT DISTINCT s.subject_id, s.subject_name
                                   FROM subjects s
                                            JOIN student_progress sp ON s.subject_id = sp.subject_id
                                   ORDER BY s.subject_name
                                   """)

        for subject_id, subject_name in subjects:
            self.progress_subject_filter.addItem(subject_name, subject_id)

    def load_years_for_progress(self):
        self.progress_year_filter.clear()
        self.progress_year_filter.addItem("Все годы", None)

        years = self.db.execute("""
                                SELECT DISTINCT academic_year
                                FROM student_progress
                                ORDER BY academic_year DESC
                                """)

        for year_tuple in years:
            year = year_tuple[0]
            if year:
                self.progress_year_filter.addItem(year, year)

    def reset_progress_filters(self):
        """Сброс всех фильтров"""
        self.progress_search.clear()
        self.progress_student_filter.setCurrentIndex(0)
        self.progress_period_filter.setCurrentIndex(0)
        self.progress_year_filter.setCurrentIndex(0)
        self.progress_subject_filter.setCurrentIndex(0)
        self.load_progress()

    def load_progress(self):
        search_text = self.progress_search.text()
        student_id = self.progress_student_filter.currentData()
        period_type = self.progress_period_filter.currentData()
        academic_year = self.progress_year_filter.currentData()
        subject_id = self.progress_subject_filter.currentData()

        query = """
                SELECT sp.progress_id,
                       CONCAT(s.last_name, ' ', s.first_name, ' ', COALESCE(s.middle_name, '')) as student_name,
                       sub.subject_name,
                       sp.period_type,
                       sp.period_number,
                       sp.academic_year,
                       sp.average_grade,
                       sp.final_grade
                FROM student_progress sp
                         JOIN students s ON sp.student_id = s.student_id
                         JOIN subjects sub ON sp.subject_id = sub.subject_id
                WHERE 1 = 1 \
                """
        params = []

        # Общий поиск по всем текстовым полям
        if search_text:
            query += """ AND (
                CONCAT(s.last_name, ' ', s.first_name, ' ', COALESCE(s.middle_name, '')) ILIKE %s OR
                sub.subject_name ILIKE %s OR
                sp.period_type ILIKE %s OR
                sp.period_number::text ILIKE %s OR
                sp.academic_year ILIKE %s OR
                sp.average_grade::text ILIKE %s OR
                sp.final_grade::text ILIKE %s
            )"""
            search_param = f"%{search_text}%"
            params.extend([search_param] * 7)

        # Фильтр по ученику
        if student_id:
            query += " AND sp.student_id = %s"
            params.append(student_id)

        # Фильтр по типу периода
        if period_type:
            query += " AND sp.period_type = %s"
            params.append(period_type)

        # Фильтр по учебному году
        if academic_year:
            query += " AND sp.academic_year = %s"
            params.append(academic_year)

        # Фильтр по предмету
        if subject_id:
            query += " AND sp.subject_id = %s"
            params.append(subject_id)

        query += """ ORDER BY 
            s.last_name, 
            s.first_name, 
            sp.academic_year DESC, 
            CASE sp.period_type 
                WHEN 'год' THEN 1
                WHEN 'полугодие' THEN 2 
                WHEN 'четверть' THEN 3
            END,
            sp.period_number,
            sub.subject_name
        """

        try:
            data = self.db.execute(query, params)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при загрузке итоговых оценок:\n{str(e)}")
            data = []

        self.progress_table.setRowCount(len(data))
        for row_idx, row in enumerate(data):
            # Пропускаем progress_id при отображении
            for col_idx in range(1, len(row)):
                value = row[col_idx]
                # Форматируем номер периода
                if col_idx == 4 and value is None:
                    value = "—"
                # Форматируем средний балл
                elif col_idx == 6 and value is not None:
                    value = f"{value:.2f}"

                item = QTableWidgetItem(str(value) if value is not None else "")
                item.setData(Qt.UserRole, row[0])  # Сохраняем progress_id
                self.progress_table.setItem(row_idx, col_idx - 1, item)





    def init_reports_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        # Кнопки отчетов в три ряда
        reports_layout = QVBoxLayout()

        # ПЕРВЫЙ ряд кнопок - ДЕТАЛЬНЫЕ ОТЧЕТЫ
        row1_layout = QHBoxLayout()
        self.btn_students_report = QPushButton("📚 Детальный отчет об учениках")
        self.btn_teachers_report = QPushButton("👨‍🏫 Детальный отчет об учителях")
        self.btn_subjects_report = QPushButton("📖 Детальный отчет о предметах")

        # Уменьшаем высоту кнопок
        for btn in [self.btn_students_report, self.btn_teachers_report, self.btn_subjects_report]:
            btn.setMaximumHeight(35)

        row1_layout.addWidget(self.btn_students_report)
        row1_layout.addWidget(self.btn_teachers_report)
        row1_layout.addWidget(self.btn_subjects_report)

        # ВТОРОЙ ряд кнопок - РАСПИСАНИЕ И УСПЕВАЕМОСТЬ
        row2_layout = QHBoxLayout()
        self.btn_schedule_report = QPushButton("🕐 Отчет о расписании")
        self.btn_student_progress_new = QPushButton("📊 Детальный отчет об успеваемости")
        self.btn_detailed_schedule_report = QPushButton("📋 Детальное расписание класса")

        for btn in [self.btn_schedule_report, self.btn_student_progress_new, self.btn_detailed_schedule_report]:
            btn.setMaximumHeight(35)

        row2_layout.addWidget(self.btn_schedule_report)
        row2_layout.addWidget(self.btn_student_progress_new)
        row2_layout.addWidget(self.btn_detailed_schedule_report)

        # ТРЕТИЙ ряд кнопок - БАЗОВЫЕ ОТЧЕТЫ
        row3_layout = QHBoxLayout()
        self.btn_simple_student_progress = QPushButton("📈 Базовый отчет успеваемости")
        self.btn_simple_class_summary = QPushButton("🏫 Базовая сводка по классам")
        self.btn_simple_teacher_workload = QPushButton("⚖️ Базовая нагрузка учителей")

        # Делаем базовые отчеты немного другого цвета для различия
        base_style = """
            QPushButton {
                background-color: #A0845C;
                color: #FFFFFF;
                border: 1px solid #5E3023;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                min-width: 80px;
                max-height: 35px;
            }
            QPushButton:hover {
                background-color: #C8A882;
            }
            QPushButton:pressed {
                background-color: #5E3023;
            }
        """

        for btn in [self.btn_simple_student_progress, self.btn_simple_class_summary, self.btn_simple_teacher_workload]:
            btn.setMaximumHeight(35)
            btn.setStyleSheet(base_style)

        row3_layout.addWidget(self.btn_simple_student_progress)
        row3_layout.addWidget(self.btn_simple_class_summary)
        row3_layout.addWidget(self.btn_simple_teacher_workload)

        # Добавляем все ряды в layout
        reports_layout.addLayout(row1_layout)
        reports_layout.addLayout(row2_layout)
        reports_layout.addLayout(row3_layout)

        # Добавляем разделительную линию
        separator_label = QLabel("━" * 100)
        separator_label.setStyleSheet("color: #895737; font-weight: bold;")
        separator_label.setAlignment(Qt.AlignCenter)
        reports_layout.addWidget(separator_label)

        # Увеличенная область для отображения отчетов
        self.report_area = QScrollArea()
        self.report_area.setWidgetResizable(True)
        self.report_area.setMinimumHeight(500)

        self.report_content = QLabel("Выберите отчет для просмотра")
        self.report_content.setAlignment(Qt.AlignTop)
        self.report_content.setWordWrap(True)
        self.report_content.setStyleSheet("""
            background-color: white; 
            padding: 20px; 
            border: 1px solid #C08552;
            font-size: 13px;
            line-height: 1.4;
        """)
        self.report_area.setWidget(self.report_content)

        # Изменяем пропорции: кнопки занимают минимум места, отчеты - максимум
        layout.addLayout(reports_layout, 0)  # 0 = минимальное растяжение
        layout.addWidget(self.report_area, 1)  # 1 = максимальное растяжение

        tab.setLayout(layout)
        self.tabs.addTab(tab, "Отчеты")

        # Подключаем события для ДЕТАЛЬНЫХ отчетов
        self.btn_students_report.clicked.connect(self.show_students_report)
        self.btn_teachers_report.clicked.connect(self.show_teachers_report)
        self.btn_subjects_report.clicked.connect(self.show_subjects_report)
        self.btn_schedule_report.clicked.connect(self.show_schedule_report)
        self.btn_student_progress_new.clicked.connect(self.show_student_progress_detailed_report)
        self.btn_detailed_schedule_report.clicked.connect(self.show_detailed_class_schedule_report)

        # Подключаем события для БАЗОВЫХ отчетов
        self.btn_simple_student_progress.clicked.connect(self.show_student_progress_report)
        self.btn_simple_class_summary.clicked.connect(self.show_class_summary_report)
        self.btn_simple_teacher_workload.clicked.connect(self.show_teacher_workload_report)

    # ВОССТАНАВЛИВАЕМ БАЗОВЫЕ МЕТОДЫ ОТЧЕТОВ:

    def show_student_progress_report(self):
        """Базовый отчет по успеваемости учеников"""
        try:
            query = """
                    SELECT s.last_name,
                           s.first_name,
                           c.class_number,
                           AVG(g.grade)   as avg_grade,
                           COUNT(g.grade) as total_grades
                    FROM students s
                             LEFT JOIN classes c ON s.class_id = c.class_id
                             LEFT JOIN grades g ON s.student_id = g.student_id
                    GROUP BY s.student_id, s.last_name, s.first_name, c.class_number
                    HAVING COUNT(g.grade) > 0
                    ORDER BY c.class_number, s.last_name, s.first_name
                    """
            data = self.db.execute(query)

            report_text = f"<h2>📈 Базовый отчет по успеваемости учеников</h2>"
            report_text += f"<p><strong>Дата формирования:</strong> {datetime.now().strftime('%d.%m.%Y %H:%M')}</p>"
            report_text += f"<p><strong>Показаны только ученики с оценками</strong></p><br>"

            if not data:
                report_text += "<p><em>Нет данных для отображения</em></p>"
            else:
                report_text += "<table border='1' cellpadding='8' style='border-collapse: collapse; width: 100%;'>"
                report_text += "<tr style='background-color: #895737; color: white;'>"
                report_text += "<th>№</th><th>ФИО</th><th>Класс</th><th>Средний балл</th><th>Количество оценок</th></tr>"

                for idx, row in enumerate(data, 1):
                    last_name, first_name, class_number, avg_grade, total_grades = row
                    full_name = f"{last_name} {first_name}"
                    avg_str = f"{avg_grade:.2f}" if avg_grade else "—"

                    # Цветовая индикация среднего балла
                    if avg_grade and avg_grade >= 4.5:
                        avg_color = "green"
                    elif avg_grade and avg_grade >= 3.5:
                        avg_color = "orange"
                    else:
                        avg_color = "red"

                    report_text += f"<tr>"
                    report_text += f"<td style='text-align: center;'>{idx}</td>"
                    report_text += f"<td>{full_name}</td>"
                    report_text += f"<td style='text-align: center;'>{class_number or 'Без класса'}</td>"
                    report_text += f"<td style='text-align: center; color: {avg_color}; font-weight: bold;'>{avg_str}</td>"
                    report_text += f"<td style='text-align: center;'>{total_grades or 0}</td>"
                    report_text += f"</tr>"

                report_text += "</table>"
                report_text += f"<p><strong>Всего учеников с оценками:</strong> {len(data)}</p>"

            self.report_content.setText(report_text)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать базовый отчет по успеваемости:\n{str(e)}")

    def show_class_summary_report(self):
        """Базовая сводка по классам"""
        try:
            query = """
                    SELECT c.class_number,
                           c.student_count,
                           CONCAT(t.last_name, ' ', t.first_name, ' ', COALESCE(t.middle_name, '')) as teacher_name,
                           COUNT(s.student_id)                                                      as actual_students
                    FROM classes c
                             LEFT JOIN teachers t ON c.homeroom_teacher_id = t.teacher_id
                             LEFT JOIN students s ON c.class_id = s.class_id
                    GROUP BY c.class_id, c.class_number, c.student_count, t.last_name, t.first_name, t.middle_name
                    ORDER BY c.class_number
                    """
            data = self.db.execute(query)

            report_text = f"<h2>🏫 Базовая сводка по классам</h2>"
            report_text += f"<p><strong>Дата формирования:</strong> {datetime.now().strftime('%d.%m.%Y %H:%M')}</p><br>"

            if not data:
                report_text += "<p><em>Нет классов в системе</em></p>"
            else:
                report_text += "<table border='1' cellpadding='8' style='border-collapse: collapse; width: 100%;'>"
                report_text += "<tr style='background-color: #895737; color: white;'>"
                report_text += "<th>Класс</th><th>Зарегистрировано учеников</th><th>Фактически учеников</th><th>Статус</th><th>Классный руководитель</th></tr>"

                total_registered = 0
                total_actual = 0

                for row in data:
                    class_number, registered, teacher_name, actual = row
                    total_registered += registered or 0
                    total_actual += actual or 0

                    # Определяем статус заполненности класса
                    if actual == 0:
                        status = "🔴 Пустой"
                        status_color = "red"
                    elif actual == registered:
                        status = "🟢 Полный"
                        status_color = "green"
                    elif actual < registered:
                        status = "🟡 Недобор"
                        status_color = "orange"
                    else:
                        status = "🔴 Переполнен"
                        status_color = "red"

                    report_text += f"<tr>"
                    report_text += f"<td style='text-align: center; font-weight: bold;'>{class_number}</td>"
                    report_text += f"<td style='text-align: center;'>{registered or 0}</td>"
                    report_text += f"<td style='text-align: center;'>{actual}</td>"
                    report_text += f"<td style='text-align: center; color: {status_color};'>{status}</td>"
                    report_text += f"<td>{teacher_name or '❌ Не назначен'}</td>"
                    report_text += f"</tr>"

                report_text += "</table>"

                report_text += f"<h3>📊 Общая статистика:</h3>"
                report_text += f"<p><strong>Всего классов:</strong> {len(data)}</p>"
                report_text += f"<p><strong>Всего зарегистрированных мест:</strong> {total_registered}</p>"
                report_text += f"<p><strong>Фактически учеников:</strong> {total_actual}</p>"
                report_text += f"<p><strong>Свободных мест:</strong> {max(0, total_registered - total_actual)}</p>"

            self.report_content.setText(report_text)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать базовую сводку по классам:\n{str(e)}")

    def show_teacher_workload_report(self):
        """Базовый отчет нагрузки учителей"""
        try:
            query = """
                    SELECT t.last_name,
                           t.first_name,
                           t.weekly_hours,
                           t.salary,
                           COUNT(DISTINCT s.subject_id) as subjects_count,
                           COUNT(DISTINCT c.class_id)   as homeroom_count
                    FROM teachers t
                             LEFT JOIN subjects s ON t.teacher_id = s.teacher_id
                             LEFT JOIN classes c ON t.teacher_id = c.homeroom_teacher_id
                    GROUP BY t.teacher_id, t.last_name, t.first_name, t.weekly_hours, t.salary
                    ORDER BY t.last_name, t.first_name
                    """
            data = self.db.execute(query)

            report_text = f"<h2>⚖️ Базовый отчет нагрузки учителей</h2>"
            report_text += f"<p><strong>Дата формирования:</strong> {datetime.now().strftime('%d.%m.%Y %H:%M')}</p><br>"

            if not data:
                report_text += "<p><em>Нет учителей в системе</em></p>"
            else:
                report_text += "<table border='1' cellpadding='8' style='border-collapse: collapse; width: 100%;'>"
                report_text += "<tr style='background-color: #895737; color: white;'>"
                report_text += "<th>№</th><th>ФИО</th><th>Недельные часы</th><th>Зарплата</th><th>Предметов</th><th>Классное руководство</th></tr>"

                total_hours = 0
                total_salary = 0

                for idx, row in enumerate(data, 1):
                    last_name, first_name, weekly_hours, salary, subjects_count, homeroom_count = row
                    full_name = f"{last_name} {first_name}"

                    if weekly_hours:
                        total_hours += weekly_hours
                    if salary:
                        total_salary += salary

                    hours_str = f"{weekly_hours} ч/нед" if weekly_hours else "❌ Не указаны"
                    salary_str = f"{salary:,} руб." if salary else "❌ Не указана"
                    homeroom_str = "✅ Да" if homeroom_count > 0 else "❌ Нет"

                    report_text += f"<tr>"
                    report_text += f"<td style='text-align: center;'>{idx}</td>"
                    report_text += f"<td>{full_name}</td>"
                    report_text += f"<td style='text-align: center;'>{hours_str}</td>"
                    report_text += f"<td style='text-align: center;'>{salary_str}</td>"
                    report_text += f"<td style='text-align: center;'>{subjects_count}</td>"
                    report_text += f"<td style='text-align: center;'>{homeroom_str}</td>"
                    report_text += f"</tr>"

                report_text += "</table>"

                report_text += f"<h3>📊 Общая статистика:</h3>"
                report_text += f"<p><strong>Всего учителей:</strong> {len(data)}</p>"
                report_text += f"<p><strong>Общая недельная нагрузка:</strong> {total_hours} часов</p>"
                report_text += f"<p><strong>Общий фонд оплаты труда:</strong> {total_salary:,} руб.</p>"
                report_text += f"<p><strong>Средняя зарплата:</strong> {total_salary // len(data):,} руб.</p>" if len(
                    data) > 0 else ""

            self.report_content.setText(report_text)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать базовый отчет нагрузки учителей:\n{str(e)}")



    def show_detailed_class_schedule_report(self):
        """Детальный отчет о расписании для конкретного класса"""
        try:
            # Создаем диалог для выбора класса
            dialog = QDialog(self)
            dialog.setWindowTitle("Выбор класса для отчета о расписании")
            dialog.setFixedSize(350, 200)
            dialog.setStyleSheet(APP_STYLE)

            layout = QVBoxLayout()

            # Выбор класса
            layout.addWidget(QLabel("Выберите класс:"))
            class_combo = QComboBox()

            classes = self.db.execute("SELECT class_id, class_number FROM classes ORDER BY class_number")
            if not classes:
                QMessageBox.warning(self, "Предупреждение", "В системе нет классов")
                return

            for class_id, class_number in classes:
                class_combo.addItem(class_number, class_id)
            layout.addWidget(class_combo)

            # Кнопки
            btn_layout = QHBoxLayout()
            generate_btn = QPushButton("Сформировать отчет")
            cancel_btn = QPushButton("Отмена")
            btn_layout.addWidget(generate_btn)
            btn_layout.addWidget(cancel_btn)
            layout.addLayout(btn_layout)

            dialog.setLayout(layout)

            def generate_report():
                dialog.accept()

            def cancel_report():
                dialog.reject()

            generate_btn.clicked.connect(generate_report)
            cancel_btn.clicked.connect(cancel_report)

            if dialog.exec_() != QDialog.Accepted:
                return

            # Получаем выбранный класс
            selected_class_id = class_combo.currentData()
            selected_class_name = class_combo.currentText()

            # Получаем информацию о классе
            class_info = self.db.execute("""
                                         SELECT c.class_number,
                                                c.student_count,
                                                c.classroom                         as home_classroom,
                                                CONCAT(t.last_name, ' ', t.first_name, ' ',
                                                       COALESCE(t.middle_name, '')) as homeroom_teacher
                                         FROM classes c
                                                  LEFT JOIN teachers t ON c.homeroom_teacher_id = t.teacher_id
                                         WHERE c.class_id = %s
                                         """, (selected_class_id,))[0]

            class_number, student_count, home_classroom, homeroom_teacher = class_info

            # Получаем расписание класса
            schedule_data = self.db.execute("""
                                            SELECT l.day_of_week,
                                                   l.lesson_time,
                                                   s.subject_name,
                                                   CONCAT(t.last_name, ' ', t.first_name, ' ',
                                                          COALESCE(t.middle_name, '')) as teacher_name,
                                                   l.classroom
                                            FROM lessons l
                                                     JOIN subjects s ON l.subject_id = s.subject_id
                                                     JOIN teachers t ON l.teacher_id = t.teacher_id
                                            WHERE l.class_id = %s
                                            ORDER BY CASE l.day_of_week
                                                         WHEN 'Понедельник' THEN 1
                                                         WHEN 'Вторник' THEN 2
                                                         WHEN 'Среда' THEN 3
                                                         WHEN 'Четверг' THEN 4
                                                         WHEN 'Пятница' THEN 5
                                                         WHEN 'Суббота' THEN 6
                                                         END,
                                                     l.lesson_time
                                            """, (selected_class_id,))

            # Группируем расписание по дням недели
            schedule_by_day = {}
            for day, time, subject, teacher, classroom in schedule_data:
                if day not in schedule_by_day:
                    schedule_by_day[day] = []

                time_str = time.strftime("%H:%M") if hasattr(time, 'strftime') else str(time)
                schedule_by_day[day].append({
                    'time': time_str,
                    'subject': subject,
                    'teacher': teacher,
                    'classroom': classroom
                })

            # Подсчитываем статистику
            total_lessons = len(schedule_data)
            unique_subjects = len(set([row[2] for row in schedule_data]))
            unique_teachers = len(set([row[3] for row in schedule_data]))
            used_classrooms = len(set([row[4] for row in schedule_data if row[4]]))

            # Формируем отчет
            report_text = f"<h2>📋 Детальное расписание класса {class_number}</h2>"
            report_text += f"<p><strong>Дата формирования:</strong> {datetime.now().strftime('%d.%m.%Y %H:%M')}</p>"

            # Информация о классе
            report_text += f"<div style='background-color: #E8D5C4; padding: 15px; border-radius: 8px; margin-bottom: 20px;'>"
            report_text += f"<h3 style='margin-top: 0; color: #5E3023;'>ℹ️ Информация о классе</h3>"
            report_text += f"<p><strong>Класс:</strong> {class_number}</p>"
            report_text += f"<p><strong>Количество учеников:</strong> {student_count}</p>"
            if homeroom_teacher:
                report_text += f"<p><strong>Классный руководитель:</strong> {homeroom_teacher}</p>"
            if home_classroom:
                report_text += f"<p><strong>Домашний кабинет:</strong> {home_classroom}</p>"
            report_text += f"</div>"

            # Статистика расписания
            report_text += f"<div style='background-color: #F5F5F5; padding: 15px; border-radius: 8px; margin-bottom: 20px;'>"
            report_text += f"<h3 style='margin-top: 0; color: #5E3023;'>📊 Статистика расписания</h3>"
            report_text += f"<p><strong>Всего уроков в неделю:</strong> {total_lessons}</p>"
            report_text += f"<p><strong>Количество предметов:</strong> {unique_subjects}</p>"
            report_text += f"<p><strong>Количество учителей:</strong> {unique_teachers}</p>"
            report_text += f"<p><strong>Используемых кабинетов:</strong> {used_classrooms}</p>"
            report_text += f"</div>"

            # Расписание по дням
            if not schedule_by_day:
                report_text += "<p style='color: #888; font-style: italic;'>У этого класса нет расписания</p>"
            else:
                days_order = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']

                for day in days_order:
                    if day in schedule_by_day:
                        report_text += f"<h3 style='color: #5E3023; border-bottom: 2px solid #895737; padding-bottom: 5px;'>📅 {day}</h3>"
                        report_text += "<table border='1' cellpadding='8' style='border-collapse: collapse; width: 100%; margin-bottom: 20px;'>"
                        report_text += "<tr style='background-color: #895737; color: white;'>"
                        report_text += "<th style='width: 15%;'>Время</th><th style='width: 30%;'>Предмет</th><th style='width: 40%;'>Учитель</th><th style='width: 15%;'>Кабинет</th></tr>"

                        for lesson in schedule_by_day[day]:
                            classroom_str = lesson['classroom'] if lesson['classroom'] else '—'
                            report_text += f"<tr>"
                            report_text += f"<td style='text-align: center; font-weight: bold;'>{lesson['time']}</td>"
                            report_text += f"<td style='font-weight: bold;'>{lesson['subject']}</td>"
                            report_text += f"<td>{lesson['teacher']}</td>"
                            report_text += f"<td style='text-align: center;'>{classroom_str}</td>"
                            report_text += f"</tr>"

                        report_text += "</table>"

            # Анализ нагрузки по дням
            if schedule_by_day:
                report_text += f"<h3 style='color: #5E3023;'>📈 Анализ нагрузки по дням недели</h3>"
                report_text += "<table border='1' cellpadding='8' style='border-collapse: collapse; margin-bottom: 20px;'>"
                report_text += "<tr style='background-color: #895737; color: white;'>"
                report_text += "<th>День недели</th><th>Количество уроков</th><th>Первый урок</th><th>Последний урок</th></tr>"

                for day in days_order:
                    if day in schedule_by_day:
                        lessons_count = len(schedule_by_day[day])
                        first_lesson = schedule_by_day[day][0]['time']
                        last_lesson = schedule_by_day[day][-1]['time']

                        report_text += f"<tr>"
                        report_text += f"<td>{day}</td>"
                        report_text += f"<td style='text-align: center;'>{lessons_count}</td>"
                        report_text += f"<td style='text-align: center;'>{first_lesson}</td>"
                        report_text += f"<td style='text-align: center;'>{last_lesson}</td>"
                        report_text += f"</tr>"

                report_text += "</table>"

            self.report_content.setText(report_text)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать отчет о расписании класса:\n{str(e)}")


    def show_students_report(self):
        """Отчет об учениках"""
        try:
            # Общая статистика
            total_students = self.db.execute("SELECT COUNT(*) FROM students")[0][0]

            # По классам
            students_by_class = self.db.execute("""
                                                SELECT c.class_number, COUNT(s.student_id) as student_count
                                                FROM classes c
                                                         LEFT JOIN students s ON c.class_id = s.class_id
                                                GROUP BY c.class_id, c.class_number
                                                ORDER BY c.class_number
                                                """)

            # По полу
            gender_stats = self.db.execute("""
                                           SELECT gender, COUNT(*) as count
                                           FROM students
                                           GROUP BY gender
                                           ORDER BY gender
                                           """)

            # По возрасту
            age_stats = self.db.execute("""
                                        SELECT EXTRACT(YEAR FROM AGE(birth_date)) as age,
                                               COUNT(*) as count
                                        FROM students
                                        WHERE birth_date IS NOT NULL
                                        GROUP BY EXTRACT (YEAR FROM AGE(birth_date))
                                        ORDER BY age
                                        """)

            # Ученики без класса
            students_without_class = self.db.execute("""
                                                     SELECT COUNT(*)
                                                     FROM students
                                                     WHERE class_id IS NULL
                                                     """)[0][0]

            report_text = f"<h2>📚 Отчет об учениках</h2>"
            report_text += f"<p><strong>Дата формирования:</strong> {datetime.now().strftime('%d.%m.%Y %H:%M')}</p>"

            report_text += f"<h3>📊 Общая статистика</h3>"
            report_text += f"<p><strong>Всего учеников:</strong> {total_students}</p>"
            report_text += f"<p><strong>Учеников без класса:</strong> {students_without_class}</p>"

            report_text += f"<h3>👥 Распределение по классам</h3>"
            report_text += "<table border='1' cellpadding='8' style='border-collapse: collapse; width: 100%;'>"
            report_text += "<tr style='background-color: #895737; color: white;'><th>Класс</th><th>Количество учеников</th></tr>"
            for class_number, count in students_by_class:
                report_text += f"<tr><td>{class_number}</td><td>{count}</td></tr>"
            report_text += "</table>"

            report_text += f"<h3>⚥ Распределение по полу</h3>"
            report_text += "<table border='1' cellpadding='8' style='border-collapse: collapse;'>"
            report_text += "<tr style='background-color: #895737; color: white;'><th>Пол</th><th>Количество</th></tr>"
            for gender, count in gender_stats:
                gender_name = "Мужской" if gender == "М" else "Женский"
                report_text += f"<tr><td>{gender_name}</td><td>{count}</td></tr>"
            report_text += "</table>"

            report_text += f"<h3>🎂 Распределение по возрасту</h3>"
            report_text += "<table border='1' cellpadding='8' style='border-collapse: collapse;'>"
            report_text += "<tr style='background-color: #895737; color: white;'><th>Возраст</th><th>Количество</th></tr>"
            for age, count in age_stats:
                report_text += f"<tr><td>{int(age)} лет</td><td>{count}</td></tr>"
            report_text += "</table>"

            self.report_content.setText(report_text)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать отчет об учениках:\n{str(e)}")

    def show_teachers_report(self):
        """Отчет об учителях"""
        try:
            # Общая статистика
            total_teachers = self.db.execute("SELECT COUNT(*) FROM teachers")[0][0]

            # Количество классных руководителей
            homeroom_teachers_count = self.db.execute("""
                                                      SELECT COUNT(DISTINCT homeroom_teacher_id)
                                                      FROM classes
                                                      WHERE homeroom_teacher_id IS NOT NULL
                                                      """)[0][0]

            # Базовая статистика по учителям
            teachers_base_stats = self.db.execute("""
                                                  SELECT t.teacher_id,
                                                         CONCAT(t.last_name, ' ', t.first_name, ' ',
                                                                COALESCE(t.middle_name, '')) as full_name,
                                                         t.weekly_hours,
                                                         t.salary,
                                                         COUNT(DISTINCT s.subject_id)        as subjects_count
                                                  FROM teachers t
                                                           LEFT JOIN subjects s ON t.teacher_id = s.teacher_id
                                                  GROUP BY t.teacher_id, t.last_name, t.first_name, t.middle_name,
                                                           t.weekly_hours, t.salary
                                                  ORDER BY t.last_name, t.first_name
                                                  """)

            # Получаем информацию о классном руководстве отдельно
            homeroom_info = {}
            homeroom_data = self.db.execute("""
                                            SELECT homeroom_teacher_id, class_number
                                            FROM classes
                                            WHERE homeroom_teacher_id IS NOT NULL
                                            ORDER BY class_number
                                            """)

            for teacher_id, class_number in homeroom_data:
                if teacher_id not in homeroom_info:
                    homeroom_info[teacher_id] = []
                homeroom_info[teacher_id].append(class_number)

            # Статистика по зарплате
            salary_stats = self.db.execute("""
                                           SELECT MIN(salary) as min_salary,
                                                  MAX(salary) as max_salary,
                                                  AVG(salary) as avg_salary,
                                                  SUM(salary) as total_salary
                                           FROM teachers
                                           WHERE salary IS NOT NULL
                                           """)[0]

            # Статистика по часам
            hours_stats = self.db.execute("""
                                          SELECT MIN(weekly_hours) as min_hours,
                                                 MAX(weekly_hours) as max_hours,
                                                 AVG(weekly_hours) as avg_hours,
                                                 SUM(weekly_hours) as total_hours
                                          FROM teachers
                                          WHERE weekly_hours IS NOT NULL
                                          """)[0]

            report_text = f"<h2>👨‍🏫 Отчет об учителях</h2>"
            report_text += f"<p><strong>Дата формирования:</strong> {datetime.now().strftime('%d.%m.%Y %H:%M')}</p>"

            report_text += f"<h3>📊 Общая статистика</h3>"
            report_text += f"<p><strong>Всего учителей:</strong> {total_teachers}</p>"
            report_text += f"<p><strong>Классных руководителей:</strong> {homeroom_teachers_count}</p>"

            if salary_stats[0] is not None:
                report_text += f"<h3>💰 Статистика по зарплате</h3>"
                report_text += f"<p><strong>Минимальная зарплата:</strong> {salary_stats[0]:,} руб.</p>"
                report_text += f"<p><strong>Максимальная зарплата:</strong> {salary_stats[1]:,} руб.</p>"
                report_text += f"<p><strong>Средняя зарплата:</strong> {salary_stats[2]:,.0f} руб.</p>"
                report_text += f"<p><strong>Общий фонд оплаты труда:</strong> {salary_stats[3]:,} руб.</p>"

            if hours_stats[0] is not None:
                report_text += f"<h3>⏰ Статистика по нагрузке</h3>"
                report_text += f"<p><strong>Минимальная нагрузка:</strong> {hours_stats[0]} ч/нед</p>"
                report_text += f"<p><strong>Максимальная нагрузка:</strong> {hours_stats[1]} ч/нед</p>"
                report_text += f"<p><strong>Средняя нагрузка:</strong> {hours_stats[2]:.1f} ч/нед</p>"
                report_text += f"<p><strong>Общая нагрузка:</strong> {hours_stats[3]} ч/нед</p>"

            report_text += f"<h3>👥 Детальная информация по учителям</h3>"
            report_text += "<table border='1' cellpadding='8' style='border-collapse: collapse; width: 100%;'>"
            report_text += "<tr style='background-color: #895737; color: white;'>"
            report_text += "<th>ФИО</th><th>Недельные часы</th><th>Зарплата</th><th>Предметов</th><th>Классное руководство</th></tr>"

            for teacher_data in teachers_base_stats:
                teacher_id, full_name, weekly_hours, salary, subjects_count = teacher_data
                salary_str = f"{salary:,} руб." if salary else "Не указана"
                hours_str = f"{weekly_hours} ч/нед" if weekly_hours else "Не указаны"

                # Формируем строку для классного руководства
                if teacher_id in homeroom_info:
                    classes_list = ", ".join(homeroom_info[teacher_id])
                    homeroom_str = f"Да ({classes_list})"
                else:
                    homeroom_str = "Нет"

                report_text += f"<tr>"
                report_text += f"<td>{full_name}</td>"
                report_text += f"<td>{hours_str}</td>"
                report_text += f"<td>{salary_str}</td>"
                report_text += f"<td>{subjects_count}</td>"
                report_text += f"<td>{homeroom_str}</td>"
                report_text += f"</tr>"

            report_text += "</table>"

            self.report_content.setText(report_text)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать отчет об учителях:\n{str(e)}")

    def show_subjects_report(self):
        """Отчет о предметах"""
        try:
            # Общая статистика
            total_subjects = self.db.execute("SELECT COUNT(*) FROM subjects")[0][0]

            # Предметы с учителями и без
            subjects_with_teachers = self.db.execute("""
                                                     SELECT COUNT(*)
                                                     FROM subjects
                                                     WHERE teacher_id IS NOT NULL
                                                     """)[0][0]

            subjects_without_teachers = total_subjects - subjects_with_teachers

            # Детальная информация о предметах
            subjects_detail = self.db.execute("""
                                              SELECT s.subject_name,
                                                     CONCAT(t.last_name, ' ', t.first_name, ' ',
                                                            COALESCE(t.middle_name, '')) as teacher_name,
                                                     s.weekly_hours,
                                                     COUNT(DISTINCT l.lesson_id)         as lessons_count,
                                                     COUNT(DISTINCT g.student_id)        as students_with_grades
                                              FROM subjects s
                                                       LEFT JOIN teachers t ON s.teacher_id = t.teacher_id
                                                       LEFT JOIN lessons l ON s.subject_id = l.subject_id
                                                       LEFT JOIN grades g ON s.subject_id = g.subject_id
                                              GROUP BY s.subject_id, s.subject_name, t.last_name, t.first_name,
                                                       t.middle_name, s.weekly_hours
                                              ORDER BY s.subject_name
                                              """)

            # Статистика по часам
            hours_stats = self.db.execute("""
                                          SELECT MIN(weekly_hours) as min_hours,
                                                 MAX(weekly_hours) as max_hours,
                                                 AVG(weekly_hours) as avg_hours,
                                                 SUM(weekly_hours) as total_hours
                                          FROM subjects
                                          WHERE weekly_hours IS NOT NULL
                                          """)[0]

            report_text = f"<h2>📖 Отчет о предметах</h2>"
            report_text += f"<p><strong>Дата формирования:</strong> {datetime.now().strftime('%d.%m.%Y %H:%M')}</p>"

            report_text += f"<h3>📊 Общая статистика</h3>"
            report_text += f"<p><strong>Всего предметов:</strong> {total_subjects}</p>"
            report_text += f"<p><strong>Предметов с назначенными учителями:</strong> {subjects_with_teachers}</p>"
            report_text += f"<p><strong>Предметов без учителей:</strong> {subjects_without_teachers}</p>"

            if hours_stats[0]:
                report_text += f"<h3>⏰ Статистика по недельным часам</h3>"
                report_text += f"<p><strong>Минимальная нагрузка предмета:</strong> {hours_stats[0]} ч/нед</p>"
                report_text += f"<p><strong>Максимальная нагрузка предмета:</strong> {hours_stats[1]} ч/нед</p>"
                report_text += f"<p><strong>Средняя нагрузка предмета:</strong> {hours_stats[2]:.1f} ч/нед</p>"
                report_text += f"<p><strong>Общая недельная нагрузка:</strong> {hours_stats[3]} ч/нед</p>"

            report_text += f"<h3>📚 Детальная информация по предметам</h3>"
            report_text += "<table border='1' cellpadding='8' style='border-collapse: collapse; width: 100%;'>"
            report_text += "<tr style='background-color: #895737; color: white;'>"
            report_text += "<th>Предмет</th><th>Учитель</th><th>Недельные часы</th><th>Уроков в расписании</th><th>Учеников с оценками</th></tr>"

            for subject_data in subjects_detail:
                subject_name, teacher_name, weekly_hours, lessons_count, students_with_grades = subject_data
                teacher_str = teacher_name if teacher_name else "Не назначен"
                hours_str = f"{weekly_hours} ч/нед" if weekly_hours else "Не указаны"

                report_text += f"<tr>"
                report_text += f"<td>{subject_name}</td>"
                report_text += f"<td>{teacher_str}</td>"
                report_text += f"<td>{hours_str}</td>"
                report_text += f"<td>{lessons_count}</td>"
                report_text += f"<td>{students_with_grades}</td>"
                report_text += f"</tr>"

            report_text += "</table>"

            self.report_content.setText(report_text)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать отчет о предметах:\n{str(e)}")

    def show_schedule_report(self):
        """Отчет о расписании"""
        try:
            # Общая статистика
            total_lessons = self.db.execute("SELECT COUNT(*) FROM lessons")[0][0]

            # Статистика по дням недели
            lessons_by_day = self.db.execute("""
                                             SELECT day_of_week,
                                                    COUNT(*) as lessons_count
                                             FROM lessons
                                             GROUP BY day_of_week
                                             ORDER BY CASE day_of_week
                                                          WHEN 'Понедельник' THEN 1
                                                          WHEN 'Вторник' THEN 2
                                                          WHEN 'Среда' THEN 3
                                                          WHEN 'Четверг' THEN 4
                                                          WHEN 'Пятница' THEN 5
                                                          WHEN 'Суббота' THEN 6
                                                          END
                                             """)

            # Статистика по времени
            lessons_by_time = self.db.execute("""
                                              SELECT lesson_time,
                                                     COUNT(*) as lessons_count
                                              FROM lessons
                                              GROUP BY lesson_time
                                              ORDER BY lesson_time
                                              """)

            # Использование кабинетов
            classroom_usage = self.db.execute("""
                                              SELECT classroom,
                                                     COUNT(*) as usage_count
                                              FROM lessons
                                              WHERE classroom IS NOT NULL
                                              GROUP BY classroom
                                              ORDER BY usage_count DESC
                                              """)

            # Нагрузка учителей по расписанию
            teacher_schedule_load = self.db.execute("""
                                                    SELECT CONCAT(t.last_name, ' ', t.first_name, ' ',
                                                                  COALESCE(t.middle_name, '')) as teacher_name,
                                                           COUNT(l.lesson_id)                  as lessons_per_week
                                                    FROM teachers t
                                                             LEFT JOIN lessons l ON t.teacher_id = l.teacher_id
                                                    GROUP BY t.teacher_id, t.last_name, t.first_name, t.middle_name
                                                    HAVING COUNT(l.lesson_id) > 0
                                                    ORDER BY lessons_per_week DESC
                                                    """)

            report_text = f"<h2>🕐 Отчет о расписании</h2>"
            report_text += f"<p><strong>Дата формирования:</strong> {datetime.now().strftime('%d.%m.%Y %H:%M')}</p>"

            report_text += f"<h3>📊 Общая статистика</h3>"
            report_text += f"<p><strong>Всего уроков в неделю:</strong> {total_lessons}</p>"

            report_text += f"<h3>📅 Распределение по дням недели</h3>"
            report_text += "<table border='1' cellpadding='8' style='border-collapse: collapse;'>"
            report_text += "<tr style='background-color: #895737; color: white;'><th>День недели</th><th>Количество уроков</th></tr>"
            for day, count in lessons_by_day:
                report_text += f"<tr><td>{day}</td><td>{count}</td></tr>"
            report_text += "</table>"

            report_text += f"<h3>⏰ Распределение по времени</h3>"
            report_text += "<table border='1' cellpadding='8' style='border-collapse: collapse;'>"
            report_text += "<tr style='background-color: #895737; color: white;'><th>Время урока</th><th>Количество уроков</th></tr>"
            for time, count in lessons_by_time:
                time_str = time.strftime("%H:%M") if hasattr(time, 'strftime') else str(time)
                report_text += f"<tr><td>{time_str}</td><td>{count}</td></tr>"
            report_text += "</table>"

            report_text += f"<h3>🏫 Использование кабинетов</h3>"
            report_text += "<table border='1' cellpadding='8' style='border-collapse: collapse;'>"
            report_text += "<tr style='background-color: #895737; color: white;'><th>Кабинет</th><th>Занятость (уроков в неделю)</th></tr>"
            for classroom, usage in classroom_usage[:10]:  # Топ 10 самых загруженных
                report_text += f"<tr><td>Кабинет {classroom}</td><td>{usage}</td></tr>"
            report_text += "</table>"

            report_text += f"<h3>👨‍🏫 Нагрузка учителей по расписанию</h3>"
            report_text += "<table border='1' cellpadding='8' style='border-collapse: collapse; width: 100%;'>"
            report_text += "<tr style='background-color: #895737; color: white;'><th>Учитель</th><th>Уроков в неделю</th></tr>"
            for teacher_name, lessons_count in teacher_schedule_load:
                report_text += f"<tr><td>{teacher_name}</td><td>{lessons_count}</td></tr>"
            report_text += "</table>"

            self.report_content.setText(report_text)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать отчет о расписании:\n{str(e)}")

    def show_student_progress_detailed_report(self):
        """Детальный отчет об успеваемости учеников как в электронном дневнике"""
        try:
            # Создаем диалог для выбора параметров отчета
            dialog = QDialog(self)
            dialog.setWindowTitle("Параметры отчета об успеваемости")
            dialog.setFixedSize(450, 350)
            dialog.setStyleSheet(APP_STYLE)

            layout = QVBoxLayout()

            # Выбор класса
            layout.addWidget(QLabel("Выберите класс:"))
            class_combo = QComboBox()
            class_combo.addItem("Все классы", None)

            classes = self.db.execute("SELECT class_id, class_number FROM classes ORDER BY class_number")
            for class_id, class_number in classes:
                class_combo.addItem(class_number, class_id)
            layout.addWidget(class_combo)

            # Выбор ученика
            layout.addWidget(QLabel("Выберите ученика (опционально):"))
            student_combo = QComboBox()
            student_combo.addItem("Все ученики", None)
            layout.addWidget(student_combo)

            # Функция для обновления списка учеников при изменении класса
            def update_students_list():
                student_combo.clear()
                student_combo.addItem("Все ученики", None)

                selected_class_id = class_combo.currentData()
                if selected_class_id:
                    # Загружаем учеников только выбранного класса
                    students = self.db.execute("""
                                               SELECT student_id,
                                                      CONCAT(last_name, ' ', first_name, ' ', COALESCE(middle_name, '')) as full_name
                                               FROM students
                                               WHERE class_id = %s
                                               ORDER BY last_name, first_name
                                               """, (selected_class_id,))
                else:
                    # Загружаем всех учеников
                    students = self.db.execute("""
                                               SELECT student_id,
                                                      CONCAT(last_name, ' ', first_name, ' ', COALESCE(middle_name, '')) as full_name
                                               FROM students
                                               ORDER BY last_name, first_name
                                               """)

                for student_id, full_name in students:
                    student_combo.addItem(full_name, student_id)

            # Подключаем обновление списка учеников к изменению класса
            class_combo.currentIndexChanged.connect(update_students_list)

            # Загружаем начальный список учеников
            update_students_list()

            # Выбор учебного года
            layout.addWidget(QLabel("Выберите учебный год:"))
            year_combo = QComboBox()
            year_combo.addItem("Текущий учебный год", "current")

            years = self.db.execute(
                "SELECT DISTINCT academic_year FROM student_progress WHERE academic_year IS NOT NULL ORDER BY academic_year DESC")
            for year_tuple in years:
                year = year_tuple[0]
                if year:
                    year_combo.addItem(year, year)
            layout.addWidget(year_combo)

            # Опция: показать только учеников с оценками
            layout.addWidget(QLabel("Дополнительные опции:"))
            only_with_grades_check = QCheckBox("Показать только учеников с оценками")
            only_with_grades_check.setChecked(True)  # По умолчанию включено
            layout.addWidget(only_with_grades_check)

            # Кнопки
            btn_layout = QHBoxLayout()
            generate_btn = QPushButton("Сформировать отчет")
            cancel_btn = QPushButton("Отмена")
            btn_layout.addWidget(generate_btn)
            btn_layout.addWidget(cancel_btn)
            layout.addLayout(btn_layout)

            dialog.setLayout(layout)

            def generate_report():
                dialog.accept()

            def cancel_report():
                dialog.reject()

            generate_btn.clicked.connect(generate_report)
            cancel_btn.clicked.connect(cancel_report)

            if dialog.exec_() != QDialog.Accepted:
                return

            # Получаем выбранные параметры
            selected_class_id = class_combo.currentData()
            selected_student_id = student_combo.currentData()
            selected_year = year_combo.currentData()
            only_with_grades = only_with_grades_check.isChecked()

            # Формируем запрос для получения оценок напрямую
            query = """
                    SELECT s.student_id, \
                           CONCAT(s.last_name, ' ', s.first_name, ' ', COALESCE(s.middle_name, '')) as student_name, \
                           c.class_number, \
                           sub.subject_name, \
                           g.grade, \
                           g.grade_date
                    FROM students s
                             LEFT JOIN classes c ON s.class_id = c.class_id \
                    """

            # Добавляем JOIN с grades только если нужны ученики с оценками
            if only_with_grades:
                query += " INNER JOIN grades g ON s.student_id = g.student_id"
            else:
                query += " LEFT JOIN grades g ON s.student_id = g.student_id"

            query += " LEFT JOIN subjects sub ON g.subject_id = sub.subject_id WHERE 1=1"

            params = []

            # Фильтр по классу
            if selected_class_id:
                query += " AND s.class_id = %s"
                params.append(selected_class_id)

            # Фильтр по ученику
            if selected_student_id:
                query += " AND s.student_id = %s"
                params.append(selected_student_id)

            # Фильтр по учебному году
            if selected_year == "current":
                query += """ AND (g.grade_date IS NULL OR g.grade_date >= CASE 
                            WHEN EXTRACT(MONTH FROM CURRENT_DATE) >= 9 
                            THEN DATE_TRUNC('year', CURRENT_DATE) + INTERVAL '8 months'
                            ELSE DATE_TRUNC('year', CURRENT_DATE) - INTERVAL '4 months'
                        END
                        AND g.grade_date <= CASE 
                            WHEN EXTRACT(MONTH FROM CURRENT_DATE) >= 9 
                            THEN DATE_TRUNC('year', CURRENT_DATE) + INTERVAL '1 year' + INTERVAL '4 months'
                            ELSE DATE_TRUNC('year', CURRENT_DATE) + INTERVAL '4 months'
                        END)"""
            elif selected_year and selected_year != "current":
                start_year = selected_year.split('-')[0]
                end_year = selected_year.split('-')[1]
                query += f" AND (g.grade_date IS NULL OR (g.grade_date >= '{start_year}-09-01' AND g.grade_date <= '{end_year}-05-31'))"

            query += " ORDER BY s.last_name, s.first_name, sub.subject_name, g.grade_date"

            # Выполняем запрос
            data = self.db.execute(query, params)

            # Группируем данные по ученикам и предметам
            student_data = {}
            for row in data:
                student_id, student_name, class_number, subject_name, grade, grade_date = row

                # Добавляем ученика в словарь, если его еще нет
                if student_id not in student_data:
                    student_data[student_id] = {
                        'name': student_name,
                        'class': class_number or 'Без класса',
                        'subjects': {}
                    }

                # Добавляем оценку, если она есть
                if subject_name and grade:
                    if subject_name not in student_data[student_id]['subjects']:
                        student_data[student_id]['subjects'][subject_name] = []
                    student_data[student_id]['subjects'][subject_name].append(grade)

            # Формируем отчет
            report_text = f"<h2>📊 Детальный отчет об успеваемости учеников</h2>"
            report_text += f"<p><strong>Дата формирования:</strong> {datetime.now().strftime('%d.%m.%Y %H:%M')}</p>"

            # Добавляем информацию о выбранных фильтрах
            if selected_class_id:
                class_name = class_combo.currentText()
                report_text += f"<p><strong>Класс:</strong> {class_name}</p>"
            if selected_student_id:
                student_name = student_combo.currentText()
                report_text += f"<p><strong>Ученик:</strong> {student_name}</p>"

            year_name = year_combo.currentText()
            report_text += f"<p><strong>Учебный год:</strong> {year_name}</p>"

            if only_with_grades:
                report_text += f"<p><strong>Показаны только ученики с оценками</strong></p>"

            students_count = len(student_data)
            report_text += f"<p><strong>Найдено учеников:</strong> {students_count}</p><hr>"

            if not student_data:
                report_text += "<p><strong>По выбранным критериям данные не найдены.</strong></p>"
            else:
                for student_id, student_info in student_data.items():
                    report_text += f"<div style='margin-bottom: 30px; padding: 15px; border: 2px solid #895737; border-radius: 8px;'>"
                    report_text += f"<h3 style='color: #5E3023; margin-top: 0;'>👤 {student_info['name']} ({student_info['class']})</h3>"

                    if student_info['subjects']:
                        report_text += "<table border='1' cellpadding='8' style='border-collapse: collapse; width: 100%; margin-top: 10px;'>"
                        report_text += "<tr style='background-color: #895737; color: white;'>"
                        report_text += "<th style='width: 25%;'>Предмет</th><th style='width: 55%;'>Оценки</th><th style='width: 20%;'>Средний балл</th></tr>"

                        total_avg = 0
                        subject_count = 0

                        # Сортируем предметы по названию для красивого отображения
                        sorted_subjects = sorted(student_info['subjects'].items())

                        for subject_name, grades in sorted_subjects:
                            if grades:  # Только если есть оценки
                                grades_str = ' '.join(map(str, grades))
                                avg_grade = sum(grades) / len(grades)
                                total_avg += avg_grade
                                subject_count += 1

                                # Цвет для среднего балла
                                if avg_grade >= 4.5:
                                    avg_color = "green"
                                elif avg_grade >= 3.5:
                                    avg_color = "orange"
                                else:
                                    avg_color = "red"

                                report_text += f"<tr>"
                                report_text += f"<td><strong>{subject_name}</strong></td>"
                                report_text += f"<td style='font-family: monospace; letter-spacing: 2px;'>{grades_str}</td>"
                                report_text += f"<td style='color: {avg_color}; font-weight: bold; text-align: center;'>{avg_grade:.1f}</td>"
                                report_text += f"</tr>"

                        # Общий средний балл Ученика
                        if subject_count > 0:
                            overall_avg = total_avg / subject_count
                            if overall_avg >= 4.5:
                                overall_color = "green"
                            elif overall_avg >= 3.5:
                                overall_color = "orange"
                            else:
                                overall_color = "red"

                            report_text += f"<tr style='background-color: #E8D5C4; font-weight: bold;'>"
                            report_text += f"<td>ОБЩИЙ СРЕДНИЙ БАЛЛ</td>"
                            report_text += f"<td style='text-align: center;'>—</td>"
                            report_text += f"<td style='color: {overall_color}; text-align: center; font-size: 16px;'>{overall_avg:.1f}</td>"
                            report_text += f"</tr>"

                        report_text += "</table>"
                    else:
                        report_text += "<p style='color: #888; font-style: italic;'>Оценок не найдено</p>"

                    report_text += "</div>"

            self.report_content.setText(report_text)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать отчет об успеваемости:\n{str(e)}")
            import traceback
            print("Подробная ошибка:", traceback.format_exc())



    def export_table_to_csv(self, table, file_path):
        with open(file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

            # Заголовки
            headers = []
            for col in range(table.columnCount()):
                headers.append(table.horizontalHeaderItem(col).text())
            writer.writerow(headers)

            # Данные
            for row in range(table.rowCount()):
                row_data = []
                for col in range(table.columnCount()):
                    item = table.item(row, col)
                    text = item.text() if item else ""
                    # Очищаем от лишних символов и переносов строк
                    text = text.replace('\n', ' ').replace('\r', ' ').strip()
                    row_data.append(text)
                writer.writerow(row_data)

    def export_current_tab_to_csv(self):
        current_index = self.tabs.currentIndex()
        tab_name = self.tabs.tabText(current_index)

        table = None
        search_input = None

        # Определяем таблицу и поле поиска по индексу вкладки
        if current_index == 0:  # Ученики
            table = self.students_table
            search_input = self.student_search
        elif current_index == 1:  # Учителя
            table = self.teachers_table
            search_input = self.teacher_search
        elif current_index == 2:  # Классы
            table = self.classes_table
            search_input = self.class_search
        elif current_index == 3:  # Предметы
            table = self.subjects_table
            search_input = self.subject_search
        elif current_index == 4:  # Оценки
            table = self.grades_table
            search_input = None  # У оценок нет простого поля поиска
        elif current_index == 5:  # Итоговые оценки
            table = self.progress_table
            search_input = None
        elif current_index == 6:  # Отчеты
            QMessageBox.information(self, "Информация", "Экспорт отчетов не поддерживается")
            return

        if not table:
            QMessageBox.warning(self, "Ошибка", "Не удалось определить таблицу для экспорта")
            return

        try:
            search_text = ""
            if search_input and hasattr(search_input, 'text'):
                search_text = search_input.text()

            # Создаем безопасное имя файла
            safe_tab_name = tab_name.replace(" ", "_").replace("/", "_")
            default_name = f"{safe_tab_name}_{search_text if search_text else 'all'}.csv"
            # Убираем недопустимые символы из имени файла
            default_name = "".join(c for c in default_name if c.isalnum() or c in "._-")

            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Сохранить CSV",
                os.path.expanduser(f"~/{default_name}"),
                "CSV Files (*.csv)"
            )

            if not file_path:
                return

            self.export_table_to_csv(table, file_path)

            QMessageBox.information(
                self,
                "Экспорт завершен",
                f"Данные успешно экспортированы в CSV:\n{file_path}"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка экспорта CSV",
                f"Произошла ошибка при экспорте в CSV:\n{str(e)}"
            )



    def export_current_tab_to_pdf(self):
        current_index = self.tabs.currentIndex()
        tab_name = self.tabs.tabText(current_index)

        # ПРОВЕРЯЕМ, ЕСЛИ ЭТО ВКЛАДКА ОТЧЕТОВ - ИСПРАВЛЕНО!
        if tab_name == "Отчеты":  # Используем название вкладки вместо индекса
            self.export_report_to_pdf()
            return

        table = None
        search_input = None

        # Определяем таблицу и поле поиска по названию вкладки
        if tab_name == "Ученики":
            table = self.students_table
            search_input = self.student_search
        elif tab_name == "Учителя":
            table = self.teachers_table
            search_input = self.teacher_search
        elif tab_name == "Классы":
            table = self.classes_table
            search_input = self.class_search
        elif tab_name == "Предметы":
            table = self.subjects_table
            search_input = self.subject_search
        elif tab_name == "Расписание":
            table = self.lessons_table
            search_input = None
        elif tab_name == "Оценки":
            table = self.grades_table
            search_input = None
        elif tab_name == "Итоговые оценки":
            table = self.progress_table
            search_input = None

        if not table:
            QMessageBox.warning(self, "Ошибка", f"Экспорт вкладки '{tab_name}' не поддерживается")
            return

        try:
            search_text = ""
            if search_input and hasattr(search_input, 'text'):
                search_text = search_input.text()

            # Создаем безопасное имя файла
            safe_tab_name = tab_name.replace(" ", "_").replace("/", "_")
            default_name = f"{safe_tab_name}_{search_text if search_text else 'all'}.pdf"
            # Убираем недопустимые символы из имени файла
            default_name = "".join(c for c in default_name if c.isalnum() or c in "._-")

            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Сохранить PDF",
                os.path.expanduser(f"~/{default_name}"),
                "PDF Files (*.pdf)"
            )

            if not file_path:
                return

            # Проверяем доступность модулей для PDF
            try:
                from PyQt5.QtPrintSupport import QPrinter
                from PyQt5.QtGui import QTextDocument, QTextCursor, QTextTableFormat, QFont
            except ImportError as e:
                QMessageBox.critical(
                    self,
                    "Ошибка импорта",
                    f"Не удается импортировать модули для создания PDF:\n{str(e)}\n\n"
                    "Установите полную версию PyQt5 с поддержкой принтера:\n"
                    "pip install PyQt5[all]"
                )
                return

            # Создаем принтер
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(file_path)

            # Устанавливаем размер страницы и отступы
            printer.setPageSize(QPrinter.A4)
            printer.setPageMargins(20, 20, 20, 20, QPrinter.Millimeter)

            # Создаем документ
            doc = QTextDocument()
            cursor = QTextCursor(doc)

            # Заголовок документа
            title_format = cursor.charFormat()
            title_font = QFont("Arial", 16, QFont.Bold)
            title_format.setFont(title_font)
            cursor.setCharFormat(title_format)
            cursor.insertText(f"Отчет: {tab_name}\n")

            if search_text:
                cursor.insertText(f"Фильтр: {search_text}\n")

            cursor.insertText(f"Дата создания: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n")

            # Проверяем, есть ли данные в таблице
            if table.rowCount() == 0:
                cursor.insertText("Нет данных для отображения")
            else:
                # Сброс форматирования для таблицы
                normal_format = cursor.charFormat()
                normal_font = QFont("Arial", 9)
                normal_format.setFont(normal_font)
                cursor.setCharFormat(normal_format)

                # Создание таблицы
                table_format = QTextTableFormat()
                table_format.setBorder(1)
                table_format.setBorderStyle(1)
                table_format.setCellPadding(3)
                table_format.setHeaderRowCount(1)

                pdf_table = cursor.insertTable(
                    table.rowCount() + 1,
                    table.columnCount(),
                    table_format
                )

                # Заголовки таблицы
                header_format = cursor.charFormat()
                header_font = QFont("Arial", 9, QFont.Bold)
                header_format.setFont(header_font)

                for col in range(table.columnCount()):
                    cell_cursor = pdf_table.cellAt(0, col).firstCursorPosition()
                    cell_cursor.setCharFormat(header_format)
                    header_item = table.horizontalHeaderItem(col)
                    header_text = header_item.text() if header_item else f"Колонка {col + 1}"
                    cell_cursor.insertText(header_text)

                # Данные таблицы
                for row in range(table.rowCount()):
                    for col in range(table.columnCount()):
                        cell_cursor = pdf_table.cellAt(row + 1, col).firstCursorPosition()
                        cell_cursor.setCharFormat(normal_format)
                        item = table.item(row, col)
                        text = item.text() if item else ""

                        # Ограничиваем длину текста для красивого отображения
                        if len(text) > 25:
                            text = text[:22] + "..."

                        cell_cursor.insertText(text)

            # Печать в PDF
            doc.print_(printer)

            QMessageBox.information(
                self,
                "Экспорт завершен",
                f"PDF документ успешно создан:\n{file_path}"
            )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка экспорта PDF",
                f"Произошла ошибка при экспорте в PDF:\n{str(e)}\n\n"
                f"Тип ошибки: {type(e).__name__}"
            )
            import traceback
            print("Подробная ошибка:", traceback.format_exc())

    def export_report_to_pdf(self):
        """Специальный метод для экспорта отчетов в PDF - ИСПРАВЛЕНА ОШИБКА QSize"""
        try:
            # Проверяем, есть ли контент для экспорта
            report_text = self.report_content.text()

            if not report_text or report_text == "Выберите отчет для просмотра":
                QMessageBox.warning(
                    self,
                    "Нет данных",
                    "Сначала сформируйте отчет, затем экспортируйте его в PDF"
                )
                return

            # Получаем заголовок отчета из текста
            lines = report_text.split('\n')
            report_title = "Отчет"
            for line in lines:
                if line.strip() and not line.startswith('<'):
                    report_title = line.strip()
                    break

            # Диалог сохранения файла
            default_filename = f"{report_title.replace(' ', '_').replace(':', '')}.pdf"
            default_filename = "".join(c for c in default_filename if c.isalnum() or c in "._-")

            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Сохранить отчет в PDF",
                os.path.expanduser(f"~/{default_filename}"),
                "PDF Files (*.pdf)"
            )

            if not file_path:
                return

            # Проверяем доступность модулей для PDF
            try:
                from PyQt5.QtPrintSupport import QPrinter
                from PyQt5.QtGui import QTextDocument
                from PyQt5.QtCore import QSizeF  # ДОБАВЛЯЕМ ИМПОРТ QSizeF
            except ImportError as e:
                QMessageBox.critical(
                    self,
                    "Ошибка импорта",
                    f"Не удается импортировать модули для создания PDF:\n{str(e)}\n\n"
                    "Установите полную версию PyQt5 с поддержкой принтера:\n"
                    "pip install PyQt5[all]"
                )
                return

            # Создаем принтер
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(file_path)
            printer.setPageSize(QPrinter.A4)  # ИСПРАВЛЕНО: используем константу QPrinter.A4
            printer.setPageMargins(15, 15, 15, 15, QPrinter.Millimeter)

            # Создаем HTML документ с улучшенным стилем
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{
                        font-family: 'Times New Roman', serif;
                        font-size: 11pt;
                        line-height: 1.4;
                        margin: 0;
                        padding: 20px;
                        color: #333;
                    }}
                    h1, h2, h3 {{
                        color: #5E3023;
                        margin-top: 20px;
                        margin-bottom: 10px;
                    }}
                    h1 {{ font-size: 18pt; border-bottom: 2px solid #895737; padding-bottom: 5px; }}
                    h2 {{ font-size: 14pt; }}
                    h3 {{ font-size: 12pt; }}
                    table {{
                        border-collapse: collapse;
                        width: 100%;
                        margin: 10px 0;
                        font-size: 10pt;
                    }}
                    th, td {{
                        border: 1px solid #C08552;
                        padding: 6px;
                        text-align: left;
                    }}
                    th {{
                        background-color: #895737;
                        color: white;
                        font-weight: bold;
                    }}
                    tr:nth-child(even) {{
                        background-color: #F9F9F9;
                    }}
                    .highlight {{
                        background-color: #E8D5C4;
                        padding: 10px;
                        border-radius: 5px;
                        margin: 10px 0;
                    }}
                    p {{
                        margin: 8px 0;
                    }}
                    .footer {{
                        margin-top: 30px;
                        font-size: 9pt;
                        color: #666;
                        text-align: center;
                        border-top: 1px solid #CCC;
                        padding-top: 10px;
                    }}
                </style>
            </head>
            <body>
                {report_text}
                <div class="footer">
                    Документ сформирован автоматически системой управления школой
                </div>
            </body>
            </html>
            """

            # Создаем и настраиваем документ
            doc = QTextDocument()
            doc.setHtml(html_content)

            # ИСПРАВЛЕНО: Правильная установка размера страницы
            page_size = printer.pageRect(QPrinter.Point).size()  # Получаем размер в пойнтах
            doc.setPageSize(QSizeF(page_size))  # Конвертируем в QSizeF

            # Печатаем в PDF
            doc.print_(printer)

            QMessageBox.information(
                self,
                "Экспорт завершен",
                f"Отчет успешно экспортирован в PDF:\n{file_path}"
            )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка экспорта PDF",
                f"Произошла ошибка при экспорте отчета в PDF:\n{str(e)}"
            )
            import traceback
            print("Подробная ошибка:", traceback.format_exc())

    def logout(self):
        reply = QMessageBox.question(self, "Выход",
                                    "Вы уверены, что хотите выйти из системы?",
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.hide()
            self.login_window = LoginWindow()
            self.login_window.show()


# Диалоги для добавления/редактирования записей

class StudentDialog(QDialog):
    def __init__(self, db, student_id=None):
        super().__init__()
        self.db = db
        self.student_id = student_id
        self.setWindowTitle("Добавить ученика" if not student_id else "Редактировать ученика")
        self.setFixedSize(550, 450)
        self.setStyleSheet(APP_STYLE)

        layout = QVBoxLayout()

        # Поля ввода
        self.last_name_edit = QLineEdit()
        self.first_name_edit = QLineEdit()
        self.middle_name_edit = QLineEdit()

        self.birth_date_edit = QDateEdit()
        self.birth_date_edit.setCalendarPopup(True)
        self.birth_date_edit.setDate(QDate.currentDate())

        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["М", "Ж"])

        self.class_combo = QComboBox()
        self.load_classes()

        # Добавляем поля в форму
        layout.addWidget(QLabel("Фамилия:"))
        layout.addWidget(self.last_name_edit)
        layout.addWidget(QLabel("Имя:"))
        layout.addWidget(self.first_name_edit)
        layout.addWidget(QLabel("Отчество:"))
        layout.addWidget(self.middle_name_edit)
        layout.addWidget(QLabel("Дата рождения:"))
        layout.addWidget(self.birth_date_edit)
        layout.addWidget(QLabel("Пол:"))
        layout.addWidget(self.gender_combo)
        layout.addWidget(QLabel("Класс:"))
        layout.addWidget(self.class_combo)

        # Кнопки
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Сохранить")
        self.cancel_btn = QPushButton("Отмена")

        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # События
        self.save_btn.clicked.connect(self.save)
        self.cancel_btn.clicked.connect(self.reject)

        # Загружаем данные для редактирования
        if self.student_id:
            self.load_student_data()

    def load_classes(self):
        self.class_combo.addItem("Без класса", None)
        classes = self.db.execute("SELECT class_id, class_number FROM classes ORDER BY class_number")
        for class_id, class_number in classes:
            self.class_combo.addItem(class_number, class_id)

    def load_student_data(self):
        data = self.db.execute(
            "SELECT last_name, first_name, middle_name, birth_date, gender, class_id FROM students WHERE student_id = %s",
            (self.student_id,)
        )[0]

        self.last_name_edit.setText(data[0] or "")
        self.first_name_edit.setText(data[1] or "")
        self.middle_name_edit.setText(data[2] or "")

        if data[3]:
            self.birth_date_edit.setDate(QDate.fromString(data[3].strftime("%Y-%m-%d"), "yyyy-MM-dd"))

        self.gender_combo.setCurrentText(data[4] or "М")

        # Устанавливаем класс
        for i in range(self.class_combo.count()):
            if self.class_combo.itemData(i) == data[5]:
                self.class_combo.setCurrentIndex(i)
                break

    def save(self):
        # Валидация
        if not self.last_name_edit.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите фамилию")
            return
        if not self.first_name_edit.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите имя")
            return

        try:
            if self.student_id:
                # Обновление
                self.db.execute("""
                                UPDATE students
                                SET last_name=%s,
                                    first_name=%s,
                                    middle_name=%s,
                                    birth_date=%s,
                                    gender=%s,
                                    class_id=%s
                                WHERE student_id = %s
                                """, (
                                    self.last_name_edit.text().strip(),
                                    self.first_name_edit.text().strip(),
                                    self.middle_name_edit.text().strip() or None,
                                    self.birth_date_edit.date().toPyDate(),
                                    self.gender_combo.currentText(),
                                    self.class_combo.currentData(),
                                    self.student_id
                                ), fetch=False)
            else:
                # Добавление
                self.db.execute("""
                                INSERT INTO students (last_name, first_name, middle_name, birth_date, gender, class_id)
                                VALUES (%s, %s, %s, %s, %s, %s)
                                """, (
                                    self.last_name_edit.text().strip(),
                                    self.first_name_edit.text().strip(),
                                    self.middle_name_edit.text().strip() or None,
                                    self.birth_date_edit.date().toPyDate(),
                                    self.gender_combo.currentText(),
                                    self.class_combo.currentData()
                                ), fetch=False)

            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить ученика:\n{str(e)}")


class TeacherDialog(QDialog):
    def __init__(self, db, teacher_id=None):
        super().__init__()
        self.db = db
        self.teacher_id = teacher_id
        self.setWindowTitle("Добавить учителя" if not teacher_id else "Редактировать учителя")
        self.setFixedSize(500, 400)
        self.setStyleSheet(APP_STYLE)

        layout = QVBoxLayout()

        # Поля ввода
        self.last_name_edit = QLineEdit()
        self.first_name_edit = QLineEdit()
        self.middle_name_edit = QLineEdit()
        self.salary_edit = QLineEdit()
        self.weekly_hours_edit = QLineEdit()

        # Добавляем поля в форму
        layout.addWidget(QLabel("Фамилия:"))
        layout.addWidget(self.last_name_edit)
        layout.addWidget(QLabel("Имя:"))
        layout.addWidget(self.first_name_edit)
        layout.addWidget(QLabel("Отчество:"))
        layout.addWidget(self.middle_name_edit)
        layout.addWidget(QLabel("Зарплата:"))
        layout.addWidget(self.salary_edit)
        layout.addWidget(QLabel("Недельные часы:"))
        layout.addWidget(self.weekly_hours_edit)

        # Кнопки
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Сохранить")
        self.cancel_btn = QPushButton("Отмена")

        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # События
        self.save_btn.clicked.connect(self.save)
        self.cancel_btn.clicked.connect(self.reject)

        # Загружаем данные для редактирования
        if self.teacher_id:
            self.load_teacher_data()

    def load_teacher_data(self):
        data = self.db.execute(
            "SELECT last_name, first_name, middle_name, salary, weekly_hours FROM teachers WHERE teacher_id = %s",
            (self.teacher_id,)
        )[0]

        self.last_name_edit.setText(data[0] or "")
        self.first_name_edit.setText(data[1] or "")
        self.middle_name_edit.setText(data[2] or "")
        self.salary_edit.setText(str(data[3]) if data[3] else "")
        self.weekly_hours_edit.setText(str(data[4]) if data[4] else "")

    def save(self):
        # Валидация
        if not self.last_name_edit.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите фамилию")
            return
        if not self.first_name_edit.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите имя")
            return

        try:
            salary = int(self.salary_edit.text()) if self.salary_edit.text().strip() else None
            weekly_hours = int(self.weekly_hours_edit.text()) if self.weekly_hours_edit.text().strip() else None
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Зарплата и часы должны быть числами")
            return

        try:
            if self.teacher_id:
                # Обновление
                self.db.execute("""
                                UPDATE teachers
                                SET last_name=%s,
                                    first_name=%s,
                                    middle_name=%s,
                                    salary=%s,
                                    weekly_hours=%s
                                WHERE teacher_id = %s
                                """, (
                                    self.last_name_edit.text().strip(),
                                    self.first_name_edit.text().strip(),
                                    self.middle_name_edit.text().strip() or None,
                                    salary,
                                    weekly_hours,
                                    self.teacher_id
                                ), fetch=False)
            else:
                # Добавление
                self.db.execute("""
                                INSERT INTO teachers (last_name, first_name, middle_name, salary, weekly_hours)
                                VALUES (%s, %s, %s, %s, %s)
                                """, (
                                    self.last_name_edit.text().strip(),
                                    self.first_name_edit.text().strip(),
                                    self.middle_name_edit.text().strip() or None,
                                    salary,
                                    weekly_hours
                                ), fetch=False)

            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить учителя:\n{str(e)}")


class ClassDialog(QDialog):
    def __init__(self, db, class_id=None):
        super().__init__()
        self.db = db
        self.class_id = class_id
        self.setWindowTitle("Добавить класс" if not class_id else "Редактировать класс")
        self.setFixedSize(400, 250)
        self.setStyleSheet(APP_STYLE)

        layout = QVBoxLayout()

        # Поля ввода
        self.class_number_edit = QLineEdit()
        self.classroom_edit = QLineEdit()

        self.teacher_combo = QComboBox()
        self.load_teachers()

        # Добавляем поля в форму
        layout.addWidget(QLabel("Номер класса:"))
        layout.addWidget(self.class_number_edit)
        layout.addWidget(QLabel("Кабинет:"))
        layout.addWidget(self.classroom_edit)
        layout.addWidget(QLabel("Классный руководитель:"))
        layout.addWidget(self.teacher_combo)

        # Кнопки
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Сохранить")
        self.cancel_btn = QPushButton("Отмена")

        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # События
        self.save_btn.clicked.connect(self.save)
        self.cancel_btn.clicked.connect(self.reject)

        # Загружаем данные для редактирования
        if self.class_id:
            self.load_class_data()

    def load_teachers(self):
        self.teacher_combo.addItem("Без руководителя", None)
        teachers = self.db.execute("""
                                   SELECT teacher_id,
                                          CONCAT(last_name, ' ', first_name, ' ', COALESCE(middle_name, '')) as full_name
                                   FROM teachers
                                   ORDER BY last_name, first_name
                                   """)
        for teacher_id, full_name in teachers:
            self.teacher_combo.addItem(full_name, teacher_id)

    def load_class_data(self):
        data = self.db.execute(
            "SELECT class_number, classroom, homeroom_teacher_id FROM classes WHERE class_id = %s",
            (self.class_id,)
        )[0]

        self.class_number_edit.setText(data[0] or "")
        self.classroom_edit.setText(str(data[1]) if data[1] else "")

        # Устанавливаем учителя
        for i in range(self.teacher_combo.count()):
            if self.teacher_combo.itemData(i) == data[2]:
                self.teacher_combo.setCurrentIndex(i)
                break

    def save(self):
        # Валидация
        if not self.class_number_edit.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите номер класса")
            return

        try:
            classroom = int(self.classroom_edit.text()) if self.classroom_edit.text().strip() else None
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Номер кабинета должен быть числом")
            return

        try:
            if self.class_id:
                # Обновление
                self.db.execute("""
                                UPDATE classes
                                SET class_number=%s,
                                    classroom=%s,
                                    homeroom_teacher_id=%s
                                WHERE class_id = %s
                                """, (
                                    self.class_number_edit.text().strip(),
                                    classroom,
                                    self.teacher_combo.currentData(),
                                    self.class_id
                                ), fetch=False)
            else:
                # Добавление
                self.db.execute("""
                                INSERT INTO classes (class_number, classroom, homeroom_teacher_id, student_count)
                                VALUES (%s, %s, %s, 0)
                                """, (
                                    self.class_number_edit.text().strip(),
                                    classroom,
                                    self.teacher_combo.currentData()
                                ), fetch=False)

            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить класс:\n{str(e)}")


class SubjectDialog(QDialog):
    def __init__(self, db, subject_id=None):
        super().__init__()
        self.db = db
        self.subject_id = subject_id
        self.setWindowTitle("Добавить предмет" if not subject_id else "Редактировать предмет")
        self.setFixedSize(400, 250)
        self.setStyleSheet(APP_STYLE)

        layout = QVBoxLayout()

        # Поля ввода
        self.subject_name_edit = QLineEdit()
        self.weekly_hours_edit = QLineEdit()

        self.teacher_combo = QComboBox()
        self.load_teachers()

        # Добавляем поля в форму
        layout.addWidget(QLabel("Название предмета:"))
        layout.addWidget(self.subject_name_edit)
        layout.addWidget(QLabel("Недельные часы:"))
        layout.addWidget(self.weekly_hours_edit)
        layout.addWidget(QLabel("Учитель:"))
        layout.addWidget(self.teacher_combo)

        # Кнопки
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Сохранить")
        self.cancel_btn = QPushButton("Отмена")

        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # События
        self.save_btn.clicked.connect(self.save)
        self.cancel_btn.clicked.connect(self.reject)

        # Загружаем данные для редактирования
        if self.subject_id:
            self.load_subject_data()

    def load_teachers(self):
        self.teacher_combo.addItem("Без учителя", None)
        teachers = self.db.execute("""
                                   SELECT teacher_id,
                                          CONCAT(last_name, ' ', first_name, ' ', COALESCE(middle_name, '')) as full_name
                                   FROM teachers
                                   ORDER BY last_name, first_name
                                   """)
        for teacher_id, full_name in teachers:
            self.teacher_combo.addItem(full_name, teacher_id)

    def load_subject_data(self):
        data = self.db.execute(
            "SELECT subject_name, weekly_hours, teacher_id FROM subjects WHERE subject_id = %s",
            (self.subject_id,)
        )[0]

        self.subject_name_edit.setText(data[0] or "")
        self.weekly_hours_edit.setText(str(data[1]) if data[1] else "")

        # Устанавливаем учителя
        for i in range(self.teacher_combo.count()):
            if self.teacher_combo.itemData(i) == data[2]:
                self.teacher_combo.setCurrentIndex(i)
                break

    def save(self):
        # Валидация
        if not self.subject_name_edit.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите название предмета")
            return

        try:
            weekly_hours = int(self.weekly_hours_edit.text()) if self.weekly_hours_edit.text().strip() else None
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Недельные часы должны быть числом")
            return

        try:
            if self.subject_id:
                # Обновление
                self.db.execute("""
                                UPDATE subjects
                                SET subject_name=%s,
                                    weekly_hours=%s,
                                    teacher_id=%s
                                WHERE subject_id = %s
                                """, (
                                    self.subject_name_edit.text().strip(),
                                    weekly_hours,
                                    self.teacher_combo.currentData(),
                                    self.subject_id
                                ), fetch=False)
            else:
                # Добавление
                self.db.execute("""
                                INSERT INTO subjects (subject_name, weekly_hours, teacher_id)
                                VALUES (%s, %s, %s)
                                """, (
                                    self.subject_name_edit.text().strip(),
                                    weekly_hours,
                                    self.teacher_combo.currentData()
                                ), fetch=False)

            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить предмет:\n{str(e)}")


class LessonDialog(QDialog):
    def __init__(self, db, lesson_id=None):
        super().__init__()
        self.db = db
        self.lesson_id = lesson_id
        self.setWindowTitle("Добавить урок" if not lesson_id else "Редактировать урок")
        self.setFixedSize(450, 550)
        self.setStyleSheet(APP_STYLE)

        layout = QVBoxLayout()

        # Поля ввода
        self.class_combo = QComboBox()
        self.load_classes()

        self.subject_combo = QComboBox()
        self.load_subjects()

        self.teacher_combo = QComboBox()
        self.load_teachers()

        self.day_combo = QComboBox()
        self.day_combo.addItems([
            "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"
        ])

        from PyQt5.QtWidgets import QTimeEdit
        from PyQt5.QtCore import QTime

        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime(8, 30))  # Время по умолчанию
        self.time_edit.setDisplayFormat("HH:mm")

        self.classroom_edit = QLineEdit()

        # Добавляем поля в форму
        layout.addWidget(QLabel("Класс:"))
        layout.addWidget(self.class_combo)
        layout.addWidget(QLabel("Предмет:"))
        layout.addWidget(self.subject_combo)
        layout.addWidget(QLabel("Учитель:"))
        layout.addWidget(self.teacher_combo)
        layout.addWidget(QLabel("День недели:"))
        layout.addWidget(self.day_combo)
        layout.addWidget(QLabel("Время урока:"))
        layout.addWidget(self.time_edit)
        layout.addWidget(QLabel("Кабинет:"))
        layout.addWidget(self.classroom_edit)

        # Кнопки
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Сохранить")
        self.cancel_btn = QPushButton("Отмена")

        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # События
        self.save_btn.clicked.connect(self.save)
        self.cancel_btn.clicked.connect(self.reject)

        # Загружаем данные для редактирования
        if self.lesson_id:
            self.load_lesson_data()

    def load_classes(self):
        classes = self.db.execute("""
                                  SELECT class_id, class_number
                                  FROM classes
                                  ORDER BY class_number
                                  """)
        for class_id, class_number in classes:
            self.class_combo.addItem(class_number, class_id)

    def load_subjects(self):
        subjects = self.db.execute("""
                                   SELECT subject_id, subject_name
                                   FROM subjects
                                   ORDER BY subject_name
                                   """)
        for subject_id, subject_name in subjects:
            self.subject_combo.addItem(subject_name, subject_id)

    def load_teachers(self):
        teachers = self.db.execute("""
                                   SELECT teacher_id,
                                          CONCAT(last_name, ' ', first_name, ' ', COALESCE(middle_name, '')) as full_name
                                   FROM teachers
                                   ORDER BY last_name, first_name
                                   """)
        for teacher_id, full_name in teachers:
            self.teacher_combo.addItem(full_name, teacher_id)

    def load_lesson_data(self):
        data = self.db.execute("""
                               SELECT class_id, subject_id, teacher_id, day_of_week, lesson_time, classroom
                               FROM lessons
                               WHERE lesson_id = %s
                               """, (self.lesson_id,))[0]

        # Устанавливаем класс
        for i in range(self.class_combo.count()):
            if self.class_combo.itemData(i) == data[0]:
                self.class_combo.setCurrentIndex(i)
                break

        # Устанавливаем предмет
        for i in range(self.subject_combo.count()):
            if self.subject_combo.itemData(i) == data[1]:
                self.subject_combo.setCurrentIndex(i)
                break

        # Устанавливаем учителя
        for i in range(self.teacher_combo.count()):
            if self.teacher_combo.itemData(i) == data[2]:
                self.teacher_combo.setCurrentIndex(i)
                break

        # Устанавливаем день недели
        if data[3]:
            index = self.day_combo.findText(data[3])
            if index >= 0:
                self.day_combo.setCurrentIndex(index)

        # Устанавливаем время
        if data[4]:
            if hasattr(data[4], 'hour'):  # timedelta object
                hours = data[4].hour
                minutes = data[4].minute
                self.time_edit.setTime(QTime(hours, minutes))
            else:  # string
                time_str = str(data[4])
                if ':' in time_str:
                    hours, minutes = map(int, time_str.split(':')[:2])
                    self.time_edit.setTime(QTime(hours, minutes))

        # Устанавливаем кабинет
        self.classroom_edit.setText(str(data[5]) if data[5] else "")

    def save(self):
        # Валидация
        if self.class_combo.currentData() is None:
            QMessageBox.warning(self, "Ошибка", "Выберите класс")
            return
        if self.subject_combo.currentData() is None:
            QMessageBox.warning(self, "Ошибка", "Выберите предмет")
            return
        if self.teacher_combo.currentData() is None:
            QMessageBox.warning(self, "Ошибка", "Выберите учителя")
            return

        # Проверяем конфликты в расписании
        time_str = self.time_edit.time().toString("HH:mm:ss")

        conflict_query = """
                         SELECT 1 \
                         FROM lessons
                         WHERE class_id = %s
                           AND day_of_week = %s
                           AND lesson_time = %s \
                         """
        conflict_params = [
            self.class_combo.currentData(),
            self.day_combo.currentText(),
            time_str
        ]

        if self.lesson_id:
            conflict_query += " AND lesson_id != %s"
            conflict_params.append(self.lesson_id)

        conflict = self.db.execute(conflict_query, conflict_params)

        if conflict:
            QMessageBox.warning(
                self,
                "Конфликт расписания",
                f"У класса {self.class_combo.currentText()} уже есть урок "
                f"в {self.day_combo.currentText()} в {self.time_edit.time().toString('HH:mm')}"
            )
            return

        try:
            classroom = int(self.classroom_edit.text()) if self.classroom_edit.text().strip() else None
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Номер кабинета должен быть числом")
            return

        try:
            if self.lesson_id:
                # Обновление
                self.db.execute("""
                                UPDATE lessons
                                SET class_id=%s,
                                    subject_id=%s,
                                    teacher_id=%s,
                                    day_of_week=%s,
                                    lesson_time=%s,
                                    classroom=%s
                                WHERE lesson_id = %s
                                """, (
                                    self.class_combo.currentData(),
                                    self.subject_combo.currentData(),
                                    self.teacher_combo.currentData(),
                                    self.day_combo.currentText(),
                                    time_str,
                                    classroom,
                                    self.lesson_id
                                ), fetch=False)
            else:
                # Добавление
                self.db.execute("""
                                INSERT INTO lessons (class_id, subject_id, teacher_id, day_of_week, lesson_time, classroom)
                                VALUES (%s, %s, %s, %s, %s, %s)
                                """, (
                                    self.class_combo.currentData(),
                                    self.subject_combo.currentData(),
                                    self.teacher_combo.currentData(),
                                    self.day_combo.currentText(),
                                    time_str,
                                    classroom
                                ), fetch=False)

            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить урок:\n{str(e)}")


class GradeDialog(QDialog):
    def __init__(self, db, grade_id=None):
        super().__init__()
        self.db = db
        self.grade_id = grade_id
        self.setWindowTitle("Добавить оценку" if not grade_id else "Редактировать оценку")
        self.setFixedSize(400, 650)
        self.setStyleSheet(APP_STYLE)

        layout = QVBoxLayout()

        # Поля ввода
        self.student_combo = QComboBox()
        self.load_students()

        self.subject_combo = QComboBox()
        self.load_subjects()

        self.grade_combo = QComboBox()
        self.grade_combo.addItems(["5", "4", "3", "2"])

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())

        self.grade_type_combo = QComboBox()
        self.grade_type_combo.addItems([
            "контрольная", "самостоятельная", "устный ответ", "домашнее задание", "тест"
        ])

        self.teacher_combo = QComboBox()
        self.load_teachers()

        self.comment_edit = QLineEdit()

        # Добавляем поля в форму
        layout.addWidget(QLabel("Ученик:"))
        layout.addWidget(self.student_combo)
        layout.addWidget(QLabel("Предмет:"))
        layout.addWidget(self.subject_combo)
        layout.addWidget(QLabel("Оценка:"))
        layout.addWidget(self.grade_combo)
        layout.addWidget(QLabel("Дата:"))
        layout.addWidget(self.date_edit)
        layout.addWidget(QLabel("Тип оценки:"))
        layout.addWidget(self.grade_type_combo)
        layout.addWidget(QLabel("Учитель:"))
        layout.addWidget(self.teacher_combo)
        layout.addWidget(QLabel("Комментарий:"))
        layout.addWidget(self.comment_edit)

        # Кнопки
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Сохранить")
        self.cancel_btn = QPushButton("Отмена")

        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # События
        self.save_btn.clicked.connect(self.save)
        self.cancel_btn.clicked.connect(self.reject)

        # Загружаем данные для редактирования
        if self.grade_id:
            self.load_grade_data()

    def load_students(self):
        students = self.db.execute("""
                                   SELECT student_id,
                                          CONCAT(last_name, ' ', first_name, ' ', COALESCE(middle_name, '')) as full_name
                                   FROM students
                                   ORDER BY last_name, first_name
                                   """)
        for student_id, full_name in students:
            self.student_combo.addItem(full_name, student_id)

    def load_subjects(self):
        subjects = self.db.execute("SELECT subject_id, subject_name FROM subjects ORDER BY subject_name")
        for subject_id, subject_name in subjects:
            self.subject_combo.addItem(subject_name, subject_id)

    def load_teachers(self):
        teachers = self.db.execute("""
                                   SELECT teacher_id,
                                          CONCAT(last_name, ' ', first_name, ' ', COALESCE(middle_name, '')) as full_name
                                   FROM teachers
                                   ORDER BY last_name, first_name
                                   """)
        for teacher_id, full_name in teachers:
            self.teacher_combo.addItem(full_name, teacher_id)

    def load_grade_data(self):
        data = self.db.execute("""
                               SELECT student_id, subject_id, grade, grade_date, grade_type, teacher_id, comment
                               FROM grades
                               WHERE grade_id = %s
                               """, (self.grade_id,))[0]

        # Устанавливаем Ученика
        for i in range(self.student_combo.count()):
            if self.student_combo.itemData(i) == data[0]:
                self.student_combo.setCurrentIndex(i)
                break

        # Устанавливаем предмет
        for i in range(self.subject_combo.count()):
            if self.subject_combo.itemData(i) == data[1]:
                self.subject_combo.setCurrentIndex(i)
                break

        # Устанавливаем оценку
        self.grade_combo.setCurrentText(str(data[2]))

        # Устанавливаем дату
        if data[3]:
            self.date_edit.setDate(QDate.fromString(data[3].strftime("%Y-%m-%d"), "yyyy-MM-dd"))

        # Устанавливаем тип
        if data[4]:
            self.grade_type_combo.setCurrentText(data[4])

        # Устанавливаем учителя
        for i in range(self.teacher_combo.count()):
            if self.teacher_combo.itemData(i) == data[5]:
                self.teacher_combo.setCurrentIndex(i)
                break

        # Устанавливаем комментарий
        self.comment_edit.setText(data[6] or "")

    def save(self):
        # Валидация
        if self.student_combo.currentData() is None:
            QMessageBox.warning(self, "Ошибка", "Выберите ученика")
            return
        if self.subject_combo.currentData() is None:
            QMessageBox.warning(self, "Ошибка", "Выберите предмет")
            return
        if self.teacher_combo.currentData() is None:
            QMessageBox.warning(self, "Ошибка", "Выберите учителя")
            return

        try:
            if self.grade_id:
                # Обновление
                self.db.execute("""
                                UPDATE grades
                                SET student_id=%s,
                                    subject_id=%s,
                                    grade=%s,
                                    grade_date=%s,
                                    grade_type=%s,
                                    teacher_id=%s,
                                    comment=%s
                                WHERE grade_id = %s
                                """, (
                                    self.student_combo.currentData(),
                                    self.subject_combo.currentData(),
                                    int(self.grade_combo.currentText()),
                                    self.date_edit.date().toPyDate(),
                                    self.grade_type_combo.currentText(),
                                    self.teacher_combo.currentData(),
                                    self.comment_edit.text().strip() or None,
                                    self.grade_id
                                ), fetch=False)
            else:
                # Добавление
                self.db.execute("""
                                INSERT INTO grades (student_id, subject_id, grade, grade_date, grade_type, teacher_id,
                                                    comment)
                                VALUES (%s, %s, %s, %s, %s, %s, %s)
                                """, (
                                    self.student_combo.currentData(),
                                    self.subject_combo.currentData(),
                                    int(self.grade_combo.currentText()),
                                    self.date_edit.date().toPyDate(),
                                    self.grade_type_combo.currentText(),
                                    self.teacher_combo.currentData(),
                                    self.comment_edit.text().strip() or None
                                ), fetch=False)

            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить оценку:\n{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_STYLE)

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#F3E9DC"))
    app.setPalette(palette)

    window = LoginWindow()
    window.show()

    sys.exit(app.exec_())