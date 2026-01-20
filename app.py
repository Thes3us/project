from flask import Flask, request, render_template, redirect, url_for
import pdf_reader 
app = Flask(__name__)
# decorator calls receive() when / is called
@app.route('/',methods=["GET","POST"])
def receive():
    #handle submit button
    message = "sample"
    if request.method == "POST":
        file = request.files["pdf"]   #receives pdf in bytestream
        content, hasContent=pdf_reader.send(file) #sends pdf to send() in pdf_reader.py. 
        if hasContent:   #if the pdf has content, send content back to html
            return render_template("index.html", message = content)
        else:
            message = "The pdf sent is empty, please send a pdf with content"
    return render_template("index.html", message = message)
if __name__ == "__main__":
    app.run(debug=True) #test