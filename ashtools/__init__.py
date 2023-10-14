from tqdm import tqdm
from .common import *

# * Need to put these into proper modules or packages


def convert_pdf_to_raw_text(
    src_pdf_fname,
    src_pdf_path=None,
    save_intermediate_images=False,
    output_file_name=None,
    no_of_pages_to_process=None,
):
    """
    Convert PDF to raw text using OCR
    :param src_pdf_fname: source PDF file name
    :param src_pdf_path: source PDF file path
    :param save_intermediate_images: save intermediate images
    :param output_file_name: output file name
    :param no_of_pages_to_process: number of pages to process (mostly for pdf to txt output sampling/debugging)
    """
    try:
        info_log("Converting PDF to raw text...")
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

        save_intermediate_text = True
        if save_intermediate_text:
            if output_file_name is None:
                output_file_name = f"{src_pdf_fname}-ocred.txt"
            with open(output_file_name, "w") as file:
                file.write("".join(extracted_text))
    except Exception as e:
        error_log(e)
        # * Need to implement better trace handling
        # import traceback
        # stack_trace = traceback.??
