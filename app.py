from flask import Flask, render_template, request, send_from_directory
import os
import sqlite3

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Database banana
def create_db():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT,
                semester TEXT,
                branch TEXT,
                uploaded_by TEXT,
                filename TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("SELECT * FROM notes")
    notes = c.fetchall()
    conn.close()
    return render_template('home.html', notes=notes)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        subject = request.form['subject']
        semester = request.form['semester']
        branch = request.form['branch']
        uploaded_by = request.form['uploaded_by']
        file = request.files['file']
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            conn = sqlite3.connect('notes.db')
            c = conn.cursor()
            c.execute("INSERT INTO notes (subject, semester, branch, uploaded_by, filename) VALUES (?,?,?,?,?)",
                      (subject, semester, branch, uploaded_by, file.filename))
            conn.commit()
            conn.close()
            return render_template('upload.html', success=True)
    return render_template('upload.html', success=False)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    create_db()
    app.run(debug=True)