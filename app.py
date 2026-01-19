from flask import Flask, request, render_template, redirect, url_for
import pdf_reader 
app = Flask(__name__)
# decorator calls receive() when / is called
@app.route('/',methods=["GET","POST"])
def receive():
    #handle submit button
    message = None
    if request.method == "POST":
        file = request.files["pdf"]   #receives pdf in bytestream
        hasContent=pdf_reader.send(file) #sends pdf to send() in pdf_reader.py. returns True if file is not None
        if hasContent:   #if the pdf has content, proceed with status success, else display message accordingly
            #sends user to a new page with parameter "success" to avoid looping bugs
            return redirect(url_for("receive", status="success"))
        else:
            message = "The pdf sent is empty, please send a pdf with content"
    status = request.args.get("status") #receives status from URL 
    if status == "success":
        message = "file successfully received"
    return render_template("index.html", message = message)
if __name__ == "__main__":
    app.run(debug=True) #test