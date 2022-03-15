from flask import Flask, render_template

app = Flask(__name__)

@app.route("/<username>")
def user(username):
    if any(char.isdigit() for char in username)==True:
        username = ''.join([i for i in username if not i.isdigit()])
    else:
        username = username.strip()
        if username.isupper()==True:
            username=username.lower()
        elif username.islower()==True:
            username=username.upper()
        elif not username.islower() and not username.isupper():
            username = username.capitalize()

    return render_template("home.html", name=username)
    
    
if __name__ == "__main__":
    app.run(debug=True)