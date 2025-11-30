from flask import Flask, render_template, request, redirect, flash
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'yaboekhouding_secret_2024'

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('Geen bestand geselecteerd')
        return redirect('/')
    
    file = request.files['file']
    klant_naam = request.form['klant_naam']
    
    if file.filename == '':
        flash('Geen bestand geselecteerd')
        return redirect('/')
    
    if file and allowed_file(file.filename):
        klant_map = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(klant_naam))
        os.makedirs(klant_map, exist_ok=True)
        
        filename = secure_filename(file.filename)
        file.save(os.path.join(klant_map, filename))
        
        flash(f'Bestand succesvol geüpload voor {klant_naam}!')
        return redirect('/')
    else:
        flash('Alleen PDF, PNG, JPG bestanden zijn toegestaan')
        return redirect('/')

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
