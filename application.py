import os 
from flask import Flask, request, redirect, url_for, render_template, send_file, request
from shutil import make_archive
from subprocess import run
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST']) 
def main_page():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        if not os.path.isdir("uploads"):
          os.makedirs('uploads')
        file.save(os.path.join('uploads', filename))
        return redirect(url_for('prediction', filename=filename))
    return render_template('index.html')

@app.route('/prediction/<filename>') 
def prediction(filename):
    def run_diffdock_command(csv_file_location=None, out_dir=None, inference_steps=20, samples_per_complex=40, batch_size=10, actual_steps=18):
        command_string_template = "python -m inference --protein_ligand_csv {csv_file_location} --out_dir {out_dir} --inference_steps {inference_steps} --samples_per_complex {samples_per_complex} --batch_size {batch_size} --actual_steps {actual_steps} --no_final_step_noise"
        command_string = command_string_template.format(csv_file_location=csv_file_location, out_dir=out_dir, inference_steps=inference_steps, samples_per_complex=samples_per_complex, batch_size=batch_size, actual_steps=actual_steps)
        run(command_string, shell=True, check=True)
    if not os.path.isdir("results"):
            os.makedirs('results')
    kwargs = {
        "csv_file_location": os.path.join("uploads", filename),
        "out_dir": os.path.join("results", filename),
        # TODO: other args
    }
    run_diffdock_command(**kwargs)
    zipfilepath = os.path.join(os.getcwd(), filename)
    zipformat = "zip"
    directory = os.path.join("results", filename)
    make_archive(zipfilepath, zipformat, directory)
    strfile = "{path}.{format}".format(path=zipfilepath, format=zipformat)
    return send_file(strfile, as_attachment=True)