from app import create_app, db
from app.models import Role

print("WARNING: THIS WILL ERASE ALL DATA IN THE DATABASE")
answer = input("Do you want to continue? (y/n)\n")

if answer == 'y':
    app = create_app('default')
    app.app_context().push()
    db.drop_all()
    db.create_all()
    Role.insert_roles()
    print("Database reset")

else:
    print("Canceled")
