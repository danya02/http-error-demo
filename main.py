from flask import Flask, abort, make_response, render_template
import yaml
import traceback

app = Flask(__name__)

def get_errors():
    with open('/ERRORS.yml') as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)

    endpoints = []
    for item in data:
        if isinstance(item, str):
            code = int(item[:3])
            endpoints.append( (item, f'/{code}') )
        else:
            endpoints.append( (item['name'], item['url']) )
    return endpoints

def verbatim(*args, **kwargs):
    response = make_response(*args, **kwargs)
    response.headers['X-Error-Verbatim'] = 'yes'
    return response


def body_and_error(title, body=None):
    response = make_response( f'<h1>{title}</h1>' + (f'<p>{body}</p>' if body else '') )
    response.headers['X-Errorpage-Title'] = title
    if body:
        response.headers['X-Errorpage-Body'] = body
    return verbatim(response)

@app.route('/')
def index():
    try:
        errors = get_errors()
    except:
        err = traceback.format_exc()
        return body_and_error("Error list misconfigured!", "<p>You can still test errors by appending <code>/(error_code)</code> to this address.</p><p>Error code:</p><p><code>" + err.replace('\n', '<br>') + "</code></p>"), 500

    return render_template('index.html', errors=errors)


@app.route('/<int:error_id>')
def error(error_id):
    if error_id < 400 or error_id >= 600:
        return body_and_error("Error codes must be between 400 and 599, inclusive."), 404
    return 'error '+str(error_id), error_id
