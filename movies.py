from flask import Blueprint
from sqlalchemy import and_

from methods import *
from models import *

route_movie = Blueprint('movies', __name__)


@route_movie.route("/<mo_id>")
def showMovies(mo_id):
    # 点击增加热度
    Movie.query.filter(Movie.mo_id == mo_id).first().mo_heat += 3
    db.session.commit()
    # 登陆用户和未登陆用户的公共部分信息
    islogin = int(request.args.get('islogin'))
    value = dealwith_list_of_dict(to_list_of_dict(Movie.query.filter(Movie.mo_id == mo_id).first().comments))
    for i in range(len(value)):
        value[i]["user_name"] = Movie.query.filter(Movie.mo_id == mo_id).first().comments[i].user.u_name
        value[i]["user_picture"] = Movie.query.filter(Movie.mo_id == mo_id).first().comments[i].user.u_picture
    key = "comments"
    w_dict = to_dict_add_one_keyval(Movie.query.filter(Movie.mo_id == mo_id).first(), key, value[0:5])
    key2 = "tags"
    value2 = dealwith_list_of_dict(to_list_of_dict(Movie.query.filter(Movie.mo_id == mo_id).first().TagstoMovie))
    w_dict[key2] = value2
    w_dict["comments_num"] = len(value)
    # 登陆的用户还要返回自己的评论内容和时间
    if islogin == 0:
        return json.dumps(w_dict, ensure_ascii=False, cls=CJsonEncoder)
    else:
        u_id = int(request.args.get('session_id'))
        # 添加times
        add_times(mo_id, "Movie",u_id)
        # 添加 看过 想看 标签，和评论内容加分数
        value3 = dealwith_list_of_dict(to_list_of_dict(Markmovie.query.filter \
                                                           (and_(Markmovie.mark_user == u_id, \
                                                                 Markmovie.mark_movie == mo_id))))
        if len(value3) > 0:

            if value3[0]["seen_date"]:
                w_dict["is_seen"] = 1
                w_dict["is_want"] = 0
                value4 = dealwith_list_of_dict(to_list_of_dict(Commentmovie.query.filter \
                                                                   (and_(Commentmovie.com_user == u_id, \
                                                                         Commentmovie.com_movie == mo_id))))
                if len(value4) > 0:
                    w_dict["Comments"] = value4[0]
            elif not value3[0]["seen_date"] and value3[0]["want_date"]:
                w_dict["is_seen"] = 0
                w_dict["is_want"] = 1
            return json.dumps(w_dict, ensure_ascii=False, cls=CJsonEncoder)
        else:
            return json.dumps(w_dict, ensure_ascii=False, cls=CJsonEncoder)


@route_movie.route("/<mo_id>/comments")
def getMovieComments(mo_id):
    limit = int(request.args.get("limit"))
    offset = int(request.args.get("offset"))
    g_d = dealwith_list_of_dict(to_list_of_dict(Movie.query.filter(Movie.mo_id == mo_id).first().comments))
    for i in range(len(g_d)):
        g_d[i]["user_name"] = Movie.query.filter(Movie.mo_id == mo_id).first().comments[i].user.u_name
        g_d[i]["user_picture"] = Movie.query.filter(Movie.mo_id == mo_id).first().comments[i].user.u_picture
    w_d = g_d[offset:offset + limit]
    return json.dumps(w_d, ensure_ascii=False, cls=CJsonEncoder)


@route_movie.route("/want")
def getWantMovie():
    u_id = request.args.get("session_id")
    offset = int(request.args.get("offset"))
    limit = int(request.args.get("limit"))
    result = sortWant(User.query.filter(User.u_id == u_id).first().moviemarks)[offset:offset + limit]
    return dealwith_mergeList(result, "movie")


@route_movie.route("/seen")
def getSeenMovie():
    u_id = request.args.get("session_id")
    offset = int(request.args.get("offset"))
    limit = int(request.args.get("limit"))
    result = sortSeen(User.query.filter(User.u_id == u_id).first().moviemarks)[offset:offset + limit]
    return dealwith_mergeList(result, "movie")
