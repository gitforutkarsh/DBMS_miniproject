from flask import Flask, render_template, request, redirect, url_for
import re
import sys
import mysql.connector

app = Flask(__name__)

# Connect to MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="utkarsh",
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
    
    # Calculate dashboard metrics
    total_apartments = len(apartments)
    total_tenants = len(tenants)
    vacant_apartments = total_apartments - total_tenants
    
    return render_template('index.html', apartments=apartments, tenants=tenants,
                           total_apartments=total_apartments, total_tenants=total_tenants,
                           vacant_apartments=vacant_apartments)

@app.route('/add_apartment', methods=['POST'])
def add_apartment():
    if request.method == 'POST':
        apartment_number = request.form['apartment_number']
        area = request.form['area']
        rent = request.form['rent']
        # Check if apartment_number is unique
        mycursor.execute("SELECT * FROM Apartments WHERE apartment_number = %s", (apartment_number,))
        existing_apartment = mycursor.fetchone()
        if existing_apartment:
            return "Apartment number already exists!"
        # Validate area and rent are positive numbers
        if float(area) <= 0 or float(rent) <= 0:
            return "Area and rent must be positive numbers!"
        mycursor.execute("INSERT INTO Apartments (apartment_number, area, rent) VALUES (%s, %s, %s)", (apartment_number, area, rent))
        mydb.commit()
        return redirect(url_for('index'))
@app.route('/edit_apartment/<int:apartment_id>', methods=['GET', 'POST'])
def edit_apartment(apartment_id):
    if request.method == 'GET':
        # Fetch apartment details
        mycursor.execute("SELECT * FROM Apartments WHERE apartment_id = %s", (apartment_id,))
        apartment = mycursor.fetchone()
        if apartment:
            return render_template('edit_apartment.html', apartment=apartment)
        else:
            return "Apartment not found"
    elif request.method == 'POST':
        # Update apartment details
        apartment_number = request.form['apartment_number']
        area = request.form['area']
        rent = request.form['rent']
        mycursor.execute("UPDATE Apartments SET apartment_number = %s, area = %s, rent = %s WHERE apartment_id = %s", (apartment_number, area, rent, apartment_id))
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
        
        # Validate mobile_number format
        if not re.match(r'^[0-9]{10}$', mobile_number):
            return "Invalid mobile number format!"
        
        mycursor.execute("INSERT INTO Tenants (name, mobile_number, apartment_id) VALUES (%s, %s, %s)", (name, mobile_number, apartment_id))
        mydb.commit()
        return redirect(url_for('index'))
@app.route('/delete_tenant/<int:tenant_id>')
def delete_tenant(tenant_id):
    mycursor.execute("DELETE FROM Tenants WHERE tenant_id = %s", (tenant_id,))
    mydb.commit()
    return redirect(url_for('index'))

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    mycursor.execute("SELECT * FROM Apartments WHERE apartment_number LIKE %s", ('%' + query + '%',))
    apartments = mycursor.fetchall()
    mycursor.execute("SELECT * FROM Tenants WHERE name LIKE %s OR mobile_number LIKE %s", ('%' + query + '%', '%' + query + '%'))
    tenants = mycursor.fetchall()
    return render_template('index.html', apartments=apartments, tenants=tenants)

@app.route('/exit')
def exit():
    sys.exit()

if __name__ == '__main__':
    app.run(debug=True)

