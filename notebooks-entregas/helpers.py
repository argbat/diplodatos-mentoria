def lift_dataset(path):
    from pathlib import Path
    import os
    import re

    def events_line_numbers(annotation):
        event_line_number_regex = '.*\s([0-9]+):[0-9]{1,2}.*'
        return int(re.match(event_line_number_regex, annotation).group(1))

    folder = Path('../dataset/2012-07-15.original-annotation.release')
    relations = [rfile for rfile in folder.iterdir() if rfile.name.endswith('tlink')]
    for filename in relations:
        with open(filename.absolute(), 'r') as f, open(str(filename.absolute()).replace('tlink', 'txt'), 'r') as s:
            sourcelines = s.readlines()
            for line in f.readlines():
                annotations = line.split('||')
                ev_1_line_number = events_line_numbers(annotations[0])
                ev_2_line_number = events_line_numbers(annotations[1])
                if ev_1_line_number > ev_2_line_number:
                    result = annotations
                    result += [sourcelines[ev_2_line_number - 1].strip() + ' ' + sourcelines[ev_1_line_number - 1].strip()]
                    result += [filename.name]
                elif ev_1_line_number < ev_2_line_number:
                    result = annotations
                    result += [sourcelines[ev_1_line_number - 1].strip() + ' ' + sourcelines[ev_2_line_number - 1].strip()]
                    result += [filename.name]
                else:
                    result = annotations + [ sourcelines[ev_1_line_number - 1].strip() ] + [filename.name]
                    
                yield result
    
