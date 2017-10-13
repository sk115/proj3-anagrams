"""
Flask web site with vocabulary matching game
(identify vocabulary words that can be made 
from a scrambled string)
"""

import flask
import logging

# Our own modules
from letterbag import LetterBag
from vocab import Vocab
from jumble import jumbled
import config

###
# Globals
###
app = flask.Flask(__name__)

CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY  # Should allow using session variables

# One shared 'Vocab' object, read-only after initialization,
# shared by all threads and instances.  Otherwise we would have to
# store it in the browser and transmit it on each request/response cycle,
# or else read it from the file on each request/responce cycle,
# neither of which would be suitable for responding keystroke by keystroke.

WORDS = Vocab(CONFIG.VOCAB)

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    """
    The main page of the application
    Get the global wordlist and set session
    variables, then render the page appropriately
    """
    flask.g.vocab = WORDS.as_list()
    flask.session["target_count"] = min(
        len(flask.g.vocab), CONFIG.SUCCESS_AT_COUNT)
    flask.session["jumble"] = jumbled(
        flask.g.vocab, flask.session["target_count"])
    flask.session["matches"] = []
    app.logger.debug("Session variables have been set")
    assert flask.session["matches"] == []
    assert flask.session["target_count"] > 0
    app.logger.debug("At least one seems to be set correctly")
    return flask.render_template('vocab.html')

@app.route("/_check")
def check():
    """
    User has typed text into the attempt input field
    which sends the text as an AJAX Request
    We evaluate if the text is a word that can be
    formed from the jumble and is on the vocabulary list,
    and if so respond with a flag indicating the new entry
    If we have enough matches to win, we skip to
    sending a flag to redirect to the success page
    """

    app.logger.debug("Received Entry")

    # Receive input to test via AJAX Request
    text = flask.request.args.get("text", type=str)
    jumble = flask.session["jumble"]
    matches = flask.session.get("matches", [])  # Default to empty list
    is_new_match = False # Assume it's not new

    in_jumble = LetterBag(jumble).contains(text)
    matched = WORDS.has(text)

    # Respond appropriately
    if matched and in_jumble and not (text in matches):
        # Cool, they found a new word
        matches.append(text)
        flask.session["matches"] = matches
        is_new_match = True

    # Other Cases
    # elif text in matches:
    #   already found this word
    # elif not matched:
    #   word not in our list
    # elif not in_jumble:
    #     has letters not in the letterbag
    # else:
    #     app.logger.debug("This case shouldn't happen!")
    #     assert False  # Raises AssertionError

    # Flag for redirect if complete, return matched text otherwise
    if len(matches) >= flask.session["target_count"]:
        return flask.jsonify(success=True)
    else:
        return flask.jsonify(match=text, is_new_match=is_new_match, success=False)

@app.route("/success")
def success():
    """Redirect Page for Game Completion"""
    return flask.render_template('success.html')

###

###################
#   Error handlers
###################


@app.errorhandler(404)
def error_404(e):
    app.logger.warning("++ 404 error: {}".format(e))
    return flask.render_template('404.html'), 404


@app.errorhandler(500)
def error_500(e):
    app.logger.warning("++ 500 error: {}".format(e))
    assert not True  # I want to invoke the debugger
    return flask.render_template('500.html'), 500


@app.errorhandler(403)
def error_403(e):
    app.logger.warning("++ 403 error: {}".format(e))
    return flask.render_template('403.html'), 403


####

if __name__ == "__main__":
    if CONFIG.DEBUG:
        app.debug = True
        app.logger.setLevel(logging.DEBUG)
    app.logger.info("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
