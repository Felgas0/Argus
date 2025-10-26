import sys
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


baseUrl = sys.argv[1]


visited_links = set()
links_to_visit = {baseUrl}
forms = []

while links_to_visit:
    current_link = links_to_visit.pop()

    if current_link in visited_links:
        continue

    if not current_link.startswith(baseUrl):
        continue

    try:
        print(f"looking for in: {current_link}")
        response = requests.get(current_link)
        visited_links.add(current_link)

        if response.status_code != 200:
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        for link in soup.find_all("a"):
            href = link["href"]

            new_link = urljoin(baseUrl, href)

            # i.e. if it is a SPA clear the fragments
            new_link = new_link.split('#')[0]

            if new_link not in visited_links and new_link not in links_to_visit:
                links_to_visit.add(new_link)

    except requests.exceptions.RequestException as e:
        print(f"error looking in  {current_link}: {e}")

print("Crawl Complete")
print(f"Total pages visited: {len(visited_links)}")