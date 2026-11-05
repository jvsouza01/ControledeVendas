import urllib.request
import re

url = "https://www.youtube.com/watch?v=0jvaqzsExyc"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        content = resp.read().decode('utf-8', errors='ignore')
        print("Length:", len(content))
        # Look for description
        desc_m = re.findall(r'"shortDescription":"(.*?)"', content)
        if desc_m:
            print("Description snippet:", desc_m[0][:200])
        # Look for instagram
        instas = re.findall(r'instagram\.com/([a-zA-Z0-9_\.]+)', content)
        print("Instas in content:", set(instas))
except Exception as e:
    print("Error:", e)
