import requests
import lxml.html as html
import os
import datetime
import properties


def parse_notice(link, folder_name):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                title = parsed.xpath(properties.XPATH_TITLE)[0]
                title = title.replace('\"', '')
                summary = parsed.xpath(properties.XPATH_SUMMARY)[0]
            except IndexError:
                return

            with open(f'{folder_name}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def save_news_in_folder(data):
    folder_name = datetime.date.today().strftime('%d-%m-%Y')
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

    for item in data:
        parse_notice(item, folder_name)


def parse_home():
    try:
        response = requests.get(properties.URL_HOME)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(properties.XPATH_LINK_TO_ARTICLE)
            # print(links_to_notices)
            save_news_in_folder(links_to_notices)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()


if __name__ == "__main__":
    run()
