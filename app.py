from flask import Flask, redirect, render_template, request, flash, session
from surveys import Survey, Question, satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'something'
"""debug = DebgugToolbarExtension(app)"""

some_list = [0]
@app.route('/')
def root_route():
    some_list.clear()
    some_list.append(0)
    if len(session['responses']) > 0:
        session['responses'] = {}
    return render_template('index.html', survey_title = satisfaction_survey.title, the_instructions = satisfaction_survey.instructions)

@app.route('/question/<number>')
def question_route(number):
    curr_question = some_list.pop(len(some_list)-1)
    session['responses'] = {}
    if((curr_question) == int(number)):
        some_list.append(curr_question+1)
        if(int(number) < len(satisfaction_survey.questions)):
            return render_template("question0.html", question = satisfaction_survey.questions[int(number)].question, mod_choices = mod_list_make_dict(satisfaction_survey.questions[int(number)].choices), choices = satisfaction_survey.questions[int(number)].choices, next_question = int(number)+1)
        else:
            return render_template("thank_you.html", questions =satisfaction_survey.questions)
    else:
        flash("Skipping answers or changing answers is not allowed. Please start the survey over.")
        return redirect('/')

@app.route('/question/<number>', methods=["POST"])
def answer_route(number):
    ses_dict = make_key_into_number(session['responses'])
    ses_dict[int(number)-1] = remove_underscores(request.form['answer'])
    session['responses'] = ses_dict
    curr_question = some_list.pop(len(some_list)-1)
    if(curr_question == int(number)):
        some_list.append(curr_question+1)
        if(int(number) < len(satisfaction_survey.questions)):
            mod_list = mod_list_make_dict(satisfaction_survey.questions[int(number)].choices)
            return render_template("question0.html", question = satisfaction_survey.questions[int(number)].question, mod_choices = mod_list, choices = satisfaction_survey.questions[int(number)].choices, next_question = int(number)+1)
        else:
            return redirect("/thanks")
    else:
        flash("Skipping answers or changing answers is not allowed. Please start the survey over.")
        return redirect('/')
        
@app.route('/thanks')
def thank_you():
    ses_dict = make_key_into_number(session['responses'])
    session['responses'] = ses_dict
    return render_template("thank_you.html", questions =satisfaction_survey.questions, survey_title = satisfaction_survey.title)

def mod_choices_list(choices_list):
    ret_list = []
    for item in choices_list:
        ret_list.append(sentence_into_word(item))
    return ret_list

def mod_list_make_dict(a_list):
    count = 0
    mod_list = mod_choices_list(a_list)
    a_dict = {}
    for item in mod_list:
        a_dict[count] = item
        count += 1
    return a_dict

def sentence_into_word(word):
    a_list = word.split(' ')
    ret_string = ''
    count = 1
    stop = len(a_list) - 1
    for item in a_list:
        if count <= stop:
            ret_string += item + "_"
            count += 1
        else:
            ret_string += item
    return ret_string

def remove_underscores(word):
    a_list = word.split("_")
    ret_string = ""
    count = 1
    stop = len(a_list) - 1
    for item in a_list:
        if count <= stop:
            ret_string += item + " "
            count +=1
        else:
            ret_string += item
    return ret_string
def make_key_into_number(arg_dict):
    new_dict = {}
    count = 0
    for val in arg_dict.values():
        new_dict[count] = val
        count += 1
    return new_dict