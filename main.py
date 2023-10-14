if __name__ == "__main__":
    from ashtools import *

    # change_log_level(logging.DEBUG)

    print("Yo VIP.")
    preprocess_hsbc_estatment(
        "Aug 23.pdf", "/home/ash/projects/ashtools-io/raw_datasets/hsbc"
    )
