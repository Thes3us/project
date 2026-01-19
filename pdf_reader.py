import pymupdf
def send(file):
    """sends pdf file from Flask app to be process
    Args:
        file (bytestream): The pdf in bytestream
    Returns:
        boolean: Whether if data exists or not
    """
    if not file:
        return False

    byte_form=file.read()        #reads the file in byte form from the object
    doc = pymupdf.open(stream=byte_form,filetype="pdf")     #opens the file from the byte form
    content = []
    for page in doc:
        text=page.get_text()   #converts byte to human readable stuff
        content.append(text)
    print(content)
    return True