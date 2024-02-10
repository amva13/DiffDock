## (WIP) Encode ICP Hakcathon submission
Building a canister for the diffdock model
## Original instructions
For instructions to setup conda environment, please see README-original.md or visit the original repo.

After completing your environment setup, run the following for this server to work.

    conda install -n diffdock flask werkzeug

Note: I recommend actually installing the esm package references in the original README via conda to avoid dependency issues running locally.

    conda install -c conda-forge fair-esm

Or (from outside conda environment)
```
conda install -n diffdock -c conda-forge fair-esm
```
After these, you can start your flask server by running the following inside your conda environment
```
flask --app application run
```
