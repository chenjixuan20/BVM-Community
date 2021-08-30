import re

from sqlalchemy import and_

from models import *
import json
import datetime
import requests
import operator


# 处理JSON中的datetime格式
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


# 去除字典值中的空格和转移字符
def remove_redundancy(dic: dict):
    for key in dic:
        if type(dic[key]) is str:
            dic[key] = ''.join(dic[key].split())
    return dic


# 将字典的列表转化成json
def to_json(objects):
    return json.dumps(objects, ensure_ascii=False, cls=CJsonEncoder)


# 将对象的列表转化为字典的列表，列表的内容是每一个对象“属性：值”的字典
def to_list_of_dict(objects):
    result = []
    for obj in objects:
        dict = obj.__dict__
        # if "_sa_instance_state" in dict:
        #     del dict["_sa_instance_state"]
        remove_redundancy(dict)
        result.append(dict)
    return result


# 将对象转成字典，并且在字典内加入一个键值对
def to_dict_add_one_keyval(objects, key, value):
    dict = objects.__dict__
    dict[key] = value
    if "_sa_instance_state" in dict:
        del dict["_sa_instance_state"]
    return dict


# 对象转成字典
def to_dict(obj):
    dict = obj.__dict__
    remove_redundancy(dict)
    return dict


# 合并两个字典，用于返回seen want
def to_expend_dict(d_1: dict, d_2: dict):
    z = d_2.copy()
    z.update(d_1)
    return z


# 返回obj表中所有的信息，并将信息转化为字典
def selectAll(obj):
    list = to_list_of_dict(obj.query.all())
    result = to_json(list)
    return result


def selectById(obj, id):
    list = to_list_of_dict(obj.query.get(id).to_json())
    result = to_json(list)
    return result


def likeSearch(obj, like, attribution, offset, limit):
    s_str = obj.getMyName(obj).lower() + '.' + attribution + ' like("%' + like + '%")'
    result = to_json(dealwith_list_of_dict(to_list_of_dict(obj.query.filter(text(s_str)).limit(limit).offset(offset))))
    return result


def searchHot(obj):
    obj_name = obj.getMyName(obj)
    if obj_name is "Book":
        s_name = "-b_heat"
    elif obj_name is "Movie":
        s_name = "-mo_heat"
    elif obj_name is "Music":
        s_name = "-mu_heat"
    result = dealwith_list_of_dict(to_list_of_dict(obj.query.order_by(text(s_name)).limit(10)))
    return result


def sortWant(a_list):
    result = []
    for i in range(len(a_list)):
        if not a_list[i].seen_date:
            result.append(a_list[i])
    return order_by_wantdate(result)


def sortSeen(a_list):
    result = []
    for i in range(len(a_list)):
        if a_list[i].seen_date:
            result.append(a_list[i])
    return result


def dealwith_list_of_dict(list_of_dict):
    for j in range(len(list_of_dict)):
        if "movie" in list_of_dict[j]:
            del list_of_dict[j]["movie"]
        if "music" in list_of_dict[j]:
            del list_of_dict[j]["music"]
        if "book" in list_of_dict[j]:
            del list_of_dict[j]["book"]
        if "_sa_instance_state" in list_of_dict[j]:
            del list_of_dict[j]["_sa_instance_state"]
    return list_of_dict


def dealwith_mergeList(listofdic, what):
    w_d = []
    if what in "movie":
        for i in range(len(listofdic)):
            w_d.append(listofdic[i])
            w_d.append(listofdic[i].movie)
    if what in "music":
        for i in range(len(listofdic)):
            w_d.append(listofdic[i])
            w_d.append(listofdic[i].music)
    if what in "book":
        for i in range(len(listofdic)):
            w_d.append(listofdic[i])
            w_d.append(listofdic[i].book)
    list_of_dict = to_list_of_dict(w_d)
    list_of_dict = dealwith_list_of_dict(list_of_dict)

    merge_list = []
    for m in range(0, len(list_of_dict), 2):
        merge_list.append(to_expend_dict(list_of_dict[m], list_of_dict[m + 1]))
    return to_json(merge_list)


def take_col(list_of_dict):
    result = []
    # print(len(list_of_dict))
    for i in range(len(list_of_dict)):
        temp = {}
        for key in list_of_dict[i]:
            if key.endswith('id'):
                temp[key] = list_of_dict[i][key]
            if key.endswith('name'):
                temp[key] = list_of_dict[i][key]
            if key.endswith('picture'):
                temp[key] = list_of_dict[i][key]
        result.append(temp)
    return result


def merge_rank(new_mo, hot_mo, hot_book, hot_mu):
    rank = {}
    rank["new_movies"] = new_mo
    rank["hot_movies"] = hot_mo
    rank["hot_books"] = hot_book
    rank["hot_music"] = hot_mu
    return rank


def get_url(appid, secret, js_code, grant_type="authorization_code"):
    new_url = "https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_co" \
              "de=%s&grant_type=%s" % (appid, secret, js_code, grant_type)

    return new_url


def send_request(url):
    response = requests.get(url)
    data = json.loads(response.content)
    return data


def showNewMovie():
    movie_date = db.session.query(Movie.mo_date, Movie.mo_id).all()
    list_len = len(movie_date)
    now_date = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
    date_spacing = datetime.timedelta(days=28)
    latest_date = now_date - date_spacing
    new_movie_list = []
    for i in range(list_len):
        if re.search(r"(\d{4}-\d{1,2}-\d{1,2})", movie_date[i][0]):
            date = datetime.datetime.strptime(str(movie_date[i][0][0:10]), '%Y-%m-%d')
        elif re.search(r"(\d{4}-\d{1,2})", movie_date[i][0]):
            date = datetime.datetime.strptime(str(movie_date[i][0][0:7]), '%Y-%m')
        elif re.search(r"(\d{4}-\d{1,2})", movie_date[i][0]):
            date = datetime.datetime.strptime(str(movie_date[i][0][0:4]), '%Y')
        else:
            continue
        if latest_date < date < now_date:
            new_movie_list.append(Movie.query.filter(Movie.mo_id == movie_date[i][1]).first())
    list_of_dict = to_list_of_dict(new_movie_list)
    list_of_dict = dealwith_list_of_dict(list_of_dict)
    return list_of_dict[0:10]


def seen(i_type, u_id, i_id):
    user = User.query.filter_by(u_id=u_id).first()
    if i_type == "Movie":
        ismark = Markmovie.query.filter_by(mark_user=u_id, mark_movie=i_id).first()
        if not ismark:
            movie = Movie.query.filter_by(mo_id=i_id).first()
            mark = Markmovie()
            mark.mark_user = user.u_id
            mark.mark_movie = movie.mo_id
            mark.seen_date = datetime.datetime.now()
            user.moviemarks.append(mark)
            movie.marks.append(mark)
            db.session.add(mark)
        elif not ismark.seen_date:
            ismark.seen_date = datetime.datetime.now()
        else:
            return "no"
    elif i_type == "Song":
        ismark = Markmusic.query.filter_by(mark_user=u_id, mark_music=i_id).first()
        if not ismark:
            music = Music.query.filter_by(mu_id=i_id).first()
            mark = Markmusic()
            mark.mark_user = user.u_id
            mark.mark_music = music.mu_id
            mark.seen_date = datetime.datetime.now()
            user.musicmarks.append(mark)
            music.marks.append(mark)
            db.session.add(mark)
        elif not ismark.seen_date:
            ismark.seen_date = datetime.datetime.now()
        else:
            return "no"
    elif i_type == "Book":
        ismark = Markbook.query.filter_by(mark_user=u_id, mark_book=i_id).first()
        if not ismark:
            book = Book.query.filter_by(b_id=i_id).first()
            mark = Markbook()
            mark.mark_user = user.u_id
            mark.mark_book = book.b_id
            mark.seen_date = datetime.datetime.now()
            user.bookmarks.append(mark)
            book.marks.append(mark)
            db.session.add(mark)
        elif not ismark.seen_date:
            ismark.seen_date = datetime.datetime.now()
        else:
            return "no"
    else:
        return "type error"

    db.session.commit()
    return "ok"


def add_times(t_id, i_type, u_id):
    if i_type is "Book":
        if UserClickBook.query.filter(and_(UserClickBook.b_id == t_id, UserClickBook.u_id == u_id)).all():
            UserClickBook.query.filter(and_(UserClickBook.b_id == t_id, UserClickBook.u_id == u_id)).first().times += 1
        else:
            user_click_book = UserClickBook()
            user_click_book.u_id = u_id
            user_click_book.b_id = t_id
            user_click_book.times = 1
            db.session.add(user_click_book)
            db.session.commit()
    if i_type is "Music":
        if UserClickMusic.query.filter(and_(UserClickMusic.mu_id == t_id, UserClickMusic.u_id == u_id)).all():
            UserClickMusic.query.filter(and_(UserClickMusic.mu_id == t_id, UserClickMusic.u_id == u_id)).first().times += 1
        else:
            user_click_music = UserClickMusic()
            user_click_music.u_id = u_id
            user_click_music.mu_id = t_id
            user_click_music.times = 1
            db.session.add(user_click_music)
            db.session.commit()
    if i_type is "Movie":
        if UserClickMovie.query.filter(and_(UserClickMovie.mo_id == t_id, UserClickMovie.u_id == u_id)).all():
            UserClickMovie.query.filter(and_(UserClickMovie.mo_id == t_id, UserClickMovie.u_id == u_id)).first().times += 1
        else:
            user_click_movie = UserClickMovie()
            user_click_movie.u_id = u_id
            user_click_movie.mo_id = t_id
            user_click_movie.times = 1
            db.session.add(user_click_movie)
            db.session.commit()
    return 0


def order_by_wantdate(list_of_object):
    have_date = []
    cmpfun = operator.attrgetter('want_date')
    null_date = []
    for i in range(len(list_of_object)):
        if not list_of_object[i].want_date:
            null_date.append(list_of_object[i])
        else:
            have_date.append(list_of_object[i])
    have_date.sort(key = cmpfun,reverse=True)
    have_date = have_date+null_date
    return have_date
