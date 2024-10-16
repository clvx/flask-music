import sentry_sdk

from flask import Flask, request, jsonify
from database import Database

sentry_sdk.init(
    dsn="https://d9f7df913ad97bdac25451ac76a71b49@o4508129378107392.ingest.us.sentry.io/4508129379614720",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

app = Flask(__name__)
db = Database('music_library.db')

@app.route('/add', methods=['POST'])
def add_music():
    data = request.get_json()
    db = Database('music_library.db')
    db.create_table()
    if 'title' not in data or 'artist' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    db.add_music(data)
    return jsonify({'message': 'Music added successfully'}), 201

@app.route('/all', methods=['GET'])
def get_all_music():
    db = Database('music_library.db')
    db.create_table()
    return jsonify(db.get_all_music())

@app.route('/update', methods=['PUT'])
def update_music():
    data = request.get_json()
    db = Database('music_library.db')
    db.create_table()
    if 'title' not in data or 'artist' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    print(data)
    db.update_music(data)
    return jsonify({'message': 'Music updated successfully'}), 200

#@app.route('/delete/<int:id>', methods=['DELETE'])
#def delete_music(id):
#    db = Database('music_library.db')
#    with db.lock:
#        try:
#            db.cursor.execute('''
#                DELETE FROM music_library
#                WHERE id = ?
#            ''', (id,))
#            self.conn.commit()
#            return jsonify({'message': 'Music deleted successfully'}), 200
#        except sqlite3.Error as e:
#            print(f"Error deleting music: {e}")
#            return jsonify({'error': 'Failed to delete music'}), 500
#        finally:
#            db.cursor.close()
#
#@app.route('/delete/all', methods=['DELETE'])
#def delete_all_music():
#    db = Database('music_library.db')
#    with db.lock:
#        try:
#            db.cursor.execute('''
#                DELETE FROM music_library
#            ''')
#            self.conn.commit()
#            return jsonify({'message': 'All music deleted successfully'}), 200
#        except sqlite3.Error as e:
#            print(f"Error deleting all music: {e}")
#            return jsonify({'error': 'Failed to delete all music'}), 500
#        finally:
#            db.cursor.close()                                 

#@app.route('/delete', methods=['DELETE'])
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_music(id):
    print(type(id))
    db = Database('music_library.db')
    db.create_table()
    result = db.delete_music(id)
    if result:
        return jsonify({'message': 'Music deleted successfully'}), 200
    else:
        return jsonify({'error': 'Failed to delete music'}), 500

if __name__ == '__main__':
    app.run(debug=True)

