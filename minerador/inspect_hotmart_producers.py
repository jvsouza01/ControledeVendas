import requests
import re
import html

urls = [
    ("Aprovasim", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFa0c4s1P_oNGCaFDNu2LH4p6Dju2DzNmckfEC6FkIOqD9rsnsQDN6u2xvk8EMmcdYQsLarVy300GJ_AnweEFO9qmBnc1roCVa7NglCMehwb8ckRzKH0Ig2Dj1j62y7ekRp6hGgLFFMHNixpSB9zI70XqLvOl8sGXehCEgbXTQz0246eMApSKYEGQ=="),
    ("Gabarito Certo", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHaded_8iZvcE6_7vxcl46rHBzPipX87NtSXlPNxHS5vAg_2pFqmIE5nYa7gwfyGJbnjIgDHWRNv4zaBZFKbsjqBDRIfGlyZ1zintZjdZ1zd_aO4FifLRBPrXHz3gVRlAxgtG-eOL6RNT6YR3C4qirJalYkIMdiPfQM6LcuErL0jMMQt10rnLLpcWdVxLe2MxP781MhpCnumc7IdPwr1g2BaZV76EQf3AjfLD7ymJNy5BmAnQ04H5a3rB8bBXviw7R_s5h1aMjwpKdybuTe4ZGsJ0mqpRW7MqtynkeTR5ild5lM8aNuPhMOiF-JSGHOw6nDSLBcPJ5WUWE="),
    ("Metodo QR", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHq1GzsQqIqzbWGGQV6B0VWSaLELErNNVkW46JBRfzJqKHOXw0QpWaj5pOKxVrHxN2qgSRtIQSkd_Ba9-4EGXAYWG0wY3kZcy2xLa9Pv9zn23ATwz4u-PxWNxKI1bTiLnRUA-oUxI-xma-XrJny3fIYKq2gchuZbDeCSIWQyq82oyVHzsJ_TcFKJl1c5HdR7H8="),
    ("Meu Cronograma", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHHj3-pXA8qW6AOWhVWzsLTjnt0xDhuDM66VU87l36VIWFM141cWzWOu3-WwnQhmtmX2-Jyc7H1-LbW2jFDZIg9d5WvK1k74j7Uq54JEtNVqUct4feAWkcBY4KM8Bh5KJEzZxHkJameokGizP-dpfW8Ulf-ggLmB4lj0mKNDBjYAlSBgvZMraXu-CsXUTr8MRCzKBa2I2mDOyPNCFYqgpFT7E-ZSDE="),
    ("TJMG 60 Dias", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFSH0F8ilULzmLorerBHgNHGyeVEIubhGjtr3EMRzA7cpH6mB1XpLFVi9yZIPpYLb8iJHy5iboEhSng2ssZPRjtSTt3qeXa5z3ondEryHo6qAENp_pBh5QnsVD7F6-6u4GN2DNIjjDjSg2f639e5SuB8kbuvgv6y_-uYcv4zX1uUgdBX6nNm3NFy6_DxbGzOl1Zg6FtD0aS3z9S")
]

for label, u in urls:
    try:
        r = requests.get(u, headers={'User-Agent': 'Mozilla/5.0'}, allow_redirects=True, timeout=6)
        print(f"\n[{label}] Final: {r.url}")
        t = re.search(r'<title>(.*?)</title>', r.text)
        print("Title:", t.group(1) if t else "")
        # look for any mention of @handle
        handles = re.findall(r'@([a-zA-Z0-9_\.]{3,30})', r.text)
        print("Handles in page:", set(handles[:5]))
    except Exception as e:
        print(f"[{label}] Error: {e}")
