from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.static_folder = 'static'

db = SQLAlchemy(app)

class Obat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    waktu = db.Column(db.String(20), nullable=False)
    status = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nama': self.nama,
            'waktu': self.waktu,
            'status': self.status
        }

@app.route('/')
def index():
    daftar_obat = Obat.query.all()
    return render_template('index.html', daftar_obat=daftar_obat)

@app.route('/tambah', methods=['POST'])
def tambah():
    nama = request.form['nama']
    waktu = request.form['waktu']
    obat_baru = Obat(nama=nama, waktu=waktu)
    db.session.add(obat_baru)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update_status/<int:id>', methods=['POST'])
def update_status(id):
    obat = Obat.query.get(id)
    if obat:
        obat.status = not obat.status
        db.session.commit()
        return jsonify({'status': obat.status})
    return jsonify({'error': 'Obat tidak ditemukan'}), 404

@app.route('/hapus/<int:id>', methods=['POST'])
def hapus(id):
    obat = Obat.query.get(id)
    if obat:
        db.session.delete(obat)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    os.makedirs(app.static_folder, exist_ok=True)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
