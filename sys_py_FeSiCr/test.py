import re
stem = 'tempstring 032544'
print(re.findall(r'\d+', 'tempstring 032544')[0])
