import os
import tika
from tika import parser
import json
import re

# define the target directory
target_dir = os.environ['USERPROFILE'] + r'\Documents'
tika_server_filepath = os.getcwd() + r'\offline\tika-server-standard-2.9.1.jar'


def find_all_matches(pattern, string):
    pat = re.compile(pattern)
    pos = 0
    out = []
    while (match := pat.search(string, pos)) is not None:
        pos = match.start() + 1
        out.append(match[1])
    return out


if os.path.exists(tika_server_filepath) == False:
    print('server_filepath value: {} not found. Exiting'.format(tika_server_filepath))
    quit(1)
    
if os.path.exists(target_dir) == False:
    print('target_dir value: {} not found. Exiting'.format(target_dir))
    quit(1)    

tika_server_environ_filepath = 'file:////' + tika_server_filepath
os.environ['TIKA_SERVER_JAR'] = tika_server_environ_filepath

# initialize tika server
tika.initVM()

# define regex pattern names/values to search
'''
- online resource to find community produced regex patterns: https://regexr.com/
- online resource to produce escaped python code for regex patterns https://www.pythonescaper.com
'''
patterns = {
    "SSN": r'\d{3}\-\d{2}\-\d{4}'
}

# walk target folder recursively
print('Processing target_dir: {} recursively...'.format(target_dir))
for r, d, f in os.walk(target_dir):
    for file in f:
        filepath = os.path.join(r, file)
        #print('working on file: {}'.format(filepath))

        # task tika to return metadata + content
        parsed = parser.from_file(filepath)
        if parsed['content']:
            # check file content for each pattern type
            for key in patterns:
                # print('-finding {} entries having pattern: "{}"'.format(key, patterns[key]))
                findings = find_all_matches('(' + patterns[key] + ')', parsed['content'])
                for finding in findings:
                    # print any of many potential findings
                    print('-found "{}" having value: "{}" in file: "{}"'.format(key, finding, filepath))
