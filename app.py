from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Fungsi untuk membaca data buku dari file JSON
def get_buku_data():
    try:
        with open('buku_data.json', 'r') as file:
            buku_data = json.load(file)
    except FileNotFoundError:
        buku_data = []
    return buku_data

# Fungsi untuk menyimpan data buku ke dalam file JSON
def save_buku_data(data):
    with open('buku_data.json', 'w') as file:
        json.dump(data, file, indent=2)

@app.route('/form', methods=['GET', 'POST'])
def handle_form():
    if request.method == 'POST':
        # Logika untuk menangani data POST disini
        data = request.form

        # Membaca data buku yang sudah ada
        buku_data = get_buku_data()

        # Menambahkan data buku baru
        new_buku = {
            "id": len(buku_data) + 1,
            "judul": data['judul'],
            "pengarang": data['pengarang']
        }

        buku_data.append(new_buku)

        # Menyimpan kembali data buku ke dalam file JSON
        save_buku_data(buku_data)

        # Tampilkan pesan berhasil dan data buku terkini
        return jsonify({"message": "Data berhasil ditambahkan", "buku_data": buku_data}), 200
    else:
        # Tampilkan formulir dengan data buku terkini
        buku_data = get_buku_data()
        return render_template('form.html', buku_data=buku_data)

@app.route('/api/buku', methods=['GET'])
def get_buku_api():
    return jsonify(get_buku_data())

@app.route('/api/buku', methods=['POST'])
def tambah_buku_api():
    data = request.get_json()

    if 'judul' not in data or 'pengarang' not in data:
        return jsonify({"error": "Data tidak lengkap"}), 400

    # Membaca data buku yang sudah ada
    buku_data = get_buku_data()

    # Menambahkan data buku baru
    new_buku = {
        "id": len(buku_data) + 1,
        "judul": data['judul'],
        "pengarang": data['pengarang']
    }

    buku_data.append(new_buku)

    # Menyimpan kembali data buku ke dalam file JSON
    save_buku_data(buku_data)

    return jsonify({"message": "Data buku berhasil ditambahkan", "buku_data": buku_data}), 201

if __name__ == '__main__':
    app.run(debug=True)
