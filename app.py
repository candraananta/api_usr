from flask import Flask,request,jsonify 
import sqlite3

app = Flask(__name__) # membuat variable app

# KONEKSI KE DATABASE DEFAULT

def get_connection():
    try:    
        koneksi = sqlite3.connect('database.db')
        koneksi.row_factory = sqlite3.Row
        return koneksi
    except sqlite3.OperationalError as e:
        print(f'Kesalahan koneksi: {e}')
        return None
    except Exception as e:
        print(f'Kesalahan umum: {e}')
        return None
    except FileNotFoundError:
        print('Database database.db tidak ditemukan.')
        return None
    finally:
        if koneksi:
            print('Berhasil konek kedatabase')
        else:
            print('Gagal konek ke database.')

def create_table():
    try:
        koneksi = get_connection()
        if koneksi:
            kursor = koneksi.cursor()
            kursor.execute(
                            '''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL
                    )
                '''
            )
            koneksi.commit()
            koneksi.close()
            print('Berhasil membuat table users')
    except sqlite3.OperationalError as e:
        print(f'Kesalahan membuat table: {e}')
    except Exception as e:
        print(f'Kesalahan umum: {e}')

# Inisialisasi tabel saat aplikasi dijalankan
create_table()
        
# MEMBUAT ENDPOINT
@app.route('/users', methods=['GET'])
def get_users():
    koneksi= get_connection()
    if koneksi:
        
        kursor = koneksi.cursor()
        kursor.execute('SELECT * FROM users')
        rows = kursor.fetchall()
        koneksi.close()
        return jsonify([dict(row) for row in rows])
        

# MAIN
if __name__ =='__main__':
    app.run(debug=True) # Menjalankan server di port 5000

    
    