from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Flask app running on AWS EKS using Jenkins, Helm and ArgoCD!"

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
