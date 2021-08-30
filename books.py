from flask import Blueprint
from sqlalchemy import and_

from methods import *
from models import *

route_book = Blueprint('books', __name__)


@route_book.route("/<b_id>")
def showBooks(b_id):
    # 点击书籍后热度增加
    Book.query.filter(Book.b_id == b_id).first().b_heat += 3
    db.session.commit()
    # 登陆用户和未登陆用户的公共部分信息
    islogin = int(request.args.get('islogin'))
    value = dealwith_list_of_dict(to_list_of_dict(Book.query.filter(Book.b_id == b_id).first().comments))
    for i in range(len(value)):
        value[i]["user_name"] = Book.query.filter(Book.b_id == b_id).first().comments[i].user.u_name
        value[i]["user_picture"] = Book.query.filter(Book.b_id == b_id).first().comments[i].user.u_picture
    key = "comments"
    w_dict = to_dict_add_one_keyval(Book.query.filter(Book.b_id == b_id).first(), key, value[0:5])
    key2 = "tags"
    value2 = dealwith_list_of_dict(to_list_of_dict(Book.query.filter(Book.b_id == b_id).first().TagstoBook))
    w_dict[key2] = value2
    w_dict["comments_num"] = len(value)
    # 登陆的用户还要返回自己的评论内容和时间
    if islogin == 0:
        return json.dumps(w_dict, ensure_ascii=False, cls=CJsonEncoder)
    else:
        u_id = int(request.args.get('session_id'))
        # 加times
        add_times(b_id, "Book", u_id)
        # 添加 看过 想看 标签，和评论内容加分数
        value3 = dealwith_list_of_dict(to_list_of_dict(Markbook.query.filter \
                                                           (and_(Markbook.mark_user == u_id, \
                                                                 Markbook.mark_book == b_id))))
        if len(value3) > 0:

            if value3[0]["seen_date"]:
                w_dict["is_seen"] = 1
                w_dict["is_want"] = 0
                value4 = dealwith_list_of_dict(to_list_of_dict(Commentbook.query.filter \
                                                                   (and_(Commentbook.com_user == u_id, \
                                                                         Commentbook.com_book == b_id))))
                if len(value4) > 0:
                    w_dict["Comments"] = value4[0]
            elif not value3[0]["seen_date"] and value3[0]["want_date"]:
                w_dict["is_seen"] = 0
                w_dict["is_want"] = 1
            return json.dumps(w_dict, ensure_ascii=False, cls=CJsonEncoder)
        else:
            return json.dumps(w_dict, ensure_ascii=False, cls=CJsonEncoder)


@route_book.route("/<b_id>/comments")
def getBookComments(b_id):
    limit = int(request.args.get("limit"))
    offset = int(request.args.get("offset"))
    g_d = dealwith_list_of_dict(to_list_of_dict(Book.query.filter(Book.b_id == b_id).first().comments))
    for i in range(len(g_d)):
        g_d[i]["user_name"] = Book.query.filter(Book.b_id == b_id).first().comments[i].user.u_name
        g_d[i]["user_picture"] = Book.query.filter(Book.b_id == b_id).first().comments[i].user.u_picture
    w_d = g_d[offset:offset + limit]
    return json.dumps(w_d, ensure_ascii=False, cls=CJsonEncoder)


@route_book.route("/want")
def getWantBook():
    u_id = request.args.get("session_id")
    offset = int(request.args.get("offset"))
    limit = int(request.args.get("limit"))
    result = sortWant(User.query.filter(User.u_id == u_id).first().bookmarks)[offset:offset + limit]
    return dealwith_mergeList(result, "book")


@route_book.route("/viewed")
def getViewedBook():
    u_id = request.args.get("session_id")
    offset = int(request.args.get("offset"))
    limit = int(request.args.get("limit"))
    result = sortSeen(User.query.filter(User.u_id == u_id).first().bookmarks)[offset:offset + limit]
    return dealwith_mergeList(result, "book")
