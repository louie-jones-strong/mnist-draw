
# Setup
```bash
pip install -r requirements.txt
```

# Usage
To launch the website, begin by starting a Python server from the repository folder:
```bash
# Start Python server (use Python 3)
python -m http.server --cgi 8000
```
Then open a browser and navigate to `http://localhost:8000/`.

## Acknowledgements
This repo is a fork of https://github.com/mco-gh/mnist-draw

Thanks to rhammell for the original Python version and to zackakil for adding support for Tensorflow.js.
In this version I added predicting while you draw, deployed the example UI on Cloud Run (bit.ly/mco-mnist-draw),
and deployed a Colab notebook (bit.ly/mco-mnist-lab) so you can build your own version of this model,
with the UI widget integrated right into the notebook.
