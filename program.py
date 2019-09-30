import requests
import bs4
import collections
import header
WeatherReport = collections.namedtuple('WeatherReport',
                                       'loc, cond, temp')


def main():
    header.print_header()
    location = get_location()
    html = get_html_from_web(location)
    report = get_weather_from_html(html)
    print('The temp in {} is {} and {}'.format(
        report.loc,
        report.temp,
        report.cond
    ))


def get_location():
    loc = ''
    while loc == '':
        loc = input('What location do you want current weather updates for ? ')

    loc = loc.strip()
    print('Getting weather updates for {}...'.format(loc.capitalize()))
    loc = loc.replace(' ', '-')
    return loc


def get_html_from_web(loc):
    url = 'https://www.wunderground.com/weather/za/{}'.format(loc)
    response = requests.get(url)
    # print(response.status_code)
    print(url)
    # print(response.text[0:250])  # slicing
    return response.text


def get_weather_from_html(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    loc = soup.find(class_='city-header').find('h1').find('span').get_text()
    condition = soup.find(class_='condition-icon').find('p').get_text()

    temp_html = soup.find(class_='current-temp').get_text()
    temp_farad = int(temp_html[:2])
    temp = convert_to_celsius(temp_farad)

    # print(loc, '{} ℃'.format(temp), condition)
    report = WeatherReport(loc=loc, cond=condition, temp='{} ℃'.format(temp))
    return report


def convert_to_celsius(temp_farad):
    return int((temp_farad - 32) * 5 / 9)


if __name__ == '__main__':
    main()
