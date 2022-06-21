import imp
import os
import base64
import uuid
import re

def get_binary_file_downloader_html(bin_file, file_label='File'):

    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()

    button_uuid = str(uuid.uuid4()).replace("-", "")
    button_id = re.sub("\d+", "", button_uuid)

    custom_css = f""" 
    <style>
            #{button_id} {{
            background-color: rgb(14, 17, 23);
            color: rgb(255, 255, 255);
            padding: 0.5em 0.5em;
            position: relative;
            text-decoration: none;
            border-radius: 10px;
            border-width: 4px;
            border-style: solid;
            border-color: rgb(230, 234, 241);
            border-image: initial;
            }} 
            #{button_id}:hover {{
            border-color: rgb(246, 51, 102);
            color: rgb(246, 51, 102);
            }}
            #{button_id}:active {{
            box-shadow: none;
            background-color: rgb(246, 51, 102);
            color: white;
            }}
    </style> """

    href = custom_css + f'<a id="{button_id}" href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href
