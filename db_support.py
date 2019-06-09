import pymysql

def temp_exec(cmd):
    print(cmd)

def format_str(s):
    return '\"{}\"'.format(s) if isinstance(s, str) else str(s)

def format_kwargs(kwargs, sep=', '):
    # {'a': 1, 'b': '2'}
    args = ''
    if kwargs:
        args += sep.join( e+'='+format_str(kwargs[e]) for e in kwargs if kwargs[e] != '')
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

    def output(self, table, args='*', kwargs=None):
        formated = format_kwargs(kwargs, ' and ')
        if formated != '':
            self.exec("SELECT " + args + ' FROM ' + table + ' WHERE ' + formated)
        else:
            self.exec("SELECT " + args + ' FROM ' + table)
        return self.cursor

    def exec(self, command):
        try:
            self.cursor.execute(command)
        except Exception as e:
            print('ERROR {}: {}'.format(e.args[0], e.args[1]))
            #print('Got error {!r}, errno is {}'.format(e, e.args[0]))

    def __del__(self):
        print('close connection')
        if self.db:
            self.db.close()

    def song(self, kwargs=None):
        empty = True
        for e in kwargs:
            if kwargs[e] != '':
                empty = False
        if empty:
            self.output('song', 'id, name, artist, album, series, time')
        else:
            self.output('song', 'id, name, artist, album, series, time', kwargs=kwargs)
        return self.cursor
    def artist(self, kwargs=None):
        self.output('artist', 'name, company', kwargs=kwargs)
        return self.cursor
    def album(self, kwargs=None):
        self.output('album', 'name. artist, year', kwargs=kwargs)
        return self.cursor
    def series(self, kwargs=None):
        self.output('series', 'name, type', kwargs=None)
        return self.cursor
    def playlist(self):
        self.exec('SELECT name, artist, album, series, time, Sequence FROM song JOIN playlist ON ID = song_id ORDER BY Sequence;')
        return self.cursor

if __name__ == "__main__":
    my_db = Database()
    my_db.connect()
    my_db.select_db(db = 'temp_muxic')
    
    for e in my_db.playlist():
        print(e)
