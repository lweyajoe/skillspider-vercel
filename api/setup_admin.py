from app import app, db, Admin  # Import your Flask app instance and the 'Admin' model from app.py

# Create a new Admin object and set the username and password
admin = Admin(username='lweyajoe')
admin.set_password('lilyjoe')

# Add the admin to the database and commit the changes
db.session.add(admin)
db.session.commit()
