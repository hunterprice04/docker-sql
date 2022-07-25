import argparse
import mysql.connector
from mysql.connector import errorcode

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
                        help="the name of the database")
    parser.add_argument('--table-name', '-t', type=str, required=True,
                        help="the name of the table to create")
    parser.add_argument('--table-file', '-f', type=str, required=True,
                        help="the sql to create the table")
    return parser.parse_args()


args = get_args()

cnx = mysql.connector.connect(user=args.username, password=args.password,
                              host=args.host, port=args.port, database=args.database)
cursor = cnx.cursor()

try:
    with open(args.table_file, 'r') as f:
        table_description = ''.join(f.readlines())

    try:
        print("Creating table {}: ".format(args.table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

    cursor.close()
    cnx.close()
except mysql.connector.Error as err:
    print("Failed creating table: {}".format(err))
    exit(1)
except FileNotFoundError as err:
    print('Could not open file: {}'.format(args.table_file))
finally:
    cnx.close()
