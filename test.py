from dbUtil import DBSession
from entity import YearTag, Task
from httpUtil import get_html
from sfdblog import logger


def built_tasks_by_url(url):
    try:
        session = DBSession()
        html = get_html(url)
        logger.debug(html)
        subjects = html.xpath('//tr[@class="item"]/td/a[@class="nbg"]/@href')
        for subject in subjects:
            task = Task(url=url, isScanned=False)
            session.add(task)
            session.commit()
    except Exception as e:
        logger.exception("built_tasks_by_tag has exception:")
        logger.exception(e)
        logger.exception("built_tasks_by_tag has exception:url:")
        logger.exception(url)
    finally:
        session.close()


def built_tasks_by_tag(year_tag):
    try:
        session = DBSession()
        year_tag_in_session = session.query(YearTag).filter(YearTag.id == year_tag.id).first()
        year_tag_in_session.isScanned = True
        session.commit()
        html = get_html("https://movie.douban.com/tag/%s?start=0&type=R" % year_tag.year)
        pages = html.xpath('//div[@class="paginator"]/a')
        max_page = 1 if len(pages) == 0 else int(pages[-1].text.strip())
        for x in range(year_tag_in_session.page, max_page):
            url = "https://movie.douban.com/tag/%s?start=%d&type=R" % (year_tag.year, x * 20)
            built_tasks_by_url(url)
            year_tag_in_session.page = x
            session.commit()
    except Exception as e:
        logger.exception("built_tasks_by_tag has exception:")
        logger.exception(e)
        logger.exception("built_tasks_by_tag has exception:year_tag:")
        logger.exception(year_tag)

        year_tag_in_session.isScanned = False
        session.commit()
    finally:
        session.close()


def built_all_tasks():
    session = DBSession()
    for year_tag in session.query(YearTag).filter(YearTag.isScanned.is_(False)).all():
        built_tasks_by_tag(year_tag)
    session.close()


def main():
    built_all_tasks()
if __name__ == "__main__":
    main()
