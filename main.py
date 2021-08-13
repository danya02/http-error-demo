from flask import Flask, abort, make_response

app = Flask(__name__)

def verbatim(*args, **kwargs):
    response = make_response(*args, **kwargs)
    response.headers['X-Error-Verbatim'] = 'yes'
    return response


def body_and_error(title, body=None):
    response = make_response( f'<h1>{title}</h1>' + (f'<p>{body}</p>' if body else '') )
    response.headers['X-Errorpage-Title'] = title
    if body:
        response.headers['X-Errorpage-Body'] = body
    return response


@app.route('/<int:error_id>')
def error(error_id):
    if error_id < 400 or error_id >= 600:
        return verbatim(body_and_error("Error codes must be between 400 and 599, inclusive.")), 404
    return 'error '+str(error_id), error_id
