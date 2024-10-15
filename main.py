from pypdf import PdfReader, PdfWriter
import questionary
import os
import sys
import logging


logger = logging.getLogger(__name__)


if __name__ == "__main__":
    file_path_choices = [f for f in os.listdir("./pdf_files/") if f.lower().endswith(".pdf")]

    if not file_path_choices:
        logger.warning("PDF files not found!")
        sys.exit()

    merger = PdfWriter()
    output = open("./pdf_files/merged-output.pdf", "wb")

    first_file_path = questionary.select(
        "Which file will be processed straight?",
        choices=file_path_choices,
    ).ask()
    
    second_file_path = questionary.select(
        "Which file will be processed inside out?",
        choices=file_path_choices,
    ).ask()

    first_file = open(f"./pdf_files/{first_file_path}", "rb")
    first_file_pdf_reader = PdfReader(first_file)
    second_file = open(f"./pdf_files/{second_file_path}", "rb")
    second_file_pdf_reader = PdfReader(second_file)

    first_file_pages = first_file_pdf_reader.get_num_pages()
    second_file_pages = second_file_pdf_reader.get_num_pages()

    if second_file_pages > first_file_pages or first_file_pages > second_file_pages + 1:
        logger.warning("Only PDFs with same amount of pages or the first one with one page more than the second one are the allowed scenarios. Exiting...")
        sys.exit()

    for page_idx in range(1, first_file_pages + 1):
        merger.append(fileobj=first_file, pages=(page_idx - 1, page_idx))
        reverse_idx = second_file_pages + 1 - page_idx
        if reverse_idx > 0:
            merger.append(fileobj=second_file, pages=(reverse_idx - 1, reverse_idx))

    for page in merger.pages:
        page.compress_content_streams(level=9)

    merger.write(output)
    merger.close()
    output.close()
    logger.info("Process completed!!")
    
    