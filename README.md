For instructions to setup conda environment, please see README-original.md or visit the original repo.

After completing your environment setup, run the following for this server to work.

    conda install -n diffdock flask werkzeug

Note: I recommend actually installing the esm package references in the original README via conda to avoid dependency issues running locally.

    conda install -c conda-forge fair-esm

After these, you can start your flask server by running
```
flask --app application run
```