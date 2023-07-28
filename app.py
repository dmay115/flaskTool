from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "bug_squish"

debug = DebugToolbarExtension(app)

RESPONSES_KEY = 'responses'

@app.route('/')
def start_session():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template("start.html", title=title, instructions=instructions)

@app.route('/start', methods=['POST'])
def clear_responses():
    session[RESPONSES_KEY] = []
    return redirect("question/0")

@app.route('/question/<int:q_num>')
def question(q_num):
    responses = session.get(RESPONSES_KEY)
    if q_num > len(satisfaction_survey.questions) -1:
        flash("Please only answer provided questions")
        return redirect(f'/question/{len(responses)}')
    if q_num > len(responses):
        flash("Please answer questions in the order they are provided")
        return redirect(f'/question/{len(responses)}')
    question = satisfaction_survey.questions[q_num]
    return render_template("question.html", question=question, number=q_num)

@app.route('/answer/<int:q_num>', methods=["POST"])
def answer(q_num):
    responses = session[RESPONSES_KEY]
    responses.append(request.form["choice"])
    session[RESPONSES_KEY] = responses
    if q_num < len(satisfaction_survey.questions) -1:
        q_num += 1
    else:
        return redirect("/thank")
    return redirect(f"/question/{q_num}")

@app.route('/thank')
def thank():
    return render_template("thank.html")