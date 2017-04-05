from dbUtil import DBSession
from entity import YearTag, Task, Celebrity, Subject, Proxy
from httpUtil import get_html, get_inner_text, get_tail, get_attr, bea_celebrity_info
from sfdblog import logger
from sqlalchemy.sql import and_


# 根据id获得影人（若该id数据库内不存在则创建该影人）
def get_or_create_celebrity(c_id):
    if c_id == "serach":
        return
    try:
        session = DBSession()
        celebrity = session.query(Celebrity).filter(Celebrity.id == c_id).first()
        if celebrity is None:
            celebrity = built_celebrity_by_id(c_id)
            session.add(celebrity)
        session.commit()
        return celebrity
    except Exception as e:
        logger.exception("get_or_create_celebrity has exception:c_id:"+c_id)
        raise
    finally:
        session.close()


def built_celebrity_by_id(c_id):
    try:
        url = "https://movie.douban.com/celebrity/%s/" % c_id
        html = get_html(url)
        return Celebrity(
            id=c_id,
            zodiac=bea_celebrity_info(get_tail(html, '//div[@id="headline"]/div[@class="info"]//span[text()="星座"]')),
            birthday=bea_celebrity_info(get_tail(html, '//div[@id="headline"]/div[@class="info"]//span[text()="出生日期"]')),
            birthplace=bea_celebrity_info(get_tail(html, '//div[@id="headline"]/div[@class="info"]//span[text()="出生地"]')),
            profession=bea_celebrity_info(get_tail(html, '//div[@id="headline"]/div[@class="info"]//span[text()="职业"]')),
            for_lang_names=bea_celebrity_info(get_tail(html, '//div[@id="headline"]/div[@class="info"]//span[text()="更多外文名"]')),
            name=get_inner_text(html, '//div[@id="content"]/h1/text()'),
            photo=get_attr(html, '//div[@id="headline"]/div[@class="pic"]//img/@src'),
            gender=bea_celebrity_info(get_tail(html, '//div[@id="headline"]/div[@class="info"]//span[text()="性别"]'))
        )
    except Exception as e:
        logger.exception("built_celebrity_by_id has exception:c_id:"+c_id)
        raise


def task_to_subject(task):
    logger.debug("======task_to_subject:begin,task:"+str(task))
    try:
        logger.debug("task_to_subject:session got")
        session = DBSession()
        year_task_in_session = session.query(Task).filter(Task.id == task.id).first()
        year_task_in_session.isScanned = True
        session.commit()
        if session.query(Subject).filter(Subject.id == task.url.split("/")[-2]).first() is not None:
            logger.debug("task_to_subject:subject(%s) is already in table" % task.url.split("/")[-2])
            session.close()
            return


        html = get_html(task.url)
        if get_inner_text(html, '//span[@class="year"]/text()') is not None:
            year = get_inner_text(html, '//span[@class="year"]/text()').replace("(", "").replace(")", "")
        else:
            year = None
        subject = Subject(
            id=task.url.split("/")[-2],
            title=get_inner_text(html, '//span[@property="v:itemreviewed"]/text()'),
            type="/".join(html.xpath('//span[@property="v:genre"]/text()')),
            product_nation=get_tail(html, '//span[@class="pl"][text()="制片国家/地区:"]'),
            language=get_tail(html, '//span[@class="pl"][text()="语言:"]'),
            premiere="/".join(html.xpath('//span[@property="v:initialReleaseDate"]/text()')),
            duration=get_attr(html, '//span[@property="v:runtime"]/@content'),
            rating_num=get_inner_text(html, '//strong[@property="v:average"]/text()'),
            rating_people=get_inner_text(html, '//span[@property="v:votes"]/text()'),
            periods=get_tail(html, '//span[@class="pl"][text()="集数:"]'),
            period_duration=get_tail(html, '//span[@class="pl"][text()="单集片长:"]'),
            photo=get_attr(html, '//img[@rel="v:image"][@title="点击看更多海报"]/@src'),
            year=year
        )
        session.add(subject)
        session.commit()
        for href in html.xpath('//a[@rel="v:directedBy"]/@href'):
            c_id = str(href).split("/")[-2];
            if c_id != "search":
                get_or_create_celebrity(c_id)
                subject.directors.append(session.query(Celebrity).filter(Celebrity.id == c_id).first())
                session.commit()

        for href in html.xpath('//a[@rel="v:starring"]/@href'):
            c_id = str(href).split("/")[-2];
            if c_id != "search":
                get_or_create_celebrity(c_id)
                subject.actors.append(session.query(Celebrity).filter(Celebrity.id == c_id).first())
                session.commit()

        if len(html.xpath('//span[@class="pl"][text()="编剧"]')) == 1:
            for href in html.xpath('//span[@class="pl"][text()="编剧"]')[0].getnext().xpath('a/@href'):
                c_id = str(href).split("/")[-2];
                if c_id != "search":
                    get_or_create_celebrity(c_id)
                    subject.screenwriters.append(session.query(Celebrity).filter(Celebrity.id == c_id).first())
                    session.commit()

        session.close()
        logger.debug("======task_to_subject:end,task:" + str(task))
    except Exception as e:
        logger.exception("task_to_subject has exception:task:"+task.url)

        year_task_in_session.isScanned = False
        session.commit()


def built_tasks_by_url(url):
    try:
        session = DBSession()
        html = get_html(url)
        subjects = html.xpath('//tr[@class="item"]/td/a[@class="nbg"]/@href')
        for subject in subjects:
            if session.query(Task).filter(Task.url == str(subject)).first() is None:
                task = Task(url=str(subject), isScanned=False)
                session.add(task)
                session.commit()
    except Exception as e:
        logger.exception("built_tasks_by_url has exception:url:"+url)
        raise
    finally:
        session.close()


def built_tasks_by_tag(year_tag):
    logger.debug("built_tasks_by_tag:begin;year_tag:"+str(year_tag))
    try:
        session = DBSession()
        year_tag_in_session = session.query(YearTag).filter(YearTag.id == year_tag.id).first()
        year_tag_in_session.isScanned = True
        session.commit()
        html = get_html("https://movie.douban.com/tag/%s?start=0&type=T" % year_tag.year)
        pages = html.xpath('//div[@class="paginator"]/a')
        max_page = 1 if len(pages) == 0 else int(pages[-1].text.strip())
        for x in range(year_tag_in_session.page, max_page):
            url = "https://movie.douban.com/tag/%s?start=%d&type=T" % (year_tag.year, x * 20)
            built_tasks_by_url(url)
            year_tag_in_session.page = x
            session.commit()
    except Exception as e:
        logger.exception("built_tasks_by_tag has exception:year_tag:"+year_tag.year)

        year_tag_in_session.isScanned = False
        session.commit()
    finally:
        session.close()


def built_all_tasks():
    logger.debug("built_all_tasks:begin")
    session = DBSession()
    for year_tag in session.query(YearTag).filter(YearTag.isScanned.is_(False)).all():
        built_tasks_by_tag(year_tag)
    session.close()


def built_all_subjects():
    logger.debug("built_all_subjects:begin")
    session = DBSession()
    logger.debug("built_all_subjects:session got")
    for task in session.query(Task).filter(and_(Task.isScanned.is_(False))).all():
        try:
            logger.debug("built_all_subjects:"+str(task))
            task_to_subject(task)
        except Exception as e:
            logger.error(e)
    session.close()


def main():
    built_all_subjects()


if __name__ == "__main__":
    main()
