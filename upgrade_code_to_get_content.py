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

        main = soup.find('div', {'class': 'container'})
        content = main.get_text()
        marker = "For the latest breaking news updates, click here to download the E! News App"
        if marker in content:
            content = content.split(marker)[0].strip()
                
        # pictures
        picture_links = []
        for img_tag in main.find_all('img'):
            if img_tag.get('src'):
                picture_links.append(img_tag['src'])
        
        print(picture_links)
        time.sleep(100000)
    
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

data = get_new_links()
get_info_new(data[1])

# func = func_to_string(get_new_links)
# func2 = func_to_string(get_info_new)

# add_func('theguardian', func, func2)
