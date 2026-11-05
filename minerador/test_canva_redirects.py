import requests
import re

url1 = "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFszx4q03q6kc1vqm4H5odA2xwtpwK53KoAKgh9gmTXzLS9sjpd5it-W5I1676jvUA6_SVgfhs1berrHBefksY_OaflfBfSeqjERD30ri0jsdQIrgfNxPmdLqONSdqc5euBeHrkivM="
url2 = "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG5RitOpv9y7IgCfr50iyuBuIF1VWsvU7Mt73q1_ZuNx8rV4r2ZHyAOF9cSs9ecosDBS3TDo1yiaFPB_HXVnlLXS8WECWWPpNhSJTxfNip1tPrqimJaUpxz3-QOsPq3Ri9A8uJfEQ=="
url3 = "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEGzYNRtQJjt4ZsIFhEugCwMk3IbTED28ItiT0IId9rKpfH8T4PCGv3hlZ4UvWzYai75lto2CkfSQsAtXkpquQvOUP6lBU1ldbJ2IbyIevv86vmzRCzRPgN20fau6-ibHF6siZZ="

for u in [url1, url2, url3]:
    try:
        r = requests.get(u, headers={'User-Agent': 'Mozilla/5.0'}, allow_redirects=True, timeout=5)
        print("Final URL:", r.url)
        # find title
        title = re.search(r'<title>(.*?)</title>', r.text)
        print("Title:", title.group(1) if title else "None")
        # find instagram links
        ig = re.findall(r'instagram\.com/([a-zA-Z0-9_\.]+)', r.text)
        print("IG:", set(ig))
    except Exception as e:
        print("Error:", e)
