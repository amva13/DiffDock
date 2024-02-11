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

    
@app.route('/icp/demo', methods=['GET'])
def icp_demo():
    def run_diffdock_command(pdb_file_location=None, out_dir=None, inference_steps=20, samples_per_complex=1, batch_size=32, actual_steps=18):
        command_string_template = "python -m inference --protein_path {pdb_file_location} --out_dir {out_dir} --inference_steps {inference_steps} --samples_per_complex {samples_per_complex} --batch_size {batch_size} --actual_steps {actual_steps} --no_final_step_noise"
        command_string = command_string_template.format(pdb_file_location=pdb_file_location, out_dir=out_dir, inference_steps=inference_steps, samples_per_complex=samples_per_complex, batch_size=batch_size, actual_steps=actual_steps)
        run(command_string, shell=True, check=True)
    data_dirpath = os.path.join(os.getcwd(), "data")
    pdb_filepath = os.path.join(data_dirpath, "1a0q/1a0q_protein_processed.pdb")
    if not os.path.isdir("results"):
        os.makedirs('results')
    run_diffdock_command(pdb_filepath, out_dir=os.path.join("results", "icp-demo"))
    res_dir = os.path.join("results", "icp-demo")
    complexes = os.listdir(res_dir)
    file_contents = []
    for dir in complexes:
        dirp = os.path.join(res_dir, dir)
        files = os.listdir(dirp)
        for file in files:
            filep = os.path.join(dirp, file)
            with open(filep, "r") as f:
                file_contents.append(f.read())
    # Join all the file contents into a single string.
    file_string = "\n".join(file_contents)

    # Print the file string.
    print(file_string)
    return file_string
    