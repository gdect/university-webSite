from flask import Flask, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'

nextId = 4
topics = [
    {'id': 1, 'title': 'Site Information', 'body': 'Site information is being tested. (The site information has been accessed successfully.)'},
    {'id': 2, 'title': 'Page Introduction', 'body': 'Page introduction is being tested. (You have successfully accessed Page introduction.)'},
    {'id': 3, 'title': 'Terms and conditions', 'body': 'The terms and conditions are being tested. (The terms and conditions have dadasd.)'}
]

# Simulated user database
users = {
    'user1': 'password1',
    'user2': 'password2'
}

def template(contents, content, id=None):
    contextUI = ''
    if id is not None:
        contextUI = f'''
            <li><a href="/update/{id}/">Edit</a></li>
            <li><form action="/delete/{id}/" method="POST"><input type="submit" value="Delete"></form></li>
        '''
    return f'''<!doctype html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f2f2f2;
            }}
            h1 {{
                text-align: center;
                margin-top: 50px;
            }}
            h2 {{
                color: #333;
            }}
            form {{
                width: 50%;
                margin: auto;
            }}
            input[type="text"],
            input[type="password"],
            textarea {{
                width: 100%;
                padding: 10px;
                margin: 10px 0;
                box-sizing: border-box;
            }}
            input[type="submit"] {{
                width: 100%;
                padding: 10px;
                margin-top: 10px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }}
            input[type="submit"]:hover {{
                background-color: #45a049;
            }}
            p {{
                margin: 10px 0;
            }}
            ol {{
                padding-left: 20px;
            }}
            ul {{
                list-style-type: none;
                padding: 0;
            }}
            li {{
                margin-bottom: 10px;
            }}
            .container {{
                max-width: 800px;
                margin: auto;
                padding: 20px;
                background-color: #fff;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <img src="static/what.PNG"> 
            <h1><a href="/">'Sub Page'</a></h1>
            <ol>
                {contents}
            </ol>
            {content}
            <ul>
                <li><a href="/create/">Post</a></li>
                {contextUI}
            </ul>
            {login_status()}
        </div>
    </body>
    </html>
    '''

def getContents():
    liTags = ''
    for topic in topics:
        liTags = liTags + f'<li><a href="/read/{topic["id"]}/">{topic["title"]}</a></li>'
    return liTags

def login_status():
    if 'username' in session:
        return f'<p>Logged in as {session["username"]} | <a href="/logout">Logout</a></p>'
    else:
        return '<p><a href="/login">Login</a> | <a href="/register">Register</a></p>'

@app.route('/')
def index():
    return template(getContents(), '<h2>Welcome to Sub Page!</h2>test')

@app.route('/read/<int:id>/')
def read(id):
    title = ''
    body = ''
    for topic in topics:
        if id == topic['id']:
            title = topic['title']
            body = topic['body']
            break
    return template(getContents(), f'<h2>{title}</h2>{body}', id)

@app.route('/create/', methods=['GET', 'POST'])
def create():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'GET': 
        content = '''
            <form action="/create/" method="POST">
                <p><input type="text" name="title" placeholder="Post"></p>
                <p><textarea name="body" placeholder="Write a Post"></textarea></p>
                <p><input type="submit" value="create"></p>
            </form>
        '''
        return template(getContents(), content)
    elif request.method == 'POST':
        global nextId
        title = request.form['title']
        body = request.form['body']
        newTopic = {'id': nextId, 'title': title, 'body': body}
        topics.append(newTopic)
        url = '/read/'+str(nextId)+'/'
        nextId += 1
        return redirect(url)

@app.route('/update/<int:id>/', methods=['GET', 'POST'])
def update(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'GET': 
        title = ''
        body = ''
        for topic in topics:
            if id == topic['id']:
                title = topic['title']
                body = topic['body']
                break
        content = f'''
            <form action="/update/{id}/" method="POST">
                <p><input type="text" name="title" placeholder="Post" value="{title}"></p>
                <p><textarea name="body" placeholder="Write a Post">{body}</textarea></p>
                <p><input type="submit" value="update"></p>
            </form>
        '''
        return template(getContents(), content)
    elif request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        for topic in topics:
            if id == topic['id']:
                topic['title'] = title
                topic['body'] = body
                break
        url = '/read/'+str(id)+'/'
        return redirect(url)

@app.route('/delete/<int:id>/', methods=['POST'])
def delete(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    for topic in topics:
        if id == topic['id']:
            topics.remove(topic)
            break
    return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username not in users:
            users[username] = password
            return redirect(url_for('login'))
        else:
            return "Username already exists!"
    return '''
        <form method="post">
            <p><input type=text name=username placeholder="Username">
            <p><input type=password name=password placeholder="Password">
            <p><input type=submit value=Register>
        </form>
    '''

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
