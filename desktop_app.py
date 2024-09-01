import sys
import json
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox,
                             QTabWidget, QScrollArea, QFormLayout, QCheckBox, QComboBox, QStackedWidget, QDialog, QMainWindow, QStatusBar)
from PyQt6.QtGui import QFont, QIcon, QDesktopServices
from PyQt6.QtCore import Qt, QSize, QUrl
from pathlib import Path
from resume_parser import extract_info_from_resume
from selenium_autofill import fill_workday_form_using_selenium

class ReferralApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.max_resumes = 5
        self.settings = self.load_settings()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('AutoRef - Professional Referral Management')
        self.setGeometry(100, 100, 1000, 700)
        self.setWindowIcon(QIcon('assets/AUTOREF.gif'))

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Create and add tabs
        self.tab_widget = QTabWidget()
        self.tab_widget.setDocumentMode(True)
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        
        self.referral_tab = QWidget()
        self.history_tab = QWidget()
        self.settings_tab = QWidget()
        
        self.tab_widget.addTab(self.referral_tab, "New Referral")
        self.tab_widget.addTab(self.history_tab, "History")
        self.tab_widget.addTab(self.settings_tab, "Settings")
        
        # Set up the tabs
        self.setup_referral_tab()
        self.setup_history_tab()
        self.setup_settings_tab()
        
        main_layout.addWidget(self.tab_widget)

        # Create status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")

        # Set the stylesheet for a professional look
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QTabWidget::pane {
                border: 1px solid #cccccc;
                background: white;
            }
            QTabBar::tab {
                background: #e0e0e0;
                border: 1px solid #c0c0c0;
                padding: 5px;
                min-width: 100px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom-color: white;
            }
            QLabel {
                font-size: 12px;
            }
            QLineEdit, QPushButton, QComboBox {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 3px;
            }
            QPushButton {
                background-color: #0078d7;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1e88e5;
            }
        """)

    def setup_referral_tab(self):
        layout = QFormLayout()
        
        # Resume Upload Section
        self.resume_path = QLineEdit()
        self.resume_path.setPlaceholderText("Select up to 5 resume files...")
        self.resume_path.setReadOnly(True)
        upload_button = QPushButton("Browse")
        upload_button.clicked.connect(self.upload_resume)
        resume_layout = QHBoxLayout()
        resume_layout.addWidget(self.resume_path)
        resume_layout.addWidget(upload_button)
        layout.addRow("Resumes:", resume_layout)

        # Job ID Section
        self.job_id_input = QLineEdit()
        self.job_id_input.setPlaceholderText("Enter Job IDs (comma separated)...")
        layout.addRow("Job IDs:", self.job_id_input)

        # HR/Referral Platform Section
        self.platform_dropdown = QComboBox()
        self.platform_dropdown.addItem("Workday + Azure SSO")
        self.platform_dropdown.addItem("Zoho (Not available yet. Work is in progress)")
        layout.addRow("HR/Referral Platform:", self.platform_dropdown)

        # Submit Button
        self.submit_button = QPushButton("Submit Referral")
        self.submit_button.clicked.connect(self.submit_referral)
        layout.addRow(self.submit_button)

        self.referral_tab.setLayout(layout)

    def setup_history_tab(self):
        layout = QVBoxLayout()
        history_label = QLabel("Your referral history will appear here. (Work in progress)")
        layout.addWidget(history_label)
        self.history_tab.setLayout(layout)

    def setup_settings_tab(self):
        layout = QFormLayout()

        # Default Country Section
        self.default_country = QLineEdit()
        self.default_country.setText(self.settings.get('default_country', ''))
        self.default_country.setPlaceholderText("Enter Default Country...")
        layout.addRow("Default Country:", self.default_country)

        # Referrer's Email Section
        self.email_input = QLineEdit()
        self.email_input.setText(self.settings.get('referrer_email', ''))
        layout.addRow("Referrer's Email:", self.email_input)

        # Referral Form Link Section
        self.form_link_input = QLineEdit()
        self.form_link_input.setText(self.settings.get('form_link', ''))
        self.form_link_input.setPlaceholderText("Enter the URL of your referral form...")
        layout.addRow("Referral Form Link:", self.form_link_input)

        # Chrome Driver Path Section
        self.chrome_driver_path = QLineEdit()
        self.chrome_driver_path.setText(self.settings.get('chrome_driver_path', ''))
        self.chrome_driver_path.setPlaceholderText("Enter the path to your Chrome driver...")
        layout.addRow("Chrome Driver Path:", self.chrome_driver_path)

        # Save Settings Button
        save_button = QPushButton("Save Settings")
        save_button.clicked.connect(self.save_settings)
        layout.addRow(save_button)

        help_text = QLabel("\n\n\nHelp us improve by reporting bugs or suggesting features.")
        help_text.setWordWrap(True)
        layout.addRow(help_text)

        github_link = QLabel('Github: <a href="https://www.github.com/jaygala223/AutoRef">https://www.github.com/jaygala223/AutoRef</a>')
        github_link.setOpenExternalLinks(True)
        layout.addRow(github_link)

        self.settings_tab.setLayout(layout)

    def upload_resume(self):
        file_names, _ = QFileDialog.getOpenFileNames(self, "Upload Resumes", "", "PDF Files (*.pdf);;All Files (*)")
        if file_names:
            if len(file_names) > self.max_resumes:
                QMessageBox.warning(self, "Too Many Resumes", f"You can only upload a maximum of {self.max_resumes} resumes at a time.")
                file_names = file_names[:self.max_resumes]
            self.resume_path.setText(", ".join(file_names))

    def submit_referral(self):
        resume_paths = self.resume_path.text().split(",")
        job_ids = self.job_id_input.text().split(",")
        referrer_email = self.settings.get('referrer_email', '')
        country_name = self.settings.get('default_country', '')
        form_link = self.settings.get('form_link', '')
        chrome_driver_path = self.settings.get('chrome_driver_path', '')

        if not resume_paths or not job_ids:
            QMessageBox.warning(self, "Missing Information", "Please provide both resumes and Job IDs.")
            return

        if len(resume_paths) > self.max_resumes or len(job_ids) > self.max_resumes:
            QMessageBox.warning(self, "Too Many Inputs", f"You can only submit a maximum of {self.max_resumes} resumes and job IDs at a time.")
            return

        if not all([referrer_email, country_name, form_link, chrome_driver_path]):
            QMessageBox.warning(self, "Missing Settings", "Please fill in all the settings before submitting a referral.")
            return

        try:
            for resume_path, job_id in zip(resume_paths, job_ids):
                candidate_name, candidate_phone_number, candidate_email = extract_info_from_resume(Path(resume_path.strip()))
                
                fill_workday_form_using_selenium(referrer_email=referrer_email, name=candidate_name, email=candidate_email, country_name=country_name, phone_number=candidate_phone_number, job_req_id=job_id.strip(), resume_path=Path(resume_path.strip()), form_link=form_link, chrome_driver_path=chrome_driver_path)
                
            QMessageBox.information(self, "Referrals Submitted", "Referrals have been submitted successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_settings(self):
        settings = {
            'default_country': self.default_country.text(),
            'referrer_email': self.email_input.text(),
            'form_link': self.form_link_input.text(),
            'chrome_driver_path': self.chrome_driver_path.text()
        }
        with open('settings.json', 'w') as f:
            json.dump(settings, f)
        self.settings = settings
        QMessageBox.information(self, "Settings Saved", "Your settings have been saved successfully!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ReferralApp()
    window.show()
    sys.exit(app.exec())