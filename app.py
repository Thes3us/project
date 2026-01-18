from flask import Flask, request, render_template, redirect, url_for
import pymupdf


app = Flask(__name__)
# decorator calls receive() when / is called
@app.route('/',methods=["GET","POST"])
def receive():
    #handle submit button
    if request.method == "POST":
        file = request.files["pdf"]   #stores pdf
        byte_form=file.read()        #reads the file in byte form from the object
        doc = pymupdf.open(stream=byte_form,filetype="pdf")     #opens the file from the byte form

        for page in doc:
            text=page.get_text()   #converts byte to human readable stuff
            print(text)
        #sends user to a new page with parameter "success" to avoid looping bugs
        return redirect(url_for("receive", status="success")) 
    
    status = request.args.get("status") #receives status from URL 

    if status == "success":
        message = "file successfully received"
    else:
        #handles message when website is visited without submit
        message = None
    return render_template("index.html", message = message)
if __name__ == "__main__":
    app.run(debug=True) #tset