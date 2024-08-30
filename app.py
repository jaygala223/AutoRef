from flask import Flask, render_template, request, flash, redirect, url_for
import os
from werkzeug.utils import secure_filename
import selenium_autofill
import resume_parser

app = Flask(__name__)
app.secret_key = 'ABCD11'  # Required for flashing messages
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # name = request.form['name']
        # phone = request.form['phone']
        country = 'India'
        # email = request.form['email']
        job_id = request.form['job_id']
        
        # File handling code...
        # Check if the post request has the file part
        if 'resume' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['resume']
        
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Call your Selenium script here
            try:
                print(f"RESUME PATH: {file_path}")
                candidate_name, candidate_mobile, candidate_email = resume_parser.extract_info_from_resume(file_path)
                result = selenium_autofill.fill_form_using_selenium(
                    name=candidate_name,
                    phone_number=candidate_mobile,
                    country_name=country,
                    email=candidate_email,
                    job_req_id=job_id,
                    resume_path=file_path
                )
                flash(f'Application submitted successfully! Result: {result}')
            except Exception as e:
                flash(f'Error submitting application: {str(e)}')
            
            return redirect(url_for('index'))
        else:
            flash('Invalid file type. Please upload a PDF.')
            return redirect(request.url)

    return render_template('index.html')

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)