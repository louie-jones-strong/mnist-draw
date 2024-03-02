from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import ModelService
import json
import io
import json
import os
import re
import base64
import numpy as np
from PIL import Image

hostName = "localhost"
serverPort = 8080

class ModelServer(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        if path == "/":
            path = "/index.html"
        path = os.path.join("Public", path[1:])

        # get the file extension
        ext = path.split(".")[-1]

        if not os.path.exists(path):
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<h1>404: Not Found</h1>", "utf-8"))
            return

        try:
            with open(path, 'rb') as file:
                content = file.read()

            self.send_response(200)
            self.send_header("Content-type", f"text/{ext}")
            self.end_headers()

            self.wfile.write(content)
        except Exception as e:
            self.wfile.write(bytes(f"<h1>500: Internal Server Error: {e}</h1>", "utf-8"))

        return

    def do_POST(self):
        res = {"result": 0,
            "data": [],
            "error": ''}

        try:

            # Get post data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_data = post_data.decode('utf-8')

            img_str = re.search(r'base64,(.*)', post_data).group(1)
            image_bytes = io.BytesIO(base64.b64decode(img_str))
            img = Image.open(image_bytes)
            # resize image to 28x28
            img = img.resize((28, 28))
            x = np.array(img)[:,:,0:1]

            # Normalize and invert pixel values
            x = (255 - x) / 255.


            prediction = self.Predict(x)

            res['result'] = 1
            res['data'] = [float(num) for num in prediction]

        except Exception as e:
            res['error'] = str(e)
            raise e

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(res), "utf-8"))
        return

    def Predict(self, x):
        modelService = ModelService.ModelService()
        prediction = modelService.Predict(x)
        return prediction



if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), ModelServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    modelService = ModelService.ModelService()
    modelService.Setup()

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")