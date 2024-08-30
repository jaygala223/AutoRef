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
