from flask import Blueprint
from sqlalchemy import and_

from methods import *
from models import *

route_music = Blueprint('songs', __name__)


@route_music.route("/<mu_id>")
def showMusic(mu_id):
    # 点击增加热度
    Music.query.filter(Music.mu_id == mu_id).first().mu_heat += 3
    db.session.commit()
    # 登陆用户和未登陆用户的公共部分信息
    islogin = int(request.args.get('islogin'))
    value = dealwith_list_of_dict(to_list_of_dict(Music.query.filter(Music.mu_id == mu_id).first().comments))
    for i in range(len(value)):
        value[i]["user_name"] = Music.query.filter(Music.mu_id == mu_id).first().comments[i].user.u_name
        value[i]["user_picture"] = Music.query.filter(Music.mu_id == mu_id).first().comments[i].user.u_picture
    key = "comments"
    w_dict = to_dict_add_one_keyval(Music.query.filter(Music.mu_id == mu_id).first(), key, value[0:5])
    key2 = "tags"
    value2 = dealwith_list_of_dict(to_list_of_dict(Music.query.filter(Music.mu_id == mu_id).first().TagstoMusic))
    w_dict[key2] = value2
    w_dict["comments_num"] = len(value)
    # 登陆的用户还要返回自己的评论内容和时间
    if islogin == 0:
        return json.dumps(w_dict, ensure_ascii=False, cls=CJsonEncoder)
    else:
        u_id = int(request.args.get('session_id'))
        # 添加times
        add_times(mu_id, "Music", u_id)
        # 添加 看过 想看 标签，和评论内容加分数
        value3 = dealwith_list_of_dict(to_list_of_dict(Markmusic.query.filter \
                                                           (and_(Markmusic.mark_user == u_id, \
                                                                 Markmusic.mark_music == mu_id))))
        if len(value3) > 0:

            if value3[0]["seen_date"]:
                w_dict["is_seen"] = 1
                w_dict["is_want"] = 0
                value4 = dealwith_list_of_dict(to_list_of_dict(Commentmusic.query.filter \
                                                                   (and_(Commentmusic.com_user == u_id, \
                                                                         Commentmusic.com_music == mu_id))))
                if len(value4) > 0:
                    w_dict["Comments"] = value4[0]
            elif not value3[0]["seen_date"] and value3[0]["want_date"]:
                w_dict["is_seen"] = 0
                w_dict["is_want"] = 1
            return json.dumps(w_dict, ensure_ascii=False, cls=CJsonEncoder)
        else:
            return json.dumps(w_dict, ensure_ascii=False, cls=CJsonEncoder)


@route_music.route("/<mu_id>/comments")
def getMusicComments(mu_id):
    limit = int(request.args.get("limit"))
    offset = int(request.args.get("offset"))
    g_d = dealwith_list_of_dict(to_list_of_dict(Music.query.filter(Music.mu_id == mu_id).first().comments))
    for i in range(len(g_d)):
        g_d[i]["user_name"] = Music.query.filter(Music.mu_id == mu_id).first().comments[i].user.u_name
        g_d[i]["user_picture"] = Music.query.filter(Music.mu_id == mu_id).first().comments[i].user.u_picture
    w_d = g_d[offset:offset + limit]
    return json.dumps(w_d, ensure_ascii=False, cls=CJsonEncoder)


@route_music.route("/want")
def getWantMusic():
    u_id = request.args.get("session_id")
    offset = int(request.args.get("offset"))
    limit = int(request.args.get("limit"))
    result = sortWant(User.query.filter(User.u_id == u_id).first().musicmarks)[offset:offset + limit]
    return dealwith_mergeList(result, "music")


@route_music.route("/listened")
def getListenedMusic():
    u_id = request.args.get("session_id")
    offset = int(request.args.get("offset"))
    limit = int(request.args.get("limit"))
    result = sortSeen(User.query.filter(User.u_id == u_id).first().musicmarks)[offset:offset + limit]
    return dealwith_mergeList(result, "music")