import json, os, base64

import pagerlib

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.print_page_options import PrintOptions

import merge

def doConvert(bookId, session):

    print("Loading ChromeDriver")
    opts = ChromeOptions()
    #opts.browser_version = 114
    #opts.add_argument("--headless")
    #opts.add_argument("--kiosk-printing")
    #opts.add_argument("--print-to-pdf")
    driver = webdriver.Chrome(options=opts)

    if (not os.path.exists(os.path.join("output", bookId))):
        print("Output folder does not exist. Please run the download.py script first.")
        exit()

    print("Opening pager.json file")
    pagerfile_path = pagerlib.get_pager_file(bookId, session="")
    if (pagerfile_path is None):
        print("Could not find pager file")
        exit(1)
    with open(pagerfile_path, "r") as pagerFile:
        pagerJson = json.loads(pagerFile.read())
        pagerFile.close()

    book_width = pagerJson["bookSize"]["width"]
    book_height = pagerJson["bookSize"]["height"]

    pages = pagerJson["pages"]

    for page_name, page_contents in pages.items():
        print("Processing page " + page_name)
        try:
            page_number = int(page_name)
        except ValueError:
            # Not a page we can process. Skip.
            print("Skipping page " + page_name + " as it is not a number")
            continue

        pagenumber_padded = str(page_number).zfill(4)

        if (not os.path.exists(os.path.join("output", bookId, pagenumber_padded + ".html"))):
            print("Page " + page_name + " does not exist.")
            continue
        
        print("Opening page " + page_name)
        page_url = "file://" + os.path.join(os.getcwd(), "output", bookId, pagenumber_padded + ".html")
        driver.get(page_url)
        driver.implicitly_wait(0.5)
        print_options = PrintOptions()
        print_options.page_width = float(book_width) / 72 # 72 PPI (Converted up later)
        print_options.page_height = float(book_height) / 72 # 72 PPI (Converted up later)
        print_options.margin_bottom = 0
        print_options.margin_top = 0
        print_options.margin_left = 0
        print_options.margin_right = 0
        print_options.shrink_to_fit = True # Just in case of rounding errors
        # print_options.scale = 1.54 # 1 inch = 2.54 cm
        print_options.page_ranges = [1] # Just in case of rounding errors
        print_options.background = True
        print("Printing page " + page_name)
        base64_pdf = driver.print_page(print_options)
        print("Saving page " + page_name)
        with open(os.path.join("output", bookId, pagenumber_padded + ".pdf"), "wb") as pdfFile:
            pdfFile.write(base64.b64decode(base64_pdf))
            pdfFile.close()

    print("Closing ChromeDriver")
    driver.quit()
    print("Done!")

    merge.doMerge(bookId, session)