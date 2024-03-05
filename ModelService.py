import Singleton

class ModelService(metaclass=Singleton.Singleton):
    Model = None
    InputShape = None
    UseNoisyImages = False

    def Setup(self, modelPath):
        print("Loading model...")
        import tensorflow.keras.models as models
        import os
        import numpy as np
        self.Np = np
        modelPath = os.path.join("Models", modelPath)
        self.Model = models.load_model(modelPath)

        self.InputShape = self.Model.layers[0].input_shape



        return

    def Predict(self, x):

        assert self.Model is not None, "Model is not loaded"

        assert x.shape == self.InputShape[1:], f'Invalid image shape: {x.shape}. Expected: {self.InputShape[1:]}'

        if self.UseNoisyImages:

            noisyImages = [x]
            num = 10
            for j in range(1, num+1):
                noisyImage = x + self.Np.random.normal(0, j/num, x.shape)
                noisyImage = noisyImage / self.Np.max(noisyImage)
                noisyImages.append(noisyImage)

            for j in range(1, num+1):
                noisyImage = x - self.Np.random.normal(0, j/num, x.shape)
                noisyImage = noisyImage / self.Np.max(noisyImage)
                noisyImages.append(noisyImage)

            noisyImages = self.Np.array(noisyImages)

            modelOutput = self.Model.predict(noisyImages)
            modelOutput = self.Np.sum(modelOutput, axis=0)
            y = modelOutput / self.Np.sum(modelOutput)

        else:
            x = x.reshape((1,) + x.shape)
            y = self.Model.predict(x)[0]

        return y