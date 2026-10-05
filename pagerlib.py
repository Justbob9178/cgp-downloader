import os

workspace_try_urls = [
    "https://library.cgpbooks.co.uk/digitalcontent/{id}/assets/html/workspace.js",
    "https://library.cgpbooks.co.uk/digitalcontent/{id}/assets/workspace.js"
]

pager_try_urls = [
    "https://library.cgpbooks.co.uk/digitalcontent/{id}/assets/common/pager.js",
    "https://library.cgpbooks.co.uk/digitalcontent/{id}/assets/pager.js"
]

if (not os.path.exists('pagers')):
    os.mkdir('pagers')

def get_book_dir(book):
    dirr = os.path.join('pagers', book)
    if (not os.path.exists(dirr)):
        os.mkdir(dirr)
    return dirr

def get_file_contents(filename):
    contents = None
    try:
        with open(filename, "r") as file:
            contents = file.read()
            file.close()
    except:
        pass
    return contents

def download_file_test_url(urls, bookid, output_file, session):
    for url in urls:
        try:
            book_url = url.replace("{id}", bookid)
            print("Trying " + book_url)
            response = session.get(book_url)
            print(response.status_code)
            if response.status_code != 200:
                print(f"received {response.status_code} status code")
                print(session.gookies.get())
            else:
                workspace = response.text
                if "NoSuchKey" in workspace:
                    print("Failed to get workspace file from " + book_url)
                    continue
                print("Writing to " + output_file)
                with open(output_file, 'w') as workspace_file:
                    workspace_file.write(workspace)
                return output_file
        except Exception as error:
            print("An exception occurred:", error)
            print("Failed to get workspace file from " + book_url)
            continue
    print("Failed to get file file for " + bookid + " from any URL (tried " + str(len(urls)) + ")")
    return None

def get_workspace_file(book):
    # Return the workspace file for the given book.
    workspace_path = os.path.join(get_book_dir(book), 'workspace.js')
    if os.path.exists(workspace_path):
        return workspace_path
    return download_file_test_url(workspace_try_urls, book, workspace_path)

def get_pager_file(book, session):
    # Return the pager file for the given book.
    pager_path = os.path.join(get_book_dir(book), 'pager.js')
    if os.path.exists(pager_path):
        return pager_path
    return download_file_test_url(urls=pager_try_urls, bookid=book, output_file=pager_path, session=session)
