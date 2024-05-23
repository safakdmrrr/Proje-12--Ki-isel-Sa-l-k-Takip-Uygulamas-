import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QMessageBox, QLineEdit, QDialog, QInputDialog, QCheckBox, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class WelcomeDialog(QDialog):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Hoş Geldiniz")
        self.setGeometry(550, 200, 30, 30)
        self.setStyleSheet("background-color: #add8e6;")
        self.init_ui()

    def init_ui(self):
        welcome_label = QLabel()
        pixmap = QPixmap("saglik.png")
        welcome_label.setPixmap(pixmap)
        welcome_label.setAlignment(Qt.AlignCenter)

        login_button = QPushButton("Giriş yap")
        login_button.setStyleSheet("background-color: #90EE90; padding: 20px;width:200px ;border-bottom:1px solid #c67639;"
                                   "margin-top:80px;border-radius:5px;border-top:none;border-left:none;border-right:none;font-size: 24px;")
        login_button.clicked.connect(self.accept)

        vbox = QVBoxLayout()
        vbox.addWidget(welcome_label)
        vbox.addWidget(login_button)
        vbox.setAlignment(Qt.AlignCenter)

        self.setLayout(vbox)

class AddRecordDialog(QDialog):
    def __init__(self, user, record_text, exercise_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Kayıt Detayları")
        self.setGeometry(750, 250, 300, 300)
        self.init_ui(user, record_text, exercise_text)

    def init_ui(self, user, record_text, exercise_text):
        name_label = QLabel("Ad Soyad:")
        name_display = QLabel(user.name)

        age_label = QLabel("Yaş:")
        age_display = QLabel(user.age)

        gender_label = QLabel("Cinsiyet:")
        gender_display = QLabel(user.gender)

        record_label = QLabel("Sağlık Verisi:")
        record_display = QTextEdit()
        record_display.setPlainText(record_text)
        record_display.setReadOnly(True)

        exercise_label = QLabel("Egzersiz:")
        exercise_display = QTextEdit()
        exercise_display.setPlainText(exercise_text)
        exercise_display.setReadOnly(True)

        vbox = QVBoxLayout()
        vbox.addWidget(name_label)
        vbox.addWidget(name_display)
        vbox.addWidget(age_label)
        vbox.addWidget(age_display)
        vbox.addWidget(gender_label)
        vbox.addWidget(gender_display)
        vbox.addWidget(record_label)
        vbox.addWidget(record_display)
        vbox.addWidget(exercise_label)
        vbox.addWidget(exercise_display)

        self.setLayout(vbox)


class ReportInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rapor Oluştur")
        self.resize(400, 200)
        self.init_ui()

    def init_ui(self):
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Raporunuzu buraya yazın...")
        self.text_edit.setStyleSheet("background-color: white;")  # Metin düzenleyici arka plan rengi

        ok_button = QPushButton("Tamam")
        ok_button.clicked.connect(self.accept)
        ok_button.setStyleSheet("background-color: #4CAF50; color: white; border: none; padding: 10px;")

        cancel_button = QPushButton("İptal")
        cancel_button.clicked.connect(self.reject)
        cancel_button.setStyleSheet("background-color: #f44336; color: white; border: none; padding: 10px;")

        button_layout = QHBoxLayout()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.text_edit)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)


class ShowReportDialog(QDialog):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Raporları Göster")
        self.setGeometry(250, 250, 300, 300)
        self.init_ui(user)

    def init_ui(self, user):
        report_label = QLabel("Raporlar:")
        report_display = QTextEdit()
        report_display.setPlainText("\n".join(user.reports))
        report_display.setReadOnly(True)

        vbox = QVBoxLayout()
        vbox.addWidget(report_label)
        vbox.addWidget(report_display)

        self.setLayout(vbox)


class User:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
        self.health_records = []
        self.exercises = []
        self.reports = []

    def add_record(self, record):
        self.health_records.append(record)

    def add_exercise(self, exercise):
        self.exercises.append(exercise)

    def add_report(self, report):
        self.reports.append(report)


class HealthRecord:
    def __init__(self, record_text):
        self.record_text = record_text

    def parse_record(self):
        cleaned_text = self.record_text.strip()
        # Girişteki virgülü nokta virgüle çevir
        cleaned_text = cleaned_text.replace(",", ";")
        return cleaned_text


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kişisel Sağlık Takip Uygulaması")
        self.setGeometry(700, 200, 400, 400)
        self.user = None  # Kullanıcıyı başlangıçta tanımlayalım
        self.init_ui()
        self.show_welcome_dialog()

    def init_ui(self):
        self.name_label = QLabel("Ad - Soyad:")
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet("padding: 11px;border-radius: 5px; background-color: #728e8c;color:black;font-size: 16px;")

        self.age_label = QLabel("Yaş:")
        self.age_input = QLineEdit()
        self.age_input.setStyleSheet("padding: 11px; border-radius: 5px; background-color: #728e8c;font-size: 16px;")

        self.gender_label = QLabel("Cinsiyet:")
        self.female_checkbox = QCheckBox("Kadın")
        self.female_checkbox.setStyleSheet(
            "QCheckBox { font-size: 20px; } QCheckBox::indicator { width: 20px; height: 20px; }")
        self.male_checkbox = QCheckBox("Erkek")
        self.male_checkbox.setStyleSheet(
            "QCheckBox { font-size: 20px; } QCheckBox::indicator { width: 20px; height: 20px; }")

        self.record_label = QLabel("Sağlık Verisi:")
        self.record_input = QTextEdit()

        self.exercise_label = QLabel("Egzersiz Ekle:")
        self.exercise_input = QTextEdit()

        self.add_record_button = QPushButton("Kayıt Ekle")
        self.add_record_button.setStyleSheet(
            "background-color: green; padding: 10px; font-size: 16px; color: white; border: none")

        self.add_report_button = QPushButton("Rapor Oluştur")
        self.add_report_button.setStyleSheet(
            "background-color: green; padding: 10px; font-size: 16px; color: white; border: none")

        self.show_reports_button = QPushButton("Raporları Göster")
        self.show_reports_button.setStyleSheet(
            "background-color: orange; padding: 10px; font-size: 16px; color: white; font-weight: 500; border: none")

        self.add_record_button.clicked.connect(self.add_record)
        self.add_report_button.clicked.connect(self.add_report)
        self.show_reports_button.clicked.connect(self.show_reports)

        vbox = QVBoxLayout()
        vbox.addWidget(self.name_label)
        vbox.addWidget(self.name_input)
        vbox.addWidget(self.age_label)
        vbox.addWidget(self.age_input)
        vbox.addWidget(self.gender_label)
        vbox.addWidget(self.female_checkbox)
        vbox.addWidget(self.male_checkbox)
        vbox.addWidget(self.record_label)
        vbox.addWidget(self.record_input)
        vbox.addWidget(self.exercise_label)
        vbox.addWidget(self.exercise_input)
        vbox.addWidget(self.add_record_button)
        vbox.addWidget(self.add_report_button)
        vbox.addWidget(self.show_reports_button)

        self.setLayout(vbox)

    def add_record(self):
        name = self.name_input.text()
        age = self.age_input.text()
        gender = ""
        if self.female_checkbox.isChecked():
            gender = "Kadın"
        elif self.male_checkbox.isChecked():
            gender = "Erkek"
        self.user = User(name, age, gender)  # Kullanıcıyı oluşturalım

        record_text = self.record_input.toPlainText()
        exercise_text = self.exercise_input.toPlainText()

        if not record_text:
            QMessageBox.warning(self, "Uyarı", "Lütfen sağlık verisi giriniz.")
            return

        health_record = HealthRecord(record_text)
        record_data = health_record.parse_record()

        if not record_data:
            QMessageBox.warning(self, "Uyarı", "Sağlık verisi eksik veya yanlış formatlı.")
            return

        health_record = HealthRecord(record_data)
        self.user.add_record(health_record)

        dialog = AddRecordDialog(self.user, record_text, exercise_text, self)
        dialog.exec_()

    def add_report(self):
        if not self.user:
            QMessageBox.warning(self, "Uyarı", "Önce bir kullanıcı ekleyin.")
            return

        dialog = ReportInputDialog(self)
        if dialog.exec_():
            text = dialog.text_edit.toPlainText()
            self.user.add_report(text)

            # Rapor penceresini yeniden boyutlandır
            dialog.resize(900, 600)

    def show_reports(self):
        if not self.user:
            QMessageBox.warning(self, "Uyarı", "Önce bir kullanıcı ekleyin.")
            return

        dialog = ShowReportDialog(self.user)
        dialog.exec_()

    def show_welcome_dialog(self):
        dialog = WelcomeDialog(self)
        if dialog.exec_() == QDialog.Rejected:
            sys.exit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
