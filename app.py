from flask import Flask, request, render_template
import pymupdf


app = Flask(__name__)
# decorator calls recieve() when / is called
@app.route('/',methods=["GET","POST"])
def recieve():
    if request.method == "POST":
        file = request.files["pdf"]     #stores an object
        byte_form=file.read()        #reads the file in byte form from the object

        doc = pymupdf.open(stream=byte_form,filetype="pdf")     #opens the file from the byte form
        for page in doc:
            text=page.get_text()                                  #converts byte to human readable stuff
            print(text)
        return "file successfully recieved"
    else:
        return render_template("index.html")
if __name__ == "__main__":
    app.run(debug=True)