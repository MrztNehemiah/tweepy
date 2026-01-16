def save_checkpoint(index):
    with open("checkpoint.txt", "w") as checkpoint:
        checkpoint.write(str(index))


def load_checkpoint():
    try:
        with open("checkpoint.txt", "r") as fh:
            # return an int of the index
            return int(fh.read().strip())

    except FileNotFoundError:
        return -1
