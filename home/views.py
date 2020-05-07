from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate
from  django.contrib.auth.models import User
from .common import user_login_valid, set_page
from .models import LongitudeLatitude, Geology, Geographic_Information
from django.db.models import Q, Count, Sum


# 用户登录
def login(request):
    error = ""
    if request.method == "POST":
        data = request.POST
        username = data.get("username")
        password = data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            response = HttpResponseRedirect("/")
            # 保存登录信息到cookie和session中
            u = User.objects.get(username=username)
            request.session["username"] = username
            request.session["id"] = u.id
            request.session["email"] = u.email
            response.set_cookie("username",username)
            print(request.session.get("username"))
            return response
        error = "用户名或密码有误"
    return render(request,"common/login.html",{"error":error})


# 退出系统，清除登录信息
def logout(request):
    response = HttpResponseRedirect('/login')
    try:
        del request.session['username']  # 删除session
        del request.session['id']  # 删除session
        del request.session['email']  # 删除session
        response.delete_cookie('username')  # 删除cookie
    except:
        pass
    return response


# 首页
@user_login_valid
def index(request):
    return render(request,"common/index.html")


# 经纬度信息展示
@user_login_valid
def longitudelatitude_message(request):
    page = request.GET.get("page", 1)
    longitudelatitude_list = LongitudeLatitude.objects.all().order_by("-id")
    data, page_list = set_page(longitudelatitude_list, 20, page)
    return render(request,"common/longitudelatitude_message.html",{"data":data, "page_list":page_list})


# 删除经纬度信息
@user_login_valid
def delete_longitudelatitude_message(request, id):
    LongitudeLatitude.objects.filter(id=id).delete()
    return HttpResponseRedirect("/longitudelatitude_message")


# 经纬度详情
@user_login_valid
def longitudelatitude_detail(request, id):
    longitudelatitude = LongitudeLatitude.objects.filter(id=id)
    return render(request,"common/longitudelatitude_detail.html",{"longitudelatitude":longitudelatitude[0]})


# detail页面使用ajax返回信息
def data_detail(request):
    id = request.GET.get("id")
    result = {"labels":[], "data":[]}
    g_list = Geographic_Information.objects.filter(longitudelatitude_id=id)
    for g in g_list:
        result["labels"].append(g.geology.geology_name)
        result["data"].append(g.depth)
    return JsonResponse(result)



#  查询所有数据
def get_all_message(request):
    g_lst = Geographic_Information.objects.values("longitudelatitude").annotate(Sum("depth"))
    result = {"data":[]}
    for g in g_lst:
        l = LongitudeLatitude.objects.get(id=g["longitudelatitude"])
        east = l.longitude.replace("西经","-").replace("东经","")
        result["data"].append([east,g["depth__sum"]])
    print(result)
    return JsonResponse(result)



# 首页搜索功能
def search(request):
    keywords = request.GET.get("keywords")
    long_list = LongitudeLatitude.objects.filter(longitude__contains=keywords)
    if not  long_list.exists():
        return render(request,"common/404.html")
    return render(request, "common/search.html", {"keywords":keywords})


# 搜索功能使用ajax传递数据
def get_message(request,keywords):
    result = {"LongitudeLatitude":[],"data":[],"Geology":[]}
    # keywords = "东经175"
    long_list = LongitudeLatitude.objects.filter(longitude__contains=keywords)
    g_list = Geology.objects.all()
    l_id_list = []
    g_id_list = []
    for i in long_list:
        if i.longitude not in result["LongitudeLatitude"]:
            result["LongitudeLatitude"].append(i.latitude)
            l_id_list.append(i.id)
    for g in g_list:
        if g.geology_name not in result["Geology"]:
            result["Geology"].append(g.geology_name)
            g_id_list.append(g.id)

    for i in l_id_list:
        for g in g_id_list:
            g_info = Geographic_Information.objects.filter(longitudelatitude=i, geology=g)
            if g_info.exists():
                result["data"].append([g_id_list.index(g),l_id_list.index(i),g_info[0].depth])
            else:
                result["data"].append([g_id_list.index(g),l_id_list.index(i),0])
    # print(result)
    return JsonResponse(result)


# 地质数据
@user_login_valid
def geology_message(request):
    page = request.GET.get("page", 1)
    geology_list = Geology.objects.all().order_by("-id")
    data, page_list = set_page(geology_list, 20, page)
    return render(request, "common/geology_message.html", {"data": data, "page_list": page_list})


# 添加地质数据
@user_login_valid
def add_geology_message(request):
    # 数据重复时返回报错信息
    error = ""
    if request.method == "POST":
        data = request.POST
        geology_name = data.get("geology_name")
        number = data.get("number")

        # 类型名和编号不允许重复
        g = Geology.objects.filter(Q(geology_name=geology_name) | Q(number=number))
        if not g.exists():
            Geology.objects.create(
                geology_name=geology_name,
                number = number
            )
            return HttpResponseRedirect("/geology_message")
        error = "类型名或编号重复。"
    return render(request, "common/add_geology.html",{"error":error})


# 删除地质数据
@user_login_valid
def delete_geology_message(request, id):
    Geology.objects.filter(id=id).delete()
    return HttpResponseRedirect("/geology_message")


# 编辑地质数据
@user_login_valid
def update_geology_message(request, id):
    geology = Geology.objects.filter(id=id)
    if request.method == "POST":
        data = request.POST
        id = data.get("id")
        geology_name = data.get("geology_name")
        number = data.get("number")
        # 类型名和编号不允许重复
        g = Geology.objects.filter(Q(geology_name=geology_name) | Q(number=number))
        if not g.exists():
            Geology.objects.filter(id=id).update(
                geology_name=geology_name,
                number=number
            )
            return HttpResponseRedirect("/geology_message")
        error = "类型名或编号重复。"
        return render(request, "common/update_geology.html", {"error": error,"geology":geology[0]})
    if geology.exists():
        return render(request,"common/update_geology.html",{"geology":geology[0]})


# 地理数据信息
def geographic_information(request):
    geographic_list = Geographic_Information.objects.all().order_by("-id")
    page = request.GET.get("page",1)
    data, page_list = set_page(geographic_list, 20, page)
    l_list = Geographic_Information.objects.values("longitudelatitude").annotate(Sum("depth"))
    print(l_list)
    return render(request, "common/geographic_information.html.html", {"data":data,"page_list":page_list,"l_list":l_list})


# 增加地理数据
def add_geographic_information(request):
    if request.method == "POST":
        data = request.POST
        geology = data.get("geology")
        longitudelatitude = data.get("longitudelatitude")
        depth = data.get("depth")
        Geographic_Information.objects.create(
            geology_id = geology,
            longitudelatitude_id = longitudelatitude,
            depth = depth
        )
        return HttpResponseRedirect("/geographic_information")
    l_lst = LongitudeLatitude.objects.all()
    g_lst = Geology.objects.all()
    return render(request,"common/add_geographic.html",{"l_lst":l_lst,"g_lst":g_lst})


# 删除地理信息
def delete_geographic_information(request, id):
    Geographic_Information.objects.filter(id=id).delete()
    return HttpResponseRedirect("/geographic_information")


# 修改地质信息
def update_geographic_information(request,id):
    geographic = Geographic_Information.objects.filter(id=id)
    if request.method == "POST":
        data = request.POST
        id = data.get("id")
        geology = data.get("geology")
        longitudelatitude = data.get("longitudelatitude")
        depth = data.get("depth")
        Geographic_Information.objects.filter(id=id).update(
            geology_id = geology,
            longitudelatitude_id = longitudelatitude,
            depth = depth
        )
        return HttpResponseRedirect("/geographic_information")
    if geographic.exists():
        l_lst = LongitudeLatitude.objects.all()
        g_lst = Geology.objects.all()
        return render(request,"common/update_geographic.html",{"geographic":geographic[0],"l_lst":l_lst,"g_lst":g_lst})


# TODO 遥感图像匹配
@user_login_valid
def image_matching(request):
    return render(request,"common/image_matching.html")

