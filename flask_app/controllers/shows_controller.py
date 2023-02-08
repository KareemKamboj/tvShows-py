from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.user_model import User
from flask_app.models.shows_model import Show

@app.route("/shows/new")
def new_show_form():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('show_new.html')

@app.route("/shows/create", methods=['POST'])
def process_show():
    if 'user_id' not in session:
        return redirect('/')
    if not Show.validator(request.form):
        return redirect('/shows/new')
    data = {
        **request.form,
        'user_id': session['user_id']
    }
    id = Show.create(data)
    return redirect(f'/shows/{id}')

@app.route("/shows/<int:id>")
def show_show(id):
    show = Show.get_by_id({'id':id})
    user_data = {
        'id': session['user_id']
    }
    user = User.get_by_id(user_data)
    return render_template("show_one.html", user=user, show=show)

@app.route("/shows/<int:id>/delete")
def del_show(id):
    if 'user_id' not in session:
        return redirect('/')
    show = Show.get_by_id({'id':id})
    if not int(session['user_id']) == show.user_id:
            flash("Whoa there, thats not yours, hands off")
            return redirect('/welcome')
    show.delete({'id':id})
    return redirect('/welcome')

@app.route("/shows/<int:id>/edit")
def edit_show(id):
    if 'user_id' not in session:
        return redirect('/')
    show = Show.get_by_id({'id':id})
    if not int(session['user_id']) == show.user_id:
        flash("Whoa there, thats not yours, hands off")
        return redirect('/welcome')
    show = Show.get_by_id({'id':id})
    return render_template("show_edit.html", show=show)

@app.route("/shows/<int:id>/update", methods=['POST'])
def update_show(id):
    if 'user_id' not in session:
        return redirect('/')
    show = Show.get_by_id({'id':id})
    if not int(session['user_id']) == show.user_id:
        flash("Whoa there, thats not yours, hands off")
        return redirect('/welcome')
    if not Show.validator(request.form):
        return redirect(f'/shows/{id}/edit')
    data = {
        **request.form,
        'id':id
    }
    Show.update(data)
    return redirect("/welcome")