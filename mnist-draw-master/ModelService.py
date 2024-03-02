import Singleton


class ModelService(metaclass=Singleton.Singleton):
    Model = None
    InputShape = None

    def GetModel(self):

        if self.Model is None:
            print("Loading model...")
            import tensorflow.keras.models as models
            self.Model = models.load_model('model.keras')

            self.InputShape = self.Model.layers[0].input_shape


        return self.Model

    def Predict(self, x):
        model = self.GetModel()

        assert x.shape == self.InputShape[1:], f'Invalid image shape: {x.shape}. Expected: {self.InputShape[1:]}'

        x = x.reshape((1,) + x.shape)

        y = model.predict(x)[0]
        return y