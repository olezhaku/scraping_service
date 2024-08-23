import requests
import codecs
from bs4 import BeautifulSoup as BS
import re
from random import randint

__all__ = ("rabota", "superjob", "remotejob", "careerjet")

headers = [
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.127",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    },
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    },
    {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    },
]


def rabota(url, city=None, language=None):
    jobs = []
    errors = []
    domain = "https://www.rabota.ru"
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])

        if resp.status_code == 200:
            soup = BS(resp.content, "html.parser")
            main_div = soup.find("div", class_="r-serp")
            div_list = main_div.find_all(
                "div", attrs={"class": "vacancy-preview-card__top"}
            )

            if main_div:
                for div in div_list:
                    title = div.find("h3")
                    href = title.a["href"]
                    content = div.find(
                        "div", class_="vacancy-preview-card__short-description"
                    )
                    company = div.find("a", itemprop="name")
                    jobs.append(
                        {
                            "title": title.text,
                            "url": domain + href,
                            "description": content.text,
                            "company": company.text,
                            "city_id": city,
                            "language_id": language,
                        }
                    )
            else:
                errors.append({"url": url, "title": "Div does not exists"})
        else:
            errors.append({"url": url, "title": "Page do not response"})

    return jobs, errors


def superjob(url, city=None, language=None):
    jobs = []
    errors = []
    domain = "https://www.superjob.ru"
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])

        if resp.status_code == 200:
            soup = BS(resp.content, "html.parser")
            main_div = soup.find("div", attrs={"class": "_1UpFp"})
            div_list = main_div.find_all(
                "div", attrs={"class": "f-test-search-result-item"}
            )
            pattern = re.compile(r"EruXX XHlOg f-test-link-.*")

            if main_div:
                for div in div_list:
                    title = div.find("div", class_="OVIuz")
                    href = title.a["href"]
                    content = div.find(
                        "span", class_="_3cUok _25Lsd rsshI FwFyY _2MmL7"
                    )
                    company = div.find("a", class_=pattern)
                    if company is not None:
                        company_text = company.text
                    else:
                        company_text = ""
                    jobs.append(
                        {
                            "title": title.text,
                            "url": domain + href,
                            "description": content.text,
                            "company": company_text,
                            "city_id": city,
                            "language_id": language,
                        }
                    )
            else:
                errors.append({"url": url, "title": "Div does not exists"})
        else:
            errors.append({"url": url, "title": "Page do not response"})

    return jobs, errors


def remotejob(url, city=None, language=None):
    jobs = []
    errors = []
    domain = "https://remote-job.ru"
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])

        if resp.status_code == 200:
            soup = BS(resp.content, "html.parser")
            main_div = soup.find(
                "div",
                attrs={"class": "contentContainer"},
            )
            div_list = main_div.find_all("div", attrs={"class": "vacancy_item"})

            if main_div:
                for div in div_list:
                    title = div.find("a", target="_blank")
                    href = div.a["href"]
                    content = div.find(
                        "div",
                        class_="col-xs-12 col-sm-12 col-md-12 col-lg-12 text-left",
                    )
                    find_company = div.select("small a")
                    for company in find_company:
                        company = company.text

                    jobs.append(
                        {
                            "title": title.text,
                            "url": domain + href,
                            "description": content.text,
                            "company": company,
                            "city_id": city,
                            "language_id": language,
                        }
                    )
            else:
                errors.append({"url": url, "title": "Div does not exists"})
        else:
            errors.append({"url": url, "title": "Page do not response"})

    return jobs, errors


def careerjet(url, city=None, language=None):
    jobs = []
    errors = []
    domain = "https://www.careerjet.ru"
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])

        if resp.status_code == 200:
            soup = BS(resp.content, "html.parser")
            main_div = soup.find(
                "ul",
                attrs={"class": "jobs"},
            )
            div_list = main_div.find_all("article", attrs={"class": "job clicky"})

            if main_div:
                for div in div_list:
                    title = div.find("h2")
                    href = title.a["href"]
                    content = div.find("div", class_="desc")
                    company = div.find("p", class_="company")
                    if company:
                        company = company.text

                    jobs.append(
                        {
                            "title": title.text,
                            "url": domain + href,
                            "description": content.text,
                            "company": company,
                            "city_id": city,
                            "language_id": language,
                        }
                    )
            else:
                errors.append({"url": url, "title": "Div does not exists"})
        else:
            errors.append({"url": url, "title": "Page do not response"})

    return jobs, errors


if __name__ == "__main__":
    url = "https://www.careerjet.ru/работа?s=Python"

    # jobs, errors = careerjet(url)

    # h = codecs.open("work.txt", "w", "utf-8")
    # h.write(str(jobs))
    # h.close()
