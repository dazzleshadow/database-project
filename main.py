from flask import Flask, render_template, url_for, request, redirect, flash
# from test_mysql import cursor, db

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('init.html')

@app.route('/song/', methods=['GET'])       # 搜尋的內容放在 GET 區 ?abc=abc
def song():
    return render_template('song.html')

@app.route('/song/edit/<id>', methods=['GET', 'POST'])
def edit_song(id):
    if request.method == 'GET':
        print("id:", id)
        return render_template('edit.html', id=id)
    elif request.method == 'POST':
        pass
        # TODO SQL update   success >> return true

@app.route('/song/create/', methods=['GET', 'POST'])
def create_song():
    if request.method == 'GET':
        print("GET create song...>")
        for e in request.args:
            print(e, ':', request.args[e])
        
        return render_template('edit.html', **request.args)
    elif request.method == 'POST':
        print("OPST create song...>")
        for e in request.values:
            print(e, ':', request.values[e])
        #input()
        # TODO SQL insert   success >> return true
        if False:
            flash('新增成功! ')
            return render_template('song.html')
        else:
            flash('新增失敗! ')
            return redirect(url_for('create_song', **request.values))
            #return redirect(url_for('create_song'), code=307)   # POST 過來的資料都會留著 讚!

@app.route('/song/_delete/', methods= ['POST'])
def delete():
    return "123"

@app.route('/artist/')
def artist():
    return render_template('init.html')



if __name__ == "__main__":
    app.secret_key = 'my secret key'
    app.run(debug = True, port = 5000)
    # db.close()