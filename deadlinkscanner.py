import requests
from bs4 import BeautifulSoup


def find_dead_links(url):
    # Make an HTTP GET request to the specified URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the <a> tags on the page
        links = soup.find_all('a')

        dead_links = []

        for link in links:
            href = link.get('href')

            if href:
                # Check if the link is an absolute URL or a relative URL
                if href.startswith('http'):
                    target_url = href
                else:
                    # Construct the absolute URL using the base URL
                    base_url = response.url
                    target_url = f'{base_url}/{href}'

                # Make a HEAD request to check the status of the link
                link_response = requests.head(target_url)
                if link_response.status_code != 200:
                    # Add the dead link to the list
                    dead_links.append(target_url)

        return dead_links

    else:
        # Request was unsuccessful, return an empty list
        return []


# Example usage
url = 'http://www.deadlinktest.com/'  # Replace with the desired URL
dead_links = find_dead_links(url)
print(dead_links)
