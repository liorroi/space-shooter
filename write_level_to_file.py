import pickle
import enemy


def write_level(level, file_path):
    with open(file_path, 'wb') as file_1:
        pickle.dump(level, file_1, protocol=pickle.HIGHEST_PROTOCOL)


def read_level(level, file_path):
    with open(file_path, 'rb') as file:
        return pickle.load(file)


