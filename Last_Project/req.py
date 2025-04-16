import requests
from bs4 import BeautifulSoup

url = "https://www.vanrenterghemenco.be/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}
for i in range(50):
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Option 1: Iterate and print
        for idx, line in enumerate(soup.stripped_strings, 1):
            print(f"{idx}. {line}")
        
        # Option 2: Convert to a list and print all at once
        # all_text = list(soup.stripped_strings)
        # print("\n".join(all_text))

    else:
        print(f"Failed to fetch: Status code {response.status_code}")

    print(i,"th time done")
