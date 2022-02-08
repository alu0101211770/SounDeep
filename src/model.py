from keras.models import model_from_json

def load_model(json, weights):
  model = model_from_json(open(json).read())
  model.load_weights(weights)
  return model