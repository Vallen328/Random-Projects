from flask import Flask, render_template, request as req
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def Index():
    return render_template("index.html")

@app.route("/Summarize", methods=["GET", "POST"])
def Summarize():
    if req.method == "POST":
        API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        headers = {"Authorization": f"Bearer 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"}

        data = req.form["data"]
        maxL = int(req.form["maxL"])
        minL = maxL // 4

        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()

        # Call the Hugging Face API and check the response structure
        output = query({
            "inputs": data,
            "parameters": {"min_length": minL, "max_length": maxL},
        })

        # Handle possible errors or unexpected responses
        if isinstance(output, list) and "summary_text" in output[0]:
            summary = output[0]["summary_text"]
        else:
            # Gracefully handle the case where the API doesn't return the expected data
            summary = "Unable to generate summary. Please try again later."

        return render_template("index.html", result=summary)
    else:
        return render_template("index.html")

if __name__ == '__main__':
    app.debug = True
    app.run()
