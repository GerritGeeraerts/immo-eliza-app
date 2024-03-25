import pickle


def load_model_from_pickle(path: str):
    model = None
    with open(path, 'rb') as file:
        model = pickle.load(file)
    return model



