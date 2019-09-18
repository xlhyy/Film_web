import qrcode
import time
from PIL import Image
from django.http import HttpResponse
from django.shortcuts import render
from six import BytesIO

from Film_App.models import FilmInfo, UserInfo, CollectInfo, ZanOrCaiInfo, CommentInfo, BarrageInfo


def index(request):
    type_list = getList(request)
    if request.method == "GET":
        type = str(request.GET.get("type"))
        is_login = request.GET.get("is_login")

        if is_login == 'False':
            request.session['login_status'] = False

        if type == "None":
            obj = FilmInfo.objects.all()
            request.session['now_type'] = '全部'
        elif type == '全部':
            obj = FilmInfo.objects.all()
            request.session['now_type'] = '全部'
        else:
            obj = FilmInfo.objects.filter(types__contains=str(type))
            request.session['now_type'] = str(type)
    temp = []
    for i in obj:
        temp.append(i)
    bubble_sort(temp)
    return render(request, 'index.html', {'obj':temp, 'type_list':type_list})

def logout(request):
    request.session['login_status'] = False
    type_list = getList(request)
    if request.method == "GET":
        type = str(request.GET.get("type"))
        if type == "None":
            obj = FilmInfo.objects.all()
        elif type == '全部':
            obj = FilmInfo.objects.all()
        else:
            obj = FilmInfo.objects.filter(types__contains=str(type))
    temp = []
    for i in obj:
        temp.append(i)
    bubble_sort(temp)
    return render(request,'index.html',{'obj':temp, 'type_list':type_list})

    # DZ = []
    # ZZ = []
    # KH = []
    # XY = []
    # XJ = []
    # AQ = []
    # LZ = []
    # DH = []
    # JS = []
    # FZ = []
    # QS = []
    # JL = []
    # JQ = []
    # for i in obj:
    #     if '动作' in i.types:
    #         DZ.append(i)
    #     if '战争' in i.types:
    #         ZZ.append(i)
    #     if '科幻' in i.types:
    #         KH.append(i)
    #     if '悬疑' in i.types:
    #         XY.append(i)
    #     if '喜剧' in i.types:
    #         XJ.append(i)
    #     if '爱情' in i.types:
    #         AQ.append(i)
    #     if '励志' in i.types:
    #         LZ.append(i)
    #     if '动画' in i.types:
    #         DH.append(i)
    #     if '惊悚' in i.types:
    #         JS.append(i)
    #     if '犯罪' in i.types:
    #         FZ.append(i)
    #     if '情色' in i.types:
    #         QS.append(i)
    #     if '记录' in i.types:
    #         JL.append(i)
    #     if '剧情' in i.types:
    #         JQ.append(i)
    #
    # bubble_sort(DZ)
    # bubble_sort(ZZ)
    # bubble_sort(KH)
    # bubble_sort(XY)
    # bubble_sort(XJ)
    # bubble_sort(AQ)
    # bubble_sort(LZ)
    # bubble_sort(DH)
    # bubble_sort(JS)
    # bubble_sort(FZ)
    # bubble_sort(QS)
    # bubble_sort(JL)
    # bubble_sort(JQ)
    # return render(request, "index.html", {"DZ":DZ,"ZZ":ZZ,"KH":KH,"XY":XY,"XJ":XJ,"AQ":AQ,"LZ":LZ,\
    #
    #                                   "DH":DH,"JS":JS,"FZ":FZ,"QS":QS,"JL":JL,"JQ":JQ,'type_list':type_list})


# 冒泡排序
def bubble_sort(l):
    n = len(l)
    for i in range(1, n): #1,n或n-1 -- i:0,1,2...
        count = 0
        for j in range(n-i): #j:0,1,2...  n-1,n-2,n-3..1
            if l[j].grades < l[j+1].grades:
                l[j], l[j+1] = l[j+1], l[j]
                count += 1
        if count == 0:
            break

def getList(request):
    new_list = []
    new_dict = {}
    needed_types = []
    obj = FilmInfo.objects.only('types')
    for i in obj:
        temp_list =  str(i.types).split(' / ')
        for j in temp_list:
            if j not in new_list and temp_list is not ' ':
                new_list.append(j)
                new_dict.setdefault(j, 1)
            else:
                new_dict[j] += 1
    sorted_list = sorted(new_dict.items(), key=lambda x:x[1], reverse=True)
    needed_types.append('全部')
    for i in sorted_list:
        if i[0] != ' ':
            needed_types.append(i[0])
    finally_list = []
    for i in range(13):
        finally_list.append(needed_types[i])
    return finally_list

def getInfo(request):
    if request.method == "GET":
        name = str(request.GET.get("name"))
        infos = FilmInfo.objects.filter(names=name)
        content = {'infos': infos[0]}

        if name in request.session['collect_film']:
            content['is_collect'] = True

        content['is_login'] = True

        user = request.session['user']
        ZanObj = ZanOrCaiInfo.objects.filter(film_name=name, user_name=user, status='like')
        CaiObj = ZanOrCaiInfo.objects.filter(film_name=name, user_name=user, status='hate')
        if CaiObj:
            request.session['cai_status'] = 'a_hate'
        else:
            request.session['cai_status'] = 'd_hate'
        if ZanObj:
            request.session['zan_status'] = 'a_like'
        else:
            request.session['zan_status'] = 'd_like'

        zan_count = len(ZanOrCaiInfo.objects.filter(film_name=name,status='like'))
        cai_count = len(ZanOrCaiInfo.objects.filter(film_name=name,status='hate'))

        content['zan_count'] = zan_count
        content['cai_count'] = cai_count
        return render(request, 'info_page.html', content)

def getInfo_nlogin(request):
    if request.method == "GET":
        # print('not login')
        name = str(request.GET.get("name"))
        infos = FilmInfo.objects.filter(names=name)
        content = {'infos':infos[0]}
        content['is_login'] = False
        return render(request, 'info_page.html', content)

def search(request):
    type_list = getList(request)
    if request.method == "GET":
        search_key = request.GET.get('search')
        obj = FilmInfo.objects.filter(names__contains=search_key)
    if obj.count() == 0:
        search_content = '搜索:“没有符合条件的电影”'
    else:
        search_content = ''
    return render(request, 'index.html', {'obj':obj, 'type_list':type_list, 'search_content':search_content})

# 用户注册
def register(request):
    r_user = request.POST['r_username']
    r_pwd = request.POST['r_password']
    type_list = getList(request)
    obj = FilmInfo.objects.all()
    try:
        r_user_is = UserInfo.objects.get(username=r_user).password
    except:
        r_user_is = ''
    content = {'obj': obj, 'type_list': type_list}

    if r_user != '' and r_pwd != '' and r_user_is == '':
        UserInfo.objects.create(username=r_user, password=r_pwd)
        content['r_success'] = True
    else:
        content['r_success'] = False
    return render(request, 'index.html', content)


# 用户登录
def login(request):
    user = request.POST['username']
    pwd = request.POST['password']
    obj = FilmInfo.objects.all()
    type_list = getList(request)
    collect_film = CollectInfo.objects.filter(user_name=user)
    temp_name = []
    for i in collect_film:
        temp_name.append(i.film_name)
    request.session['collect_film'] = temp_name

    content = {'obj': obj, 'type_list': type_list}

    try:
        password = UserInfo.objects.get(username=user).password
        if pwd == password:
            request.session['login_status'] = True
            request.session['user'] = user
            content['success'] = True
            content['is_login'] = True
        else:
            request.session['login_status'] = False
            request.session['user'] = None
            content['success'] = False
    except:
        request.session['login_status'] = False
        request.session['user'] = None
        content['success'] = False
    return render(request, 'index.html', content)

# 用户名校验是否重复
def verify(request):
    r_user = request.GET.get("username")
    try:
        UserInfo.objects.get(username=r_user)
        return HttpResponse("用户名已存在")
    except:
        return HttpResponse("")

def collect(request):
    user=request.session['user']
    collect_name = request.GET.get("collect_name")
    CollectInfo.objects.create(user_name=user, film_name=collect_name)
    infos = FilmInfo.objects.filter(names=collect_name)
    content = {'infos': infos[0]}
    content['is_login'] = True
    content['is_collect'] = True

    collect_film = CollectInfo.objects.filter(user_name=user)
    temp_name = []
    for i in collect_film:
        temp_name.append(i.film_name)
    request.session['collect_film'] = temp_name

    zan_count = len(ZanOrCaiInfo.objects.filter(film_name=collect_name, status='like'))
    cai_count = len(ZanOrCaiInfo.objects.filter(film_name=collect_name, status='hate'))

    content['zan_count'] = zan_count
    content['cai_count'] = cai_count

    return render(request, 'info_page.html', content)

def cancel_collect(request):
    user=request.session['user']
    collect_name = request.GET.get("collect_name")
    CollectInfo.objects.filter(user_name=user,film_name=collect_name).delete()
    infos = FilmInfo.objects.filter(names=collect_name)
    content = {'infos': infos[0]}
    content['is_login'] = True
    content['is_collect'] = False

    collect_film = CollectInfo.objects.filter(user_name=user)
    temp_name = []
    for i in collect_film:
        temp_name.append(i.film_name)
    request.session['collect_film'] = temp_name

    zan_count = len(ZanOrCaiInfo.objects.filter(film_name=collect_name, status='like'))
    cai_count = len(ZanOrCaiInfo.objects.filter(film_name=collect_name, status='hate'))

    content['zan_count'] = zan_count
    content['cai_count'] = cai_count

    return render(request, 'info_page.html', content)

def getMyCollection(request):
    user = request.session['user']
    collect_film = CollectInfo.objects.filter(user_name=user)
    temp_infos = []
    for i in collect_film:
        obj_list = FilmInfo.objects.filter(names=i.film_name)
        for x in obj_list:
            temp_infos.append(x)
    return render(request, 'my_collect_page.html', {'collect_obj_list':temp_infos})

# 生成二维码
def generate_qrcode(request):
    logo = "E:/far sight/PyCharmProjects/Film/static_files/img/logo4.png"
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=1
    )
    qr.add_data(request.GET.get("link"))
    qr.make(fit=True)

    img = qr.make_image()
    img = img.convert("RGBA")

    icon = Image.open(logo)

    img_w, img_h = img.size
    factor = 3
    size_w = int(img_w / factor)
    size_h = int(img_h / factor)

    icon_w, icon_h = icon.size
    if icon_w > size_w:
        icon_w = size_w
    if icon_h > size_h:
        icon_h = size_h
    icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)

    w = int((img_w - icon_w) / 2)
    h = int((img_h - icon_h) / 2)
    img.paste(icon, (w, h), icon)
    buf = BytesIO()
    img.save(buf, format='PNG')
    image_stream = buf.getvalue()
    response = HttpResponse(image_stream, content_type="image/png")
    return response

def zan(request):
    content = {}
    user = request.session['user']
    name = request.GET.get('name')
    # print(user)
    # print(name)
    zanOrCaiObj = ZanOrCaiInfo.objects.filter(film_name=name, user_name=user,status='like')
    if zanOrCaiObj:
        ZanOrCaiInfo.objects.filter(film_name=name, user_name=user, status='like').delete();
        request.session['zan_status'] = 'd_like'
    else:
        ZanOrCaiInfo.objects.create(film_name=name, user_name=user, status='like')
        request.session['zan_status'] = 'a_like'
    zan_count = len(ZanOrCaiInfo.objects.filter(film_name=name, status='like'))
    cai_count = len(ZanOrCaiInfo.objects.filter(film_name=name, status='hate'))
    content['zan_count'] = zan_count
    content['cai_count'] = cai_count
    return render(request, 'zan_or_cai.html', content)

def cai(request):
    content = {}
    user = request.session['user']
    name = request.GET.get('name')
    # print(user)
    # print(name)
    zanOrCaiObj = ZanOrCaiInfo.objects.filter(film_name=name, user_name=user,status='hate')
    if zanOrCaiObj:
        ZanOrCaiInfo.objects.filter(film_name=name, user_name=user, status='hate').delete();
        request.session['cai_status'] = 'd_hate'
    else:
        ZanOrCaiInfo.objects.create(film_name=name, user_name=user, status='hate')
        request.session['cai_status'] = 'a_hate'
    zan_count = len(ZanOrCaiInfo.objects.filter(film_name=name, status='like'))
    cai_count = len(ZanOrCaiInfo.objects.filter(film_name=name, status='hate'))
    content['zan_count'] = zan_count
    content['cai_count'] = cai_count
    return render(request, 'zan_or_cai.html', content)

def comment(request):
    content = {}
    film_name = request.GET.get('name')
    content['film_name'] = film_name
    content['commentObjList'] = CommentInfo.objects.filter(film_name=film_name)
    return render(request,'comment.html',content)

def write_comment(request):
    content = {}
    user_name = request.session['user']
    comment_text = request.GET.get('comment_text')
    film_name = request.GET.get('film_name')
    comment_time = time.strftime("%Y-%m-%d %X",time.localtime())
    CommentInfo.objects.create(film_name=film_name,comment_text=comment_text,user_name=user_name,comment_time=comment_time)
    content['film_name'] = film_name
    content['commentObjList'] = CommentInfo.objects.filter(film_name=film_name)
    return render(request,'comment.html',content)

def send_barrage(request):
    timeCount = request.GET.get('timeCount')
    barrageText = request.GET.get('barrageText')
    filmName = request.GET.get('film_name')
    BarrageInfo.objects.create(barrage_text=barrageText,time_count=timeCount,film_name=filmName)

def get_barrage(request):
    now_count = str(request.GET.get('now_count'))
    # print(now_count)
    getBarrageObj = BarrageInfo.objects.filter(time_count=now_count)
    if getBarrageObj:
        # print(getBarrageObj[0].barrage_text)
        return render(request, 'barrage.html', {'barrageObj':getBarrageObj[0]})
    else:
        return render(request, 'barrage.html', {'barrageObj': ''})
