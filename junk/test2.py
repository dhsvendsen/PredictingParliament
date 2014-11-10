import json

with open('projectproposal.txt', 'r') as in_file:
	a = json.load(in_file)

print json.dumps(a, indent=1)