import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox,
                             QTabWidget, QScrollArea, QFormLayout, QCheckBox, QComboBox, QStackedWidget, QDialog, QMainWindow, QStatusBar)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt, QSize
from pathlib import Path
from resume_parser import extract_info_from_resume
from selenium_autofill import fill_workday_form_using_selenium
import stripe

class PaymentDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Payment")
        self.setGeometry(300, 300, 400, 250)
        
        layout = QVBoxLayout()
        
        self.amount_label = QLabel("Your card will be charged $5 for 5 referrals.\nPayments are processed securely using Stripe.")
        self.amount_label.setWordWrap(True)
        layout.addWidget(self.amount_label)
        
        self.card_number = QLineEdit()
        self.card_number.setPlaceholderText("Card Number")
        layout.addWidget(self.card_number)
        
        self.expiry = QLineEdit()
        self.expiry.setPlaceholderText("MM/YY")
        layout.addWidget(self.expiry)
        
        self.cvc = QLineEdit()
        self.cvc.setPlaceholderText("CVC")
        layout.addWidget(self.cvc)
        
        self.pay_button = QPushButton("Pay")
        self.pay_button.clicked.connect(self.process_payment)
        layout.addWidget(self.pay_button)
        
        self.setLayout(layout)

    def process_payment(self):
        # Here you would integrate with Stripe API to process the payment
        # For demonstration, we'll just show a success message
        QMessageBox.information(self, "Payment Successful", "Your payment was processed successfully!")
        self.accept()

class ReferralApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.referral_count = 0
        self.max_free_referrals = 5
        self.max_resumes = 5
        self.initUI()
        
        # Initialize Stripe
        stripe.api_key = "your_stripe_secret_key"

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
        self.help_tab = QWidget()
        
        self.tab_widget.addTab(self.referral_tab, "New Referral")
        self.tab_widget.addTab(self.history_tab, "History")
        self.tab_widget.addTab(self.help_tab, "Help")
        
        # Set up the tabs
        self.setup_referral_tab()
        self.setup_history_tab()
        self.setup_help_tab()
        
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

        # Default Email Section
        self.email_input = QLineEdit()
        layout.addRow("Default Email:", self.email_input)

        # Default Country Section
        self.default_country = QLineEdit()
        self.default_country.setPlaceholderText("Enter Default Country...")
        layout.addRow("Default Country:", self.default_country)

        # HR/Referral Platform Section
        self.platform_dropdown = QComboBox()
        self.platform_dropdown.addItem("Workday + Azure SSO")
        self.platform_dropdown.addItem("Zoho (Not available yet. Work is in progress)")
        layout.addRow("HR/Referral Platform:", self.platform_dropdown)

        # Referral Form Link Section
        self.form_link_input = QLineEdit()
        self.form_link_input.setPlaceholderText("Enter the URL of your referral form...")
        layout.addRow("Referral Form Link:", self.form_link_input)

        # Submit Button
        self.submit_button = QPushButton("Submit Referral")
        self.submit_button.clicked.connect(self.submit_referral)
        layout.addRow(self.submit_button)

        # Referral Count Label
        self.referral_count_label = QLabel(f"Referrals remaining: {self.max_free_referrals - self.referral_count}")
        layout.addRow(self.referral_count_label)

        self.referral_tab.setLayout(layout)

    def setup_history_tab(self):
        layout = QVBoxLayout()
        history_label = QLabel("Your referral history will appear here.")
        layout.addWidget(history_label)
        self.history_tab.setLayout(layout)

    def setup_help_tab(self):
        layout = QVBoxLayout()
        help_text = QLabel("Help us improve by reporting bugs or suggesting features.\nContact us at support@referralapp.com")
        help_text.setWordWrap(True)
        layout.addWidget(help_text)
        self.help_tab.setLayout(layout)

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
        referrer_email = self.email_input.text()
        country_name = self.default_country.text()

        if not resume_paths or not job_ids:
            QMessageBox.warning(self, "Missing Information", "Please provide both resumes and Job IDs.")
            return

        if len(resume_paths) > self.max_resumes or len(job_ids) > self.max_resumes:
            QMessageBox.warning(self, "Too Many Inputs", f"You can only submit a maximum of {self.max_resumes} resumes and job IDs at a time.")
            return

        if self.referral_count >= self.max_free_referrals:
            reply = QMessageBox.question(self, "Free Limit Reached", 
                                         "You have reached the limit of free referrals. Would you like to make a payment to continue?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                payment_dialog = PaymentDialog(self)
                if payment_dialog.exec() == QDialog.DialogCode.Accepted:
                    self.referral_count = 0
                    self.referral_count_label.setText(f"Referrals remaining: {self.max_free_referrals - self.referral_count}")
                else:
                    return
            else:
                return

        try:
            for resume_path, job_id in zip(resume_paths, job_ids):
                if self.referral_count >= self.max_free_referrals:
                    break
                
                candidate_name, candidate_phone_number, candidate_email = extract_info_from_resume(Path(resume_path.strip()))
                
                fill_workday_form_using_selenium(referrer_email=referrer_email, name=candidate_name, email=candidate_email, country_name=country_name, phone_number=candidate_phone_number, job_req_id=job_id.strip(), resume_path=Path(resume_path.strip()))
                
                self.referral_count += 1
                self.referral_count_label.setText(f"Referrals remaining: {self.max_free_referrals - self.referral_count}")

            QMessageBox.information(self, "Referrals Submitted", "Referrals have been submitted successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ReferralApp()
    window.show()
    sys.exit(app.exec())