import sqlite3 as sql
import os, time, locale, sys

database_name = 'accounting.db'
db_create_file = 'database.sql'
db_pop_file = 'populate.sql'

def read_statement(fh):
    '''
    Read a statement from the *.sql file and return it. This skips comments and concatinates lines
    until a ';' is read.

    A comment is text that starts with a '#' and continues to the end of the line.
    '''
    retv = ''
    for line in fh:
        # strip comments from the line
        idx = line.find('#')
        line = line[0:idx].strip()
        # If there is anything left, append it to the return value.
        if len(line) > 0:
            retv += " %s"%(line)
            if line[-1] == ';':
                break

    return retv

def run_file(db, name):
    '''
    Execute all of the statements in a *.sql file.
    '''
    sys.stderr.write('running file: %s\n'%(name))
    with open(name) as fh:
        while True:
            line = read_statement(fh)
            if len(line) > 0:
                #print(line)
                sys.stderr.write('.')
                db.execute(line)
            else:
                break

    sys.stderr.write('\n')

def create_database():
    '''
    Create the database if it does not exist already.
    '''
    # Load the DB creation file and create the database from that.

    c = sql.connect(database_name)
    db = c.cursor()
    run_file(db, db_create_file)
    run_file(db, db_pop_file)
    c.commit()
    c.close()

if __name__ == '__main__':

    if os.path.exists(database_name):
        os.remove(database_name)
    create_database()
