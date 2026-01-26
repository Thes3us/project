from flask import Flask, request, render_template
import pdf_reader 
import resumeai 
app = Flask(__name__)
# decorator calls receive() when / is called
@app.route('/',methods=["GET","POST"])
def receive():
    #handle submit button
    message = ""
    if request.method == "POST":
        file = request.files["pdf"]   #receives pdf in bytestream
        response = pdf_reader.send(file) #sends pdf to send() in pdf_reader.py. 
        # error handling
        if response == "too large":  
           message = "ERROR: File size exceeded. Please send a smaller file."
           return render_template("index.html", message = message) #if the pdf has content, send content back to html
        elif response == "invalid format":
            message = "ERROR: Invalid format. Please send a file ending with .pdf."
        elif response == "unable to open":
            message = "ERROR: Unable to open given file. Please try a different file."
        elif response == "empty":
            message = "ERROR: The pdf sent is empty, please send a pdf with content."
        # API call
        else:
            message = resumeai.airesponse(response)
            return render_template("index.html", message = message) # return messages for processed text

    return render_template("index.html", message = message) # return messages for errors
if __name__ == "__main__":
    app.run(debug=True) # test