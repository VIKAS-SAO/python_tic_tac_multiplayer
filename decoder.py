import pickle

def decoder(d):
    return pickle.loads(d)


def encoder(d):
    return pickle.dumps(d)

    