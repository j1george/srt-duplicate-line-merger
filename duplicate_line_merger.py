import glob
import re


class Time:
    hours = None
    minutes = None
    seconds = None
    milliseconds = None

    def __init__(self, line):
        self.hours, self.minutes, self.seconds, self.milliseconds = (int(x) for x in line.replace(',', ':').split(':'))

    @property
    def total_milliseconds(self):
        return self.get_normalized_time()

    def get_normalized_time(self):
        normalized_time = self.hours * 3600000
        normalized_time += self.minutes * 60000
        normalized_time += self.seconds * 1000

        return normalized_time + self.milliseconds

    def __repr__(self):
        return ('{}:{}:{},{}').format(str(self.hours).zfill(2), str(self.minutes).zfill(2), str(self.seconds).zfill(2), str(self.milliseconds).zfill(3))


class Timestamp:
    start = None
    end = None

    def __init__(self, line):
        self.start, self.end = (Time(x) for x in line.split(' --> '))

    def __repr__(self):
        return ('{} --> {}').format(self.start, self.end)


class SubtitleSection:
    num = None
    timestamp = None
    lines = None

    def __init__(self, num):
        self.num = num

    def __repr__(self):
        return ('{num}\n{timestamp}\n{lines}'.format(num=self.num, timestamp=self.timestamp, lines='\n'.join(self.lines)))


def create_sub_arr(subs):
    lines = subs.splitlines()

    sections = []

    for line in lines:
        if line.isdigit():
            sections.append(SubtitleSection(int(line)))
        else:
            if sections[-1].timestamp is None:
                sections[-1].timestamp = Timestamp(line)
            elif line == '':
                pass
            else:
                if sections[-1].lines is None:
                    sections[-1].lines = [line]
                else:
                    sections[-1].lines.append(line)

    return sections


def merge_sub_array(sub_arr):
    i = 1
    while i < len(sub_arr):
        prev_sub = sub_arr[i-1]
        cur_sub = sub_arr[i]

        lower_prev_sub, lower_cur_sub = list(x.lower() for x in prev_sub.lines), list(x.lower() for x in cur_sub.lines)
        stripped_prev_sub, stripped_cur_sub = list(re.sub(r'\W+', '', x).lower() for x in prev_sub.lines), list(re.sub(r'\W+', '', x).lower() for x in cur_sub.lines)
        if stripped_cur_sub == stripped_prev_sub:
            if cur_sub.timestamp.start.total_milliseconds - prev_sub.timestamp.end.total_milliseconds < 2:
                sub_arr[i-1].timestamp.end = cur_sub.timestamp.end
                sub_arr.pop(i)
                i -= 1
        i += 1

    return sub_arr


def renumbered_subs(merged_sub_arr):
    for i, e in enumerate(merged_sub_arr):
        merged_sub_arr[i].num = i+1
    return merged_sub_arr

for file_path in glob.glob("*.srt"):
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        subs = f.read()

    sub_arr = create_sub_arr(subs)

    merged_sub_arr = merge_sub_array(sub_arr)

    renumbered_merged_sub_arr = renumbered_subs(merged_sub_arr)

    merged_subs = '\n\n'.join(str(x) for x in renumbered_merged_sub_arr)

    with open('merged/' + file_path, 'w+', encoding='utf-8-sig') as f:
        f.write(merged_subs)
