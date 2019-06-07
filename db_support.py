import pymysql

def temp_exec(cmd):
    print(cmd)

def format_str(s):
    return '\"{}\"'.format(s) if isinstance(s, str) else str(s)

def format_kwargs(kwargs, sep=', '):
    # {'a': 1, 'b': '2'}
    args = ''
    args += sep.join( e+'='+format_str(kwargs[e]) for e in kwargs)
    return args

def format_args(args):
    # (1, 2, '3')
    return ', '.join(format_str(e) for e in args)


class Database():
    def __init__(self):
        self.db = None
        self.cursor = None
    def connect(self, host='localhost', user="root", passwd="12345678"):
        try:
            self.db = pymysql.connect(host=host, user=user, passwd=passwd)
            self.cursor = self.db.cursor()
            return True
        except:
            print("Error: Connect denied")
            return False
    def select_db(self, db='university'):
        try:
            self.cursor.execute("USE " + db)
        except:
            print("Error: Can\'t use database " + db)

    def insert(self, table, args, default = False):
        temp_exec('INSERT INTO {} VALUES({}{});'.format(
                  table, 'default, 'if default else '', format_args(args)))

    def update(self, table, kwargs, **restrict):
        temp_exec('UPDATE {} SET {} WHERE {};'.format(
                  table, format_kwargs(kwargs), format_kwargs(restrict, sep=' and ') ))
        
    def delete(self, table, **restrict):
        temp_exec('DELETE FROM {} WHERE {};'.format(table, format_kwargs(restrict, sep=' and ')))


    def exec(self, command):
        try:
            self.cursor.execute(command)
        except Exception as e:
            print('ERROR {}: {}'.format(e.args[0], e.args[1]))
            #print('Got error {!r}, errno is {}'.format(e, e.args[0]))
 
    def output(self, table):
        self.exec('SELECT * FROM ' + table)
        return self.cursor
    
    def __del__(self):
        print('close connection')
        if self.db:
            self.db.close()

if __name__ == "__main__":
    my_db = Database()
    '''
    my_db.connect()
    my_db.select_db(db = 'practice')
    '''
    myd={}
    myd['hi'] = 0
    myd['ho'] = '1'
    my_db.update(123, myd, **myd)
    print()
    my_db.insert('table', (1, 2, 3, '4', '6'), default=True)
    print()
    my_db.delete('table', **{'abc': 1, '456': 'a'})
    

    '''
    cmd = input('mysql> ')
    while cmd != '0':
        my_db.exec(cmd)
        for e in my_db.cursor:
            print(e)
        cmd = input('mysql> ')
    '''