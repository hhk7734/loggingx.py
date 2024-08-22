import json

try:
    import orjson

    orjson_imported = True
except ImportError:
    orjson_imported = False

if orjson_imported:

    def dumps(obj):
        return orjson.dumps(obj).decode()
else:

    def dumps(obj):
        # Set ensure_ascii to False to output the message as it is typed.
        return json.dumps(obj, ensure_ascii=False)
