from flask import render_template, request, redirect, url_for, flash, Response
from flask import Blueprint
from flask import session

from flask_mongoengine import MongoEngine
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

# stdlib
from datetime import datetime

from .. import app, bcrypt, client
from ..forms import (PlayerCommentForm)
from ..models import User, Comments, load_user
from ..utils import current_time

football = Blueprint('football', __name__)


@football.route('/players/<player_id>', methods=['GET', 'POST'])
def player_detail(player_id):
    r = client.getPlayerByID(player_id)

    if type(r) == dict:
        return render_template('player_detail.html', error_msg=r['error'])

    form = PlayerCommentForm()
    if form.validate_on_submit():
        comment = Comments(
            commenter=load_user(current_user.username),
            content=form.text.data,
            draftRound=form.draftRound.data,
            playAgain=form.playAgain.data,
            date=current_time(),
            player_id=player_id,
            player_name=r.fullname
        )

        comment.save()

        return redirect(request.path)

    comm= Comments.objects(player_id=player_id)

    print(current_user.is_authenticated)

    return render_template('player_detail.html', form=form, player=r, reviews=comm)

@football.route('/team-results/<query>', methods=['GET'])
def team_results(query):
    if query != 'ALL':
        r =client.get_players_by_team(query)
    else:
        r =  client.getAll()

    if type(r) == dict:
        return render_template('query.html', error_msg=r['error'])

    return render_template('query.html', results=r)






