from flask import Blueprint, render_template, request, flash, redirect
from .models import Feedback
from . import db

feedbacks = Blueprint('feedbacks', __name__)

@feedbacks.route('/', methods=['GET', 'POST'])
def feedback_page():
    if request.method == 'POST':
        feedback_text = request.form.get('feedback')
        if feedback_text:
            new_feedback = Feedback(text=feedback_text)
            db.session.add(new_feedback)
            db.session.commit()
            flash("Thank you for your feedback!", category='success')
            return redirect('/')
        else:
            flash("Feedback cannot be empty.", category='error')
    return render_template('feedback_form.html')