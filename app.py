from flask import Flask, request, render_template
app = Flask(__name__)
# decorator calls age() when / is called
@app.route('/',methods=["GET","POST"])
def age():
    if request.method == "POST":
        file = request.files["pdf"]
        return "file successfully recieved"
    else:
        return "error occured"
if __name__ == "__main__":
    app.run(debug=True)