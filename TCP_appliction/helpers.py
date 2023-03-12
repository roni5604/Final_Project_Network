import os


# function to simply get any kind of file for our comfort
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


def to_html_format_OK(file_path, file_content):
    # organize the response as '200 OK' format
    response_headers = [
        f'HTTP/1.1 200 OK',
        f'Content-Type: {get_content_type(file_path)}',
        f'Content-Length: {len(file_content)}',
        f'Content-Disposition: attachment; filename="{os.path.basename(file_path)}"',
        'Connection: close',
        '',
        ''
    ]
    return '\r\n'.join(response_headers).encode() + file_content


def to_html_format_Redirect(location_header):
    # organize the response data for a 301 redirect
    response_headers = [
        'HTTP/1.1 301 Moved Permanently',
        location_header,
        'Connection: close',
        '',
        ''
    ]
    return '\r\n'.join(response_headers).encode()