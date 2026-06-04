content = open('visaflow/extraction/extractors.py').read()
old = '''    documents = dedupe_ordered(documents)
    return [d for d in documents
            if normalize_for_matching(d) not in {"documents","materials","items","file","record"}
            and not d.lower().startswith("please ")]'''
new = '''    documents = dedupe_ordered(documents)
    noise = {"documents","materials","items","file","record","my supervisor",
             "supervisor","both me","me and my supervisor","my employer"}
    return [d for d in documents
            if normalize_for_matching(d) not in noise
            and not d.lower().startswith("please ")
            and not d.lower().startswith("both ")
            and not d.lower().startswith("me and ")
            and len(d.strip()) > 4]'''
assert old in content, "Pattern not found"
content = content.replace(old, new)
open('visaflow/extraction/extractors.py', 'w').write(content)
print("done")
