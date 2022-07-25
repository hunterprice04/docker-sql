import argparse
import mysql.connector


def get_args():
    parser = argparse.ArgumentParser(description='Create a database.')
    parser.add_argument('--username', '-u',  type=str, required=True,
                        help='the username')
    parser.add_argument('--password', '-p', type=str, required=True,
                        help="the users password")
    parser.add_argument('--host', type=str, required=False,
                        default='127.0.0.1',
                        help="the host")
    parser.add_argument('--port', type=int, required=False,
                        default=3306,
                        help="the port")
    parser.add_argument('--database', '-d', type=str, required=True,
                        help="the name of the database to create")
    return parser.parse_args()


args = get_args()
DB_NAME = args.database

cnx = mysql.connector.connect(user=args.username, password=args.password,
                              host=args.host, port=args.port)
cursor = cnx.cursor()

try:
    cursor.execute(
        "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    print("Database {} created successfully.".format(DB_NAME))
except mysql.connector.Error as err:
    print("Failed creating database: {}".format(err))
    exit(1)
finally:
    cnx.close()