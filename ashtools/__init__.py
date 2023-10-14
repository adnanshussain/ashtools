from tqdm import tqdm
from .common import *

# * Need to put these into proper modules or packages


def convert_pdf_to_raw_text(
    src_pdf_fname,
    src_pdf_path=None,
    save_intermediate_images=False,
    save_intermediate_text=False,
    output_file_name=None,
    no_of_pages_to_process=None,
):
    """
    Convert PDF to raw text using OCR
    :param src_pdf_fname: source PDF file name
    :param src_pdf_path: source PDF file path
    :param save_intermediate_images: save intermediate images
    :param output_file_name: output file name
    :param no_of_pages_to_process: number of pages to process (mostly for debugging)
    """
    try:
        info_log("Converting PDF to raw text using OCR...")
        from pdf2image import convert_from_path

        # end path with a slash
        if src_pdf_path is not None:
            src_pdf_path = (
                src_pdf_path if src_pdf_path.endswith("/") else src_pdf_path + "/"
            )

        # Convert PDF to images
        images = convert_from_path(src_pdf_path + src_pdf_fname)

        if no_of_pages_to_process is not None and no_of_pages_to_process > 0:
            images = images[:no_of_pages_to_process]

        import pytesseract

        # Initialize Tesseract
        pytesseract.pytesseract.tesseract_cmd = (
            "/usr/bin/tesseract"  # Path to your Tesseract executable
        )

        extracted_text = []
        # Extract text from images into a list of strings
        for i, img in tqdm(enumerate(images), total=len(images)):
            debug_log(
                f"Processing page {i+1} of {len(images)} of {src_pdf_path}{src_pdf_fname}"
            )
            if save_intermediate_images:
                with open(f"{src_pdf_fname}-preocr-pg{i+1}.jpg", "wb") as file:
                    img.save(file, format="JPEG")
            text = pytesseract.image_to_string(
                img,
                lang="eng",  # * this should be user defined
                config="--psm 6",  # most efficient for eStatement formats (also tried 11 & 12 & 3)
            )
            extracted_text.append(text)
            extracted_text.append(f"===PGEND===pg-{i+1}===\n")

        # save_intermediate_text = True
        if save_intermediate_text:
            if output_file_name is None:
                output_file_name = f"{src_pdf_fname}-ocred.txt"
            with open(output_file_name, "w") as file:
                file.write("".join(extracted_text))

        return extracted_text

    except Exception as e:
        error_log(e)
        # * Need to implement better trace handling
        # import traceback
        # stack_trace = traceback.
        # error_log(stack_trace)


def _find_all_indices_of_rexps_in_list_of_list_of_words(
    src_list_of_words, word_to_find
):
    """
    Return all the indices of the list where the regular expression is present in the inner list, search using regex
    :param src_list_of_words: source list of words
    :param word_to_find: word to find
    :return: list of indices
    """
    import re

    indices = []
    for i, inner_list in enumerate(src_list_of_words):
        for word in inner_list:
            if re.search(word_to_find, word):
                indices.append(i)
    return indices


def preprocess_hsbc_estatment(src_pdf_fname, src_pdf_path):
    """
    Preprocess HSBC eStatement into only transaction text lines
    :param src_pdf_fname: source PDF file name
    :param src_pdf_path: source PDF file path
    :return: list of words
    """
    raw_text = convert_pdf_to_raw_text(src_pdf_fname, src_pdf_path)
    info_log("Preprocessing HSBC eStatement...")
    result = [
        lines.split(" ")
        for lines in [
            line for page in [page.split("\n") for page in raw_text] for line in page
        ]
    ]  # analyze this !
    start_indices = _find_all_indices_of_rexps_in_list_of_list_of_words(
        result, "FORWARD|CLOSING"
    )
    cleared_for_processing = []

    for index, start_i in tqdm(enumerate(start_indices), total=len(start_indices)):
        import time

        time.sleep(
            0.25
        )  # Gives the impression some heavy duty number crunching is happening. LOL.

        debug_log(f"===== BATCH #{index + 1} =====")
        mid_result = (
            result[start_i : start_indices[index + 1]]
            if index + 1 < len(start_indices)
            else result[start_i:]
        )
        do_not_process_batch = _find_all_indices_of_rexps_in_list_of_list_of_words(
            mid_result, "PGEND"
        )
        if len(do_not_process_batch) == 0:
            # clear batch for processing
            for i in range(start_i, start_indices[index + 1] + 1):
                debug_log(f"{index}, {i}, {result[i]}")
                cleared_for_processing.append(result[i])
        else:
            debug_log(
                f"Skipping batch #{index + 1} as it has a page end marker {mid_result[do_not_process_batch[0]]}"
            )

    cleared_for_processing = [" ".join(words) for words in cleared_for_processing]

    # save cleared_for_processing to a text file
    with open(f"{src_pdf_fname}-cfp.txt", "w") as file:
        file.write("\n".join(cleared_for_processing))

    return cleared_for_processing


def read_text_file_to_list_of_words_per_line(src_text_file_name):
    """
    Read text file and convert each line to a list of words
    :param src_text_file_name: source text file name
    :return: list of words
    """
    with open(src_text_file_name, "r") as file:
        lines = file.readlines()
        words = []
        for line in lines:
            words.append(line.split())
    return words
