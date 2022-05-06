import json

bool = {'mon': True}
json_bool = json.dumps(bool)
print(json_bool)
str_bool = json.loads(json_bool)
print(str_bool)