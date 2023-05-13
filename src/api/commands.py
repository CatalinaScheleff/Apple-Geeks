import click
from api.models import db, User, Proveedor, Categoria, Servicio, ImagenServicio


def setup_commands(app):
    """ 
    This is an example command "insert-test-users" that you can run from the command line
    by typing: $ flask insert-test-users 5
    Note: 5 is the number of users to add
    """
    @app.cli.command("insert-test-users")  # name of our command
    @click.argument("count")  # argument of out command
    def insert_test_data(count):
        with app.app_context():
            print("Creating test users")
            for x in range(1, int(count) + 1):
                user = User()
                user.email = "test_user" + str(x) + "@test.com"
                user.password = "123456"
                user.is_active = True
                db.session.add(user)
                db.session.commit()
                print("User: ", user.email, " created.")

            print("All test users created")
