from methods import *
from music import route_music
from movies import route_movie
from books import route_book
import datetime

app.register_blueprint(route_music, url_prefix='/songs')
app.register_blueprint(route_movie, url_prefix='/movies')
app.register_blueprint(route_book, url_prefix='/books')


# @app.route("/movies/<mo_id>")
# def showMovies(mo_id):
#     value = dealwith_list_of_dict(to_list_of_dict(Movie.query.filter(Movie.mo_id == mo_id).first().comments))
#     key = "comments"
#     w_dict = to_dict_add_one_keyval(Movie.query.filter(Movie.mo_id == mo_id).first(), key, value)
#     key2 = "tags"
#     value2 = dealwith_list_of_dict(to_list_of_dict(Movie.query.filter(Movie.mo_id == mo_id).first().TagstoMovie))
#     w_dict[key2] = value2
#     return json.dumps(w_dict, ensure_ascii=False, cls=CJsonEncoder)


# @app.route("/songs/<mu_id>")
# def showMusic(mu_id):
#     value = dealwith_list_of_dict(to_list_of_dict(Music.query.filter(Music.mu_id == mu_id).first().comments))
#     key = "comments"
#     w_dict = to_dict_add_one_keyval(Music.query.filter(Music.mu_id == mu_id).first(), key, value)
#     return json.dumps(w_dict, ensure_ascii=False, cls=CJsonEncoder)


# @app.route("/books/<b_id>")
# def showBooks(b_id):
#     value = dealwith_list_of_dict(to_list_of_dict(Book.query.filter(Book.b_id == b_id).first().comments))
#     key = "comments"
#     w_dict = to_dict_add_one_keyval(Book.query.filter(Book.b_id == b_id).first(), key, value)
#     return json.dumps(w_dict, ensure_ascii=False, cls=CJsonEncoder)


# @app.route("/movies/<mo_id>/comments")
# def getMovieComments(mo_id):
#     limit = int(request.args.get("limit"))
#     offset = int(request.args.get("offset"))
#     w_d = dealwith_list_of_dict(
#         to_list_of_dict(Movie.query.filter(Movie.mo_id == mo_id).first().comments)[offset:offset + limit])
#     return json.dumps(w_d, ensure_ascii=False, cls=CJsonEncoder)


# @app.route("/songs/<mu_id>/comments")
# def getMusicComments(mu_id):
#     limit = int(request.args.get("limit"))
#     offset = int(request.args.get("offset"))
#     w_d = dealwith_list_of_dict(
#         to_list_of_dict(Music.query.filter(Music.mu_id == mu_id).first().comments)[offset:offset + limit])
#     return json.dumps(w_d, ensure_ascii=False, cls=CJsonEncoder)


# @app.route("/books/<b_id>/comments")
# def getBookComments(b_id):
#     limit = int(request.args.get("limit"))
#     offset = int(request.args.get("offset"))
#     w_d = dealwith_list_of_dict(
#         to_list_of_dict(Book.query.filter(Book.b_id == b_id).first().comments)[offset:offset + limit])
#     return json.dumps(w_d, ensure_ascii=False, cls=CJsonEncoder)


# @app.route("/movies/want")
# def getWantMovie():
#     u_id = request.args.get("session_id")
#     offset = int(request.args.get("offset"))
#     limit = int(request.args.get("limit"))
#     result = sortWant(User.query.filter(User.u_id == u_id).first().moviemarks)[offset:offset + limit]
#     return dealwith_mergeList(result, "movie")


# @app.route("/books/want")
# def getWantBook():
#     u_id = request.args.get("session_id")
#     offset = int(request.args.get("offset"))
#     limit = int(request.args.get("limit"))
#     result = sortWant(User.query.filter(User.u_id == u_id).first().bookmarks)[offset:offset + limit]
#     return dealwith_mergeList(result, "book")


# @app.route("/songs/want")
# def getWantMusic():
#     u_id = request.args.get("session_id")
#     offset = int(request.args.get("offset"))
#     limit = int(request.args.get("limit"))
#     result = sortWant(User.query.filter(User.u_id == u_id).first().musicmarks)[offset:offset + limit]
#     return dealwith_mergeList(result, "music")


# @app.route("/movies/seen")
# def getSeenMovie():
#     u_id = request.args.get("session_id")
#     offset = int(request.args.get("offset"))
#     limit = int(request.args.get("limit"))
#     result = sortSeen(User.query.filter(User.u_id == u_id).first().moviemarks)[offset:offset + limit]
#     return dealwith_mergeList(result, "movie")


# @app.route("/books/viewed")
# def getViewedBook():
#     u_id = request.args.get("session_id")
#     offset = int(request.args.get("offset"))
#     limit = int(request.args.get("limit"))
#     result = sortSeen(User.query.filter(User.u_id == u_id).first().bookmarks)[offset:offset + limit]
#     return dealwith_mergeList(result, "book")


# @app.route("/songs/listened")
# def getListenedMusic():
#     u_id = request.args.get("session_id")
#     offset = int(request.args.get("offset"))
#     limit = int(request.args.get("limit"))
#     result = sortSeen(User.query.filter(User.u_id == u_id).first().musicmarks)[offset:offset + limit]
#     return dealwith_mergeList(result, "music")

@app.route("/search")
def search():
    wd = request.args.get("wd")
    the_type = request.args.get("type")
    #
    offset = int(request.args.get("offset"))
    limit = int(request.args.get("limit"))
    if the_type in "Book":
        return likeSearch(Book, wd, "b_name", offset, limit)
    elif the_type in "Movie":
        return likeSearch(Movie, wd, "mo_name", offset, limit)
    elif the_type in "Song":
        return likeSearch(Music, wd, "mu_name", offset, limit)


@app.route("/want", methods=["POST"])
def want():
    data = request.get_json()
    i_type = data.get("type")
    i_id = data.get("id")
    u_id = data.get("session_id")
    user = User.query.filter_by(u_id=u_id).first()

    if i_type == "Movie":
        ismark = Markmovie.query.filter_by(mark_user=u_id, mark_movie=i_id).first()
        if not ismark:
            movie = Movie.query.filter_by(mo_id=i_id).first()
            mark = Markmovie()
            mark.mark_user = user.u_id
            mark.mark_movie = movie.mo_id
            mark.want_date = datetime.datetime.now()
            user.moviemarks.append(mark)
            movie.marks.append(mark)
            db.session.add(mark)
        else:
            return "no"

    elif i_type == "Song":
        ismark = Markmusic.query.filter_by(mark_user=u_id, mark_music=i_id).first()
        if not ismark:
            music = Music.query.filter_by(mu_id=i_id).first()
            mark = Markmusic()
            mark.mark_user = user.u_id
            mark.mark_music = music.mu_id
            mark.want_date = datetime.datetime.now()
            user.musicmarks.append(mark)
            music.marks.append(mark)
            db.session.add(mark)
        else:
            return "no"

    elif i_type == "Book":
        ismark = Markbook.query.filter_by(mark_user=u_id, mark_book=i_id).first()
        if not ismark:
            book = Book.query.filter_by(b_id=i_id).first()
            mark = Markbook()
            mark.mark_user = user.u_id
            mark.mark_book = book.b_id
            mark.want_date = datetime.datetime.now()
            user.bookmarks.append(mark)
            book.marks.append(mark)
            db.session.add(mark)
        else:
            return "no"
    else:
        return "type error"
    db.session.commit()
    return "ok"


# @app.route("/seen", methods=["POST"])
# def seen():
#     data = request.get_json()
#     i_type = data.get("type")
#     i_id = int(data.get("id"))
#     u_id = int(data.get("session_id"))
#     user = User.query.filter_by(u_id=u_id).first()
#     if i_type == "Movie":
#         ismark = Markmovie.query.filter_by(mark_user=u_id, mark_movie=i_id).first()
#         if not ismark:
#             movie = Movie.query.filter_by(mo_id=i_id).first()
#             mark = Markmovie()
#             mark.mark_user = user.u_id
#             mark.mark_movie = movie.mo_id
#             mark.seen_date = datetime.datetime.now()
#             user.moviemarks.append(mark)
#             movie.marks.append(mark)
#             db.session.add(mark)
#         elif not ismark.seen_date:
#             ismark.seen_date = datetime.datetime.now()
#         else:
#             return "no"
#     elif i_type == "Song":
#         ismark = Markmusic.query.filter_by(mark_user=u_id, mark_music=i_id).first()
#         if not ismark:
#             music = Music.query.filter_by(mu_id=i_id).first()
#             mark = Markmusic()
#             mark.mark_user = user.u_id
#             mark.mark_music = music.mu_id
#             mark.seen_date = datetime.datetime.now()
#             user.musicmarks.append(mark)
#             music.marks.append(mark)
#             db.session.add(mark)
#         elif not ismark.seen_date:
#             ismark.seen_date = datetime.datetime.now()
#         else:
#             return "no"
#     elif i_type == "Book":
#         ismark = Markbook.query.filter_by(mark_user=u_id, mark_book=i_id).first()
#         if not ismark:
#             book = Book.query.filter_by(b_id=i_id).first()
#             mark = Markbook()
#             mark.mark_user = user.u_id
#             mark.mark_book = book.b_id
#             mark.seen_date = datetime.datetime.now()
#             user.bookmarks.append(mark)
#             book.marks.append(mark)
#             db.session.add(mark)
#         elif not ismark.seen_date:
#             ismark.seen_date = datetime.datetime.now()
#         else:
#             return "no"
#     else:
#         return "type error"
#     db.session.commit()
#     return "ok"


@app.route("/comment", methods=["POST"])
def comment():
    data = request.get_json()
    i_type = data.get('type')
    i_id = int(data.get('id'))
    u_id = data.get('session_id')
    i_comment = data.get('comment')
    score = data.get('score')
    user = User.query.filter_by(u_id=u_id).first()

    if i_type == "Movie":
        flag = False
        for com in user.moviecomments:
            if com.com_movie == i_id:
                cm = Commentmovie.query.filter_by(com_movie=i_id, com_user=u_id).first()
                cm.comment = i_comment
                cm.score = score
                cm.date = datetime.datetime.now()
                return "update"
        if not flag:
            cm = Commentmovie()
            movie = Movie.query.filter_by(mo_id=i_id).first()
            cm.com_user = u_id
            cm.com_movie = i_id
            cm.comment = i_comment
            cm.score = score
            user.moviecomments.append(cm)
            movie.comments.append(cm)
            db.session.add(cm)
            seen(i_type, u_id, i_id)
        else:
            return "no"
    elif i_type == "Song":
        flag = False
        for com in user.musiccomments:
            if com.com_music == i_id:
                cm = Commentmusic.query.filter_by(com_music=i_id, com_user=u_id).first()
                cm.comment = i_comment
                cm.score = score
                cm.date = datetime.datetime.now()
                return "update"
        if not flag:
            cm = Commentmusic()
            music = Music.query.filter_by(mu_id=i_id).first()
            cm.com_user = user.u_id
            cm.com_movie = i_id
            cm.comment = i_comment
            cm.score = score
            music.comments.append(cm)
            db.session.add(cm)
            user.musiccomments.append(cm)
            seen(i_type, u_id, i_id)
        else:
            return "no"
    elif i_type == "Book":
        flag = False
        for com in user.bookcomments:
            if com.com_book == i_id:
                cm = Commentbook.query.filter_by(com_book=i_id, com_user=u_id).first()
                cm.comment = i_comment
                cm.score = score
                cm.date = datetime.datetime.now()
                return "update"
        if not flag:
            cm = Commentbook()
            book = Book.query.filter_by(b_id=i_id).first()
            cm.com_user = user.u_id
            cm.com_movie = i_id
            cm.comment = i_comment
            cm.score = score
            book.comments.append(cm)
            user.bookcomments.append(cm)
            db.session.add(cm)
            seen(i_type, u_id, i_id)
        else:
            return "no"
    else:
        return "type error"
    db.session.commit()
    return "ok"


@app.route("/rank")
def rank():
    return to_json(merge_rank(take_col(showNewMovie()), take_col(searchHot(Movie)), take_col(searchHot(Book)),
                              take_col(searchHot(Music))))


@app.route("/login", methods=['POST', 'GET'])
def login():
    data = request.get_json()
    code = data.get("code")
    user = data.get("user")
    name = user.get("nickName")
    avatar_url = user.get("avatarUrl")
    # 通过得到的code 和 avatarUrl向微信服务器请求session_id,经过处理后返回给前
    appid = "wx64a1acbd25ba6342"
    secret = "3bc02e157777a7438b5e45d5cb160bfc"
    url = get_url(appid, secret, code)
    user_data = send_request(url)
    ret = {"openid": ""}
    openid = user_data['openid']
    list_u = User.query.filter(User.u_openid == openid).first()
    if not list_u:
        user = User()
        user.u_picture = avatar_url
        user.u_openid = openid
        user.u_name = name
        db.session.add(user)
        db.session.commit()
        u_id = to_list_of_dict(User.query.filter(User.u_openid == openid))[0]["u_id"]
    else:
        u_id = to_list_of_dict(User.query.filter(User.u_openid == openid))[0]["u_id"]
    ret["openid"] = u_id
    return json.dumps(ret, ensure_ascii=False)


@app.route("/users/<u_id>/comments")
def getUserComments(u_id):
    limit = int(request.args.get("limit"))
    offset = int(request.args.get("offset"))
    w_dict = {}
    key_1 = "movies"
    vaule_1 = dealwith_list_of_dict(to_list_of_dict(User.query.filter(User.u_id == u_id).first().moviecomments))
    for i in range(len(vaule_1)):
        vaule_1[i]["mo_name"] = User.query.filter(User.u_id == u_id).first().moviecomments[i].movie.mo_name
        vaule_1[i]["mo_picture"] = User.query.filter(User.u_id == u_id).first().moviecomments[i].movie.mo_picture
    w_dict[key_1] = vaule_1[offset:offset + limit]
    key_2 = "songs"
    vaule_2 = dealwith_list_of_dict(to_list_of_dict(User.query.filter(User.u_id == u_id).first().musiccomments))
    for i in range(len(vaule_2)):
        vaule_2[i]["mu_name"] = User.query.filter(User.u_id == u_id).first().musiccomments[i].music.mu_name
        vaule_2[i]["mu_picture"] = User.query.filter(User.u_id == u_id).first().musiccomments[i].music.mu_picture
    w_dict[key_2] = vaule_2[offset:offset + limit]
    key_3 = "books"
    vaule_3 = dealwith_list_of_dict(to_list_of_dict(User.query.filter(User.u_id == u_id).first().bookcomments))
    for i in range(len(vaule_3)):
        vaule_3[i]["b_name"] = User.query.filter(User.u_id == u_id).first().bookcomments[i].book.b_name
        vaule_3[i]["b_picture"] = User.query.filter(User.u_id == u_id).first().bookcomments[i].book.b_picture
    w_dict[key_3] = vaule_3[offset:offset + limit]
    return json.dumps(w_dict, ensure_ascii=False, cls=CJsonEncoder)


@app.route("/users/<u_id>/recommends")
def recommend(u_id):
    u_id = int(u_id)
    user = User.query.filter(User.u_id == u_id).first()
    print(user)
    movies = dealwith_list_of_dict(to_list_of_dict(user.recommendmovies))
    music = dealwith_list_of_dict(to_list_of_dict(user.recommendmusic))
    books = dealwith_list_of_dict(to_list_of_dict(user.recommendbook))
    # offset = int(request.args.get("offset"))
    # limit = int(request.args.get("limit"))
    result = {"movies":movies,"music":music,"books":books}
    return json.dumps(result,ensure_ascii=False)



if __name__ == '__main__':
    app.run(debug=True)
