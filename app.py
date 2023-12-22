from flask import Flask, render_template, request
from rasa.core.agent import Agent
from rasa.shared.constants import DEFAULT_ACTIONS_PATH

app = Flask(__name__)

# Load Rasa model
agent = Agent.load("rasa/rasa.py")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_message = request.form["user_message"]
    response = agent.handle_text(user_message)
    return {"response": response[0]["text"]}

if __name__ == "__main__":
    app.run(debug=True)
