import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g

app = Flask(__name__)
DATABASE = 'database.db'

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        # This allows accessing columns by name, like a dictionary
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Closes the database again at the end of the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    """Route to display all items."""
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM items ORDER BY created_at DESC")
    items = cursor.fetchall()
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add_item():
    """Route to add a new item."""
    name = request.form['name']
    code = request.form['code']
    purchase_date = request.form['purchase_date']
    price = request.form['price']
    status = request.form['status']

    db = get_db()
    db.execute(
        'INSERT INTO items (name, code, purchase_date, price, status) VALUES (?, ?, ?, ?, ?)',
        (name, code, purchase_date, price, status)
    )
    db.commit()
    # We can add flash messaging later for user feedback
    return redirect(url_for('index'))

@app.route('/update/<int:item_id>', methods=['POST'])
def update_item(item_id):
    """Route to update an item."""
    name = request.form['name']
    code = request.form['code']
    purchase_date = request.form['purchase_date']
    price = request.form['price']
    status = request.form['status']

    db = get_db()
    db.execute(
        'UPDATE items SET name = ?, code = ?, purchase_date = ?, price = ?, status = ? WHERE id = ?',
        (name, code, purchase_date, price, status, item_id)
    )
    db.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    """Route to delete an item."""
    db = get_db()
    db.execute('DELETE FROM items WHERE id = ?', (item_id,))
    db.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=8080)
