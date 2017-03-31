from dbUtil import DBSession
from entity import YearTag, Task, Celebrity, Subject, Proxy
from httpUtil import get_html, get_inner_text, get_tail, get_attr, bea_celebrity_info
from sfdblog import logger


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
    # logger.info("星座：" +
    #             bea_celebrity_info(get_tail(html, '//div[@id="headline"]/div[@class="info"]//span[text()="星座"]')))
    # logger.info("出生日期：" +
    #             bea_celebrity_info(get_tail(html, '//div[@id="headline"]/div[@class="info"]//span[text()="出生日期"]')))
    # logger.info("出生地：" +
    #             bea_celebrity_info(get_tail(html, '//div[@id="headline"]/div[@class="info"]//span[text()="出生地"]')))
    # logger.info("职业：" +
    #             bea_celebrity_info(get_tail(html, '//div[@id="headline"]/div[@class="info"]//span[text()="职业"]')))
    # logger.info("更多外文名：" +
    #             bea_celebrity_info(get_tail(html, '//div[@id="headline"]/div[@class="info"]//span[text()="更多外文名"]')))
    # logger.info("名字：" +
    #             get_inner_text(html, '//div[@id="content"]/h1/text()'))
    # logger.info("性别：" +
    #             bea_celebrity_info(get_tail(html, '//div[@id="headline"]/div[@class="info"]//span[text()="性别"]')))
    # logger.info("图片：" +
    #             get_attr(html, '//div[@id="headline"]/div[@class="pic"]//img/@src'))


def task_to_subject(task):
    try:
        session = DBSession()
        year_task_in_session = session.query(Task).filter(Task.id == task.id).first()
        if session.query(Subject).filter(Subject.id == task.url.split("/")[-2]).first() is not None:
            session.close()
            return
        year_task_in_session.isScanned = True
        session.commit()

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
            year=get_inner_text(html, '//span[@class="year"]/text()').replace("(", "").replace(")", "")
        )
    # logger.info("标题：" + get_inner_text(html, '//span[@property="v:itemreviewed"]/text()'))
    # logger.info("评分：" + get_inner_text(html, '//strong[@property="v:average"]/text()'))
    # logger.info("评价人数：" + get_inner_text(html, '//span[@property="v:votes"]/text()'))
    # logger.info("类型：" + "/".join(html.xpath('//span[@property="v:genre"]/text()')))
    # logger.info("制片国家/地区：" + get_tail(html, '//span[@class="pl"][text()="制片国家/地区:"]'))
    # logger.info("语言:" + get_tail(html, '//span[@class="pl"][text()="语言:"]'))
    # logger.info("年份:" + get_inner_text(html, '//span[@class="year"]/text()').replace("(", "").replace(")", ""))
    # logger.info("上映时间：" + "/".join(html.xpath('//span[@property="v:initialReleaseDate"]/text()')))
    # logger.info("片长:" + get_attr(html, '//span[@property="v:runtime"]/@content'))
    # logger.info("海报:" + get_attr(html, '//img[@rel="v:image"][@title="点击看更多海报"]/@src'))
    # logger.info("集数：" + get_tail(html, '//span[@class="pl"][text()="集数:"]'))
    # logger.info("单集片长:" + get_tail(html, '//span[@class="pl"][text()="单集片长:"]'))

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
            if session.query(Task).filter(Task.url == url).first() is not None:
                pass
            task = Task(url=str(subject), isScanned=False)
            session.add(task)
            session.commit()
    except Exception as e:
        logger.exception("built_tasks_by_url has exception:url:"+url)
        raise
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
        logger.exception("built_tasks_by_tag has exception:year_tag:"+year_tag.year)

        year_tag_in_session.isScanned = False
        session.commit()
    finally:
        session.close()


def built_all_tasks():
    session = DBSession()
    for year_tag in session.query(YearTag).filter(YearTag.isScanned.is_(False)).all():
        built_tasks_by_tag(year_tag)
    session.close()


def built_all_subjects():
    session = DBSession()
    for task in session.query(Task).filter(Task.isScanned.is_(False)).all():
        try:
            task_to_subject(task)
        except Exception as e:
            pass
    session.close()


def main():
    # built_all_tasks()
    # session = DBSession()
    # task = Task(url="https://movie.douban.com/subject/25921812/", isScanned=False)
    # session.add(task)
    # session.commit()
    # session.close()
    # task_to_subject(task)
    # session.add(built_celebrity_by_id("1363486"))
    # session.commit()
    # built_all_subjects()
    # for x in range(1890 , 2020):
    #     print("INSERT INTO `douban`.`year_tag`(`year`,`page`,`isScanned`)VALUES(%d,0,0);" % x)
    # html = get_html("http://www.proxy360.cn/Region/Taiwan")
    # proxies = html.xpath('//div[@style="float:left; display:block; width:630px;"]')
    # session = DBSession()
    # for proxy in proxies:
    #     proxy_b = Proxy(
    #         ip=proxy.xpath('./span')[0].text.strip(),
    #         port=proxy.xpath('./span')[1].text.strip(),
    #         status="unUsed"
    #     )
    #     session.add(proxy_b)
    #     session.commit()
    # session.close()
    # session = DBSession()
    # for proxy in session.query(Proxy).all():
    #     pstr = 'http://113.121.246.193:808'
    proxies = {
        'http': 'http://115.215.49.245:37746',
        'https': 'http://115.215.49.245:37746'
    }
    html = get_html("https://movie.douban.com/subject/26602933/?from=showing", proxies)
    # session.close()

if __name__ == "__main__":
    main()
