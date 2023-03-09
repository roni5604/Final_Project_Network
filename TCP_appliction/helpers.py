import os
def get_content_type(file_path):
    """Returns the Content-Type for the given file path"""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.html':
        return 'text/html'
    elif ext == '.txt':
        return 'text/plain'
    elif ext == '.css':
        return 'text/css'
    elif ext == '.js':
        return 'application/javascript'
    elif ext == '.jpg' or ext == '.jpeg':
        return 'image/jpeg'
    elif ext == '.png':
        return 'image/png'
    elif ext == '.gif':
        return 'image/gif'
    else:
        return 'application/octet-stream'
