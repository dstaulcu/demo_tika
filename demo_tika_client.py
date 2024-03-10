import os
import tika
from tika import parser
import json
import re

target_dir = os.environ['USERPROFILE'] + r'\Documents'
if os.path.exists(target_dir) == False:
    print('target_dir value: {} not found. Exiting'.format(target_dir))
    quit(1)

tika_server_filepath = os.getcwd() + r'\offline\tika-server-standard-2.9.1.jar'
if os.path.exists(tika_server_filepath) == False:
    print('server_filepath value: {} not found. Exiting'.format(tika_server_filepath))
    quit(1)
tika_server_environ_filepath = 'file:////' + tika_server_filepath
os.environ['TIKA_SERVER_JAR'] = tika_server_environ_filepath


def find_all_matches(pattern, string):
    pat = re.compile(pattern)
    pos = 0
    out = []
    while (match := pat.search(string, pos)) is not None:
        pos = match.start() + 1
        out.append(match[1])
    return out


# initialize tika server
tika.initVM()

# define regex pattern names/values to search
# -online resource to find community produced regex patterns: https://regexr.com/
# -online resource to produce escaped python code for regex patterns https://www.pythonescaper.com
patterns = {
    "SSN": r'\d{3}\-\d{2}\-\d{4}',
    "EMAIL": r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b',
    "URL": r'(http|ftp|https)://([\w+?\.\w+])+([a-zA-Z0-9\~\!\@\#\$\%\^\&\*\(\)_\-\=\+\\\/\?\.\:\;\'\,]*)?',
    "IPV4": r'\b(?:(?:2(?:[0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9])\.){3}(?:(?:2([0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9]))\b',
    "GEO": r'^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$'
}

# walk target folder recursively
print('Processing target_dir: {} recursively...'.format(target_dir))
for r, d, f in os.walk(target_dir):
    for file in f:
        filepath = os.path.join(r, file)
        # task tika to return metadata + content
        parsed = parser.from_file(filepath)
        # process the content
        if parsed['content']:
            # check file content for each pattern type
            for pattern in patterns:
                findings = find_all_matches(
                    '\s?(' + patterns[pattern] + ')\s?', parsed['content'])
                for finding in findings:
                    # print any of many potential findings
                    print(
                        '-found "{}" having value: "{}" in file: "{}"'.format(pattern, finding, filepath))
