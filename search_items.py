import json
def search_items(name, userID):
    items = json.load(open('items.json','r',encoding='utf-8'))
    if(name == "ALL_ITEMS"):
        if(userID not in items):
            return "ERROR"
        result = json.dumps(items[userID],ensure_ascii=False)
        result = result.replace('{','').replace('}','').replace('\"','').replace(',','\n').replace(' ','').replace(':',': ')
        return result
    else:
        if(userID not in items or name not in items[userID]):
            return "ERROR"
        return str(items[userID][name])