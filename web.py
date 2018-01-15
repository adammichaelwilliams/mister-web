import os
from flask import Flask, request, redirect, url_for, send_from_directory, render_template, send_file, abort
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/Users/adam/mister-web/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', defaults={'req_path': ''}, methods=['POST'])
@app.route('/<path:req_path>upload', methods=['POST'])
def upload_file(req_path):
    # check if the post request has the file part
    if 'file' not in request.files:
	flash('No file part')
	return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
	flash('No selected file')
	return redirect(request.url)
    if file and allowed_file(file.filename):
	filename = secure_filename(file.filename)
	print filename
	file.save(os.path.join(app.config['UPLOAD_FOLDER'] + req_path, filename))
	print "sending redirect"
	return redirect(req_path)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def dir_listing(req_path):
    BASE_DIR = '/Users/adam/mister-web'

    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    directory = '/' + req_path.rstrip('/') + '/' if req_path else '/'
    print directory

    #directory = os.path.join(BASE_DIR, req_path)

    # Show directory contents
    files = os.listdir(abs_path)
    print files
    return render_template('index.html', files=files, directory=directory)
