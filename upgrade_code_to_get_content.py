from untils import func_to_string
from db_mongodb import add_func
import time


def get_new_links():
    from bs4 import BeautifulSoup
    import requests

    url = 'https://www.eonline.com/news'
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    top_items = soup.find_all('div', class_='top-two__item')
    link = []
    for item in top_items:
        data = item.find('a')['href']
        if '/news/' in data:
            link.append(f'https://www.eonline.com{data}')

    old_items = soup.find_all('div', class_='content-item')
    for item in old_items:
        data = item.find('a')['href']
        if '/news/' in data:
            link.append(f'https://www.eonline.com{data}')

    return link


def get_info_new(url):
    try:
        from bs4 import BeautifulSoup
        import requests
        import json
        import re

        headers = {
            'User-Agent': 'Mozilla/5.0'
        }

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # title, description and content
        title = None
        meta_tag = soup.find('meta', attrs={'property': 'og:title'})
        if meta_tag:
            title = meta_tag.get('content', None)

        description = None
        meta_tag = soup.find('meta', attrs={'name': 'description'})
        if meta_tag:
            description = meta_tag.get('content', None)

        tags = None
        meta_tag = soup.find('meta', attrs={'property': 'article:tag'})
        if meta_tag:
            tags = meta_tag.get('content', None)
            
        mains = soup.find_all('div', class_='is-desktop')
        target_div = None
        for main in mains:
            if not main.find_parent('header'):
                target_div = main
                break
        cta_divs = target_div.find_all('div', class_='article-detail__cta__body')
        for cta in cta_divs:
            cta.decompose()
            
        content = target_div.get_text()
        marker = "For the latest breaking news updates, click here to download the E! News App"
        if marker in content:
            content = content.split(marker)[0].strip()

        # pictures
        picture_links = []
        script_tag = soup.find(
        'script', string=re.compile(r'window\.__APOLLO_STATE__'))
        if script_tag:
            script_content = script_tag.get_text()
            script_content = script_content.encode().decode("unicode_escape")
            pattern = r'"Image:(\d+)":\s*\{(.*?)\}'
            matches = re.findall(pattern, script_content, flags=re.DOTALL)
            for img_id, block in matches:
                width_match = re.search(r'"sourceWidth"\s*:\s*"(\d+)"', block)
                height_match = re.search(
                    r'"sourceHeight"\s*:\s*"(\d+)"', block)

                width = int(width_match.group(1)) if width_match else 0
                height = int(height_match.group(1)) if height_match else 0

                if width == 1200 and height == 1200:
                    continue
                if width_match is None and height_match is None:
                    continue
                uri_match = re.search(
                    r'"uri"\s*:\s*"([^"]+)"',
                    block
                )
                if uri_match:
                    url_img = uri_match.group(1)
                    if "akns-images.eonline.com" in url_img:
                        picture_links.append(url_img)

            picture_links = sorted(set(picture_links))

        if (picture_links.__len__() == 0 or content is None or tags is None or title is None or description is None):
            return None

        return {
            "content": content,
            "title": title,
            "description": description,
            "tags": tags,
            "picture_links": picture_links
        }
    except:
        return None


# data1 = get_new_links()
# data = get_info_new(data1[0])
# print(data1[0])
# print(data)

func = func_to_string(get_new_links)
func2 = func_to_string(get_info_new)

add_func('eonline', func, func2)
