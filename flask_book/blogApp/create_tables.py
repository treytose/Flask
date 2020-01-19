from app import create_app, db
from app.models import Role, User, Post

print("WARNING: THIS WILL ERASE ALL DATA IN THE DATABASE")
answer = input("Do you want to continue? (y/n)\n")

if answer == 'y':
    app = create_app('default')
    app.app_context().push()
    db.drop_all()

    db.create_all()
    Role.insert_roles()
    User.generate_fake()
    Post.generate_fake()
    u = User(email='treyholthe@gmail.com',
             username='treytose',
             password='asdf',
             confirmed=True,
             name='Trey Holthe')
    db.session.add(u)
    db.session.commit()
    print("Database reset")

else:
    print("Canceled")
