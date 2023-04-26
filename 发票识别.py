# encoding:utf-8

import requests
import base64
import os
import xlwt


'''
增值税发票识别
'''


def get_access_token():
    ak = '***'
    sk = '*****'

    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = r"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}".format(ak, sk)
    print(host)
    response = requests.get(host)
    if response:
        access_token = response.json()['access_token']
        print(access_token)
    return access_token


def get_context(pic, access_token):
    """获取发票正文内容"""
    data = {}
    try:
        request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/vat_invoice"
        # 二进制方式打开图片文件
        f = open(pic, 'rb')
        img = base64.b64encode(f.read())
        params = {"image": img}

        # 这里需要替换成自己的access_token
        access_token = access_token

        request_url = request_url + "?access_token=" + access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            print(response.json())
            json1 = response.json()
            data['SellerRegisterNum'] = json1['words_result']['SellerRegisterNum']
            data['InvoiceDate'] = json1['words_result']['InvoiceDate']
            data['PurchasserName'] = json1['words_result']['PurchaserName']
            data['SellerName'] = json1['words_result']['SellerName']
            data['AmountInFiguers'] = json1['words_result']['AmountInFiguers']
            data['InvoiceCodeConfirm'] = json1['words_result']['InvoiceCodeConfirm']  # 发票代码
            data['InvoiceNumConfirm'] = json1['words_result']['InvoiceNumConfirm']  # 发票号码
            data['TotalAmount'] = json1['words_result']['TotalAmount']  # 不含税金额
            print(data['AmountInFiguers'])
        print('正文内容获取成功！')
        return data

    except Exception as e:
        print(e)
    return data


def pics(path):
    """定义生成图片路径的函数"""
    print('正在生成图片路径')
    # 生成一个空列表用于存放图片路径
    pics = []
    # 遍历文件夹，找到后缀为jpg和png的文件，整理之后加入列表
    for filename in os.listdir(path):
        if filename.endswith('jpg') or filename.endswith('png'):
            pic = path + '/' + filename
            pics.append(pic)
    print('图片路径生成成功！')
    return pics


def datas(pics, access_token):
    """定义一个获取文件夹内所有文件正文内容的函数，每次返回一个字典，把返回的所有字典存放在一个列表里"""
    datas = []
    for p in pics:
        data = get_context(p, access_token)
        datas.append(data)
    return datas


# 定义一个写入将数据excel表格的函数
def save(datas):
    print('正在写入数据！')
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet('增值税发票内容登记', cell_overwrite_ok=True)
    # 设置表头，这里可以根据自己的需求设置，我这里设置了5个
    title = ['发票代码', '发票号码', '开具金额（不含税）', '开票日期', '纳税人识别号', '购买方名称', '卖方名称',
             '购买金额']
    for i in range(len(title)):
        sheet.write(0, i, title[i])
    for d in range(len(datas)):
        for j in range(len(title)):
            sheet.write(d + 1, 0, datas[d]['InvoiceCodeConfirm'])
            sheet.write(d + 1, 1, datas[d]['InvoiceNumConfirm'])
            sheet.write(d + 1, 2, datas[d]['TotalAmount'])
            sheet.write(d + 1, 3, datas[d]['InvoiceDate'])
            sheet.write(d + 1, 4, datas[d]['SellerRegisterNum'])
            sheet.write(d + 1, 5, datas[d]['PurchasserName'])
            sheet.write(d + 1, 6, datas[d]['SellerName'])
            sheet.write(d + 1, 7, datas[d]['AmountInFiguers'])
    print('数据写入成功！')
    book.save('增值税发票.xls')


def main():
    print('开始执行！！！')
    # 这是你发票的存放地址，自行更改
    access_token = get_access_token()
    path = r'F:\PYTHON工具包\PYTHON_WORK\图像识别\发票信息'
    Pics = pics(path)
    Datas = datas(Pics, access_token)
    save(Datas)
    print('执行结束！')


if __name__ == '__main__':
    main()
