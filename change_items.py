import json

def change_items(name, amount, user_ID):
    items = json.load(open('items.json','r'))
    if(user_ID not in items):
        items[user_ID] = {}
    if(name not in items[user_ID]):
        # reduce
        if(int(amount)<0):
            return "ERROR"
        else:
            items[user_ID][name] = 0
    items[user_ID][name] =  str(int(items[user_ID][name])+int(amount))
    if(int(items[user_ID][name]) <= 0):
        items[user_ID][name] = '0'
    output = json.dumps(items, indent=4,ensure_ascii=False, sort_keys=True)
    with open('items.json','w') as f:
        f.write(output)
    return "Success"