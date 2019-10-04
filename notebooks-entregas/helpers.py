def lift_dataset(path):
    from pathlib import Path
    import os
    import re
    folder = Path(path)
    if not folder.exists() or not folder.is_dir():
        exit("Either folder doesn't exist or is a file")

    relations = [rfile for rfile in folder.iterdir() if rfile.name.endswith('tlink')]
    for filename in relations:
        with open(filename.absolute(), 'r') as f, open(str(filename.absolute()).replace('tlink', 'txt'), 'r') as s:
            sourcelines = s.readlines()
            for line in f.readlines():
                first_annotation = line.split('||')[0]
                linenumber = int(re.match('.*\s([0-9]+):[0-9]{1,2}.*', first_annotation).group(1))
                yield line.split('||') + [ sourcelines[linenumber - 1] ] + [filename.name]
    
