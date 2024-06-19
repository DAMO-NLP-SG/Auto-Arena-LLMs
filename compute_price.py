import json
def read_jsonl(path):
    data = []
    with open(path, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data

price = read_jsonl("price.jsonl")
total = 0
for x in price:
    total += x["Price"]
print('total price', total)