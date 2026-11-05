import requests
import re
import html

url = 'https://hotmart.com/pt-br/marketplace/produtos/mentoria-tjsp-escrevente-tecnico-judiciario-interior/W105412850U'
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
text = r.text

print("Title:", re.search(r'<title>(.*?)</title>', text).group(1))
# Find producer
producer = re.findall(r'"producer":\{"name":"([^"]+)"', text)
print("Producer:", producer)
# Find author / vendor
author = re.findall(r'"author":\{"@type":"Person","name":"([^"]+)"', text)
print("Author:", author)
# Find any description
desc = re.findall(r'"description":"([^"]+)"', text)
if desc:
    print("Description:", html.unescape(desc[0])[:200])
