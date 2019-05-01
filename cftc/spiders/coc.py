import re
import scrapy

from datetime import datetime


def get_dates(date_text):
    months = []
    for date in date_text.getall():
        month = re.findall(r'(\D+)\s', date)
        year = re.findall(r'\d+', date)
        months.append((month[0], year[0]))
    return months


class CoCSpider(scrapy.Spider):
    name = "coc"

    start_urls = [
        'https://www.cftc.gov/MarketReports/CottonOnCall/index.htm'
    ]

    def parse(self, response):

        report_table = response.xpath("//article/table[position()=2]")
        date_text = report_table.xpath(".//tr/th[@axis='date']/text()")

        dates = get_dates(date_text)

        for count, data in enumerate(report_table.xpath(".//tr[./th[@axis='date']]")):

            numbers = data.xpath(".//td/text()")

            numbers = [num.get().replace('\xa0', '') for num in numbers]

            yield {
                'call_cotton': {
                    'report_date': datetime.now().strftime("%m-%d-%Y"),
                    'month': dates[count][0],
                    'year': dates[count][1],
                    'unfixed_call_sales': numbers[0],
                    'unfixed_call_purchases': numbers[2],
                },
                'ice_futures': {
                    'at_close': numbers[4]
                }
            }

