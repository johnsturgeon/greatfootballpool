""" Passenger wsgi file, this is the main 'routing' logic for
    The Great Football Pool website
"""
import os
import sys
dirname = os.path.dirname(os.path.abspath(__file__))
DOT_ENV_PATH = os.path.normpath(os.path.join(dirname, '../conf/.env'))
INTERP = os.path.normpath(os.path.join(dirname, '../env/bin/python'))

if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)
# pylint: disable=wrong-import-position
import sentry_sdk  # noqa: E402
from flask import Flask, session, request, abort  # noqa: E402
from flask import render_template, redirect, url_for, g  # noqa: E402
from sentry_sdk.integrations.flask import FlaskIntegration  # noqa: E402
from bson import ObjectId  # noqa: E402
from tgfp import TGFP, TGFPPick  # noqa: E402
from dotenv import load_dotenv  # noqa: E402

load_dotenv(dotenv_path=DOT_ENV_PATH)

DEBUG = bool(os.getenv('DEBUG'))
LOGGING_DIR = os.getenv('LOGGING_DIR')

if DEBUG:
    print("DEBUG MODE")
    from flask_profile import Profiler

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_APP_SECRET_KEY')

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[FlaskIntegration()],
    traces_sample_rate=0.0
)

if DEBUG:
    Profiler(app)
    app.config["flask_profiler"] = {
        "storage": {
            "engine": "mongodb",
        },
        "profile_dir": LOGGING_DIR
    }


@app.before_request
def before_request():
    """ This runs before every single request to make sure the user is logged in """
    if os.path.exists("maintenance"):
        abort(503)
    if 'static' not in request.path and '_profile' not in request.path:
        tgfp = None
        if not hasattr(g, 'tgfp'):
            tgfp = TGFP()
        g.current_week = tgfp.current_week()
        g.tgfp = tgfp


@app.route('/')
def index():
    """ default route / -> home """
    return redirect(url_for('home'))


@app.route('/home')
def home():
    """ Home page route for the football pool """
    if 'player_name' not in session:
        session['login_status'] = 'not logged in'
        return redirect(url_for('login'))

    return render_template('home.j2', home_page_text=g.tgfp.home_page_text())


@app.route('/picks')
def picks():
    """ Picks page route """
    if 'player_name' not in session:
        session['login_status'] = 'not logged in'
        return redirect(url_for('login'))

    tgfp = g.tgfp
    player_email = session['player_email']
    player = tgfp.find_players(player_email=player_email)[0]
    all_player_picks = tgfp.find_picks(week_no=g.current_week, player_id=player.id)
    pick = None
    if all_player_picks:
        return render_template(
            'error_picks.j2',
            error_messages=[
                "Sorry, you can't change your picks.  If you think this is a problem, contact John"
                ],
            goto_route='allpicks')

    games = tgfp.find_games(week_no=g.current_week, ordered_by='start_time')
    valid_games = []
    started_games = []
    for game in games:
        if game.game_status == 'pregame':
            valid_games.append(game)
        else:
            started_games.append(game)
    valid_lock_teams = []
    valid_upset_teams = []
    for game in valid_games:
        valid_upset_teams.append(tgfp.find_teams(team_id=game.underdog_team_id)[0])
        valid_lock_teams.append(tgfp.find_teams(team_id=game.home_team_id)[0])
        valid_lock_teams.append(tgfp.find_teams(team_id=game.road_team_id)[0])
    valid_lock_teams.sort(key=lambda x: x.long_name, reverse=False)
    valid_upset_teams.sort(key=lambda x: x.long_name, reverse=False)
    return render_template(
        'picks.j2',
        valid_games=valid_games,
        started_games=started_games,
        valid_lock_teams=valid_lock_teams,
        valid_upset_teams=valid_upset_teams,
        tgfp=tgfp,
        player=player,
        pick=pick
    )


# pylint: disable=too-many-locals
@app.route('/picks_form', methods=['POST'])
def picks_form():
    """ This is the form route that handles processing the form data from the picks page """
    tgfp = g.tgfp
    week_no = g.current_week
    if 'player_email' not in session:
        error_msg = "Your session timed out, please log out and log\
                     back in again -- if the problem persists, contact John"
        return render_template('error_picks.j2', error_messages=error_msg, goto_route='picks')

    player_email = session['player_email']
    player = tgfp.find_players(player_email=player_email)[0]
    games = tgfp.find_games(week_no=week_no, ordered_by='start_time')

    # now get the form variables
    lock_id = request.form["lock"]
    upset_id = request.form["upset"]
    pick_detail = []
    for game in games:
        print("Game")
        key = "game_%s" % game.id
        if key in request.form:
            winner_id = request.form[key]
            print("winner_id " + winner_id)
            item = {
                "game_id": game.id,
                "winner_id": ObjectId(winner_id)
            }
            pick_detail.append(item)

    # Below is where we check for errors
    error_messages = get_error_messages(pick_detail, games, upset_id, lock_id)
    if error_messages:
        return render_template('error_picks.j2', error_messages=error_messages, goto_route='picks')

    player_pick = None
    player_picks = tgfp.find_picks(player_id=player.id, week_no=week_no)
    if player_picks:
        player_pick = player_picks[0]
    if not player_pick:
        player_pick = TGFPPick(tgfp=tgfp, data=None)

    player_pick.player_id = player.id
    player_pick.week_no = int(week_no)
    player_pick.lock_team_id = ObjectId(lock_id)
    if upset_id:
        player_pick.upset_team_id = ObjectId(upset_id)
    else:
        player_pick.upset_team_id = None

    player_pick.pick_detail = pick_detail
    player_pick.save()

    return render_template('picks_form.j2')
# pylint: enable=too-many-locals


@app.route('/allpicks', defaults={'week_no': None})
@app.route('/allpicks/<int:week_no>')
def allpicks(week_no=None):
    """ route for the 'allpicks' page """
    tgfp = g.tgfp
    if 'player_name' not in session:
        session['login_status'] = 'not logged in'
        return redirect(url_for('login'))

    picks_week_no = g.current_week
    if week_no:
        picks_week_no = week_no
    player_email = session['player_email']
    active_players = tgfp.find_players(
        player_active=True,
        ordered_by='total_points',
        reverse_order=True)
    player = tgfp.find_players(player_email=player_email)[0]
    games = tgfp.find_games(week_no=picks_week_no, ordered_by='start_time')
    return render_template(
        'allpicks.j2',
        games=games,
        active_players=active_players,
        tgfp=tgfp,
        player=player,
        week_no=picks_week_no)


@app.route('/standings')
def standings():
    """ route for the 'standings' page """
    if 'player_name' not in session:
        session['login_status'] = 'not logged in'
        return redirect(url_for('login'))

    active_players = g.tgfp.find_players(
        player_active=True,
        ordered_by="total_points",
        reverse_order=True)
    return render_template(
        'standings.j2',
        active_players=active_players)


# pylint: disable=missing-function-docstring
@app.route('/rules')
def rules():
    return render_template('rules.j2')


@app.route('/picks_form_static')
def picks_form_static():
    return render_template('picks_form.j2')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'player_name' in session:
        return redirect(url_for('home'))

    if request.method != 'POST':
        return render_template('login.j2')

    tgfp = g.tgfp
    players = tgfp.find_players(player_email=request.form['email'])
    if not players:
        session.clear()
        session['login_status'] = 'incorrect login'
        return redirect(url_for('login'))

    tgfp_player = players[0]
    if tgfp_player.password != request.form['password']:
        session.clear()
        session['login_status'] = 'incorrect login'
        return redirect(url_for('login'))

    session['login_status'] = 'logged in'
    session['player_name'] = tgfp_player.first_name + ' ' + tgfp_player.last_name
    session['player_email'] = tgfp_player.email
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session.clear()
    g.current_week = None
    g.tgfp = None
    app.secret_key = os.urandom(32)
    return redirect(url_for('home'))


@app.errorhandler(503)
def error_503(error):
    # pylint: disable=unused-argument
    assert error
    return "The Great Football Pool is undergoing some maintenance right now, we'll be back soon!"


# pylint: enable=missing-function-docstring
def get_error_messages(pick_detail, games, upset_id, lock_id):
    """
     Get Error Messages
    Args:
        pick_detail: list of all the picks details
       games: all the current week's games
       upset_id: team_id of the upset team
       lock_id: lock_id of the lock team
    Returns:
        error_message array (empty array if none)
    """
    errors = []
    if len(pick_detail) != len(games):
        errors.append("You missed a pick")
    if not lock_id:
        errors.append("You missed your lock.  (You must choose a lock)")
    for game in games:
        if upset_id:
            if game.favorite_team_id == ObjectId(upset_id):
                errors.append("You cannot pick a favorite as your upset")
    if upset_id:
        pick_is_ok = False
        for pick_item in pick_detail:
            if upset_id == str(pick_item['winner_id']):
                pick_is_ok = True

        if not pick_is_ok:
            errors.append("You cannot choose an upset that you didn't choose as a winner")

    return errors
