from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Connect to MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="fuckshivtej",
    database="apartment"
)
mycursor = mydb.cursor()

# Define routes
@app.route('/')
def index():
    # Fetch all apartments and tenants
    mycursor.execute("SELECT * FROM Apartments")
    apartments = mycursor.fetchall()
    mycursor.execute("SELECT * FROM Tenants")
    tenants = mycursor.fetchall()
    return render_template('index.html', apartments=apartments, tenants=tenants)

@app.route('/add_apartment', methods=['POST'])
def add_apartment():
    if request.method == 'POST':
        apartment_number = request.form['apartment_number']
        area = request.form['area']
        rent = request.form['rent']
        mycursor.execute("INSERT INTO Apartments (apartment_number, area, rent) VALUES (%s, %s, %s)", (apartment_number, area, rent))
        mydb.commit()
        return redirect(url_for('index'))

@app.route('/delete_apartment/<int:apartment_id>')
def delete_apartment(apartment_id):
    mycursor.execute("DELETE FROM Apartments WHERE apartment_id = %s", (apartment_id,))
    mydb.commit()
    return redirect(url_for('index'))

@app.route('/add_tenant', methods=['POST'])
def add_tenant():
    if request.method == 'POST':
        name = request.form['name']
        mobile_number = request.form['mobile_number']
        apartment_id = request.form['apartment_id']
        
        # Check if the apartment_id exists in the Apartments table
        mycursor.execute("SELECT * FROM Apartments WHERE apartment_id = %s", (apartment_id,))
        apartment = mycursor.fetchone()
        if not apartment:
            return "Apartment ID does not exist!"
        
        # Insert the new tenant
        mycursor.execute("INSERT INTO Tenants (name, mobile_number, apartment_id) VALUES (%s, %s, %s)", (name, mobile_number, apartment_id))
        mydb.commit()
        return redirect(url_for('index'))

@app.route('/delete_tenant/<int:tenant_id>')
def delete_tenant(tenant_id):
    mycursor.execute("DELETE FROM Tenants WHERE tenant_id = %s", (tenant_id,))
    mydb.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
