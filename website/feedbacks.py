from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Feedback
from . import db

feedbacks = Blueprint('feedbacks', __name__)

@feedbacks.route('/', methods=['GET', 'POST'])
@login_required
def feedback_page():
    if request.method == 'POST':
        feedback_text = request.form.get('feedback')
        if feedback_text:
            new_feedback = Feedback(
                text=feedback_text,
                user_id=current_user.id
            )
            db.session.add(new_feedback)
            db.session.commit()
            flash("Thank you for your feedback!", category='success')
            return redirect(url_for('views.home'))
        else:
            flash("Feedback cannot be empty.", category='error')
    return render_template('feedback_form.html', user=current_user)