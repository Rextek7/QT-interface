import sys
import pymysql
from config import host, user, password, db_name
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QTabWidget, QLabel, QLineEdit, QHBoxLayout, QComboBox


class Database:
    def __init__(self):
        self.connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )

    def close(self):
        self.connection.close()


class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.resize(600, 600)

    def init_ui(self):
        self.setWindowTitle('Подбор персонала')
        self.setWindowIcon(QtGui.QIcon(r'C:\Users\Rextek\Desktop\НИПИГАЗ\177 nipigaz-logo'))

        self.logo = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap(r'C:\Users\Rextek\Desktop\НИПИГАЗ\177 nipigaz-logo')
        self.logo.setPixmap(pixmap)
        self.logo.resize(600, 500)
        self.logo.setAlignment(QtCore.Qt.AlignTop)
        # self.update_logo()

        self.label = QtWidgets.QLabel('Подбор персонала')
        self.label.setFont(QtGui.QFont('Arial', 20))
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.button1 = QtWidgets.QPushButton('Ведение вакансий')
        self.button1.clicked.connect(self.show_vacancies)

        self.button2 = QtWidgets.QPushButton('Справочники')
        self.button2.clicked.connect(self.directories)

        # Увеличение размера шрифта для кнопок
        font = self.button1.font()
        font.setPointSize(font.pointSize() + 4)
        self.button1.setFont(font)
        self.button2.setFont(font)

        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(self.label)
        v_box.addWidget(self.button1)
        v_box.addWidget(self.button2)

        # self.setStyleSheet("background-color: white;")
        # self.logo.raise_()
        # self.label.raise_()
        # self.button1.raise_()
        # self.button2.raise_()
        self.setLayout(v_box)
        self.show()

    # def update_logo(self):
    #     pixmap = QtGui.QPixmap(r'C:\Users\Rextek\Desktop\НИПИГАЗ\177 nipigaz-logo')
    #     width = self.width()
    #     hight = self.height()
    #     pixmap = pixmap.scaledToWidth(int(width))
    #     pixmap = pixmap.scaledToHeight(int(hight))
    #     self.logo.setPixmap(pixmap)

    # def resizeEvent(self, event):
    #     super().resizeEvent(event)
    #     # self.update_logo()

    def show_vacancies(self):
        self.vacancies_window = Vacancy()
        self.vacancies_window.show()

    def directories(self):
        self.directories_window = DirectoriesWindow()
        self.directories_window.show()


class Vacancy(QtWidgets.QWidget):
    button_data = []

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.resize(600, 600)

    def init_ui(self):
        self.setWindowTitle('Вакансии')

        self.label = QtWidgets.QLabel('Вакансии')
        self.label.setFont(QtGui.QFont('Arial', 20))

        self.tab_widget = QtWidgets.QTabWidget()
        self.tab_widget.addTab(self.create_table_widget('vacancy'), 'Вакансия')

        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(self.tab_widget)
        v_box.addWidget(self.label)

        self.setLayout(v_box)

    def create_table_widget(self, table_name):
        table_widget = QtWidgets.QTableWidget()
        db = Database()

        # Выполнение запроса к базе данных для получения данных
        with db.connection.cursor() as cursor:
            select_all_rows = f"SELECT * FROM `{table_name}`"
            cursor.execute(select_all_rows)
            data = cursor.fetchall()

        # Заполнение таблицы данными
        table_widget.setRowCount(len(data))
        table_widget.setColumnCount(len(data[0]) + 1)
        headers = []
        for row, row_data in enumerate(data):
            for column, (key, value) in enumerate(row_data.items()):
                if key != 'id':
                    if row == 0:
                        headers.append(key)
                    item = QtWidgets.QTableWidgetItem(str(value))
                    table_widget.setItem(row, column, item)
            # Add a button to the last column
            btn = QtWidgets.QPushButton('Open Form')
            btn.clicked.connect(lambda checked, row=row: self.open_form_with_data(row))
            table_widget.setCellWidget(row, 0, btn)

        # Set header
        headers.insert(0, 'Выбор')
        headers.append('')
        table_widget.setHorizontalHeaderLabels(headers)

        table_widget.resizeColumnsToContents()

        db.close()

        return table_widget

    def open_form_with_data(self, row):
        button_data = row + 1
        self.vacancies_window = VacanciesWindow(button_data)
        self.vacancies_window.show()


class VacanciesWindow(QtWidgets.QWidget):
    def __init__(self, button_data):

        super().__init__()
        self.setWindowTitle("Ведение вакансии")
        self.setGeometry(100, 100, 400, 300)
        self.button_data = button_data

        layout = QVBoxLayout()
        self.setLayout(layout)

        vacancies_layout = QVBoxLayout()
        layout.addLayout(vacancies_layout)

        field_labels = ["Локация", "Проект", "Подразделение 1", "Подразделение 2", "Подразделение 3", "Подразделение 4",
                        "Позиция", "Роль", "Описание",
                        "Грейд", "МВЗ", "Заказчик", "Дата начала поиска вакансии", "Дата окончания поиска вакансии",
                        "Зарплата", "Приостановка поиска", "Дата начала приостановки",
                        "Дата конца приостановки", "Кандидат", "HR", "Статус"]

        fields_layout = QHBoxLayout()
        vacancies_layout.addLayout(fields_layout)

        for i, label in enumerate(field_labels):
            field_label = QLabel(label, self)
            field_layout = QVBoxLayout()

            if i == 0:
                field_input = QComboBox(self)
                db = Database()
                # Выполнение запроса к базе данных для получения данных
                # Выполнение запроса к базе данных для получения location_id
                with db.connection.cursor() as cursor:
                    select_location_id = f"SELECT location_id FROM vacancy WHERE id = {button_data}"
                    cursor.execute(select_location_id)
                    result = cursor.fetchone()
                    location_id = result['location_id']

                # Выполнение запроса к базе данных для получения location
                with db.connection.cursor() as cursor:
                    select_location = f"SELECT location FROM location WHERE id = {location_id}"
                    cursor.execute(select_location)
                    result = cursor.fetchone()
                    location = result['location']
                    field_input.addItem(location)

                cursor.close()
                db.close()

            elif i == 1:
                field_input = QComboBox(self)
                db = Database()
                # Выполнение запроса к базе данных для получения данных
                # Выполнение запроса к базе данных для получения location_id
                with db.connection.cursor() as cursor:
                    select_ = f"SELECT project_id FROM vacancy WHERE id = {button_data}"
                    cursor.execute(select_)
                    result = cursor.fetchone()
                    res = result['project_id']

                # Выполнение запроса к базе данных для получения location
                with db.connection.cursor() as cursor:
                    select = f"SELECT project_name FROM project WHERE id = {res}"
                    cursor.execute(select)
                    result = cursor.fetchone()
                    res_ = result['project_name']
                    field_input.addItem(res_)

                cursor.close()
                db.close()

            elif i == 2:
                field_input = QComboBox(self)
                db = Database()
                # Выполнение запроса к базе данных для получения данных
                with db.connection.cursor() as cursor:
                    select_ = f"SELECT division_1 FROM vacancy WHERE id = {button_data}"
                    cursor.execute(select_)
                    result = cursor.fetchone()
                    res = result['division_1']
                    field_input.addItem(res)

                cursor.close()
                db.close()

            elif i == 3:
                field_input = QComboBox(self)
                db = Database()
                # Выполнение запроса к базе данных для получения данных
                with db.connection.cursor() as cursor:
                    select_ = f"SELECT division_2 FROM vacancy WHERE id = {button_data}"
                    cursor.execute(select_)
                    result = cursor.fetchone()
                    res = result['division_2']
                    field_input.addItem(res)

                cursor.close()
                db.close()

            elif i == 4:
                field_input = QComboBox(self)
                db = Database()
                # Выполнение запроса к базе данных для получения данных
                with db.connection.cursor() as cursor:
                    select_ = f"SELECT division_3 FROM vacancy WHERE id = {button_data}"
                    cursor.execute(select_)
                    result = cursor.fetchone()
                    res = result['division_3']
                    field_input.addItem(res)

                cursor.close()
                db.close()

            elif i == 5:
                field_input = QComboBox(self)
                db = Database()
                # Выполнение запроса к базе данных для получения данных
                with db.connection.cursor() as cursor:
                    select_ = f"SELECT division_4 FROM vacancy WHERE id = {button_data}"
                    cursor.execute(select_)
                    result = cursor.fetchone()
                    res = result['division_4']
                    field_input.addItem(res)

                cursor.close()
                db.close()

            elif i == 6:
                field_input = QComboBox(self)
                db = Database()
                # Выполнение запроса к базе данных для получения данных
                with db.connection.cursor() as cursor:
                    select_ = f"SELECT position FROM vacancy WHERE id = {button_data}"
                    cursor.execute(select_)
                    result = cursor.fetchone()
                    res = result['position']
                    field_input.addItem(res)

                cursor.close()
                db.close()

            elif i == 7:
                field_input = QComboBox(self)
                db = Database()
                # Выполнение запроса к базе данных для получения данных
                # Выполнение запроса к базе данных для получения location_id
                with db.connection.cursor() as cursor:
                    select_ = f"SELECT role_id FROM vacancy WHERE id = {button_data}"
                    cursor.execute(select_)
                    result = cursor.fetchone()
                    res = result['role_id']

                # Выполнение запроса к базе данных для получения location
                with db.connection.cursor() as cursor:
                    select = f"SELECT role_name FROM `role` WHERE id = {res}"
                    cursor.execute(select)
                    result = cursor.fetchone()
                    res_ = result['role_name']
                    field_input.addItem(res_)

                cursor.close()
                db.close()

            elif i == 8:
                field_input = QComboBox(self)
                db = Database()
                # Выполнение запроса к базе данных для получения данных
                with db.connection.cursor() as cursor:
                    select_ = f"SELECT description FROM vacancy WHERE id = {button_data}"
                    cursor.execute(select_)
                    result = cursor.fetchone()
                    res = result['description']
                    field_input.addItem(res)

                cursor.close()
                db.close()

            elif i == 9:
                field_input = QComboBox(self)
                db = Database()
                # Выполнение запроса к базе данных для получения данных
                # Выполнение запроса к базе данных для получения location_id
                with db.connection.cursor() as cursor:
                    select_ = f"SELECT grade_id FROM vacancy WHERE id = {button_data}"
                    cursor.execute(select_)
                    result = cursor.fetchone()
                    res = result['grade_id']

                # Выполнение запроса к базе данных для получения location
                with db.connection.cursor() as cursor:
                    select = f"SELECT `value` FROM `grade` WHERE id = {res}"
                    cursor.execute(select)
                    result = cursor.fetchone()
                    res_ = result['value']
                    field_input.addItem(str(res_))

                cursor.close()
                db.close()

            elif i == 10:
                field_input = QComboBox(self)
                db = Database()
                # Выполнение запроса к базе данных для получения данных
                # Выполнение запроса к базе данных для получения location_id
                with db.connection.cursor() as cursor:
                    select_ = f"SELECT MVZ_id FROM vacancy WHERE id = {button_data}"
                    cursor.execute(select_)
                    result = cursor.fetchone()
                    res = result['MVZ_id']

                # Выполнение запроса к базе данных для получения location
                with db.connection.cursor() as cursor:
                    select = f"SELECT `MVZ` FROM `mvz` WHERE id = {res}"
                    cursor.execute(select)
                    result = cursor.fetchone()
                    res_ = result['MVZ']
                    field_input.addItem(res_)

                cursor.close()
                db.close()

            elif i == 11:
                field_input = QComboBox(self)
                db = Database()
                # Выполнение запроса к базе данных для получения данных
                # Выполнение запроса к базе данных для получения location_id
                with db.connection.cursor() as cursor:
                    select_ = f"SELECT customer_id FROM vacancy WHERE id = {button_data}"
                    cursor.execute(select_)
                    result = cursor.fetchone()
                    res = result['customer_id']

                # Выполнение запроса к базе данных для получения location
                with db.connection.cursor() as cursor:
                    select = f"SELECT `customer_name` FROM `customer` WHERE id = {res}"
                    cursor.execute(select)
                    result = cursor.fetchone()
                    res_ = result['customer_name']
                    field_input.addItem(res_)

                cursor.close()
                db.close()

            elif i == 12:
                field_input = QComboBox(self)
                db = Database()
                # Выполнение запроса к базе данных для получения данных
                with db.connection.cursor() as cursor:
                    select_ = f"SELECT start_date FROM vacancy WHERE id = {button_data}"
                    cursor.execute(select_)
                    result = cursor.fetchone()
                    res = result['start_date']
                    field_input.addItem(str(res))

                cursor.close()
                db.close()

            elif i == 13:
                field_input = QComboBox(self)
                db = Database()
                # Выполнение запроса к базе данных для получения данных
                with db.connection.cursor() as cursor:
                    select_ = f"SELECT finish_date FROM vacancy WHERE id = {button_data}"
                    cursor.execute(select_)
                    result = cursor.fetchone()
                    res = result['finish_date']
                    field_input.addItem(str(res))

                cursor.close()
                db.close()

            elif i == 14:
                field_input = QComboBox(self)
                db = Database()
                # Выполнение запроса к базе данных для получения данных
                with db.connection.cursor() as cursor:
                    select_ = f"SELECT salary FROM vacancy WHERE id = {button_data}"
                    cursor.execute(select_)
                    result = cursor.fetchone()
                    res = result['salary']
                    field_input.addItem(str(res))

                cursor.close()
                db.close()

            elif i == 15:
                field_input = QComboBox(self)
                db = Database()
                # Выполнение запроса к базе данных для получения данных
                with db.connection.cursor() as cursor:
                    select_ = f"SELECT pause FROM vacancy WHERE id = {button_data}"
                    cursor.execute(select_)
                    result = cursor.fetchone()
                    res = result['pause']
                    field_input.addItem(str(res))

                cursor.close()
                db.close()

            elif i == 16:
                field_input = QComboBox(self)
                db = Database()
                # Выполнение запроса к базе данных для получения данных
                with db.connection.cursor() as cursor:
                    select_ = f"SELECT pause_start FROM vacancy WHERE id = {button_data}"
                    cursor.execute(select_)
                    result = cursor.fetchone()
                    res = result['pause_start']
                    field_input.addItem(str(res))

                cursor.close()
                db.close()

            elif i == 17:
                field_input = QComboBox(self)
                db = Database()
                # Выполнение запроса к базе данных для получения данных
                with db.connection.cursor() as cursor:
                    select_ = f"SELECT pause_finish FROM vacancy WHERE id = {button_data}"
                    cursor.execute(select_)
                    result = cursor.fetchone()
                    res = result['pause_finish']
                    field_input.addItem(str(res))

                cursor.close()
                db.close()

            elif i == 18:
                field_input = QComboBox(self)
                db = Database()
                # Выполнение запроса к базе данных для получения данных
                with db.connection.cursor() as cursor:
                    select_ = f"SELECT candidate FROM vacancy WHERE id = {button_data}"
                    cursor.execute(select_)
                    result = cursor.fetchone()
                    res = result['candidate']
                    field_input.addItem(res)

                cursor.close()
                db.close()

            elif i == 19:
                field_input = QComboBox(self)
                db = Database()
                # Выполнение запроса к базе данных для получения данных
                # Выполнение запроса к базе данных для получения location_id
                with db.connection.cursor() as cursor:
                    select_ = f"SELECT HR_id FROM vacancy WHERE id = {button_data}"
                    cursor.execute(select_)
                    result = cursor.fetchone()
                    res = result['HR_id']

                # Выполнение запроса к базе данных для получения location
                with db.connection.cursor() as cursor:
                    select = f"SELECT `name` FROM `hr_` WHERE id = {res}"
                    cursor.execute(select)
                    result = cursor.fetchone()
                    res_ = result['name']
                    field_input.addItem(res_)

                cursor.close()
                db.close()

            elif i == 20:
                field_input = QComboBox(self)
                db = Database()
                # Выполнение запроса к базе данных для получения данных
                with db.connection.cursor() as cursor:
                    select_ = f"SELECT status FROM vacancy WHERE id = {button_data}"
                    cursor.execute(select_)
                    result = cursor.fetchone()
                    res = result['status']
                    field_input.addItem(res)

                cursor.close()
                db.close()

            else:
                field_input = QLineEdit(self)

            field_layout.addWidget(field_label)
            field_layout.addWidget(field_input)
            fields_layout.addLayout(field_layout)

            if (i + 1) % 6 == 0:
                fields_layout = QHBoxLayout()
                vacancies_layout.addLayout(fields_layout)

        tab_widget = QTabWidget()
        table_widget = QtWidgets.QTableWidget()
        layout.addWidget(tab_widget)


        tab_widget.addTab(self.create_table_widget('security_check', button_data), 'СЭБ')
        tab_widget.addTab(self.create_table_widget('talentq_check', button_data), 'TalentQ')
        tab_widget.addTab(self.create_table_widget('offer', button_data), 'Оффер')
        tab_widget.addTab(self.create_table_widget('rejection', button_data), 'Отказы')
        tab_widget.addTab(self.create_table_widget('candidate', button_data), 'Кандидаты')


        db = Database()
        # Выполнение запроса к базе данных для получения comment
        with db.connection.cursor() as cursor:
            select = f"SELECT * FROM `comment` WHERE vac_id = {button_data} "
            cursor.execute(select)
            data = cursor.fetchall()

        if len(data) > 0:
            # Заполнение таблицы данными
            table_widget.setRowCount(len(data))
            table_widget.setColumnCount(len(data[0]))
            headers = []
            for row, row_data in enumerate(data):
                for column, (key, value) in enumerate(row_data.items()):
                    if key != 'id':
                        if row == 0:
                            headers.append(key)
                        item = QtWidgets.QTableWidgetItem(str(value))
                        table_widget.setItem(row, column, item)
            # Set header
            headers.insert(0, '')
            table_widget.setHorizontalHeaderLabels(headers)

            table_widget.resizeColumnsToContents()

            db.close()

            table_widget.removeColumn(0)

            tab_widget.addTab(table_widget, 'Комментарии')

    def create_table_widget(self, table_name, button_data):
        table_widget = QtWidgets.QTableWidget()
        db = Database()
        self.button_data = button_data

        # Выполнение запроса к базе данных для получения данных
        with db.connection.cursor() as cursor:
            select_all_rows = f"SELECT * FROM vac_candid WHERE vacancy_id = {button_data}"
            cursor.execute(select_all_rows)
            data = cursor.fetchall()

        if len(data) > 0:
            # Получение candidate_id
            candidate_ids = [row['candidate_id'] for row in data]

            if table_name != 'candidate':
                # Выполнение запроса к базе данных для получения данных по candidate_id
                with db.connection.cursor() as cursor:
                    select_candidate_data = f"SELECT * FROM {table_name} WHERE candidate_id IN ({','.join(map(str, candidate_ids))})"
                    cursor.execute(select_candidate_data)
                    candidate_data = cursor.fetchall()
            else:
                # Выполнение запроса к базе данных для получения данных по candidate_id
                with db.connection.cursor() as cursor:
                    select_candidate_data = f"SELECT * FROM {table_name} WHERE id IN ({','.join(map(str, candidate_ids))})"
                    cursor.execute(select_candidate_data)
                    candidate_data = cursor.fetchall()

            if len(candidate_data) > 0:
                # Заполнение таблицы данными
                table_widget.setRowCount(len(candidate_data))
                table_widget.setColumnCount(len(candidate_data[0]))
                headers = []
                for row, row_data in enumerate(candidate_data):
                    for column, (key, value) in enumerate(row_data.items()):
                        if key != 'id':
                            if row == 0:
                                headers.append(key)
                            item = QtWidgets.QTableWidgetItem(str(value))
                            table_widget.setItem(row, column, item)
                # Set header
                headers.insert(0, '')
                table_widget.setHorizontalHeaderLabels(headers)

                table_widget.resizeColumnsToContents()

                db.close()

                table_widget.removeColumn(0)

                return table_widget


class DirectoriesWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.resize(600, 600)

    def init_ui(self):
        self.setWindowTitle('Справочники')

        self.label = QtWidgets.QLabel('Справочники')
        self.label.setFont(QtGui.QFont('Arial', 20))

        self.tab_widget = QtWidgets.QTabWidget()
        self.tab_widget.addTab(self.create_table_widget('customer'), 'Заказчик')
        self.tab_widget.addTab(self.create_table_widget('role'), 'Роль')
        self.tab_widget.addTab(self.create_table_widget('project'), 'Проект')
        self.tab_widget.addTab(self.create_table_widget('location'), 'Локация')
        self.tab_widget.addTab(self.create_table_widget('grade'), 'Грейд')
        self.tab_widget.addTab(self.create_table_widget('MVZ'), 'МВЗ')
        self.tab_widget.addTab(self.create_table_widget('past_work'), 'Предыдущее место работы')
        self.tab_widget.addTab(self.create_table_widget('recruit_agency'), 'Агенство по найму')
        self.tab_widget.addTab(self.create_table_widget('source'), 'Ресурс')

        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(self.tab_widget)
        v_box.addWidget(self.label)

        self.setLayout(v_box)

    def create_table_widget(self, table_name):
        table_widget = QtWidgets.QTableWidget()
        db = Database()

        # Выполнение запроса к базе данных для получения данных
        with db.connection.cursor() as cursor:
            select_all_rows = f"SELECT * FROM `{table_name}`"
            cursor.execute(select_all_rows)
            data = cursor.fetchall()

        # Заполнение таблицы данными
        table_widget.setRowCount(len(data))
        table_widget.setColumnCount(len(data[0]))
        headers = []
        for row, row_data in enumerate(data):
            for column, (key, value) in enumerate(row_data.items()):
                if key != 'id':
                    if row == 0:
                        headers.append(key)
                    item = QtWidgets.QTableWidgetItem(str(value))
                    table_widget.setItem(row, column, item)
        # Set header
        headers.insert(0, '')
        table_widget.setHorizontalHeaderLabels(headers)

        table_widget.resizeColumnsToContents()

        db.close()

        table_widget.removeColumn(0)

        return table_widget


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
