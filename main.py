from flask import Flask, render_template, url_for, request, redirect, flash
from db_support import Database

app = Flask(__name__)

@app.route('/test_page/')
def test_page():
    return render_template('test.html')

@app.route('/test/', methods=['GET', 'POST'])
def for_testing():
    print('GET')
    for e in request.args:
        print(e, ': ', repr(request.args[e]))
    print('POST')
    for e in request.values:
        print(e, ': ', repr(request.values[e]))
    return redirect(url_for('test_page'))

@app.route('/')
def main_page():
    return render_template('init.html')

@app.route('/add_to_list', methods=['GET'])
def add_to_list():
    id = request.args['id']
    # insert song(id) to playlist
    flash("add song: {} to list".format(id))
    return redirect(url_for('song'))

@app.route('/song/', methods=['GET'])       # 搜尋的內容放在 GET 區 ?abc=abc
def song():
    # id, name, artist, album, series, time
    outputstr= ""
    for e in request.args:
        print(e, ': ', repr(request.args[e]))
        outputstr += ' {}: {}'.format(e, request.args[e])
    if request.args:
        flash("search for"+ outputstr)

    data = []
    song_attr_seq=['id', 'name', 'artist', 'album', 'series', 'time']
    for e in db.song(request.args):
        song={}
        for i in range(6):
            song[song_attr_seq[i]] = e[i]
        data += [song]
    return render_template('song.html', data = data)

@app.route('/artist/', methods=['GET'])
def artist():
    return render_template('artist.html')

@app.route('/album/', methods=['GET'])
def album():
    return render_template('album.html')

@app.route('/series/', methods=['GET'])
def series():
    return render_template('series.html')

@app.route('/info/', methods=['GET'])
def info():
    return render_template('info.html')

@app.route('/song/edit/<int:id>', methods=['GET', 'POST'])
def edit_song(id):
    if request.method == 'GET':
        print("id:", id)
        data = fake_song_data()[id]
        data['link'] = 'templink'
        for e in request.args:
            data[e] = request.args[e]
        # print(data)
        return render_template('edits/edit song.html', **data)
    elif request.method == 'POST':
        print("POST create song...>")
        for e in request.values:
            print(e, ':', request.values[e])
        # TODO SQL update   success >> return true
        if True:
            flash('更新成功! ')
            return redirect(url_for('song'))
        else:
            flash('更新失敗! ')
            return redirect(url_for('edit_song', **request.values, id=id))

@app.route('/song/create/', methods=['GET', 'POST'])
def create_song():
    song_attr_seq=['name', 'link', 'artist', 'album', 'series', 'time']
    if request.method == 'GET':
        print("GET create song...>")
        for e in request.args:
            print(e, ':', request.args[e])
        
        return render_template('edits/edit song.html', **request.args)
    elif request.method == 'POST':
        print("POST create song...>")
        for e in request.values:
            print(e, ':', request.values[e])
        # TODO SQL insert   success >> return true
        
        args={}
        for e in request.values:
            if e is 'time':
                args[e] = int(request.values[e])
            else:
                args[e] = request.values[e]

        result= db.insert('song', [args[e] for e in song_attr_seq], default=True)
        if result:
            flash('新增成功! ')
            return redirect(url_for('song'))
        else:
            flash('新增失敗! ')
            return redirect(url_for('create_song'))
            #return redirect(url_for('create_song'), code=307)   # POST 過來的資料都會留著 讚!

@app.route('/song/_delete/', methods= ['POST'])
def delete():
    return "123"

def fake_song_data():
    data = []
    for i in range(5):    # id, name, artist, album, series, time
        song = {}
        song['id'] = i
        song['name'] = 'name {}'.format(i)
        song['artist'] = 'artist {}'.format(i)
        song['album'] = 'album {}'.format(i)
        song['series'] = 'series {}'.format(i)
        song['time'] = 'time {}'.format(i)
        data += [song]
    return data

if __name__ == "__main__":
    db = Database()
    db.connect()
    db.select_db(db = 'temp_muxic')

    app.secret_key = 'my secret key'
    app.run(debug = True, port = 5000)
    # db.close()