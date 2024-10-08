# AutoRef

This tool is designed to streamline the process of managing referrals and resumes for professional services. It allows users to upload resumes, select referral platforms and submit bulk referrals in one click.

## Features

- **Resume Upload:** Users can upload their resumes in PDF format.
- **Platform Selection:** Users can select the referral platform from a dropdown list.
- **Bulk Referral Submission:** Users can submit bulk referrals in one click.

## Technologies Used

- **Python:** The application is built using Python.
- **Selenium:** The application uses Selenium for web automation. We use Selenium for several key reasons:
  - Avoids firewall issues that may arise with direct API integrations
  - Bypasses Single Sign-On (SSO) complications
  - Works without requiring the user's passwords
  - Simulates human interaction with the referral platform, ensuring compatibility with various systems
- **PyQt6:** The application uses PyQt6 for the GUI of the desktop app.

## How to use

It is recommended to use the application on a computer which can login to the platform you want to refer to. This ensures that Selenium can interact with the referral platform seamlessly, leveraging your existing authentication.


1. **Installation:**
   - Clone the repository: `git clone https://github.com/jaygala223/AutoRef.git`
   - Navigate to the project directory: `cd AutoRef`
   - Create a virtual environment: `python -m venv venv`
   - Activate the virtual environment:
     - On Windows: `venv\Scripts\activate`
     - On macOS and Linux: `source venv/bin/activate`
   - Install the required dependencies: `pip install -r requirements.txt`

2. **Setup:**
   - Launch the application by running `python desktop_app.py`
   - Go to the "Settings" tab and fill in the following information:
     - Default Country
     - Referrer's Email
     - Referral Form Link
     - Chrome Driver Path (download ChromeDriver compatible with your Chrome version)

3. **Using the Application:**
   - In the "New Referral" tab:
     - Click "Upload Resume(s)" to select up to 5 PDF resumes
     - Enter the corresponding Job ID(s) in the "Job ID(s)" field
     - Select the appropriate HR/Referral Platform from the dropdown
   - Click "Submit Referral" to process the referral(s)

4. **Troubleshooting:**
   - Ensure you're logged into the referral platform in your default browser
   - Check that all settings are correctly filled out
   - Verify that the ChromeDriver version matches your Chrome browser version

5. **Note:**
   - The application uses Selenium to automate the referral process, simulating human interaction with the platform
   - Ensure you have the necessary permissions and are following your company's referral policies when using this tool

