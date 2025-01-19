import re

pattern = r"\((.*?)\)"

string = ':  Key (driver_id)=(0) is not present in table "driver".'
matches = re.findall(pattern, string)

print(matches)  # Output: ['driver_id', '0']
