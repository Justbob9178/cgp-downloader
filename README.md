# cgp-smarter-download
## Disclaimer
This software is provided for the sole purpose of personal use of offline and private copies of the CGP books. Do not distribute any copyrighted files downloaded by this program. All property downloaded remains the copyright of CGP or the respected author. The author of this software does not condone copyright infringement and will not take any responsibility for any actions of any user of this software. Please note that you can only download books you already own on the CGP Online platform with this software. Books which you do not own cannot be downloaded.

## Introduction
This is an updated version of [this](https://github.com/TheJoeCoder/cgp-download/) - `https://github.com/TheJoeCoder/cgp-smarter-download` repository which I added my own quality of life features to (login with username/password and multi book downloads). Also fixed it as some things were broken.

## Running
Documentation is currently not finished and the software is still a work-in-progress, but here's a quick rundown:
* Install Python and Git if you don't already have them.
* Clone the repo: `git clone https://github.com/Justbob9178/cgp-smarter-download`
* CD into directory: `cd cgp-smarter-download`
* This next step assumes you are using linux - Windows users you are on your own for a few steps (google python venv)
* Create a virtual python enviroment `python -m venv .venv` and switch to it `source .venv/bin/activate`
* Windows user you *should* be able to join back now
* Install required packages `pip install -r requirements.txt`
* Copy the contents of `.env.example` to `.env` and fill in your details. This step is optional as the script will ask for your details if not provided.
* Run the program with `python login.py`
* Follow steps on screen
* Pray it works

## Programming Progress
Ordered in level of importance/difficulty
- [ ] Add page labels (FC, IFC, Contents-i, etc.)
- [ ] Add Links
- [ ] Order page based on "structure" pager page def, not on order of pages
- [ ] 403 Forbidden (Cookie expiration/Access Denied) handling
- [x] Book browser/selection (userguid and signature collection)
- [x] Remove collecting cookie dependency (username+password login to gain userguid and signature)
- [ ] For that matter, work out how userguids and signatures work at all
- [ ] Book Frontend page + flippingbook index page parsing (/digitalaccess/{id}/Online/ and /digitalcontent/{id}/index.html: useful info contained within...)
- [ ] Fancy GUI
- [ ] Make code cleaner (especially download.py)
- [x] Parse pager.js manifest
- [x] Download books
- [x] Download pager.js and workspace.js manifests from web
- [x] Convert HTML to PDF
- [x] Merge PDFs
- [x] Add bookmarks
