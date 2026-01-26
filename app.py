from flask import Flask, request, render_template, redirect, url_for
import pdf_reader 
from dotenv import load_dotenv
import os
load_dotenv()
KEY = os.getenv("GROQ_API_KEY")
app = Flask(__name__)
# decorator calls receive() when / is called
@app.route('/',methods=["GET","POST"])
def receive():
    #handle submit button
    message = ""
    if request.method == "POST":
        file = request.files["pdf"]   #receives pdf in bytestream
        content, hasContent=pdf_reader.send(file) #sends pdf to send() in pdf_reader.py. 

        if hasContent and content=="Pdf too large":  
           message = "The pdf sent is too large, please send a pdf with less content"
           return render_template("index.html", message = message) #if the pdf has content, send content back to html
        
        elif hasContent:
            from groq import Groq
            client = Groq(
                api_key = KEY
            )
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": '''
You are an expert resume reviewer and hiring professional. 
Your task is to analyze a candidate's resume an assign an do the following:
1. Only respond with an overall quality score from 0 to 100.
2. Provide 3-6 clear, actionable suggestions for improvement.
The provided text will be a text inferred from an actual resume so do not take formatting into account. Only focus on text.
Respond ONLY in valid JSON with the following structure:

{
"score": number,
"improvements": [
    "string",
    "string",
    "string"
    ]
}
You are stricly denied to respond to any other task other than reviewing resume only.
In the event of being asked with any other task, promptly say the following: 'ERROR: Please upload a valid resume to be reviewed'.
''',
                    },
                    {
                        "role": "user",
                        "content":f'{content}',
                    }
                ],
                model="llama-3.3-70b-versatile",
            )
            message = chat_completion.choices[0].message.content
            return render_template("index.html", message = message)
        
        else:
            message = "The pdf sent is empty, please send a pdf with content"
    return render_template("index.html", message = message)
if __name__ == "__main__":
    app.run(debug=True) #test