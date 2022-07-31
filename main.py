# 动漫之家漫画爬取程序
# 作者：格林哈德
# 团队：格林工作室
# 协作方：尘埃工作室
# ------------------------------
# 流程：
# 一、获取每一话的网址及序号，便于命名
# 二、获取每一话的所有图片地址
# 三、获取图片地址后下载
# 四、获取图片名称并根据需求排版成pdf格式
#
# 功能需求：
# 输入目标网址及参考并保存至txt文档，作为历史记录(格式为字典)
# 根据需求下载目标网址的漫画
# 根据需求(正序/倒序)排版至pdf文档中并自行选择下载地址
#
# ---------start------------
import sys
import tools
import pdf
from os import makedirs


# 章节网址
head='https://manhua.dmzj.com'
end='#@page='


def main():
    # 历史记录
    url,file_name=tools.his()
    # 获取源码
    data = tools.url_io(url, True)
    # 获取每话网址后缀及名称
    lists, names = tools.list(data)
    # 计算下载范围及长度
    top,under=tools.x(names)
    long = under - top
    # 获取存储地址
    address = f'manga/{file_name}/'
    makedirs(address,exist_ok=True)
    # 开始爬取
    print("开始爬取！")
    list_all = []
    for i in range(top,under):
        # 每一话的url
        new_url = head + lists[i] + end + '1'
        # 获得该话所有图片地址
        pages = tools.get_page_detail(new_url)

        # 进度条所需数据
        cool=[long,i+1]
        # 根据图片地址下载并保存至指定文件夹
        the_list=tools.get_image(pages,names[i],address,cool)
        # 总图片列表
        list_all.append(the_list)
    print("下载完成！")
    # 转换为pdf格式
    BOOL=input("是否转换为pdf格式？(Y/N)\n")
    if BOOL=="Y":
        # pdf地址
        makedirs('pdf/', exist_ok=True)
        # 开始转换
        pdf.to_pdf(address,file_name,list_all)
    else:
        sys.exit(0)



if __name__=="__main__":
    print("动漫之蛛——动漫之家漫画爬取程序")
    print("作者：格林哈德")
    print("团队：格林工作室")
    print("协作方：尘埃工作室")
    print("未经作者许可，请勿随意转载！")
    print("------------------------------")
    flag="Y"
    while flag=="Y":
        main()
        flag=input("是否继续下载？(Y/N)\n")