import Singleton

class ModelService(metaclass=Singleton.Singleton):
    Model = None
    InputShape = None

    def Setup(self, modelPath):
        print("Loading model...")
        import tensorflow.keras.models as models
        import os
        modelPath = os.path.join("Models", modelPath)
        self.Model = models.load_model(modelPath)

        self.InputShape = self.Model.layers[0].input_shape



        return

    def Predict(self, x):

        assert self.Model is not None, "Model is not loaded"

        assert x.shape == self.InputShape[1:], f'Invalid image shape: {x.shape}. Expected: {self.InputShape[1:]}'

        x = x.reshape((1,) + x.shape)
        y = self.Model.predict(x)[0]

        return y