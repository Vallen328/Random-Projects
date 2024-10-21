from flask import Flask, render_template, request as req
import requests
from config import HF_API_KEY  

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def Index():
    return render_template("index.html")

@app.route("/Summarize", methods=["GET", "POST"])
def Summarize():
    if req.method == "POST":
        API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        headers = {"Authorization": f"Bearer {HF_API_KEY}"}

        data = req.form["data"]
        maxL = int(req.form["maxL"])
        minL = maxL // 4

        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()

        output = query({
            "inputs": data,
            "parameters": {"min_length": minL, "max_length": maxL},
        })

        if isinstance(output, list) and "summary_text" in output[0]:
            summary = output[0]["summary_text"]
        else:
            summary = "Unable to generate summary. Please try again later."

        return render_template("index.html", result=summary)
    else:
        return render_template("index.html")

if __name__ == '__main__':
    app.debug = True
    app.run()
