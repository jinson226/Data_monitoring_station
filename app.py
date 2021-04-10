import decimal
from os import stat, path
import numpy as np
from flask import Flask, render_template, url_for
import json
import pymysql
from datetime import timedelta
from datetime import datetime
import pandas as pd
import xlwt as xlwt
from flask import jsonify
from flask import request
import warnings
import openpyxl

# warnings.filterwarnings("ignore")
app = Flask(__name__)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)
def ifnull(var, val):
  if var is None:
    return val
  return var
def ifnull2(var, val):
  if var ==0:
    return val
  return var
def save(input):
    a = np.array(input).tolist()
    for i in range(len(a)):
        a[i] = tuple(a[i])
    a = tuple(a)
    return a
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index_2.html')
def index_2():
    return render_template('index_2.html')


@app.route('/rk_tx.html')
def rk_tx():
    return render_template('rk_tx.html')


@app.route('/mv_hm.html')
def mv_hm():
    return render_template('mv_hm.html')


@app.route('/mv_tx.html')
def mv_tx():
    return render_template('mv_tx.html')


@app.route('/rk_hm.html')
def rk_hm():
    return render_template('rk_hm.html')


@app.route('/rk_hm_abnormal.html')
def rk_hm_abnormal():
    return render_template('rk_hm_abnormal.html')


@app.route('/rk_tx_abnormal.html')
def rk_tx_abnormal():
    return render_template('rk_tx_abnormal.html')


@app.route('/hm_diaobo.html')
def hm_diaobo():
    return render_template('hm_diaobo.html')


@app.route('/tx_diaobo.html')
def tx_diaobo():
    return render_template('tx_diaobo.html')


# 滞留库存页面
@app.route('/test', methods=['GET', 'POST'])
def mytest():
    input = pd.read_excel('test.xlsx')
    see=save(input)
    print(see)

    ck = []
    shelf = []
    cost = []
    name = []
    num = []
    stime = []
    jsonData = {}

    for data in see:
        ck.append(data[0])
        shelf.append(data[2])
        cost.append(decimal.Decimal(data[5]))
        name.append(data[4])
        num.append(decimal.Decimal(data[6]))
        stime.append(decimal.Decimal(data[7]))
    hm_shelf = []
    hm_name = []
    hm_cost = []
    hm_num = []
    hm_stime = []
    tx_shelf = []
    tx_name = []
    tx_cost = []
    tx_num = []
    tx_stime = []
    for i in range(len(ck)):
        if ck[i] == 'HM_AA':
            hm_shelf.append(shelf[i])
            hm_name.append(name[i])
            hm_cost.append(cost[i])
            hm_num.append(num[i])
            hm_stime.append(stime[i])
    for i in range(len(ck)):
        if ck[i] == 'SZ_AA':
            tx_shelf.append(shelf[i])
            tx_name.append(name[i])
            tx_cost.append(cost[i])
            tx_num.append(num[i])
            tx_stime.append(stime[i])

    hm_data = np.dstack((hm_shelf, hm_cost, hm_num, hm_stime, hm_name))
    tx_data = np.dstack((tx_shelf, tx_cost, tx_num, tx_stime, tx_name))

    hm_jh1_b_num = []  # JHA/B/D的笔数
    hm_jh1_j_num = []  # JHA/B/D的件数
    hm_jh1_price = []  # JHA/B/D的单价
    hm_jh1_time = []  # JHA/B/D的时效
    hm_jh1_name = []  # JHA/B/D的责任人

    hm_jh2_b_num = []  # JHC/E的笔数
    hm_jh2_j_num = []  # JHC/E的件数
    hm_jh2_price = []  # JHC/E的单价
    hm_jh2_time = []  # JHC/E的时效
    hm_jh2_name = []  # JHC/E的责任人

    hm_rk_b_num = []  # rk的笔数
    hm_rk_j_num = []  # rk的件数
    hm_rk_price = []  # rk的单价
    hm_rk_time = []  # rk的时效
    hm_rk_name = []  # rk的责任人

    hm_ry_b_num = []  # ry的笔数
    hm_ry_j_num = []  # ry的件数
    hm_ry_price = []  # ry的单价
    hm_ry_time = []  # ry的时效
    hm_ry_name = []  # ry的责任人

    hm_zj_b_num = []  # zj的笔数
    hm_zj_j_num = []  # zj的件数
    hm_zj_price = []  # zj的单价
    hm_zj_time = []  # zj的时效
    hm_zj_name = []  # zj的责任人

    hm_tj_b_num = []  # tj的笔数
    hm_tj_j_num = []  # tj的件数
    hm_tj_price = []  # tj的单价
    hm_tj_time = []  # tj的时效
    hm_tj_name = []  # tj的责任人

    hm_fj_b_num = []  # fj的笔数
    hm_fj_j_num = []  # fj的件数
    hm_fj_price = []  # fj的单价
    hm_fj_time = []  # fj的时效
    hm_fj_name = []  # fj的责任人

    hm_bga_b_num = []  # bga的笔数
    hm_bga_j_num = []  # bga的件数
    hm_bga_price = []  # bga的单价
    hm_bga_time = []  # bga的时效
    hm_bga_name = []  # bga的责任人

    hm_dj_b_num = []  # dj的笔数
    hm_dj_j_num = []  # dj的件数
    hm_dj_price = []  # dj的单价
    hm_dj_time = []  # dj的时效
    hm_dj_name = []  # dj的责任人

    hm_wt_b_num = []  # wt的笔数
    hm_wt_j_num = []  # wt的件数
    hm_wt_price = []  # wt的单价
    hm_wt_time = []  # wt的时效
    hm_wt_name = []  # wt的责任人

    # hm_mv1_data = ["MV0004","MV0005","MV0006","MV0007","MV0008","MV0009","MV0010","MV0011","MV0012","MV0013","MV0014","MV0015","MV0016","MV0017","MV0018","MV0019","MV0020","MV0021 ","MV0022 ","MV0023 ","MV0024 ","MV0025 ","MV0026 ","MV0027 ","MV0028 ","MV0031","MV0032","MV0033","MV0034","MV0035","MV0036","MV0037","MV0038","MV0039","MV0040","MV0041","MV0042","MV0043","MV0044","MV0045","MV0046","MV0047","MV0048","MV0049","MV0050","MV0051","MV0052","MV0053","MV0054","MV0055","MV0057 ","MV0058 ","MV0059 ","MV0060 ","MV0061 ","MV0062 ","MV0063 ","MV0064 ","MV0065 ","MV0066 ","MV0067 ","MV0068 ","MV0069 ","MV0070 ","MV0071 ","MV0072 ","MV0073 ","MV0074 ","MV0075 ","MV0076 ","MV0077 ","MV0078 ","MV0079"]
    hm_mv11_data = ["MV0005", "MV0006", "MV0007", "MV0008", "MV0009", "MV0010", "MV0011", "MV0012", "MV0013", "MV0014",
                    "MV0016", "MV0017", "MV0018", "MV0019", "MV0020", "MV0021", "MV0022", "MV0023", "MV0024", "MV0025",
                    "MV0026", "MV0027", "MV0051", "MV0052", "MV0053", "MV0055"]
    hm_mv1_data = ["MV0004", "MV0031", "MV0032", "MV0033", "MV0034", "MV0035", "MV0036", "MV0037", "MV0038", "MV0039",
                   "MV0040", "MV0041", "MV0042", "MV0043", "MV0044", "MV0045", "MV0046", "MV0047", "MV0048", "MV0049",
                   "MV0050"]

    hm_mv4_data = ["MV0001", "MV0080", "MV0081", "MV0082", "MV0083", "MV0084", "MV0085", "MV0087", "MV0088", "MV0090"]
    hm_mv10_data = ["MV0002", "MV0098", "MV0100"]
    hm_mv12_data = ["WT0001", "WT0002", "WT0003", "WT0004", "WT0005", "WT0006", "WT0007", "WT0008", "WT0009", "WT0010",
                    "WT0052"]

    hm_mv1_b_num = []  # mv1的笔数
    hm_mv1_j_num = []  # mv1的件数
    hm_mv1_price = []  # mv1的单价
    hm_mv1_time = []  # mv1的时效
    hm_mv1_name = []  # mv1的责任人

    hm_mv2_b_num = []  # mv2的笔数
    hm_mv2_j_num = []  # mv2的件数
    hm_mv2_price = []  # mv2的单价
    hm_mv2_time = []  # mv2的时效
    hm_mv2_name = []  # mv2的责任人

    hm_mv3_b_num = []  # mv3的笔数
    hm_mv3_j_num = []  # mv3的件数
    hm_mv3_price = []  # mv3的单价
    hm_mv3_time = []  # mv3的时效
    hm_mv3_name = []  # mv3的责任人

    hm_mv4_b_num = []  # mv4的笔数
    hm_mv4_j_num = []  # mv4的件数
    hm_mv4_price = []  # mv4的单价
    hm_mv4_time = []  # mv4的时效
    hm_mv4_name = []  # mv4的责任人

    hm_mv5_b_num = []  # mv5的笔数
    hm_mv5_j_num = []  # mv5的件数
    hm_mv5_price = []  # mv5的单价
    hm_mv5_time = []  # mv5的时效
    hm_mv5_name = []  # mv5的责任人

    hm_mv6_b_num = []  # mv6的笔数
    hm_mv6_j_num = []  # mv6的件数
    hm_mv6_price = []  # mv6的单价
    hm_mv6_time = []  # mv6的时效
    hm_mv6_name = []  # mv6的责任人

    hm_mv7_b_num = []  # mv7的笔数
    hm_mv7_j_num = []  # mv7的件数
    hm_mv7_price = []  # mv7的单价
    hm_mv7_time = []  # mv7的时效
    hm_mv7_name = []  # mv7的责任人

    tx_jh1_b_num = []  # JHA/B/D的笔数
    tx_jh1_j_num = []  # JHA/B/D的件数
    tx_jh1_price = []  # JHA/B/D的单价
    tx_jh1_time = []  # JHA/B/D的时效
    tx_jh1_name = []  # JHA/B/D的责任人

    tx_jh2_b_num = []  # JHC/E的笔数
    tx_jh2_j_num = []  # JHC/E的件数
    tx_jh2_price = []  # JHC/E的单价
    tx_jh2_time = []  # JHC/E的时效
    tx_jh2_name = []  # JHC/E的责任人

    tx_rk_b_num = []  # rk的笔数
    tx_rk_j_num = []  # rk的件数
    tx_rk_price = []  # rk的单价
    tx_rk_time = []  # rk的时效
    tx_rk_name = []  # rk的责任人

    tx_ry_b_num = []  # ry的笔数
    tx_ry_j_num = []  # ry的件数
    tx_ry_price = []  # ry的单价
    tx_ry_time = []  # ry的时效
    tx_ry_name = []  # ry的责任人

    tx_zj_b_num = []  # zj的笔数
    tx_zj_j_num = []  # zj的件数
    tx_zj_price = []  # zj的单价
    tx_zj_time = []  # zj的时效
    tx_zj_name = []  # zj的责任人

    tx_tj_b_num = []  # tj的笔数
    tx_tj_j_num = []  # tj的件数
    tx_tj_price = []  # tj的单价
    tx_tj_time = []  # tj的时效
    tx_tj_name = []  # tj的责任人

    tx_fj_b_num = []  # fj的笔数
    tx_fj_j_num = []  # fj的件数
    tx_fj_price = []  # fj的单价
    tx_fj_time = []  # fj的时效
    tx_fj_name = []  # fj的责任人

    tx_bg_b_num = []  # bg的笔数
    tx_bg_j_num = []  # bg的件数
    tx_bg_price = []  # bg的单价
    tx_bg_time = []  # bg的时效
    tx_bg_name = []  # bg的责任人

    tx_bga_b_num = []  # bga的笔数
    tx_bga_j_num = []  # bga的件数
    tx_bga_price = []  # bga的单价
    tx_bga_time = []  # bga的时效
    tx_bga_name = []  # bga的责任人

    tx_dj_b_num = []  # dj的笔数
    tx_dj_j_num = []  # dj的件数
    tx_dj_price = []  # dj的单价
    tx_dj_time = []  # dj的时效
    tx_dj_name = []  # dj的责任人

    tx_wt_b_num = []  # wt的笔数
    tx_wt_j_num = []  # wt的件数
    tx_wt_price = []  # wt的单价
    tx_wt_time = []  # wt的时效
    tx_wt_name = []  # wt的责任人

    tx_mv1_b_num = []  # mv1的笔数
    tx_mv1_j_num = []  # mv1的件数
    tx_mv1_price = []  # mv1的单价
    tx_mv1_time = []  # mv1的时效
    tx_mv1_name = []  # mv1的责任人

    tx_mv2_b_num = []  # mv2的笔数
    tx_mv2_j_num = []  # mv2的件数
    tx_mv2_price = []  # mv2的单价
    tx_mv2_time = []  # mv2的时效
    tx_mv2_name = []  # mv2的责任人

    tx_mv3_data = ["MV0001", "MV0005", "MV00124", "MV2000"]
    tx_mv3_b_num = []  # mv3的笔数
    tx_mv3_j_num = []  # mv3的件数
    tx_mv3_price = []  # mv3的单价
    tx_mv3_time = []  # mv3的时效
    tx_mv3_name = []  # mv3的责任人

    tx_mv4_b_num = []  # mv4的笔数
    tx_mv4_j_num = []  # mv4的件数
    tx_mv4_price = []  # mv4的单价
    tx_mv4_time = []  # mv4的时效
    tx_mv4_name = []  # mv4的责任人

    tx_mv5_b_num = []  # mv5的笔数
    tx_mv5_j_num = []  # mv5的件数
    tx_mv5_price = []  # mv5的单价
    tx_mv5_time = []  # mv5的时效
    tx_mv5_name = []  # mv5的责任人

    tx_mv6_b_num = []  # mv6的笔数
    tx_mv6_j_num = []  # mv6的件数
    tx_mv6_price = []  # mv6的单价
    tx_mv6_time = []  # mv6的时效
    tx_mv6_name = []  # mv6的责任人

    tx_mv7_b_num = []  # mv7的笔数
    tx_mv7_j_num = []  # mv7的件数
    tx_mv7_price = []  # mv7的单价
    tx_mv7_time = []  # mv7的时效
    tx_mv7_name = []  # mv7的责任人

    for i in range(len(hm_stime)):
        if (hm_data[0][i][0] in hm_mv4_data):
            hm_jh1_b_num.append(1)
            hm_jh1_j_num.append(hm_data[0][i][2])
            hm_jh1_price.append(hm_data[0][i][1])
            hm_jh1_time.append(hm_data[0][i][3])

    hm_jh1_j = np.array(hm_jh1_j_num)
    hm_jh1_p = np.array(hm_jh1_price)
    hm_jh1_all_price = hm_jh1_j * hm_jh1_p

    for i in range(len(hm_stime)):
        if hm_data[0][i][0] == 'MV0101':
            hm_jh2_b_num.append(1)
            hm_jh2_j_num.append(hm_data[0][i][2])
            hm_jh2_price.append(hm_data[0][i][1])
            hm_jh2_time.append(hm_data[0][i][3])

    hm_jh2_j = np.array(hm_jh2_j_num)
    hm_jh2_p = np.array(hm_jh2_price)
    hm_jh2_all_price = hm_jh2_j * hm_jh2_p

    for i in range(len(hm_stime)):
        if (hm_data[0][i][0] in hm_mv10_data):
            hm_rk_b_num.append(1)
            hm_rk_j_num.append(hm_data[0][i][2])
            hm_rk_price.append(hm_data[0][i][1])
            hm_rk_time.append(hm_data[0][i][3])

    hm_rk_j = np.array(hm_rk_j_num)
    hm_rk_p = np.array(hm_rk_price)
    hm_rk_all_price = hm_rk_j * hm_rk_p

    for i in range(len(hm_stime)):
        if hm_data[0][i][0][0:1] == 'ZJ':
            hm_ry_b_num.append(1)
            hm_ry_j_num.append(hm_data[0][i][2])
            hm_ry_price.append(hm_data[0][i][1])
            hm_ry_time.append(hm_data[0][i][3])

    hm_ry_j = np.array(hm_ry_j_num)
    hm_ry_p = np.array(hm_ry_price)
    hm_ry_all_price = hm_ry_j * hm_ry_p

    for i in range(len(hm_stime)):
        if hm_data[0][i][0] == 'MV0003':
            hm_zj_b_num.append(1)
            hm_zj_j_num.append(hm_data[0][i][2])
            hm_zj_price.append(hm_data[0][i][1])
            hm_zj_time.append(hm_data[0][i][3])

    hm_zj_j = np.array(hm_zj_j_num)
    hm_zj_p = np.array(hm_zj_price)
    hm_zj_all_price = hm_zj_j * hm_zj_p
    for i in range(len(hm_stime)):
        if (hm_data[0][i][0][0:1] == 'RK' or hm_data[0][i][0][0:1] == 'RY'):
            hm_tj_b_num.append(1)
            hm_tj_j_num.append(hm_data[0][i][2])
            hm_tj_price.append(hm_data[0][i][1])
            hm_tj_time.append(hm_data[0][i][3])

    hm_tj_j = np.array(hm_tj_j_num)
    hm_tj_p = np.array(hm_tj_price)
    hm_tj_all_price = hm_tj_j * hm_tj_p

    for i in range(len(hm_stime)):
        if hm_data[0][i][0] == 'MV0056':
            hm_fj_b_num.append(1)
            hm_fj_j_num.append(hm_data[0][i][2])
            hm_fj_price.append(hm_data[0][i][1])
            hm_fj_time.append(hm_data[0][i][3])

    hm_fj_j = np.array(hm_fj_j_num)
    hm_fj_p = np.array(hm_fj_price)
    hm_fj_all_price = hm_fj_j * hm_fj_p

    for i in range(len(hm_stime)):
        if hm_data[0][i][0][0:3] == 'BGA' or hm_data[0][i][0][0:3] == 'JHC' or hm_data[0][i][0][0:3] == 'JHE':
            hm_bga_b_num.append(1)
            hm_bga_j_num.append(hm_data[0][i][2])
            hm_bga_price.append(hm_data[0][i][1])
            hm_bga_time.append(hm_data[0][i][3])

    hm_bga_j = np.array(hm_bga_j_num)
    hm_bga_p = np.array(hm_bga_price)
    hm_bga_all_price = hm_bga_j * hm_bga_p

    for i in range(len(hm_stime)):
        if hm_data[0][i][0] == 'MV0030':
            hm_dj_b_num.append(1)
            hm_dj_j_num.append(hm_data[0][i][2])
            hm_dj_price.append(hm_data[0][i][1])
            hm_dj_time.append(hm_data[0][i][3])

    hm_dj_j = np.array(hm_dj_j_num)
    hm_dj_p = np.array(hm_dj_price)
    hm_dj_all_price = hm_dj_j * hm_dj_p

    for i in range(len(hm_stime)):
        if hm_data[0][i][0] == 'WT060':
            hm_wt_b_num.append(1)
            hm_wt_j_num.append(hm_data[0][i][2])
            hm_wt_price.append(hm_data[0][i][1])
            hm_wt_time.append(hm_data[0][i][3])

    hm_wt_j = np.array(hm_wt_j_num)
    hm_wt_p = np.array(hm_wt_price)
    hm_wt_all_price = hm_wt_j * hm_wt_p

    for i in range(len(hm_stime)):
        if (hm_data[0][i][0] in hm_mv1_data):
            hm_mv1_b_num.append(1)
            hm_mv1_j_num.append(hm_data[0][i][2])
            hm_mv1_price.append(hm_data[0][i][1])
            hm_mv1_time.append(hm_data[0][i][3])

    hm_mv1_j = np.array(hm_mv1_j_num)
    hm_mv1_p = np.array(hm_mv1_price)
    hm_mv1_all_price = hm_mv1_j * hm_mv1_p

    for i in range(len(hm_stime)):
        if (hm_data[0][i][0][0:3] == 'JHA' or hm_data[0][i][0][0:3] == 'JHB' or hm_data[0][i][0][0:3] == 'JHD'):
            hm_mv2_b_num.append(1)
            hm_mv2_j_num.append(hm_data[0][i][2])
            hm_mv2_price.append(hm_data[0][i][1])
            hm_mv2_time.append(hm_data[0][i][3])

    hm_mv2_j = np.array(hm_mv2_j_num)
    hm_mv2_p = np.array(hm_mv2_price)
    hm_mv2_all_price = hm_mv2_j * hm_mv2_p

    for i in range(len(hm_stime)):
        if (hm_data[0][i][0] in hm_mv11_data):
            hm_mv3_b_num.append(1)
            hm_mv3_j_num.append(hm_data[0][i][2])
            hm_mv3_price.append(hm_data[0][i][1])
            hm_mv3_time.append(hm_data[0][i][3])

    hm_mv3_j = np.array(hm_mv3_j_num)
    hm_mv3_p = np.array(hm_mv3_price)
    hm_mv3_all_price = hm_mv3_j * hm_mv3_p

    for i in range(len(hm_stime)):
        if hm_data[0][i][0][0:2] == 'TJ':
            hm_mv4_b_num.append(1)
            hm_mv4_j_num.append(hm_data[0][i][2])
            hm_mv4_price.append(hm_data[0][i][1])
            hm_mv4_time.append(hm_data[0][i][3])

    hm_mv4_j = np.array(hm_mv4_j_num)
    hm_mv4_p = np.array(hm_mv4_price)
    hm_mv4_all_price = hm_mv4_j * hm_mv4_p

    for i in range(len(hm_stime)):
        if hm_data[0][i][0] == 'MV0029':
            hm_mv5_b_num.append(1)
            hm_mv5_j_num.append(hm_data[0][i][2])
            hm_mv5_price.append(hm_data[0][i][1])
            hm_mv5_time.append(hm_data[0][i][3])

    hm_mv5_j = np.array(hm_mv5_j_num)
    hm_mv5_p = np.array(hm_mv5_price)
    hm_mv5_all_price = hm_mv5_j * hm_mv5_p

    for i in range(len(hm_stime)):
        if (hm_data[0][i][0] in hm_mv12_data):
            hm_mv6_b_num.append(1)
            hm_mv6_j_num.append(hm_data[0][i][2])
            hm_mv6_price.append(hm_data[0][i][1])
            hm_mv6_time.append(hm_data[0][i][3])

    hm_mv6_j = np.array(hm_mv6_j_num)
    hm_mv6_p = np.array(hm_mv6_price)
    hm_mv6_all_price = hm_mv6_j * hm_mv6_p

    for i in range(len(hm_stime)):
        if hm_data[0][i][0][0:2] == 'BG' and hm_data[0][i][0][0:3] != 'BGA':
            hm_mv7_b_num.append(1)
            hm_mv7_j_num.append(hm_data[0][i][2])
            hm_mv7_price.append(hm_data[0][i][1])
            hm_mv7_time.append(hm_data[0][i][3])

    hm_mv7_j = np.array(hm_mv7_j_num)
    hm_mv7_p = np.array(hm_mv7_price)
    hm_mv7_all_price = hm_mv7_j * hm_mv7_p

    for i in range(len(tx_stime)):
        if tx_data[0][i][0][0:2] == 'RK' or tx_data[0][i][0][0:2] == 'RY' or tx_data[0][i][0] == 'MV0128':
            tx_jh1_b_num.append(1)
            tx_jh1_j_num.append(tx_data[0][i][2])
            tx_jh1_price.append(tx_data[0][i][1])
            tx_jh1_time.append(tx_data[0][i][3])

    tx_jh1_j = np.array(tx_jh1_j_num)
    tx_jh1_p = np.array(tx_jh1_price)
    tx_jh1_all_price = tx_jh1_j * tx_jh1_p
    for i in range(len(tx_stime)):
        if tx_data[0][i][0][0:2] == 'ZJ':
            tx_jh2_b_num.append(1)
            tx_jh2_j_num.append(tx_data[0][i][2])
            tx_jh2_price.append(tx_data[0][i][1])
            tx_jh2_time.append(tx_data[0][i][3])

    tx_jh2_j = np.array(tx_jh2_j_num)
    tx_jh2_p = np.array(tx_jh2_price)
    tx_jh2_all_price = tx_jh2_j * tx_jh2_p

    for i in range(len(tx_stime)):
        if tx_data[0][i][0] == 'MV0126':
            tx_rk_b_num.append(1)
            tx_rk_j_num.append(tx_data[0][i][2])
            tx_rk_price.append(tx_data[0][i][1])
            tx_rk_time.append(tx_data[0][i][3])

    tx_rk_j = np.array(tx_rk_j_num)
    tx_rk_p = np.array(tx_rk_price)
    tx_rk_all_price = tx_rk_j * tx_rk_p

    for i in range(len(tx_stime)):
        if (tx_data[0][i][0][0:3] == 'JHA' or tx_data[0][i][0][0:3] == 'JHB' or tx_data[0][i][0][0:3] == 'JHD'):
            tx_ry_b_num.append(1)
            tx_ry_j_num.append(tx_data[0][i][2])
            tx_ry_price.append(tx_data[0][i][1])
            tx_ry_time.append(tx_data[0][i][3])

    tx_ry_j = np.array(tx_ry_j_num)
    tx_ry_p = np.array(tx_ry_price)
    tx_ry_all_price = tx_ry_j * tx_ry_p

    for i in range(len(tx_stime)):
        if tx_data[0][i][0] == 'MV0084':
            tx_zj_b_num.append(1)
            tx_zj_j_num.append(tx_data[0][i][2])
            tx_zj_price.append(tx_data[0][i][1])
            tx_zj_time.append(tx_data[0][i][3])

    tx_zj_j = np.array(tx_zj_j_num)
    tx_zj_p = np.array(tx_zj_price)
    tx_zj_all_price = tx_zj_j * tx_zj_p

    for i in range(len(tx_stime)):
        if tx_data[0][i][0][0:2] == 'FJ':
            tx_tj_b_num.append(1)
            tx_tj_j_num.append(tx_data[0][i][2])
            tx_tj_price.append(tx_data[0][i][1])
            tx_tj_time.append(tx_data[0][i][3])

    tx_tj_j = np.array(tx_tj_j_num)
    tx_tj_p = np.array(tx_tj_price)
    tx_tj_all_price = tx_tj_j * tx_tj_p

    for i in range(len(tx_stime)):
        if (tx_data[0][i][0] == 'MV0125' or (tx_data[0][i][0][0:2] == 'BG' and tx_data[0][i][0][0:3] != 'BGA')):
            tx_mv1_b_num.append(1)
            tx_mv1_j_num.append(tx_data[0][i][2])
            tx_mv1_price.append(tx_data[0][i][1])
            tx_mv1_time.append(tx_data[0][i][3])

    tx_mv1_j = np.array(tx_mv1_j_num)
    tx_mv1_p = np.array(tx_mv1_price)
    tx_mv1_all_price = tx_mv1_j * tx_mv1_p

    for i in range(len(tx_stime)):
        if (tx_data[0][i][0][0:3] == 'JHC' or tx_data[0][i][0][0:3] == 'JHE' or tx_data[0][i][0][0:3] == 'BGA'):
            tx_mv2_b_num.append(1)
            tx_mv2_j_num.append(tx_data[0][i][2])
            tx_mv2_price.append(tx_data[0][i][1])
            tx_mv2_time.append(tx_data[0][i][3])

    tx_mv2_j = np.array(tx_mv2_j_num)
    tx_mv2_p = np.array(tx_mv2_price)
    tx_mv2_all_price = tx_mv2_j * tx_mv2_p

    for i in range(len(tx_stime)):
        if (tx_data[0][i][0] == 'MV0112'):
            tx_mv3_b_num.append(1)
            tx_mv3_j_num.append(tx_data[0][i][2])
            tx_mv3_price.append(tx_data[0][i][1])
            tx_mv3_time.append(tx_data[0][i][3])

    tx_mv3_j = np.array(tx_mv3_j_num)
    tx_mv3_p = np.array(tx_mv3_price)
    tx_mv3_all_price = tx_mv3_j * tx_mv3_p

    for i in range(len(tx_stime)):
        if (tx_data[0][i][0] == 'MV0123'):
            tx_mv4_b_num.append(1)
            tx_mv4_j_num.append(tx_data[0][i][2])
            tx_mv4_price.append(tx_data[0][i][1])
            tx_mv4_time.append(tx_data[0][i][3])

    tx_mv4_j = np.array(tx_mv4_j_num)
    tx_mv4_p = np.array(tx_mv4_price)
    tx_mv4_all_price = tx_mv4_j * tx_mv4_p

    for i in range(len(tx_stime)):
        if tx_data[0][i][0] == 'MV0124' or tx_data[0][i][0] == 'MV0005':
            tx_mv5_b_num.append(1)
            tx_mv5_j_num.append(tx_data[0][i][2])
            tx_mv5_price.append(tx_data[0][i][1])
            tx_mv5_time.append(tx_data[0][i][3])

    tx_mv5_j = np.array(tx_mv5_j_num)
    tx_mv5_p = np.array(tx_mv5_price)
    tx_mv5_all_price = tx_mv5_j * tx_mv5_p

    for i in range(len(tx_stime)):
        if tx_data[0][i][0] == 'MV0001' or tx_data[0][i][0] == 'MV0127' or tx_data[0][i][0] == 'MV2000':
            tx_mv6_b_num.append(1)
            tx_mv6_j_num.append(tx_data[0][i][2])
            tx_mv6_price.append(tx_data[0][i][1])
            tx_mv6_time.append(tx_data[0][i][3])

    tx_mv6_j = np.array(tx_mv6_j_num)
    tx_mv6_p = np.array(tx_mv6_price)
    tx_mv6_all_price = tx_mv6_j * tx_mv6_p

    for i in range(len(tx_stime)):
        if tx_data[0][i][0] == 'MV0127':
            tx_mv7_b_num.append(1)
            tx_mv7_j_num.append(tx_data[0][i][2])
            tx_mv7_price.append(tx_data[0][i][1])
            tx_mv7_time.append(tx_data[0][i][3])

    tx_mv7_j = np.array(tx_mv7_j_num)
    tx_mv7_p = np.array(tx_mv7_price)
    tx_mv7_all_price = tx_mv7_j * tx_mv7_p

    hm_jh1 = np.dstack((hm_jh1_b_num, hm_jh1_j_num, hm_jh1_all_price, hm_jh1_time))
    hm_jh2 = np.dstack((hm_jh2_b_num, hm_jh2_j_num, hm_jh2_all_price, hm_jh2_time))
    hm_rk = np.dstack((hm_rk_b_num, hm_rk_j_num, hm_rk_all_price, hm_rk_time))
    hm_ry = np.dstack((hm_ry_b_num, hm_ry_j_num, hm_ry_all_price, hm_ry_time))
    hm_zj = np.dstack((hm_zj_b_num, hm_zj_j_num, hm_zj_all_price, hm_zj_time))
    hm_tj = np.dstack((hm_tj_b_num, hm_tj_j_num, hm_tj_all_price, hm_tj_time))
    hm_fj = np.dstack((hm_fj_b_num, hm_fj_j_num, hm_fj_all_price, hm_fj_time))
    hm_bga = np.dstack((hm_bga_b_num, hm_bga_j_num, hm_bga_all_price, hm_bga_time))
    hm_dj = np.dstack((hm_dj_b_num, hm_dj_j_num, hm_dj_all_price, hm_dj_time))
    hm_wt = np.dstack((hm_wt_b_num, hm_wt_j_num, hm_wt_all_price, hm_wt_time))
    hm_mv1 = np.dstack((hm_mv1_b_num, hm_mv1_j_num, hm_mv1_all_price, hm_mv1_time))
    hm_mv2 = np.dstack((hm_mv2_b_num, hm_mv2_j_num, hm_mv2_all_price, hm_mv2_time))
    hm_mv3 = np.dstack((hm_mv3_b_num, hm_mv3_j_num, hm_mv3_all_price, hm_mv3_time))
    hm_mv4 = np.dstack((hm_mv4_b_num, hm_mv4_j_num, hm_mv4_all_price, hm_mv4_time))
    hm_mv5 = np.dstack((hm_mv5_b_num, hm_mv5_j_num, hm_mv5_all_price, hm_mv5_time))
    hm_mv6 = np.dstack((hm_mv6_b_num, hm_mv6_j_num, hm_mv6_all_price, hm_mv6_time))
    hm_mv7 = np.dstack((hm_mv7_b_num, hm_mv7_j_num, hm_mv7_all_price, hm_mv7_time))

    hm_jh1_b_num1 = [0, 0, 0, 0, 0, 0]
    hm_jh1_j_num1 = [0, 0, 0, 0, 0, 0]
    hm_jh1_p_num1 = [0, 0, 0, 0, 0, 0]
    hm_jh2_b_num1 = [0, 0, 0, 0, 0, 0]
    hm_jh2_j_num1 = [0, 0, 0, 0, 0, 0]
    hm_jh2_p_num1 = [0, 0, 0, 0, 0, 0]
    hm_rk_b_num1 = [0, 0, 0, 0, 0, 0]
    hm_rk_j_num1 = [0, 0, 0, 0, 0, 0]
    hm_rk_p_num1 = [0, 0, 0, 0, 0, 0]
    hm_ry_b_num1 = [0, 0, 0, 0, 0, 0]
    hm_ry_j_num1 = [0, 0, 0, 0, 0, 0]
    hm_ry_p_num1 = [0, 0, 0, 0, 0, 0]
    hm_zj_b_num1 = [0, 0, 0, 0, 0, 0]
    hm_zj_j_num1 = [0, 0, 0, 0, 0, 0]
    hm_zj_p_num1 = [0, 0, 0, 0, 0, 0]
    hm_tj_b_num1 = [0, 0, 0, 0, 0, 0]
    hm_tj_j_num1 = [0, 0, 0, 0, 0, 0]
    hm_tj_p_num1 = [0, 0, 0, 0, 0, 0]
    hm_fj_b_num1 = [0, 0, 0, 0, 0, 0]
    hm_fj_j_num1 = [0, 0, 0, 0, 0, 0]
    hm_fj_p_num1 = [0, 0, 0, 0, 0, 0]
    hm_bga_b_num1 = [0, 0, 0, 0, 0, 0]
    hm_bga_j_num1 = [0, 0, 0, 0, 0, 0]
    hm_bga_p_num1 = [0, 0, 0, 0, 0, 0]
    hm_dj_b_num1 = [0, 0, 0, 0, 0, 0]
    hm_dj_j_num1 = [0, 0, 0, 0, 0, 0]
    hm_dj_p_num1 = [0, 0, 0, 0, 0, 0]
    hm_wt_b_num1 = [0, 0, 0, 0, 0, 0]
    hm_wt_j_num1 = [0, 0, 0, 0, 0, 0]
    hm_wt_p_num1 = [0, 0, 0, 0, 0, 0]
    hm_mv1_b_num1 = [0, 0, 0, 0, 0, 0]
    hm_mv1_j_num1 = [0, 0, 0, 0, 0, 0]
    hm_mv1_p_num1 = [0, 0, 0, 0, 0, 0]
    hm_mv2_b_num1 = [0, 0, 0, 0, 0, 0]
    hm_mv2_j_num1 = [0, 0, 0, 0, 0, 0]
    hm_mv2_p_num1 = [0, 0, 0, 0, 0, 0]
    hm_mv3_b_num1 = [0, 0, 0, 0, 0, 0]
    hm_mv3_j_num1 = [0, 0, 0, 0, 0, 0]
    hm_mv3_p_num1 = [0, 0, 0, 0, 0, 0]
    hm_mv4_b_num1 = [0, 0, 0, 0, 0, 0]
    hm_mv4_j_num1 = [0, 0, 0, 0, 0, 0]
    hm_mv4_p_num1 = [0, 0, 0, 0, 0, 0]
    hm_mv5_b_num1 = [0, 0, 0, 0, 0, 0]
    hm_mv5_j_num1 = [0, 0, 0, 0, 0, 0]
    hm_mv5_p_num1 = [0, 0, 0, 0, 0, 0]
    hm_mv6_b_num1 = [0, 0, 0, 0, 0, 0]
    hm_mv6_j_num1 = [0, 0, 0, 0, 0, 0]
    hm_mv6_p_num1 = [0, 0, 0, 0, 0, 0]
    hm_mv7_b_num1 = [0, 0, 0, 0, 0, 0]
    hm_mv7_j_num1 = [0, 0, 0, 0, 0, 0]
    hm_mv7_p_num1 = [0, 0, 0, 0, 0, 0]

    for i in range(len(hm_jh1[0])):
        if float(hm_jh1[0][i][3]) > 24 and float(hm_jh1[0][i][3]) <= 48:
            hm_jh1_b_num1[0] = hm_jh1_b_num1[0] + 1
            hm_jh1_j_num1[0] = hm_jh1_j_num1[0] + hm_jh1[0][i][1]
            hm_jh1_p_num1[0] = hm_jh1_p_num1[0] + hm_jh1[0][i][2]
        if float(hm_jh1[0][i][3]) > 48 and float(hm_jh1[0][i][3]) <= 72:
            hm_jh1_b_num1[1] = hm_jh1_b_num1[1] + 1
            hm_jh1_j_num1[1] = hm_jh1_j_num1[1] + hm_jh1[0][i][1]
            hm_jh1_p_num1[1] = hm_jh1_p_num1[1] + hm_jh1[0][i][2]
        if float(hm_jh1[0][i][3]) > 72 and float(hm_jh1[0][i][3]) <= 120:
            hm_jh1_b_num1[2] = hm_jh1_b_num1[2] + 1
            hm_jh1_j_num1[2] = hm_jh1_j_num1[2] + hm_jh1[0][i][1]
            hm_jh1_p_num1[2] = hm_jh1_p_num1[2] + hm_jh1[0][i][2]
        if float(hm_jh1[0][i][3]) > 120 and float(hm_jh1[0][i][3]) <= 360:
            hm_jh1_b_num1[3] = hm_jh1_b_num1[3] + 1
            hm_jh1_j_num1[3] = hm_jh1_j_num1[3] + hm_jh1[0][i][1]
            hm_jh1_p_num1[3] = hm_jh1_p_num1[3] + hm_jh1[0][i][2]
        if float(hm_jh1[0][i][3]) > 360 and float(hm_jh1[0][i][3]) <= 510:
            hm_jh1_b_num1[4] = hm_jh1_b_num1[4] + 1
            hm_jh1_j_num1[4] = hm_jh1_j_num1[4] + hm_jh1[0][i][1]
            hm_jh1_p_num1[4] = hm_jh1_p_num1[4] + hm_jh1[0][i][2]
        if float(hm_jh1[0][i][3]) > 510:
            hm_jh1_b_num1[5] = hm_jh1_b_num1[5] + 1
            hm_jh1_j_num1[5] = hm_jh1_j_num1[5] + hm_jh1[0][i][1]
            hm_jh1_p_num1[5] = hm_jh1_p_num1[5] + hm_jh1[0][i][2]
    for i in range(len(hm_jh2[0])):
        if float(hm_jh2[0][i][3]) > 24 and float(hm_jh2[0][i][3]) <= 48:
            hm_jh2_b_num1[0] = hm_jh2_b_num1[0] + 1
            hm_jh2_j_num1[0] = hm_jh2_j_num1[0] + hm_jh2[0][i][1]
            hm_jh2_p_num1[0] = hm_jh2_p_num1[0] + hm_jh2[0][i][2]
        if float(hm_jh2[0][i][3]) > 48 and float(hm_jh2[0][i][3]) <= 72:
            hm_jh2_b_num1[1] = hm_jh2_b_num1[1] + 1
            hm_jh2_j_num1[1] = hm_jh2_j_num1[1] + hm_jh2[0][i][1]
            hm_jh2_p_num1[1] = hm_jh2_p_num1[1] + hm_jh2[0][i][2]
        if float(hm_jh2[0][i][3]) > 72 and float(hm_jh2[0][i][3]) <= 120:
            hm_jh2_b_num1[2] = hm_jh2_b_num1[2] + 1
            hm_jh2_j_num1[2] = hm_jh2_j_num1[2] + hm_jh2[0][i][1]
            hm_jh2_p_num1[2] = hm_jh2_p_num1[2] + hm_jh2[0][i][2]
        if float(hm_jh2[0][i][3]) > 120 and float(hm_jh2[0][i][3]) <= 360:
            hm_jh2_b_num1[3] = hm_jh2_b_num1[3] + 1
            hm_jh2_j_num1[3] = hm_jh2_j_num1[3] + hm_jh2[0][i][1]
            hm_jh2_p_num1[3] = hm_jh2_p_num1[3] + hm_jh2[0][i][2]
        if float(hm_jh2[0][i][3]) > 360 and float(hm_jh2[0][i][3]) <= 510:
            hm_jh2_b_num1[4] = hm_jh2_b_num1[4] + 1
            hm_jh2_j_num1[4] = hm_jh2_j_num1[4] + hm_jh2[0][i][1]
            hm_jh2_p_num1[4] = hm_jh2_p_num1[4] + hm_jh2[0][i][2]
        if float(hm_jh2[0][i][3]) > 510:
            hm_jh2_b_num1[5] = hm_jh2_b_num1[5] + 1
            hm_jh2_j_num1[5] = hm_jh2_j_num1[5] + hm_jh2[0][i][1]
            hm_jh2_p_num1[5] = hm_jh2_p_num1[5] + hm_jh2[0][i][2]
    for i in range(len(hm_rk[0])):
        if float(hm_rk[0][i][3]) > 24 and float(hm_rk[0][i][3]) <= 48:
            hm_rk_b_num1[0] = hm_rk_b_num1[0] + 1
            hm_rk_j_num1[0] = hm_rk_j_num1[0] + hm_rk[0][i][1]
            hm_rk_p_num1[0] = hm_rk_p_num1[0] + hm_rk[0][i][2]
        if float(hm_rk[0][i][3]) > 48 and float(hm_rk[0][i][3]) <= 72:
            hm_rk_b_num1[1] = hm_rk_b_num1[1] + 1
            hm_rk_j_num1[1] = hm_rk_j_num1[1] + hm_rk[0][i][1]
            hm_rk_p_num1[1] = hm_rk_p_num1[1] + hm_rk[0][i][2]
        if float(hm_rk[0][i][3]) > 72 and float(hm_rk[0][i][3]) <= 120:
            hm_rk_b_num1[2] = hm_rk_b_num1[2] + 1
            hm_rk_j_num1[2] = hm_rk_j_num1[2] + hm_rk[0][i][1]
            hm_rk_p_num1[2] = hm_rk_p_num1[2] + hm_rk[0][i][2]
        if float(hm_rk[0][i][3]) > 120 and float(hm_rk[0][i][3]) <= 360:
            hm_rk_b_num1[3] = hm_rk_b_num1[3] + 1
            hm_rk_j_num1[3] = hm_rk_j_num1[3] + hm_rk[0][i][1]
            hm_rk_p_num1[3] = hm_rk_p_num1[3] + hm_rk[0][i][2]
        if float(hm_rk[0][i][3]) > 360 and float(hm_rk[0][i][3]) <= 510:
            hm_rk_b_num1[4] = hm_rk_b_num1[4] + 1
            hm_rk_j_num1[4] = hm_rk_j_num1[4] + hm_rk[0][i][1]
            hm_rk_p_num1[4] = hm_rk_p_num1[4] + hm_rk[0][i][2]
        if float(hm_rk[0][i][3]) > 510:
            hm_rk_b_num1[5] = hm_rk_b_num1[5] + 1
            hm_rk_j_num1[5] = hm_rk_j_num1[5] + hm_rk[0][i][1]
            hm_rk_p_num1[5] = hm_rk_p_num1[5] + hm_rk[0][i][2]
    for i in range(len(hm_ry[0])):
        if float(hm_ry[0][i][3]) > 24 and float(hm_ry[0][i][3]) <= 48:
            hm_ry_b_num1[0] = hm_ry_b_num1[0] + 1
            hm_ry_j_num1[0] = hm_ry_j_num1[0] + hm_ry[0][i][1]
            hm_ry_p_num1[0] = hm_ry_p_num1[0] + hm_ry[0][i][2]
        if float(hm_ry[0][i][3]) > 48 and float(hm_ry[0][i][3]) <= 72:
            hm_ry_b_num1[1] = hm_ry_b_num1[1] + 1
            hm_ry_j_num1[1] = hm_ry_j_num1[1] + hm_ry[0][i][1]
            hm_ry_p_num1[1] = hm_ry_p_num1[1] + hm_ry[0][i][2]
        if float(hm_ry[0][i][3]) > 72 and float(hm_ry[0][i][3]) <= 120:
            hm_ry_b_num1[2] = hm_ry_b_num1[2] + 1
            hm_ry_j_num1[2] = hm_ry_j_num1[2] + hm_ry[0][i][1]
            hm_ry_p_num1[2] = hm_ry_p_num1[2] + hm_ry[0][i][2]
        if float(hm_ry[0][i][3]) > 120 and float(hm_ry[0][i][3]) <= 360:
            hm_ry_b_num1[3] = hm_ry_b_num1[3] + 1
            hm_ry_j_num1[3] = hm_ry_j_num1[3] + hm_ry[0][i][1]
            hm_ry_p_num1[3] = hm_ry_p_num1[3] + hm_ry[0][i][2]
        if float(hm_ry[0][i][3]) > 360 and float(hm_ry[0][i][3]) <= 510:
            hm_ry_b_num1[4] = hm_ry_b_num1[4] + 1
            hm_ry_j_num1[4] = hm_ry_j_num1[4] + hm_ry[0][i][1]
            hm_ry_p_num1[4] = hm_ry_p_num1[4] + hm_ry[0][i][2]
        if float(hm_ry[0][i][3]) > 510:
            hm_ry_b_num1[5] = hm_ry_b_num1[5] + 1
            hm_ry_j_num1[5] = hm_ry_j_num1[5] + hm_ry[0][i][1]
            hm_ry_p_num1[5] = hm_ry_p_num1[5] + hm_ry[0][i][2]
    for i in range(len(hm_zj[0])):
        if float(hm_zj[0][i][3]) > 24 and float(hm_zj[0][i][3]) <= 48:
            hm_zj_b_num1[0] = hm_zj_b_num1[0] + 1
            hm_zj_j_num1[0] = hm_zj_j_num1[0] + hm_zj[0][i][1]
            hm_zj_p_num1[0] = hm_zj_p_num1[0] + hm_zj[0][i][2]
        if float(hm_zj[0][i][3]) > 48 and float(hm_zj[0][i][3]) <= 72:
            hm_zj_b_num1[1] = hm_zj_b_num1[1] + 1
            hm_zj_j_num1[1] = hm_zj_j_num1[1] + hm_zj[0][i][1]
            hm_zj_p_num1[1] = hm_zj_p_num1[1] + hm_zj[0][i][2]
        if float(hm_zj[0][i][3]) > 72 and float(hm_zj[0][i][3]) <= 120:
            hm_zj_b_num1[2] = hm_zj_b_num1[2] + 1
            hm_zj_j_num1[2] = hm_zj_j_num1[2] + hm_zj[0][i][1]
            hm_zj_p_num1[2] = hm_zj_p_num1[2] + hm_zj[0][i][2]
        if float(hm_zj[0][i][3]) > 120 and float(hm_zj[0][i][3]) <= 360:
            hm_zj_b_num1[3] = hm_zj_b_num1[3] + 1
            hm_zj_j_num1[3] = hm_zj_j_num1[3] + hm_zj[0][i][1]
            hm_zj_p_num1[3] = hm_zj_p_num1[3] + hm_zj[0][i][2]
        if float(hm_zj[0][i][3]) > 360 and float(hm_zj[0][i][3]) <= 510:
            hm_zj_b_num1[4] = hm_zj_b_num1[4] + 1
            hm_zj_j_num1[4] = hm_zj_j_num1[4] + hm_zj[0][i][1]
            hm_zj_p_num1[4] = hm_zj_p_num1[4] + hm_zj[0][i][2]
        if float(hm_zj[0][i][3]) > 510:
            hm_zj_b_num1[5] = hm_zj_b_num1[5] + 1
            hm_zj_j_num1[5] = hm_zj_j_num1[5] + hm_zj[0][i][1]
            hm_zj_p_num1[5] = hm_zj_p_num1[5] + hm_zj[0][i][2]
    for i in range(len(hm_tj[0])):
        if float(hm_tj[0][i][3]) > 24 and float(hm_tj[0][i][3]) <= 48:
            hm_tj_b_num1[0] = hm_tj_b_num1[0] + 1
            hm_tj_j_num1[0] = hm_tj_j_num1[0] + hm_tj[0][i][1]
            hm_tj_p_num1[0] = hm_tj_p_num1[0] + hm_tj[0][i][2]
        if float(hm_tj[0][i][3]) > 48 and float(hm_tj[0][i][3]) <= 72:
            hm_tj_b_num1[1] = hm_tj_b_num1[1] + 1
            hm_tj_j_num1[1] = hm_tj_j_num1[1] + hm_tj[0][i][1]
            hm_tj_p_num1[1] = hm_tj_p_num1[1] + hm_tj[0][i][2]
        if float(hm_tj[0][i][3]) > 72 and float(hm_tj[0][i][3]) <= 120:
            hm_tj_b_num1[2] = hm_tj_b_num1[2] + 1
            hm_tj_j_num1[2] = hm_tj_j_num1[2] + hm_tj[0][i][1]
            hm_tj_p_num1[2] = hm_tj_p_num1[2] + hm_tj[0][i][2]
        if float(hm_tj[0][i][3]) > 120 and float(hm_tj[0][i][3]) <= 360:
            hm_tj_b_num1[3] = hm_tj_b_num1[3] + 1
            hm_tj_j_num1[3] = hm_tj_j_num1[3] + hm_tj[0][i][1]
            hm_tj_p_num1[3] = hm_tj_p_num1[3] + hm_tj[0][i][2]
        if float(hm_tj[0][i][3]) > 360 and float(hm_tj[0][i][3]) <= 510:
            hm_tj_b_num1[4] = hm_tj_b_num1[4] + 1
            hm_tj_j_num1[4] = hm_tj_j_num1[4] + hm_tj[0][i][1]
            hm_tj_p_num1[4] = hm_tj_p_num1[4] + hm_tj[0][i][2]
        if float(hm_tj[0][i][3]) > 510:
            hm_tj_b_num1[5] = hm_tj_b_num1[5] + 1
            hm_tj_j_num1[5] = hm_tj_j_num1[5] + hm_tj[0][i][1]
            hm_tj_p_num1[5] = hm_tj_p_num1[5] + hm_tj[0][i][2]
    for i in range(len(hm_fj[0])):
        if float(hm_fj[0][i][3]) > 24 and float(hm_fj[0][i][3]) <= 48:
            hm_fj_b_num1[0] = hm_fj_b_num1[0] + 1
            hm_fj_j_num1[0] = hm_fj_j_num1[0] + hm_fj[0][i][1]
            hm_fj_p_num1[0] = hm_fj_p_num1[0] + hm_fj[0][i][2]
        if float(hm_fj[0][i][3]) > 48 and float(hm_fj[0][i][3]) <= 72:
            hm_fj_b_num1[1] = hm_fj_b_num1[1] + 1
            hm_fj_j_num1[1] = hm_fj_j_num1[1] + hm_fj[0][i][1]
            hm_fj_p_num1[1] = hm_fj_p_num1[1] + hm_fj[0][i][2]
        if float(hm_fj[0][i][3]) > 72 and float(hm_fj[0][i][3]) <= 120:
            hm_fj_b_num1[2] = hm_fj_b_num1[2] + 1
            hm_fj_j_num1[2] = hm_fj_j_num1[2] + hm_fj[0][i][1]
            hm_fj_p_num1[2] = hm_fj_p_num1[2] + hm_fj[0][i][2]
        if float(hm_fj[0][i][3]) > 120 and float(hm_fj[0][i][3]) <= 360:
            hm_fj_b_num1[3] = hm_fj_b_num1[3] + 1
            hm_fj_j_num1[3] = hm_fj_j_num1[3] + hm_fj[0][i][1]
            hm_fj_p_num1[3] = hm_fj_p_num1[3] + hm_fj[0][i][2]
        if float(hm_fj[0][i][3]) > 360 and float(hm_fj[0][i][3]) <= 510:
            hm_fj_b_num1[4] = hm_fj_b_num1[4] + 1
            hm_fj_j_num1[4] = hm_fj_j_num1[4] + hm_fj[0][i][1]
            hm_fj_p_num1[4] = hm_fj_p_num1[4] + hm_fj[0][i][2]
        if float(hm_fj[0][i][3]) > 510:
            hm_fj_b_num1[5] = hm_fj_b_num1[5] + 1
            hm_fj_j_num1[5] = hm_fj_j_num1[5] + hm_fj[0][i][1]
            hm_fj_p_num1[5] = hm_fj_p_num1[5] + hm_fj[0][i][2]
    for i in range(len(hm_bga[0])):
        if float(hm_bga[0][i][3]) > 24 and float(hm_bga[0][i][3]) <= 48:
            hm_bga_b_num1[0] = hm_bga_b_num1[0] + 1
            hm_bga_j_num1[0] = hm_bga_j_num1[0] + hm_bga[0][i][1]
            hm_bga_p_num1[0] = hm_bga_p_num1[0] + hm_bga[0][i][2]
        if float(hm_bga[0][i][3]) > 48 and float(hm_bga[0][i][3]) <= 72:
            hm_bga_b_num1[1] = hm_bga_b_num1[1] + 1
            hm_bga_j_num1[1] = hm_bga_j_num1[1] + hm_bga[0][i][1]
            hm_bga_p_num1[1] = hm_bga_p_num1[1] + hm_bga[0][i][2]
        if float(hm_bga[0][i][3]) > 72 and float(hm_bga[0][i][3]) <= 120:
            hm_bga_b_num1[2] = hm_bga_b_num1[2] + 1
            hm_bga_j_num1[2] = hm_bga_j_num1[2] + hm_bga[0][i][1]
            hm_bga_p_num1[2] = hm_bga_p_num1[2] + hm_bga[0][i][2]
        if float(hm_bga[0][i][3]) > 120 and float(hm_bga[0][i][3]) <= 360:
            hm_bga_b_num1[3] = hm_bga_b_num1[3] + 1
            hm_bga_j_num1[3] = hm_bga_j_num1[3] + hm_bga[0][i][1]
            hm_bga_p_num1[3] = hm_bga_p_num1[3] + hm_bga[0][i][2]
        if float(hm_bga[0][i][3]) > 360 and float(hm_bga[0][i][3]) <= 510:
            hm_bga_b_num1[4] = hm_bga_b_num1[4] + 1
            hm_bga_j_num1[4] = hm_bga_j_num1[4] + hm_bga[0][i][1]
            hm_bga_p_num1[4] = hm_bga_p_num1[4] + hm_bga[0][i][2]
        if float(hm_bga[0][i][3]) > 510:
            hm_bga_b_num1[5] = hm_bga_b_num1[5] + 1
            hm_bga_j_num1[5] = hm_bga_j_num1[5] + hm_bga[0][i][1]
            hm_bga_p_num1[5] = hm_bga_p_num1[5] + hm_bga[0][i][2]
    for i in range(len(hm_dj[0])):
        if float(hm_dj[0][i][3]) > 24 and float(hm_dj[0][i][3]) <= 48:
            hm_dj_b_num1[0] = hm_dj_b_num1[0] + 1
            hm_dj_j_num1[0] = hm_dj_j_num1[0] + hm_dj[0][i][1]
            hm_dj_p_num1[0] = hm_dj_p_num1[0] + hm_dj[0][i][2]
        if float(hm_dj[0][i][3]) > 48 and float(hm_dj[0][i][3]) <= 72:
            hm_dj_b_num1[1] = hm_dj_b_num1[1] + 1
            hm_dj_j_num1[1] = hm_dj_j_num1[1] + hm_dj[0][i][1]
            hm_dj_p_num1[1] = hm_dj_p_num1[1] + hm_dj[0][i][2]
        if float(hm_dj[0][i][3]) > 72 and float(hm_dj[0][i][3]) <= 120:
            hm_dj_b_num1[2] = hm_dj_b_num1[2] + 1
            hm_dj_j_num1[2] = hm_dj_j_num1[2] + hm_dj[0][i][1]
            hm_dj_p_num1[2] = hm_dj_p_num1[2] + hm_dj[0][i][2]
        if float(hm_dj[0][i][3]) > 120 and float(hm_dj[0][i][3]) <= 360:
            hm_dj_b_num1[3] = hm_dj_b_num1[3] + 1
            hm_dj_j_num1[3] = hm_dj_j_num1[3] + hm_dj[0][i][1]
            hm_dj_p_num1[3] = hm_dj_p_num1[3] + hm_dj[0][i][2]
        if float(hm_dj[0][i][3]) > 360 and float(hm_dj[0][i][3]) <= 510:
            hm_dj_b_num1[4] = hm_dj_b_num1[4] + 1
            hm_dj_j_num1[4] = hm_dj_j_num1[4] + hm_dj[0][i][1]
            hm_dj_p_num1[4] = hm_dj_p_num1[4] + hm_dj[0][i][2]
        if float(hm_dj[0][i][3]) > 510:
            hm_dj_b_num1[5] = hm_dj_b_num1[5] + 1
            hm_dj_j_num1[5] = hm_dj_j_num1[5] + hm_dj[0][i][1]
            hm_dj_p_num1[5] = hm_dj_p_num1[5] + hm_dj[0][i][2]
    for i in range(len(hm_wt[0])):
        if float(hm_wt[0][i][3]) > 24 and float(hm_wt[0][i][3]) <= 48:
            hm_wt_b_num1[0] = hm_wt_b_num1[0] + 1
            hm_wt_j_num1[0] = hm_wt_j_num1[0] + hm_wt[0][i][1]
            hm_wt_p_num1[0] = hm_wt_p_num1[0] + hm_wt[0][i][2]
        if float(hm_wt[0][i][3]) > 48 and float(hm_wt[0][i][3]) <= 72:
            hm_wt_b_num1[1] = hm_wt_b_num1[1] + 1
            hm_wt_j_num1[1] = hm_wt_j_num1[1] + hm_wt[0][i][1]
            hm_wt_p_num1[1] = hm_wt_p_num1[1] + hm_wt[0][i][2]
        if float(hm_wt[0][i][3]) > 72 and float(hm_wt[0][i][3]) <= 120:
            hm_wt_b_num1[2] = hm_wt_b_num1[2] + 1
            hm_wt_j_num1[2] = hm_wt_j_num1[2] + hm_wt[0][i][1]
            hm_wt_p_num1[2] = hm_wt_p_num1[2] + hm_wt[0][i][2]
        if float(hm_wt[0][i][3]) > 120 and float(hm_wt[0][i][3]) <= 360:
            hm_wt_b_num1[3] = hm_wt_b_num1[3] + 1
            hm_wt_j_num1[3] = hm_wt_j_num1[3] + hm_wt[0][i][1]
            hm_wt_p_num1[3] = hm_wt_p_num1[3] + hm_wt[0][i][2]
        if float(hm_wt[0][i][3]) > 360 and float(hm_wt[0][i][3]) <= 510:
            hm_wt_b_num1[4] = hm_wt_b_num1[4] + 1
            hm_wt_j_num1[4] = hm_wt_j_num1[4] + hm_wt[0][i][1]
            hm_wt_p_num1[4] = hm_wt_p_num1[4] + hm_wt[0][i][2]
        if float(hm_wt[0][i][3]) > 510:
            hm_wt_b_num1[5] = hm_wt_b_num1[5] + 1
            hm_wt_j_num1[5] = hm_wt_j_num1[5] + hm_wt[0][i][1]
            hm_wt_p_num1[5] = hm_wt_p_num1[5] + hm_wt[0][i][2]
    for i in range(len(hm_mv1[0])):
        if float(hm_mv1[0][i][3]) > 24 and float(hm_mv1[0][i][3]) <= 48:
            hm_mv1_b_num1[0] = hm_mv1_b_num1[0] + 1
            hm_mv1_j_num1[0] = hm_mv1_j_num1[0] + hm_mv1[0][i][1]
            hm_mv1_p_num1[0] = hm_mv1_p_num1[0] + hm_mv1[0][i][2]
        if float(hm_mv1[0][i][3]) > 48 and float(hm_mv1[0][i][3]) <= 72:
            hm_mv1_b_num1[1] = hm_mv1_b_num1[1] + 1
            hm_mv1_j_num1[1] = hm_mv1_j_num1[1] + hm_mv1[0][i][1]
            hm_mv1_p_num1[1] = hm_mv1_p_num1[1] + hm_mv1[0][i][2]
        if float(hm_mv1[0][i][3]) > 72 and float(hm_mv1[0][i][3]) <= 120:
            hm_mv1_b_num1[2] = hm_mv1_b_num1[2] + 1
            hm_mv1_j_num1[2] = hm_mv1_j_num1[2] + hm_mv1[0][i][1]
            hm_mv1_p_num1[2] = hm_mv1_p_num1[2] + hm_mv1[0][i][2]
        if float(hm_mv1[0][i][3]) > 120 and float(hm_mv1[0][i][3]) <= 360:
            hm_mv1_b_num1[3] = hm_mv1_b_num1[3] + 1
            hm_mv1_j_num1[3] = hm_mv1_j_num1[3] + hm_mv1[0][i][1]
            hm_mv1_p_num1[3] = hm_mv1_p_num1[3] + hm_mv1[0][i][2]
        if float(hm_mv1[0][i][3]) > 360 and float(hm_mv1[0][i][3]) <= 510:
            hm_mv1_b_num1[4] = hm_mv1_b_num1[4] + 1
            hm_mv1_j_num1[4] = hm_mv1_j_num1[4] + hm_mv1[0][i][1]
            hm_mv1_p_num1[4] = hm_mv1_p_num1[4] + hm_mv1[0][i][2]
        if float(hm_mv1[0][i][3]) > 510:
            hm_mv1_b_num1[5] = hm_mv1_b_num1[5] + 1
            hm_mv1_j_num1[5] = hm_mv1_j_num1[5] + hm_mv1[0][i][1]
            hm_mv1_p_num1[5] = hm_mv1_p_num1[5] + hm_mv1[0][i][2]
    for i in range(len(hm_mv2[0])):
        if float(hm_mv2[0][i][3]) > 24 and float(hm_mv2[0][i][3]) <= 48:
            hm_mv2_b_num1[0] = hm_mv2_b_num1[0] + 1
            hm_mv2_j_num1[0] = hm_mv2_j_num1[0] + hm_mv2[0][i][1]
            hm_mv2_p_num1[0] = hm_mv2_p_num1[0] + hm_mv2[0][i][2]
        if float(hm_mv2[0][i][3]) > 48 and float(hm_mv2[0][i][3]) <= 72:
            hm_mv2_b_num1[1] = hm_mv2_b_num1[1] + 1
            hm_mv2_j_num1[1] = hm_mv2_j_num1[1] + hm_mv2[0][i][1]
            hm_mv2_p_num1[1] = hm_mv2_p_num1[1] + hm_mv2[0][i][2]
        if float(hm_mv2[0][i][3]) > 72 and float(hm_mv2[0][i][3]) <= 120:
            hm_mv2_b_num1[2] = hm_mv2_b_num1[2] + 1
            hm_mv2_j_num1[2] = hm_mv2_j_num1[2] + hm_mv2[0][i][1]
            hm_mv2_p_num1[2] = hm_mv2_p_num1[2] + hm_mv2[0][i][2]
        if float(hm_mv2[0][i][3]) > 120 and float(hm_mv2[0][i][3]) <= 360:
            hm_mv2_b_num1[3] = hm_mv2_b_num1[3] + 1
            hm_mv2_j_num1[3] = hm_mv2_j_num1[3] + hm_mv2[0][i][1]
            hm_mv2_p_num1[3] = hm_mv2_p_num1[3] + hm_mv2[0][i][2]
        if float(hm_mv2[0][i][3]) > 360 and float(hm_mv2[0][i][3]) <= 510:
            hm_mv2_b_num1[4] = hm_mv2_b_num1[4] + 1
            hm_mv2_j_num1[4] = hm_mv2_j_num1[4] + hm_mv2[0][i][1]
            hm_mv2_p_num1[4] = hm_mv2_p_num1[4] + hm_mv2[0][i][2]
        if float(hm_mv2[0][i][3]) > 510:
            hm_mv2_b_num1[5] = hm_mv2_b_num1[5] + 1
            hm_mv2_j_num1[5] = hm_mv2_j_num1[5] + hm_mv2[0][i][1]
            hm_mv2_p_num1[5] = hm_mv2_p_num1[5] + hm_mv2[0][i][2]
    for i in range(len(hm_mv3[0])):
        if float(hm_mv3[0][i][3]) > 24 and float(hm_mv3[0][i][3]) <= 48:
            hm_mv3_b_num1[0] = hm_mv3_b_num1[0] + 1
            hm_mv3_j_num1[0] = hm_mv3_j_num1[0] + hm_mv3[0][i][1]
            hm_mv3_p_num1[0] = hm_mv3_p_num1[0] + hm_mv3[0][i][2]
        if float(hm_mv3[0][i][3]) > 48 and float(hm_mv3[0][i][3]) <= 72:
            hm_mv3_b_num1[1] = hm_mv3_b_num1[1] + 1
            hm_mv3_j_num1[1] = hm_mv3_j_num1[1] + hm_mv3[0][i][1]
            hm_mv3_p_num1[1] = hm_mv3_p_num1[1] + hm_mv3[0][i][2]
        if float(hm_mv3[0][i][3]) > 72 and float(hm_mv3[0][i][3]) <= 120:
            hm_mv3_b_num1[2] = hm_mv3_b_num1[2] + 1
            hm_mv3_j_num1[2] = hm_mv3_j_num1[2] + hm_mv3[0][i][1]
            hm_mv3_p_num1[2] = hm_mv3_p_num1[2] + hm_mv3[0][i][2]
        if float(hm_mv3[0][i][3]) > 120 and float(hm_mv3[0][i][3]) <= 360:
            hm_mv3_b_num1[3] = hm_mv3_b_num1[3] + 1
            hm_mv3_j_num1[3] = hm_mv3_j_num1[3] + hm_mv3[0][i][1]
            hm_mv3_p_num1[3] = hm_mv3_p_num1[3] + hm_mv3[0][i][2]
        if float(hm_mv3[0][i][3]) > 360 and float(hm_mv3[0][i][3]) <= 510:
            hm_mv3_b_num1[4] = hm_mv3_b_num1[4] + 1
            hm_mv3_j_num1[4] = hm_mv3_j_num1[4] + hm_mv3[0][i][1]
            hm_mv3_p_num1[4] = hm_mv3_p_num1[4] + hm_mv3[0][i][2]
        if float(hm_mv3[0][i][3]) > 510:
            hm_mv3_b_num1[5] = hm_mv3_b_num1[5] + 1
            hm_mv3_j_num1[5] = hm_mv3_j_num1[5] + hm_mv3[0][i][1]
            hm_mv3_p_num1[5] = hm_mv3_p_num1[5] + hm_mv3[0][i][2]
    for i in range(len(hm_mv4[0])):
        if float(hm_mv4[0][i][3]) > 24 and float(hm_mv4[0][i][3]) <= 48:
            hm_mv4_b_num1[0] = hm_mv4_b_num1[0] + 1
            hm_mv4_j_num1[0] = hm_mv4_j_num1[0] + hm_mv4[0][i][1]
            hm_mv4_p_num1[0] = hm_mv4_p_num1[0] + hm_mv4[0][i][2]
        if float(hm_mv4[0][i][3]) > 48 and float(hm_mv4[0][i][3]) <= 72:
            hm_mv4_b_num1[1] = hm_mv4_b_num1[1] + 1
            hm_mv4_j_num1[1] = hm_mv4_j_num1[1] + hm_mv4[0][i][1]
            hm_mv4_p_num1[1] = hm_mv4_p_num1[1] + hm_mv4[0][i][2]
        if float(hm_mv4[0][i][3]) > 72 and float(hm_mv4[0][i][3]) <= 120:
            hm_mv4_b_num1[2] = hm_mv4_b_num1[2] + 1
            hm_mv4_j_num1[2] = hm_mv4_j_num1[2] + hm_mv4[0][i][1]
            hm_mv4_p_num1[2] = hm_mv4_p_num1[2] + hm_mv4[0][i][2]
        if float(hm_mv4[0][i][3]) > 120 and float(hm_mv4[0][i][3]) <= 360:
            hm_mv4_b_num1[3] = hm_mv4_b_num1[3] + 1
            hm_mv4_j_num1[3] = hm_mv4_j_num1[3] + hm_mv4[0][i][1]
            hm_mv4_p_num1[3] = hm_mv4_p_num1[3] + hm_mv4[0][i][2]
        if float(hm_mv4[0][i][3]) > 360 and float(hm_mv4[0][i][3]) <= 510:
            hm_mv4_b_num1[4] = hm_mv4_b_num1[4] + 1
            hm_mv4_j_num1[4] = hm_mv4_j_num1[4] + hm_mv4[0][i][1]
            hm_mv4_p_num1[4] = hm_mv4_p_num1[4] + hm_mv4[0][i][2]
        if float(hm_mv4[0][i][3]) > 510:
            hm_mv4_b_num1[5] = hm_mv4_b_num1[5] + 1
            hm_mv4_j_num1[5] = hm_mv4_j_num1[5] + hm_mv4[0][i][1]
            hm_mv4_p_num1[5] = hm_mv4_p_num1[5] + hm_mv4[0][i][2]
    for i in range(len(hm_mv5[0])):
        if float(hm_mv5[0][i][3]) > 24 and float(hm_mv5[0][i][3]) <= 48:
            hm_mv5_b_num1[0] = hm_mv5_b_num1[0] + 1
            hm_mv5_j_num1[0] = hm_mv5_j_num1[0] + hm_mv5[0][i][1]
            hm_mv5_p_num1[0] = hm_mv5_p_num1[0] + hm_mv5[0][i][2]
        if float(hm_mv5[0][i][3]) > 48 and float(hm_mv5[0][i][3]) <= 72:
            hm_mv5_b_num1[1] = hm_mv5_b_num1[1] + 1
            hm_mv5_j_num1[1] = hm_mv5_j_num1[1] + hm_mv5[0][i][1]
            hm_mv5_p_num1[1] = hm_mv5_p_num1[1] + hm_mv5[0][i][2]
        if float(hm_mv5[0][i][3]) > 72 and float(hm_mv5[0][i][3]) <= 120:
            hm_mv5_b_num1[2] = hm_mv5_b_num1[2] + 1
            hm_mv5_j_num1[2] = hm_mv5_j_num1[2] + hm_mv5[0][i][1]
            hm_mv5_p_num1[2] = hm_mv5_p_num1[2] + hm_mv5[0][i][2]
        if float(hm_mv5[0][i][3]) > 120 and float(hm_mv5[0][i][3]) <= 360:
            hm_mv5_b_num1[3] = hm_mv5_b_num1[3] + 1
            hm_mv5_j_num1[3] = hm_mv5_j_num1[3] + hm_mv5[0][i][1]
            hm_mv5_p_num1[3] = hm_mv5_p_num1[3] + hm_mv5[0][i][2]
        if float(hm_mv5[0][i][3]) > 360 and float(hm_mv5[0][i][3]) <= 510:
            hm_mv5_b_num1[4] = hm_mv5_b_num1[4] + 1
            hm_mv5_j_num1[4] = hm_mv5_j_num1[4] + hm_mv5[0][i][1]
            hm_mv5_p_num1[4] = hm_mv5_p_num1[4] + hm_mv5[0][i][2]
        if float(hm_mv5[0][i][3]) > 510:
            hm_mv5_b_num1[5] = hm_mv5_b_num1[5] + 1
            hm_mv5_j_num1[5] = hm_mv5_j_num1[5] + hm_mv5[0][i][1]
            hm_mv5_p_num1[5] = hm_mv5_p_num1[5] + hm_mv5[0][i][2]
    for i in range(len(hm_mv6[0])):
        if float(hm_mv6[0][i][3]) > 24 and float(hm_mv6[0][i][3]) <= 48:
            hm_mv6_b_num1[0] = hm_mv6_b_num1[0] + 1
            hm_mv6_j_num1[0] = hm_mv6_j_num1[0] + hm_mv6[0][i][1]
            hm_mv6_p_num1[0] = hm_mv6_p_num1[0] + hm_mv6[0][i][2]
        if float(hm_mv6[0][i][3]) > 48 and float(hm_mv6[0][i][3]) <= 72:
            hm_mv6_b_num1[1] = hm_mv6_b_num1[1] + 1
            hm_mv6_j_num1[1] = hm_mv6_j_num1[1] + hm_mv6[0][i][1]
            hm_mv6_p_num1[1] = hm_mv6_p_num1[1] + hm_mv6[0][i][2]
        if float(hm_mv6[0][i][3]) > 72 and float(hm_mv6[0][i][3]) <= 120:
            hm_mv6_b_num1[2] = hm_mv6_b_num1[2] + 1
            hm_mv6_j_num1[2] = hm_mv6_j_num1[2] + hm_mv6[0][i][1]
            hm_mv6_p_num1[2] = hm_mv6_p_num1[2] + hm_mv6[0][i][2]
        if float(hm_mv6[0][i][3]) > 120 and float(hm_mv6[0][i][3]) <= 360:
            hm_mv6_b_num1[3] = hm_mv6_b_num1[3] + 1
            hm_mv6_j_num1[3] = hm_mv6_j_num1[3] + hm_mv6[0][i][1]
            hm_mv6_p_num1[3] = hm_mv6_p_num1[3] + hm_mv6[0][i][2]
        if float(hm_mv6[0][i][3]) > 360 and float(hm_mv6[0][i][3]) <= 510:
            hm_mv6_b_num1[4] = hm_mv6_b_num1[4] + 1
            hm_mv6_j_num1[4] = hm_mv6_j_num1[4] + hm_mv6[0][i][1]
            hm_mv6_p_num1[4] = hm_mv6_p_num1[4] + hm_mv6[0][i][2]
        if float(hm_mv6[0][i][3]) > 510:
            hm_mv6_b_num1[5] = hm_mv6_b_num1[5] + 1
            hm_mv6_j_num1[5] = hm_mv6_j_num1[5] + hm_mv6[0][i][1]
            hm_mv6_p_num1[5] = hm_mv6_p_num1[5] + hm_mv6[0][i][2]
    for i in range(len(hm_mv7[0])):
        if float(hm_mv7[0][i][3]) > 24 and float(hm_mv7[0][i][3]) <= 48:
            hm_mv7_b_num1[0] = hm_mv7_b_num1[0] + 1
            hm_mv7_j_num1[0] = hm_mv7_j_num1[0] + hm_mv7[0][i][1]
            hm_mv7_p_num1[0] = hm_mv7_p_num1[0] + hm_mv7[0][i][2]
        if float(hm_mv7[0][i][3]) > 48 and float(hm_mv7[0][i][3]) <= 72:
            hm_mv7_b_num1[1] = hm_mv7_b_num1[1] + 1
            hm_mv7_j_num1[1] = hm_mv7_j_num1[1] + hm_mv7[0][i][1]
            hm_mv7_p_num1[1] = hm_mv7_p_num1[1] + hm_mv7[0][i][2]
        if float(hm_mv7[0][i][3]) > 72 and float(hm_mv7[0][i][3]) <= 120:
            hm_mv7_b_num1[2] = hm_mv7_b_num1[2] + 1
            hm_mv7_j_num1[2] = hm_mv7_j_num1[2] + hm_mv7[0][i][1]
            hm_mv7_p_num1[2] = hm_mv7_p_num1[2] + hm_mv7[0][i][2]
        if float(hm_mv7[0][i][3]) > 120 and float(hm_mv7[0][i][3]) <= 360:
            hm_mv7_b_num1[3] = hm_mv7_b_num1[3] + 1
            hm_mv7_j_num1[3] = hm_mv7_j_num1[3] + hm_mv7[0][i][1]
            hm_mv7_p_num1[3] = hm_mv7_p_num1[3] + hm_mv7[0][i][2]
        if float(hm_mv7[0][i][3]) > 360 and float(hm_mv7[0][i][3]) <= 510:
            hm_mv7_b_num1[4] = hm_mv7_b_num1[4] + 1
            hm_mv7_j_num1[4] = hm_mv7_j_num1[4] + hm_mv7[0][i][1]
            hm_mv7_p_num1[4] = hm_mv7_p_num1[4] + hm_mv7[0][i][2]
        if float(hm_mv7[0][i][3]) > 510:
            hm_mv7_b_num1[5] = hm_mv7_b_num1[5] + 1
            hm_mv7_j_num1[5] = hm_mv7_j_num1[5] + hm_mv7[0][i][1]
            hm_mv7_p_num1[5] = hm_mv7_p_num1[5] + hm_mv7[0][i][2]

    hm_bga_b_num2 = [0, 0, 0, 0, 0, 0]
    hm_bga_p_num2 = [0, 0, 0, 0, 0, 0]
    hm_wt_b_num2 = [0, 0, 0, 0, 0, 0]
    hm_wt_p_num2 = [0, 0, 0, 0, 0, 0]

    hm_b_num_48 = np.r_[
        hm_jh1_b_num1[0], hm_jh2_b_num1[0], hm_rk_b_num1[0], hm_ry_b_num1[0], hm_zj_b_num1[0], hm_tj_b_num1[0],
        hm_mv1_b_num1[0], hm_mv2_b_num1[0], hm_mv3_b_num1[0], hm_mv4_b_num1[0], hm_mv5_b_num1[0], hm_mv6_b_num1[0],
        hm_mv7_b_num1[0], hm_fj_b_num1[0], hm_bga_b_num2[0], hm_dj_b_num1[0], hm_wt_b_num2[0]]
    hm_b_num_48_max = max(hm_b_num_48)
    hm_b_num_72 = np.r_[
        hm_jh1_b_num1[1], hm_jh2_b_num1[1], hm_rk_b_num1[1], hm_ry_b_num1[1], hm_zj_b_num1[1], hm_tj_b_num1[1],
        hm_mv1_b_num1[1], hm_mv2_b_num1[1], hm_mv3_b_num1[1], hm_mv4_b_num1[1], hm_mv5_b_num1[1], hm_mv6_b_num1[1],
        hm_mv7_b_num1[1], hm_fj_b_num1[1], hm_bga_b_num2[1], hm_dj_b_num1[1], hm_wt_b_num2[1]]
    hm_b_num_120 = np.r_[
        hm_jh1_b_num1[2], hm_jh2_b_num1[2], hm_rk_b_num1[2], hm_ry_b_num1[2], hm_zj_b_num1[2], hm_tj_b_num1[2],
        hm_mv1_b_num1[2], hm_mv2_b_num1[2], hm_mv3_b_num1[2], hm_mv4_b_num1[2], hm_mv5_b_num1[2], hm_mv6_b_num1[2],
        hm_mv7_b_num1[2], hm_fj_b_num1[2], hm_bga_b_num2[2], hm_dj_b_num1[2], hm_wt_b_num2[2]]
    hm_b_num_360 = np.r_[
        hm_jh1_b_num1[3], hm_jh2_b_num1[3], hm_rk_b_num1[3], hm_ry_b_num1[3], hm_zj_b_num1[3], hm_tj_b_num1[3],
        hm_mv1_b_num1[3], hm_mv2_b_num1[3], hm_mv3_b_num1[3], hm_mv4_b_num1[3], hm_mv5_b_num1[3], hm_mv6_b_num1[3],
        hm_mv7_b_num1[3], hm_fj_b_num1[3], hm_bga_b_num2[3], hm_dj_b_num1[3], hm_wt_b_num2[3]]
    hm_b_num_510 = np.r_[
        hm_jh1_b_num1[4], hm_jh2_b_num1[4], hm_rk_b_num1[4], hm_ry_b_num1[4], hm_zj_b_num1[4], hm_tj_b_num1[4],
        hm_mv1_b_num1[4], hm_mv2_b_num1[4], hm_mv3_b_num1[4], hm_mv4_b_num1[4], hm_mv5_b_num1[4], hm_mv6_b_num1[4],
        hm_mv7_b_num1[4], hm_fj_b_num1[4], hm_bga_b_num2[4], hm_dj_b_num1[4], hm_wt_b_num2[4]]
    hm_b_num_510_ = np.r_[
        hm_jh1_b_num1[5], hm_jh2_b_num1[5], hm_rk_b_num1[5], hm_ry_b_num1[5], hm_zj_b_num1[5], hm_tj_b_num1[5],
        hm_mv1_b_num1[5], hm_mv2_b_num1[5], hm_mv3_b_num1[5], hm_mv4_b_num1[5], hm_mv5_b_num1[5], hm_mv6_b_num1[5],
        hm_mv7_b_num1[5], hm_fj_b_num1[5], hm_bga_b_num2[5], hm_dj_b_num1[5], hm_wt_b_num2[5]]
    hm_p_num_48 = np.r_[
        hm_jh1_p_num1[0], hm_jh2_p_num1[0], hm_rk_p_num1[0], hm_ry_p_num1[0], hm_zj_p_num1[0], hm_tj_p_num1[0],
        hm_mv1_p_num1[0], hm_mv2_p_num1[0], hm_mv3_p_num1[0], hm_mv4_p_num1[0], hm_mv5_p_num1[0], hm_mv6_p_num1[0],
        hm_mv7_p_num1[0], hm_fj_p_num1[0], hm_bga_p_num2[0], hm_dj_p_num1[0], hm_wt_p_num2[0]]
    hm_p_num_72 = np.r_[
        hm_jh1_p_num1[1], hm_jh2_p_num1[1], hm_rk_p_num1[1], hm_ry_p_num1[1], hm_zj_p_num1[1], hm_tj_p_num1[1],
        hm_mv1_p_num1[1], hm_mv2_p_num1[1], hm_mv3_p_num1[1], hm_mv4_p_num1[1], hm_mv5_p_num1[1], hm_mv6_p_num1[1],
        hm_mv7_p_num1[1], hm_fj_p_num1[1], hm_bga_p_num2[1], hm_dj_p_num1[1], hm_wt_p_num2[1]]
    hm_p_num_120 = np.r_[
        hm_jh1_p_num1[2], hm_jh2_p_num1[2], hm_rk_p_num1[2], hm_ry_p_num1[2], hm_zj_p_num1[2], hm_tj_p_num1[2],
        hm_mv1_p_num1[2], hm_mv2_p_num1[2], hm_mv3_p_num1[2], hm_mv4_p_num1[2], hm_mv5_p_num1[2], hm_mv6_p_num1[2],
        hm_mv7_p_num1[2], hm_fj_p_num1[2], hm_bga_p_num2[2], hm_dj_p_num1[2], hm_wt_p_num2[2]]
    hm_p_num_360 = np.r_[
        hm_jh1_p_num1[3], hm_jh2_p_num1[3], hm_rk_p_num1[3], hm_ry_p_num1[3], hm_zj_p_num1[3], hm_tj_p_num1[3],
        hm_mv1_p_num1[3], hm_mv2_p_num1[3], hm_mv3_p_num1[3], hm_mv4_p_num1[3], hm_mv5_p_num1[3], hm_mv6_p_num1[3],
        hm_mv7_p_num1[3], hm_fj_p_num1[3], hm_bga_p_num2[3], hm_dj_p_num1[3], hm_wt_p_num2[3]]
    hm_p_num_510 = np.r_[
        hm_jh1_p_num1[4], hm_jh2_p_num1[4], hm_rk_p_num1[4], hm_ry_p_num1[4], hm_zj_p_num1[4], hm_tj_p_num1[4],
        hm_mv1_p_num1[4], hm_mv2_p_num1[4], hm_mv3_p_num1[4], hm_mv4_p_num1[4], hm_mv5_p_num1[4], hm_mv6_p_num1[4],
        hm_mv7_p_num1[4], hm_fj_p_num1[4], hm_bga_p_num2[4], hm_dj_p_num1[4], hm_wt_p_num2[4]]
    hm_p_num_510_ = np.r_[
        hm_jh1_p_num1[5], hm_jh2_p_num1[5], hm_rk_p_num1[5], hm_ry_p_num1[5], hm_zj_p_num1[5], hm_tj_p_num1[5],
        hm_mv1_p_num1[5], hm_mv2_p_num1[5], hm_mv3_p_num1[5], hm_mv4_p_num1[5], hm_mv5_p_num1[5], hm_mv6_p_num1[5],
        hm_mv7_p_num1[5], hm_fj_p_num1[5], hm_bga_p_num2[5], hm_dj_p_num1[5], hm_wt_p_num2[5]]

    tx_jh1 = np.dstack((tx_jh1_b_num, tx_jh1_j_num, tx_jh1_all_price, tx_jh1_time))
    tx_jh2 = np.dstack((tx_jh2_b_num, tx_jh2_j_num, tx_jh2_all_price, tx_jh2_time))
    tx_rk = np.dstack((tx_rk_b_num, tx_rk_j_num, tx_rk_all_price, tx_rk_time))
    tx_ry = np.dstack((tx_ry_b_num, tx_ry_j_num, tx_ry_all_price, tx_ry_time))
    tx_zj = np.dstack((tx_zj_b_num, tx_zj_j_num, tx_zj_all_price, tx_zj_time))
    tx_tj = np.dstack((tx_tj_b_num, tx_tj_j_num, tx_tj_all_price, tx_tj_time))
    tx_mv1 = np.dstack((tx_mv1_b_num, tx_mv1_j_num, tx_mv1_all_price, tx_mv1_time))
    tx_mv2 = np.dstack((tx_mv2_b_num, tx_mv2_j_num, tx_mv2_all_price, tx_mv2_time))
    tx_mv3 = np.dstack((tx_mv3_b_num, tx_mv3_j_num, tx_mv3_all_price, tx_mv3_time))
    tx_mv4 = np.dstack((tx_mv4_b_num, tx_mv4_j_num, tx_mv4_all_price, tx_mv4_time))
    tx_mv5 = np.dstack((tx_mv5_b_num, tx_mv5_j_num, tx_mv5_all_price, tx_mv5_time))
    tx_mv6 = np.dstack((tx_mv6_b_num, tx_mv6_j_num, tx_mv6_all_price, tx_mv6_time))

    tx_jh1_b_num1 = [0, 0, 0, 0, 0, 0]
    tx_jh1_j_num1 = [0, 0, 0, 0, 0, 0]
    tx_jh1_p_num1 = [0, 0, 0, 0, 0, 0]

    tx_jh2_b_num1 = [0, 0, 0, 0, 0, 0]
    tx_jh2_j_num1 = [0, 0, 0, 0, 0, 0]
    tx_jh2_p_num1 = [0, 0, 0, 0, 0, 0]

    tx_rk_b_num1 = [0, 0, 0, 0, 0, 0]
    tx_rk_j_num1 = [0, 0, 0, 0, 0, 0]
    tx_rk_p_num1 = [0, 0, 0, 0, 0, 0]

    tx_ry_b_num1 = [0, 0, 0, 0, 0, 0]
    tx_ry_j_num1 = [0, 0, 0, 0, 0, 0]
    tx_ry_p_num1 = [0, 0, 0, 0, 0, 0]

    tx_zj_b_num1 = [0, 0, 0, 0, 0, 0]
    tx_zj_j_num1 = [0, 0, 0, 0, 0, 0]
    tx_zj_p_num1 = [0, 0, 0, 0, 0, 0]

    tx_tj_b_num1 = [0, 0, 0, 0, 0, 0]
    tx_tj_j_num1 = [0, 0, 0, 0, 0, 0]
    tx_tj_p_num1 = [0, 0, 0, 0, 0, 0]

    tx_mv1_b_num1 = [0, 0, 0, 0, 0, 0]
    tx_mv1_j_num1 = [0, 0, 0, 0, 0, 0]
    tx_mv1_p_num1 = [0, 0, 0, 0, 0, 0]

    tx_mv2_b_num1 = [0, 0, 0, 0, 0, 0]
    tx_mv2_j_num1 = [0, 0, 0, 0, 0, 0]
    tx_mv2_p_num1 = [0, 0, 0, 0, 0, 0]

    tx_mv3_b_num1 = [0, 0, 0, 0, 0, 0]
    tx_mv3_j_num1 = [0, 0, 0, 0, 0, 0]
    tx_mv3_p_num1 = [0, 0, 0, 0, 0, 0]

    tx_mv4_b_num1 = [0, 0, 0, 0, 0, 0]
    tx_mv4_j_num1 = [0, 0, 0, 0, 0, 0]
    tx_mv4_p_num1 = [0, 0, 0, 0, 0, 0]

    tx_mv5_b_num1 = [0, 0, 0, 0, 0, 0]
    tx_mv5_j_num1 = [0, 0, 0, 0, 0, 0]
    tx_mv5_p_num1 = [0, 0, 0, 0, 0, 0]

    tx_mv6_b_num1 = [0, 0, 0, 0, 0, 0]
    tx_mv6_j_num1 = [0, 0, 0, 0, 0, 0]
    tx_mv6_p_num1 = [0, 0, 0, 0, 0, 0]

    for i in range(len(tx_jh1[0])):
        if float(tx_jh1[0][i][3]) > 24 and float(tx_jh1[0][i][3]) <= 48:
            tx_jh1_b_num1[0] = tx_jh1_b_num1[0] + 1
            tx_jh1_j_num1[0] = tx_jh1_j_num1[0] + tx_jh1[0][i][1]
            tx_jh1_p_num1[0] = tx_jh1_p_num1[0] + tx_jh1[0][i][2]
        if float(tx_jh1[0][i][3]) > 48 and float(tx_jh1[0][i][3]) <= 72:
            tx_jh1_b_num1[1] = tx_jh1_b_num1[1] + 1
            tx_jh1_j_num1[1] = tx_jh1_j_num1[1] + tx_jh1[0][i][1]
            tx_jh1_p_num1[1] = tx_jh1_p_num1[1] + tx_jh1[0][i][2]
        if float(tx_jh1[0][i][3]) > 72 and float(tx_jh1[0][i][3]) <= 120:
            tx_jh1_b_num1[2] = tx_jh1_b_num1[2] + 1
            tx_jh1_j_num1[2] = tx_jh1_j_num1[2] + tx_jh1[0][i][1]
            tx_jh1_p_num1[2] = tx_jh1_p_num1[2] + tx_jh1[0][i][2]
        if float(tx_jh1[0][i][3]) > 120 and float(tx_jh1[0][i][3]) <= 360:
            tx_jh1_b_num1[3] = tx_jh1_b_num1[3] + 1
            tx_jh1_j_num1[3] = tx_jh1_j_num1[3] + tx_jh1[0][i][1]
            tx_jh1_p_num1[3] = tx_jh1_p_num1[3] + tx_jh1[0][i][2]
        if float(tx_jh1[0][i][3]) > 360 and float(tx_jh1[0][i][3]) <= 510:
            tx_jh1_b_num1[4] = tx_jh1_b_num1[4] + 1
            tx_jh1_j_num1[4] = tx_jh1_j_num1[4] + tx_jh1[0][i][1]
            tx_jh1_p_num1[4] = tx_jh1_p_num1[4] + tx_jh1[0][i][2]
        if float(tx_jh1[0][i][3]) > 510:
            tx_jh1_b_num1[5] = tx_jh1_b_num1[5] + 1
            tx_jh1_j_num1[5] = tx_jh1_j_num1[5] + tx_jh1[0][i][1]
            tx_jh1_p_num1[5] = tx_jh1_p_num1[5] + tx_jh1[0][i][2]
    for i in range(len(tx_jh2[0])):
        if float(tx_jh2[0][i][3]) > 24 and float(tx_jh2[0][i][3]) <= 48:
            tx_jh2_b_num1[0] = tx_jh2_b_num1[0] + 1
            tx_jh2_j_num1[0] = tx_jh2_j_num1[0] + tx_jh2[0][i][1]
            tx_jh2_p_num1[0] = tx_jh2_p_num1[0] + tx_jh2[0][i][2]
        if float(tx_jh2[0][i][3]) > 48 and float(tx_jh2[0][i][3]) <= 72:
            tx_jh2_b_num1[1] = tx_jh2_b_num1[1] + 1
            tx_jh2_j_num1[1] = tx_jh2_j_num1[1] + tx_jh2[0][i][1]
            tx_jh2_p_num1[1] = tx_jh2_p_num1[1] + tx_jh2[0][i][2]
        if float(tx_jh2[0][i][3]) > 72 and float(tx_jh2[0][i][3]) <= 120:
            tx_jh2_b_num1[2] = tx_jh2_b_num1[2] + 1
            tx_jh2_j_num1[2] = tx_jh2_j_num1[2] + tx_jh2[0][i][1]
            tx_jh2_p_num1[2] = tx_jh2_p_num1[2] + tx_jh2[0][i][2]
        if float(tx_jh2[0][i][3]) > 120 and float(tx_jh2[0][i][3]) <= 360:
            tx_jh2_b_num1[3] = tx_jh2_b_num1[3] + 1
            tx_jh2_j_num1[3] = tx_jh2_j_num1[3] + tx_jh2[0][i][1]
            tx_jh2_p_num1[3] = tx_jh2_p_num1[3] + tx_jh2[0][i][2]
        if float(tx_jh2[0][i][3]) > 360 and float(tx_jh2[0][i][3]) <= 510:
            tx_jh2_b_num1[4] = tx_jh2_b_num1[4] + 1
            tx_jh2_j_num1[4] = tx_jh2_j_num1[4] + tx_jh2[0][i][1]
            tx_jh2_p_num1[4] = tx_jh2_p_num1[4] + tx_jh2[0][i][2]
        if float(tx_jh2[0][i][3]) > 510:
            tx_jh2_b_num1[5] = tx_jh2_b_num1[5] + 1
            tx_jh2_j_num1[5] = tx_jh2_j_num1[5] + tx_jh2[0][i][1]
            tx_jh2_p_num1[5] = tx_jh2_p_num1[5] + tx_jh2[0][i][2]
    for i in range(len(tx_rk[0])):
        if float(tx_rk[0][i][3]) > 24 and float(tx_rk[0][i][3]) <= 48:
            tx_rk_b_num1[0] = tx_rk_b_num1[0] + 1
            tx_rk_j_num1[0] = tx_rk_j_num1[0] + tx_rk[0][i][1]
            tx_rk_p_num1[0] = tx_rk_p_num1[0] + tx_rk[0][i][2]
        if float(tx_rk[0][i][3]) > 48 and float(tx_rk[0][i][3]) <= 72:
            tx_rk_b_num1[1] = tx_rk_b_num1[1] + 1
            tx_rk_j_num1[1] = tx_rk_j_num1[1] + tx_rk[0][i][1]
            tx_rk_p_num1[1] = tx_rk_p_num1[1] + tx_rk[0][i][2]
        if float(tx_rk[0][i][3]) > 72 and float(tx_rk[0][i][3]) <= 120:
            tx_rk_b_num1[2] = tx_rk_b_num1[2] + 1
            tx_rk_j_num1[2] = tx_rk_j_num1[2] + tx_rk[0][i][1]
            tx_rk_p_num1[2] = tx_rk_p_num1[2] + tx_rk[0][i][2]
        if float(tx_rk[0][i][3]) > 120 and float(tx_rk[0][i][3]) <= 360:
            tx_rk_b_num1[3] = tx_rk_b_num1[3] + 1
            tx_rk_j_num1[3] = tx_rk_j_num1[3] + tx_rk[0][i][1]
            tx_rk_p_num1[3] = tx_rk_p_num1[3] + tx_rk[0][i][2]
        if float(tx_rk[0][i][3]) > 360 and float(tx_rk[0][i][3]) <= 510:
            tx_rk_b_num1[4] = tx_rk_b_num1[4] + 1
            tx_rk_j_num1[4] = tx_rk_j_num1[4] + tx_rk[0][i][1]
            tx_rk_p_num1[4] = tx_rk_p_num1[4] + tx_rk[0][i][2]
        if float(tx_rk[0][i][3]) > 510:
            tx_rk_b_num1[5] = tx_rk_b_num1[5] + 1
            tx_rk_j_num1[5] = tx_rk_j_num1[5] + tx_rk[0][i][1]
            tx_rk_p_num1[5] = tx_rk_p_num1[5] + tx_rk[0][i][2]
    for i in range(len(tx_ry[0])):
        if float(tx_ry[0][i][3]) > 24 and float(tx_ry[0][i][3]) <= 48:
            tx_ry_b_num1[0] = tx_ry_b_num1[0] + 1
            tx_ry_j_num1[0] = tx_ry_j_num1[0] + tx_ry[0][i][1]
            tx_ry_p_num1[0] = tx_ry_p_num1[0] + tx_ry[0][i][2]
        if float(tx_ry[0][i][3]) > 48 and float(tx_ry[0][i][3]) <= 72:
            tx_ry_b_num1[1] = tx_ry_b_num1[1] + 1
            tx_ry_j_num1[1] = tx_ry_j_num1[1] + tx_ry[0][i][1]
            tx_ry_p_num1[1] = tx_ry_p_num1[1] + tx_ry[0][i][2]
        if float(tx_ry[0][i][3]) > 72 and float(tx_ry[0][i][3]) <= 120:
            tx_ry_b_num1[2] = tx_ry_b_num1[2] + 1
            tx_ry_j_num1[2] = tx_ry_j_num1[2] + tx_ry[0][i][1]
            tx_ry_p_num1[2] = tx_ry_p_num1[2] + tx_ry[0][i][2]
        if float(tx_ry[0][i][3]) > 120 and float(tx_ry[0][i][3]) <= 360:
            tx_ry_b_num1[3] = tx_ry_b_num1[3] + 1
            tx_ry_j_num1[3] = tx_ry_j_num1[3] + tx_ry[0][i][1]
            tx_ry_p_num1[3] = tx_ry_p_num1[3] + tx_ry[0][i][2]
        if float(tx_ry[0][i][3]) > 360 and float(tx_ry[0][i][3]) <= 510:
            tx_ry_b_num1[4] = tx_ry_b_num1[4] + 1
            tx_ry_j_num1[4] = tx_ry_j_num1[4] + tx_ry[0][i][1]
            tx_ry_p_num1[4] = tx_ry_p_num1[4] + tx_ry[0][i][2]
        if float(tx_ry[0][i][3]) > 510:
            tx_ry_b_num1[5] = tx_ry_b_num1[5] + 1
            tx_ry_j_num1[5] = tx_ry_j_num1[5] + tx_ry[0][i][1]
            tx_ry_p_num1[5] = tx_ry_p_num1[5] + tx_ry[0][i][2]
    for i in range(len(tx_zj[0])):
        if float(tx_zj[0][i][3]) > 24 and float(tx_zj[0][i][3]) <= 48:
            tx_zj_b_num1[0] = tx_zj_b_num1[0] + 1
            tx_zj_j_num1[0] = tx_zj_j_num1[0] + tx_zj[0][i][1]
            tx_zj_p_num1[0] = tx_zj_p_num1[0] + tx_zj[0][i][2]
        if float(tx_zj[0][i][3]) > 48 and float(tx_zj[0][i][3]) <= 72:
            tx_zj_b_num1[1] = tx_zj_b_num1[1] + 1
            tx_zj_j_num1[1] = tx_zj_j_num1[1] + tx_zj[0][i][1]
            tx_zj_p_num1[1] = tx_zj_p_num1[1] + tx_zj[0][i][2]
        if float(tx_zj[0][i][3]) > 72 and float(tx_zj[0][i][3]) <= 120:
            tx_zj_b_num1[2] = tx_zj_b_num1[2] + 1
            tx_zj_j_num1[2] = tx_zj_j_num1[2] + tx_zj[0][i][1]
            tx_zj_p_num1[2] = tx_zj_p_num1[2] + tx_zj[0][i][2]
        if float(tx_zj[0][i][3]) > 120 and float(tx_zj[0][i][3]) <= 360:
            tx_zj_b_num1[3] = tx_zj_b_num1[3] + 1
            tx_zj_j_num1[3] = tx_zj_j_num1[3] + tx_zj[0][i][1]
            tx_zj_p_num1[3] = tx_zj_p_num1[3] + tx_zj[0][i][2]
        if float(tx_zj[0][i][3]) > 360 and float(tx_zj[0][i][3]) <= 510:
            tx_zj_b_num1[4] = tx_zj_b_num1[4] + 1
            tx_zj_j_num1[4] = tx_zj_j_num1[4] + tx_zj[0][i][1]
            tx_zj_p_num1[4] = tx_zj_p_num1[4] + tx_zj[0][i][2]
        if float(tx_zj[0][i][3]) > 510:
            tx_zj_b_num1[5] = tx_zj_b_num1[5] + 1
            tx_zj_j_num1[5] = tx_zj_j_num1[5] + tx_zj[0][i][1]
            tx_zj_p_num1[5] = tx_zj_p_num1[5] + tx_zj[0][i][2]
    for i in range(len(tx_tj[0])):
        if float(tx_tj[0][i][3]) > 24 and float(tx_tj[0][i][3]) <= 48:
            tx_tj_b_num1[0] = tx_tj_b_num1[0] + 1
            tx_tj_j_num1[0] = tx_tj_j_num1[0] + tx_tj[0][i][1]
            tx_tj_p_num1[0] = tx_tj_p_num1[0] + tx_tj[0][i][2]
        if float(tx_tj[0][i][3]) > 48 and float(tx_tj[0][i][3]) <= 72:
            tx_tj_b_num1[1] = tx_tj_b_num1[1] + 1
            tx_tj_j_num1[1] = tx_tj_j_num1[1] + tx_tj[0][i][1]
            tx_tj_p_num1[1] = tx_tj_p_num1[1] + tx_tj[0][i][2]
        if float(tx_tj[0][i][3]) > 72 and float(tx_tj[0][i][3]) <= 120:
            tx_tj_b_num1[2] = tx_tj_b_num1[2] + 1
            tx_tj_j_num1[2] = tx_tj_j_num1[2] + tx_tj[0][i][1]
            tx_tj_p_num1[2] = tx_tj_p_num1[2] + tx_tj[0][i][2]
        if float(tx_tj[0][i][3]) > 120 and float(tx_tj[0][i][3]) <= 360:
            tx_tj_b_num1[3] = tx_tj_b_num1[3] + 1
            tx_tj_j_num1[3] = tx_tj_j_num1[3] + tx_tj[0][i][1]
            tx_tj_p_num1[3] = tx_tj_p_num1[3] + tx_tj[0][i][2]
        if float(tx_tj[0][i][3]) > 360 and float(tx_tj[0][i][3]) <= 510:
            tx_tj_b_num1[4] = tx_tj_b_num1[4] + 1
            tx_tj_j_num1[4] = tx_tj_j_num1[4] + tx_tj[0][i][1]
            tx_tj_p_num1[4] = tx_tj_p_num1[4] + tx_tj[0][i][2]
        if float(tx_tj[0][i][3]) > 510:
            tx_tj_b_num1[5] = tx_tj_b_num1[5] + 1
            tx_tj_j_num1[5] = tx_tj_j_num1[5] + tx_tj[0][i][1]
            tx_tj_p_num1[5] = tx_tj_p_num1[5] + tx_tj[0][i][2]
    for i in range(len(tx_mv1[0])):
        if float(tx_mv1[0][i][3]) > 24 and float(tx_mv1[0][i][3]) <= 48:
            tx_mv1_b_num1[0] = tx_mv1_b_num1[0] + 1
            tx_mv1_j_num1[0] = tx_mv1_j_num1[0] + tx_mv1[0][i][1]
            tx_mv1_p_num1[0] = tx_mv1_p_num1[0] + tx_mv1[0][i][2]
        if float(tx_mv1[0][i][3]) > 48 and float(tx_mv1[0][i][3]) <= 72:
            tx_mv1_b_num1[1] = tx_mv1_b_num1[1] + 1
            tx_mv1_j_num1[1] = tx_mv1_j_num1[1] + tx_mv1[0][i][1]
            tx_mv1_p_num1[1] = tx_mv1_p_num1[1] + tx_mv1[0][i][2]
        if float(tx_mv1[0][i][3]) > 72 and float(tx_mv1[0][i][3]) <= 120:
            tx_mv1_b_num1[2] = tx_mv1_b_num1[2] + 1
            tx_mv1_j_num1[2] = tx_mv1_j_num1[2] + tx_mv1[0][i][1]
            tx_mv1_p_num1[2] = tx_mv1_p_num1[2] + tx_mv1[0][i][2]
        if float(tx_mv1[0][i][3]) > 120 and float(tx_mv1[0][i][3]) <= 360:
            tx_mv1_b_num1[3] = tx_mv1_b_num1[3] + 1
            tx_mv1_j_num1[3] = tx_mv1_j_num1[3] + tx_mv1[0][i][1]
            tx_mv1_p_num1[3] = tx_mv1_p_num1[3] + tx_mv1[0][i][2]
        if float(tx_mv1[0][i][3]) > 360 and float(tx_mv1[0][i][3]) <= 510:
            tx_mv1_b_num1[4] = tx_mv1_b_num1[4] + 1
            tx_mv1_j_num1[4] = tx_mv1_j_num1[4] + tx_mv1[0][i][1]
            tx_mv1_p_num1[4] = tx_mv1_p_num1[4] + tx_mv1[0][i][2]
        if float(tx_mv1[0][i][3]) > 510:
            tx_mv1_b_num1[5] = tx_mv1_b_num1[5] + 1
            tx_mv1_j_num1[5] = tx_mv1_j_num1[5] + tx_mv1[0][i][1]
            tx_mv1_p_num1[5] = tx_mv1_p_num1[5] + tx_mv1[0][i][2]
    for i in range(len(tx_mv2[0])):
        if float(tx_mv2[0][i][3]) > 24 and float(tx_mv2[0][i][3]) <= 48:
            tx_mv2_b_num1[0] = tx_mv2_b_num1[0] + 1
            tx_mv2_j_num1[0] = tx_mv2_j_num1[0] + tx_mv2[0][i][1]
            tx_mv2_p_num1[0] = tx_mv2_p_num1[0] + tx_mv2[0][i][2]
        if float(tx_mv2[0][i][3]) > 48 and float(tx_mv2[0][i][3]) <= 72:
            tx_mv2_b_num1[1] = tx_mv2_b_num1[1] + 1
            tx_mv2_j_num1[1] = tx_mv2_j_num1[1] + tx_mv2[0][i][1]
            tx_mv2_p_num1[1] = tx_mv2_p_num1[1] + tx_mv2[0][i][2]
        if float(tx_mv2[0][i][3]) > 72 and float(tx_mv2[0][i][3]) <= 120:
            tx_mv2_b_num1[2] = tx_mv2_b_num1[2] + 1
            tx_mv2_j_num1[2] = tx_mv2_j_num1[2] + tx_mv2[0][i][1]
            tx_mv2_p_num1[2] = tx_mv2_p_num1[2] + tx_mv2[0][i][2]
        if float(tx_mv2[0][i][3]) > 120 and float(tx_mv2[0][i][3]) <= 360:
            tx_mv2_b_num1[3] = tx_mv2_b_num1[3] + 1
            tx_mv2_j_num1[3] = tx_mv2_j_num1[3] + tx_mv2[0][i][1]
            tx_mv2_p_num1[3] = tx_mv2_p_num1[3] + tx_mv2[0][i][2]
        if float(tx_mv2[0][i][3]) > 360 and float(tx_mv2[0][i][3]) <= 510:
            tx_mv2_b_num1[4] = tx_mv2_b_num1[4] + 1
            tx_mv2_j_num1[4] = tx_mv2_j_num1[4] + tx_mv2[0][i][1]
            tx_mv2_p_num1[4] = tx_mv2_p_num1[4] + tx_mv2[0][i][2]
        if float(tx_mv2[0][i][3]) > 510:
            tx_mv2_b_num1[5] = tx_mv2_b_num1[5] + 1
            tx_mv2_j_num1[5] = tx_mv2_j_num1[5] + tx_mv2[0][i][1]
            tx_mv2_p_num1[5] = tx_mv2_p_num1[5] + tx_mv2[0][i][2]
    for i in range(len(tx_mv3[0])):
        if float(tx_mv3[0][i][3]) > 24 and float(tx_mv3[0][i][3]) <= 48:
            tx_mv3_b_num1[0] = tx_mv3_b_num1[0] + 1
            tx_mv3_j_num1[0] = tx_mv3_j_num1[0] + tx_mv3[0][i][1]
            tx_mv3_p_num1[0] = tx_mv3_p_num1[0] + tx_mv3[0][i][2]
        if float(tx_mv3[0][i][3]) > 48 and float(tx_mv3[0][i][3]) <= 72:
            tx_mv3_b_num1[1] = tx_mv3_b_num1[1] + 1
            tx_mv3_j_num1[1] = tx_mv3_j_num1[1] + tx_mv3[0][i][1]
            tx_mv3_p_num1[1] = tx_mv3_p_num1[1] + tx_mv3[0][i][2]
        if float(tx_mv3[0][i][3]) > 72 and float(tx_mv3[0][i][3]) <= 120:
            tx_mv3_b_num1[2] = tx_mv3_b_num1[2] + 1
            tx_mv3_j_num1[2] = tx_mv3_j_num1[2] + tx_mv3[0][i][1]
            tx_mv3_p_num1[2] = tx_mv3_p_num1[2] + tx_mv3[0][i][2]
        if float(tx_mv3[0][i][3]) > 120 and float(tx_mv3[0][i][3]) <= 360:
            tx_mv3_b_num1[3] = tx_mv3_b_num1[3] + 1
            tx_mv3_j_num1[3] = tx_mv3_j_num1[3] + tx_mv3[0][i][1]
            tx_mv3_p_num1[3] = tx_mv3_p_num1[3] + tx_mv3[0][i][2]
        if float(tx_mv3[0][i][3]) > 360 and float(tx_mv3[0][i][3]) <= 510:
            tx_mv3_b_num1[4] = tx_mv3_b_num1[4] + 1
            tx_mv3_j_num1[4] = tx_mv3_j_num1[4] + tx_mv3[0][i][1]
            tx_mv3_p_num1[4] = tx_mv3_p_num1[4] + tx_mv3[0][i][2]
        if float(tx_mv3[0][i][3]) > 510:
            tx_mv3_b_num1[5] = tx_mv3_b_num1[5] + 1
            tx_mv3_j_num1[5] = tx_mv3_j_num1[5] + tx_mv3[0][i][1]
            tx_mv3_p_num1[5] = tx_mv3_p_num1[5] + tx_mv3[0][i][2]
    for i in range(len(tx_mv4[0])):
        if float(tx_mv4[0][i][3]) > 24 and float(tx_mv4[0][i][3]) <= 48:
            tx_mv4_b_num1[0] = tx_mv4_b_num1[0] + 1
            tx_mv4_j_num1[0] = tx_mv4_j_num1[0] + tx_mv4[0][i][1]
            tx_mv4_p_num1[0] = tx_mv4_p_num1[0] + tx_mv4[0][i][2]
        if float(tx_mv4[0][i][3]) > 48 and float(tx_mv4[0][i][3]) <= 72:
            tx_mv4_b_num1[1] = tx_mv4_b_num1[1] + 1
            tx_mv4_j_num1[1] = tx_mv4_j_num1[1] + tx_mv4[0][i][1]
            tx_mv4_p_num1[1] = tx_mv4_p_num1[1] + tx_mv4[0][i][2]
        if float(tx_mv4[0][i][3]) > 72 and float(tx_mv4[0][i][3]) <= 120:
            tx_mv4_b_num1[2] = tx_mv4_b_num1[2] + 1
            tx_mv4_j_num1[2] = tx_mv4_j_num1[2] + tx_mv4[0][i][1]
            tx_mv4_p_num1[2] = tx_mv4_p_num1[2] + tx_mv4[0][i][2]
        if float(tx_mv4[0][i][3]) > 120 and float(tx_mv4[0][i][3]) <= 360:
            tx_mv4_b_num1[3] = tx_mv4_b_num1[3] + 1
            tx_mv4_j_num1[3] = tx_mv4_j_num1[3] + tx_mv4[0][i][1]
            tx_mv4_p_num1[3] = tx_mv4_p_num1[3] + tx_mv4[0][i][2]
        if float(tx_mv4[0][i][3]) > 360 and float(tx_mv4[0][i][3]) <= 510:
            tx_mv4_b_num1[4] = tx_mv4_b_num1[4] + 1
            tx_mv4_j_num1[4] = tx_mv4_j_num1[4] + tx_mv4[0][i][1]
            tx_mv4_p_num1[4] = tx_mv4_p_num1[4] + tx_mv4[0][i][2]
        if float(tx_mv4[0][i][3]) > 510:
            tx_mv4_b_num1[5] = tx_mv4_b_num1[5] + 1
            tx_mv4_j_num1[5] = tx_mv4_j_num1[5] + tx_mv4[0][i][1]
            tx_mv4_p_num1[5] = tx_mv4_p_num1[5] + tx_mv4[0][i][2]
    for i in range(len(tx_mv5[0])):
        if float(tx_mv5[0][i][3]) > 24 and float(tx_mv5[0][i][3]) <= 48:
            tx_mv5_b_num1[0] = tx_mv5_b_num1[0] + 1
            tx_mv5_j_num1[0] = tx_mv5_j_num1[0] + tx_mv5[0][i][1]
            tx_mv5_p_num1[0] = tx_mv5_p_num1[0] + tx_mv5[0][i][2]
        if float(tx_mv5[0][i][3]) > 48 and float(tx_mv5[0][i][3]) <= 72:
            tx_mv5_b_num1[1] = tx_mv5_b_num1[1] + 1
            tx_mv5_j_num1[1] = tx_mv5_j_num1[1] + tx_mv5[0][i][1]
            tx_mv5_p_num1[1] = tx_mv5_p_num1[1] + tx_mv5[0][i][2]
        if float(tx_mv5[0][i][3]) > 72 and float(tx_mv5[0][i][3]) <= 120:
            tx_mv5_b_num1[2] = tx_mv5_b_num1[2] + 1
            tx_mv5_j_num1[2] = tx_mv5_j_num1[2] + tx_mv5[0][i][1]
            tx_mv5_p_num1[2] = tx_mv5_p_num1[2] + tx_mv5[0][i][2]
        if float(tx_mv5[0][i][3]) > 120 and float(tx_mv5[0][i][3]) <= 360:
            tx_mv5_b_num1[3] = tx_mv5_b_num1[3] + 1
            tx_mv5_j_num1[3] = tx_mv5_j_num1[3] + tx_mv5[0][i][1]
            tx_mv5_p_num1[3] = tx_mv5_p_num1[3] + tx_mv5[0][i][2]
        if float(tx_mv5[0][i][3]) > 360 and float(tx_mv5[0][i][3]) <= 510:
            tx_mv5_b_num1[4] = tx_mv5_b_num1[4] + 1
            tx_mv5_j_num1[4] = tx_mv5_j_num1[4] + tx_mv5[0][i][1]
            tx_mv5_p_num1[4] = tx_mv5_p_num1[4] + tx_mv5[0][i][2]
        if float(tx_mv5[0][i][3]) > 510:
            tx_mv5_b_num1[5] = tx_mv5_b_num1[5] + 1
            tx_mv5_j_num1[5] = tx_mv5_j_num1[5] + tx_mv5[0][i][1]
            tx_mv5_p_num1[5] = tx_mv5_p_num1[5] + tx_mv5[0][i][2]
    for i in range(len(tx_mv6[0])):
        if float(tx_mv6[0][i][3]) > 24 and float(tx_mv6[0][i][3]) <= 48:
            tx_mv6_b_num1[0] = tx_mv6_b_num1[0] + 1
            tx_mv6_j_num1[0] = tx_mv6_j_num1[0] + tx_mv6[0][i][1]
            tx_mv6_p_num1[0] = tx_mv6_p_num1[0] + tx_mv6[0][i][2]
        if float(tx_mv6[0][i][3]) > 48 and float(tx_mv6[0][i][3]) <= 72:
            tx_mv6_b_num1[1] = tx_mv6_b_num1[1] + 1
            tx_mv6_j_num1[1] = tx_mv6_j_num1[1] + tx_mv6[0][i][1]
            tx_mv6_p_num1[1] = tx_mv6_p_num1[1] + tx_mv6[0][i][2]
        if float(tx_mv6[0][i][3]) > 72 and float(tx_mv6[0][i][3]) <= 120:
            tx_mv6_b_num1[2] = tx_mv6_b_num1[2] + 1
            tx_mv6_j_num1[2] = tx_mv6_j_num1[2] + tx_mv6[0][i][1]
            tx_mv6_p_num1[2] = tx_mv6_p_num1[2] + tx_mv6[0][i][2]
        if float(tx_mv6[0][i][3]) > 120 and float(tx_mv6[0][i][3]) <= 360:
            tx_mv6_b_num1[3] = tx_mv6_b_num1[3] + 1
            tx_mv6_j_num1[3] = tx_mv6_j_num1[3] + tx_mv6[0][i][1]
            tx_mv6_p_num1[3] = tx_mv6_p_num1[3] + tx_mv6[0][i][2]
        if float(tx_mv6[0][i][3]) > 360 and float(tx_mv6[0][i][3]) <= 510:
            tx_mv6_b_num1[4] = tx_mv6_b_num1[4] + 1
            tx_mv6_j_num1[4] = tx_mv6_j_num1[4] + tx_mv6[0][i][1]
            tx_mv6_p_num1[4] = tx_mv6_p_num1[4] + tx_mv6[0][i][2]
        if float(tx_mv6[0][i][3]) > 510:
            tx_mv6_b_num1[5] = tx_mv6_b_num1[5] + 1
            tx_mv6_j_num1[5] = tx_mv6_j_num1[5] + tx_mv6[0][i][1]
            tx_mv6_p_num1[5] = tx_mv6_p_num1[5] + tx_mv6[0][i][2]

    tx_mv2_b_num2 = [0, 0, 0, 0, 0, 0]
    tx_mv2_p_num2 = [0, 0, 0, 0, 0, 0]

    tx_b_num_48 = np.r_[tx_jh1_b_num1[0], tx_jh2_b_num1[0], tx_rk_b_num1[0],
                        tx_ry_b_num1[0], tx_zj_b_num1[0], tx_tj_b_num1[0],
                        tx_mv1_b_num1[0], tx_mv2_b_num2[0], tx_mv3_b_num1[1], tx_mv4_b_num1[1], tx_mv5_b_num1[1],
                        tx_mv6_b_num1[1]]

    tx_b_num_72 = np.r_[tx_jh1_b_num1[1], tx_jh2_b_num1[1], tx_rk_b_num1[1], tx_ry_b_num1[1],
                        tx_zj_b_num1[1], tx_tj_b_num1[1], tx_mv1_b_num1[1], tx_mv2_b_num2[1],
                        tx_mv3_b_num1[1], tx_mv4_b_num1[1], tx_mv5_b_num1[1], tx_mv6_b_num1[1]]
    tx_b_num_120 = np.r_[
        tx_jh1_b_num1[2], tx_jh2_b_num1[2], tx_rk_b_num1[2], tx_ry_b_num1[2], tx_zj_b_num1[2], tx_tj_b_num1[2],
        tx_mv1_b_num1[2], tx_mv2_b_num2[2], tx_mv3_b_num1[2], tx_mv4_b_num1[2], tx_mv5_b_num1[2], tx_mv6_b_num1[2]]

    tx_b_num_360 = np.r_[
        tx_jh1_b_num1[3], tx_jh2_b_num1[3], tx_rk_b_num1[3], tx_ry_b_num1[3], tx_zj_b_num1[3], tx_tj_b_num1[3],
        tx_mv1_b_num1[3], tx_mv2_b_num2[3], tx_mv3_b_num1[3], tx_mv4_b_num1[3], tx_mv5_b_num1[3], tx_mv6_b_num1[3]]
    tx_b_num_510 = np.r_[
        tx_jh1_b_num1[4], tx_jh2_b_num1[4], tx_rk_b_num1[4], tx_ry_b_num1[4], tx_zj_b_num1[4], tx_tj_b_num1[4],
        tx_mv1_b_num1[4], tx_mv2_b_num2[4], tx_mv3_b_num1[4], tx_mv4_b_num1[4], tx_mv5_b_num1[4], tx_mv6_b_num1[4]]
    tx_b_num_510_ = np.r_[
        tx_jh1_b_num1[5], tx_jh2_b_num1[5], tx_rk_b_num1[5], tx_ry_b_num1[5], tx_zj_b_num1[5], tx_tj_b_num1[5],
        tx_mv1_b_num1[5], tx_mv2_b_num2[5], tx_mv3_b_num1[5], tx_mv4_b_num1[5], tx_mv5_b_num1[5], tx_mv6_b_num1[5]]
    tx_p_num_48 = np.r_[
        tx_jh1_p_num1[0], tx_jh2_p_num1[0], tx_rk_p_num1[0], tx_ry_p_num1[0], tx_zj_p_num1[0], tx_tj_p_num1[0],
        tx_mv1_p_num1[0], tx_mv2_p_num2[0], tx_mv3_p_num1[0], tx_mv4_p_num1[0], tx_mv5_p_num1[0], tx_mv6_p_num1[0]]
    tx_p_num_72 = np.r_[
        tx_jh1_p_num1[1], tx_jh2_p_num1[1], tx_rk_p_num1[1], tx_ry_p_num1[1], tx_zj_p_num1[1], tx_tj_p_num1[1],
        tx_mv1_p_num1[1], tx_mv2_p_num2[1], tx_mv3_p_num1[1], tx_mv4_p_num1[1], tx_mv5_p_num1[1], tx_mv6_p_num1[1]]
    tx_p_num_120 = np.r_[
        tx_jh1_p_num1[2], tx_jh2_p_num1[2], tx_rk_p_num1[2], tx_ry_p_num1[2], tx_zj_p_num1[2], tx_tj_p_num1[2],
        tx_mv1_p_num1[2], tx_mv2_p_num2[2], tx_mv3_p_num1[2], tx_mv4_p_num1[2], tx_mv5_p_num1[2], tx_mv6_p_num1[2]]
    tx_p_num_360 = np.r_[
        tx_jh1_p_num1[3], tx_jh2_p_num1[3], tx_rk_p_num1[3], tx_ry_p_num1[3], tx_zj_p_num1[3], tx_tj_p_num1[3],
        tx_mv1_p_num1[3], tx_mv2_p_num2[3], tx_mv3_p_num1[3], tx_mv4_p_num1[3], tx_mv5_p_num1[3], tx_mv6_p_num1[3]]
    tx_p_num_510 = np.r_[
        tx_jh1_p_num1[4], tx_jh2_p_num1[4], tx_rk_p_num1[4], tx_ry_p_num1[4], tx_zj_p_num1[4], tx_tj_p_num1[4],
        tx_mv1_p_num1[4], tx_mv2_p_num2[4], tx_mv3_p_num1[4], tx_mv4_p_num1[4], tx_mv5_p_num1[4], tx_mv6_p_num1[4]]
    tx_p_num_510_ = np.r_[
        tx_jh1_p_num1[5], tx_jh2_p_num1[5], tx_rk_p_num1[5], tx_ry_p_num1[5], tx_zj_p_num1[5], tx_tj_p_num1[5],
        tx_mv1_p_num1[5], tx_mv2_p_num2[5], tx_mv3_p_num1[5], tx_mv4_p_num1[5], tx_mv5_p_num1[5], tx_mv6_p_num1[5]]

    hm_b_p_48 = []
    hm_b_p_72 = []
    hm_b_p_120 = []
    hm_b_p_360 = []
    hm_b_p_510 = []
    hm_b_p_510_ = []

    hm_p_p_48 = []
    hm_p_p_72 = []
    hm_p_p_120 = []
    hm_p_p_360 = []
    hm_p_p_510 = []
    hm_p_p_510_ = []

    for i in range(len(hm_b_num_48)):
        hm_b_p_48.append('{:.2%}'.format(hm_b_num_48[i] / max(hm_b_num_48)))
    for i in range(len(hm_b_num_72)):
        hm_b_p_72.append('{:.2%}'.format(hm_b_num_72[i] / max(hm_b_num_72)))
    for i in range(len(hm_b_num_120)):
        hm_b_p_120.append('{:.2%}'.format(hm_b_num_120[i] / max(hm_b_num_120)))
    for i in range(len(hm_b_num_360)):
        hm_b_p_360.append('{:.2%}'.format(hm_b_num_360[i] / max(hm_b_num_360)))
    for i in range(len(hm_b_num_510)):
        hm_b_p_510.append('{:.2%}'.format(hm_b_num_510[i] / max(hm_b_num_510)))
    for i in range(len(hm_b_num_510_)):
        hm_b_p_510_.append('{:.2%}'.format(hm_b_num_510_[i] / max(hm_b_num_510_)))

    for i in range(len(hm_b_num_48)):
        hm_p_p_48.append('{:.2%}'.format(hm_p_num_48[i] / max(hm_p_num_48)))
    for i in range(len(hm_b_num_72)):
        hm_p_p_72.append('{:.2%}'.format(hm_p_num_72[i] / max(hm_p_num_72)))
    for i in range(len(hm_b_num_120)):
        hm_p_p_120.append('{:.2%}'.format(hm_p_num_120[i] / max(hm_p_num_120)))
    for i in range(len(hm_b_num_360)):
        hm_p_p_360.append('{:.2%}'.format(hm_p_num_360[i] / max(hm_p_num_360)))
    for i in range(len(hm_b_num_510)):
        hm_p_p_510.append('{:.2%}'.format(hm_p_num_510[i] / max(hm_p_num_510)))
    for i in range(len(hm_b_num_510_)):
        hm_p_p_510_.append('{:.2%}'.format(hm_p_num_510_[i] / max(hm_p_num_510_)))

    tx_b_p_48 = []
    tx_b_p_72 = []
    tx_b_p_120 = []
    tx_b_p_360 = []
    tx_b_p_510 = []
    tx_b_p_510_ = []

    tx_p_p_48 = []
    tx_p_p_72 = []
    tx_p_p_120 = []
    tx_p_p_360 = []
    tx_p_p_510 = []
    tx_p_p_510_ = []

    for i in range(len(tx_b_num_48)):
        tx_b_p_48.append('{:.2%}'.format(tx_b_num_48[i] / max(tx_b_num_48)))

    for i in range(len(tx_b_num_72)):
        tx_b_p_72.append('{:.2%}'.format(tx_b_num_72[i] / max(tx_b_num_72)))
    for i in range(len(tx_b_num_120)):
        tx_b_p_120.append('{:.2%}'.format(tx_b_num_120[i] / max(tx_b_num_120)))
    for i in range(len(tx_b_num_360)):
        tx_b_p_360.append('{:.2%}'.format(tx_b_num_360[i] / max(tx_b_num_360)))
    for i in range(len(tx_b_num_510)):
        tx_b_p_510.append('{:.2%}'.format(tx_b_num_510[i] / max(tx_b_num_510)))
    for i in range(len(tx_b_num_510_)):
        tx_b_p_510_.append('{:.2%}'.format(tx_b_num_510_[i] / max(tx_b_num_510_)))

    for i in range(len(tx_b_num_48)):
        tx_p_p_48.append('{:.2%}'.format(tx_p_num_48[i] / max(tx_p_num_48)))
    for i in range(len(tx_b_num_72)):
        tx_p_p_72.append('{:.2%}'.format(tx_p_num_72[i] / max(tx_p_num_72)))
    for i in range(len(tx_b_num_120)):
        tx_p_p_120.append('{:.2%}'.format(tx_p_num_120[i] / max(tx_p_num_120)))
    for i in range(len(tx_b_num_360)):
        tx_p_p_360.append('{:.2%}'.format(tx_p_num_360[i] / max(tx_p_num_360)))
    for i in range(len(tx_b_num_510)):
        tx_p_p_510.append('{:.2%}'.format(tx_p_num_510[i] / max(tx_p_num_510)))
    for i in range(len(tx_b_num_510_)):
        tx_p_p_510_.append('{:.2%}'.format(tx_p_num_510_[i] / max(tx_p_num_510_)))

    jsonData['tx_jh1_b_num1'] = tx_jh1_b_num1
    jsonData['tx_jh1_j_num1'] = tx_jh1_j_num1
    jsonData['tx_jh1_p_num1'] = tx_jh1_p_num1

    jsonData['tx_jh2_b_num1'] = tx_jh2_b_num1
    jsonData['tx_jh2_j_num1'] = tx_jh2_j_num1
    jsonData['tx_jh2_p_num1'] = tx_jh2_p_num1

    jsonData['tx_rk_b_num1'] = tx_rk_b_num1
    jsonData['tx_rk_j_num1'] = tx_rk_j_num1
    jsonData['tx_rk_p_num1'] = tx_rk_p_num1

    jsonData['tx_ry_b_num1'] = tx_ry_b_num1
    jsonData['tx_ry_j_num1'] = tx_ry_j_num1
    jsonData['tx_ry_p_num1'] = tx_ry_p_num1

    jsonData['tx_zj_b_num1'] = tx_zj_b_num1
    jsonData['tx_zj_j_num1'] = tx_zj_j_num1
    jsonData['tx_zj_p_num1'] = tx_zj_p_num1

    jsonData['tx_tj_b_num1'] = tx_tj_b_num1
    jsonData['tx_tj_j_num1'] = tx_tj_j_num1
    jsonData['tx_tj_p_num1'] = tx_tj_p_num1

    jsonData['tx_mv1_b_num1'] = tx_mv1_b_num1
    jsonData['tx_mv1_j_num1'] = tx_mv1_j_num1
    jsonData['tx_mv1_p_num1'] = tx_mv1_p_num1

    jsonData['tx_mv2_b_num1'] = tx_mv2_b_num1
    jsonData['tx_mv2_j_num1'] = tx_mv2_j_num1
    jsonData['tx_mv2_p_num1'] = tx_mv2_p_num1

    jsonData['tx_mv3_b_num1'] = tx_mv3_b_num1
    jsonData['tx_mv3_j_num1'] = tx_mv3_j_num1
    jsonData['tx_mv3_p_num1'] = tx_mv3_p_num1

    jsonData['tx_mv4_b_num1'] = tx_mv4_b_num1
    jsonData['tx_mv4_j_num1'] = tx_mv4_j_num1
    jsonData['tx_mv4_p_num1'] = tx_mv4_p_num1

    jsonData['tx_mv5_b_num1'] = tx_mv5_b_num1
    jsonData['tx_mv5_j_num1'] = tx_mv5_j_num1
    jsonData['tx_mv5_p_num1'] = tx_mv5_p_num1

    jsonData['tx_mv6_b_num1'] = tx_mv6_b_num1
    jsonData['tx_mv6_j_num1'] = tx_mv6_j_num1
    jsonData['tx_mv6_p_num1'] = tx_mv6_p_num1

    jsonData['tx_b_p_48'] = tx_b_p_48
    jsonData['tx_b_p_72'] = tx_b_p_72
    jsonData['tx_b_p_120'] = tx_b_p_120
    jsonData['tx_b_p_360'] = tx_b_p_360
    jsonData['tx_b_p_510'] = tx_b_p_510
    jsonData['tx_b_p_510_'] = tx_b_p_510_
    jsonData['tx_p_p_48'] = tx_p_p_48
    jsonData['tx_p_p_72'] = tx_p_p_72
    jsonData['tx_p_p_120'] = tx_p_p_120
    jsonData['tx_p_p_360'] = tx_p_p_360
    jsonData['tx_p_p_510'] = tx_p_p_510
    jsonData['tx_p_p_510_'] = tx_p_p_510_

    jsonData['hm_jh1_b_num1'] = hm_jh1_b_num1
    jsonData['hm_jh1_j_num1'] = hm_jh1_j_num1
    jsonData['hm_jh1_p_num1'] = hm_jh1_p_num1
    jsonData['hm_jh2_b_num1'] = hm_jh2_b_num1
    jsonData['hm_jh2_j_num1'] = hm_jh2_j_num1
    jsonData['hm_jh2_p_num1'] = hm_jh2_p_num1
    jsonData['hm_rk_b_num1'] = hm_rk_b_num1
    jsonData['hm_rk_j_num1'] = hm_rk_j_num1
    jsonData['hm_rk_p_num1'] = hm_rk_p_num1
    jsonData['hm_ry_b_num1'] = hm_ry_b_num1
    jsonData['hm_ry_j_num1'] = hm_ry_j_num1
    jsonData['hm_ry_p_num1'] = hm_ry_p_num1
    jsonData['hm_zj_b_num1'] = hm_zj_b_num1
    jsonData['hm_zj_j_num1'] = hm_zj_j_num1
    jsonData['hm_zj_p_num1'] = hm_zj_p_num1
    jsonData['hm_tj_b_num1'] = hm_tj_b_num1
    jsonData['hm_tj_j_num1'] = hm_tj_j_num1
    jsonData['hm_tj_p_num1'] = hm_tj_p_num1
    jsonData['hm_fj_b_num1'] = hm_fj_b_num1
    jsonData['hm_fj_j_num1'] = hm_fj_j_num1
    jsonData['hm_fj_p_num1'] = hm_fj_p_num1
    jsonData['hm_bga_b_num1'] = hm_bga_b_num1
    jsonData['hm_bga_j_num1'] = hm_bga_j_num1
    jsonData['hm_bga_p_num1'] = hm_bga_p_num1
    jsonData['hm_dj_b_num1'] = hm_dj_b_num1
    jsonData['hm_dj_j_num1'] = hm_dj_j_num1
    jsonData['hm_dj_p_num1'] = hm_dj_p_num1
    jsonData['hm_wt_b_num1'] = hm_wt_b_num1
    jsonData['hm_wt_j_num1'] = hm_wt_j_num1
    jsonData['hm_wt_p_num1'] = hm_wt_p_num1
    jsonData['hm_mv1_b_num1'] = hm_mv1_b_num1
    jsonData['hm_mv1_j_num1'] = hm_mv1_j_num1
    jsonData['hm_mv1_p_num1'] = hm_mv1_p_num1
    jsonData['hm_mv2_b_num1'] = hm_mv2_b_num1
    jsonData['hm_mv2_j_num1'] = hm_mv2_j_num1
    jsonData['hm_mv2_p_num1'] = hm_mv2_p_num1
    jsonData['hm_mv3_b_num1'] = hm_mv3_b_num1
    jsonData['hm_mv3_j_num1'] = hm_mv3_j_num1
    jsonData['hm_mv3_p_num1'] = hm_mv3_p_num1
    jsonData['hm_mv4_b_num1'] = hm_mv4_b_num1
    jsonData['hm_mv4_j_num1'] = hm_mv4_j_num1
    jsonData['hm_mv4_p_num1'] = hm_mv4_p_num1
    jsonData['hm_mv5_b_num1'] = hm_mv5_b_num1
    jsonData['hm_mv5_j_num1'] = hm_mv5_j_num1
    jsonData['hm_mv5_p_num1'] = hm_mv5_p_num1
    jsonData['hm_mv6_b_num1'] = hm_mv6_b_num1
    jsonData['hm_mv6_j_num1'] = hm_mv6_j_num1
    jsonData['hm_mv6_p_num1'] = hm_mv6_p_num1
    jsonData['hm_mv7_b_num1'] = hm_mv7_b_num1
    jsonData['hm_mv7_j_num1'] = hm_mv7_j_num1
    jsonData['hm_mv7_p_num1'] = hm_mv7_p_num1
    jsonData['hm_b_p_48'] = hm_b_p_48
    jsonData['hm_b_p_72'] = hm_b_p_72
    jsonData['hm_b_p_120'] = hm_b_p_120
    jsonData['hm_b_p_360'] = hm_b_p_360
    jsonData['hm_b_p_510'] = hm_b_p_510
    jsonData['hm_b_p_510_'] = hm_b_p_510_

    jsonData['hm_p_p_48'] = hm_p_p_48
    jsonData['hm_p_p_72'] = hm_p_p_72
    jsonData['hm_p_p_120'] = hm_p_p_120
    jsonData['hm_p_p_360'] = hm_p_p_360
    jsonData['hm_p_p_510'] = hm_p_p_510
    jsonData['hm_p_p_510_'] = hm_p_p_510_
    j = json.dumps(jsonData, cls=DecimalEncoder)

    return (j)


@app.route('/button_mv', methods=['POST'])
def button_mv():
    input = pd.read_excel('button_mv.xlsx')
    see=save(input)
    ck = ['-']
    shelf = ['-']
    sku = ['-']
    cost = ['-']
    num = ['-']
    all_cost = ['-']
    stime = ['-']
    stime1 = ['-']
    jsonData = {}

    for data in see:
        ck.append(data[0])
        shelf.append(data[1])
        sku.append(data[2])
        cost.append(data[3])
        num.append(data[4])
        all_cost.append(data[5])
        stime.append(datetime.strftime(data[6], '%Y-%m-%d'))
        stime1.append(data[7])

    new_data_1 = np.dstack((ck, shelf, sku, cost, num, all_cost, stime, stime1))
    new_data_2 = []
    for i in new_data_1[0]:
        new_data_2.append(i)
    new_data_1 = new_data_1.tolist()

    jsonData['new_data_1'] = new_data_1
    j = json.dumps(jsonData, cls=DecimalEncoder)

    return j


@app.route('/button_rk', methods=['POST'])
def button_rk():
    input = pd.read_excel('button_rk.xlsx')
    see=save(input)
    # seee.columns = ['仓库', '采购单号&快递单号', '货位', 'sku','入库件数(件数&箱数)','入库状态','时效开始时间','时效']
    ck = ['-']
    po = ['-']
    shelf = ['-']
    sku = ['-']
    num = ['-']
    state = ['-']
    stime = ['-']
    stime1 = ['-']
    jsonData = {}
    for data in see:
        ck.append(data[0])
        po.append(data[1])
        shelf.append(data[2])
        sku.append(data[3])
        num.append(data[4])
        state.append(data[5])
        stime.append(datetime.strftime(data[6], '%Y-%m-%d'))
        stime1.append(data[7])
    new_data_1 = np.dstack((ck, po, shelf, sku, num, state, stime, stime1))
    new_data_1 = new_data_1.tolist()
    jsonData['new_data_1'] = new_data_1

    j = json.dumps(jsonData, cls=DecimalEncoder)

    return j


@app.route('/button_rk_normal', methods=['POST'])
def button_rk_normal():
    input = pd.read_excel('button_rk_normal.xlsx')
    see=save(input)
    seee = np.array(see)
    seee = pd.DataFrame(seee)
    seee.columns = ['仓库', '时间', 'sku', '采购单号/异常单号', '换图情况', '状态', '时效']
    seee.to_excel("c:/入库&退货异常监控数据(两仓).xlsx")
    return seee


@app.route('/button_diaobo', methods=['POST'])
def button_diaobo():
    input = pd.read_excel('button_diaobo.xlsx')
    see=save(input)
    seee = np.array(see)
    seee = pd.DataFrame(seee)
    seee.columns = ['仓库', '订单号', '订单时间', '状态', 'sku', '件数', '时效']
    file_path = "c:/调拨监控表(两仓).xlsx"
    seee.to_excel(file_path)
    return file_path


# 入库节点监控


@app.route('/test2', methods=['POST'])
def montor():
    # sql_updata='UPDATE ueb_warehouse_shelf_sku_map  SET shelf_type = 99 WHERE shelf LIKE "%BGA%";'
    #sql = 'SELECT	warehouse_code,	purchase_order_no,	storage_position,	sku,	actual_num,	CASE		WHEN post_code_start_time IS NOT NULL 		AND post_code_end_time IS NOT NULL 		AND quality_time IS NOT NULL 		AND upper_start_time IS NOT NULL 		AND upper_end_time IS NULL THEN			"SJZ" 			WHEN post_code_start_time IS NOT NULL 			AND post_code_end_time IS NOT NULL 			AND quality_time IS NOT NULL 			AND paragraph != 11 			AND upper_start_time IS NULL THEN				"DSJ" 				WHEN post_code_start_time IS NOT NULL 				AND post_code_end_time IS NOT NULL 				AND quality_time IS NOT NULL 				AND paragraph = 11 				AND upper_start_time IS NULL THEN					"DGNZJ" 					WHEN post_code_start_time IS NULL THEN					"DTM" ELSE "else" 				END AS type,				cast(ROUND( ( unix_timestamp( now()) - unix_timestamp( quality_start_time ) ) / 3600, 2 ) as DECIMAL  ) AS s 			FROM				ueb_quality_warehousing_record 			WHERE				paragraph != 5 				AND purchase_order_no NOT LIKE "ABD%" 				AND warehouse_code IN ( "HM_AA", "SZ_AA" ) 			GROUP BY				purchase_order_no,				sku,				warehouse_code UNION			SELECT				warehouse_code,				"RK" AS purchase_order_no,				car_no AS storage_position,				"RK" AS sku,				box_number AS quality_num,				"DRK" AS type,				cast(ROUND( ( unix_timestamp( now()) - unix_timestamp( add_time ) ) / 3600, 2 ) as DECIMAL   )AS s 			FROM				ueb_express_receipt 			WHERE				STATUS = 1 				AND warehouse_type = 1 				AND is_abnormal = "2" 			AND is_quality = "2" 	AND is_end = "1"'
    #sql_fba = 'select * from (select warehouse_code,order_id,case when pay_time >0 and wait_pull_time >0 and pick_time >0 and  pack_time >0 and outstock_time > 0 and delivery_time = 0  then "DJY"when pay_time >0 and wait_pull_time >0 and pick_time >0 and ((choice_time =0 and pack_time>0) or (choice_time >0 and pack_time >0)) and outstock_time = 0  then "DCK"when pay_time >0 and wait_pull_time >0 and pick_time >0 and pack_time = 0  then "DDB"when pay_time >0 and wait_pull_time >0 and pick_time =0  then "DJH"when pay_time >0 and wait_pull_time =0  then "DLD"ELSE "else" end as `status`,CAST(order_product_number AS SIGNED) as `order_product_number`,ROUND(( unix_timestamp(now()) - greatest(pay_time,wait_pull_time,pick_time,choice_time,pack_time) ) / 3600, 2 ) AS time from ueb_order_operate_time where order_is_cancel =0 and delivery_time = 0 and order_id like "FB%"  union    select warehouse_code,order_id,case when wh_order_status=-1 then "DPK" when wh_order_status in (1)then  "DFPLD" when wh_order_status in (2)then  "DLD" else "else" end  as `status`,CAST(sum(order_product_number) AS SIGNED) as `order_product_number`,case  when wh_order_status=-1 then ROUND(( unix_timestamp(now()) - paytime_int) / 3600, 2 )  when wh_order_status in (1,2) then     ROUND(( unix_timestamp(now()) - wait_pull_time) / 3600, 2 ) else "else" end  AS time       from ueb_order where order_id like "FB%" and wh_order_status in(-1,1,2)  group by warehouse_code,order_id) a  order by time  DESC'
    #sql_xb='select * from (select warehouse_code,order_id,case when pay_time >0 and wait_pull_time >0 and pick_time >0 and  pack_time >0 and outstock_time > 0 and delivery_time = 0  then "DJY"when pay_time >0 and wait_pull_time >0 and pick_time >0 and ((choice_time =0 and pack_time>0) or (choice_time >0 and pack_time >0)) and outstock_time = 0  then "DCK"when pay_time >0 and wait_pull_time >0 and pick_time >0 and pack_time = 0  then "DDB"when pay_time >0 and wait_pull_time >0 and pick_time =0  then "DJH"when pay_time >0 and wait_pull_time =0  then "DLD"ELSE "else" end as `status`,CAST(order_product_number AS SIGNED) as `order_product_number`,ROUND(( unix_timestamp(now()) - greatest(pay_time,wait_pull_time,pick_time,choice_time,pack_time) ) / 3600, 2 ) AS time from ueb_order_operate_time where order_is_cancel =0 and delivery_time = 0 and 	 batch_no NOT LIKE "%-6-%"  union   select warehouse_code,order_id,case when wh_order_status=-1 then "DPK" when wh_order_status in (1)then  "DFPLD" when wh_order_status in (2)then  "DLD" else "else" end  as `status`,CAST(sum(order_product_number) AS SIGNED) as `order_product_number`,case  when wh_order_status=-1 then ROUND(( unix_timestamp(now()) - paytime_int) / 3600, 2 )  when wh_order_status in (1,2) then     ROUND(( unix_timestamp(now()) - wait_pull_time) / 3600, 2 ) else "else" end  AS time       from ueb_order  WHERE batch_type != 6 and wh_order_status < 9  group by warehouse_code,order_id) a  order by time  DESC'
    input = pd.read_excel('test2_xb.xlsx')
    see_xb=save(input)
    input = pd.read_excel('test2_fba.xlsx')
    see_fba=save(input)
    input = pd.read_excel('test2_sql.xlsx')
    see=save(input)
    print('aa')
    print(see_xb)
    print(see_fba)
    print(see)
    print('--')
    warehouse_xb = []
    type_xb = []
    order_xb = []
    num_xb = []
    s_xb = []
    for data_xb in see_xb:
        warehouse_xb.append(data_xb[0])
        type_xb.append(data_xb[2])
        order_xb.append(data_xb[1])
        num_xb.append(data_xb[3])
        s_xb.append(data_xb[4])
    hm_type_xb = []
    hm_order_xb = []
    hm_num_xb = []
    hm_s_xb = []
    tx_type_xb = []
    tx_order_xb = []
    tx_num_xb = []
    tx_s_xb = []
    for i in range(len(warehouse_xb)):
        if warehouse_xb[i] == 'HM_AA':
            hm_type_xb.append(type_xb[i])
            hm_order_xb.append(order_xb[i])
            hm_num_xb.append(num_xb[i])
            hm_s_xb.append(s_xb[i])
    for i in range(len(warehouse_xb)):
        if warehouse_xb[i] == 'SZ_AA':
            tx_type_xb.append(type_xb[i])
            tx_order_xb.append(order_xb[i])
            tx_num_xb.append(num_xb[i])
            tx_s_xb.append(s_xb[i])
    hm_xb_data = np.dstack((hm_type_xb, hm_order_xb, hm_num_xb, hm_s_xb))
    tx_xb_data = np.dstack((tx_type_xb, tx_order_xb, tx_num_xb, tx_s_xb))
    hm_xb_djy_b_num = []
    hm_xb_djy_j_num = []
    hm_xb_djy_time = []
    hm_xb_dfpld_b_num = []
    hm_xb_dfpld_j_num = []
    hm_xb_dfpld_time = []
    hm_xb_dpk_b_num = []
    hm_xb_dpk_j_num = []
    hm_xb_dpk_time = []
    hm_xb_dld_b_num = []
    hm_xb_dld_j_num = []
    hm_xb_dld_time = []
    hm_xb_djh_b_num = []
    hm_xb_djh_j_num = []
    hm_xb_djh_time = []
    hm_xb_ddb_b_num = []
    hm_xb_ddb_j_num = []
    hm_xb_ddb_time = []
    hm_xb_dck_b_num = []
    hm_xb_dck_j_num = []
    hm_xb_dck_time = []
    tx_xb_djy_b_num = []
    tx_xb_djy_j_num = []
    tx_xb_djy_time = []
    tx_xb_dfpld_b_num = []
    tx_xb_dfpld_j_num = []
    tx_xb_dfpld_time = []
    tx_xb_dpk_b_num = []
    tx_xb_dpk_j_num = []
    tx_xb_dpk_time = []
    tx_xb_dld_b_num = []
    tx_xb_dld_j_num = []
    tx_xb_dld_time = []
    tx_xb_djh_b_num = []
    tx_xb_djh_j_num = []
    tx_xb_djh_time = []
    tx_xb_ddb_b_num = []
    tx_xb_ddb_j_num = []
    tx_xb_ddb_time = []
    tx_xb_dck_b_num = []
    tx_xb_dck_j_num = []
    tx_xb_dck_time = []
    for i in range(len(hm_s_xb)):
        if (hm_xb_data[0][i][0] == 'DJY'):
            hm_xb_djy_b_num.append(1)
            hm_xb_djy_j_num.append(hm_xb_data[0][i][2])
            hm_xb_djy_time.append(hm_xb_data[0][i][3])
    for i in range(len(hm_s_xb)):
        if (hm_xb_data[0][i][0] == 'DFPLD'):
            hm_xb_dfpld_b_num.append(1)
            hm_xb_dfpld_j_num.append(hm_xb_data[0][i][2])
            hm_xb_dfpld_time.append(hm_xb_data[0][i][3])
    for i in range(len(hm_s_xb)):
        if (hm_xb_data[0][i][0] == 'DPK'):
            hm_xb_dpk_b_num.append(1)
            hm_xb_dpk_j_num.append(hm_xb_data[0][i][2])
            hm_xb_dpk_time.append(hm_xb_data[0][i][3])

    for i in range(len(hm_s_xb)):
        if (hm_xb_data[0][i][0] == 'DLD'):
            hm_xb_dld_b_num.append(1)
            hm_xb_dld_j_num.append(hm_xb_data[0][i][2])
            hm_xb_dld_time.append(hm_xb_data[0][i][3])
    for i in range(len(hm_s_xb)):
        if (hm_xb_data[0][i][0] == 'DJH'):
            hm_xb_djh_b_num.append(1)
            hm_xb_djh_j_num.append(hm_xb_data[0][i][2])
            hm_xb_djh_time.append(hm_xb_data[0][i][3])
    for i in range(len(hm_s_xb)):
        if (hm_xb_data[0][i][0] == 'DDB'):
            hm_xb_ddb_b_num.append(1)
            hm_xb_ddb_j_num.append(hm_xb_data[0][i][2])
            hm_xb_ddb_time.append(hm_xb_data[0][i][3])
    for i in range(len(hm_s_xb)):
        if (hm_xb_data[0][i][0] == 'DCK'):
            hm_xb_dck_b_num.append(1)
            hm_xb_dck_j_num.append(hm_xb_data[0][i][2])
            hm_xb_dck_time.append(hm_xb_data[0][i][3])
    for i in range(len(tx_s_xb)):
        if (tx_xb_data[0][i][0] == 'DJY'):
            tx_xb_djy_b_num.append(1)
            tx_xb_djy_j_num.append(tx_xb_data[0][i][2])
            tx_xb_djy_time.append(tx_xb_data[0][i][3])
    for i in range(len(tx_s_xb)):
        if (tx_xb_data[0][i][0] == 'DFPLD'):
            tx_xb_dfpld_b_num.append(1)
            tx_xb_dfpld_j_num.append(tx_xb_data[0][i][2])
            tx_xb_dfpld_time.append(tx_xb_data[0][i][3])
    for i in range(len(tx_s_xb)):
        if (tx_xb_data[0][i][0] == 'DPK'):
            tx_xb_dpk_b_num.append(1)
            tx_xb_dpk_j_num.append(tx_xb_data[0][i][2])
            tx_xb_dpk_time.append(tx_xb_data[0][i][3])
    for i in range(len(tx_s_xb)):
        if (tx_xb_data[0][i][0] == 'DLD'):
            tx_xb_dld_b_num.append(1)
            tx_xb_dld_j_num.append(tx_xb_data[0][i][2])
            tx_xb_dld_time.append(tx_xb_data[0][i][3])
    for i in range(len(tx_s_xb)):
        if (tx_xb_data[0][i][0] == 'DJH'):
            tx_xb_djh_b_num.append(1)
            tx_xb_djh_j_num.append(tx_xb_data[0][i][2])
            tx_xb_djh_time.append(tx_xb_data[0][i][3])
    for i in range(len(tx_s_xb)):
        if (tx_xb_data[0][i][0] == 'DDB'):
            tx_xb_ddb_b_num.append(1)
            tx_xb_ddb_j_num.append(tx_xb_data[0][i][2])
            tx_xb_ddb_time.append(tx_xb_data[0][i][3])
    for i in range(len(tx_s_xb)):
        if (tx_xb_data[0][i][0] == 'DCK'):
            tx_xb_dck_b_num.append(1)
            tx_xb_dck_j_num.append(tx_xb_data[0][i][2])
            tx_xb_dck_time.append(tx_xb_data[0][i][3])

    hm_xb_djy = np.dstack((hm_xb_djy_b_num,hm_xb_djy_j_num,hm_xb_djy_time))
    hm_xb_dfpld = np.dstack((hm_xb_dfpld_b_num,hm_xb_dfpld_j_num,hm_xb_dfpld_time))
    hm_xb_dpk = np.dstack((hm_xb_dpk_b_num,hm_xb_dpk_j_num,hm_xb_dpk_time))
    hm_xb_dld = np.dstack((hm_xb_dld_b_num,hm_xb_dld_j_num,hm_xb_dld_time))
    hm_xb_djh = np.dstack((hm_xb_djh_b_num,hm_xb_djh_j_num,hm_xb_djh_time))
    hm_xb_ddb = np.dstack((hm_xb_ddb_b_num,hm_xb_ddb_j_num,hm_xb_ddb_time))
    hm_xb_dck = np.dstack((hm_xb_dck_b_num,hm_xb_dck_j_num,hm_xb_dck_time))
    tx_xb_djy = np.dstack((tx_xb_djy_b_num,tx_xb_djy_j_num,tx_xb_djy_time))
    tx_xb_dfpld = np.dstack((tx_xb_dfpld_b_num,tx_xb_dfpld_j_num,tx_xb_dfpld_time))
    tx_xb_dpk = np.dstack((tx_xb_dpk_b_num,tx_xb_dpk_j_num,tx_xb_dpk_time))
    tx_xb_dld = np.dstack((tx_xb_dld_b_num,tx_xb_dld_j_num,tx_xb_dld_time))
    tx_xb_djh = np.dstack((tx_xb_djh_b_num,tx_xb_djh_j_num,tx_xb_djh_time))
    tx_xb_ddb = np.dstack((tx_xb_ddb_b_num,tx_xb_ddb_j_num,tx_xb_ddb_time))
    tx_xb_dck = np.dstack((tx_xb_dck_b_num,tx_xb_dck_j_num,tx_xb_dck_time))

    hm_xb_djy_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_xb_djy_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_xb_dfpld_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_xb_dfpld_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_xb_djy_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_xb_djy_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_xb_dfpld_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_xb_dfpld_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_xb_dpk_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_xb_dld_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_xb_djh_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_xb_ddb_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_xb_dck_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_xb_dpk_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_xb_dld_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_xb_djh_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_xb_ddb_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_xb_dck_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_xb_dpk_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_xb_dld_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_xb_djh_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_xb_ddb_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_xb_dck_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_xb_dpk_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_xb_dld_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_xb_djh_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_xb_ddb_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_xb_dck_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]




    hm_xb_b_2 = []
    hm_xb_b_4 = []
    hm_xb_b_6 = []
    hm_xb_b_8 = []
    hm_xb_b_10 = []
    hm_xb_b_12 = []
    hm_xb_b_24 = []
    hm_xb_b_24_ = []
    tx_xb_b_2 = []
    tx_xb_b_4 = []
    tx_xb_b_6 = []
    tx_xb_b_8 = []
    tx_xb_b_10 = []
    tx_xb_b_12 = []
    tx_xb_b_24 = []
    tx_xb_b_24_= []
    # hm_j_12 = []
    # hm_j_24 = []
    # hm_j_48 = []
    # hm_j_72 = []
    # hm_j_120 = []
    # hm_j_240 = []
    # hm_j_360 = []
    # hm_j_361 = []
    #
    # tx_j_12 = []
    # tx_j_24 = []
    # tx_j_48 = []
    # tx_j_72 = []
    # tx_j_120 = []
    # tx_j_240 = []
    # tx_j_360 = []
    # tx_j_361 = []

    for i in range(len(hm_xb_djy[0])):
        if float(hm_xb_djy[0][i][2]) > 0 and float(hm_xb_djy[0][i][2]) <= 2:
            hm_xb_djy_b_num1[0] = hm_xb_djy_b_num1[0] + 1
            hm_xb_djy_j_num1[0] = hm_xb_djy_j_num1[0] + float(hm_xb_djy[0][i][1])
        if float(hm_xb_djy[0][i][2]) > 2 and float(hm_xb_djy[0][i][2]) <= 4:
            hm_xb_djy_b_num1[1] = hm_xb_djy_b_num1[1] + 1
            hm_xb_djy_j_num1[1] = hm_xb_djy_j_num1[1] + float(hm_xb_djy[0][i][1])
        if float(hm_xb_djy[0][i][2]) > 4 and float(hm_xb_djy[0][i][2]) <= 6:
            hm_xb_djy_b_num1[2] = hm_xb_djy_b_num1[2] + 1
            hm_xb_djy_j_num1[2] = hm_xb_djy_j_num1[2] + float(hm_xb_djy[0][i][1])
        if float(hm_xb_djy[0][i][2]) > 6 and float(hm_xb_djy[0][i][2]) <= 8:
            hm_xb_djy_b_num1[3] = hm_xb_djy_b_num1[3] + 1
            hm_xb_djy_j_num1[3] = hm_xb_djy_j_num1[3] + float(hm_xb_djy[0][i][1])
        if float(hm_xb_djy[0][i][2]) > 8 and float(hm_xb_djy[0][i][2]) <= 10:
            hm_xb_djy_b_num1[4] = hm_xb_djy_b_num1[4] + 1
            hm_xb_djy_j_num1[4] = hm_xb_djy_j_num1[4] + float(hm_xb_djy[0][i][1])
        if float(hm_xb_djy[0][i][2]) > 10 and float(hm_xb_djy[0][i][2]) <= 12:
            hm_xb_djy_b_num1[5] = hm_xb_djy_b_num1[5] + 1
            hm_xb_djy_j_num1[5] = hm_xb_djy_j_num1[5] + float(hm_xb_djy[0][i][1])
        if float(hm_xb_djy[0][i][2]) > 12 and float(hm_xb_djy[0][i][2]) <= 24:
            hm_xb_djy_b_num1[6] = hm_xb_djy_b_num1[6] + 1
            hm_xb_djy_j_num1[6] = hm_xb_djy_j_num1[6] + float(hm_xb_djy[0][i][1])
        if float(hm_xb_djy[0][i][2]) > 24:
            hm_xb_djy_b_num1[7] = hm_xb_djy_b_num1[7] + 1
            hm_xb_djy_j_num1[7] = hm_xb_djy_j_num1[7] + float(hm_xb_djy[0][i][1])

    for i in range(len(hm_xb_dfpld[0])):
        if float(hm_xb_dfpld[0][i][2]) > 0 and float(hm_xb_dfpld[0][i][2]) <= 2:
            hm_xb_dfpld_b_num1[0] = hm_xb_dfpld_b_num1[0] + 1
            hm_xb_dfpld_j_num1[0] = hm_xb_dfpld_j_num1[0] + float(hm_xb_dfpld[0][i][1])
        if float(hm_xb_dfpld[0][i][2]) > 2 and float(hm_xb_dfpld[0][i][2]) <= 4:
            hm_xb_dfpld_b_num1[1] = hm_xb_dfpld_b_num1[1] + 1
            hm_xb_dfpld_j_num1[1] = hm_xb_dfpld_j_num1[1] + float(hm_xb_dfpld[0][i][1])
        if float(hm_xb_dfpld[0][i][2]) > 4 and float(hm_xb_dfpld[0][i][2]) <= 6:
            hm_xb_dfpld_b_num1[2] = hm_xb_dfpld_b_num1[2] + 1
            hm_xb_dfpld_j_num1[2] = hm_xb_dfpld_j_num1[2] + float(hm_xb_dfpld[0][i][1])
        if float(hm_xb_dfpld[0][i][2]) > 6 and float(hm_xb_dfpld[0][i][2]) <= 8:
            hm_xb_dfpld_b_num1[3] = hm_xb_dfpld_b_num1[3] + 1
            hm_xb_dfpld_j_num1[3] = hm_xb_dfpld_j_num1[3] + float(hm_xb_dfpld[0][i][1])
        if float(hm_xb_dfpld[0][i][2]) > 8 and float(hm_xb_dfpld[0][i][2]) <= 10:
            hm_xb_dfpld_b_num1[4] = hm_xb_dfpld_b_num1[4] + 1
            hm_xb_dfpld_j_num1[4] = hm_xb_dfpld_j_num1[4] + float(hm_xb_dfpld[0][i][1])
        if float(hm_xb_dfpld[0][i][2]) > 10 and float(hm_xb_dfpld[0][i][2]) <= 12:
            hm_xb_dfpld_b_num1[5] = hm_xb_dfpld_b_num1[5] + 1
            hm_xb_dfpld_j_num1[5] = hm_xb_dfpld_j_num1[5] + float(hm_xb_dfpld[0][i][1])
        if float(hm_xb_dfpld[0][i][2]) > 12 and float(hm_xb_dfpld[0][i][2]) <= 24:
            hm_xb_dfpld_b_num1[6] = hm_xb_dfpld_b_num1[6] + 1
            hm_xb_dfpld_j_num1[6] = hm_xb_dfpld_j_num1[6] + float(hm_xb_dfpld[0][i][1])
        if float(hm_xb_dfpld[0][i][2]) > 24:
            hm_xb_dfpld_b_num1[7] = hm_xb_dfpld_b_num1[7] + 1
            hm_xb_dfpld_j_num1[7] = hm_xb_dfpld_j_num1[7] + float(hm_xb_dfpld[0][i][1])
    for i in range(len(hm_xb_dpk[0])):
        if float(hm_xb_dpk[0][i][2]) > 0 and float(hm_xb_dpk[0][i][2]) <= 2:
            hm_xb_dpk_b_num1[0] = hm_xb_dpk_b_num1[0] + 1
            hm_xb_dpk_j_num1[0] = hm_xb_dpk_j_num1[0] + float(hm_xb_dpk[0][i][1])
        if float(hm_xb_dpk[0][i][2]) > 2 and float(hm_xb_dpk[0][i][2]) <= 4:
            hm_xb_dpk_b_num1[1] = hm_xb_dpk_b_num1[1] + 1
            hm_xb_dpk_j_num1[1] = hm_xb_dpk_j_num1[1] + float(hm_xb_dpk[0][i][1])
        if float(hm_xb_dpk[0][i][2]) > 4 and float(hm_xb_dpk[0][i][2]) <= 6:
            hm_xb_dpk_b_num1[2] = hm_xb_dpk_b_num1[2] + 1
            hm_xb_dpk_j_num1[2] = hm_xb_dpk_j_num1[2] + float(hm_xb_dpk[0][i][1])
        if float(hm_xb_dpk[0][i][2]) > 6 and float(hm_xb_dpk[0][i][2]) <= 8:
            hm_xb_dpk_b_num1[3] = hm_xb_dpk_b_num1[3] + 1
            hm_xb_dpk_j_num1[3] = hm_xb_dpk_j_num1[3] + float(hm_xb_dpk[0][i][1])
        if float(hm_xb_dpk[0][i][2]) > 8 and float(hm_xb_dpk[0][i][2]) <= 10:
            hm_xb_dpk_b_num1[4] = hm_xb_dpk_b_num1[4] + 1
            hm_xb_dpk_j_num1[4] = hm_xb_dpk_j_num1[4] + float(hm_xb_dpk[0][i][1])
        if float(hm_xb_dpk[0][i][2]) > 10 and float(hm_xb_dpk[0][i][2]) <= 12:
            hm_xb_dpk_b_num1[5] = hm_xb_dpk_b_num1[5] + 1
            hm_xb_dpk_j_num1[5] = hm_xb_dpk_j_num1[5] + float(hm_xb_dpk[0][i][1])
        if float(hm_xb_dpk[0][i][2]) > 12 and float(hm_xb_dpk[0][i][2]) <= 24:
            hm_xb_dpk_b_num1[6] = hm_xb_dpk_b_num1[6] + 1
            hm_xb_dpk_j_num1[6] = hm_xb_dpk_j_num1[6] + float(hm_xb_dpk[0][i][1])
        if float(hm_xb_dpk[0][i][2]) > 24:
            hm_xb_dpk_b_num1[7] = hm_xb_dpk_b_num1[7] + 1
            hm_xb_dpk_j_num1[7] = hm_xb_dpk_j_num1[7] + float(hm_xb_dpk[0][i][1])
    for i in range(len(hm_xb_dld[0])):
        if float(hm_xb_dld[0][i][2]) > 0 and float(hm_xb_dld[0][i][2]) <= 2:
            hm_xb_dld_b_num1[0] = hm_xb_dld_b_num1[0] + 1
            hm_xb_dld_j_num1[0] = hm_xb_dld_j_num1[0] + float(hm_xb_dld[0][i][1])
        if float(hm_xb_dld[0][i][2]) > 2 and float(hm_xb_dld[0][i][2]) <= 4:
            hm_xb_dld_b_num1[1] = hm_xb_dld_b_num1[1] + 1
            hm_xb_dld_j_num1[1] = hm_xb_dld_j_num1[1] + float(hm_xb_dld[0][i][1])
        if float(hm_xb_dld[0][i][2]) > 4 and float(hm_xb_dld[0][i][2]) <= 6:
            hm_xb_dld_b_num1[2] = hm_xb_dld_b_num1[2] + 1
            hm_xb_dld_j_num1[2] = hm_xb_dld_j_num1[2] + float(hm_xb_dld[0][i][1])
        if float(hm_xb_dld[0][i][2]) > 6 and float(hm_xb_dld[0][i][2]) <= 8:
            hm_xb_dld_b_num1[3] = hm_xb_dld_b_num1[3] + 1
            hm_xb_dld_j_num1[3] = hm_xb_dld_j_num1[3] + float(hm_xb_dld[0][i][1])
        if float(hm_xb_dld[0][i][2]) > 8 and float(hm_xb_dld[0][i][2]) <= 10:
            hm_xb_dld_b_num1[4] = hm_xb_dld_b_num1[4] + 1
            hm_xb_dld_j_num1[4] = hm_xb_dld_j_num1[4] + float(hm_xb_dld[0][i][1])
        if float(hm_xb_dld[0][i][2]) > 10 and float(hm_xb_dld[0][i][2]) <= 12:
            hm_xb_dld_b_num1[5] = hm_xb_dld_b_num1[5] + 1
            hm_xb_dld_j_num1[5] = hm_xb_dld_j_num1[5] + float(hm_xb_dld[0][i][1])
        if float(hm_xb_dld[0][i][2]) > 12 and float(hm_xb_dld[0][i][2]) <= 24:
            hm_xb_dld_b_num1[6] = hm_xb_dld_b_num1[6] + 1
            hm_xb_dld_j_num1[6] = hm_xb_dld_j_num1[6] + float(hm_xb_dld[0][i][1])
        if float(hm_xb_dld[0][i][2]) > 24:
            hm_xb_dld_b_num1[7] = hm_xb_dld_b_num1[7] + 1
            hm_xb_dld_j_num1[7] = hm_xb_dld_j_num1[7] + float(hm_xb_dld[0][i][1])

    for i in range(len(hm_xb_djh[0])):
        if float(hm_xb_djh[0][i][2]) > 0 and float(hm_xb_djh[0][i][2]) <= 2:
            hm_xb_djh_b_num1[0] = hm_xb_djh_b_num1[0] + 1
            hm_xb_djh_j_num1[0] = hm_xb_djh_j_num1[0] + float(hm_xb_djh[0][i][1])
        if float(hm_xb_djh[0][i][2]) > 2 and float(hm_xb_djh[0][i][2]) <= 4:
            hm_xb_djh_b_num1[1] = hm_xb_djh_b_num1[1] + 1
            hm_xb_djh_j_num1[1] = hm_xb_djh_j_num1[1] + float(hm_xb_djh[0][i][1])
        if float(hm_xb_djh[0][i][2]) > 4 and float(hm_xb_djh[0][i][2]) <= 6:
            hm_xb_djh_b_num1[2] = hm_xb_djh_b_num1[2] + 1
            hm_xb_djh_j_num1[2] = hm_xb_djh_j_num1[2] + float(hm_xb_djh[0][i][1])
        if float(hm_xb_djh[0][i][2]) > 6 and float(hm_xb_djh[0][i][2]) <= 8:
            hm_xb_djh_b_num1[3] = hm_xb_djh_b_num1[3] + 1
            hm_xb_djh_j_num1[3] = hm_xb_djh_j_num1[3] + float(hm_xb_djh[0][i][1])
        if float(hm_xb_djh[0][i][2]) > 8 and float(hm_xb_djh[0][i][2]) <= 10:
            hm_xb_djh_b_num1[4] = hm_xb_djh_b_num1[4] + 1
            hm_xb_djh_j_num1[4] = hm_xb_djh_j_num1[4] + float(hm_xb_djh[0][i][1])
        if float(hm_xb_djh[0][i][2]) > 10 and float(hm_xb_djh[0][i][2]) <= 12:
            hm_xb_djh_b_num1[5] = hm_xb_djh_b_num1[5] + 1
            hm_xb_djh_j_num1[5] = hm_xb_djh_j_num1[5] + float(hm_xb_djh[0][i][1])
        if float(hm_xb_djh[0][i][2]) > 12 and float(hm_xb_djh[0][i][2]) <= 24:
            hm_xb_djh_b_num1[6] = hm_xb_djh_b_num1[6] + 1
            hm_xb_djh_j_num1[6] = hm_xb_djh_j_num1[6] + float(hm_xb_djh[0][i][1])
        if float(hm_xb_djh[0][i][2]) > 24:
            hm_xb_djh_b_num1[7] = hm_xb_djh_b_num1[7] + 1
            hm_xb_djh_j_num1[7] = hm_xb_djh_j_num1[7] + float(hm_xb_djh[0][i][1])

    for i in range(len(hm_xb_ddb[0])):
        if float(hm_xb_ddb[0][i][2]) > 0 and float(hm_xb_ddb[0][i][2]) <= 2:
            hm_xb_ddb_b_num1[0] = hm_xb_ddb_b_num1[0] + 1
            hm_xb_ddb_j_num1[0] = hm_xb_ddb_j_num1[0] + float(hm_xb_ddb[0][i][1])
        if float(hm_xb_ddb[0][i][2]) > 2 and float(hm_xb_ddb[0][i][2]) <= 4:
            hm_xb_ddb_b_num1[1] = hm_xb_ddb_b_num1[1] + 1
            hm_xb_ddb_j_num1[1] = hm_xb_ddb_j_num1[1] + float(hm_xb_ddb[0][i][1])
        if float(hm_xb_ddb[0][i][2]) > 4 and float(hm_xb_ddb[0][i][2]) <= 6:
            hm_xb_ddb_b_num1[2] = hm_xb_ddb_b_num1[2] + 1
            hm_xb_ddb_j_num1[2] = hm_xb_ddb_j_num1[2] + float(hm_xb_ddb[0][i][1])
        if float(hm_xb_ddb[0][i][2]) > 6 and float(hm_xb_ddb[0][i][2]) <= 8:
            hm_xb_ddb_b_num1[3] = hm_xb_ddb_b_num1[3] + 1
            hm_xb_ddb_j_num1[3] = hm_xb_ddb_j_num1[3] + float(hm_xb_ddb[0][i][1])
        if float(hm_xb_ddb[0][i][2]) > 8 and float(hm_xb_ddb[0][i][2]) <= 10:
            hm_xb_ddb_b_num1[4] = hm_xb_ddb_b_num1[4] + 1
            hm_xb_ddb_j_num1[4] = hm_xb_ddb_j_num1[4] + float(hm_xb_ddb[0][i][1])
        if float(hm_xb_ddb[0][i][2]) > 10 and float(hm_xb_ddb[0][i][2]) <= 12:
            hm_xb_ddb_b_num1[5] = hm_xb_ddb_b_num1[5] + 1
            hm_xb_ddb_j_num1[5] = hm_xb_ddb_j_num1[5] + float(hm_xb_ddb[0][i][1])
        if float(hm_xb_ddb[0][i][2]) > 12 and float(hm_xb_ddb[0][i][2]) <= 24:
            hm_xb_ddb_b_num1[6] = hm_xb_ddb_b_num1[6] + 1
            hm_xb_ddb_j_num1[6] = hm_xb_ddb_j_num1[6] + float(hm_xb_ddb[0][i][1])
        if float(hm_xb_ddb[0][i][2]) > 24:
            hm_xb_ddb_b_num1[7] = hm_xb_ddb_b_num1[7] + 1
            hm_xb_ddb_j_num1[7] = hm_xb_ddb_j_num1[7] + float(hm_xb_ddb[0][i][1])

    for i in range(len(hm_xb_dck[0])):
        if float(hm_xb_dck[0][i][2]) > 0 and float(hm_xb_dck[0][i][2]) <= 2:
            hm_xb_dck_b_num1[0] = hm_xb_dck_b_num1[0] + 1
            hm_xb_dck_j_num1[0] = hm_xb_dck_j_num1[0] + float(hm_xb_dck[0][i][1])
        if float(hm_xb_dck[0][i][2]) > 2 and float(hm_xb_dck[0][i][2]) <= 4:
            hm_xb_dck_b_num1[1] = hm_xb_dck_b_num1[1] + 1
            hm_xb_dck_j_num1[1] = hm_xb_dck_j_num1[1] + float(hm_xb_dck[0][i][1])
        if float(hm_xb_dck[0][i][2]) > 4 and float(hm_xb_dck[0][i][2]) <= 6:
            hm_xb_dck_b_num1[2] = hm_xb_dck_b_num1[2] + 1
            hm_xb_dck_j_num1[2] = hm_xb_dck_j_num1[2] + float(hm_xb_dck[0][i][1])
        if float(hm_xb_dck[0][i][2]) > 6 and float(hm_xb_dck[0][i][2]) <= 8:
            hm_xb_dck_b_num1[3] = hm_xb_dck_b_num1[3] + 1
            hm_xb_dck_j_num1[3] = hm_xb_dck_j_num1[3] + float(hm_xb_dck[0][i][1])
        if float(hm_xb_dck[0][i][2]) > 8 and float(hm_xb_dck[0][i][2]) <= 10:
            hm_xb_dck_b_num1[4] = hm_xb_dck_b_num1[4] + 1
            hm_xb_dck_j_num1[4] = hm_xb_dck_j_num1[4] + float(hm_xb_dck[0][i][1])
        if float(hm_xb_dck[0][i][2]) > 10 and float(hm_xb_dck[0][i][2]) <= 12:
            hm_xb_dck_b_num1[5] = hm_xb_dck_b_num1[5] + 1
            hm_xb_dck_j_num1[5] = hm_xb_dck_j_num1[5] + float(hm_xb_dck[0][i][1])
        if float(hm_xb_dck[0][i][2]) > 12 and float(hm_xb_dck[0][i][2]) <= 24:
            hm_xb_dck_b_num1[6] = hm_xb_dck_b_num1[6] + 1
            hm_xb_dck_j_num1[6] = hm_xb_dck_j_num1[6] + float(hm_xb_dck[0][i][1])
        if float(hm_xb_dck[0][i][2]) > 24:
            hm_xb_dck_b_num1[7] = hm_xb_dck_b_num1[7] + 1
            hm_xb_dck_j_num1[7] = hm_xb_dck_j_num1[7] + float(hm_xb_dck[0][i][1])

    for i in range(len(tx_xb_djy[0])):
        if float(tx_xb_djy[0][i][2]) > 0 and float(tx_xb_djy[0][i][2]) <= 2:
            tx_xb_djy_b_num1[0] = tx_xb_djy_b_num1[0] + 1
            tx_xb_djy_j_num1[0] = tx_xb_djy_j_num1[0] + float(tx_xb_djy[0][i][1])
        if float(tx_xb_djy[0][i][2]) > 2 and float(tx_xb_djy[0][i][2]) <= 4:
            tx_xb_djy_b_num1[1] = tx_xb_djy_b_num1[1] + 1
            tx_xb_djy_j_num1[1] = tx_xb_djy_j_num1[1] + float(tx_xb_djy[0][i][1])
        if float(tx_xb_djy[0][i][2]) > 4 and float(tx_xb_djy[0][i][2]) <= 6:
            tx_xb_djy_b_num1[2] = tx_xb_djy_b_num1[2] + 1
            tx_xb_djy_j_num1[2] = tx_xb_djy_j_num1[2] + float(tx_xb_djy[0][i][1])
        if float(tx_xb_djy[0][i][2]) > 6 and float(tx_xb_djy[0][i][2]) <= 8:
            tx_xb_djy_b_num1[3] = tx_xb_djy_b_num1[3] + 1
            tx_xb_djy_j_num1[3] = tx_xb_djy_j_num1[3] + float(tx_xb_djy[0][i][1])
        if float(tx_xb_djy[0][i][2]) > 8 and float(tx_xb_djy[0][i][2]) <= 10:
            tx_xb_djy_b_num1[4] = tx_xb_djy_b_num1[4] + 1
            tx_xb_djy_j_num1[4] = tx_xb_djy_j_num1[4] + float(tx_xb_djy[0][i][1])
        if float(tx_xb_djy[0][i][2]) > 10 and float(tx_xb_djy[0][i][2]) <= 12:
            tx_xb_djy_b_num1[5] = tx_xb_djy_b_num1[5] + 1
            tx_xb_djy_j_num1[5] = tx_xb_djy_j_num1[5] + float(tx_xb_djy[0][i][1])
        if float(tx_xb_djy[0][i][2]) > 12 and float(tx_xb_djy[0][i][2]) <= 24:
            tx_xb_djy_b_num1[6] = tx_xb_djy_b_num1[6] + 1
            tx_xb_djy_j_num1[6] = tx_xb_djy_j_num1[6] + float(tx_xb_djy[0][i][1])
        if float(tx_xb_djy[0][i][2]) > 24:
            tx_xb_djy_b_num1[7] = tx_xb_djy_b_num1[7] + 1
            tx_xb_djy_j_num1[7] = tx_xb_djy_j_num1[7] + float(tx_xb_djy[0][i][1])
    for i in range(len(tx_xb_dfpld[0])):
        if float(tx_xb_dfpld[0][i][2]) > 0 and float(tx_xb_dfpld[0][i][2]) <= 2:
            tx_xb_dfpld_b_num1[0] = tx_xb_dfpld_b_num1[0] + 1
            tx_xb_dfpld_j_num1[0] = tx_xb_dfpld_j_num1[0] + float(tx_xb_dfpld[0][i][1])
        if float(tx_xb_dfpld[0][i][2]) > 2 and float(tx_xb_dfpld[0][i][2]) <= 4:
            tx_xb_dfpld_b_num1[1] = tx_xb_dfpld_b_num1[1] + 1
            tx_xb_dfpld_j_num1[1] = tx_xb_dfpld_j_num1[1] + float(tx_xb_dfpld[0][i][1])
        if float(tx_xb_dfpld[0][i][2]) > 4 and float(tx_xb_dfpld[0][i][2]) <= 6:
            tx_xb_dfpld_b_num1[2] = tx_xb_dfpld_b_num1[2] + 1
            tx_xb_dfpld_j_num1[2] = tx_xb_dfpld_j_num1[2] + float(tx_xb_dfpld[0][i][1])
        if float(tx_xb_dfpld[0][i][2]) > 6 and float(tx_xb_dfpld[0][i][2]) <= 8:
            tx_xb_dfpld_b_num1[3] = tx_xb_dfpld_b_num1[3] + 1
            tx_xb_dfpld_j_num1[3] = tx_xb_dfpld_j_num1[3] + float(tx_xb_dfpld[0][i][1])
        if float(tx_xb_dfpld[0][i][2]) > 8 and float(tx_xb_dfpld[0][i][2]) <= 10:
            tx_xb_dfpld_b_num1[4] = tx_xb_dfpld_b_num1[4] + 1
            tx_xb_dfpld_j_num1[4] = tx_xb_dfpld_j_num1[4] + float(tx_xb_dfpld[0][i][1])
        if float(tx_xb_dfpld[0][i][2]) > 10 and float(tx_xb_dfpld[0][i][2]) <= 12:
            tx_xb_dfpld_b_num1[5] = tx_xb_dfpld_b_num1[5] + 1
            tx_xb_dfpld_j_num1[5] = tx_xb_dfpld_j_num1[5] + float(tx_xb_dfpld[0][i][1])
        if float(tx_xb_dfpld[0][i][2]) > 12 and float(tx_xb_dfpld[0][i][2]) <= 24:
            tx_xb_dfpld_b_num1[6] = tx_xb_dfpld_b_num1[6] + 1
            tx_xb_dfpld_j_num1[6] = tx_xb_dfpld_j_num1[6] + float(tx_xb_dfpld[0][i][1])
        if float(tx_xb_dfpld[0][i][2]) > 24:
            tx_xb_dfpld_b_num1[7] = tx_xb_dfpld_b_num1[7] + 1
            tx_xb_dfpld_j_num1[7] = tx_xb_dfpld_j_num1[7] + float(tx_xb_dfpld[0][i][1])
    for i in range(len(tx_xb_dpk[0])):
        if float(tx_xb_dpk[0][i][2]) > 0 and float(tx_xb_dpk[0][i][2]) <= 2:
            tx_xb_dpk_b_num1[0] = tx_xb_dpk_b_num1[0] + 1
            tx_xb_dpk_j_num1[0] = tx_xb_dpk_j_num1[0] + float(tx_xb_dpk[0][i][1])
        if float(tx_xb_dpk[0][i][2]) > 2 and float(tx_xb_dpk[0][i][2]) <= 4:
            tx_xb_dpk_b_num1[1] = tx_xb_dpk_b_num1[1] + 1
            tx_xb_dpk_j_num1[1] = tx_xb_dpk_j_num1[1] + float(tx_xb_dpk[0][i][1])
        if float(tx_xb_dpk[0][i][2]) > 4 and float(tx_xb_dpk[0][i][2]) <= 6:
            tx_xb_dpk_b_num1[2] = tx_xb_dpk_b_num1[2] + 1
            tx_xb_dpk_j_num1[2] = tx_xb_dpk_j_num1[2] + float(tx_xb_dpk[0][i][1])
        if float(tx_xb_dpk[0][i][2]) > 6 and float(tx_xb_dpk[0][i][2]) <= 8:
            tx_xb_dpk_b_num1[3] = tx_xb_dpk_b_num1[3] + 1
            tx_xb_dpk_j_num1[3] = tx_xb_dpk_j_num1[3] + float(tx_xb_dpk[0][i][1])
        if float(tx_xb_dpk[0][i][2]) > 8 and float(tx_xb_dpk[0][i][2]) <= 10:
            tx_xb_dpk_b_num1[4] = tx_xb_dpk_b_num1[4] + 1
            tx_xb_dpk_j_num1[4] = tx_xb_dpk_j_num1[4] + float(tx_xb_dpk[0][i][1])
        if float(tx_xb_dpk[0][i][2]) > 10 and float(tx_xb_dpk[0][i][2]) <= 12:
            tx_xb_dpk_b_num1[5] = tx_xb_dpk_b_num1[5] + 1
            tx_xb_dpk_j_num1[5] = tx_xb_dpk_j_num1[5] + float(tx_xb_dpk[0][i][1])
        if float(tx_xb_dpk[0][i][2]) > 12 and float(tx_xb_dpk[0][i][2]) <= 24:
            tx_xb_dpk_b_num1[6] = tx_xb_dpk_b_num1[6] + 1
            tx_xb_dpk_j_num1[6] = tx_xb_dpk_j_num1[6] + float(tx_xb_dpk[0][i][1])
        if float(tx_xb_dpk[0][i][2]) > 24:
            tx_xb_dpk_b_num1[7] = tx_xb_dpk_b_num1[7] + 1
            tx_xb_dpk_j_num1[7] = tx_xb_dpk_j_num1[7] + float(tx_xb_dpk[0][i][1])

    for i in range(len(tx_xb_dld[0])):
        if float(tx_xb_dld[0][i][2]) > 0 and float(tx_xb_dld[0][i][2]) <= 2:
            tx_xb_dld_b_num1[0] = tx_xb_dld_b_num1[0] + 1
            tx_xb_dld_j_num1[0] = tx_xb_dld_j_num1[0] + float(tx_xb_dld[0][i][1])
        if float(tx_xb_dld[0][i][2]) > 2 and float(tx_xb_dld[0][i][2]) <= 4:
            tx_xb_dld_b_num1[1] = tx_xb_dld_b_num1[1] + 1
            tx_xb_dld_j_num1[1] = tx_xb_dld_j_num1[1] + float(tx_xb_dld[0][i][1])
        if float(tx_xb_dld[0][i][2]) > 4 and float(tx_xb_dld[0][i][2]) <= 6:
            tx_xb_dld_b_num1[2] = tx_xb_dld_b_num1[2] + 1
            tx_xb_dld_j_num1[2] = tx_xb_dld_j_num1[2] + float(tx_xb_dld[0][i][1])
        if float(tx_xb_dld[0][i][2]) > 6 and float(tx_xb_dld[0][i][2]) <= 8:
            tx_xb_dld_b_num1[3] = tx_xb_dld_b_num1[3] + 1
            tx_xb_dld_j_num1[3] = tx_xb_dld_j_num1[3] + float(tx_xb_dld[0][i][1])
        if float(tx_xb_dld[0][i][2]) > 8 and float(tx_xb_dld[0][i][2]) <= 10:
            tx_xb_dld_b_num1[4] = tx_xb_dld_b_num1[4] + 1
            tx_xb_dld_j_num1[4] = tx_xb_dld_j_num1[4] + float(tx_xb_dld[0][i][1])
        if float(tx_xb_dld[0][i][2]) > 10 and float(tx_xb_dld[0][i][2]) <= 12:
            tx_xb_dld_b_num1[5] = tx_xb_dld_b_num1[5] + 1
            tx_xb_dld_j_num1[5] = tx_xb_dld_j_num1[5] + float(tx_xb_dld[0][i][1])
        if float(tx_xb_dld[0][i][2]) > 12 and float(tx_xb_dld[0][i][2]) <= 24:
            tx_xb_dld_b_num1[6] = tx_xb_dld_b_num1[6] + 1
            tx_xb_dld_j_num1[6] = tx_xb_dld_j_num1[6] + float(tx_xb_dld[0][i][1])
        if float(tx_xb_dld[0][i][2]) > 24:
            tx_xb_dld_b_num1[7] = tx_xb_dld_b_num1[7] + 1
            tx_xb_dld_j_num1[7] = tx_xb_dld_j_num1[7] + float(tx_xb_dld[0][i][1])

    for i in range(len(tx_xb_djh[0])):
        if float(tx_xb_djh[0][i][2]) > 0 and float(tx_xb_djh[0][i][2]) <= 2:
            tx_xb_djh_b_num1[0] = tx_xb_djh_b_num1[0] + 1
            tx_xb_djh_j_num1[0] = tx_xb_djh_j_num1[0] + float(tx_xb_djh[0][i][1])
        if float(tx_xb_djh[0][i][2]) > 2 and float(tx_xb_djh[0][i][2]) <= 4:
            tx_xb_djh_b_num1[1] = tx_xb_djh_b_num1[1] + 1
            tx_xb_djh_j_num1[1] = tx_xb_djh_j_num1[1] + float(tx_xb_djh[0][i][1])
        if float(tx_xb_djh[0][i][2]) > 4 and float(tx_xb_djh[0][i][2]) <= 6:
            tx_xb_djh_b_num1[2] = tx_xb_djh_b_num1[2] + 1
            tx_xb_djh_j_num1[2] = tx_xb_djh_j_num1[2] + float(tx_xb_djh[0][i][1])
        if float(tx_xb_djh[0][i][2]) > 6 and float(tx_xb_djh[0][i][2]) <= 8:
            tx_xb_djh_b_num1[3] = tx_xb_djh_b_num1[3] + 1
            tx_xb_djh_j_num1[3] = tx_xb_djh_j_num1[3] + float(tx_xb_djh[0][i][1])
        if float(tx_xb_djh[0][i][2]) > 8 and float(tx_xb_djh[0][i][2]) <= 10:
            tx_xb_djh_b_num1[4] = tx_xb_djh_b_num1[4] + 1
            tx_xb_djh_j_num1[4] = tx_xb_djh_j_num1[4] + float(tx_xb_djh[0][i][1])
        if float(tx_xb_djh[0][i][2]) > 10 and float(tx_xb_djh[0][i][2]) <= 12:
            tx_xb_djh_b_num1[5] = tx_xb_djh_b_num1[5] + 1
            tx_xb_djh_j_num1[5] = tx_xb_djh_j_num1[5] + float(tx_xb_djh[0][i][1])
        if float(tx_xb_djh[0][i][2]) > 12 and float(tx_xb_djh[0][i][2]) <= 24:
            tx_xb_djh_b_num1[6] = tx_xb_djh_b_num1[6] + 1
            tx_xb_djh_j_num1[6] = tx_xb_djh_j_num1[6] + float(tx_xb_djh[0][i][1])
        if float(tx_xb_djh[0][i][2]) > 24:
            tx_xb_djh_b_num1[7] = tx_xb_djh_b_num1[7] + 1
            tx_xb_djh_j_num1[7] = tx_xb_djh_j_num1[7] + float(tx_xb_djh[0][i][1])

    for i in range(len(tx_xb_ddb[0])):
        if float(tx_xb_ddb[0][i][2]) > 0 and float(tx_xb_ddb[0][i][2]) <= 2:
            tx_xb_ddb_b_num1[0] = tx_xb_ddb_b_num1[0] + 1
            tx_xb_ddb_j_num1[0] = tx_xb_ddb_j_num1[0] + float(tx_xb_ddb[0][i][1])
        if float(tx_xb_ddb[0][i][2]) > 2 and float(tx_xb_ddb[0][i][2]) <= 4:
            tx_xb_ddb_b_num1[1] = tx_xb_ddb_b_num1[1] + 1
            tx_xb_ddb_j_num1[1] = tx_xb_ddb_j_num1[1] + float(tx_xb_ddb[0][i][1])
        if float(tx_xb_ddb[0][i][2]) > 4 and float(tx_xb_ddb[0][i][2]) <= 6:
            tx_xb_ddb_b_num1[2] = tx_xb_ddb_b_num1[2] + 1
            tx_xb_ddb_j_num1[2] = tx_xb_ddb_j_num1[2] + float(tx_xb_ddb[0][i][1])
        if float(tx_xb_ddb[0][i][2]) > 6 and float(tx_xb_ddb[0][i][2]) <= 8:
            tx_xb_ddb_b_num1[3] = tx_xb_ddb_b_num1[3] + 1
            tx_xb_ddb_j_num1[3] = tx_xb_ddb_j_num1[3] + float(tx_xb_ddb[0][i][1])
        if float(tx_xb_ddb[0][i][2]) > 8 and float(tx_xb_ddb[0][i][2]) <= 10:
            tx_xb_ddb_b_num1[4] = tx_xb_ddb_b_num1[4] + 1
            tx_xb_ddb_j_num1[4] = tx_xb_ddb_j_num1[4] + float(tx_xb_ddb[0][i][1])
        if float(tx_xb_ddb[0][i][2]) > 10 and float(tx_xb_ddb[0][i][2]) <= 12:
            tx_xb_ddb_b_num1[5] = tx_xb_ddb_b_num1[5] + 1
            tx_xb_ddb_j_num1[5] = tx_xb_ddb_j_num1[5] + float(tx_xb_ddb[0][i][1])
        if float(tx_xb_ddb[0][i][2]) > 12 and float(tx_xb_ddb[0][i][2]) <= 24:
            tx_xb_ddb_b_num1[6] = tx_xb_ddb_b_num1[6] + 1
            tx_xb_ddb_j_num1[6] = tx_xb_ddb_j_num1[6] + float(tx_xb_ddb[0][i][1])
        if float(tx_xb_ddb[0][i][2]) > 24:
            tx_xb_ddb_b_num1[7] = tx_xb_ddb_b_num1[7] + 1
            tx_xb_ddb_j_num1[7] = tx_xb_ddb_j_num1[7] + float(tx_xb_ddb[0][i][1])

    for i in range(len(tx_xb_dck[0])):
        if float(tx_xb_dck[0][i][2]) > 0 and float(tx_xb_dck[0][i][2]) <= 2:
            tx_xb_dck_b_num1[0] = tx_xb_dck_b_num1[0] + 1
            tx_xb_dck_j_num1[0] = tx_xb_dck_j_num1[0] + float(tx_xb_dck[0][i][1])
        if float(tx_xb_dck[0][i][2]) > 2 and float(tx_xb_dck[0][i][2]) <= 4:
            tx_xb_dck_b_num1[1] = tx_xb_dck_b_num1[1] + 1
            tx_xb_dck_j_num1[1] = tx_xb_dck_j_num1[1] + float(tx_xb_dck[0][i][1])
        if float(tx_xb_dck[0][i][2]) > 4 and float(tx_xb_dck[0][i][2]) <= 6:
            tx_xb_dck_b_num1[2] = tx_xb_dck_b_num1[2] + 1
            tx_xb_dck_j_num1[2] = tx_xb_dck_j_num1[2] + float(tx_xb_dck[0][i][1])
        if float(tx_xb_dck[0][i][2]) > 6 and float(tx_xb_dck[0][i][2]) <= 8:
            tx_xb_dck_b_num1[3] = tx_xb_dck_b_num1[3] + 1
            tx_xb_dck_j_num1[3] = tx_xb_dck_j_num1[3] + float(tx_xb_dck[0][i][1])
        if float(tx_xb_dck[0][i][2]) > 8 and float(tx_xb_dck[0][i][2]) <= 10:
            tx_xb_dck_b_num1[4] = tx_xb_dck_b_num1[4] + 1
            tx_xb_dck_j_num1[4] = tx_xb_dck_j_num1[4] + float(tx_xb_dck[0][i][1])
        if float(tx_xb_dck[0][i][2]) > 10 and float(tx_xb_dck[0][i][2]) <= 12:
            tx_xb_dck_b_num1[5] = tx_xb_dck_b_num1[5] + 1
            tx_xb_dck_j_num1[5] = tx_xb_dck_j_num1[5] + float(tx_xb_dck[0][i][1])
        if float(tx_xb_dck[0][i][2]) > 12 and float(tx_xb_dck[0][i][2]) <= 24:
            tx_xb_dck_b_num1[6] = tx_xb_dck_b_num1[6] + 1
            tx_xb_dck_j_num1[6] = tx_xb_dck_j_num1[6] + float(tx_xb_dck[0][i][1])
        if float(tx_xb_dck[0][i][2]) > 24:
            tx_xb_dck_b_num1[7] = tx_xb_dck_b_num1[7] + 1
            tx_xb_dck_j_num1[7] = tx_xb_dck_j_num1[7] + float(tx_xb_dck[0][i][1])

    hm_b_xb_num_2 = np.r_[
        hm_xb_dpk_b_num1[0], hm_xb_dfpld_b_num1[0], hm_xb_dld_b_num1[0], hm_xb_djh_b_num1[0], hm_xb_ddb_b_num1[0], hm_xb_dck_b_num1[0],
        hm_xb_djy_b_num1[0]]

    hm_b_xb_num_4 = np.r_[
        hm_xb_dpk_b_num1[1], hm_xb_dfpld_b_num1[1], hm_xb_dld_b_num1[1], hm_xb_djh_b_num1[1], hm_xb_ddb_b_num1[1], hm_xb_dck_b_num1[1],
        hm_xb_djy_b_num1[1]]
    hm_b_xb_num_6 = np.r_[
        hm_xb_dpk_b_num1[2], hm_xb_dfpld_b_num1[2], hm_xb_dld_b_num1[2], hm_xb_djh_b_num1[2], hm_xb_ddb_b_num1[2], hm_xb_dck_b_num1[2],
        hm_xb_djy_b_num1[2]]
    hm_b_xb_num_8 = np.r_[
        hm_xb_dpk_b_num1[3], hm_xb_dfpld_b_num1[3], hm_xb_dld_b_num1[3], hm_xb_djh_b_num1[3], hm_xb_ddb_b_num1[3], hm_xb_dck_b_num1[3],
        hm_xb_djy_b_num1[3]]
    hm_b_xb_num_10 = np.r_[
        hm_xb_dpk_b_num1[4], hm_xb_dfpld_b_num1[4], hm_xb_dld_b_num1[4], hm_xb_djh_b_num1[4], hm_xb_ddb_b_num1[4], hm_xb_dck_b_num1[4],
        hm_xb_djy_b_num1[4]]
    hm_b_xb_num_12 = np.r_[
        hm_xb_dpk_b_num1[5], hm_xb_dfpld_b_num1[5], hm_xb_dld_b_num1[5], hm_xb_djh_b_num1[5], hm_xb_ddb_b_num1[5], hm_xb_dck_b_num1[5],
        hm_xb_djy_b_num1[5]]
    hm_b_xb_num_24 = np.r_[
        hm_xb_dpk_b_num1[6], hm_xb_dfpld_b_num1[6], hm_xb_dld_b_num1[6], hm_xb_djh_b_num1[6], hm_xb_ddb_b_num1[6], hm_xb_dck_b_num1[6],
        hm_xb_djy_b_num1[6]]
    hm_b_xb_num_24_ = np.r_[
        hm_xb_dpk_b_num1[7], hm_xb_dfpld_b_num1[7], hm_xb_dld_b_num1[7], hm_xb_djh_b_num1[7], hm_xb_ddb_b_num1[7], hm_xb_dck_b_num1[7],
        hm_xb_djy_b_num1[7]]




    tx_b_xb_num_2 = np.r_[
        tx_xb_dpk_b_num1[0], tx_xb_dfpld_b_num1[0], tx_xb_dld_b_num1[0], tx_xb_djh_b_num1[0], tx_xb_ddb_b_num1[0], tx_xb_dck_b_num1[0],
        tx_xb_djy_b_num1[0]]

    tx_b_xb_num_4 = np.r_[
        tx_xb_dpk_b_num1[1], tx_xb_dfpld_b_num1[1], tx_xb_dld_b_num1[1], tx_xb_djh_b_num1[1], tx_xb_ddb_b_num1[1], tx_xb_dck_b_num1[1],
        tx_xb_djy_b_num1[1]]
    tx_b_xb_num_6 = np.r_[
        tx_xb_dpk_b_num1[2], tx_xb_dfpld_b_num1[2], tx_xb_dld_b_num1[2], tx_xb_djh_b_num1[2], tx_xb_ddb_b_num1[2], tx_xb_dck_b_num1[2],
        tx_xb_djy_b_num1[2]]
    tx_b_xb_num_8 = np.r_[
        tx_xb_dpk_b_num1[3], tx_xb_dfpld_b_num1[3], tx_xb_dld_b_num1[3], tx_xb_djh_b_num1[3], tx_xb_ddb_b_num1[3], tx_xb_dck_b_num1[3],
        tx_xb_djy_b_num1[3]]
    tx_b_xb_num_10 = np.r_[
        tx_xb_dpk_b_num1[4], tx_xb_dfpld_b_num1[4], tx_xb_dld_b_num1[4], tx_xb_djh_b_num1[4], tx_xb_ddb_b_num1[4], tx_xb_dck_b_num1[4],
        tx_xb_djy_b_num1[4]]
    tx_b_xb_num_12 = np.r_[
        tx_xb_dpk_b_num1[5], tx_xb_dfpld_b_num1[5], tx_xb_dld_b_num1[5], tx_xb_djh_b_num1[5], tx_xb_ddb_b_num1[5], tx_xb_dck_b_num1[5],
        tx_xb_djy_b_num1[5]]
    tx_b_xb_num_24 = np.r_[
        tx_xb_dpk_b_num1[6], tx_xb_dfpld_b_num1[6], tx_xb_dld_b_num1[6], tx_xb_djh_b_num1[6], tx_xb_ddb_b_num1[6], tx_xb_dck_b_num1[6],
        tx_xb_djy_b_num1[6]]
    tx_b_xb_num_24_ = np.r_[
        tx_xb_dpk_b_num1[7], tx_xb_dfpld_b_num1[7], tx_xb_dld_b_num1[7], tx_xb_djh_b_num1[7], tx_xb_ddb_b_num1[7], tx_xb_dck_b_num1[7],
        tx_xb_djy_b_num1[7]]
    print(hm_b_xb_num_2)

    arrayA = np.divide(hm_b_xb_num_2, max(hm_b_xb_num_2), out=np.zeros_like(hm_b_xb_num_2, dtype=np.float64),
                       where=max(hm_b_xb_num_2) != 0)
    for i in range(len(hm_b_xb_num_2)):
        hm_xb_b_2.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_xb_num_2[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_xb_num_2)):
            hm_b_xb_num_2[i] = '{:.2%}'.format(a)

    arrayA = np.divide(hm_b_xb_num_4, max(hm_b_xb_num_4), out=np.zeros_like(hm_b_xb_num_4, dtype=np.float64),
                       where=max(hm_b_xb_num_4) != 0)
    for i in range(len(hm_b_xb_num_4)):
        hm_xb_b_4.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_xb_num_4[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_xb_num_4)):
            hm_b_xb_num_4[i] = '{:.2%}'.format(a)

    arrayA = np.divide(hm_b_xb_num_6, max(hm_b_xb_num_6), out=np.zeros_like(hm_b_xb_num_6, dtype=np.float64),
                       where=max(hm_b_xb_num_6) != 0)
    for i in range(len(hm_b_xb_num_6)):
        hm_xb_b_6.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_xb_num_6[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_xb_num_6)):
            hm_b_xb_num_6[i] = '{:.2%}'.format(a)

    arrayA = np.divide(hm_b_xb_num_8, max(hm_b_xb_num_8), out=np.zeros_like(hm_b_xb_num_8, dtype=np.float64),
                       where=max(hm_b_xb_num_8) != 0)
    for i in range(len(hm_b_xb_num_8)):
        hm_xb_b_8.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_xb_num_8[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_xb_num_8)):
            hm_b_xb_num_8[i] = '{:.2%}'.format(a)

    arrayA = np.divide(hm_b_xb_num_10, max(hm_b_xb_num_10), out=np.zeros_like(hm_b_xb_num_10, dtype=np.float64),
                       where=max(hm_b_xb_num_10) != 0)
    for i in range(len(hm_b_xb_num_10)):
        hm_xb_b_10.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_xb_num_10[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_xb_num_10)):
            hm_b_xb_num_10[i] = '{:.2%}'.format(a)

    arrayA = np.divide(hm_b_xb_num_12, max(hm_b_xb_num_12), out=np.zeros_like(hm_b_xb_num_12, dtype=np.float64),
                       where=max(hm_b_xb_num_12) != 0)
    for i in range(len(hm_b_xb_num_12)):
        hm_xb_b_12.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_xb_num_12[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_xb_num_12)):
            hm_b_xb_num_12[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_b_xb_num_24, max(hm_b_xb_num_24), out=np.zeros_like(hm_b_xb_num_24, dtype=np.float64),
                       where=max(hm_b_xb_num_24) != 0)
    for i in range(len(hm_b_xb_num_24)):
        hm_xb_b_24.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_xb_num_24[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_xb_num_24)):
            hm_b_xb_num_24[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_b_xb_num_24_, max(hm_b_xb_num_24_), out=np.zeros_like(hm_b_xb_num_24_, dtype=np.float64),
                       where=max(hm_b_xb_num_24_) != 0)
    for i in range(len(hm_b_xb_num_24_)):
        hm_xb_b_24_.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_xb_num_24_[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_xb_num_24_)):
            hm_b_xb_num_24_[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_b_xb_num_2, max(tx_b_xb_num_2), out=np.zeros_like(tx_b_xb_num_2, dtype=np.float64),
                       where=max(tx_b_xb_num_2) != 0)
    for i in range(len(tx_b_xb_num_2)):
        tx_xb_b_2.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_xb_num_2[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_xb_num_2)):
            tx_b_xb_num_2[i] = '{:.2%}'.format(a)

    arrayA = np.divide(tx_b_xb_num_4, max(tx_b_xb_num_4), out=np.zeros_like(tx_b_xb_num_4, dtype=np.float64),
                       where=max(tx_b_xb_num_4) != 0)
    for i in range(len(tx_b_xb_num_4)):
        tx_xb_b_4.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_xb_num_4[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_xb_num_4)):
            tx_b_xb_num_4[i] = '{:.2%}'.format(a)

    arrayA = np.divide(tx_b_xb_num_6, max(tx_b_xb_num_6), out=np.zeros_like(tx_b_xb_num_6, dtype=np.float64),
                       where=max(tx_b_xb_num_6) != 0)
    for i in range(len(tx_b_xb_num_6)):
        tx_xb_b_6.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_xb_num_6[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_xb_num_6)):
            tx_b_xb_num_6[i] = '{:.2%}'.format(a)

    arrayA = np.divide(tx_b_xb_num_8, max(tx_b_xb_num_8), out=np.zeros_like(tx_b_xb_num_8, dtype=np.float64),
                       where=max(tx_b_xb_num_8) != 0)
    for i in range(len(tx_b_xb_num_8)):
        tx_xb_b_8.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_xb_num_8[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_xb_num_8)):
            tx_b_xb_num_8[i] = '{:.2%}'.format(a)

    arrayA = np.divide(tx_b_xb_num_10, max(tx_b_xb_num_10), out=np.zeros_like(tx_b_xb_num_10, dtype=np.float64),
                       where=max(tx_b_xb_num_10) != 0)
    for i in range(len(tx_b_xb_num_10)):
        tx_xb_b_10.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_xb_num_10[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_xb_num_10)):
            tx_b_xb_num_10[i] = '{:.2%}'.format(a)

    arrayA = np.divide(tx_b_xb_num_12, max(tx_b_xb_num_12), out=np.zeros_like(tx_b_xb_num_12, dtype=np.float64),
                       where=max(tx_b_xb_num_12) != 0)
    for i in range(len(tx_b_xb_num_12)):
        tx_xb_b_12.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_xb_num_12[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_xb_num_12)):
            tx_b_xb_num_12[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_b_xb_num_24, max(tx_b_xb_num_24), out=np.zeros_like(tx_b_xb_num_24, dtype=np.float64),
                       where=max(tx_b_xb_num_24) != 0)
    for i in range(len(tx_b_xb_num_24)):
        tx_xb_b_24.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_xb_num_24[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_xb_num_24)):
            tx_b_xb_num_24[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_b_xb_num_24_, max(tx_b_xb_num_24_), out=np.zeros_like(tx_b_xb_num_24_, dtype=np.float64),
                       where=max(tx_b_xb_num_24_) != 0)
    for i in range(len(tx_b_xb_num_24_)):
        tx_xb_b_24_.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_xb_num_24_[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_xb_num_24_)):
            tx_b_xb_num_24_[i] = '{:.2%}'.format(a)


    warehouse_fba = []
    type_fba = []
    order_fba = []
    num_fba = []
    s_fba = []

    for data_fba in see_fba:
        warehouse_fba.append(data_fba[0])
        type_fba.append(data_fba[2])
        order_fba.append(data_fba[1])
        num_fba.append(data_fba[3])
        s_fba.append(data_fba[4])
    print(num_fba)
    hm_type_fba = []
    hm_order_fba = []
    hm_num_fba = []
    hm_s_fba = []
    tx_type_fba = []
    tx_order_fba = []
    tx_num_fba = []
    tx_s_fba = []
    for i in range(len(warehouse_fba)):
        if warehouse_fba[i] == 'HM_AA':
            hm_type_fba.append(type_fba[i])
            hm_order_fba.append(order_fba[i])
            hm_num_fba.append(num_fba[i])
            hm_s_fba.append(s_fba[i])
    for i in range(len(warehouse_fba)):
        if warehouse_fba[i] == 'SZ_AA':
            tx_type_fba.append(type_fba[i])
            tx_order_fba.append(order_fba[i])
            tx_num_fba.append(num_fba[i])
            tx_s_fba.append(s_fba[i])
    hm_fba_data = np.dstack((hm_type_fba, hm_order_fba, hm_num_fba, hm_s_fba))
    tx_fba_data = np.dstack((tx_type_fba, tx_order_fba, tx_num_fba, tx_s_fba))

    hm_djy_b_num = []
    hm_djy_j_num = []
    hm_djy_time = []
    hm_dfpld_b_num = []
    hm_dfpld_j_num = []
    hm_dfpld_time = []
    hm_dpk_b_num = []
    hm_dpk_j_num = []
    hm_dpk_time = []
    hm_dld_b_num = []
    hm_dld_j_num = []
    hm_dld_time = []
    hm_djh_b_num = []
    hm_djh_j_num = []
    hm_djh_time = []
    hm_ddb_b_num = []
    hm_ddb_j_num = []
    hm_ddb_time = []
    hm_dck_b_num = []
    hm_dck_j_num = []
    hm_dck_time = []
    tx_djy_b_num = []
    tx_djy_j_num = []
    tx_djy_time = []
    tx_dfpld_b_num = []
    tx_dfpld_j_num = []
    tx_dfpld_time = []
    tx_dpk_b_num = []
    tx_dpk_j_num = []
    tx_dpk_time = []
    tx_dld_b_num = []
    tx_dld_j_num = []
    tx_dld_time = []
    tx_djh_b_num = []
    tx_djh_j_num = []
    tx_djh_time = []
    tx_ddb_b_num = []
    tx_ddb_j_num = []
    tx_ddb_time = []
    tx_dck_b_num = []
    tx_dck_j_num = []
    tx_dck_time = []




    for i in range(len(hm_s_fba)):
        if (hm_fba_data[0][i][0] == 'DJY'):
            hm_djy_b_num.append(1)
            hm_djy_j_num.append(hm_fba_data[0][i][2])
            hm_djy_time.append(hm_fba_data[0][i][3])
    for i in range(len(hm_s_fba)):
        if (hm_fba_data[0][i][0] == 'DFPLD'):
            hm_dfpld_b_num.append(1)
            hm_dfpld_j_num.append(hm_fba_data[0][i][2])
            hm_dfpld_time.append(hm_fba_data[0][i][3])
    for i in range(len(hm_s_fba)):
        if (hm_fba_data[0][i][0] == 'DPK'):
            hm_dpk_b_num.append(1)
            hm_dpk_j_num.append(hm_fba_data[0][i][2])
            hm_dpk_time.append(hm_fba_data[0][i][3])

    for i in range(len(hm_s_fba)):
        if (hm_fba_data[0][i][0] == 'DLD'):
            hm_dld_b_num.append(1)
            hm_dld_j_num.append(hm_fba_data[0][i][2])
            hm_dld_time.append(hm_fba_data[0][i][3])
    for i in range(len(hm_s_fba)):
        if (hm_fba_data[0][i][0] == 'DJH'):
            hm_djh_b_num.append(1)
            hm_djh_j_num.append(hm_fba_data[0][i][2])
            hm_djh_time.append(hm_fba_data[0][i][3])
    for i in range(len(hm_s_fba)):
        if (hm_fba_data[0][i][0] == 'DDB'):
            hm_ddb_b_num.append(1)
            hm_ddb_j_num.append(hm_fba_data[0][i][2])
            hm_ddb_time.append(hm_fba_data[0][i][3])
    for i in range(len(hm_s_fba)):
        if (hm_fba_data[0][i][0] == 'DCK'):
            hm_dck_b_num.append(1)
            hm_dck_j_num.append(hm_fba_data[0][i][2])
            hm_dck_time.append(hm_fba_data[0][i][3])
    for i in range(len(tx_s_fba)):
        if (tx_fba_data[0][i][0] == 'DJY'):
            tx_djy_b_num.append(1)
            tx_djy_j_num.append(tx_fba_data[0][i][2])
            tx_djy_time.append(tx_fba_data[0][i][3])
    for i in range(len(tx_s_fba)):
        if (tx_fba_data[0][i][0] == 'DFPLD'):
            tx_dfpld_b_num.append(1)
            tx_dfpld_j_num.append(tx_fba_data[0][i][2])
            tx_dfpld_time.append(tx_fba_data[0][i][3])
    for i in range(len(tx_s_fba)):
        if (tx_fba_data[0][i][0] == 'DPK'):
            tx_dpk_b_num.append(1)
            tx_dpk_j_num.append(tx_fba_data[0][i][2])
            tx_dpk_time.append(tx_fba_data[0][i][3])
    for i in range(len(tx_s_fba)):
        if (tx_fba_data[0][i][0] == 'DLD'):
            tx_dld_b_num.append(1)
            tx_dld_j_num.append(tx_fba_data[0][i][2])
            tx_dld_time.append(tx_fba_data[0][i][3])
    for i in range(len(tx_s_fba)):
        if (tx_fba_data[0][i][0] == 'DJH'):
            tx_djh_b_num.append(1)
            tx_djh_j_num.append(tx_fba_data[0][i][2])
            tx_djh_time.append(tx_fba_data[0][i][3])
    for i in range(len(tx_s_fba)):
        if (tx_fba_data[0][i][0] == 'DDB'):
            tx_ddb_b_num.append(1)
            tx_ddb_j_num.append(tx_fba_data[0][i][2])
            tx_ddb_time.append(tx_fba_data[0][i][3])
    for i in range(len(tx_s_fba)):
        if (tx_fba_data[0][i][0] == 'DCK'):
            tx_dck_b_num.append(1)
            tx_dck_j_num.append(tx_fba_data[0][i][2])
            tx_dck_time.append(tx_fba_data[0][i][3])


    hm_djy = np.dstack((hm_djy_b_num, hm_djy_j_num, hm_djy_time))
    hm_dfpld = np.dstack((hm_dfpld_b_num, hm_dfpld_j_num, hm_dfpld_time))
    hm_dpk = np.dstack((hm_dpk_b_num, hm_dpk_j_num, hm_dpk_time))
    hm_dld = np.dstack((hm_dld_b_num, hm_dld_j_num, hm_dld_time))
    hm_djh = np.dstack((hm_djh_b_num, hm_djh_j_num, hm_djh_time))
    hm_ddb = np.dstack((hm_ddb_b_num, hm_ddb_j_num, hm_ddb_time))
    hm_dck = np.dstack((hm_dck_b_num, hm_dck_j_num, hm_dck_time))
    tx_djy = np.dstack((tx_djy_b_num, tx_djy_j_num, tx_djy_time))
    tx_dfpld = np.dstack((tx_dfpld_b_num, tx_dfpld_j_num, tx_dfpld_time))
    tx_dpk = np.dstack((tx_dpk_b_num, tx_dpk_j_num, tx_dpk_time))
    tx_dld = np.dstack((tx_dld_b_num, tx_dld_j_num, tx_dld_time))
    tx_djh = np.dstack((tx_djh_b_num, tx_djh_j_num, tx_djh_time))
    tx_ddb = np.dstack((tx_ddb_b_num, tx_ddb_j_num, tx_ddb_time))
    tx_dck = np.dstack((tx_dck_b_num, tx_dck_j_num, tx_dck_time))

    hm_djy_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_djy_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_dfpld_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_dfpld_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_djy_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_djy_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_dfpld_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_dfpld_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_dpk_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_dld_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_djh_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_ddb_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_dck_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_dpk_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_dld_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_djh_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_ddb_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_dck_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_dpk_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_dld_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_djh_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_ddb_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_dck_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_dpk_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_dld_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_djh_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_ddb_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_dck_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]

    hm_b_12 = []
    hm_b_24 = []
    hm_b_48 = []
    hm_b_72 = []
    hm_b_120 = []
    hm_b_240 = []
    hm_b_360 = []
    hm_b_361 = []
    tx_b_12 = []
    tx_b_24 = []
    tx_b_48 = []
    tx_b_72 = []
    tx_b_120 = []
    tx_b_240 = []
    tx_b_360 = []
    tx_b_361 = []

    hm_j_12 = []
    hm_j_24 = []
    hm_j_48 = []
    hm_j_72 = []
    hm_j_120 = []
    hm_j_240 = []
    hm_j_360 = []
    hm_j_361 = []

    tx_j_12 = []
    tx_j_24 = []
    tx_j_48 = []
    tx_j_72 = []
    tx_j_120 = []
    tx_j_240 = []
    tx_j_360 = []
    tx_j_361 = []

    for i in range(len(hm_djy[0])):
        if float(hm_djy[0][i][2]) > 0 and float(hm_djy[0][i][2]) <= 12:
            hm_djy_b_num1[0] = hm_djy_b_num1[0] + 1
            hm_djy_j_num1[0] = hm_djy_j_num1[0] + float(hm_djy[0][i][1])
        if float(hm_djy[0][i][2]) > 12 and float(hm_djy[0][i][2]) <= 24:
            hm_djy_b_num1[1] = hm_djy_b_num1[1] + 1
            hm_djy_j_num1[1] = hm_djy_j_num1[1] + float(hm_djy[0][i][1])
        if float(hm_djy[0][i][2]) > 24 and float(hm_djy[0][i][2]) <= 48:
            hm_djy_b_num1[2] = hm_djy_b_num1[2] + 1
            hm_djy_j_num1[2] = hm_djy_j_num1[2] + float(hm_djy[0][i][1])
        if float(hm_djy[0][i][2]) > 48 and float(hm_djy[0][i][2]) <= 72:
            hm_djy_b_num1[3] = hm_djy_b_num1[3] + 1
            hm_djy_j_num1[3] = hm_djy_j_num1[3] + float(hm_djy[0][i][1])
        if float(hm_djy[0][i][2]) > 72 and float(hm_djy[0][i][2]) <= 120:
            hm_djy_b_num1[4] = hm_djy_b_num1[4] + 1
            hm_djy_j_num1[4] = hm_djy_j_num1[4] + float(hm_djy[0][i][1])
        if float(hm_djy[0][i][2]) > 120 and float(hm_djy[0][i][2]) <= 240:
            hm_djy_b_num1[5] = hm_djy_b_num1[5] + 1
            hm_djy_j_num1[5] = hm_djy_j_num1[5] + float(hm_djy[0][i][1])
        if float(hm_djy[0][i][2]) > 240 and float(hm_djy[0][i][2]) <= 360:
            hm_djy_b_num1[6] = hm_djy_b_num1[6] + 1
            hm_djy_j_num1[6] = hm_djy_j_num1[6] + float(hm_djy[0][i][1])
        if float(hm_djy[0][i][2]) > 360:
            hm_djy_b_num1[7] = hm_djy_b_num1[7] + 1
            hm_djy_j_num1[7] = hm_djy_j_num1[7] + float(hm_djy[0][i][1])

    for i in range(len(hm_dfpld[0])):
        if float(hm_dfpld[0][i][2]) > 0 and float(hm_dfpld[0][i][2]) <= 12:
            hm_dfpld_b_num1[0] = hm_dfpld_b_num1[0] + 1
            hm_dfpld_j_num1[0] = hm_dfpld_j_num1[0] + float(hm_dfpld[0][i][1])
        if float(hm_dfpld[0][i][2]) > 12 and float(hm_dfpld[0][i][2]) <= 24:
            hm_dfpld_b_num1[1] = hm_dfpld_b_num1[1] + 1
            hm_dfpld_j_num1[1] = hm_dfpld_j_num1[1] + float(hm_dfpld[0][i][1])
        if float(hm_dfpld[0][i][2]) > 24 and float(hm_dfpld[0][i][2]) <= 48:
            hm_dfpld_b_num1[2] = hm_dfpld_b_num1[2] + 1
            hm_dfpld_j_num1[2] = hm_dfpld_j_num1[2] + float(hm_dfpld[0][i][1])
        if float(hm_dfpld[0][i][2]) > 48 and float(hm_dfpld[0][i][2]) <= 72:
            hm_dfpld_b_num1[3] = hm_dfpld_b_num1[3] + 1
            hm_dfpld_j_num1[3] = hm_dfpld_j_num1[3] + float(hm_dfpld[0][i][1])
        if float(hm_dfpld[0][i][2]) > 72 and float(hm_dfpld[0][i][2]) <= 120:
            hm_dfpld_b_num1[4] = hm_dfpld_b_num1[4] + 1
            hm_dfpld_j_num1[4] = hm_dfpld_j_num1[4] + float(hm_dfpld[0][i][1])
        if float(hm_dfpld[0][i][2]) > 120 and float(hm_dfpld[0][i][2]) <= 240:
            hm_dfpld_b_num1[5] = hm_dfpld_b_num1[5] + 1
            hm_dfpld_j_num1[5] = hm_dfpld_j_num1[5] + float(hm_dfpld[0][i][1])
        if float(hm_dfpld[0][i][2]) > 240 and float(hm_dfpld[0][i][2]) <= 360:
            hm_dfpld_b_num1[6] = hm_dfpld_b_num1[6] + 1
            hm_dfpld_j_num1[6] = hm_dfpld_j_num1[6] + float(hm_dfpld[0][i][1])
        if float(hm_dfpld[0][i][2]) > 360:
            hm_dfpld_b_num1[7] = hm_dfpld_b_num1[7] + 1
            hm_dfpld_j_num1[7] = hm_dfpld_j_num1[7] + float(hm_dfpld[0][i][1])
    for i in range(len(hm_dpk[0])):
        if float(hm_dpk[0][i][2]) > 0 and float(hm_dpk[0][i][2]) <= 12:
            hm_dpk_b_num1[0] = hm_dpk_b_num1[0] + 1
            hm_dpk_j_num1[0] = hm_dpk_j_num1[0] + float(hm_dpk[0][i][1])
        if float(hm_dpk[0][i][2]) > 12 and float(hm_dpk[0][i][2]) <= 24:
            hm_dpk_b_num1[1] = hm_dpk_b_num1[1] + 1
            hm_dpk_j_num1[1] = hm_dpk_j_num1[1] + float(hm_dpk[0][i][1])
        if float(hm_dpk[0][i][2]) > 24 and float(hm_dpk[0][i][2]) <= 48:
            hm_dpk_b_num1[2] = hm_dpk_b_num1[2] + 1
            hm_dpk_j_num1[2] = hm_dpk_j_num1[2] + float(hm_dpk[0][i][1])
        if float(hm_dpk[0][i][2]) > 48 and float(hm_dpk[0][i][2]) <= 72:
            hm_dpk_b_num1[3] = hm_dpk_b_num1[3] + 1
            hm_dpk_j_num1[3] = hm_dpk_j_num1[3] + float(hm_dpk[0][i][1])
        if float(hm_dpk[0][i][2]) > 72 and float(hm_dpk[0][i][2]) <= 120:
            hm_dpk_b_num1[4] = hm_dpk_b_num1[4] + 1
            hm_dpk_j_num1[4] = hm_dpk_j_num1[4] + float(hm_dpk[0][i][1])
        if float(hm_dpk[0][i][2]) > 120 and float(hm_dpk[0][i][2]) <= 240:
            hm_dpk_b_num1[5] = hm_dpk_b_num1[5] + 1
            hm_dpk_j_num1[5] = hm_dpk_j_num1[5] + float(hm_dpk[0][i][1])
        if float(hm_dpk[0][i][2]) > 240 and float(hm_dpk[0][i][2]) <= 360:
            hm_dpk_b_num1[6] = hm_dpk_b_num1[6] + 1
            hm_dpk_j_num1[6] = hm_dpk_j_num1[6] + float(hm_dpk[0][i][1])
        if float(hm_dpk[0][i][2]) > 360:
            hm_dpk_b_num1[7] = hm_dpk_b_num1[7] + 1
            hm_dpk_j_num1[7] = hm_dpk_j_num1[7] + float(hm_dpk[0][i][1])
    for i in range(len(hm_dld[0])):
        if float(hm_dld[0][i][2]) > 0 and float(hm_dld[0][i][2]) <= 12:
            hm_dld_b_num1[0] = hm_dld_b_num1[0] + 1
            hm_dld_j_num1[0] = hm_dld_j_num1[0] + float(hm_dld[0][i][1])
        if float(hm_dld[0][i][2]) > 12 and float(hm_dld[0][i][2]) <= 24:
            hm_dld_b_num1[1] = hm_dld_b_num1[1] + 1
            hm_dld_j_num1[1] = hm_dld_j_num1[1] + float(hm_dld[0][i][1])
        if float(hm_dld[0][i][2]) > 24 and float(hm_dld[0][i][2]) <= 48:
            hm_dld_b_num1[2] = hm_dld_b_num1[2] + 1
            hm_dld_j_num1[2] = hm_dld_j_num1[2] + float(hm_dld[0][i][1])
        if float(hm_dld[0][i][2]) > 48 and float(hm_dld[0][i][2]) <= 72:
            hm_dld_b_num1[3] = hm_dld_b_num1[3] + 1
            hm_dld_j_num1[3] = hm_dld_j_num1[3] + float(hm_dld[0][i][1])
        if float(hm_dld[0][i][2]) > 72 and float(hm_dld[0][i][2]) <= 120:
            hm_dld_b_num1[4] = hm_dld_b_num1[4] + 1
            hm_dld_j_num1[4] = hm_dld_j_num1[4] + float(hm_dld[0][i][1])
        if float(hm_dld[0][i][2]) > 120 and float(hm_dld[0][i][2]) <= 240:
            hm_dld_b_num1[5] = hm_dld_b_num1[5] + 1
            hm_dld_j_num1[5] = hm_dld_j_num1[5] + float(hm_dld[0][i][1])
        if float(hm_dld[0][i][2]) > 240 and float(hm_dld[0][i][2]) <= 360:
            hm_dld_b_num1[6] = hm_dld_b_num1[6] + 1
            hm_dld_j_num1[6] = hm_dld_j_num1[6] + float(hm_dld[0][i][1])
        if float(hm_dld[0][i][2]) > 360:
            hm_dld_b_num1[7] = hm_dld_b_num1[7] + 1
            hm_dld_j_num1[7] = hm_dld_j_num1[7] + float(hm_dld[0][i][1])

    for i in range(len(hm_djh[0])):
        if float(hm_djh[0][i][2]) > 0 and float(hm_djh[0][i][2]) <= 12:
            hm_djh_b_num1[0] = hm_djh_b_num1[0] + 1
            hm_djh_j_num1[0] = hm_djh_j_num1[0] + float(hm_djh[0][i][1])
        if float(hm_djh[0][i][2]) > 12 and float(hm_djh[0][i][2]) <= 24:
            hm_djh_b_num1[1] = hm_djh_b_num1[1] + 1
            hm_djh_j_num1[1] = hm_djh_j_num1[1] + float(hm_djh[0][i][1])
        if float(hm_djh[0][i][2]) > 24 and float(hm_djh[0][i][2]) <= 48:
            hm_djh_b_num1[2] = hm_djh_b_num1[2] + 1
            hm_djh_j_num1[2] = hm_djh_j_num1[2] + float(hm_djh[0][i][1])
        if float(hm_djh[0][i][2]) > 48 and float(hm_djh[0][i][2]) <= 72:
            hm_djh_b_num1[3] = hm_djh_b_num1[3] + 1
            hm_djh_j_num1[3] = hm_djh_j_num1[3] + float(hm_djh[0][i][1])
        if float(hm_djh[0][i][2]) > 72 and float(hm_djh[0][i][2]) <= 120:
            hm_djh_b_num1[4] = hm_djh_b_num1[4] + 1
            hm_djh_j_num1[4] = hm_djh_j_num1[4] + float(hm_djh[0][i][1])
        if float(hm_djh[0][i][2]) > 120 and float(hm_djh[0][i][2]) <= 240:
            hm_djh_b_num1[5] = hm_djh_b_num1[5] + 1
            hm_djh_j_num1[5] = hm_djh_j_num1[5] + float(hm_djh[0][i][1])
        if float(hm_djh[0][i][2]) > 240 and float(hm_djh[0][i][2]) <= 360:
            hm_djh_b_num1[6] = hm_djh_b_num1[6] + 1
            hm_djh_j_num1[6] = hm_djh_j_num1[6] + float(hm_djh[0][i][1])
        if float(hm_djh[0][i][2]) > 360:
            hm_djh_b_num1[7] = hm_djh_b_num1[7] + 1
            hm_djh_j_num1[7] = hm_djh_j_num1[7] + float(hm_djh[0][i][1])

    for i in range(len(hm_ddb[0])):
        if float(hm_ddb[0][i][2]) > 0 and float(hm_ddb[0][i][2]) <= 12:
            hm_ddb_b_num1[0] = hm_ddb_b_num1[0] + 1
            hm_ddb_j_num1[0] = hm_ddb_j_num1[0] + float(hm_ddb[0][i][1])
        if float(hm_ddb[0][i][2]) > 12 and float(hm_ddb[0][i][2]) <= 24:
            hm_ddb_b_num1[1] = hm_ddb_b_num1[1] + 1
            hm_ddb_j_num1[1] = hm_ddb_j_num1[1] + float(hm_ddb[0][i][1])
        if float(hm_ddb[0][i][2]) > 24 and float(hm_ddb[0][i][2]) <= 48:
            hm_ddb_b_num1[2] = hm_ddb_b_num1[2] + 1
            hm_ddb_j_num1[2] = hm_ddb_j_num1[2] + float(hm_ddb[0][i][1])
        if float(hm_ddb[0][i][2]) > 48 and float(hm_ddb[0][i][2]) <= 72:
            hm_ddb_b_num1[3] = hm_ddb_b_num1[3] + 1
            hm_ddb_j_num1[3] = hm_ddb_j_num1[3] + float(hm_ddb[0][i][1])
        if float(hm_ddb[0][i][2]) > 72 and float(hm_ddb[0][i][2]) <= 120:
            hm_ddb_b_num1[4] = hm_ddb_b_num1[4] + 1
            hm_ddb_j_num1[4] = hm_ddb_j_num1[4] + float(hm_ddb[0][i][1])
        if float(hm_ddb[0][i][2]) > 120 and float(hm_ddb[0][i][2]) <= 240:
            hm_ddb_b_num1[5] = hm_ddb_b_num1[5] + 1
            hm_ddb_j_num1[5] = hm_ddb_j_num1[5] + float(hm_ddb[0][i][1])
        if float(hm_ddb[0][i][2]) > 240 and float(hm_ddb[0][i][2]) <= 360:
            hm_ddb_b_num1[6] = hm_ddb_b_num1[6] + 1
            hm_ddb_j_num1[6] = hm_ddb_j_num1[6] + float(hm_ddb[0][i][1])
        if float(hm_ddb[0][i][2]) > 360:
            hm_ddb_b_num1[7] = hm_ddb_b_num1[7] + 1
            hm_ddb_j_num1[7] = hm_ddb_j_num1[7] + float(hm_ddb[0][i][1])

    for i in range(len(hm_dck[0])):
        if float(hm_dck[0][i][2]) > 0 and float(hm_dck[0][i][2]) <= 12:
            hm_dck_b_num1[0] = hm_dck_b_num1[0] + 1
            hm_dck_j_num1[0] = hm_dck_j_num1[0] + float(hm_dck[0][i][1])
        if float(hm_dck[0][i][2]) > 12 and float(hm_dck[0][i][2]) <= 24:
            hm_dck_b_num1[1] = hm_dck_b_num1[1] + 1
            hm_dck_j_num1[1] = hm_dck_j_num1[1] + float(hm_dck[0][i][1])
        if float(hm_dck[0][i][2]) > 24 and float(hm_dck[0][i][2]) <= 48:
            hm_dck_b_num1[2] = hm_dck_b_num1[2] + 1
            hm_dck_j_num1[2] = hm_dck_j_num1[2] + float(hm_dck[0][i][1])
        if float(hm_dck[0][i][2]) > 48 and float(hm_dck[0][i][2]) <= 72:
            hm_dck_b_num1[3] = hm_dck_b_num1[3] + 1
            hm_dck_j_num1[3] = hm_dck_j_num1[3] + float(hm_dck[0][i][1])
        if float(hm_dck[0][i][2]) > 72 and float(hm_dck[0][i][2]) <= 120:
            hm_dck_b_num1[4] = hm_dck_b_num1[4] + 1
            hm_dck_j_num1[4] = hm_dck_j_num1[4] + float(hm_dck[0][i][1])
        if float(hm_dck[0][i][2]) > 120 and float(hm_dck[0][i][2]) <= 240:
            hm_dck_b_num1[5] = hm_dck_b_num1[5] + 1
            hm_dck_j_num1[5] = hm_dck_j_num1[5] + float(hm_dck[0][i][1])
        if float(hm_dck[0][i][2]) > 240 and float(hm_dck[0][i][2]) <= 360:
            hm_dck_b_num1[6] = hm_dck_b_num1[6] + 1
            hm_dck_j_num1[6] = hm_dck_j_num1[6] + float(hm_dck[0][i][1])
        if float(hm_dck[0][i][2]) > 360:
            hm_dck_b_num1[7] = hm_dck_b_num1[7] + 1
            hm_dck_j_num1[7] = hm_dck_j_num1[7] + float(hm_dck[0][i][1])

    for i in range(len(tx_djy[0])):
        if float(tx_djy[0][i][2]) > 0 and float(tx_djy[0][i][2]) <= 12:
            tx_djy_b_num1[0] = tx_djy_b_num1[0] + 1
            tx_djy_j_num1[0] = tx_djy_j_num1[0] + float(tx_djy[0][i][1])
        if float(tx_djy[0][i][2]) > 12 and float(tx_djy[0][i][2]) <= 24:
            tx_djy_b_num1[1] = tx_djy_b_num1[1] + 1
            tx_djy_j_num1[1] = tx_djy_j_num1[1] + float(tx_djy[0][i][1])
        if float(tx_djy[0][i][2]) > 24 and float(tx_djy[0][i][2]) <= 48:
            tx_djy_b_num1[2] = tx_djy_b_num1[2] + 1
            tx_djy_j_num1[2] = tx_djy_j_num1[2] + float(tx_djy[0][i][1])
        if float(tx_djy[0][i][2]) > 48 and float(tx_djy[0][i][2]) <= 72:
            tx_djy_b_num1[3] = tx_djy_b_num1[3] + 1
            tx_djy_j_num1[3] = tx_djy_j_num1[3] + float(tx_djy[0][i][1])
        if float(tx_djy[0][i][2]) > 72 and float(tx_djy[0][i][2]) <= 120:
            tx_djy_b_num1[4] = tx_djy_b_num1[4] + 1
            tx_djy_j_num1[4] = tx_djy_j_num1[4] + float(tx_djy[0][i][1])
        if float(tx_djy[0][i][2]) > 120 and float(tx_djy[0][i][2]) <= 240:
            tx_djy_b_num1[5] = tx_djy_b_num1[5] + 1
            tx_djy_j_num1[5] = tx_djy_j_num1[5] + float(tx_djy[0][i][1])
        if float(tx_djy[0][i][2]) > 240 and float(tx_djy[0][i][2]) <= 360:
            tx_djy_b_num1[6] = tx_djy_b_num1[6] + 1
            tx_djy_j_num1[6] = tx_djy_j_num1[6] + float(tx_djy[0][i][1])
        if float(tx_djy[0][i][2]) > 360:
            tx_djy_b_num1[7] = tx_djy_b_num1[7] + 1
            tx_djy_j_num1[7] = tx_djy_j_num1[7] + float(tx_djy[0][i][1])
    for i in range(len(tx_dfpld[0])):
        if float(tx_dfpld[0][i][2]) > 0 and float(tx_dfpld[0][i][2]) <= 12:
            tx_dfpld_b_num1[0] = tx_dfpld_b_num1[0] + 1
            tx_dfpld_j_num1[0] = tx_dfpld_j_num1[0] + float(tx_dfpld[0][i][1])
        if float(tx_dfpld[0][i][2]) > 12 and float(tx_dfpld[0][i][2]) <= 24:
            tx_dfpld_b_num1[1] = tx_dfpld_b_num1[1] + 1
            tx_dfpld_j_num1[1] = tx_dfpld_j_num1[1] + float(tx_dfpld[0][i][1])
        if float(tx_dfpld[0][i][2]) > 24 and float(tx_dfpld[0][i][2]) <= 48:
            tx_dfpld_b_num1[2] = tx_dfpld_b_num1[2] + 1
            tx_dfpld_j_num1[2] = tx_dfpld_j_num1[2] + float(tx_dfpld[0][i][1])
        if float(tx_dfpld[0][i][2]) > 48 and float(tx_dfpld[0][i][2]) <= 72:
            tx_dfpld_b_num1[3] = tx_dfpld_b_num1[3] + 1
            tx_dfpld_j_num1[3] = tx_dfpld_j_num1[3] + float(tx_dfpld[0][i][1])
        if float(tx_dfpld[0][i][2]) > 72 and float(tx_dfpld[0][i][2]) <= 120:
            tx_dfpld_b_num1[4] = tx_dfpld_b_num1[4] + 1
            tx_dfpld_j_num1[4] = tx_dfpld_j_num1[4] + float(tx_dfpld[0][i][1])
        if float(tx_dfpld[0][i][2]) > 120 and float(tx_dfpld[0][i][2]) <= 240:
            tx_dfpld_b_num1[5] = tx_dfpld_b_num1[5] + 1
            tx_dfpld_j_num1[5] = tx_dfpld_j_num1[5] + float(tx_dfpld[0][i][1])
        if float(tx_dfpld[0][i][2]) > 240 and float(tx_dfpld[0][i][2]) <= 360:
            tx_dfpld_b_num1[6] = tx_dfpld_b_num1[6] + 1
            tx_dfpld_j_num1[6] = tx_dfpld_j_num1[6] + float(tx_dfpld[0][i][1])
        if float(tx_dfpld[0][i][2]) > 360:
            tx_dfpld_b_num1[7] = tx_dfpld_b_num1[7] + 1
            tx_dfpld_j_num1[7] = tx_dfpld_j_num1[7] + float(tx_dfpld[0][i][1])
    for i in range(len(tx_dpk[0])):
        if float(tx_dpk[0][i][2]) > 0 and float(tx_dpk[0][i][2]) <= 12:
            tx_dpk_b_num1[0] = tx_dpk_b_num1[0] + 1
            tx_dpk_j_num1[0] = tx_dpk_j_num1[0] + float(tx_dpk[0][i][1])
        if float(tx_dpk[0][i][2]) > 12 and float(tx_dpk[0][i][2]) <= 24:
            tx_dpk_b_num1[1] = tx_dpk_b_num1[1] + 1
            tx_dpk_j_num1[1] = tx_dpk_j_num1[1] + float(tx_dpk[0][i][1])
        if float(tx_dpk[0][i][2]) > 24 and float(tx_dpk[0][i][2]) <= 48:
            tx_dpk_b_num1[2] = tx_dpk_b_num1[2] + 1
            tx_dpk_j_num1[2] = tx_dpk_j_num1[2] + float(tx_dpk[0][i][1])
        if float(tx_dpk[0][i][2]) > 48 and float(tx_dpk[0][i][2]) <= 72:
            tx_dpk_b_num1[3] = tx_dpk_b_num1[3] + 1
            tx_dpk_j_num1[3] = tx_dpk_j_num1[3] + float(tx_dpk[0][i][1])
        if float(tx_dpk[0][i][2]) > 72 and float(tx_dpk[0][i][2]) <= 120:
            tx_dpk_b_num1[4] = tx_dpk_b_num1[4] + 1
            tx_dpk_j_num1[4] = tx_dpk_j_num1[4] + float(tx_dpk[0][i][1])
        if float(tx_dpk[0][i][2]) > 120 and float(tx_dpk[0][i][2]) <= 240:
            tx_dpk_b_num1[5] = tx_dpk_b_num1[5] + 1
            tx_dpk_j_num1[5] = tx_dpk_j_num1[5] + float(tx_dpk[0][i][1])
        if float(tx_dpk[0][i][2]) > 240 and float(tx_dpk[0][i][2]) <= 360:
            tx_dpk_b_num1[6] = tx_dpk_b_num1[6] + 1
            tx_dpk_j_num1[6] = tx_dpk_j_num1[6] + float(tx_dpk[0][i][1])
        if float(tx_dpk[0][i][2]) > 360:
            tx_dpk_b_num1[7] = tx_dpk_b_num1[7] + 1
            tx_dpk_j_num1[7] = tx_dpk_j_num1[7] + float(tx_dpk[0][i][1])

    for i in range(len(tx_dld[0])):
        if float(tx_dld[0][i][2]) > 0 and float(tx_dld[0][i][2]) <= 12:
            tx_dld_b_num1[0] = tx_dld_b_num1[0] + 1
            tx_dld_j_num1[0] = tx_dld_j_num1[0] + float(tx_dld[0][i][1])
        if float(tx_dld[0][i][2]) > 12 and float(tx_dld[0][i][2]) <= 24:
            tx_dld_b_num1[1] = tx_dld_b_num1[1] + 1
            tx_dld_j_num1[1] = tx_dld_j_num1[1] + float(tx_dld[0][i][1])
        if float(tx_dld[0][i][2]) > 24 and float(tx_dld[0][i][2]) <= 48:
            tx_dld_b_num1[2] = tx_dld_b_num1[2] + 1
            tx_dld_j_num1[2] = tx_dld_j_num1[2] + float(tx_dld[0][i][1])
        if float(tx_dld[0][i][2]) > 48 and float(tx_dld[0][i][2]) <= 72:
            tx_dld_b_num1[3] = tx_dld_b_num1[3] + 1
            tx_dld_j_num1[3] = tx_dld_j_num1[3] + float(tx_dld[0][i][1])
        if float(tx_dld[0][i][2]) > 72 and float(tx_dld[0][i][2]) <= 120:
            tx_dld_b_num1[4] = tx_dld_b_num1[4] + 1
            tx_dld_j_num1[4] = tx_dld_j_num1[4] + float(tx_dld[0][i][1])
        if float(tx_dld[0][i][2]) > 120 and float(tx_dld[0][i][2]) <= 240:
            tx_dld_b_num1[5] = tx_dld_b_num1[5] + 1
            tx_dld_j_num1[5] = tx_dld_j_num1[5] + float(tx_dld[0][i][1])
        if float(tx_dld[0][i][2]) > 240 and float(tx_dld[0][i][2]) <= 360:
            tx_dld_b_num1[6] = tx_dld_b_num1[6] + 1
            tx_dld_j_num1[6] = tx_dld_j_num1[6] + float(tx_dld[0][i][1])
        if float(tx_dld[0][i][2]) > 360:
            tx_dld_b_num1[7] = tx_dld_b_num1[7] + 1
            tx_dld_j_num1[7] = tx_dld_j_num1[7] + float(tx_dld[0][i][1])

    for i in range(len(tx_djh[0])):
        if float(tx_djh[0][i][2]) > 0 and float(tx_djh[0][i][2]) <= 12:
            tx_djh_b_num1[0] = tx_djh_b_num1[0] + 1
            tx_djh_j_num1[0] = tx_djh_j_num1[0] + float(tx_djh[0][i][1])
        if float(tx_djh[0][i][2]) > 12 and float(tx_djh[0][i][2]) <= 24:
            tx_djh_b_num1[1] = tx_djh_b_num1[1] + 1
            tx_djh_j_num1[1] = tx_djh_j_num1[1] + float(tx_djh[0][i][1])
        if float(tx_djh[0][i][2]) > 24 and float(tx_djh[0][i][2]) <= 48:
            tx_djh_b_num1[2] = tx_djh_b_num1[2] + 1
            tx_djh_j_num1[2] = tx_djh_j_num1[2] + float(tx_djh[0][i][1])
        if float(tx_djh[0][i][2]) > 48 and float(tx_djh[0][i][2]) <= 72:
            tx_djh_b_num1[3] = tx_djh_b_num1[3] + 1
            tx_djh_j_num1[3] = tx_djh_j_num1[3] + float(tx_djh[0][i][1])
        if float(tx_djh[0][i][2]) > 72 and float(tx_djh[0][i][2]) <= 120:
            tx_djh_b_num1[4] = tx_djh_b_num1[4] + 1
            tx_djh_j_num1[4] = tx_djh_j_num1[4] + float(tx_djh[0][i][1])
        if float(tx_djh[0][i][2]) > 120 and float(tx_djh[0][i][2]) <= 240:
            tx_djh_b_num1[5] = tx_djh_b_num1[5] + 1
            tx_djh_j_num1[5] = tx_djh_j_num1[5] + float(tx_djh[0][i][1])
        if float(tx_djh[0][i][2]) > 240 and float(tx_djh[0][i][2]) <= 360:
            tx_djh_b_num1[6] = tx_djh_b_num1[6] + 1
            tx_djh_j_num1[6] = tx_djh_j_num1[6] + float(tx_djh[0][i][1])
        if float(tx_djh[0][i][2]) > 360:
            tx_djh_b_num1[7] = tx_djh_b_num1[7] + 1
            tx_djh_j_num1[7] = tx_djh_j_num1[7] + float(tx_djh[0][i][1])

    for i in range(len(tx_ddb[0])):
        if float(tx_ddb[0][i][2]) > 0 and float(tx_ddb[0][i][2]) <= 12:
            tx_ddb_b_num1[0] = tx_ddb_b_num1[0] + 1
            tx_ddb_j_num1[0] = tx_ddb_j_num1[0] + float(tx_ddb[0][i][1])
        if float(tx_ddb[0][i][2]) > 12 and float(tx_ddb[0][i][2]) <= 24:
            tx_ddb_b_num1[1] = tx_ddb_b_num1[1] + 1
            tx_ddb_j_num1[1] = tx_ddb_j_num1[1] + float(tx_ddb[0][i][1])
        if float(tx_ddb[0][i][2]) > 24 and float(tx_ddb[0][i][2]) <= 48:
            tx_ddb_b_num1[2] = tx_ddb_b_num1[2] + 1
            tx_ddb_j_num1[2] = tx_ddb_j_num1[2] + float(tx_ddb[0][i][1])
        if float(tx_ddb[0][i][2]) > 48 and float(tx_ddb[0][i][2]) <= 72:
            tx_ddb_b_num1[3] = tx_ddb_b_num1[3] + 1
            tx_ddb_j_num1[3] = tx_ddb_j_num1[3] + float(tx_ddb[0][i][1])
        if float(tx_ddb[0][i][2]) > 72 and float(tx_ddb[0][i][2]) <= 120:
            tx_ddb_b_num1[4] = tx_ddb_b_num1[4] + 1
            tx_ddb_j_num1[4] = tx_ddb_j_num1[4] + float(tx_ddb[0][i][1])
        if float(tx_ddb[0][i][2]) > 120 and float(tx_ddb[0][i][2]) <= 240:
            tx_ddb_b_num1[5] = tx_ddb_b_num1[5] + 1
            tx_ddb_j_num1[5] = tx_ddb_j_num1[5] + float(tx_ddb[0][i][1])
        if float(tx_ddb[0][i][2]) > 240 and float(tx_ddb[0][i][2]) <= 360:
            tx_ddb_b_num1[6] = tx_ddb_b_num1[6] + 1
            tx_ddb_j_num1[6] = tx_ddb_j_num1[6] + float(tx_ddb[0][i][1])
        if float(tx_ddb[0][i][2]) > 360:
            tx_ddb_b_num1[7] = tx_ddb_b_num1[7] + 1
            tx_ddb_j_num1[7] = tx_ddb_j_num1[7] + float(tx_ddb[0][i][1])

    for i in range(len(tx_dck[0])):
        if float(tx_dck[0][i][2]) > 0 and float(tx_dck[0][i][2]) <= 12:
            tx_dck_b_num1[0] = tx_dck_b_num1[0] + 1
            tx_dck_j_num1[0] = tx_dck_j_num1[0] + float(tx_dck[0][i][1])
        if float(tx_dck[0][i][2]) > 12 and float(tx_dck[0][i][2]) <= 24:
            tx_dck_b_num1[1] = tx_dck_b_num1[1] + 1
            tx_dck_j_num1[1] = tx_dck_j_num1[1] + float(tx_dck[0][i][1])
        if float(tx_dck[0][i][2]) > 24 and float(tx_dck[0][i][2]) <= 48:
            tx_dck_b_num1[2] = tx_dck_b_num1[2] + 1
            tx_dck_j_num1[2] = tx_dck_j_num1[2] + float(tx_dck[0][i][1])
        if float(tx_dck[0][i][2]) > 48 and float(tx_dck[0][i][2]) <= 72:
            tx_dck_b_num1[3] = tx_dck_b_num1[3] + 1
            tx_dck_j_num1[3] = tx_dck_j_num1[3] + float(tx_dck[0][i][1])
        if float(tx_dck[0][i][2]) > 72 and float(tx_dck[0][i][2]) <= 120:
            tx_dck_b_num1[4] = tx_dck_b_num1[4] + 1
            tx_dck_j_num1[4] = tx_dck_j_num1[4] + float(tx_dck[0][i][1])
        if float(tx_dck[0][i][2]) > 120 and float(tx_dck[0][i][2]) <= 240:
            tx_dck_b_num1[5] = tx_dck_b_num1[5] + 1
            tx_dck_j_num1[5] = tx_dck_j_num1[5] + float(tx_dck[0][i][1])
        if float(tx_dck[0][i][2]) > 240 and float(tx_dck[0][i][2]) <= 360:
            tx_dck_b_num1[6] = tx_dck_b_num1[6] + 1
            tx_dck_j_num1[6] = tx_dck_j_num1[6] + float(tx_dck[0][i][1])
        if float(tx_dck[0][i][2]) > 360:
            tx_dck_b_num1[7] = tx_dck_b_num1[7] + 1
            tx_dck_j_num1[7] = tx_dck_j_num1[7] + float(tx_dck[0][i][1])

    hm_b_fba_num_12 = np.r_[
        hm_dpk_b_num1[0], hm_dfpld_b_num1[0], hm_dld_b_num1[0], hm_djh_b_num1[0], hm_ddb_b_num1[0], hm_dck_b_num1[0],
        hm_djy_b_num1[0]]

    hm_b_fba_num_24 = np.r_[
        hm_dpk_b_num1[1], hm_dfpld_b_num1[1], hm_dld_b_num1[1], hm_djh_b_num1[1], hm_ddb_b_num1[1], hm_dck_b_num1[1],
        hm_djy_b_num1[1]]
    hm_b_fba_num_48 = np.r_[
        hm_dpk_b_num1[2], hm_dfpld_b_num1[2], hm_dld_b_num1[2], hm_djh_b_num1[2], hm_ddb_b_num1[2], hm_dck_b_num1[2],
        hm_djy_b_num1[2]]
    hm_b_fba_num_72 = np.r_[
        hm_dpk_b_num1[3], hm_dfpld_b_num1[3], hm_dld_b_num1[3], hm_djh_b_num1[3], hm_ddb_b_num1[3], hm_dck_b_num1[3],
        hm_djy_b_num1[3]]
    hm_b_fba_num_120 = np.r_[
        hm_dpk_b_num1[4], hm_dfpld_b_num1[4], hm_dld_b_num1[4], hm_djh_b_num1[4], hm_ddb_b_num1[4], hm_dck_b_num1[4],
        hm_djy_b_num1[4]]
    hm_b_fba_num_240 = np.r_[
        hm_dpk_b_num1[5], hm_dfpld_b_num1[5], hm_dld_b_num1[5], hm_djh_b_num1[5], hm_ddb_b_num1[5], hm_dck_b_num1[5],
        hm_djy_b_num1[5]]
    hm_b_fba_num_360 = np.r_[
        hm_dpk_b_num1[6], hm_dfpld_b_num1[6], hm_dld_b_num1[6], hm_djh_b_num1[6], hm_ddb_b_num1[6], hm_dck_b_num1[6],
        hm_djy_b_num1[6]]
    hm_b_fba_num_361 = np.r_[
        hm_dpk_b_num1[7], hm_dfpld_b_num1[7], hm_dld_b_num1[7], hm_djh_b_num1[7], hm_ddb_b_num1[7], hm_dck_b_num1[7],
        hm_djy_b_num1[7]]
    hm_j_fba_num_12 = np.r_[
        hm_dpk_j_num1[0], hm_dfpld_j_num1[0], hm_dld_j_num1[0], hm_djh_j_num1[0], hm_ddb_j_num1[0], hm_dck_j_num1[0],
        hm_djy_j_num1[0]]

    hm_j_fba_num_24 = np.r_[
        hm_dpk_j_num1[1], hm_dfpld_j_num1[1], hm_dld_j_num1[1], hm_djh_j_num1[1], hm_ddb_j_num1[1], hm_dck_j_num1[1],
        hm_djy_j_num1[1]]
    hm_j_fba_num_48 = np.r_[
        hm_dpk_j_num1[2], hm_dfpld_j_num1[2], hm_dld_j_num1[2], hm_djh_j_num1[2], hm_ddb_j_num1[2], hm_dck_j_num1[2],
        hm_djy_j_num1[2]]
    hm_j_fba_num_72 = np.r_[
        hm_dpk_j_num1[3], hm_dfpld_j_num1[3], hm_dld_j_num1[3], hm_djh_j_num1[3], hm_ddb_j_num1[3], hm_dck_j_num1[3],
        hm_djy_j_num1[3]]
    hm_j_fba_num_120 = np.r_[
        hm_dpk_j_num1[4], hm_dfpld_j_num1[4], hm_dld_j_num1[4], hm_djh_j_num1[4], hm_ddb_j_num1[4], hm_dck_j_num1[4],
        hm_djy_j_num1[4]]
    hm_j_fba_num_240 = np.r_[
        hm_dpk_j_num1[5], hm_dfpld_j_num1[5], hm_dld_j_num1[5], hm_djh_j_num1[5], hm_ddb_j_num1[5], hm_dck_j_num1[5],
        hm_djy_j_num1[5]]
    hm_j_fba_num_360 = np.r_[
        hm_dpk_j_num1[6], hm_dfpld_j_num1[6], hm_dld_j_num1[6], hm_djh_j_num1[6], hm_ddb_j_num1[6], hm_dck_j_num1[6],
        hm_djy_j_num1[6]]
    hm_j_fba_num_361 = np.r_[
        hm_dpk_j_num1[7], hm_dfpld_j_num1[7], hm_dld_j_num1[7], hm_djh_j_num1[7], hm_ddb_j_num1[7], hm_dck_j_num1[7],
        hm_djy_j_num1[7]]

    tx_b_fba_num_12 = np.r_[
        tx_dpk_b_num1[0], tx_dfpld_b_num1[0], tx_dld_b_num1[0], tx_djh_b_num1[0], tx_ddb_b_num1[0], tx_dck_b_num1[0],
        tx_djy_b_num1[0]]

    tx_b_fba_num_24 = np.r_[
        tx_dpk_b_num1[1], tx_dfpld_b_num1[1], tx_dld_b_num1[1], tx_djh_b_num1[1], tx_ddb_b_num1[1], tx_dck_b_num1[1],
        tx_djy_b_num1[1]]
    tx_b_fba_num_48 = np.r_[
        tx_dpk_b_num1[2], tx_dfpld_b_num1[2], tx_dld_b_num1[2], tx_djh_b_num1[2], tx_ddb_b_num1[2], tx_dck_b_num1[2],
        tx_djy_b_num1[2]]
    tx_b_fba_num_72 = np.r_[
        tx_dpk_b_num1[3], tx_dfpld_b_num1[3], tx_dld_b_num1[3], tx_djh_b_num1[3], tx_ddb_b_num1[3], tx_dck_b_num1[3],
        tx_djy_b_num1[3]]
    tx_b_fba_num_120 = np.r_[
        tx_dpk_b_num1[4], tx_dfpld_b_num1[4], tx_dld_b_num1[4], tx_djh_b_num1[4], tx_ddb_b_num1[4], tx_dck_b_num1[4],
        tx_djy_b_num1[4]]
    tx_b_fba_num_240 = np.r_[
        tx_dpk_b_num1[5], tx_dfpld_b_num1[5], tx_dld_b_num1[5], tx_djh_b_num1[5], tx_ddb_b_num1[5], tx_dck_b_num1[5],
        tx_djy_b_num1[5]]
    tx_b_fba_num_360 = np.r_[
        tx_dpk_b_num1[6], tx_dfpld_b_num1[6], tx_dld_b_num1[6], tx_djh_b_num1[6], tx_ddb_b_num1[6], tx_dck_b_num1[6],
        tx_djy_b_num1[6]]
    tx_b_fba_num_361 = np.r_[
        tx_dpk_b_num1[7], tx_dfpld_b_num1[7], tx_dld_b_num1[7], tx_djh_b_num1[7], tx_ddb_b_num1[7], tx_dck_b_num1[7],
        tx_djy_b_num1[7]]
    tx_j_fba_num_12 = np.r_[
        tx_dpk_j_num1[0], tx_dfpld_j_num1[0], tx_dld_j_num1[0], tx_djh_j_num1[0], tx_ddb_j_num1[0], tx_dck_j_num1[0],
        tx_djy_j_num1[0]]

    tx_j_fba_num_24 = np.r_[
        tx_dpk_j_num1[1], tx_dfpld_j_num1[1], tx_dld_j_num1[1], tx_djh_j_num1[1], tx_ddb_j_num1[1], tx_dck_j_num1[1],
        tx_djy_j_num1[1]]
    tx_j_fba_num_48 = np.r_[
        tx_dpk_j_num1[2], tx_dfpld_j_num1[2], tx_dld_j_num1[2], tx_djh_j_num1[2], tx_ddb_j_num1[2], tx_dck_j_num1[2],
        tx_djy_j_num1[2]]
    tx_j_fba_num_72 = np.r_[
        tx_dpk_j_num1[3], tx_dfpld_j_num1[3], tx_dld_j_num1[3], tx_djh_j_num1[3], tx_ddb_j_num1[3], tx_dck_j_num1[3],
        tx_djy_j_num1[3]]
    tx_j_fba_num_120 = np.r_[
        tx_dpk_j_num1[4], tx_dfpld_j_num1[4], tx_dld_j_num1[4], tx_djh_j_num1[4], tx_ddb_j_num1[4], tx_dck_j_num1[4],
        tx_djy_j_num1[4]]
    tx_j_fba_num_240 = np.r_[
        tx_dpk_j_num1[5], tx_dfpld_j_num1[5], tx_dld_j_num1[5], tx_djh_j_num1[5], tx_ddb_j_num1[5], tx_dck_j_num1[5],
        tx_djy_j_num1[5]]
    tx_j_fba_num_360 = np.r_[
        tx_dpk_j_num1[6], tx_dfpld_j_num1[6], tx_dld_j_num1[6], tx_djh_j_num1[6], tx_ddb_j_num1[6], tx_dck_j_num1[6],
        tx_djy_j_num1[6]]
    tx_j_fba_num_361 = np.r_[
        tx_dpk_j_num1[7], tx_dfpld_j_num1[7], tx_dld_j_num1[7], tx_djh_j_num1[7], tx_ddb_j_num1[7], tx_dck_j_num1[7],
        tx_djy_j_num1[7]]

    arrayA = np.divide(hm_b_fba_num_12, max(hm_b_fba_num_12), out=np.zeros_like(hm_b_fba_num_12, dtype=np.float64),
                       where=max(hm_b_fba_num_12) != 0)
    for i in range(len(hm_b_fba_num_12)):
        hm_b_12.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_fba_num_12[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_fba_num_12)):
            hm_b_fba_num_12[i] = '{:.2%}'.format(a)

    arrayA = np.divide(hm_j_fba_num_12, max(hm_j_fba_num_12), out=np.zeros_like(hm_j_fba_num_12, dtype=np.float64),
                       where=max(hm_j_fba_num_12) != 0)
    for i in range(len(hm_j_fba_num_12)):
        hm_j_12.append("%.2f%%" % (arrayA[i] * 100))
    if hm_j_fba_num_12[0] == 'nan%':
        a = 0
        for i in range(len(hm_j_fba_num_12)):
            hm_j_fba_num_12[i] = '{:.2%}'.format(a)
    print(hm_j_12)
    arrayA = np.divide(hm_b_fba_num_24, max(hm_b_fba_num_24), out=np.zeros_like(hm_b_fba_num_24, dtype=np.float64),
                       where=max(hm_b_fba_num_24) != 0)
    for i in range(len(hm_b_fba_num_24)):
        hm_b_24.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_fba_num_24[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_fba_num_24)):
            hm_b_fba_num_24[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_j_fba_num_24, max(hm_j_fba_num_24), out=np.zeros_like(hm_j_fba_num_24, dtype=np.float64), where=max(hm_j_fba_num_24) != 0)
    for i in range(len(hm_j_fba_num_24)):
        hm_j_24.append("%.2f%%" % (arrayA[i]*100))
    if hm_j_fba_num_24[0] == 'nan%':
        a=0
        for i in range(len(hm_j_fba_num_24)):
            hm_j_fba_num_24[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_b_fba_num_48, max(hm_b_fba_num_48), out=np.zeros_like(hm_b_fba_num_48, dtype=np.float64),
                       where=max(hm_b_fba_num_48) != 0)
    for i in range(len(hm_b_fba_num_48)):
        hm_b_48.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_fba_num_48[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_fba_num_48)):
            hm_b_fba_num_48[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_j_fba_num_48, max(hm_j_fba_num_48), out=np.zeros_like(hm_j_fba_num_48, dtype=np.float64), where=max(hm_j_fba_num_48) != 0)
    for i in range(len(hm_j_fba_num_48)):
        hm_j_48.append("%.2f%%" % (arrayA[i]*100))
    if hm_j_fba_num_48[0] == 'nan%':
        a=0
        for i in range(len(hm_j_fba_num_48)):
            hm_j_fba_num_48[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_b_fba_num_72, max(hm_b_fba_num_72), out=np.zeros_like(hm_b_fba_num_72, dtype=np.float64),
                       where=max(hm_b_fba_num_72) != 0)
    for i in range(len(hm_b_fba_num_72)):
        hm_b_72.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_fba_num_72[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_fba_num_72)):
            hm_b_fba_num_72[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_j_fba_num_72, max(hm_j_fba_num_72), out=np.zeros_like(hm_j_fba_num_72, dtype=np.float64), where=max(hm_j_fba_num_72) != 0)
    for i in range(len(hm_j_fba_num_72)):
        hm_j_72.append("%.2f%%" % (arrayA[i]*100))
    if hm_j_fba_num_72[0] == 'nan%':
        a=0
        for i in range(len(hm_j_fba_num_72)):
            hm_j_fba_num_72[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_b_fba_num_120, max(hm_b_fba_num_120), out=np.zeros_like(hm_b_fba_num_120, dtype=np.float64),
                       where=max(hm_b_fba_num_120) != 0)
    for i in range(len(hm_b_fba_num_120)):
        hm_b_120.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_fba_num_120[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_fba_num_120)):
            hm_b_fba_num_120[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_j_fba_num_120, max(hm_j_fba_num_120), out=np.zeros_like(hm_j_fba_num_120, dtype=np.float64), where=max(hm_j_fba_num_120) != 0)
    for i in range(len(hm_j_fba_num_120)):
        hm_j_120.append("%.2f%%" % (arrayA[i]*100))
    if hm_j_fba_num_120[0] == 'nan%':
        a=0
        for i in range(len(hm_j_fba_num_120)):
            hm_j_fba_num_120[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_b_fba_num_240, max(hm_b_fba_num_240), out=np.zeros_like(hm_b_fba_num_240, dtype=np.float64),
                       where=max(hm_b_fba_num_240) != 0)
    for i in range(len(hm_b_fba_num_240)):
        hm_b_240.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_fba_num_240[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_fba_num_240)):
            hm_b_fba_num_240[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_j_fba_num_240, max(hm_j_fba_num_240), out=np.zeros_like(hm_j_fba_num_240, dtype=np.float64), where=max(hm_j_fba_num_240) != 0)
    for i in range(len(hm_j_fba_num_240)):
        hm_j_240.append("%.2f%%" % (arrayA[i]*100))
    if hm_j_fba_num_240[0] == 'nan%':
        a=0
        for i in range(len(hm_j_fba_num_240)):
            hm_j_fba_num_240[i] = '{:.2%}'.format(a)    # print(hm_j_240)
    arrayA = np.divide(hm_b_fba_num_360, max(hm_b_fba_num_360), out=np.zeros_like(hm_b_fba_num_360, dtype=np.float64),
                       where=max(hm_b_fba_num_360) != 0)
    for i in range(len(hm_b_fba_num_360)):
        hm_b_360.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_fba_num_360[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_fba_num_360)):
            hm_b_fba_num_360[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_j_fba_num_360, max(hm_j_fba_num_360), out=np.zeros_like(hm_j_fba_num_360, dtype=np.float64), where=max(hm_j_fba_num_360) != 0)
    for i in range(len(hm_j_fba_num_360)):
        hm_j_360.append("%.2f%%" % (arrayA[i]*100))
    if hm_j_fba_num_360[0] == 'nan%':
        a=0
        for i in range(len(hm_j_fba_num_360)):
            hm_j_fba_num_360[i] = '{:.2%}'.format(a)

    arrayA = np.divide(hm_b_fba_num_361, max(hm_b_fba_num_361), out=np.zeros_like(hm_b_fba_num_361, dtype=np.float64),
                       where=max(hm_b_fba_num_361) != 0)
    for i in range(len(hm_b_fba_num_361)):
        hm_b_361.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_fba_num_361[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_fba_num_361)):
            hm_b_fba_num_361[i] = '{:.2%}'.format(a)
    # print(hm_b_361)
    arrayA = np.divide(hm_j_fba_num_361, max(hm_j_fba_num_361), out=np.zeros_like(hm_j_fba_num_361, dtype=np.float64), where=max(hm_j_fba_num_361) != 0)
    for i in range(len(hm_j_fba_num_361)):
        hm_j_361.append("%.2f%%" % (arrayA[i]*100))
    if hm_j_fba_num_361[0] == 'nan%':
        a=0
        for i in range(len(hm_j_fba_num_361)):
            hm_j_fba_num_361[i] = '{:.2%}'.format(a)
    # print(hm_j_361)
    arrayA = np.divide(tx_b_fba_num_12, max(tx_b_fba_num_12), out=np.zeros_like(tx_b_fba_num_12, dtype=np.float64),
                       where=max(tx_b_fba_num_12) != 0)
    for i in range(len(tx_b_fba_num_12)):
        tx_b_12.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_fba_num_12[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_fba_num_12)):
            tx_b_fba_num_12[i] = '{:.2%}'.format(a)
    # print(tx_b_12)
    arrayA = np.divide(tx_j_fba_num_12, max(tx_j_fba_num_12), out=np.zeros_like(tx_j_fba_num_12, dtype=np.float64), where=max(tx_j_fba_num_12) != 0)
    for i in range(len(tx_j_fba_num_12)):
        tx_j_12.append("%.2f%%" % (arrayA[i]*100))
    if tx_j_fba_num_12[0] == 'nan%':
        a=0
        for i in range(len(tx_j_fba_num_12)):
            tx_j_fba_num_12[i] = '{:.2%}'.format(a)
    # print(tx_j_12)
    arrayA = np.divide(tx_b_fba_num_24, max(tx_b_fba_num_24), out=np.zeros_like(tx_b_fba_num_24, dtype=np.float64),
                       where=max(tx_b_fba_num_24) != 0)
    for i in range(len(tx_b_fba_num_24)):
        tx_b_24.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_fba_num_24[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_fba_num_24)):
            tx_b_fba_num_24[i] = '{:.2%}'.format(a)
    # print(tx_b_24)
    arrayA = np.divide(tx_j_fba_num_24, max(tx_j_fba_num_24), out=np.zeros_like(tx_j_fba_num_24, dtype=np.float64), where=max(tx_j_fba_num_24) != 0)
    for i in range(len(tx_j_fba_num_24)):
        tx_j_24.append("%.2f%%" % (arrayA[i]*100))
    if tx_j_fba_num_24[0] == 'nan%':
        a=0
        for i in range(len(tx_j_fba_num_24)):
            tx_j_fba_num_24[i] = '{:.2%}'.format(a)
    # print(tx_j_24)
    arrayA = np.divide(tx_b_fba_num_48, max(tx_b_fba_num_48), out=np.zeros_like(tx_b_fba_num_48, dtype=np.float64),
                       where=max(tx_b_fba_num_48) != 0)
    for i in range(len(tx_b_fba_num_48)):
        tx_b_48.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_fba_num_48[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_fba_num_48)):
            tx_b_fba_num_48[i] = '{:.2%}'.format(a)
    # print(tx_b_48)
    arrayA = np.divide(tx_j_fba_num_48, max(tx_j_fba_num_48), out=np.zeros_like(tx_j_fba_num_48, dtype=np.float64), where=max(tx_j_fba_num_48) != 0)
    for i in range(len(tx_j_fba_num_48)):
        tx_j_48.append("%.2f%%" % (arrayA[i]*100))
    if tx_j_fba_num_48[0] == 'nan%':
        a=0
        for i in range(len(tx_j_fba_num_48)):
            tx_j_fba_num_48[i] = '{:.2%}'.format(a)
    # print(tx_j_48)
    arrayA = np.divide(tx_b_fba_num_72, max(tx_b_fba_num_72), out=np.zeros_like(tx_b_fba_num_72, dtype=np.float64),
                       where=max(tx_b_fba_num_72) != 0)
    for i in range(len(tx_b_fba_num_72)):
        tx_b_72.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_fba_num_72[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_fba_num_72)):
            tx_b_fba_num_72[i] = '{:.2%}'.format(a)
    # print(tx_b_72)
    arrayA = np.divide(tx_j_fba_num_72, max(tx_j_fba_num_72), out=np.zeros_like(tx_j_fba_num_72, dtype=np.float64), where=max(tx_j_fba_num_72) != 0)
    for i in range(len(tx_j_fba_num_72)):
        tx_j_72.append("%.2f%%" % (arrayA[i]*100))
    if tx_j_fba_num_72[0] == 'nan%':
        a=0
        for i in range(len(tx_j_fba_num_72)):
            tx_j_fba_num_72[i] = '{:.2%}'.format(a)
    # print(tx_j_72)
    arrayA = np.divide(tx_b_fba_num_120, max(tx_b_fba_num_120), out=np.zeros_like(tx_b_fba_num_120, dtype=np.float64),
                       where=max(tx_b_fba_num_120) != 0)
    for i in range(len(tx_b_fba_num_120)):
        tx_b_120.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_fba_num_120[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_fba_num_120)):
            tx_b_fba_num_120[i] = '{:.2%}'.format(a)
    # print(tx_b_120)
    arrayA = np.divide(tx_j_fba_num_120, max(tx_j_fba_num_120), out=np.zeros_like(tx_j_fba_num_120, dtype=np.float64), where=max(tx_j_fba_num_120) != 0)
    for i in range(len(tx_j_fba_num_120)):
        tx_j_120.append("%.2f%%" % (arrayA[i]*100))
    if tx_j_fba_num_120[0] == 'nan%':
        a=0
        for i in range(len(tx_j_fba_num_120)):
            tx_j_fba_num_120[i] = '{:.2%}'.format(a)
    # print(tx_j_120)
    arrayA = np.divide(tx_b_fba_num_240, max(tx_b_fba_num_240), out=np.zeros_like(tx_b_fba_num_240, dtype=np.float64),
                       where=max(tx_b_fba_num_240) != 0)
    for i in range(len(tx_b_fba_num_240)):
        tx_b_240.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_fba_num_240[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_fba_num_240)):
            tx_b_fba_num_240[i] = '{:.2%}'.format(a)
    # print(tx_b_240)
    arrayA = np.divide(tx_j_fba_num_240, max(tx_j_fba_num_240), out=np.zeros_like(tx_j_fba_num_240, dtype=np.float64), where=max(tx_j_fba_num_240) != 0)
    for i in range(len(tx_j_fba_num_240)):
        tx_j_240.append("%.2f%%" % (arrayA[i]*100))
    if tx_j_fba_num_240[0] == 'nan%':
        a=0
        for i in range(len(tx_j_fba_num_240)):
            tx_j_fba_num_240[i] = '{:.2%}'.format(a)
    # print(tx_j_240)
    arrayA = np.divide(tx_b_fba_num_360, max(tx_b_fba_num_360), out=np.zeros_like(tx_b_fba_num_360, dtype=np.float64),
                       where=max(tx_b_fba_num_360) != 0)
    for i in range(len(tx_b_fba_num_360)):
        tx_b_360.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_fba_num_360[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_fba_num_360)):
            tx_b_fba_num_360[i] = '{:.2%}'.format(a)
    # print(tx_b_360)
    arrayA = np.divide(tx_j_fba_num_360, max(tx_j_fba_num_360), out=np.zeros_like(tx_j_fba_num_360, dtype=np.float64), where=max(tx_j_fba_num_360) != 0)
    for i in range(len(tx_j_fba_num_360)):
        tx_j_360.append("%.2f%%" % (arrayA[i]*100))
    if tx_j_fba_num_360[0] == 'nan%':
        a=0
        for i in range(len(tx_j_fba_num_360)):
            tx_j_fba_num_360[i] = '{:.2%}'.format(a)
    # print(tx_j_360)    cur.execute(sql)
    arrayA = np.divide(tx_b_fba_num_361, max(tx_b_fba_num_361), out=np.zeros_like(tx_b_fba_num_361, dtype=np.float64),
                       where=max(tx_b_fba_num_361) != 0)
    for i in range(len(tx_b_fba_num_361)):
        tx_b_361.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_fba_num_361[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_fba_num_361)):
            tx_b_fba_num_361[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_j_fba_num_361, max(tx_j_fba_num_361), out=np.zeros_like(tx_j_fba_num_361, dtype=np.float64), where=max(tx_j_fba_num_361) != 0)
    for i in range(len(tx_j_fba_num_361)):
        tx_j_361.append("%.2f%%" % (arrayA[i]*100))
    if tx_j_fba_num_361[0] == 'nan%':
        a=0
        for i in range(len(tx_j_fba_num_361)):
            tx_j_fba_num_361[i] = '{:.2%}'.format(a)


    warehouse = []
    type = []
    num = []
    time = []
    storage = []
    jsonData = {}
    for data in see:
        warehouse.append(data[0])
        type.append(data[5])
        num.append(float(data[4]))
        time.append(decimal.Decimal(data[6]))
        storage.append(data[2])

    hm_type = []
    hm_num = []
    hm_time = []
    hm_storage = []
    tx_type = []
    tx_num = []
    tx_time = []
    tx_storage = []
    for i in range(len(warehouse)):
        if warehouse[i] == 'HM_AA':
            hm_type.append(type[i])
            hm_num.append(num[i])
            hm_time.append(time[i])
            hm_storage.append(storage[i])
    for i in range(len(warehouse)):
        if warehouse[i] == 'SZ_AA':
            tx_type.append(type[i])
            tx_num.append(num[i])
            tx_time.append(time[i])
            tx_storage.append(storage[i])

    hm_data = np.dstack((hm_type, hm_num, hm_time, hm_storage))
    tx_data = np.dstack((tx_type, tx_num, tx_time, tx_storage))

    hm_drk_b_num = []
    hm_drk_j_num = []
    hm_drk_time = []

    hm_dtm_b_num = []
    hm_dtm_j_num = []
    hm_dtm_time = []

    hm_dgnzj_b_num = []
    hm_dgnzj_j_num = []
    hm_dgnzj_time = []

    hm_dsj_b_num = []
    hm_dsj_j_num = []
    hm_dsj_time = []

    hm_sjz_b_num = []
    hm_sjz_j_num = []
    hm_sjz_time = []

    tx_drk_b_num = []
    tx_drk_j_num = []
    tx_drk_time = []

    tx_dtm_b_num = []
    tx_dtm_j_num = []
    tx_dtm_time = []

    tx_dgnzj_b_num = []
    tx_dgnzj_j_num = []
    tx_dgnzj_time = []

    tx_dsj_b_num = []
    tx_dsj_j_num = []
    tx_dsj_time = []

    tx_sjz_b_num = []
    tx_sjz_j_num = []
    tx_sjz_time = []

    hm_data_shelf = np.vstack((hm_storage, hm_time, hm_type)).T
    tx_data_shelf = np.vstack((tx_storage, tx_time, tx_type)).T
    hm_storage = np.array(hm_storage)
    tx_storage = np.array(tx_storage)
    hm_data_shelf = hm_data_shelf[np.argsort(-hm_data_shelf[:, 1])]
    tx_data_shelf = tx_data_shelf[np.argsort(-tx_data_shelf[:, 1])]


    hm_drk_shelf = []
    hm_drk_shelf_time = []
    hm_dtm_shelf = []
    hm_dtm_shelf_time = []
    hm_dgnzj_shelf = []
    hm_dgnzj_shelf_time = []
    hm_dsj_shelf = []
    hm_dsj_shelf_time = []
    hm_sjz_shelf = []
    hm_sjz_shelf_time = []

    tx_drk_shelf = []
    tx_drk_shelf_time = []
    tx_dtm_shelf = []
    tx_dtm_shelf_time = []
    tx_dgnzj_shelf = []
    tx_dgnzj_shelf_time = []
    tx_dsj_shelf = []
    tx_dsj_shelf_time = []
    tx_sjz_shelf = []
    tx_sjz_shelf_time = []
    for i in range(len(hm_data_shelf)):
        if (hm_data_shelf[i][2] == 'DRK'):
            hm_drk_shelf.append(hm_data_shelf[i][0])
            hm_drk_shelf_time.append(hm_data_shelf[i][1])
    hm_drk_all = np.dstack((hm_drk_shelf, hm_drk_shelf_time))

    for i in range(len(hm_data_shelf)):
        if (hm_data_shelf[i][2] == 'DTM'):
            hm_dtm_shelf.append(hm_data_shelf[i][0])
            hm_dtm_shelf_time.append(hm_data_shelf[i][1])
    hm_dtm_all = np.dstack((hm_dtm_shelf, hm_dtm_shelf_time))

    for i in range(len(hm_data_shelf)):
        if (hm_data_shelf[i][2] == 'DGNZJ'):
            hm_dgnzj_shelf.append(hm_data_shelf[i][0])
            hm_dgnzj_shelf_time.append(hm_data_shelf[i][1])
    hm_dgnzj_all = np.dstack((hm_dgnzj_shelf, hm_dgnzj_shelf_time))

    for i in range(len(hm_data_shelf)):
        if (hm_data_shelf[i][2] == 'DSJ'):
            hm_dsj_shelf.append(hm_data_shelf[i][0])
            hm_dsj_shelf_time.append(hm_data_shelf[i][1])
    hm_dsj_all = np.dstack((hm_dsj_shelf, hm_dsj_shelf_time))

    for i in range(len(hm_data_shelf)):
        if (hm_data_shelf[i][2] == 'SJZ'):
            hm_sjz_shelf.append(hm_data_shelf[i][0])
            hm_sjz_shelf_time.append(hm_data_shelf[i][1])
    hm_sjz_all = np.dstack((hm_sjz_shelf, hm_sjz_shelf_time))

    for i in range(len(tx_data_shelf)):
        if (tx_data_shelf[i][2] == 'DRK'):
            tx_drk_shelf.append(tx_data_shelf[i][0])
            tx_drk_shelf_time.append(tx_data_shelf[i][1])
    tx_drk_all = np.dstack((tx_drk_shelf, tx_drk_shelf_time))

    for i in range(len(tx_data_shelf)):
        if (tx_data_shelf[i][2] == 'DTM'):
            tx_dtm_shelf.append(tx_data_shelf[i][0])
            tx_dtm_shelf_time.append(tx_data_shelf[i][1])
    tx_dtm_all = np.dstack((tx_dtm_shelf, tx_dtm_shelf_time))

    for i in range(len(tx_data_shelf)):
        if (tx_data_shelf[i][2] == 'DGNZJ'):
            tx_dgnzj_shelf.append(tx_data_shelf[i][0])
            tx_dgnzj_shelf_time.append(tx_data_shelf[i][1])
    tx_dgnzj_all = np.dstack((tx_dgnzj_shelf, tx_dgnzj_shelf_time))

    for i in range(len(tx_data_shelf)):
        if (tx_data_shelf[i][2] == 'DSJ'):
            tx_dsj_shelf.append(tx_data_shelf[i][0])
            tx_dsj_shelf_time.append(tx_data_shelf[i][1])
    tx_dsj_all = np.dstack((tx_dsj_shelf, tx_dsj_shelf_time))

    for i in range(len(tx_data_shelf)):
        if (tx_data_shelf[i][2] == 'SJZ'):
            tx_sjz_shelf.append(tx_data_shelf[i][0])
            tx_sjz_shelf_time.append(tx_data_shelf[i][1])
    tx_sjz_all = np.dstack((tx_sjz_shelf, tx_sjz_shelf_time))

    ###数组去重
    #########################################################
    a1 = []
    a2 = []
    tx_drk_shelf = []
    tx_drk_shelf_time = []
    for i in range(len(tx_drk_all[0])):
        if tx_drk_all[0][i][0] not in a2:
            a1.append(tx_drk_all[0][i])
        a2.append(tx_drk_all[0][i][0])
    for i in range(len(a1)):
        tx_drk_shelf.append(a1[i][0])
        tx_drk_shelf_time.append(a1[i][1])
    #########################################################
    a1 = []
    a2 = []
    tx_dtm_shelf = []
    tx_dtm_shelf_time = []
    for i in range(len(tx_dtm_all[0])):
        if tx_dtm_all[0][i][0] not in a2:
            a1.append(tx_dtm_all[0][i])
        a2.append(tx_dtm_all[0][i][0])
    for i in range(len(a1)):
        tx_dtm_shelf.append(a1[i][0])
        tx_dtm_shelf_time.append(a1[i][1])
    #########################################################
    a1 = []
    a2 = []
    tx_dgnzj_shelf = []
    tx_dgnzj_shelf_time = []
    for i in range(len(tx_dgnzj_all[0])):
        if tx_dgnzj_all[0][i][0] not in a2:
            a1.append(tx_dgnzj_all[0][i])
        a2.append(tx_dgnzj_all[0][i][0])
    for i in range(len(a1)):
        tx_dgnzj_shelf.append(a1[i][0])
        tx_dgnzj_shelf_time.append(a1[i][1])
    #########################################################
    a1 = []
    a2 = []
    tx_dsj_shelf = []
    tx_dsj_shelf_time = []
    for i in range(len(tx_dsj_all[0])):
        if tx_dsj_all[0][i][0] not in a2:
            a1.append(tx_dsj_all[0][i])
        a2.append(tx_dsj_all[0][i][0])
    for i in range(len(a1)):
        tx_dsj_shelf.append(a1[i][0])
        tx_dsj_shelf_time.append(a1[i][1])
    #########################################################
    a1 = []
    a2 = []
    tx_sjz_shelf = []
    tx_sjz_shelf_time = []
    for i in range(len(tx_sjz_all[0])):
        if tx_sjz_all[0][i][0] not in a2:
            a1.append(tx_sjz_all[0][i])
        a2.append(tx_sjz_all[0][i][0])
    for i in range(len(a1)):
        tx_sjz_shelf.append(a1[i][0])
        tx_sjz_shelf_time.append(a1[i][1])

    tx_drk_shelf_num = np.r_[tx_drk_shelf_time[0:10]]
    tx_dtm_shelf_num = np.r_[tx_dtm_shelf_time[0:10]]
    tx_dgnzj_shelf_num = np.r_[tx_dgnzj_shelf_time[0:10]]
    tx_dsj_shelf_num = np.r_[tx_dsj_shelf_time[0:10]]
    tx_sjz_shelf_num = np.r_[tx_sjz_shelf_time[0:10]]
    tx_drk_shelf_num1 = []
    tx_dtm_shelf_num1 = []
    tx_dgnzj_shelf_num1 = []
    tx_dsj_shelf_num1 = []
    tx_sjz_shelf_num1 = []

    for i in range(len(tx_drk_shelf_num)):
        a = tx_drk_shelf_num[i] / max(tx_drk_shelf_num)
        tx_drk_shelf_num1.append('{:.2%}'.format(a))

    for i in range(len(tx_dtm_shelf_num)):
        a = tx_dtm_shelf_num[i] / max(tx_dtm_shelf_num)
        tx_dtm_shelf_num1.append('{:.2%}'.format(a))

    for i in range(len(tx_dgnzj_shelf_num)):
        a = tx_dgnzj_shelf_num[i] / max(tx_dgnzj_shelf_num)
        tx_dgnzj_shelf_num1.append('{:.2%}'.format(a))

    for i in range(len(tx_dsj_shelf_num)):
        a = tx_dsj_shelf_num[i] / max(tx_dsj_shelf_num)
        tx_dsj_shelf_num1.append('{:.2%}'.format(a))

    for i in range(len(tx_sjz_shelf_num)):
        a = tx_sjz_shelf_num[i] / max(tx_sjz_shelf_num)
        tx_sjz_shelf_num1.append('{:.2%}'.format(a))

    a1 = []
    a2 = []
    hm_drk_shelf = []
    hm_drk_shelf_time = []
    for i in range(len(hm_drk_all[0])):
        if hm_drk_all[0][i][0] not in a2:
            a1.append(hm_drk_all[0][i])
        a2.append(hm_drk_all[0][i][0])
    for i in range(len(a1)):
        hm_drk_shelf.append(a1[i][0])
        hm_drk_shelf_time.append(a1[i][1])
    #########################################################
    a1 = []
    a2 = []
    hm_dtm_shelf = []
    hm_dtm_shelf_time = []
    for i in range(len(hm_dtm_all[0])):
        if hm_dtm_all[0][i][0] not in a2:
            a1.append(hm_dtm_all[0][i])
        a2.append(hm_dtm_all[0][i][0])
    for i in range(len(a1)):
        hm_dtm_shelf.append(a1[i][0])
        hm_dtm_shelf_time.append(a1[i][1])
    #########################################################
    a1 = []
    a2 = []
    hm_dgnzj_shelf = []
    hm_dgnzj_shelf_time = []
    for i in range(len(hm_dgnzj_all[0])):
        if hm_dgnzj_all[0][i][0] not in a2:
            a1.append(hm_dgnzj_all[0][i])
        a2.append(hm_dgnzj_all[0][i][0])
    for i in range(len(a1)):
        hm_dgnzj_shelf.append(a1[i][0])
        hm_dgnzj_shelf_time.append(a1[i][1])
    #########################################################
    a1 = []
    a2 = []
    hm_dsj_shelf = []
    hm_dsj_shelf_time = []
    for i in range(len(hm_dsj_all[0])):
        if hm_dsj_all[0][i][0] not in a2:
            a1.append(hm_dsj_all[0][i])
        a2.append(hm_dsj_all[0][i][0])
    for i in range(len(a1)):
        hm_dsj_shelf.append(a1[i][0])
        hm_dsj_shelf_time.append(a1[i][1])
    #########################################################
    a1 = []
    a2 = []
    hm_sjz_shelf = []
    hm_sjz_shelf_time = []
    for i in range(len(hm_sjz_all[0])):
        if hm_sjz_all[0][i][0] not in a2:
            a1.append(hm_sjz_all[0][i])
        a2.append(hm_sjz_all[0][i][0])
    for i in range(len(a1)):
        hm_sjz_shelf.append(a1[i][0])
        hm_sjz_shelf_time.append(a1[i][1])

    hm_drk_shelf_num = np.r_[hm_drk_shelf_time[0:10]]
    hm_dtm_shelf_num = np.r_[hm_dtm_shelf_time[0:10]]
    hm_dgnzj_shelf_num = np.r_[hm_dgnzj_shelf_time[0:10]]
    hm_dsj_shelf_num = np.r_[hm_dsj_shelf_time[0:10]]
    hm_sjz_shelf_num = np.r_[hm_sjz_shelf_time[0:10]]
    hm_drk_shelf_num1 = []
    hm_dtm_shelf_num1 = []
    hm_dgnzj_shelf_num1 = []
    hm_dsj_shelf_num1 = []
    hm_sjz_shelf_num1 = []

    for i in range(len(hm_drk_shelf_num)):
        a = hm_drk_shelf_num[i] / max(hm_drk_shelf_num)
        hm_drk_shelf_num1.append('{:.2%}'.format(a))

    for i in range(len(hm_dtm_shelf_num)):
        a = hm_dtm_shelf_num[i] / max(hm_dtm_shelf_num)
        hm_dtm_shelf_num1.append('{:.2%}'.format(a))

    for i in range(len(hm_dgnzj_shelf_num)):
        a = hm_dgnzj_shelf_num[i] / max(hm_dgnzj_shelf_num)
        hm_dgnzj_shelf_num1.append('{:.2%}'.format(a))

    for i in range(len(hm_dsj_shelf_num)):
        a = hm_dsj_shelf_num[i] / max(hm_dsj_shelf_num)
        hm_dsj_shelf_num1.append('{:.2%}'.format(a))

    for i in range(len(hm_sjz_shelf_num)):
        a = hm_sjz_shelf_num[i] / max(hm_sjz_shelf_num)
        hm_sjz_shelf_num1.append('{:.2%}'.format(a))

    for i in range(len(hm_time)):
        if (hm_data[0][i][0] == 'DRK'):
            hm_drk_b_num.append(1)
            hm_drk_j_num.append(hm_data[0][i][1])
            hm_drk_time.append(hm_data[0][i][2])
    for i in range(len(hm_time)):
        if (hm_data[0][i][0] == 'DTM'):
            hm_dtm_b_num.append(1)
            hm_dtm_j_num.append(hm_data[0][i][1])
            hm_dtm_time.append(hm_data[0][i][2])
    for i in range(len(hm_time)):
        if (hm_data[0][i][0] == 'DGNZJ'):
            hm_dgnzj_b_num.append(1)
            hm_dgnzj_j_num.append(hm_data[0][i][1])
            hm_dgnzj_time.append(hm_data[0][i][2])
    for i in range(len(hm_time)):
        if (hm_data[0][i][0] == 'DSJ'):
            hm_dsj_b_num.append(1)
            hm_dsj_j_num.append(hm_data[0][i][1])
            hm_dsj_time.append(hm_data[0][i][2])
    for i in range(len(hm_time)):
        if (hm_data[0][i][0] == 'SJZ'):
            hm_sjz_b_num.append(1)
            hm_sjz_j_num.append(hm_data[0][i][1])
            hm_sjz_time.append(hm_data[0][i][2])

    for i in range(len(tx_time)):
        if (tx_data[0][i][0] == 'DRK'):
            tx_drk_b_num.append(1)
            tx_drk_j_num.append(tx_data[0][i][1])
            tx_drk_time.append(tx_data[0][i][2])
    for i in range(len(tx_time)):
        if (tx_data[0][i][0] == 'DTM'):
            tx_dtm_b_num.append(1)
            tx_dtm_j_num.append(tx_data[0][i][1])
            tx_dtm_time.append(tx_data[0][i][2])
    for i in range(len(tx_time)):
        if (tx_data[0][i][0] == 'DGNZJ'):
            tx_dgnzj_b_num.append(1)
            tx_dgnzj_j_num.append(tx_data[0][i][1])
            tx_dgnzj_time.append(tx_data[0][i][2])
    for i in range(len(tx_time)):
        if (tx_data[0][i][0] == 'DSJ'):
            tx_dsj_b_num.append(1)
            tx_dsj_j_num.append(tx_data[0][i][1])
            tx_dsj_time.append(tx_data[0][i][2])
    for i in range(len(tx_time)):
        if (tx_data[0][i][0] == 'SJZ'):
            tx_sjz_b_num.append(1)
            tx_sjz_j_num.append(tx_data[0][i][1])
            tx_sjz_time.append(tx_data[0][i][2])

    hm_drk = np.dstack((hm_drk_b_num, hm_drk_j_num, hm_drk_time))
    hm_dtm = np.dstack((hm_dtm_b_num, hm_dtm_j_num, hm_dtm_time))
    hm_dgnzj = np.dstack((hm_dgnzj_b_num, hm_dgnzj_j_num, hm_dgnzj_time))
    hm_dsj = np.dstack((hm_dsj_b_num, hm_dsj_j_num, hm_dsj_time))
    hm_sjz = np.dstack((hm_sjz_b_num, hm_sjz_j_num, hm_sjz_time))

    tx_drk = np.dstack((tx_drk_b_num, tx_drk_j_num, tx_drk_time))
    tx_dtm = np.dstack((tx_dtm_b_num, tx_dtm_j_num, tx_dtm_time))
    tx_dgnzj = np.dstack((tx_dgnzj_b_num, tx_dgnzj_j_num, tx_dgnzj_time))
    tx_dsj = np.dstack((tx_dsj_b_num, tx_dsj_j_num, tx_dsj_time))
    tx_sjz = np.dstack((tx_sjz_b_num, tx_sjz_j_num, tx_sjz_time))

    hm_drk_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_dtm_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_dgnzj_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_dsj_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_sjz_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]

    tx_drk_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_dtm_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_dgnzj_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_dsj_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_sjz_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]

    hm_drk_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_dtm_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_dgnzj_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_dsj_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_sjz_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]

    tx_drk_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_dtm_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_dgnzj_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_dsj_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_sjz_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]

    for i in range(len(hm_drk[0])):
        if float(hm_drk[0][i][2]) > 0 and float(hm_drk[0][i][2]) <= 6:
            hm_drk_b_num1[0] = hm_drk_b_num1[0] + 1
            hm_drk_j_num1[0] = hm_drk_j_num1[0] + hm_drk[0][i][1]
        if float(hm_drk[0][i][2]) > 6 and float(hm_drk[0][i][2]) <= 12:
            hm_drk_b_num1[1] = hm_drk_b_num1[1] + 1
            hm_drk_j_num1[1] = hm_drk_j_num1[1] + hm_drk[0][i][1]
        if float(hm_drk[0][i][2]) > 12 and float(hm_drk[0][i][2]) <= 24:
            hm_drk_b_num1[2] = hm_drk_b_num1[2] + 1
            hm_drk_j_num1[2] = hm_drk_j_num1[2] + hm_drk[0][i][1]
        if float(hm_drk[0][i][2]) > 24 and float(hm_drk[0][i][2]) <= 36:
            hm_drk_b_num1[3] = hm_drk_b_num1[3] + 1
            hm_drk_j_num1[3] = hm_drk_j_num1[3] + hm_drk[0][i][1]
        if float(hm_drk[0][i][2]) > 36 and float(hm_drk[0][i][2]) <= 48:
            hm_drk_b_num1[4] = hm_drk_b_num1[4] + 1
            hm_drk_j_num1[4] = hm_drk_j_num1[4] + hm_drk[0][i][1]
        if float(hm_drk[0][i][2]) > 48 and float(hm_drk[0][i][2]) <= 72:
            hm_drk_b_num1[5] = hm_drk_b_num1[5] + 1
            hm_drk_j_num1[5] = hm_drk_j_num1[5] + hm_drk[0][i][1]
        if float(hm_drk[0][i][2]) > 72 and float(hm_drk[0][i][2]) <= 96:
            hm_drk_b_num1[6] = hm_drk_b_num1[6] + 1
            hm_drk_j_num1[6] = hm_drk_j_num1[6] + hm_drk[0][i][1]
        if float(hm_drk[0][i][2]) > 96:
            hm_drk_b_num1[7] = hm_drk_b_num1[7] + 1
            hm_drk_j_num1[7] = hm_drk_j_num1[7] + hm_drk[0][i][1]

    for i in range(len(hm_dtm[0])):
        if float(hm_dtm[0][i][2]) > 0 and float(hm_dtm[0][i][2]) <= 6:
            hm_dtm_b_num1[0] = hm_dtm_b_num1[0] + 1
            hm_dtm_j_num1[0] = hm_dtm_j_num1[0] + hm_dtm[0][i][1]
        if float(hm_dtm[0][i][2]) > 6 and float(hm_dtm[0][i][2]) <= 12:
            hm_dtm_b_num1[1] = hm_dtm_b_num1[1] + 1
            hm_dtm_j_num1[1] = hm_dtm_j_num1[1] + hm_dtm[0][i][1]
        if float(hm_dtm[0][i][2]) > 12 and float(hm_dtm[0][i][2]) <= 24:
            hm_dtm_b_num1[2] = hm_dtm_b_num1[2] + 1
            hm_dtm_j_num1[2] = hm_dtm_j_num1[2] + hm_dtm[0][i][1]
        if float(hm_dtm[0][i][2]) > 24 and float(hm_dtm[0][i][2]) <= 36:
            hm_dtm_b_num1[3] = hm_dtm_b_num1[3] + 1
            hm_dtm_j_num1[3] = hm_dtm_j_num1[3] + hm_dtm[0][i][1]
        if float(hm_dtm[0][i][2]) > 36 and float(hm_dtm[0][i][2]) <= 48:
            hm_dtm_b_num1[4] = hm_dtm_b_num1[4] + 1
            hm_dtm_j_num1[4] = hm_dtm_j_num1[4] + hm_dtm[0][i][1]
        if float(hm_dtm[0][i][2]) > 48 and float(hm_dtm[0][i][2]) <= 72:
            hm_dtm_b_num1[5] = hm_dtm_b_num1[5] + 1
            hm_dtm_j_num1[5] = hm_dtm_j_num1[5] + hm_dtm[0][i][1]
        if float(hm_dtm[0][i][2]) > 72 and float(hm_dtm[0][i][2]) <= 96:
            hm_dtm_b_num1[6] = hm_dtm_b_num1[6] + 1
            hm_dtm_j_num1[6] = hm_dtm_j_num1[6] + hm_dtm[0][i][1]
        if float(hm_dtm[0][i][2]) > 96:
            hm_dtm_b_num1[7] = hm_dtm_b_num1[7] + 1
            hm_dtm_j_num1[7] = hm_dtm_j_num1[7] + hm_dtm[0][i][1]
    for i in range(len(hm_dgnzj[0])):
        if float(hm_dgnzj[0][i][2]) > 0 and float(hm_dgnzj[0][i][2]) <= 6:
            hm_dgnzj_b_num1[0] = hm_dgnzj_b_num1[0] + 1
            hm_dgnzj_j_num1[0] = hm_dgnzj_j_num1[0] + hm_dgnzj[0][i][1]
        if float(hm_dgnzj[0][i][2]) > 6 and float(hm_dgnzj[0][i][2]) <= 12:
            hm_dgnzj_b_num1[1] = hm_dgnzj_b_num1[1] + 1
            hm_dgnzj_j_num1[1] = hm_dgnzj_j_num1[1] + hm_dgnzj[0][i][1]
        if float(hm_dgnzj[0][i][2]) > 12 and float(hm_dgnzj[0][i][2]) <= 24:
            hm_dgnzj_b_num1[2] = hm_dgnzj_b_num1[2] + 1
            hm_dgnzj_j_num1[2] = hm_dgnzj_j_num1[2] + hm_dgnzj[0][i][1]
        if float(hm_dgnzj[0][i][2]) > 24 and float(hm_dgnzj[0][i][2]) <= 36:
            hm_dgnzj_b_num1[3] = hm_dgnzj_b_num1[3] + 1
            hm_dgnzj_j_num1[3] = hm_dgnzj_j_num1[3] + hm_dgnzj[0][i][1]
        if float(hm_dgnzj[0][i][2]) > 36 and float(hm_dgnzj[0][i][2]) <= 48:
            hm_dgnzj_b_num1[4] = hm_dgnzj_b_num1[4] + 1
            hm_dgnzj_j_num1[4] = hm_dgnzj_j_num1[4] + hm_dgnzj[0][i][1]
        if float(hm_dgnzj[0][i][2]) > 48 and float(hm_dgnzj[0][i][2]) <= 72:
            hm_dgnzj_b_num1[5] = hm_dgnzj_b_num1[5] + 1
            hm_dgnzj_j_num1[5] = hm_dgnzj_j_num1[5] + hm_dgnzj[0][i][1]
        if float(hm_dgnzj[0][i][2]) > 72 and float(hm_dgnzj[0][i][2]) <= 96:
            hm_dgnzj_b_num1[6] = hm_dgnzj_b_num1[6] + 1
            hm_dgnzj_j_num1[6] = hm_dgnzj_j_num1[6] + hm_dgnzj[0][i][1]
        if float(hm_dgnzj[0][i][2]) > 96:
            hm_dgnzj_b_num1[7] = hm_dgnzj_b_num1[7] + 1
            hm_dgnzj_j_num1[7] = hm_dgnzj_j_num1[7] + hm_dgnzj[0][i][1]

    for i in range(len(hm_dsj[0])):
        if float(hm_dsj[0][i][2]) > 0 and float(hm_dsj[0][i][2]) <= 6:
            hm_dsj_b_num1[0] = hm_dsj_b_num1[0] + 1
            hm_dsj_j_num1[0] = hm_dsj_j_num1[0] + hm_dsj[0][i][1]
        if float(hm_dsj[0][i][2]) > 6 and float(hm_dsj[0][i][2]) <= 12:
            hm_dsj_b_num1[1] = hm_dsj_b_num1[1] + 1
            hm_dsj_j_num1[1] = hm_dsj_j_num1[1] + hm_dsj[0][i][1]
        if float(hm_dsj[0][i][2]) > 12 and float(hm_dsj[0][i][2]) <= 24:
            hm_dsj_b_num1[2] = hm_dsj_b_num1[2] + 1
            hm_dsj_j_num1[2] = hm_dsj_j_num1[2] + hm_dsj[0][i][1]
        if float(hm_dsj[0][i][2]) > 24 and float(hm_dsj[0][i][2]) <= 36:
            hm_dsj_b_num1[3] = hm_dsj_b_num1[3] + 1
            hm_dsj_j_num1[3] = hm_dsj_j_num1[3] + hm_dsj[0][i][1]
        if float(hm_dsj[0][i][2]) > 36 and float(hm_dsj[0][i][2]) <= 48:
            hm_dsj_b_num1[4] = hm_dsj_b_num1[4] + 1
            hm_dsj_j_num1[4] = hm_dsj_j_num1[4] + hm_dsj[0][i][1]
        if float(hm_dsj[0][i][2]) > 48 and float(hm_dsj[0][i][2]) <= 72:
            hm_dsj_b_num1[5] = hm_dsj_b_num1[5] + 1
            hm_dsj_j_num1[5] = hm_dsj_j_num1[5] + hm_dsj[0][i][1]
        if float(hm_dsj[0][i][2]) > 72 and float(hm_dsj[0][i][2]) <= 96:
            hm_dsj_b_num1[6] = hm_dsj_b_num1[6] + 1
            hm_dsj_j_num1[6] = hm_dsj_j_num1[6] + hm_dsj[0][i][1]
        if float(hm_dsj[0][i][2]) > 96:
            hm_dsj_b_num1[7] = hm_dsj_b_num1[7] + 1
            hm_dsj_j_num1[7] = hm_dsj_j_num1[7] + hm_dsj[0][i][1]

    for i in range(len(hm_sjz[0])):
        if float(hm_sjz[0][i][2]) > 0 and float(hm_sjz[0][i][2]) <= 6:
            hm_sjz_b_num1[0] = hm_sjz_b_num1[0] + 1
            hm_sjz_j_num1[0] = hm_sjz_j_num1[0] + hm_sjz[0][i][1]
        if float(hm_sjz[0][i][2]) > 6 and float(hm_sjz[0][i][2]) <= 12:
            hm_sjz_b_num1[1] = hm_sjz_b_num1[1] + 1
            hm_sjz_j_num1[1] = hm_sjz_j_num1[1] + hm_sjz[0][i][1]
        if float(hm_sjz[0][i][2]) > 12 and float(hm_sjz[0][i][2]) <= 24:
            hm_sjz_b_num1[2] = hm_sjz_b_num1[2] + 1
            hm_sjz_j_num1[2] = hm_sjz_j_num1[2] + hm_sjz[0][i][1]
        if float(hm_sjz[0][i][2]) > 24 and float(hm_sjz[0][i][2]) <= 36:
            hm_sjz_b_num1[3] = hm_sjz_b_num1[3] + 1
            hm_sjz_j_num1[3] = hm_sjz_j_num1[3] + hm_sjz[0][i][1]
        if float(hm_sjz[0][i][2]) > 36 and float(hm_sjz[0][i][2]) <= 48:
            hm_sjz_b_num1[4] = hm_sjz_b_num1[4] + 1
            hm_sjz_j_num1[4] = hm_sjz_j_num1[4] + hm_sjz[0][i][1]
        if float(hm_sjz[0][i][2]) > 48 and float(hm_sjz[0][i][2]) <= 72:
            hm_sjz_b_num1[5] = hm_sjz_b_num1[5] + 1
            hm_sjz_j_num1[5] = hm_sjz_j_num1[5] + hm_sjz[0][i][1]
        if float(hm_sjz[0][i][2]) > 72 and float(hm_sjz[0][i][2]) <= 96:
            hm_sjz_b_num1[6] = hm_sjz_b_num1[6] + 1
            hm_sjz_j_num1[6] = hm_sjz_j_num1[6] + hm_sjz[0][i][1]
        if float(hm_sjz[0][i][2]) > 96:
            hm_sjz_b_num1[7] = hm_sjz_b_num1[7] + 1
            hm_sjz_j_num1[7] = hm_sjz_j_num1[7] + hm_sjz[0][i][1]

    for i in range(len(tx_drk[0])):
        if float(tx_drk[0][i][2]) > 0 and float(tx_drk[0][i][2]) <= 6:
            tx_drk_b_num1[0] = tx_drk_b_num1[0] + 1
            tx_drk_j_num1[0] = tx_drk_j_num1[0] + tx_drk[0][i][1]
        if float(tx_drk[0][i][2]) > 6 and float(tx_drk[0][i][2]) <= 12:
            tx_drk_b_num1[1] = tx_drk_b_num1[1] + 1
            tx_drk_j_num1[1] = tx_drk_j_num1[1] + tx_drk[0][i][1]
        if float(tx_drk[0][i][2]) > 12 and float(tx_drk[0][i][2]) <= 24:
            tx_drk_b_num1[2] = tx_drk_b_num1[2] + 1
            tx_drk_j_num1[2] = tx_drk_j_num1[2] + tx_drk[0][i][1]
        if float(tx_drk[0][i][2]) > 24 and float(tx_drk[0][i][2]) <= 36:
            tx_drk_b_num1[3] = tx_drk_b_num1[3] + 1
            tx_drk_j_num1[3] = tx_drk_j_num1[3] + tx_drk[0][i][1]
        if float(tx_drk[0][i][2]) > 36 and float(tx_drk[0][i][2]) <= 48:
            tx_drk_b_num1[4] = tx_drk_b_num1[4] + 1
            tx_drk_j_num1[4] = tx_drk_j_num1[4] + tx_drk[0][i][1]
        if float(tx_drk[0][i][2]) > 48 and float(tx_drk[0][i][2]) <= 72:
            tx_drk_b_num1[5] = tx_drk_b_num1[5] + 1
            tx_drk_j_num1[5] = tx_drk_j_num1[5] + tx_drk[0][i][1]
        if float(tx_drk[0][i][2]) > 72 and float(tx_drk[0][i][2]) <= 96:
            tx_drk_b_num1[6] = tx_drk_b_num1[6] + 1
            tx_drk_j_num1[6] = tx_drk_j_num1[6] + tx_drk[0][i][1]
        if float(tx_drk[0][i][2]) > 96:
            tx_drk_b_num1[7] = tx_drk_b_num1[7] + 1
            tx_drk_j_num1[7] = tx_drk_j_num1[7] + tx_drk[0][i][1]

    for i in range(len(tx_dtm[0])):
        if float(tx_dtm[0][i][2]) > 0 and float(tx_dtm[0][i][2]) <= 6:
            tx_dtm_b_num1[0] = tx_dtm_b_num1[0] + 1
            tx_dtm_j_num1[0] = tx_dtm_j_num1[0] + tx_dtm[0][i][1]
        if float(tx_dtm[0][i][2]) > 6 and float(tx_dtm[0][i][2]) <= 12:
            tx_dtm_b_num1[1] = tx_dtm_b_num1[1] + 1
            tx_dtm_j_num1[1] = tx_dtm_j_num1[1] + tx_dtm[0][i][1]
        if float(tx_dtm[0][i][2]) > 12 and float(tx_dtm[0][i][2]) <= 24:
            tx_dtm_b_num1[2] = tx_dtm_b_num1[2] + 1
            tx_dtm_j_num1[2] = tx_dtm_j_num1[2] + tx_dtm[0][i][1]
        if float(tx_dtm[0][i][2]) > 24 and float(tx_dtm[0][i][2]) <= 36:
            tx_dtm_b_num1[3] = tx_dtm_b_num1[3] + 1
            tx_dtm_j_num1[3] = tx_dtm_j_num1[3] + tx_dtm[0][i][1]
        if float(tx_dtm[0][i][2]) > 36 and float(tx_dtm[0][i][2]) <= 48:
            tx_dtm_b_num1[4] = tx_dtm_b_num1[4] + 1
            tx_dtm_j_num1[4] = tx_dtm_j_num1[4] + tx_dtm[0][i][1]
        if float(tx_dtm[0][i][2]) > 48 and float(tx_dtm[0][i][2]) <= 72:
            tx_dtm_b_num1[5] = tx_dtm_b_num1[5] + 1
            tx_dtm_j_num1[5] = tx_dtm_j_num1[5] + tx_dtm[0][i][1]
        if float(tx_dtm[0][i][2]) > 72 and float(tx_dtm[0][i][2]) <= 96:
            tx_dtm_b_num1[6] = tx_dtm_b_num1[6] + 1
            tx_dtm_j_num1[6] = tx_dtm_j_num1[6] + tx_dtm[0][i][1]
        if float(tx_dtm[0][i][2]) > 96:
            tx_dtm_b_num1[7] = tx_dtm_b_num1[7] + 1
            tx_dtm_j_num1[7] = tx_dtm_j_num1[7] + tx_dtm[0][i][1]

    for i in range(len(tx_dgnzj[0])):
        if float(tx_dgnzj[0][i][2]) > 0 and float(tx_dgnzj[0][i][2]) <= 6:
            tx_dgnzj_b_num1[0] = tx_dgnzj_b_num1[0] + 1
            tx_dgnzj_j_num1[0] = tx_dgnzj_j_num1[0] + tx_dgnzj[0][i][1]
        if float(tx_dgnzj[0][i][2]) > 6 and float(tx_dgnzj[0][i][2]) <= 12:
            tx_dgnzj_b_num1[1] = tx_dgnzj_b_num1[1] + 1
            tx_dgnzj_j_num1[1] = tx_dgnzj_j_num1[1] + tx_dgnzj[0][i][1]
        if float(tx_dgnzj[0][i][2]) > 12 and float(tx_dgnzj[0][i][2]) <= 24:
            tx_dgnzj_b_num1[2] = tx_dgnzj_b_num1[2] + 1
            tx_dgnzj_j_num1[2] = tx_dgnzj_j_num1[2] + tx_dgnzj[0][i][1]
        if float(tx_dgnzj[0][i][2]) > 24 and float(tx_dgnzj[0][i][2]) <= 36:
            tx_dgnzj_b_num1[3] = tx_dgnzj_b_num1[3] + 1
            tx_dgnzj_j_num1[3] = tx_dgnzj_j_num1[3] + tx_dgnzj[0][i][1]
        if float(tx_dgnzj[0][i][2]) > 36 and float(tx_dgnzj[0][i][2]) <= 48:
            tx_dgnzj_b_num1[4] = tx_dgnzj_b_num1[4] + 1
            tx_dgnzj_j_num1[4] = tx_dgnzj_j_num1[4] + tx_dgnzj[0][i][1]
        if float(tx_dgnzj[0][i][2]) > 48 and float(tx_dgnzj[0][i][2]) <= 72:
            tx_dgnzj_b_num1[5] = tx_dgnzj_b_num1[5] + 1
            tx_dgnzj_j_num1[5] = tx_dgnzj_j_num1[5] + tx_dgnzj[0][i][1]
        if float(tx_dgnzj[0][i][2]) > 72 and float(tx_dgnzj[0][i][2]) <= 96:
            tx_dgnzj_b_num1[6] = tx_dgnzj_b_num1[6] + 1
            tx_dgnzj_j_num1[6] = tx_dgnzj_j_num1[6] + tx_dgnzj[0][i][1]
        if float(tx_dgnzj[0][i][2]) > 96:
            tx_dgnzj_b_num1[7] = tx_dgnzj_b_num1[7] + 1
            tx_dgnzj_j_num1[7] = tx_dgnzj_j_num1[7] + tx_dgnzj[0][i][1]

    for i in range(len(tx_dsj[0])):
        if float(tx_dsj[0][i][2]) > 0 and float(tx_dsj[0][i][2]) <= 6:
            tx_dsj_b_num1[0] = tx_dsj_b_num1[0] + 1
            tx_dsj_j_num1[0] = tx_dsj_j_num1[0] + tx_dsj[0][i][1]
        if float(tx_dsj[0][i][2]) > 6 and float(tx_dsj[0][i][2]) <= 12:
            tx_dsj_b_num1[1] = tx_dsj_b_num1[1] + 1
            tx_dsj_j_num1[1] = tx_dsj_j_num1[1] + tx_dsj[0][i][1]
        if float(tx_dsj[0][i][2]) > 12 and float(tx_dsj[0][i][2]) <= 24:
            tx_dsj_b_num1[2] = tx_dsj_b_num1[2] + 1
            tx_dsj_j_num1[2] = tx_dsj_j_num1[2] + tx_dsj[0][i][1]
        if float(tx_dsj[0][i][2]) > 24 and float(tx_dsj[0][i][2]) <= 36:
            tx_dsj_b_num1[3] = tx_dsj_b_num1[3] + 1
            tx_dsj_j_num1[3] = tx_dsj_j_num1[3] + tx_dsj[0][i][1]
        if float(tx_dsj[0][i][2]) > 36 and float(tx_dsj[0][i][2]) <= 48:
            tx_dsj_b_num1[4] = tx_dsj_b_num1[4] + 1
            tx_dsj_j_num1[4] = tx_dsj_j_num1[4] + tx_dsj[0][i][1]
        if float(tx_dsj[0][i][2]) > 48 and float(tx_dsj[0][i][2]) <= 72:
            tx_dsj_b_num1[5] = tx_dsj_b_num1[5] + 1
            tx_dsj_j_num1[5] = tx_dsj_j_num1[5] + tx_dsj[0][i][1]
        if float(tx_dsj[0][i][2]) > 72 and float(tx_dsj[0][i][2]) <= 96:
            tx_dsj_b_num1[6] = tx_dsj_b_num1[6] + 1
            tx_dsj_j_num1[6] = tx_dsj_j_num1[6] + tx_dsj[0][i][1]
        if float(tx_dsj[0][i][2]) > 96:
            tx_dsj_b_num1[7] = tx_dsj_b_num1[7] + 1
            tx_dsj_j_num1[7] = tx_dsj_j_num1[7] + tx_dsj[0][i][1]

    for i in range(len(tx_sjz[0])):
        if float(tx_sjz[0][i][2]) > 0 and float(tx_sjz[0][i][2]) <= 6:
            tx_sjz_b_num1[0] = tx_sjz_b_num1[0] + 1
            tx_sjz_j_num1[0] = tx_sjz_j_num1[0] + tx_sjz[0][i][1]
        if float(tx_sjz[0][i][2]) > 6 and float(tx_sjz[0][i][2]) <= 12:
            tx_sjz_b_num1[1] = tx_sjz_b_num1[1] + 1
            tx_sjz_j_num1[1] = tx_sjz_j_num1[1] + tx_sjz[0][i][1]
        if float(tx_sjz[0][i][2]) > 12 and float(tx_sjz[0][i][2]) <= 24:
            tx_sjz_b_num1[2] = tx_sjz_b_num1[2] + 1
            tx_sjz_j_num1[2] = tx_sjz_j_num1[2] + tx_sjz[0][i][1]
        if float(tx_sjz[0][i][2]) > 24 and float(tx_sjz[0][i][2]) <= 36:
            tx_sjz_b_num1[3] = tx_sjz_b_num1[3] + 1
            tx_sjz_j_num1[3] = tx_sjz_j_num1[3] + tx_sjz[0][i][1]
        if float(tx_sjz[0][i][2]) > 36 and float(tx_sjz[0][i][2]) <= 48:
            tx_sjz_b_num1[4] = tx_sjz_b_num1[4] + 1
            tx_sjz_j_num1[4] = tx_sjz_j_num1[4] + tx_sjz[0][i][1]
        if float(tx_sjz[0][i][2]) > 48 and float(tx_sjz[0][i][2]) <= 72:
            tx_sjz_b_num1[5] = tx_sjz_b_num1[5] + 1
            tx_sjz_j_num1[5] = tx_sjz_j_num1[5] + tx_sjz[0][i][1]
        if float(tx_sjz[0][i][2]) > 72 and float(tx_sjz[0][i][2]) <= 96:
            tx_sjz_b_num1[6] = tx_sjz_b_num1[6] + 1
            tx_sjz_j_num1[6] = tx_sjz_j_num1[6] + tx_sjz[0][i][1]
        if float(tx_sjz[0][i][2]) > 96:
            tx_sjz_b_num1[7] = tx_sjz_b_num1[7] + 1
            tx_sjz_j_num1[7] = tx_sjz_j_num1[7] + tx_sjz[0][i][1]

    hm_b_num_6 = np.r_[
        hm_drk_b_num1[0], hm_dtm_b_num1[0], hm_dgnzj_b_num1[0], hm_dsj_b_num1[0], hm_sjz_b_num1[0]]
    hm_b_num_12 = np.r_[
        hm_drk_b_num1[1], hm_dtm_b_num1[1], hm_dgnzj_b_num1[1], hm_dsj_b_num1[1], hm_sjz_b_num1[1]]
    hm_b_num_24 = np.r_[
        hm_drk_b_num1[2], hm_dtm_b_num1[2], hm_dgnzj_b_num1[2], hm_dsj_b_num1[2], hm_sjz_b_num1[2]]
    hm_b_num_36 = np.r_[
        hm_drk_b_num1[3], hm_dtm_b_num1[3], hm_dgnzj_b_num1[3], hm_dsj_b_num1[3], hm_sjz_b_num1[3]]
    hm_b_num_48 = np.r_[
        hm_drk_b_num1[4], hm_dtm_b_num1[4], hm_dgnzj_b_num1[4], hm_dsj_b_num1[4], hm_sjz_b_num1[4]]
    hm_b_num_72 = np.r_[
        hm_drk_b_num1[5], hm_dtm_b_num1[5], hm_dgnzj_b_num1[5], hm_dsj_b_num1[5], hm_sjz_b_num1[5]]
    hm_b_num_96 = np.r_[
        hm_drk_b_num1[6], hm_dtm_b_num1[6], hm_dgnzj_b_num1[6], hm_dsj_b_num1[6], hm_sjz_b_num1[6]]
    hm_b_num_96_ = np.r_[
        hm_drk_b_num1[7], hm_dtm_b_num1[7], hm_dgnzj_b_num1[7], hm_dsj_b_num1[7], hm_sjz_b_num1[7]]
    hm_j_num_6 = np.r_[
        hm_drk_j_num1[0], hm_dtm_j_num1[0], hm_dgnzj_j_num1[0], hm_dsj_j_num1[0], hm_sjz_j_num1[0]]
    hm_j_num_12 = np.r_[
        hm_drk_j_num1[1], hm_dtm_j_num1[1], hm_dgnzj_j_num1[1], hm_dsj_j_num1[1], hm_sjz_j_num1[1]]
    hm_j_num_24 = np.r_[
        hm_drk_j_num1[2], hm_dtm_j_num1[2], hm_dgnzj_j_num1[2], hm_dsj_j_num1[2], hm_sjz_j_num1[2]]
    hm_j_num_36 = np.r_[
        hm_drk_j_num1[3], hm_dtm_j_num1[3], hm_dgnzj_j_num1[3], hm_dsj_j_num1[3], hm_sjz_j_num1[3]]
    hm_j_num_48 = np.r_[
        hm_drk_j_num1[4], hm_dtm_j_num1[4], hm_dgnzj_j_num1[4], hm_dsj_j_num1[4], hm_sjz_j_num1[4]]
    hm_j_num_72 = np.r_[
        hm_drk_j_num1[5], hm_dtm_j_num1[5], hm_dgnzj_j_num1[5], hm_dsj_j_num1[5], hm_sjz_j_num1[5]]
    hm_j_num_96 = np.r_[
        hm_drk_j_num1[6], hm_dtm_j_num1[6], hm_dgnzj_j_num1[6], hm_dsj_j_num1[6], hm_sjz_j_num1[6]]
    hm_j_num_96_ = np.r_[
        hm_drk_j_num1[7], hm_dtm_j_num1[7], hm_dgnzj_j_num1[7], hm_dsj_j_num1[7], hm_sjz_j_num1[7]]
    tx_b_num_6 = np.r_[
        tx_drk_b_num1[0], tx_dtm_b_num1[0], tx_dgnzj_b_num1[0], tx_dsj_b_num1[0], tx_sjz_b_num1[0]]
    tx_b_num_12 = np.r_[
        tx_drk_b_num1[1], tx_dtm_b_num1[1], tx_dgnzj_b_num1[1], tx_dsj_b_num1[1], tx_sjz_b_num1[1]]
    tx_b_num_24 = np.r_[
        tx_drk_b_num1[2], tx_dtm_b_num1[2], tx_dgnzj_b_num1[2], tx_dsj_b_num1[2], tx_sjz_b_num1[2]]
    tx_b_num_36 = np.r_[
        tx_drk_b_num1[3], tx_dtm_b_num1[3], tx_dgnzj_b_num1[3], tx_dsj_b_num1[3], tx_sjz_b_num1[3]]
    tx_b_num_48 = np.r_[
        tx_drk_b_num1[4], tx_dtm_b_num1[4], tx_dgnzj_b_num1[4], tx_dsj_b_num1[4], tx_sjz_b_num1[4]]
    tx_b_num_72 = np.r_[
        tx_drk_b_num1[5], tx_dtm_b_num1[5], tx_dgnzj_b_num1[5], tx_dsj_b_num1[5], tx_sjz_b_num1[5]]
    tx_b_num_96 = np.r_[
        tx_drk_b_num1[6], tx_dtm_b_num1[6], tx_dgnzj_b_num1[6], tx_dsj_b_num1[6], tx_sjz_b_num1[6]]
    tx_b_num_96_ = np.r_[
        tx_drk_b_num1[7], tx_dtm_b_num1[7], tx_dgnzj_b_num1[7], tx_dsj_b_num1[7], tx_sjz_b_num1[7]]
    tx_j_num_6 = np.r_[
        tx_drk_j_num1[0], tx_dtm_j_num1[0], tx_dgnzj_j_num1[0], tx_dsj_j_num1[0], tx_sjz_j_num1[0]]
    tx_j_num_12 = np.r_[
        tx_drk_j_num1[1], tx_dtm_j_num1[1], tx_dgnzj_j_num1[1], tx_dsj_j_num1[1], tx_sjz_j_num1[1]]
    tx_j_num_24 = np.r_[
        tx_drk_j_num1[2], tx_dtm_j_num1[2], tx_dgnzj_j_num1[2], tx_dsj_j_num1[2], tx_sjz_j_num1[2]]
    tx_j_num_36 = np.r_[
        tx_drk_j_num1[3], tx_dtm_j_num1[3], tx_dgnzj_j_num1[3], tx_dsj_j_num1[3], tx_sjz_j_num1[3]]
    tx_j_num_48 = np.r_[
        tx_drk_j_num1[4], tx_dtm_j_num1[4], tx_dgnzj_j_num1[4], tx_dsj_j_num1[4], tx_sjz_j_num1[4]]
    tx_j_num_72 = np.r_[
        tx_drk_j_num1[5], tx_dtm_j_num1[5], tx_dgnzj_j_num1[5], tx_dsj_j_num1[5], tx_sjz_j_num1[5]]
    tx_j_num_96 = np.r_[
        tx_drk_j_num1[6], tx_dtm_j_num1[6], tx_dgnzj_j_num1[6], tx_dsj_j_num1[6], tx_sjz_j_num1[6]]
    tx_j_num_96_ = np.r_[
        tx_drk_j_num1[7], tx_dtm_j_num1[7], tx_dgnzj_j_num1[7], tx_dsj_j_num1[7], tx_sjz_j_num1[7]]

    hm_b_p_6 = []
    hm_b_p_12 = []
    hm_b_p_24 = []
    hm_b_p_36 = []
    hm_b_p_48 = []
    hm_b_p_72 = []
    hm_b_p_96 = []
    hm_b_p_96_ = []

    hm_j_p_6 = []
    hm_j_p_12 = []
    hm_j_p_24 = []
    hm_j_p_36 = []
    hm_j_p_48 = []
    hm_j_p_72 = []
    hm_j_p_96 = []
    hm_j_p_96_ = []

    tx_b_p_6 = []
    tx_b_p_12 = []
    tx_b_p_24 = []
    tx_b_p_36 = []
    tx_b_p_48 = []
    tx_b_p_72 = []
    tx_b_p_96 = []
    tx_b_p_96_ = []

    tx_j_p_6 = []
    tx_j_p_12 = []
    tx_j_p_24 = []
    tx_j_p_36 = []
    tx_j_p_48 = []
    tx_j_p_72 = []
    tx_j_p_96 = []
    tx_j_p_96_ = []

    arrayA = np.divide(hm_b_num_6, max(hm_b_num_6), out=np.zeros_like(hm_b_num_6, dtype=np.float64), casting="unsafe",
                       where=max(hm_b_num_6) != 0)
    for i in range(len(hm_b_num_6)):
        hm_b_p_6.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_p_6[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_p_6)):
            hm_b_p_6[i] = '{:.2%}'.format(a)

    arrayA = np.divide(hm_b_num_12, max(hm_b_num_12), out=np.zeros_like(hm_b_num_12, dtype=np.float64),
                       casting="unsafe", where=max(hm_b_num_12) != 0)
    for i in range(len(hm_b_num_12)):
        hm_b_p_12.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_p_12[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_p_12)):
            hm_b_p_12[i] = '{:.2%}'.format(a)

    arrayA = np.divide(hm_b_num_24, max(hm_b_num_24), out=np.zeros_like(hm_b_num_24, dtype=np.float64),
                       casting="unsafe", where=max(hm_b_num_24) != 0)
    for i in range(len(hm_b_num_24)):
        hm_b_p_24.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_p_24[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_p_24)):
            hm_b_p_24[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_b_num_36, max(hm_b_num_36), out=np.zeros_like(hm_b_num_36, dtype=np.float64),
                       casting="unsafe", where=max(hm_b_num_36) != 0)
    for i in range(len(hm_b_num_36)):
        hm_b_p_36.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_p_36[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_p_36)):
            hm_b_p_36[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_b_num_48, max(hm_b_num_48), out=np.zeros_like(hm_b_num_48, dtype=np.float64),
                       casting="unsafe", where=max(hm_b_num_48) != 0)
    for i in range(len(hm_b_num_48)):
        hm_b_p_48.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_p_48[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_p_48)):
            hm_b_p_48[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_b_num_72, max(hm_b_num_72), out=np.zeros_like(hm_b_num_72, dtype=np.float64),
                       casting="unsafe", where=max(hm_b_num_72) != 0)
    for i in range(len(hm_b_num_72)):
        hm_b_p_72.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_p_72[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_p_72)):
            hm_b_p_72[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_b_num_96, max(hm_b_num_96), out=np.zeros_like(hm_b_num_96, dtype=np.float64),
                       casting="unsafe", where=max(hm_b_num_96) != 0)
    for i in range(len(hm_b_num_96)):
        hm_b_p_96.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_p_96[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_p_96)):
            hm_b_p_96[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_b_num_96_, max(hm_b_num_96_), out=np.zeros_like(hm_b_num_96_, dtype=np.float64),
                       casting="unsafe", where=max(hm_b_num_96_) != 0)
    for i in range(len(hm_b_num_96_)):
        hm_b_p_96_.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_p_96_[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_p_96_)):
            hm_b_p_96_[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_j_num_6, max(hm_j_num_6), out=np.zeros_like(hm_j_num_6, dtype=np.float64),
                       casting="unsafe", where=max(hm_j_num_6) != 0)
    for i in range(len(hm_j_num_6)):
        hm_j_p_6.append("%.2f%%" % (arrayA[i] * 100))
    if hm_j_p_6[0] == 'nan%':
        a = 0
        for i in range(len(hm_j_p_6)):
            hm_j_p_6[i] = '{:.2%}'.format(a)

    arrayA = np.divide(hm_j_num_12, max(hm_j_num_12), out=np.zeros_like(hm_j_num_12, dtype=np.float64),
                       casting="unsafe", where=max(hm_j_num_12) != 0)
    for i in range(len(hm_j_num_12)):
        hm_j_p_12.append("%.2f%%" % (arrayA[i] * 100))
    if hm_j_p_12[0] == 'nan%':
        a = 0
        for i in range(len(hm_j_p_12)):
            hm_j_p_12[i] = '{:.2%}'.format(a)

    arrayA = np.divide(hm_j_num_24, max(hm_j_num_24), out=np.zeros_like(hm_j_num_24, dtype=np.float64),
                       casting="unsafe", where=max(hm_j_num_24) != 0)
    for i in range(len(hm_j_num_24)):
        hm_j_p_24.append("%.2f%%" % (arrayA[i] * 100))
    if hm_j_p_24[0] == 'nan%':
        a = 0
        for i in range(len(hm_j_p_24)):
            hm_j_p_24[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_j_num_36, max(hm_j_num_36), out=np.zeros_like(hm_j_num_36, dtype=np.float64),
                       casting="unsafe", where=max(hm_j_num_36) != 0)
    for i in range(len(hm_j_num_36)):
        hm_j_p_36.append("%.2f%%" % (arrayA[i] * 100))
    if hm_j_p_36[0] == 'nan%':
        a = 0
        for i in range(len(hm_j_p_36)):
            hm_j_p_36[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_j_num_48, max(hm_j_num_48), out=np.zeros_like(hm_j_num_48, dtype=np.float64),
                       casting="unsafe", where=max(hm_j_num_48) != 0)
    for i in range(len(hm_j_num_48)):
        hm_j_p_48.append("%.2f%%" % (arrayA[i] * 100))
    if hm_j_p_48[0] == 'nan%':
        a = 0
        for i in range(len(hm_j_p_48)):
            hm_j_p_48[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_j_num_72, max(hm_j_num_72), out=np.zeros_like(hm_j_num_72, dtype=np.float64),
                       casting="unsafe", where=max(hm_j_num_72) != 0)
    for i in range(len(hm_j_num_72)):
        hm_j_p_72.append("%.2f%%" % (arrayA[i] * 100))
    if hm_j_p_72[0] == 'nan%':
        a = 0
        for i in range(len(hm_j_p_72)):
            hm_j_p_72[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_j_num_96, max(hm_j_num_96), out=np.zeros_like(hm_j_num_96, dtype=np.float64),
                       casting="unsafe", where=max(hm_j_num_96) != 0)
    for i in range(len(hm_j_num_96)):
        hm_j_p_96.append("%.2f%%" % (arrayA[i] * 100))
    if hm_j_p_96[0] == 'nan%':
        a = 0
        for i in range(len(hm_j_p_96)):
            hm_j_p_96[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_j_num_96_, max(hm_j_num_96_), out=np.zeros_like(hm_j_num_96_, dtype=np.float64),
                       casting="unsafe", where=max(hm_j_num_96_) != 0)
    for i in range(len(hm_j_num_96_)):
        hm_j_p_96_.append("%.2f%%" % (arrayA[i] * 100))
    if hm_j_p_96_[0] == 'nan%':
        a = 0
        for i in range(len(hm_j_p_96_)):
            hm_j_p_96_[i] = '{:.2%}'.format(a)

    arrayA = np.divide(tx_b_num_6, max(tx_b_num_6), out=np.zeros_like(tx_b_num_6, dtype=np.float64), casting="unsafe",
                       where=max(tx_b_num_6) != 0)
    for i in range(len(tx_b_num_6)):
        tx_b_p_6.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_p_6[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_p_6)):
            tx_b_p_6[i] = '{:.2%}'.format(a)

    arrayA = np.divide(tx_b_num_12, max(tx_b_num_12), out=np.zeros_like(tx_b_num_12, dtype=np.float64),
                       casting="unsafe", where=max(tx_b_num_12) != 0)
    for i in range(len(tx_b_num_12)):
        tx_b_p_12.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_p_12[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_p_12)):
            tx_b_p_12[i] = '{:.2%}'.format(a)

    arrayA = np.divide(tx_b_num_24, max(tx_b_num_24), out=np.zeros_like(tx_b_num_24, dtype=np.float64),
                       casting="unsafe", where=max(tx_b_num_24) != 0)
    for i in range(len(tx_b_num_24)):
        tx_b_p_24.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_p_24[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_p_24)):
            tx_b_p_24[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_b_num_36, max(tx_b_num_36), out=np.zeros_like(tx_b_num_36, dtype=np.float64),
                       casting="unsafe", where=max(tx_b_num_36) != 0)
    for i in range(len(tx_b_num_36)):
        tx_b_p_36.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_p_36[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_p_36)):
            tx_b_p_36[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_b_num_48, max(tx_b_num_48), out=np.zeros_like(tx_b_num_48, dtype=np.float64),
                       casting="unsafe", where=max(tx_b_num_48) != 0)
    for i in range(len(tx_b_num_48)):
        tx_b_p_48.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_p_48[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_p_48)):
            tx_b_p_48[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_b_num_72, max(tx_b_num_72), out=np.zeros_like(tx_b_num_72, dtype=np.float64),
                       casting="unsafe", where=max(tx_b_num_72) != 0)
    for i in range(len(tx_b_num_72)):
        tx_b_p_72.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_p_72[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_p_72)):
            tx_b_p_72[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_b_num_96, max(tx_b_num_96), out=np.zeros_like(tx_b_num_96, dtype=np.float64),
                       casting="unsafe", where=max(tx_b_num_96) != 0)
    for i in range(len(tx_b_num_96)):
        tx_b_p_96.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_p_96[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_p_96)):
            tx_b_p_96[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_b_num_96_, max(tx_b_num_96_), out=np.zeros_like(tx_b_num_96_, dtype=np.float64),
                       casting="unsafe", where=max(tx_b_num_96_) != 0)
    for i in range(len(tx_b_num_96_)):
        tx_b_p_96_.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_p_96_[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_p_96_)):
            tx_b_p_96_[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_j_num_6, max(tx_j_num_6), out=np.zeros_like(tx_j_num_6, dtype=np.float64),
                       casting="unsafe", where=max(tx_j_num_6) != 0)
    for i in range(len(tx_j_num_6)):
        tx_j_p_6.append("%.2f%%" % (arrayA[i] * 100))
    if tx_j_p_6[0] == 'nan%':
        a = 0
        for i in range(len(tx_j_p_6)):
            tx_j_p_6[i] = '{:.2%}'.format(a)

    arrayA = np.divide(tx_j_num_12, max(tx_j_num_12), out=np.zeros_like(tx_j_num_12, dtype=np.float64),
                       casting="unsafe", where=max(tx_j_num_12) != 0)
    for i in range(len(tx_j_num_12)):
        tx_j_p_12.append("%.2f%%" % (arrayA[i] * 100))
    if tx_j_p_12[0] == 'nan%':
        a = 0
        for i in range(len(tx_j_p_12)):
            tx_j_p_12[i] = '{:.2%}'.format(a)

    arrayA = np.divide(tx_j_num_24, max(tx_j_num_24), out=np.zeros_like(tx_j_num_24, dtype=np.float64),
                       casting="unsafe", where=max(tx_j_num_24) != 0)
    for i in range(len(tx_j_num_24)):
        tx_j_p_24.append("%.2f%%" % (arrayA[i] * 100))
    if tx_j_p_24[0] == 'nan%':
        a = 0
        for i in range(len(tx_j_p_24)):
            tx_j_p_24[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_j_num_36, max(tx_j_num_36), out=np.zeros_like(tx_j_num_36, dtype=np.float64),
                       casting="unsafe", where=max(tx_j_num_36) != 0)
    for i in range(len(tx_j_num_36)):
        tx_j_p_36.append("%.2f%%" % (arrayA[i] * 100))
    if tx_j_p_36[0] == 'nan%':
        a = 0
        for i in range(len(tx_j_p_36)):
            tx_j_p_36[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_j_num_48, max(tx_j_num_48), out=np.zeros_like(tx_j_num_48, dtype=np.float64),
                       casting="unsafe", where=max(tx_j_num_48) != 0)
    for i in range(len(tx_j_num_48)):
        tx_j_p_48.append("%.2f%%" % (arrayA[i] * 100))
    if tx_j_p_48[0] == 'nan%':
        a = 0
        for i in range(len(tx_j_p_48)):
            tx_j_p_48[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_j_num_72, max(tx_j_num_72), out=np.zeros_like(tx_j_num_72, dtype=np.float64),
                       casting="unsafe", where=max(tx_j_num_72) != 0)
    for i in range(len(tx_j_num_72)):
        tx_j_p_72.append("%.2f%%" % (arrayA[i] * 100))
    if tx_j_p_72[0] == 'nan%':
        a = 0
        for i in range(len(tx_j_p_72)):
            tx_j_p_72[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_j_num_96, max(tx_j_num_96), out=np.zeros_like(tx_j_num_96, dtype=np.float64),
                       casting="unsafe", where=max(tx_j_num_96) != 0)
    for i in range(len(tx_j_num_96)):
        tx_j_p_96.append("%.2f%%" % (arrayA[i] * 100))
    if tx_j_p_96[0] == 'nan%':
        a = 0
        for i in range(len(tx_j_p_96)):
            tx_j_p_96[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_j_num_96_, max(tx_j_num_96_), out=np.zeros_like(tx_j_num_96_, dtype=np.float64),
                       casting="unsafe", where=max(tx_j_num_96_) != 0)
    for i in range(len(tx_j_num_96_)):
        tx_j_p_96_.append("%.2f%%" % (arrayA[i] * 100))
    if tx_j_p_96_[0] == 'nan%':
        a = 0
        for i in range(len(tx_j_p_96_)):
            tx_j_p_96_[i] = '{:.2%}'.format(a)


    jsonData['tx_xb_b_2'] = tx_xb_b_2
    jsonData['tx_xb_b_4'] = tx_xb_b_4
    jsonData['tx_xb_b_6'] = tx_xb_b_6
    jsonData['tx_xb_b_8'] = tx_xb_b_8
    jsonData['tx_xb_b_10'] = tx_xb_b_10
    jsonData['tx_xb_b_12'] = tx_xb_b_12
    jsonData['tx_xb_b_24'] = tx_xb_b_24
    jsonData['tx_xb_b_24_'] = tx_xb_b_24_
    jsonData['hm_xb_b_2'] = hm_xb_b_2
    jsonData['hm_xb_b_4'] = hm_xb_b_4
    jsonData['hm_xb_b_6'] = hm_xb_b_6
    jsonData['hm_xb_b_8'] = hm_xb_b_8
    jsonData['hm_xb_b_10'] = hm_xb_b_10
    jsonData['hm_xb_b_12'] = hm_xb_b_12
    jsonData['hm_xb_b_24'] = hm_xb_b_24
    jsonData['hm_xb_b_24_'] = hm_xb_b_24_

    jsonData['hm_j_12'] = hm_j_12
    jsonData['hm_j_24'] = hm_j_24
    jsonData['hm_j_48'] = hm_j_48
    jsonData['hm_j_72'] = hm_j_72
    jsonData['hm_j_120'] = hm_j_120
    jsonData['hm_j_240'] = hm_j_240
    jsonData['hm_j_360'] = hm_j_360
    jsonData['hm_j_361'] = hm_j_361
    jsonData['tx_j_12'] = tx_j_12
    jsonData['tx_j_24'] = tx_j_24
    jsonData['tx_j_48'] = tx_j_48
    jsonData['tx_j_72'] = tx_j_72
    jsonData['tx_j_120'] = tx_j_120
    jsonData['tx_j_240'] = tx_j_240
    jsonData['tx_j_360'] = tx_j_360
    jsonData['tx_j_361'] = tx_j_361
    jsonData['hm_b_12'] = hm_b_12
    jsonData['hm_b_24'] = hm_b_24
    jsonData['hm_b_48'] = hm_b_48
    jsonData['hm_b_72'] = hm_b_72
    jsonData['hm_b_120'] = hm_b_120
    jsonData['hm_b_240'] = hm_b_240
    jsonData['hm_b_360'] = hm_b_360
    jsonData['hm_b_361'] = hm_b_361
    jsonData['tx_b_12'] = tx_b_12
    jsonData['tx_b_24'] = tx_b_24
    jsonData['tx_b_48'] = tx_b_48
    jsonData['tx_b_72'] = tx_b_72
    jsonData['tx_b_120'] = tx_b_120
    jsonData['tx_b_240'] = tx_b_240
    jsonData['tx_b_360'] = tx_b_360
    jsonData['tx_b_361'] = tx_b_361
    jsonData['hm_b_xb_num_2'] = hm_b_xb_num_2.tolist()
    jsonData['hm_b_xb_num_4'] = hm_b_xb_num_4.tolist()
    jsonData['hm_b_xb_num_6'] = hm_b_xb_num_6.tolist()
    jsonData['hm_b_xb_num_8'] = hm_b_xb_num_8.tolist()
    jsonData['hm_b_xb_num_10'] = hm_b_xb_num_10.tolist()
    jsonData['hm_b_xb_num_12'] = hm_b_xb_num_12.tolist()
    jsonData['hm_b_xb_num_24'] = hm_b_xb_num_24.tolist()
    jsonData['hm_b_xb_num_24_'] = hm_b_xb_num_24_.tolist()
    jsonData['tx_b_xb_num_2'] = tx_b_xb_num_2.tolist()
    jsonData['tx_b_xb_num_4'] = tx_b_xb_num_4.tolist()
    jsonData['tx_b_xb_num_6'] = tx_b_xb_num_6.tolist()
    jsonData['tx_b_xb_num_8'] = tx_b_xb_num_8.tolist()
    jsonData['tx_b_xb_num_10'] = tx_b_xb_num_10.tolist()
    jsonData['tx_b_xb_num_12'] = tx_b_xb_num_12.tolist()
    jsonData['tx_b_xb_num_24'] = tx_b_xb_num_24.tolist()
    jsonData['tx_b_xb_num_24_'] = tx_b_xb_num_24_.tolist()
    jsonData['hm_b_fba_num_12'] = hm_b_fba_num_12.tolist()
    jsonData['hm_b_fba_num_24'] = hm_b_fba_num_24.tolist()
    jsonData['hm_b_fba_num_48'] = hm_b_fba_num_48.tolist()
    jsonData['hm_b_fba_num_72'] = hm_b_fba_num_72.tolist()
    jsonData['hm_b_fba_num_120'] = hm_b_fba_num_120.tolist()
    jsonData['hm_b_fba_num_240'] = hm_b_fba_num_240.tolist()
    jsonData['hm_b_fba_num_360'] = hm_b_fba_num_360.tolist()
    jsonData['hm_b_fba_num_361'] = hm_b_fba_num_361.tolist()
    jsonData['tx_b_fba_num_12'] = tx_b_fba_num_12.tolist()
    jsonData['tx_b_fba_num_24'] = tx_b_fba_num_24.tolist()
    jsonData['tx_b_fba_num_48'] = tx_b_fba_num_48.tolist()
    jsonData['tx_b_fba_num_72'] = tx_b_fba_num_72.tolist()
    jsonData['tx_b_fba_num_120'] = tx_b_fba_num_120.tolist()
    jsonData['tx_b_fba_num_240'] = tx_b_fba_num_240.tolist()
    jsonData['tx_b_fba_num_360'] = tx_b_fba_num_360.tolist()
    jsonData['tx_b_fba_num_361'] = tx_b_fba_num_361.tolist()
    jsonData['hm_j_fba_num_12'] = hm_j_fba_num_12.tolist()
    jsonData['hm_j_fba_num_24'] = hm_j_fba_num_24.tolist()
    jsonData['hm_j_fba_num_48'] = hm_j_fba_num_48.tolist()
    jsonData['hm_j_fba_num_72'] = hm_j_fba_num_72.tolist()
    jsonData['hm_j_fba_num_120'] = hm_j_fba_num_120.tolist()
    jsonData['hm_j_fba_num_240'] = hm_j_fba_num_240.tolist()
    jsonData['hm_j_fba_num_360'] = hm_j_fba_num_360.tolist()
    jsonData['hm_j_fba_num_361'] = hm_j_fba_num_361.tolist()
    jsonData['tx_j_fba_num_12'] = tx_j_fba_num_12.tolist()
    jsonData['tx_j_fba_num_24'] = tx_j_fba_num_24.tolist()
    jsonData['tx_j_fba_num_48'] = tx_j_fba_num_48.tolist()
    jsonData['tx_j_fba_num_72'] = tx_j_fba_num_72.tolist()
    jsonData['tx_j_fba_num_120'] = tx_j_fba_num_120.tolist()
    jsonData['tx_j_fba_num_240'] = tx_j_fba_num_240.tolist()
    jsonData['tx_j_fba_num_360'] = tx_j_fba_num_360.tolist()
    jsonData['tx_j_fba_num_361'] = tx_j_fba_num_361.tolist()

    jsonData['hm_drk_b_num1'] = hm_drk_b_num1
    jsonData['hm_drk_j_num1'] = hm_drk_j_num1

    jsonData['hm_dtm_b_num1'] = hm_dtm_b_num1
    jsonData['hm_dtm_j_num1'] = hm_dtm_j_num1

    jsonData['hm_dgnzj_b_num1'] = hm_dgnzj_b_num1
    jsonData['hm_dgnzj_j_num1'] = hm_dgnzj_j_num1

    jsonData['hm_dsj_b_num1'] = hm_dsj_b_num1
    jsonData['hm_dsj_j_num1'] = hm_dsj_j_num1

    jsonData['hm_sjz_b_num1'] = hm_sjz_b_num1
    jsonData['hm_sjz_j_num1'] = hm_sjz_j_num1

    jsonData['tx_drk_b_num1'] = tx_drk_b_num1
    jsonData['tx_drk_j_num1'] = tx_drk_j_num1

    jsonData['tx_dtm_b_num1'] = tx_dtm_b_num1
    jsonData['tx_dtm_j_num1'] = tx_dtm_j_num1

    jsonData['tx_dgnzj_b_num1'] = tx_dgnzj_b_num1
    jsonData['tx_dgnzj_j_num1'] = tx_dgnzj_j_num1

    jsonData['tx_dsj_b_num1'] = tx_dsj_b_num1
    jsonData['tx_dsj_j_num1'] = tx_dsj_j_num1

    jsonData['tx_sjz_b_num1'] = tx_sjz_b_num1
    jsonData['tx_sjz_j_num1'] = tx_sjz_j_num1

    jsonData['hm_b_p_6'] = hm_b_p_6
    jsonData['hm_b_p_12'] = hm_b_p_12
    jsonData['hm_b_p_24'] = hm_b_p_24
    jsonData['hm_b_p_36'] = hm_b_p_36
    jsonData['hm_b_p_48'] = hm_b_p_48
    jsonData['hm_b_p_72'] = hm_b_p_72
    jsonData['hm_b_p_96'] = hm_b_p_96
    jsonData['hm_b_p_96_'] = hm_b_p_96_

    jsonData['hm_j_p_6'] = hm_j_p_6
    jsonData['hm_j_p_12'] = hm_j_p_12
    jsonData['hm_j_p_24'] = hm_j_p_24
    jsonData['hm_j_p_36'] = hm_j_p_36
    jsonData['hm_j_p_48'] = hm_j_p_48
    jsonData['hm_j_p_72'] = hm_j_p_72
    jsonData['hm_j_p_96'] = hm_j_p_96
    jsonData['hm_j_p_96_'] = hm_j_p_96_

    jsonData['tx_b_p_6'] = tx_b_p_6
    jsonData['tx_b_p_12'] = tx_b_p_12
    jsonData['tx_b_p_24'] = tx_b_p_24
    jsonData['tx_b_p_36'] = tx_b_p_36
    jsonData['tx_b_p_48'] = tx_b_p_48
    jsonData['tx_b_p_72'] = tx_b_p_72
    jsonData['tx_b_p_96'] = tx_b_p_96
    jsonData['tx_b_p_96_'] = tx_b_p_96_

    jsonData['tx_j_p_6'] = tx_j_p_6
    jsonData['tx_j_p_12'] = tx_j_p_12
    jsonData['tx_j_p_24'] = tx_j_p_24
    jsonData['tx_j_p_36'] = tx_j_p_36
    jsonData['tx_j_p_48'] = tx_j_p_48
    jsonData['tx_j_p_72'] = tx_j_p_72
    jsonData['tx_j_p_96'] = tx_j_p_96
    jsonData['tx_j_p_96_'] = tx_j_p_96_

    jsonData['tx_drk_shelf'] = tx_drk_shelf
    jsonData['tx_dtm_shelf'] = tx_dtm_shelf
    jsonData['tx_dgnzj_shelf'] = tx_dgnzj_shelf
    jsonData['tx_dsj_shelf'] = tx_dsj_shelf
    jsonData['tx_sjz_shelf'] = tx_sjz_shelf

    jsonData['hm_drk_shelf'] = hm_drk_shelf

    jsonData['hm_dtm_shelf'] = hm_dtm_shelf
    jsonData['hm_dgnzj_shelf'] = hm_dgnzj_shelf
    jsonData['hm_dsj_shelf'] = hm_dsj_shelf
    jsonData['hm_sjz_shelf'] = hm_sjz_shelf
    jsonData['tx_drk_shelf_time'] = tx_drk_shelf_time
    jsonData['tx_dtm_shelf_time'] = tx_dtm_shelf_time
    jsonData['tx_dgnzj_shelf_time'] = tx_dgnzj_shelf_time
    jsonData['tx_dsj_shelf_time'] = tx_dsj_shelf_time
    jsonData['tx_sjz_shelf_time'] = tx_sjz_shelf_time

    jsonData['hm_drk_shelf_time'] = hm_drk_shelf_time
    jsonData['hm_dtm_shelf_time'] = hm_dtm_shelf_time
    jsonData['hm_dgnzj_shelf_time'] = hm_dgnzj_shelf_time
    jsonData['hm_dsj_shelf_time'] = hm_dsj_shelf_time
    jsonData['hm_sjz_shelf_time'] = hm_sjz_shelf_time

    jsonData['tx_drk_shelf_num1'] = tx_drk_shelf_num1
    jsonData['tx_dtm_shelf_num1'] = tx_dtm_shelf_num1
    jsonData['tx_dgnzj_shelf_num1'] = tx_dgnzj_shelf_num1
    jsonData['tx_dsj_shelf_num1'] = tx_dsj_shelf_num1
    jsonData['tx_sjz_shelf_num1'] = tx_sjz_shelf_num1
    jsonData['hm_drk_shelf_num1'] = hm_drk_shelf_num1
    jsonData['hm_dtm_shelf_num1'] = hm_dtm_shelf_num1
    jsonData['hm_dgnzj_shelf_num1'] = hm_dgnzj_shelf_num1
    jsonData['hm_dsj_shelf_num1'] = hm_dsj_shelf_num1
    jsonData['hm_sjz_shelf_num1'] = hm_sjz_shelf_num1

    j = json.dumps(jsonData, cls=DecimalEncoder)
    return (j)


# 首页
@app.route('/test3', methods=['POST'])
def index_jy():
    input = pd.read_excel('daily1_jy.xlsx')
    see_jy=save(input)
    input = pd.read_excel('daily1_zl.xlsx')
    see_zl=save(input)
    input = pd.read_excel('daily1_sx.xlsx')
    see_sx=save(input)
    input = pd.read_excel('daily1_rk.xlsx')
    see_rk=save(input)
    input = pd.read_excel('daily1_tph.xlsx')
    see_tph=save(input)
    input = pd.read_excel('daily1_ry.xlsx')
    see_ry=save(input)
    input = pd.read_excel('daily1_ry2.xlsx')
    see_ry2=save(input)
    input = pd.read_excel('daily1_zt.xlsx')
    see_zt=save(input)
    input = pd.read_excel('daily1_dcl.xlsx')
    see_dcl=save(input)
    input = pd.read_excel('daily1_db.xlsx')
    see_db=save(input)
    input = pd.read_excel('daily1_dcl2.xlsx')
    see_dcl2=save(input)
    # print('----dcl2推送成功----')
    dcl2_in = []
    dcl2_out = []
    dcl2_fba = []
    for data_dcl2 in see_dcl2:
        dcl2_in.append(data_dcl2[4])
        dcl2_out.append(data_dcl2[3])
        dcl2_fba.append(data_dcl2[2])

    dcl2_in.append(sum(dcl2_in[0:2]))
    dcl2_in.append(sum(dcl2_in[3:5]))
    dcl2_out.append(sum(dcl2_out[0:2]))
    dcl2_out.append(sum(dcl2_out[3:5]))
    dcl2_fba.append(sum(dcl2_fba[0:2]))
    dcl2_fba.append(sum(dcl2_fba[0:3]))
    dcl2_fba.append(sum(dcl2_fba[3:5]))
    dcl2_fba.append(sum(dcl2_fba[3:6]))

    db_in = []
    db_out = []
    db_total = []
    db_date = []
    for data_db in see_db:
        db_in.append(data_db[2])
        db_out.append(data_db[3])
        db_total.append(data_db[4])
        db_date.append(data_db[0])
    db_date = db_date[0:7]
    db_in.append(max(db_in[0:7] + db_out[0:7]) + 100)
    db_in.append(max(db_in[7:15] + db_out[7:15]) + 100)
    db_in.append(max(db_total[0:7]) + 100)
    db_in.append(max(db_total[7:15]) + 100)

    dcl_1 = []
    dcl_2 = []
    dcl_3 = []
    dcl_4 = []
    for data_dcl in see_dcl:
        dcl_1.append(round(data_dcl[3], 2))
        dcl_2.append(round(data_dcl[4], 2))
        dcl_3.append(round(data_dcl[5], 2))
        dcl_4.append(round(data_dcl[6], 2))

    zt_warehouse = []
    zt_date = []
    zt_1 = []
    zt_2 = []
    zt_3 = []
    zt_4 = []
    zt_5 = []
    for data_zt in see_zt:
        zt_warehouse.append(data_zt[0])
        zt_date.append(data_zt[1])
        zt_1.append(data_zt[2])
        zt_2.append(data_zt[3])
        zt_3.append(data_zt[4])
        zt_4.append(data_zt[5])
        zt_5.append(data_zt[6])
    zt_1.append(max(zt_1[0:4]) + max(zt_2[0:4]) + max(zt_4[0:4]) + 40000)
    zt_1.append(max(zt_1[5:9]) + max(zt_2[5:9]) + max(zt_4[5:9]) + 40000)
    zt_1.append(max(zt_3[0:4]) + 10000)
    zt_1.append(max(zt_3[5:9]) + 10000)
    print(zt_1)
    print(zt_4)


    ry_warehouse = []
    ry_date = []
    ry_1 = []
    ry_2 = []
    ry_3 = []
    ry_4 = []
    ry_5 = []
    ry_6 = []
    ry_7 = []
    ry_8 = []
    ry_9 = []
    ry_10 = []
    ry_11 = []
    ry_12 = []
    ry_13 = []
    ry_14 = []

    for data_ry in see_ry:
        ry_warehouse.append(data_ry[0])
        ry_date.append(data_ry[1])
        ry_1.append(data_ry[2])
        ry_2.append(data_ry[3])
        ry_3.append(data_ry[4])
        ry_4.append(data_ry[5])
        ry_5.append(data_ry[6])
        ry_6.append(data_ry[7])
        ry_7.append(data_ry[8])
        ry_8.append(data_ry[9])
        ry_9.append(data_ry[10])
        ry_10.append(data_ry[11])
        ry_11.append(data_ry[12])
        ry_12.append(data_ry[13])


    for data_ry in see_ry2:
        ry_13.append(data_ry[4])
        ry_14.append(data_ry[5])
    if ry_13:
        print('1')
    else:
        ry_13 = [0, 0, 0, 0]

    if ry_14:
        print('1')
    else:
        ry_14 = [0, 0, 0, 0]

    ##需语句修正
    hm_total = []
    tx_total = []
    hm_change = []
    tx_change = []
    hm_total.append(float(ry_1[1]))
    hm_total.append(float(ry_1[0]))
    hm_total.append(float(ry_3[0] + ry_3[1]))
    hm_total.append(float(ry_5[0] + ry_5[1]))
    hm_total.append(float(ry_7[0] + ry_7[1]))
    hm_total.append(float(ry_9[0] + ry_9[1]))
    print(hm_total[5])
    print(hm_total[2])
    try:
       hm_total.append(round(hm_total[5] / hm_total[2], 2))
    except ZeroDivisionError:
       hm_total.append(0)


    hm_total.append(float(ry_13[0] + ry_13[1]))
    hm_total.append(float(ry_14[0] + ry_14[1]))

    tx_total.append(float(ry_1[2]))
    tx_total.append(float(ry_1[3]))
    tx_total.append(float(ry_3[3] + ry_3[2]))
    tx_total.append(float(ry_5[3] + ry_5[2]))
    tx_total.append(float(ry_7[3] + ry_7[2]))
    tx_total.append(float(ry_9[3] + ry_9[2]))
    try:
       tx_total.append(round(tx_total[5] / tx_total[2], 2))
    except ZeroDivisionError:
       tx_total.append(0)
    tx_total.append(float(ry_13[2] + ry_13[3]))
    tx_total.append(float(ry_14[2] + ry_14[3]))

    hm_change.append(float(ry_2[1]))
    hm_change.append(float(ry_2[0]))
    hm_change.append(float(ry_4[0]) + float(ry_4[1]))
    hm_change.append(float(ry_6[0]) + float(ry_6[1]))
    hm_change.append(round(float(ry_8[0]) + float(ry_8[1]), 0))
    hm_change.append(round(float(ry_10[0]) + float(ry_10[1]), 0))
    try:
     hm_change.append(
        round(float(hm_total[6]) - ((float(ry_12[0]) + float(ry_12[1])) / (float(ry_11[0]) + float(ry_11[1]))), 2))
    except ZeroDivisionError:
     hm_change.append(0)
    tx_change.append(float(ry_2[3]))
    tx_change.append(float(ry_2[2]))
    tx_change.append(float(ry_4[3]) + float(ry_4[2]))
    tx_change.append(float(ry_6[3]) + float(ry_6[2]))
    tx_change.append(round(float(ry_8[3]) + float(ry_8[2]), 0))
    tx_change.append(round(float(ry_10[3]) + float(ry_10[2]), 0))
    try:
     tx_change.append(
        round(tx_total[6] - ((float(ry_12[3]) + float(ry_12[2])) / (float(ry_11[3]) + float(ry_11[2]))), 2))
    except ZeroDivisionError:
        tx_change.append(0)
    warehouse_tph = []
    tph_date = []
    tph = []
    uph = []
    for data_tph in see_tph:
        tph_date.append(data_tph[0])
        warehouse_tph.append(data_tph[1])
        tph.append(data_tph[2])
        uph.append(data_tph[3])
    hm_tph_date = []
    hm_tph = []
    hm_uph = []
    tx_tph_date = []
    tx_tph = []
    tx_uph = []
    for i in range(len(warehouse_tph)):
        if warehouse_tph[i] == 'HM_AA':
            hm_tph_date.append(tph_date[i])
            hm_tph.append(tph[i])
            hm_uph.append(uph[i])
    for i in range(len(warehouse_tph)):
        if warehouse_tph[i] == 'SZ_AA':
            tx_tph_date.append(tph_date[i])
            tx_tph.append(tph[i])
            tx_uph.append(uph[i])
    a = round(max(hm_tph), 0) + 10
    b = round(min(hm_uph), 0) - 10
    hm_tph.append(a)
    hm_tph.append(b)
    a = round(max(tx_tph), 0) + 10
    b = round(min(tx_uph), 0) - 10
    hm_uph.append(a)
    hm_uph.append(b)

    warehouse_jy = []
    num_jy = []
    type_jy = []
    for data_jy in see_jy:
        warehouse_jy.append(data_jy[0])
        num_jy.append(data_jy[1])
        type_jy.append(data_jy[2])

    warehouse_zl = []
    cost_zl = []
    time_zl = []
    jsonData = {}
    for data_zl in see_zl:
        warehouse_zl.append(data_zl[0])
        cost_zl.append(data_zl[1])
        time_zl.append(data_zl[2])

    warehouse_sx = []
    type_sx = []
    time_sx = []
    date_sx = []

    for data_sx in see_sx:
        date_sx.append(data_sx[0])
        warehouse_sx.append(data_sx[1])
        type_sx.append(data_sx[2])
        time_sx.append(data_sx[3])

    warehouse_rk = []
    type_rk = []
    num_rk = []

    for data_rk in see_rk:
        warehouse_rk.append(data_rk[0])
        type_rk.append(data_rk[2])
        num_rk.append(data_rk[3])

    hm_rk_in = []
    hm_rk_out = []
    hm_rk_ld = []
    tx_rk_in = []
    tx_rk_out = []
    tx_rk_ld = []

    for i in range(len(warehouse_rk)):
        if warehouse_rk[i] == 'HM_AA' and type_rk[i] == 'in':
            hm_rk_in.append(num_rk[i])
    for i in range(len(warehouse_rk)):
        if warehouse_rk[i] == 'HM_AA' and type_rk[i] == 'out':
            hm_rk_out.append(num_rk[i])
    for i in range(len(warehouse_rk)):
        if warehouse_rk[i] == 'HM_AA' and type_rk[i] == 'LD':
            hm_rk_ld.append(num_rk[i])
    for i in range(len(warehouse_rk)):
        if warehouse_rk[i] == 'SZ_AA' and type_rk[i] == 'in':
            tx_rk_in.append(num_rk[i])
    for i in range(len(warehouse_rk)):
        if warehouse_rk[i] == 'SZ_AA' and type_rk[i] == 'out':
            tx_rk_out.append(num_rk[i])
    for i in range(len(warehouse_rk)):
        if warehouse_rk[i] == 'SZ_AA' and type_rk[i] == 'LD':
            tx_rk_ld.append(num_rk[i])

    hm_sx_date = []
    tx_sx_date = []
    hm_sx_in = []
    hm_sx_out = []
    hm_sx_fba = []
    tx_sx_in = []
    tx_sx_out = []
    tx_sx_fba = []
    for i in range(len(warehouse_sx)):
        if warehouse_sx[i] == 'HM_AA' and type_sx[i] == 'in':
            hm_sx_date.append(date_sx[i])

    for i in range(len(warehouse_sx)):
        if warehouse_sx[i] == 'HM_AA' and type_sx[i] == 'in':
            hm_sx_in.append(time_sx[i])
    for i in range(len(warehouse_sx)):
        if warehouse_sx[i] == 'HM_AA' and type_sx[i] == 'out':
            hm_sx_out.append(time_sx[i])
    for i in range(len(warehouse_sx)):
        if warehouse_sx[i] == 'HM_AA' and type_sx[i] == 'FBA':
            hm_sx_fba.append(time_sx[i])

    for i in range(len(warehouse_sx)):
        if warehouse_sx[i] == 'SZ_AA' and type_sx[i] == 'in':
            tx_sx_date.append(date_sx[i])
    for i in range(len(warehouse_sx)):
        if warehouse_sx[i] == 'SZ_AA' and type_sx[i] == 'in':
            tx_sx_in.append(time_sx[i])
    for i in range(len(warehouse_sx)):
        if warehouse_sx[i] == 'SZ_AA' and type_sx[i] == 'out':
            tx_sx_out.append(time_sx[i])
    for i in range(len(warehouse_sx)):
        if warehouse_sx[i] == 'SZ_AA' and type_sx[i] == 'FBA':
            tx_sx_fba.append(time_sx[i])

    num_jy_hm = []
    type_jy_hm = []
    num_jy_tx = []
    type_jy_tx = []
    for i in range(len(warehouse_jy)):
        if warehouse_jy[i] == 'HM_AA':
            num_jy_hm.append(num_jy[i])
            type_jy_hm.append(type_jy[i])
    for i in range(len(warehouse_jy)):
        if warehouse_jy[i] == 'SZ_AA':
            num_jy_tx.append(num_jy[i])
            type_jy_tx.append(type_jy[i])

    hm_zl_cost = []
    hm_zl_time = []
    tx_zl_cost = []
    tx_zl_time = []

    for i in range(len(warehouse_zl)):
        if warehouse_zl[i] == "HM_AA":
            hm_zl_cost.append(cost_zl[i])
            hm_zl_time.append(time_zl[i])
    for i in range(len(warehouse_zl)):
        if warehouse_zl[i] == "SZ_AA":
            tx_zl_cost.append(cost_zl[i])
            tx_zl_time.append(time_zl[i])

    hm_jy_data = np.dstack((num_jy_hm, type_jy_hm))
    tx_jy_data = np.dstack((num_jy_tx, type_jy_tx))

    hm_jy_DLD_num = [0]
    hm_jy_DCK_num = [0]
    hm_jy_DDB_num = [0]
    hm_jy_DGNZJ_num = [0]
    hm_jy_DJH_num = [0]
    hm_jy_DRK_num = [0]
    hm_jy_DSJ_num = [0]
    hm_jy_DTM_num = [0]
    hm_jy_FDCK_num = [0]
    hm_jy_FDDB_num = [0]
    hm_jy_FDJH_num = [0]
    hm_jy_FDJY_num = [0]
    hm_jy_FJHZ_num = [0]
    hm_jy_FDLD_num = [0]
    hm_jy_DBDRK_num = [0]
    hm_jy_DBRKZ_num = [0]
    hm_jy_DBDLD_num = [0]
    hm_jy_DBDJH_num = [0]
    hm_jy_DBDDB_num = [0]
    hm_jy_DBDCK_num = [0]
    hm_jy_DBDJY_num = [0]
    hm_jy_DPK_num = [0]
    hm_jy_FDPK_num = [0]
    hm_jy_FDFPLD_num = [0]
    tx_jy_FDFPLD_num = [0]

    tx_jy_DPK_num = [0]
    tx_jy_FDPK_num = [0]
    tx_jy_DBDRK_num = [0]
    tx_jy_DBRKZ_num = [0]
    tx_jy_DBDLD_num = [0]
    tx_jy_DBDJH_num = [0]
    tx_jy_DBDDB_num = [0]
    tx_jy_DBDCK_num = [0]
    tx_jy_DBDJY_num = [0]
    tx_jy_DLD_num = [0]
    tx_jy_DCK_num = [0]
    tx_jy_DDB_num = [0]
    tx_jy_DGNZJ_num = [0]
    tx_jy_DJH_num = [0]
    tx_jy_DRK_num = [0]
    tx_jy_DSJ_num = [0]
    tx_jy_DTM_num = [0]
    tx_jy_FDCK_num = [0]
    tx_jy_FDDB_num = [0]
    tx_jy_FDJH_num = [0]
    tx_jy_FDJY_num = [0]
    tx_jy_FJHZ_num = [0]
    tx_jy_FDLD_num = [0]

    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DCK':
            hm_jy_DCK_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DLD':
            hm_jy_DLD_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DDB':
            hm_jy_DDB_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DGNZJ':
            hm_jy_DGNZJ_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DRK':
            hm_jy_DRK_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DSJ':
            hm_jy_DSJ_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DTM':
            hm_jy_DTM_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'FDCK':
            hm_jy_FDCK_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'FDDB':
            hm_jy_FDDB_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'FDJH':
            hm_jy_FDJH_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'FDJY':
            hm_jy_FDJY_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'FJHZ':
            hm_jy_FJHZ_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'FDLD':
            hm_jy_FDLD_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DJH':
            hm_jy_DJH_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DBDRK':
            hm_jy_DBDRK_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DBRKZ':
            hm_jy_DBRKZ_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DBDLD':
            hm_jy_DBDLD_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DBDJH':
            hm_jy_DBDJH_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DBDDB':
            hm_jy_DBDDB_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DBDCK':
            hm_jy_DBDCK_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DBDJY':
            hm_jy_DBDJY_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DPK':
            hm_jy_DPK_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'FDPK':
            hm_jy_FDPK_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'FDFPLD':
            hm_jy_FDFPLD_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'FDFPLD':
            tx_jy_FDFPLD_num[0] = (tx_jy_data[0][i][0])

    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DPK':
            tx_jy_DPK_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'FDPK':
            tx_jy_FDPK_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DLD':
            tx_jy_DLD_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DCK':
            tx_jy_DCK_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DDB':
            tx_jy_DDB_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DGNZJ':
            tx_jy_DGNZJ_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DRK':
            tx_jy_DRK_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DSJ':
            tx_jy_DSJ_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DTM':
            tx_jy_DTM_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'FDCK':
            tx_jy_FDCK_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'FDDB':
            tx_jy_FDDB_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'FDJH':
            tx_jy_FDJH_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'FDJY':
            tx_jy_FDJY_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'FJHZ':
            tx_jy_FJHZ_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'FDLD':
            tx_jy_FDLD_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DJH':
            tx_jy_DJH_num[0] = tx_jy_data[0][i][0]
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DBDRK':
            tx_jy_DBDRK_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DBRKZ':
            tx_jy_DBRKZ_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DBDLD':
            tx_jy_DBDLD_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DBDJH':
            tx_jy_DBDJH_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DBDDB':
            tx_jy_DBDDB_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DBDCK':
            tx_jy_DBDCK_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DBDJY':
            tx_jy_DBDJY_num[0] = (tx_jy_data[0][i][0])
    hm_jy_XB_totoal = []
    hm_jy_FB_totoal = []
    tx_jy_XB_totoal = []
    tx_jy_FB_totoal = []
    hm_jy_DB_totoal = []
    tx_jy_DB_totoal = []

    hm_jy_XB_totoal.append(float(hm_jy_DCK_num[0]))
    hm_jy_XB_totoal.append(float(hm_jy_DDB_num[0]))
    hm_jy_XB_totoal.append(float(hm_jy_DJH_num[0]))
    hm_jy_XB_totoal.append(float(hm_jy_DLD_num[0]))
    hm_jy_XB_totoal.append(float(hm_jy_DPK_num[0]))
    hm_jy_XB_totoal.append(float(hm_jy_DSJ_num[0]))
    hm_jy_XB_totoal.append(float(hm_jy_DTM_num[0]))
    hm_jy_XB_totoal.append(float(hm_jy_DGNZJ_num[0]))
    hm_jy_XB_totoal.append(float(hm_jy_DRK_num[0]))

    hm_jy_DB_totoal.append(float(hm_jy_DBDJY_num[0]))
    hm_jy_DB_totoal.append(float(hm_jy_DBDCK_num[0]))
    hm_jy_DB_totoal.append(float(hm_jy_DBDDB_num[0]))
    hm_jy_DB_totoal.append(float(hm_jy_DBDJH_num[0]))
    hm_jy_DB_totoal.append(float(hm_jy_DBDLD_num[0]))
    hm_jy_DB_totoal.append(float(hm_jy_DBRKZ_num[0]))
    hm_jy_DB_totoal.append(float(hm_jy_DBDRK_num[0]))

    tx_jy_DB_totoal.append(float(tx_jy_DBDJY_num[0]))
    tx_jy_DB_totoal.append(float(tx_jy_DBDCK_num[0]))
    tx_jy_DB_totoal.append(float(tx_jy_DBDDB_num[0]))
    tx_jy_DB_totoal.append(float(tx_jy_DBDJH_num[0]))
    tx_jy_DB_totoal.append(float(tx_jy_DBDLD_num[0]))
    tx_jy_DB_totoal.append(float(tx_jy_DBRKZ_num[0]))
    tx_jy_DB_totoal.append(float(tx_jy_DBDRK_num[0]))

    tx_jy_XB_totoal.append(float(tx_jy_DCK_num[0]))
    tx_jy_XB_totoal.append(float(tx_jy_DDB_num[0]))
    tx_jy_XB_totoal.append(float(tx_jy_DJH_num[0]))
    tx_jy_XB_totoal.append(float(tx_jy_DLD_num[0]))
    tx_jy_XB_totoal.append(float(tx_jy_DPK_num[0]))
    tx_jy_XB_totoal.append(float(tx_jy_DSJ_num[0]))
    tx_jy_XB_totoal.append(float(tx_jy_DTM_num[0]))
    tx_jy_XB_totoal.append(float(tx_jy_DGNZJ_num[0]))
    tx_jy_XB_totoal.append(float(tx_jy_DRK_num[0]))

    hm_jy_FB_totoal.append(float(hm_jy_FDJY_num[0]))
    hm_jy_FB_totoal.append(float(hm_jy_FDCK_num[0]))
    hm_jy_FB_totoal.append(float(hm_jy_FDDB_num[0]))
    hm_jy_FB_totoal.append(float(hm_jy_FJHZ_num[0]))
    hm_jy_FB_totoal.append(float(hm_jy_FDJH_num[0]))
    hm_jy_FB_totoal.append(float(hm_jy_FDLD_num[0]))
    hm_jy_FB_totoal.append(float(hm_jy_FDFPLD_num[0]))
    hm_jy_FB_totoal.append(float(hm_jy_FDPK_num[0]))

    tx_jy_FB_totoal.append(float(tx_jy_FDJY_num[0]))
    tx_jy_FB_totoal.append(float(tx_jy_FDCK_num[0]))
    tx_jy_FB_totoal.append(float(tx_jy_FDDB_num[0]))
    tx_jy_FB_totoal.append(float(tx_jy_FJHZ_num[0]))
    tx_jy_FB_totoal.append(float(tx_jy_FDJH_num[0]))
    tx_jy_FB_totoal.append(float(tx_jy_FDLD_num[0]))
    tx_jy_FB_totoal.append(float(tx_jy_FDFPLD_num[0]))
    tx_jy_FB_totoal.append(float(tx_jy_FDPK_num[0]))

    hm_jy_XB_totoal_color = []
    hm_jy_FB_totoal_color = []
    hm_jy_DB_totoal_color = []
    tx_jy_XB_totoal_color = []
    tx_jy_FB_totoal_color = []
    tx_jy_DB_totoal_color = []
    for i in range(len(hm_jy_XB_totoal)):
        hm_jy_XB_totoal_color.append('{:.2%}'.format(hm_jy_XB_totoal[i] / max(hm_jy_XB_totoal)))
    if hm_jy_XB_totoal_color[0] == 'nan%':
        a = 0
        for i in range(len(hm_jy_XB_totoal)):
            hm_jy_XB_totoal_color[i] = '{:.2%}'.format(a)
    for i in range(len(hm_jy_FB_totoal)):
        hm_jy_FB_totoal_color.append('{:.2%}'.format(hm_jy_FB_totoal[i] / max(hm_jy_FB_totoal)))
    if hm_jy_FB_totoal_color[0] == 'nan%':
        a = 0
        for i in range(len(hm_jy_FB_totoal)):
            hm_jy_FB_totoal_color[i] = '{:.2%}'.format(a)
    for i in range(len(hm_jy_DB_totoal)):
        hm_jy_DB_totoal_color.append('{:.2%}'.format(hm_jy_DB_totoal[i] / max(hm_jy_DB_totoal)))
    if hm_jy_DB_totoal_color[0] == 'nan%':
        a = 0
        for i in range(len(hm_jy_DB_totoal)):
            hm_jy_DB_totoal_color[i] = '{:.2%}'.format(a)
    for i in range(len(tx_jy_XB_totoal)):
        tx_jy_XB_totoal_color.append('{:.2%}'.format(tx_jy_XB_totoal[i] / max(tx_jy_XB_totoal)))
    if tx_jy_XB_totoal_color[0] == 'nan%':
        a = 0
        for i in range(len(tx_jy_XB_totoal)):
            tx_jy_XB_totoal_color[i] = '{:.2%}'.format(a)
    for i in range(len(tx_jy_FB_totoal)):
        tx_jy_FB_totoal_color.append('{:.2%}'.format(tx_jy_FB_totoal[i] / max(tx_jy_FB_totoal)))
    if tx_jy_FB_totoal_color[0] == 'nan%':
        a = 0
        for i in range(len(tx_jy_FB_totoal)):
            tx_jy_FB_totoal_color[i] = '{:.2%}'.format(a)
    for i in range(len(tx_jy_DB_totoal)):
        tx_jy_DB_totoal_color.append('{:.2%}'.format(tx_jy_DB_totoal[i] / max(tx_jy_DB_totoal)))
    if tx_jy_DB_totoal_color[0] == 'nan%':
        a = 0
        for i in range(len(tx_jy_DB_totoal)):
            tx_jy_DB_totoal_color[i] = '{:.2%}'.format(a)

    jsonData['dcl2_in'] = dcl2_in
    jsonData['dcl2_out'] = dcl2_out
    jsonData['dcl2_fba'] = dcl2_fba

    jsonData['db_in'] = db_in
    jsonData['db_out'] = db_out
    jsonData['db_total'] = db_total
    jsonData['db_date'] = db_date
    jsonData['dcl_1'] = dcl_1
    jsonData['dcl_2'] = dcl_2
    jsonData['dcl_3'] = dcl_3
    jsonData['dcl_4'] = dcl_4
    jsonData['zt_date'] = zt_date
    jsonData['zt_1'] = zt_1
    jsonData['zt_2'] = zt_2
    jsonData['zt_3'] = zt_3
    jsonData['zt_4'] = zt_4
    jsonData['zt_5'] = zt_5

    jsonData['hm_change'] = hm_change
    jsonData['tx_change'] = tx_change
    jsonData['hm_total'] = hm_total
    jsonData['tx_total'] = tx_total
    jsonData['hm_jy_XB_totoal'] = hm_jy_XB_totoal
    jsonData['hm_jy_FB_totoal'] = hm_jy_FB_totoal
    jsonData['tx_jy_XB_totoal'] = tx_jy_XB_totoal
    jsonData['tx_jy_FB_totoal'] = tx_jy_FB_totoal
    jsonData['hm_jy_DB_totoal'] = hm_jy_DB_totoal
    jsonData['tx_jy_DB_totoal'] = tx_jy_DB_totoal
    jsonData['hm_jy_XB_totoal_color'] = hm_jy_XB_totoal_color
    jsonData['hm_jy_FB_totoal_color'] = hm_jy_FB_totoal_color
    jsonData['hm_jy_DB_totoal_color'] = hm_jy_DB_totoal_color
    jsonData['tx_jy_XB_totoal_color'] = tx_jy_XB_totoal_color
    jsonData['tx_jy_FB_totoal_color'] = tx_jy_FB_totoal_color
    jsonData['tx_jy_DB_totoal_color'] = tx_jy_DB_totoal_color
    jsonData['hm_zl_cost'] = hm_zl_cost
    jsonData['hm_zl_time'] = hm_zl_time
    jsonData['tx_zl_cost'] = tx_zl_cost
    jsonData['tx_zl_time'] = tx_zl_time

    jsonData['tx_sx_date'] = tx_sx_date
    jsonData['hm_sx_date'] = hm_sx_date
    jsonData['hm_sx_in'] = hm_sx_in
    jsonData['hm_sx_out'] = hm_sx_out
    jsonData['hm_sx_fba'] = hm_sx_fba
    jsonData['tx_sx_in'] = tx_sx_in
    jsonData['tx_sx_out'] = tx_sx_out
    jsonData['tx_sx_fba'] = tx_sx_fba
    jsonData['hm_rk_in'] = hm_rk_in
    jsonData['hm_rk_out'] = hm_rk_out
    jsonData['hm_rk_ld'] = hm_rk_ld
    jsonData['tx_rk_in'] = tx_rk_in
    jsonData['tx_rk_out'] = tx_rk_out
    jsonData['tx_rk_ld'] = tx_rk_ld
    jsonData['hm_tph_date'] = hm_tph_date
    jsonData['hm_tph'] = hm_tph
    jsonData['hm_uph'] = hm_uph
    jsonData['tx_tph_date'] = tx_tph_date
    jsonData['tx_tph'] = tx_tph
    jsonData['tx_uph'] = tx_uph
    j = json.dumps(jsonData, cls=DecimalEncoder)

    return (j)


##入库异常监控页面
@app.route('/test4', methods=['POST'])
def montor2():
    input = pd.read_excel('test4.xlsx')
    see=save(input)
    warehouse = []
    num = []
    photo = []
    status = []
    s = []
    jsonData = {}
    for data in see:
        warehouse.append(data[0])
        num.append(data[4])
        photo.append(data[5])
        status.append(data[6])
        s.append(data[7])
    hm_num = []
    hm_photo = []
    hm_status = []
    hm_s = []
    tx_num = []
    tx_photo = []
    tx_status = []
    tx_s = []

    for i in range(len(warehouse)):
        if warehouse[i] == 'HM_AA':
            hm_num.append(num[i])
            hm_photo.append(photo[i])
            hm_status.append(status[i])
            hm_s.append(s[i])
    for i in range(len(warehouse)):
        if warehouse[i] == 'SZ_AA':
            tx_num.append(num[i])
            tx_photo.append(photo[i])
            tx_status.append(status[i])
            tx_s.append(s[i])

    hm_data = np.dstack((hm_num, hm_photo, hm_status, hm_s))
    tx_data = np.dstack((tx_num, tx_photo, tx_status, tx_s))

    hm_dqr_num = []
    hm_dqr_s = []
    hm_dzkcl_num = []
    hm_dzkcl_s = []
    hm_thdcl_num = []
    hm_thdcl_s = []
    hm_dhq_num = []
    hm_dhq_s = []
    hm_yhq_num = []
    hm_yhq_s = []
    hm_ddcl_num = []
    hm_ddcl_s = []
    hm_ht_num = []
    hm_ht_s = []
    tx_dqr_num = []
    tx_dqr_s = []
    tx_dzkcl_num = []
    tx_dzkcl_s = []
    tx_thdcl_num = []
    tx_thdcl_s = []
    tx_dhq_num = []
    tx_dhq_s = []
    tx_yhq_num = []
    tx_yhq_s = []
    tx_ddcl_num = []
    tx_ddcl_s = []
    tx_ht_num = []
    tx_ht_s = []

    for i in range(len(hm_s)):
        if (hm_data[0][i][2] == 1):
            hm_dqr_num.append(hm_data[0][i][0])
            hm_dqr_s.append(hm_data[0][i][3])
    for i in range(len(hm_s)):
        if (hm_data[0][i][2] == 2 or hm_data[0][i][2] == 7):
            hm_dhq_num.append(hm_data[0][i][0])
            hm_dhq_s.append(hm_data[0][i][3])
    for i in range(len(hm_s)):
        if (hm_data[0][i][2] == 3):
            hm_yhq_num.append(hm_data[0][i][0])
            hm_yhq_s.append(hm_data[0][i][3])
    for i in range(len(hm_s)):
        if (hm_data[0][i][2] == 4):
            hm_dzkcl_num.append(hm_data[0][i][0])
            hm_dzkcl_s.append(hm_data[0][i][3])
    for i in range(len(hm_s)):
        if (hm_data[0][i][2] == 6):
            hm_ddcl_num.append(hm_data[0][i][0])
            hm_ddcl_s.append(hm_data[0][i][3])
    for i in range(len(tx_s)):
        if (tx_data[0][i][2] == 1):
            tx_dqr_num.append(tx_data[0][i][0])
            tx_dqr_s.append(tx_data[0][i][3])
    for i in range(len(tx_s)):
        if (tx_data[0][i][2] == 2 or tx_data[0][i][2] == 7):
            tx_dhq_num.append(tx_data[0][i][0])
            tx_dhq_s.append(tx_data[0][i][3])
    for i in range(len(tx_s)):
        if (tx_data[0][i][2] == 3):
            tx_yhq_num.append(tx_data[0][i][0])
            tx_yhq_s.append(tx_data[0][i][3])
    for i in range(len(tx_s)):
        if (tx_data[0][i][2] == 4):
            tx_dzkcl_num.append(tx_data[0][i][0])
            tx_dzkcl_s.append(tx_data[0][i][3])
    for i in range(len(tx_s)):
        if (tx_data[0][i][2] == 6):
            tx_ddcl_num.append(tx_data[0][i][0])
            tx_ddcl_s.append(tx_data[0][i][3])
    for i in range(len(tx_s)):
        if (tx_data[0][i][2] == 11):
            tx_thdcl_num.append(tx_data[0][i][0])
            tx_thdcl_s.append(tx_data[0][i][3])
    for i in range(len(tx_s)):
        if (tx_data[0][i][1] == 1):
            tx_ht_num.append(tx_data[0][i][0])
            tx_ht_s.append(tx_data[0][i][3])
    for i in range(len(hm_s)):
        if (hm_data[0][i][2] == 11):
            hm_thdcl_num.append(hm_data[0][i][0])
            hm_thdcl_s.append(hm_data[0][i][3])
    for i in range(len(hm_s)):
        if (hm_data[0][i][1] == 1):
            hm_ht_num.append(hm_data[0][i][0])
            hm_ht_s.append(hm_data[0][i][3])

    hm_dqr = np.dstack((hm_dqr_num, hm_dqr_s))
    hm_dzkcl = np.dstack((hm_dzkcl_num, hm_dzkcl_s))
    hm_thdcl = np.dstack((hm_thdcl_num, hm_thdcl_s))
    hm_dhq = np.dstack((hm_dhq_num, hm_dhq_s))
    hm_yhq = np.dstack((hm_yhq_num, hm_yhq_s))
    hm_ddcl = np.dstack((hm_ddcl_num, hm_ddcl_s))
    hm_ht = np.dstack((hm_ht_num, hm_ht_s))
    tx_dqr = np.dstack((tx_dqr_num, tx_dqr_s))
    tx_dzkcl = np.dstack((tx_dzkcl_num, tx_dzkcl_s))
    tx_thdcl = np.dstack((tx_thdcl_num, tx_thdcl_s))
    tx_dhq = np.dstack((tx_dhq_num, tx_dhq_s))
    tx_yhq = np.dstack((tx_yhq_num, tx_yhq_s))
    tx_ddcl = np.dstack((tx_ddcl_num, tx_ddcl_s))
    tx_ht = np.dstack((tx_ht_num, tx_ht_s))

    hm_dqr_num1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    hm_dzkcl_num1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    hm_thdcl_num1 = [0, 0, 0, 0, 0, 0]
    hm_dhq_num1 = [0, 0, 0, 0, 0]
    hm_yhq_num1 = [0, 0, 0, 0, 0]
    hm_ddcl_num1 = [0, 0, 0, 0, 0]
    hm_yhq_15 = [0]
    hm_ddcl_30 = [0]
    tx_yhq_15 = [0]
    tx_ddcl_30 = [0]
    hm_ht_num1 = [0]
    tx_dqr_num1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    tx_dzkcl_num1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    tx_thdcl_num1 = [0, 0, 0, 0, 0, 0]
    tx_dhq_num1 = [0, 0, 0, 0, 0, 0]
    tx_yhq_num1 = [0, 0, 0, 0, 0, 0]
    tx_ddcl_num1 = [0, 0, 0, 0, 0, 0]
    tx_ht_num1 = [0]
    for i in range(len(hm_dqr[0])):
        if float(hm_dqr_s[i]) > 0 and float(hm_dqr_s[i]) <= 4:
            hm_dqr_num1[0] = hm_dqr_num1[0] + hm_dqr[0][i][0]
        if float(hm_dqr_s[i]) > 4 and float(hm_dqr_s[i]) <= 12:
            hm_dqr_num1[1] = hm_dqr_num1[1] + hm_dqr[0][i][0]
        if float(hm_dqr_s[i]) > 12 and float(hm_dqr_s[i]) <= 24:
            hm_dqr_num1[2] = hm_dqr_num1[2] + hm_dqr[0][i][0]
        if float(hm_dqr_s[i]) > 24 and float(hm_dqr_s[i]) <= 36:
            hm_dqr_num1[3] = hm_dqr_num1[3] + hm_dqr[0][i][0]
        if float(hm_dqr_s[i]) > 36 and float(hm_dqr_s[i]) <= 48:
            hm_dqr_num1[4] = hm_dqr_num1[4] + hm_dqr[0][i][0]
        if float(hm_dqr_s[i]) > 48 and float(hm_dqr_s[i]) <= 72:
            hm_dqr_num1[5] = hm_dqr_num1[5] + hm_dqr[0][i][0]
        if float(hm_dqr_s[i]) > 72 and float(hm_dqr_s[i]) <= 96:
            hm_dqr_num1[6] = hm_dqr_num1[6] + hm_dqr[0][i][0]
        if float(hm_dqr_s[i]) > 96 and float(hm_dqr_s[i]) <= 120:
            hm_dqr_num1[7] = hm_dqr_num1[7] + hm_dqr[0][i][0]
        if float(hm_dqr_s[i]) > 120:
            hm_dqr_num1[8] = hm_dqr_num1[8] + hm_dqr[0][i][0]
        hm_dqr_num1[9] = hm_dqr_num1[9] + hm_dqr[0][i][0]
    for i in range(len(hm_dzkcl[0])):
        if float(hm_dzkcl_s[i]) > 0 and float(hm_dzkcl_s[i]) <= 4:
            hm_dzkcl_num1[0] = hm_dzkcl_num1[0] + hm_dzkcl[0][i][0]
        if float(hm_dzkcl_s[i]) > 4 and float(hm_dzkcl_s[i]) <= 12:
            hm_dzkcl_num1[1] = hm_dzkcl_num1[1] + hm_dzkcl[0][i][0]
        if float(hm_dzkcl_s[i]) > 12 and float(hm_dzkcl_s[i]) <= 24:
            hm_dzkcl_num1[2] = hm_dzkcl_num1[2] + hm_dzkcl[0][i][0]
        if float(hm_dzkcl_s[i]) > 24 and float(hm_dzkcl_s[i]) <= 36:
            hm_dzkcl_num1[3] = hm_dzkcl_num1[3] + hm_dzkcl[0][i][0]
        if float(hm_dzkcl_s[i]) > 36 and float(hm_dzkcl_s[i]) <= 48:
            hm_dzkcl_num1[4] = hm_dzkcl_num1[4] + hm_dzkcl[0][i][0]
        if float(hm_dzkcl_s[i]) > 48 and float(hm_dzkcl_s[i]) <= 72:
            hm_dzkcl_num1[5] = hm_dzkcl_num1[5] + hm_dzkcl[0][i][0]
        if float(hm_dzkcl_s[i]) > 72 and float(hm_dzkcl_s[i]) <= 96:
            hm_dzkcl_num1[6] = hm_dzkcl_num1[6] + hm_dzkcl[0][i][0]
        if float(hm_dzkcl_s[i]) > 96 and float(hm_dzkcl_s[i]) <= 120:
            hm_dzkcl_num1[7] = hm_dzkcl_num1[7] + hm_dzkcl[0][i][0]
        if float(hm_dzkcl_s[i]) > 120:
            hm_dzkcl_num1[8] = hm_dzkcl_num1[8] + hm_dzkcl[0][i][0]
        hm_dzkcl_num1[9] = hm_dzkcl_num1[9] + hm_dzkcl[0][i][0]

    for i in range(len(hm_thdcl[0])):
        if float(hm_thdcl_s[i]) > 0 and float(hm_thdcl_s[i]) <= 12:
            hm_thdcl_num1[0] = hm_thdcl_num1[0] + hm_thdcl[0][i][0]
        if float(hm_thdcl_s[i]) > 12 and float(hm_thdcl_s[i]) <= 24:
            hm_thdcl_num1[1] = hm_thdcl_num1[1] + hm_thdcl[0][i][0]
        if float(hm_thdcl_s[i]) > 24 and float(hm_thdcl_s[i]) <= 48:
            hm_thdcl_num1[2] = hm_thdcl_num1[2] + hm_thdcl[0][i][0]
        if float(hm_thdcl_s[i]) > 48 and float(hm_thdcl_s[i]) <= 72:
            hm_thdcl_num1[3] = hm_thdcl_num1[3] + hm_thdcl[0][i][0]
        if float(hm_thdcl_s[i]) > 72:
            hm_thdcl_num1[4] = hm_thdcl_num1[4] + hm_thdcl[0][i][0]
        hm_thdcl_num1[5] = hm_thdcl_num1[5] + hm_thdcl[0][i][0]

    for i in range(len(hm_dhq[0])):
        if float(hm_dhq_s[i]) > 0 and float(hm_dhq_s[i]) <= 24:
            hm_dhq_num1[0] = hm_dhq_num1[0] + hm_dhq[0][i][0]
        if float(hm_dhq_s[i]) > 24 and float(hm_dhq_s[i]) <= 168:
            hm_dhq_num1[1] = hm_dhq_num1[1] + hm_dhq[0][i][0]
        if float(hm_dhq_s[i]) > 168 and float(hm_dhq_s[i]) <= 360:
            hm_dhq_num1[2] = hm_dhq_num1[2] + hm_dhq[0][i][0]
        if float(hm_dhq_s[i]) > 360:
            hm_dhq_num1[3] = hm_dhq_num1[3] + hm_dhq[0][i][0]
        hm_dhq_num1[4] = hm_dhq_num1[4] + hm_dhq[0][i][0]
    for i in range(len(hm_yhq[0])):
        if float(hm_yhq_s[i]) > 0 and float(hm_yhq_s[i]) <= 24:
            hm_yhq_num1[0] = hm_yhq_num1[0] + hm_yhq[0][i][0]
        if float(hm_yhq_s[i]) > 24 and float(hm_yhq_s[i]) <= 168:
            hm_yhq_num1[1] = hm_yhq_num1[1] + hm_yhq[0][i][0]
        if float(hm_yhq_s[i]) > 168 and float(hm_yhq_s[i]) <= 360:
            hm_yhq_num1[2] = hm_yhq_num1[2] + hm_yhq[0][i][0]
        if float(hm_yhq_s[i]) > 360:
            hm_yhq_num1[3] = hm_yhq_num1[3] + hm_yhq[0][i][0]
        hm_yhq_num1[4] = hm_yhq_num1[4] + hm_yhq[0][i][0]
    for i in range(len(hm_ddcl[0])):
        if float(hm_ddcl_s[i]) > 0 and float(hm_ddcl_s[i]) <= 24:
            hm_ddcl_num1[0] = hm_ddcl_num1[0] + hm_ddcl[0][i][0]
        if float(hm_ddcl_s[i]) > 24 and float(hm_ddcl_s[i]) <= 168:
            hm_ddcl_num1[1] = hm_ddcl_num1[1] + hm_ddcl[0][i][0]
        if float(hm_ddcl_s[i]) > 168 and float(hm_ddcl_s[i]) <= 360:
            hm_ddcl_num1[2] = hm_ddcl_num1[2] + hm_ddcl[0][i][0]
        if float(hm_ddcl_s[i]) > 360:
            hm_ddcl_num1[3] = hm_ddcl_num1[3] + hm_ddcl[0][i][0]
        hm_ddcl_num1[4] = hm_ddcl_num1[4] + hm_ddcl[0][i][0]
    for i in range(len(hm_yhq[0])):
        if float(hm_yhq_s[i]) > 360:
            hm_yhq_15[0] = hm_yhq_15[0] + hm_yhq[0][i][0]
    for i in range(len(hm_ddcl[0])):
        if float(hm_ddcl_s[i]) > 360:
            hm_ddcl_30[0] = hm_ddcl_30[0] + hm_ddcl[0][i][0]
    for i in range(len(hm_ht[0])):
        if float(hm_ht_s[i]) > 360:
            hm_ht_num1[0] = hm_ht_num1[0] + hm_ht[0][i][0]

    for i in range(len(tx_dqr[0])):
        if float(tx_dqr_s[i]) > 0 and float(tx_dqr_s[i]) <= 4:
            tx_dqr_num1[0] = tx_dqr_num1[0] + tx_dqr[0][i][0]
        if float(tx_dqr_s[i]) > 4 and float(tx_dqr_s[i]) <= 12:
            tx_dqr_num1[1] = tx_dqr_num1[1] + tx_dqr[0][i][0]
        if float(tx_dqr_s[i]) > 12 and float(tx_dqr_s[i]) <= 24:
            tx_dqr_num1[2] = tx_dqr_num1[2] + tx_dqr[0][i][0]
        if float(tx_dqr_s[i]) > 24 and float(tx_dqr_s[i]) <= 36:
            tx_dqr_num1[3] = tx_dqr_num1[3] + tx_dqr[0][i][0]
        if float(tx_dqr_s[i]) > 36 and float(tx_dqr_s[i]) <= 48:
            tx_dqr_num1[4] = tx_dqr_num1[4] + tx_dqr[0][i][0]
        if float(tx_dqr_s[i]) > 48 and float(tx_dqr_s[i]) <= 72:
            tx_dqr_num1[5] = tx_dqr_num1[5] + tx_dqr[0][i][0]
        if float(tx_dqr_s[i]) > 72 and float(tx_dqr_s[i]) <= 96:
            tx_dqr_num1[6] = tx_dqr_num1[6] + tx_dqr[0][i][0]
        if float(tx_dqr_s[i]) > 96 and float(tx_dqr_s[i]) <= 120:
            tx_dqr_num1[7] = tx_dqr_num1[7] + tx_dqr[0][i][0]
        if float(tx_dqr_s[i]) > 120:
            tx_dqr_num1[8] = tx_dqr_num1[8] + tx_dqr[0][i][0]
        tx_dqr_num1[9] = tx_dqr_num1[9] + tx_dqr[0][i][0]

    for i in range(len(tx_dzkcl[0])):
        if float(tx_dzkcl_s[i]) > 0 and float(tx_dzkcl_s[i]) <= 4:
            tx_dzkcl_num1[0] = tx_dzkcl_num1[0] + tx_dzkcl[0][i][0]
        if float(tx_dzkcl_s[i]) > 4 and float(tx_dzkcl_s[i]) <= 12:
            tx_dzkcl_num1[1] = tx_dzkcl_num1[1] + tx_dzkcl[0][i][0]
        if float(tx_dzkcl_s[i]) > 12 and float(tx_dzkcl_s[i]) <= 24:
            tx_dzkcl_num1[2] = tx_dzkcl_num1[2] + tx_dzkcl[0][i][0]
        if float(tx_dzkcl_s[i]) > 24 and float(tx_dzkcl_s[i]) <= 36:
            tx_dzkcl_num1[3] = tx_dzkcl_num1[3] + tx_dzkcl[0][i][0]
        if float(tx_dzkcl_s[i]) > 36 and float(tx_dzkcl_s[i]) <= 48:
            tx_dzkcl_num1[4] = tx_dzkcl_num1[4] + tx_dzkcl[0][i][0]
        if float(tx_dzkcl_s[i]) > 48 and float(tx_dzkcl_s[i]) <= 72:
            tx_dzkcl_num1[5] = tx_dzkcl_num1[5] + tx_dzkcl[0][i][0]
        if float(tx_dzkcl_s[i]) > 72 and float(tx_dzkcl_s[i]) <= 96:
            tx_dzkcl_num1[6] = tx_dzkcl_num1[6] + tx_dzkcl[0][i][0]
        if float(tx_dzkcl_s[i]) > 96 and float(tx_dzkcl_s[i]) <= 120:
            tx_dzkcl_num1[7] = tx_dzkcl_num1[7] + tx_dzkcl[0][i][0]
        if float(tx_dzkcl_s[i]) > 120:
            tx_dzkcl_num1[8] = tx_dzkcl_num1[8] + tx_dzkcl[0][i][0]
        tx_dzkcl_num1[9] = tx_dzkcl_num1[9] + tx_dzkcl[0][i][0]

    for i in range(len(tx_thdcl[0])):
        if float(tx_thdcl_s[i]) > 0 and float(tx_thdcl_s[i]) <= 12:
            tx_thdcl_num1[0] = tx_thdcl_num1[0] + tx_thdcl[0][i][0]
        if float(tx_thdcl_s[i]) > 12 and float(tx_thdcl_s[i]) <= 24:
            tx_thdcl_num1[1] = tx_thdcl_num1[1] + tx_thdcl[0][i][0]
        if float(tx_thdcl_s[i]) > 24 and float(tx_thdcl_s[i]) <= 48:
            tx_thdcl_num1[2] = tx_thdcl_num1[2] + tx_thdcl[0][i][0]
        if float(tx_thdcl_s[i]) > 48 and float(tx_thdcl_s[i]) <= 72:
            tx_thdcl_num1[3] = tx_thdcl_num1[3] + tx_thdcl[0][i][0]
        if float(tx_thdcl_s[i]) > 72:
            tx_thdcl_num1[4] = tx_thdcl_num1[4] + tx_thdcl[0][i][0]
        tx_thdcl_num1[5] = tx_thdcl_num1[5] + tx_thdcl[0][i][0]

    for i in range(len(tx_dhq[0])):
        if float(tx_dhq_s[i]) > 0 and float(tx_dhq_s[i]) <= 24:
            tx_dhq_num1[0] = tx_dhq_num1[0] + tx_dhq[0][i][0]
        if float(tx_dhq_s[i]) > 24 and float(tx_dhq_s[i]) <= 168:
            tx_dhq_num1[1] = tx_dhq_num1[1] + tx_dhq[0][i][0]
        if float(tx_dhq_s[i]) > 168 and float(tx_dhq_s[i]) <= 360:
            tx_dhq_num1[2] = tx_dhq_num1[2] + tx_dhq[0][i][0]
        if float(tx_dhq_s[i]) > 360:
            tx_dhq_num1[3] = tx_dhq_num1[3] + tx_dhq[0][i][0]
        tx_dhq_num1[4] = tx_dhq_num1[4] + tx_dhq[0][i][0]
    for i in range(len(tx_yhq[0])):
        if float(tx_yhq_s[i]) > 0 and float(tx_yhq_s[i]) <= 24:
            tx_yhq_num1[0] = tx_yhq_num1[0] + tx_yhq[0][i][0]
        if float(tx_yhq_s[i]) > 24 and float(tx_yhq_s[i]) <= 168:
            tx_yhq_num1[1] = tx_yhq_num1[1] + tx_yhq[0][i][0]
        if float(tx_yhq_s[i]) > 168 and float(tx_yhq_s[i]) <= 360:
            tx_yhq_num1[2] = tx_yhq_num1[2] + tx_yhq[0][i][0]
        if float(tx_yhq_s[i]) > 360:
            tx_yhq_num1[3] = tx_yhq_num1[3] + tx_yhq[0][i][0]
        tx_yhq_num1[4] = tx_yhq_num1[4] + tx_yhq[0][i][0]
    for i in range(len(tx_ddcl[0])):
        if float(tx_ddcl_s[i]) > 0 and float(tx_ddcl_s[i]) <= 24:
            tx_ddcl_num1[0] = tx_ddcl_num1[0] + tx_ddcl[0][i][0]
        if float(tx_ddcl_s[i]) > 24 and float(tx_ddcl_s[i]) <= 168:
            tx_ddcl_num1[1] = tx_ddcl_num1[1] + tx_ddcl[0][i][0]
        if float(tx_ddcl_s[i]) > 168 and float(tx_ddcl_s[i]) <= 360:
            tx_ddcl_num1[2] = tx_ddcl_num1[2] + tx_ddcl[0][i][0]
        if float(tx_ddcl_s[i]) > 360:
            tx_ddcl_num1[3] = tx_ddcl_num1[3] + tx_ddcl[0][i][0]
        tx_ddcl_num1[4] = tx_ddcl_num1[4] + tx_ddcl[0][i][0]
    for i in range(len(tx_yhq[0])):
        if float(tx_yhq_s[i]) > 360:
            tx_yhq_15[0] = tx_yhq_15[0] + tx_yhq[0][i][0]
    for i in range(len(tx_ddcl[0])):
        if float(tx_ddcl_s[i]) > 360:
            tx_ddcl_30[0] = tx_ddcl_30[0] + tx_ddcl[0][i][0]
    for i in range(len(tx_ht[0])):
        if float(tx_ht_s[i]) > 360:
            tx_ht_num1[0] = tx_ht_num1[0] + tx_ht[0][i][0]

    hm_dqr_color = []
    hm_dzkcl_color = []
    hm_thdcl_color = []
    hm_dhq_color = []
    hm_yhq_color = []
    hm_ddcl_color = []
    tx_dqr_color = []
    tx_dzkcl_color = []
    tx_thdcl_color = []
    tx_dhq_color = []
    tx_yhq_color = []
    tx_ddcl_color = []
    arrayA = np.divide(hm_dqr_num1, max(hm_dqr_num1), out=np.zeros_like(hm_dqr_num1, dtype=np.float64),
                       where=max(hm_dqr_num1) != 0)
    for i in range(len(hm_dqr_num1)):
        hm_dqr_color.append("%.2f%%" % (arrayA[i] * 100))
    if hm_dqr_num1[0] == 'nan%':
        a = 0
        for i in range(len(hm_dqr_num1)):
            hm_dqr_num1[i] = '{:.2%}'.format(a)

    arrayA = np.divide(hm_dzkcl_num1, max(hm_dzkcl_num1), out=np.zeros_like(hm_dzkcl_num1, dtype=np.float64),
                       where=max(hm_dzkcl_num1) != 0)
    for i in range(len(hm_dzkcl_num1)):
        hm_dzkcl_color.append("%.2f%%" % (arrayA[i] * 100))
    if hm_dzkcl_num1[0] == 'nan%':
        a = 0
        for i in range(len(hm_dzkcl_num1)):
            hm_dzkcl_num1[i] = '{:.2%}'.format(a)

    arrayA = np.divide(hm_thdcl_num1, max(hm_thdcl_num1), out=np.zeros_like(hm_thdcl_num1, dtype=np.float64),
                       where=max(hm_thdcl_num1) != 0)
    for i in range(len(hm_thdcl_num1)):
        hm_thdcl_color.append("%.2f%%" % (arrayA[i] * 100))
    if hm_thdcl_num1[0] == 'nan%':
        a = 0
        for i in range(len(hm_thdcl_num1)):
            hm_thdcl_num1[i] = '{:.2%}'.format(a)

    arrayA = np.divide(hm_dhq_num1, max(hm_dhq_num1), out=np.zeros_like(hm_dhq_num1, dtype=np.float64),
                       where=max(hm_dhq_num1) != 0)
    for i in range(len(hm_dhq_num1)):
        hm_dhq_color.append("%.2f%%" % (arrayA[i] * 100))
    if hm_dhq_num1[0] == 'nan%':
        a = 0
        for i in range(len(hm_dhq_num1)):
            hm_dhq_num1[i] = '{:.2%}'.format(a)

    arrayA = np.divide(hm_yhq_num1, max(hm_yhq_num1), out=np.zeros_like(hm_yhq_num1, dtype=np.float64),
                       where=max(hm_yhq_num1) != 0)
    for i in range(len(hm_yhq_num1)):
        hm_yhq_color.append("%.2f%%" % (arrayA[i] * 100))
    if hm_yhq_num1[0] == 'nan%':
        a = 0
        for i in range(len(hm_yhq_num1)):
            hm_yhq_num1[i] = '{:.2%}'.format(a)

    arrayA = np.divide(hm_ddcl_num1, max(hm_ddcl_num1), out=np.zeros_like(hm_ddcl_num1, dtype=np.float64),
                       where=max(hm_ddcl_num1) != 0)
    for i in range(len(hm_ddcl_num1)):
        hm_ddcl_color.append("%.2f%%" % (arrayA[i] * 100))
    if hm_ddcl_num1[0] == 'nan%':
        a = 0
        for i in range(len(hm_ddcl_num1)):
            hm_ddcl_num1[i] = '{:.2%}'.format(a)

    arrayA = np.divide(tx_dzkcl_num1, max(tx_dzkcl_num1), out=np.zeros_like(tx_dzkcl_num1, dtype=np.float64),
                       where=max(tx_dzkcl_num1) != 0)
    for i in range(len(tx_dzkcl_num1)):
        tx_dzkcl_color.append("%.2f%%" % (arrayA[i] * 100))
    if tx_dzkcl_num1[0] == 'nan%':
        a = 0
        for i in range(len(tx_dzkcl_num1)):
            tx_dzkcl_num1[i] = '{:.2%}'.format(a)

    arrayA = np.divide(tx_thdcl_num1, max(tx_thdcl_num1), out=np.zeros_like(tx_thdcl_num1, dtype=np.float64),
                       where=max(tx_thdcl_num1) != 0)
    for i in range(len(tx_thdcl_num1)):
        tx_thdcl_color.append("%.2f%%" % (arrayA[i] * 100))
    if tx_thdcl_num1[0] == 'nan%':
        a = 0
        for i in range(len(tx_thdcl_num1)):
            tx_thdcl_num1[i] = '{:.2%}'.format(a)

    arrayA = np.divide(tx_dhq_num1, max(tx_dhq_num1), out=np.zeros_like(tx_dhq_num1, dtype=np.float64),
                       where=max(tx_dhq_num1) != 0)
    for i in range(len(tx_dhq_num1)):
        tx_dhq_color.append("%.2f%%" % (arrayA[i] * 100))
    if tx_dhq_num1[0] == 'nan%':
        a = 0
        for i in range(len(tx_dhq_num1)):
            tx_dhq_num1[i] = '{:.2%}'.format(a)

    arrayA = np.divide(tx_yhq_num1, max(tx_yhq_num1), out=np.zeros_like(tx_yhq_num1, dtype=np.float64),
                       where=max(tx_yhq_num1) != 0)
    for i in range(len(tx_yhq_num1)):
        tx_yhq_color.append("%.2f%%" % (arrayA[i] * 100))
    if tx_yhq_num1[0] == 'nan%':
        a = 0
        for i in range(len(tx_yhq_num1)):
            tx_yhq_num1[i] = '{:.2%}'.format(a)

    arrayA = np.divide(tx_ddcl_num1, max(tx_ddcl_num1), out=np.zeros_like(tx_ddcl_num1, dtype=np.float64),
                       where=max(tx_ddcl_num1) != 0)
    for i in range(len(tx_ddcl_num1)):
        tx_ddcl_color.append("%.2f%%" % (arrayA[i] * 100))
    if tx_ddcl_num1[0] == 'nan%':
        a = 0
        for i in range(len(tx_ddcl_num1)):
            tx_ddcl_num1[i] = '{:.2%}'.format(a)

    jsonData['hm_dqr_num1'] = hm_dqr_num1
    jsonData['hm_dzkcl_num1'] = hm_dzkcl_num1
    jsonData['hm_thdcl_num1'] = hm_thdcl_num1
    jsonData['hm_dhq_num1'] = hm_dhq_num1
    jsonData['hm_yhq_num1'] = hm_yhq_num1
    jsonData['hm_ddcl_num1'] = hm_ddcl_num1
    jsonData['hm_yhq_15'] = hm_yhq_15
    jsonData['hm_ddcl_30'] = hm_ddcl_30
    jsonData['hm_ht_num1'] = hm_ht_num1
    jsonData['tx_dqr_num1'] = tx_dqr_num1
    jsonData['tx_dzkcl_num1'] = tx_dzkcl_num1
    jsonData['tx_thdcl_num1'] = tx_thdcl_num1
    jsonData['tx_dhq_num1'] = tx_dhq_num1
    jsonData['tx_yhq_num1'] = tx_yhq_num1
    jsonData['tx_ddcl_num1'] = tx_ddcl_num1
    jsonData['tx_yhq_15'] = tx_yhq_15
    jsonData['tx_ddcl_30'] = tx_ddcl_30
    jsonData['tx_ht_num1'] = tx_ht_num1

    jsonData['hm_dqr_color'] = hm_dqr_color
    jsonData['hm_dzkcl_color'] = hm_dzkcl_color
    jsonData['hm_thdcl_color'] = hm_thdcl_color
    jsonData['hm_dhq_color'] = hm_dhq_color
    jsonData['hm_yhq_color'] = hm_yhq_color
    jsonData['hm_ddcl_color'] = hm_ddcl_color
    jsonData['tx_dqr_color'] = tx_dqr_color
    jsonData['tx_dzkcl_color'] = tx_dzkcl_color
    jsonData['tx_thdcl_color'] = tx_thdcl_color
    jsonData['tx_dhq_color'] = tx_dhq_color
    jsonData['tx_yhq_color'] = tx_yhq_color
    jsonData['tx_ddcl_color'] = tx_ddcl_color
    j = json.dumps(jsonData, cls=DecimalEncoder)
    return (j)


@app.route('/test5', methods=['POST'])
def diaobo():
    input = pd.read_excel('test5.xlsx')
    see=save(input)
    input = pd.read_excel('test5_sql2.xlsx')
    see_ck=save(input)
    warehouse = []
    order_id = []
    status = []
    num = []
    s = []
    jsonData = {}
    # cur.execute(sql3)
    # cur.fetchall()

    for data in see:
        warehouse.append(data[0])
        order_id.append(data[1])
        status.append(data[2])
        num.append(decimal.Decimal(data[4]))
        s.append(decimal.Decimal(data[5]))

    warehouse_ck = []
    order_id_ck = []
    status_ck = []
    num_ck = []
    s_ck = []


    for data_ck in see_ck:
        warehouse_ck.append(data_ck[0])
        order_id_ck.append(data_ck[1])
        status_ck.append(data_ck[2])
        num_ck.append(decimal.Decimal(data_ck[3]))
        s_ck.append(decimal.Decimal(data_ck[4]))

    hm_order_id_ck = []
    hm_status_ck = []
    hm_num_ck = []
    hm_s_ck = []

    tx_order_id_ck = []
    tx_status_ck = []
    tx_num_ck = []
    tx_s_ck = []

    for i in range(len(warehouse_ck)):
        if warehouse_ck[i] == "HM_AA":
            hm_order_id_ck.append(order_id_ck[i])
            hm_status_ck.append(status_ck[i])
            hm_num_ck.append(num_ck[i])
            hm_s_ck.append(s_ck[i])
    for i in range(len(warehouse_ck)):
        if warehouse_ck[i] == "SZ_AA":
            tx_order_id_ck.append(order_id_ck[i])
            tx_status_ck.append(status_ck[i])
            tx_num_ck.append(num_ck[i])
            tx_s_ck.append(s_ck[i])
    hm_data_ck = np.dstack((hm_order_id_ck, hm_status_ck, hm_num_ck, hm_s_ck))
    tx_data_ck = np.dstack((tx_order_id_ck, tx_status_ck, tx_num_ck, tx_s_ck))
    print(hm_num_ck)
    print(hm_data_ck)
    hm_ck_dld_order = []
    hm_ck_dld_num = []
    hm_ck_dld_s = []
    hm_ck_djh_order = []
    hm_ck_djh_num = []
    hm_ck_djh_s = []
    hm_ck_ddb_order = []
    hm_ck_ddb_num = []
    hm_ck_ddb_s = []
    hm_ck_dck_order = []
    hm_ck_dck_num = []
    hm_ck_dck_s = []
    hm_ck_djy_order = []
    hm_ck_djy_num = []
    hm_ck_djy_s = []
    tx_ck_dld_order = []
    tx_ck_dld_num = []
    tx_ck_dld_s = []
    tx_ck_djh_order = []
    tx_ck_djh_num = []
    tx_ck_djh_s = []
    tx_ck_ddb_order = []
    tx_ck_ddb_num = []
    tx_ck_ddb_s = []
    tx_ck_dck_order = []
    tx_ck_dck_num = []
    tx_ck_dck_s = []
    tx_ck_djy_order = []
    tx_ck_djy_num = []
    tx_ck_djy_s = []
    for i in range(len(hm_data_ck[0])):
        if (hm_data_ck[0][i][1] == "DLD"):
            hm_ck_dld_order.append(hm_data_ck[0][i][0])
            hm_ck_dld_num.append(hm_data_ck[0][i][2])
            hm_ck_dld_s.append(hm_data_ck[0][i][3])

    for i in range(len(hm_data_ck[0])):
        if (hm_data_ck[0][i][1] == "DJH"):
            hm_ck_djh_order.append(hm_data_ck[0][i][0])
            hm_ck_djh_num.append(hm_data_ck[0][i][2])
            hm_ck_djh_s.append(hm_data_ck[0][i][3])

    for i in range(len(hm_data_ck[0])):
        if (hm_data_ck[0][i][1] == "DDB"):
            hm_ck_ddb_order.append(hm_data_ck[0][i][0])
            hm_ck_ddb_num.append(hm_data_ck[0][i][2])
            hm_ck_ddb_s.append(hm_data_ck[0][i][3])
    for i in range(len(hm_data_ck[0])):
        if (hm_data_ck[0][i][1] == "DCK"):
            hm_ck_dck_order.append(hm_data_ck[0][i][0])
            hm_ck_dck_num.append(hm_data_ck[0][i][2])
            hm_ck_dck_s.append(hm_data_ck[0][i][3])
    for i in range(len(hm_data_ck[0])):
        if (hm_data_ck[0][i][1] == "DJY"):
            hm_ck_djy_order.append(hm_data_ck[0][i][0])
            hm_ck_djy_num.append(hm_data_ck[0][i][2])
            hm_ck_djy_s.append(hm_data_ck[0][i][3])

    for i in range(len(tx_data_ck[0])):
        if (tx_data_ck[0][i][1] == "DLD"):
            tx_ck_dld_order.append(tx_data_ck[0][i][0])
            tx_ck_dld_num.append(tx_data_ck[0][i][2])
            tx_ck_dld_s.append(tx_data_ck[0][i][3])

    for i in range(len(tx_data_ck[0])):
        if (tx_data_ck[0][i][1] == "DJH"):
            tx_ck_djh_order.append(tx_data_ck[0][i][0])
            tx_ck_djh_num.append(tx_data_ck[0][i][2])
            tx_ck_djh_s.append(tx_data_ck[0][i][3])
    for i in range(len(tx_data_ck[0])):
        if (tx_data_ck[0][i][1] == "DDB"):
            tx_ck_ddb_order.append(tx_data_ck[0][i][0])
            tx_ck_ddb_num.append(tx_data_ck[0][i][2])
            tx_ck_ddb_s.append(tx_data_ck[0][i][3])
    for i in range(len(tx_data_ck[0])):
        if (tx_data_ck[0][i][1] == "DCK"):
            tx_ck_dck_order.append(tx_data_ck[0][i][0])
            tx_ck_dck_num.append(tx_data_ck[0][i][2])
            tx_ck_dck_s.append(tx_data_ck[0][i][3])
    for i in range(len(tx_data_ck[0])):
        if (tx_data_ck[0][i][1] == "DJY"):
            tx_ck_djy_order.append(tx_data_ck[0][i][0])
            tx_ck_djy_num.append(tx_data_ck[0][i][2])
            tx_ck_djy_s.append(tx_data_ck[0][i][3])
    print(hm_ck_dld_num)
    hm_dld = np.dstack((hm_ck_dld_order, hm_ck_dld_num, hm_ck_dld_s))
    hm_djh = np.dstack((hm_ck_djh_order, hm_ck_djh_num, hm_ck_djh_s))
    hm_ddb = np.dstack((hm_ck_ddb_order, hm_ck_ddb_num, hm_ck_ddb_s))
    hm_dck = np.dstack((hm_ck_dck_order, hm_ck_dck_num, hm_ck_dck_s))
    hm_djy = np.dstack((hm_ck_djy_order, hm_ck_djy_num, hm_ck_djy_s))
    tx_dld = np.dstack((tx_ck_dld_order, tx_ck_dld_num, tx_ck_dld_s))
    tx_djh = np.dstack((tx_ck_djh_order, tx_ck_djh_num, tx_ck_djh_s))
    tx_ddb = np.dstack((tx_ck_ddb_order, tx_ck_ddb_num, tx_ck_ddb_s))
    tx_dck = np.dstack((tx_ck_dck_order, tx_ck_dck_num, tx_ck_dck_s))
    tx_djy = np.dstack((tx_ck_djy_order, tx_ck_djy_num, tx_ck_djy_s))
    hm_dld_j = [0, 0, 0, 0, 0, 0, 0]
    hm_dld_b = [0, 0, 0, 0, 0, 0, 0]
    hm_djh_j = [0, 0, 0, 0, 0, 0, 0]
    hm_djh_b = [0, 0, 0, 0, 0, 0, 0]
    hm_ddb_j = [0, 0, 0, 0, 0, 0, 0]
    hm_ddb_b = [0, 0, 0, 0, 0, 0, 0]
    hm_dck_j = [0, 0, 0, 0, 0, 0, 0]
    hm_dck_b = [0, 0, 0, 0, 0, 0, 0]
    hm_djy_j = [0, 0, 0, 0, 0, 0, 0]
    hm_djy_b = [0, 0, 0, 0, 0, 0, 0]
    tx_dld_j = [0, 0, 0, 0, 0, 0, 0]
    tx_dld_b = [0, 0, 0, 0, 0, 0, 0]
    tx_djh_j = [0, 0, 0, 0, 0, 0, 0]
    tx_djh_b = [0, 0, 0, 0, 0, 0, 0]
    tx_ddb_j = [0, 0, 0, 0, 0, 0, 0]
    tx_ddb_b = [0, 0, 0, 0, 0, 0, 0]
    tx_dck_j = [0, 0, 0, 0, 0, 0, 0]
    tx_dck_b = [0, 0, 0, 0, 0, 0, 0]
    tx_djy_j = [0, 0, 0, 0, 0, 0, 0]
    tx_djy_b = [0, 0, 0, 0, 0, 0, 0]
    print(hm_dld_j)
    print(hm_dld)
    for i in range(len(hm_dld[0])):
        if float(hm_ck_dld_s[i]) > 0 and float(hm_ck_dld_s[i]) < 2:
            hm_dld_j[0] = hm_dld_j[0] + hm_dld[0][i][1]
        if float(hm_ck_dld_s[i]) > 2 and float(hm_ck_dld_s[i]) < 4:
            hm_dld_j[1] = hm_dld_j[1] + hm_dld[0][i][1]
        if float(hm_ck_dld_s[i]) > 4 and float(hm_ck_dld_s[i]) < 6:
            hm_dld_j[2] = hm_dld_j[2] + hm_dld[0][i][1]
        if float(hm_ck_dld_s[i]) > 6 and float(hm_ck_dld_s[i]) < 8:
            hm_dld_j[3] = hm_dld_j[3] + hm_dld[0][i][1]
        if float(hm_ck_dld_s[i]) > 8 and float(hm_ck_dld_s[i]) < 12:
            hm_dld_j[4] = hm_dld_j[4] + hm_dld[0][i][1]
        if float(hm_ck_dld_s[i]) > 12 and float(hm_ck_dld_s[i]) < 24:
            hm_dld_j[5] = hm_dld_j[5] + hm_dld[0][i][1]
        if float(hm_ck_dld_s[i]) > 24:
            hm_dld_j[6] = hm_dld_j[6] + hm_dld[0][i][1]
    print(hm_dld_j[5])
    for i in range(len(hm_dld[0])):
        if float(hm_ck_dld_s[i]) > 0 and float(hm_ck_dld_s[i]) < 2:
            hm_dld_b[0] = hm_dld_b[0] + 1
        if float(hm_ck_dld_s[i]) > 2 and float(hm_ck_dld_s[i]) < 4:
            hm_dld_b[1] = hm_dld_b[1] + 1
        if float(hm_ck_dld_s[i]) > 4 and float(hm_ck_dld_s[i]) < 6:
            hm_dld_b[2] = hm_dld_b[2] + 1
        if float(hm_ck_dld_s[i]) > 6 and float(hm_ck_dld_s[i]) < 8:
            hm_dld_b[3] = hm_dld_b[3] + 1
        if float(hm_ck_dld_s[i]) > 8 and float(hm_ck_dld_s[i]) < 12:
            hm_dld_b[4] = hm_dld_b[4] + 1
        if float(hm_ck_dld_s[i]) > 12 and float(hm_ck_dld_s[i]) < 24:
            hm_dld_b[5] = hm_dld_b[5] + 1
        if float(hm_ck_dld_s[i]) > 24:
            hm_dld_b[6] = hm_dld_b[6] + 1

    for i in range(len(hm_djh[0])):
        if float(hm_ck_djh_s[i]) > 0 and float(hm_ck_djh_s[i]) < 2:
            hm_djh_j[0] = hm_djh_j[0] + hm_djh[0][i][1]
        if float(hm_ck_djh_s[i]) > 2 and float(hm_ck_djh_s[i]) < 4:
            hm_djh_j[1] = hm_djh_j[1] + hm_djh[0][i][1]
        if float(hm_ck_djh_s[i]) > 4 and float(hm_ck_djh_s[i]) < 6:
            hm_djh_j[2] = hm_djh_j[2] + hm_djh[0][i][1]
        if float(hm_ck_djh_s[i]) > 6 and float(hm_ck_djh_s[i]) < 8:
            hm_djh_j[3] = hm_djh_j[3] + hm_djh[0][i][1]
        if float(hm_ck_djh_s[i]) > 8 and float(hm_ck_djh_s[i]) < 12:
            hm_djh_j[4] = hm_djh_j[4] + hm_djh[0][i][1]
        if float(hm_ck_djh_s[i]) > 12 and float(hm_ck_djh_s[i]) < 24:
            hm_djh_j[5] = hm_djh_j[5] + hm_djh[0][i][1]
        if float(hm_ck_djh_s[i]) > 24:
            hm_djh_j[6] = hm_djh_j[6] + hm_djh[0][i][1]
    for i in range(len(hm_djh[0])):
        if float(hm_ck_djh_s[i]) > 0 and float(hm_ck_djh_s[i]) < 2:
            hm_djh_b[0] = hm_djh_b[0] + 1
        if float(hm_ck_djh_s[i]) > 2 and float(hm_ck_djh_s[i]) < 4:
            hm_djh_b[1] = hm_djh_b[1] + 1
        if float(hm_ck_djh_s[i]) > 4 and float(hm_ck_djh_s[i]) < 6:
            hm_djh_b[2] = hm_djh_b[2] + 1
        if float(hm_ck_djh_s[i]) > 6 and float(hm_ck_djh_s[i]) < 8:
            hm_djh_b[3] = hm_djh_b[3] + 1
        if float(hm_ck_djh_s[i]) > 8 and float(hm_ck_djh_s[i]) < 12:
            hm_djh_b[4] = hm_djh_b[4] + 1
        if float(hm_ck_djh_s[i]) > 12 and float(hm_ck_djh_s[i]) < 24:
            hm_djh_b[5] = hm_djh_b[5] + 1
        if float(hm_ck_djh_s[i]) > 24:
            hm_djh_b[6] = hm_djh_b[6] + 1

    for i in range(len(hm_ddb[0])):
        if float(hm_ck_ddb_s[i]) > 0 and float(hm_ck_ddb_s[i]) < 2:
            hm_ddb_j[0] = hm_ddb_j[0] + hm_ddb[0][i][1]
        if float(hm_ck_ddb_s[i]) > 2 and float(hm_ck_ddb_s[i]) < 4:
            hm_ddb_j[1] = hm_ddb_j[1] + hm_ddb[0][i][1]
        if float(hm_ck_ddb_s[i]) > 4 and float(hm_ck_ddb_s[i]) < 6:
            hm_ddb_j[2] = hm_ddb_j[2] + hm_ddb[0][i][1]
        if float(hm_ck_ddb_s[i]) > 6 and float(hm_ck_ddb_s[i]) < 8:
            hm_ddb_j[3] = hm_ddb_j[3] + hm_ddb[0][i][1]
        if float(hm_ck_ddb_s[i]) > 8 and float(hm_ck_ddb_s[i]) < 12:
            hm_ddb_j[4] = hm_ddb_j[4] + hm_ddb[0][i][1]
        if float(hm_ck_ddb_s[i]) > 12 and float(hm_ck_ddb_s[i]) < 24:
            hm_ddb_j[5] = hm_ddb_j[5] + hm_ddb[0][i][1]
        if float(hm_ck_ddb_s[i]) > 24:
            hm_ddb_j[6] = hm_ddb_j[6] + hm_ddb[0][i][1]
    for i in range(len(hm_ddb[0])):
        if float(hm_ck_ddb_s[i]) > 0 and float(hm_ck_ddb_s[i]) < 2:
            hm_ddb_b[0] = hm_ddb_b[0] + 1
        if float(hm_ck_ddb_s[i]) > 2 and float(hm_ck_ddb_s[i]) < 4:
            hm_ddb_b[1] = hm_ddb_b[1] + 1
        if float(hm_ck_ddb_s[i]) > 4 and float(hm_ck_ddb_s[i]) < 6:
            hm_ddb_b[2] = hm_ddb_b[2] + 1
        if float(hm_ck_ddb_s[i]) > 6 and float(hm_ck_ddb_s[i]) < 8:
            hm_ddb_b[3] = hm_ddb_b[3] + 1
        if float(hm_ck_ddb_s[i]) > 8 and float(hm_ck_ddb_s[i]) < 12:
            hm_ddb_b[4] = hm_ddb_b[4] + 1
        if float(hm_ck_ddb_s[i]) > 12 and float(hm_ck_ddb_s[i]) < 24:
            hm_ddb_b[5] = hm_ddb_b[5] + 1
        if float(hm_ck_ddb_s[i]) > 24:
            hm_ddb_b[6] = hm_ddb_b[6] + 1
    for i in range(len(hm_dck[0])):
        if float(hm_ck_dck_s[i]) > 0 and float(hm_ck_dck_s[i]) < 2:
            hm_dck_j[0] = hm_dck_j[0] + hm_dck[0][i][1]
        if float(hm_ck_dck_s[i]) > 2 and float(hm_ck_dck_s[i]) < 4:
            hm_dck_j[1] = hm_dck_j[1] + hm_dck[0][i][1]
        if float(hm_ck_dck_s[i]) > 4 and float(hm_ck_dck_s[i]) < 6:
            hm_dck_j[2] = hm_dck_j[2] + hm_dck[0][i][1]
        if float(hm_ck_dck_s[i]) > 6 and float(hm_ck_dck_s[i]) < 8:
            hm_dck_j[3] = hm_dck_j[3] + hm_dck[0][i][1]
        if float(hm_ck_dck_s[i]) > 8 and float(hm_ck_dck_s[i]) < 12:
            hm_dck_j[4] = hm_dck_j[4] + hm_dck[0][i][1]
        if float(hm_ck_dck_s[i]) > 12 and float(hm_ck_dck_s[i]) < 24:
            hm_dck_j[5] = hm_dck_j[5] + hm_dck[0][i][1]
        if float(hm_ck_dck_s[i]) > 24:
            hm_dck_j[6] = hm_dck_j[6] + hm_dck[0][i][1]
    for i in range(len(hm_dck[0])):
        if float(hm_ck_dck_s[i]) > 0 and float(hm_ck_dck_s[i]) < 2:
            hm_dck_b[0] = hm_dck_b[0] + 1
        if float(hm_ck_dck_s[i]) > 2 and float(hm_ck_dck_s[i]) < 4:
            hm_dck_b[1] = hm_dck_b[1] + 1
        if float(hm_ck_dck_s[i]) > 4 and float(hm_ck_dck_s[i]) < 6:
            hm_dck_b[2] = hm_dck_b[2] + 1
        if float(hm_ck_dck_s[i]) > 6 and float(hm_ck_dck_s[i]) < 8:
            hm_dck_b[3] = hm_dck_b[3] + 1
        if float(hm_ck_dck_s[i]) > 8 and float(hm_ck_dck_s[i]) < 12:
            hm_dck_b[4] = hm_dck_b[4] + 1
        if float(hm_ck_dck_s[i]) > 12 and float(hm_ck_dck_s[i]) < 24:
            hm_dck_b[5] = hm_dck_b[5] + 1
        if float(hm_ck_dck_s[i]) > 24:
            hm_dck_b[6] = hm_dck_b[6] + 1
    for i in range(len(hm_djy[0])):
        if float(hm_ck_djy_s[i]) > 0 and float(hm_ck_djy_s[i]) < 2:
            hm_djy_j[0] = hm_djy_j[0] + hm_djy[0][i][1]
        if float(hm_ck_djy_s[i]) > 2 and float(hm_ck_djy_s[i]) < 4:
            hm_djy_j[1] = hm_djy_j[1] + hm_djy[0][i][1]
        if float(hm_ck_djy_s[i]) > 4 and float(hm_ck_djy_s[i]) < 6:
            hm_djy_j[2] = hm_djy_j[2] + hm_djy[0][i][1]
        if float(hm_ck_djy_s[i]) > 6 and float(hm_ck_djy_s[i]) < 8:
            hm_djy_j[3] = hm_djy_j[3] + hm_djy[0][i][1]
        if float(hm_ck_djy_s[i]) > 8 and float(hm_ck_djy_s[i]) < 12:
            hm_djy_j[4] = hm_djy_j[4] + hm_djy[0][i][1]
        if float(hm_ck_djy_s[i]) > 12 and float(hm_ck_djy_s[i]) < 24:
            hm_djy_j[5] = hm_djy_j[5] + hm_djy[0][i][1]
        if float(hm_ck_djy_s[i]) > 24:
            hm_djy_j[6] = hm_djy_j[6] + hm_djy[0][i][1]
    for i in range(len(hm_djy[0])):
        if float(hm_ck_djy_s[i]) > 0 and float(hm_ck_djy_s[i]) < 2:
            hm_djy_b[0] = hm_djy_b[0] + 1
        if float(hm_ck_djy_s[i]) > 2 and float(hm_ck_djy_s[i]) < 4:
            hm_djy_b[1] = hm_djy_b[1] + 1
        if float(hm_ck_djy_s[i]) > 4 and float(hm_ck_djy_s[i]) < 6:
            hm_djy_b[2] = hm_djy_b[2] + 1
        if float(hm_ck_djy_s[i]) > 6 and float(hm_ck_djy_s[i]) < 8:
            hm_djy_b[3] = hm_djy_b[3] + 1
        if float(hm_ck_djy_s[i]) > 8 and float(hm_ck_djy_s[i]) < 12:
            hm_djy_b[4] = hm_djy_b[4] + 1
        if float(hm_ck_djy_s[i]) > 12 and float(hm_ck_djy_s[i]) < 24:
            hm_djy_b[5] = hm_djy_b[5] + 1
        if float(hm_ck_djy_s[i]) > 24:
            hm_djy_b[6] = hm_djy_b[6] + 1
    for i in range(len(tx_dld[0])):
        if float(tx_ck_dld_s[i]) > 0 and float(tx_ck_dld_s[i]) < 2:
            tx_dld_j[0] = tx_dld_j[0] + tx_dld[0][i][1]
        if float(tx_ck_dld_s[i]) > 2 and float(tx_ck_dld_s[i]) < 4:
            tx_dld_j[1] = tx_dld_j[1] + tx_dld[0][i][1]
        if float(tx_ck_dld_s[i]) > 4 and float(tx_ck_dld_s[i]) < 6:
            tx_dld_j[2] = tx_dld_j[2] + tx_dld[0][i][1]
        if float(tx_ck_dld_s[i]) > 6 and float(tx_ck_dld_s[i]) < 8:
            tx_dld_j[3] = tx_dld_j[3] + tx_dld[0][i][1]
        if float(tx_ck_dld_s[i]) > 8 and float(tx_ck_dld_s[i]) < 12:
            tx_dld_j[4] = tx_dld_j[4] + tx_dld[0][i][1]
        if float(tx_ck_dld_s[i]) > 12 and float(tx_ck_dld_s[i]) < 24:
            tx_dld_j[5] = tx_dld_j[5] + tx_dld[0][i][1]
        if float(tx_ck_dld_s[i]) > 24:
            tx_dld_j[6] = tx_dld_j[6] + tx_dld[0][i][1]
    for i in range(len(tx_dld[0])):
        if float(tx_ck_dld_s[i]) > 0 and float(tx_ck_dld_s[i]) < 2:
            tx_dld_b[0] = tx_dld_b[0] + 1
        if float(tx_ck_dld_s[i]) > 2 and float(tx_ck_dld_s[i]) < 4:
            tx_dld_b[1] = tx_dld_b[1] + 1
        if float(tx_ck_dld_s[i]) > 4 and float(tx_ck_dld_s[i]) < 6:
            tx_dld_b[2] = tx_dld_b[2] + 1
        if float(tx_ck_dld_s[i]) > 6 and float(tx_ck_dld_s[i]) < 8:
            tx_dld_b[3] = tx_dld_b[3] + 1
        if float(tx_ck_dld_s[i]) > 8 and float(tx_ck_dld_s[i]) < 12:
            tx_dld_b[4] = tx_dld_b[4] + 1
        if float(tx_ck_dld_s[i]) > 12 and float(tx_ck_dld_s[i]) < 24:
            tx_dld_b[5] = tx_dld_b[5] + 1
        if float(tx_ck_dld_s[i]) > 24:
            tx_dld_b[6] = tx_dld_b[6] + 1
    for i in range(len(tx_djh[0])):
        if float(tx_ck_djh_s[i]) > 0 and float(tx_ck_djh_s[i]) < 2:
            tx_djh_j[0] = tx_djh_j[0] + tx_djh[0][i][1]
        if float(tx_ck_djh_s[i]) > 2 and float(tx_ck_djh_s[i]) < 4:
            tx_djh_j[1] = tx_djh_j[1] + tx_djh[0][i][1]
        if float(tx_ck_djh_s[i]) > 4 and float(tx_ck_djh_s[i]) < 6:
            tx_djh_j[2] = tx_djh_j[2] + tx_djh[0][i][1]
        if float(tx_ck_djh_s[i]) > 6 and float(tx_ck_djh_s[i]) < 8:
            tx_djh_j[3] = tx_djh_j[3] + tx_djh[0][i][1]
        if float(tx_ck_djh_s[i]) > 8 and float(tx_ck_djh_s[i]) < 12:
            tx_djh_j[4] = tx_djh_j[4] + tx_djh[0][i][1]
        if float(tx_ck_djh_s[i]) > 12 and float(tx_ck_djh_s[i]) < 24:
            tx_djh_j[5] = tx_djh_j[5] + tx_djh[0][i][1]
        if float(tx_ck_djh_s[i]) > 24:
            tx_djh_j[6] = tx_djh_j[6] + tx_djh[0][i][1]
    for i in range(len(tx_djh[0])):
        if float(tx_ck_djh_s[i]) > 0 and float(tx_ck_djh_s[i]) < 2:
            tx_djh_b[0] = tx_djh_b[0] + 1
        if float(tx_ck_djh_s[i]) > 2 and float(tx_ck_djh_s[i]) < 4:
            tx_djh_b[1] = tx_djh_b[1] + 1
        if float(tx_ck_djh_s[i]) > 4 and float(tx_ck_djh_s[i]) < 6:
            tx_djh_b[2] = tx_djh_b[2] + 1
        if float(tx_ck_djh_s[i]) > 6 and float(tx_ck_djh_s[i]) < 8:
            tx_djh_b[3] = tx_djh_b[3] + 1
        if float(tx_ck_djh_s[i]) > 8 and float(tx_ck_djh_s[i]) < 12:
            tx_djh_b[4] = tx_djh_b[4] + 1
        if float(tx_ck_djh_s[i]) > 12 and float(tx_ck_djh_s[i]) < 24:
            tx_djh_b[5] = tx_djh_b[5] + 1
        if float(tx_ck_djh_s[i]) > 24:
            tx_djh_b[6] = tx_djh_b[6] + 1

    for i in range(len(tx_ddb[0])):
        if float(tx_ck_ddb_s[i]) > 0 and float(tx_ck_ddb_s[i]) < 2:
            tx_ddb_j[0] = tx_ddb_j[0] + tx_ddb[0][i][1]
        if float(tx_ck_ddb_s[i]) > 2 and float(tx_ck_ddb_s[i]) < 4:
            tx_ddb_j[1] = tx_ddb_j[1] + tx_ddb[0][i][1]
        if float(tx_ck_ddb_s[i]) > 4 and float(tx_ck_ddb_s[i]) < 6:
            tx_ddb_j[2] = tx_ddb_j[2] + tx_ddb[0][i][1]
        if float(tx_ck_ddb_s[i]) > 6 and float(tx_ck_ddb_s[i]) < 8:
            tx_ddb_j[3] = tx_ddb_j[3] + tx_ddb[0][i][1]
        if float(tx_ck_ddb_s[i]) > 8 and float(tx_ck_ddb_s[i]) < 12:
            tx_ddb_j[4] = tx_ddb_j[4] + tx_ddb[0][i][1]
        if float(tx_ck_ddb_s[i]) > 12 and float(tx_ck_ddb_s[i]) < 24:
            tx_ddb_j[5] = tx_ddb_j[5] + tx_ddb[0][i][1]
        if float(tx_ck_ddb_s[i]) > 24:
            tx_ddb_j[6] = tx_ddb_j[6] + tx_ddb[0][i][1]
    for i in range(len(tx_ddb[0])):
        if float(tx_ck_ddb_s[i]) > 0 and float(tx_ck_ddb_s[i]) < 2:
            tx_ddb_b[0] = tx_ddb_b[0] + 1
        if float(tx_ck_ddb_s[i]) > 2 and float(tx_ck_ddb_s[i]) < 4:
            tx_ddb_b[1] = tx_ddb_b[1] + 1
        if float(tx_ck_ddb_s[i]) > 4 and float(tx_ck_ddb_s[i]) < 6:
            tx_ddb_b[2] = tx_ddb_b[2] + 1
        if float(tx_ck_ddb_s[i]) > 6 and float(tx_ck_ddb_s[i]) < 8:
            tx_ddb_b[3] = tx_ddb_b[3] + 1
        if float(tx_ck_ddb_s[i]) > 8 and float(tx_ck_ddb_s[i]) < 12:
            tx_ddb_b[4] = tx_ddb_b[4] + 1
        if float(tx_ck_ddb_s[i]) > 12 and float(tx_ck_ddb_s[i]) < 24:
            tx_ddb_b[5] = tx_ddb_b[5] + 1
        if float(tx_ck_ddb_s[i]) > 24:
            tx_ddb_b[6] = tx_ddb_b[6] + 1
    for i in range(len(tx_dck[0])):
        if float(tx_ck_dck_s[i]) > 0 and float(tx_ck_dck_s[i]) < 2:
            tx_dck_j[0] = tx_dck_j[0] + tx_dck[0][i][1]
        if float(tx_ck_dck_s[i]) > 2 and float(tx_ck_dck_s[i]) < 4:
            tx_dck_j[1] = tx_dck_j[1] + tx_dck[0][i][1]
        if float(tx_ck_dck_s[i]) > 4 and float(tx_ck_dck_s[i]) < 6:
            tx_dck_j[2] = tx_dck_j[2] + tx_dck[0][i][1]
        if float(tx_ck_dck_s[i]) > 6 and float(tx_ck_dck_s[i]) < 8:
            tx_dck_j[3] = tx_dck_j[3] + tx_dck[0][i][1]
        if float(tx_ck_dck_s[i]) > 8 and float(tx_ck_dck_s[i]) < 12:
            tx_dck_j[4] = tx_dck_j[4] + tx_dck[0][i][1]
        if float(tx_ck_dck_s[i]) > 12 and float(tx_ck_dck_s[i]) < 24:
            tx_dck_j[5] = tx_dck_j[5] + tx_dck[0][i][1]
        if float(tx_ck_dck_s[i]) > 24:
            tx_dck_j[6] = tx_dck_j[6] + tx_dck[0][i][1]
    for i in range(len(tx_dck[0])):
        if float(tx_ck_dck_s[i]) > 0 and float(tx_ck_dck_s[i]) < 2:
            tx_dck_b[0] = tx_dck_b[0] + 1
        if float(tx_ck_dck_s[i]) > 2 and float(tx_ck_dck_s[i]) < 4:
            tx_dck_b[1] = tx_dck_b[1] + 1
        if float(tx_ck_dck_s[i]) > 4 and float(tx_ck_dck_s[i]) < 6:
            tx_dck_b[2] = tx_dck_b[2] + 1
        if float(tx_ck_dck_s[i]) > 6 and float(tx_ck_dck_s[i]) < 8:
            tx_dck_b[3] = tx_dck_b[3] + 1
        if float(tx_ck_dck_s[i]) > 8 and float(tx_ck_dck_s[i]) < 12:
            tx_dck_b[4] = tx_dck_b[4] + 1
        if float(tx_ck_dck_s[i]) > 12 and float(tx_ck_dck_s[i]) < 24:
            tx_dck_b[5] = tx_dck_b[5] + 1
        if float(tx_ck_dck_s[i]) > 24:
            tx_dck_b[6] = tx_dck_b[6] + 1
    for i in range(len(tx_djy[0])):
        if float(tx_ck_djy_s[i]) > 0 and float(tx_ck_djy_s[i]) < 2:
            tx_djy_j[0] = tx_djy_j[0] + tx_djy[0][i][1]
        if float(tx_ck_djy_s[i]) > 2 and float(tx_ck_djy_s[i]) < 4:
            tx_djy_j[1] = tx_djy_j[1] + tx_djy[0][i][1]
        if float(tx_ck_djy_s[i]) > 4 and float(tx_ck_djy_s[i]) < 6:
            tx_djy_j[2] = tx_djy_j[2] + tx_djy[0][i][1]
        if float(tx_ck_djy_s[i]) > 6 and float(tx_ck_djy_s[i]) < 8:
            tx_djy_j[3] = tx_djy_j[3] + tx_djy[0][i][1]
        if float(tx_ck_djy_s[i]) > 8 and float(tx_ck_djy_s[i]) < 12:
            tx_djy_j[4] = tx_djy_j[4] + tx_djy[0][i][1]
        if float(tx_ck_djy_s[i]) > 12 and float(tx_ck_djy_s[i]) < 24:
            tx_djy_j[5] = tx_djy_j[5] + tx_djy[0][i][1]
        if float(tx_ck_djy_s[i]) > 24:
            tx_djy_j[6] = tx_djy_j[6] + tx_djy[0][i][1]
    for i in range(len(tx_djy[0])):
        if float(tx_ck_djy_s[i]) > 0 and float(tx_ck_djy_s[i]) < 2:
            tx_djy_b[0] = tx_djy_b[0] + 1
        if float(tx_ck_djy_s[i]) > 2 and float(tx_ck_djy_s[i]) < 4:
            tx_djy_b[1] = tx_djy_b[1] + 1
        if float(tx_ck_djy_s[i]) > 4 and float(tx_ck_djy_s[i]) < 6:
            tx_djy_b[2] = tx_djy_b[2] + 1
        if float(tx_ck_djy_s[i]) > 6 and float(tx_ck_djy_s[i]) < 8:
            tx_djy_b[3] = tx_djy_b[3] + 1
        if float(tx_ck_djy_s[i]) > 8 and float(tx_ck_djy_s[i]) < 12:
            tx_djy_b[4] = tx_djy_b[4] + 1
        if float(tx_ck_djy_s[i]) > 12 and float(tx_ck_djy_s[i]) < 24:
            tx_djy_b[5] = tx_djy_b[5] + 1
        if float(tx_ck_djy_s[i]) > 24:
            tx_djy_b[6] = tx_djy_b[6] + 1
    hm_ck_dld_j_color = []
    hm_ck_djh_j_color = []
    hm_ck_ddb_j_color = []
    hm_ck_dck_j_color = []
    hm_ck_djy_j_color = []
    hm_ck_dld_b_color = []
    hm_ck_djh_b_color = []
    hm_ck_ddb_b_color = []
    hm_ck_dck_b_color = []
    hm_ck_djy_b_color = []
    tx_ck_dld_j_color = []
    tx_ck_djh_j_color = []
    tx_ck_ddb_j_color = []
    tx_ck_dck_j_color = []
    tx_ck_djy_j_color = []
    tx_ck_dld_b_color = []
    tx_ck_djh_b_color = []
    tx_ck_ddb_b_color = []
    tx_ck_dck_b_color = []
    tx_ck_djy_b_color = []

    arrayA = np.divide(hm_dld_j, max(hm_dld_j), out=np.zeros_like(hm_dld_j, dtype=np.float64), where=max(hm_dld_j) != 0,
                       casting="unsafe")
    for i in range(len(hm_dld_j)):
        hm_ck_dld_j_color.append("%.2f%%" % (arrayA[i] * 100))
    if hm_dld_j[0] == 'nan%':
        a = 0
        for i in range(len(hm_dld_j)):
            hm_dld_j[i] = '{:.2%}'.format(a)

    arrayA = np.divide(hm_djh_j, max(hm_djh_j), out=np.zeros_like(hm_djh_j, dtype=np.float64), casting="unsafe",
                       where=max(hm_djh_j) != 0)
    for i in range(len(hm_djh_j)):
        hm_ck_djh_j_color.append("%.2f%%" % (arrayA[i] * 100))
    if hm_djh_j[0] == 'nan%':
        a = 0
        for i in range(len(hm_djh_j)):
            hm_djh_j[i] = '{:.2%}'.format(a)

    arrayA = np.divide(hm_ddb_j, max(hm_ddb_j), out=np.zeros_like(hm_ddb_j, dtype=np.float64), casting="unsafe",
                       where=max(hm_ddb_j) != 0)
    for i in range(len(hm_ddb_j)):
        hm_ck_ddb_j_color.append("%.2f%%" % (arrayA[i] * 100))
    if hm_ddb_j[0] == 'nan%':
        a = 0
        for i in range(len(hm_ddb_j)):
            hm_ddb_j[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_dck_j, max(hm_dck_j), out=np.zeros_like(hm_dck_j, dtype=np.float64), casting="unsafe",
                       where=max(hm_dck_j) != 0)
    for i in range(len(hm_dck_j)):
        hm_ck_dck_j_color.append("%.2f%%" % (arrayA[i] * 100))
    if hm_dck_j[0] == 'nan%':
        a = 0
        for i in range(len(hm_dck_j)):
            hm_dck_j[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_djy_j, max(hm_djy_j), out=np.zeros_like(hm_djy_j, dtype=np.float64), casting="unsafe",
                       where=max(hm_djy_j) != 0)
    for i in range(len(hm_djy_j)):
        hm_ck_djy_j_color.append("%.2f%%" % (arrayA[i] * 100))
    if hm_djy_j[0] == 'nan%':
        a = 0
        for i in range(len(hm_djy_j)):
            hm_djy_j[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_dld_b, max(hm_dld_b), out=np.zeros_like(hm_dld_b, dtype=np.float64), casting="unsafe",
                       where=max(hm_dld_b) != 0)
    for i in range(len(hm_dld_b)):
        hm_ck_dld_b_color.append("%.2f%%" % (arrayA[i] * 100))
    if hm_dld_b[0] == 'nan%':
        a = 0
        for i in range(len(hm_dld_b)):
            hm_dld_b[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_djh_b, max(hm_djh_b), out=np.zeros_like(hm_djh_b, dtype=np.float64), casting="unsafe",
                       where=max(hm_djh_b) != 0)
    for i in range(len(hm_djh_b)):
        hm_ck_djh_b_color.append("%.2f%%" % (arrayA[i] * 100))
    if hm_djh_b[0] == 'nan%':
        a = 0
        for i in range(len(hm_djh_b)):
            hm_djh_b[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_ddb_b, max(hm_ddb_b), out=np.zeros_like(hm_ddb_b, dtype=np.float64), casting="unsafe",
                       where=max(hm_ddb_b) != 0)
    for i in range(len(hm_ddb_b)):
        hm_ck_ddb_b_color.append("%.2f%%" % (arrayA[i] * 100))
    if hm_ddb_b[0] == 'nan%':
        a = 0
        for i in range(len(hm_ddb_b)):
            hm_ddb_b[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_dck_b, max(hm_dck_b), out=np.zeros_like(hm_dck_b, dtype=np.float64), casting="unsafe",
                       where=max(hm_dck_b) != 0)
    for i in range(len(hm_dck_b)):
        hm_ck_dck_b_color.append("%.2f%%" % (arrayA[i] * 100))
    if hm_dck_b[0] == 'nan%':
        a = 0
        for i in range(len(hm_dck_b)):
            hm_dck_b[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_djy_b, max(hm_djy_b), out=np.zeros_like(hm_djy_b, dtype=np.float64), casting="unsafe",
                       where=max(hm_djy_b) != 0)
    for i in range(len(hm_djy_b)):
        hm_ck_djy_b_color.append("%.2f%%" % (arrayA[i] * 100))
    if hm_djy_b[0] == 'nan%':
        a = 0
        for i in range(len(hm_djy_b)):
            hm_djy_b[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_dld_j, max(tx_dld_j), out=np.zeros_like(tx_dld_j, dtype=np.float64), casting="unsafe",
                       where=max(tx_dld_j) != 0)
    for i in range(len(tx_dld_j)):
        tx_ck_dld_j_color.append("%.2f%%" % (arrayA[i] * 100))
    if tx_dld_j[0] == 'nan%':
        a = 0
        for i in range(len(tx_dld_j)):
            tx_dld_j[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_djh_j, max(tx_djh_j), out=np.zeros_like(tx_djh_j, dtype=np.float64), casting="unsafe",
                       where=max(tx_djh_j) != 0)
    for i in range(len(tx_djh_j)):
        tx_ck_djh_j_color.append("%.2f%%" % (arrayA[i] * 100))
    if tx_djh_j[0] == 'nan%':
        a = 0
        for i in range(len(tx_djh_j)):
            tx_djh_j[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_ddb_j, max(tx_ddb_j), out=np.zeros_like(tx_ddb_j, dtype=np.float64), casting="unsafe",
                       where=max(tx_ddb_j) != 0)
    for i in range(len(tx_ddb_j)):
        tx_ck_ddb_j_color.append("%.2f%%" % (arrayA[i] * 100))
    if tx_ddb_j[0] == 'nan%':
        a = 0
        for i in range(len(tx_ddb_j)):
            tx_ddb_j[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_dck_j, max(tx_dck_j), out=np.zeros_like(tx_dck_j, dtype=np.float64), casting="unsafe",
                       where=max(tx_dck_j) != 0)
    for i in range(len(tx_dck_j)):
        tx_ck_dck_j_color.append("%.2f%%" % (arrayA[i] * 100))
    if tx_dck_j[0] == 'nan%':
        a = 0
        for i in range(len(tx_dck_j)):
            tx_dck_j[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_djy_j, max(tx_djy_j), out=np.zeros_like(tx_djy_j, dtype=np.float64), casting="unsafe",
                       where=max(tx_djy_j) != 0)
    for i in range(len(tx_djy_j)):
        tx_ck_djy_j_color.append("%.2f%%" % (arrayA[i] * 100))
    if tx_djy_j[0] == 'nan%':
        a = 0
        for i in range(len(tx_djy_j)):
            tx_djy_j[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_dld_b, max(tx_dld_b), out=np.zeros_like(tx_dld_b, dtype=np.float64), casting="unsafe",
                       where=max(tx_dld_b) != 0)
    for i in range(len(tx_dld_b)):
        tx_ck_dld_b_color.append("%.2f%%" % (arrayA[i] * 100))
    if tx_dld_b[0] == 'nan%':
        a = 0
        for i in range(len(tx_dld_b)):
            tx_dld_b[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_djh_b, max(tx_djh_b), out=np.zeros_like(tx_djh_b, dtype=np.float64), casting="unsafe",
                       where=max(tx_djh_b) != 0)
    for i in range(len(tx_djh_b)):
        tx_ck_djh_b_color.append("%.2f%%" % (arrayA[i] * 100))
    if tx_djh_b[0] == 'nan%':
        a = 0
        for i in range(len(tx_djh_b)):
            tx_djh_b[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_ddb_b, max(tx_ddb_b), out=np.zeros_like(tx_ddb_b, dtype=np.float64), casting="unsafe",
                       where=max(tx_ddb_b) != 0)
    for i in range(len(tx_ddb_b)):
        tx_ck_ddb_b_color.append("%.2f%%" % (arrayA[i] * 100))
    if tx_ddb_b[0] == 'nan%':
        a = 0
        for i in range(len(tx_ddb_b)):
            tx_ddb_b[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_dck_b, max(tx_dck_b), out=np.zeros_like(tx_dck_b, dtype=np.float64), casting="unsafe",
                       where=max(tx_dck_b) != 0)
    for i in range(len(tx_dck_b)):
        tx_ck_dck_b_color.append("%.2f%%" % (arrayA[i] * 100))
    if tx_dck_b[0] == 'nan%':
        a = 0
        for i in range(len(tx_dck_b)):
            tx_dck_b[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_djy_b, max(tx_djy_b), out=np.zeros_like(tx_djy_b, dtype=np.float64), casting="unsafe",
                       where=max(tx_djy_b) != 0)
    for i in range(len(tx_djy_b)):
        tx_ck_djy_b_color.append("%.2f%%" % (arrayA[i] * 100))
    if tx_djy_b[0] == 'nan%':
        a = 0
        for i in range(len(tx_djy_b)):
            tx_djy_b[i] = '{:.2%}'.format(a)

    jsonData['hm_dld_j'] = hm_dld_j
    jsonData['hm_dld_b'] = hm_dld_b
    jsonData['hm_djh_j'] = hm_djh_j
    jsonData['hm_djh_b'] = hm_djh_b
    jsonData['hm_ddb_j'] = hm_ddb_j
    jsonData['hm_ddb_b'] = hm_ddb_b
    jsonData['hm_dck_j'] = hm_dck_j
    jsonData['hm_dck_b'] = hm_dck_b
    jsonData['hm_djy_j'] = hm_djy_j
    jsonData['hm_djy_b'] = hm_djy_b
    jsonData['tx_dld_j'] = tx_dld_j
    jsonData['tx_dld_b'] = tx_dld_b
    jsonData['tx_djh_j'] = tx_djh_j
    jsonData['tx_djh_b'] = tx_djh_b
    jsonData['tx_ddb_j'] = tx_ddb_j
    jsonData['tx_ddb_b'] = tx_ddb_b
    jsonData['tx_dck_j'] = tx_dck_j
    jsonData['tx_dck_b'] = tx_dck_b
    jsonData['tx_djy_j'] = tx_djy_j
    jsonData['tx_djy_b'] = tx_djy_b
    jsonData['hm_ck_dld_j_color'] = hm_ck_dld_j_color
    jsonData['hm_ck_djh_j_color'] = hm_ck_djh_j_color
    jsonData['hm_ck_ddb_j_color'] = hm_ck_ddb_j_color
    jsonData['hm_ck_dck_j_color'] = hm_ck_dck_j_color
    jsonData['hm_ck_djy_j_color'] = hm_ck_djy_j_color
    jsonData['hm_ck_dld_b_color'] = hm_ck_dld_b_color
    jsonData['hm_ck_djh_b_color'] = hm_ck_djh_b_color
    jsonData['hm_ck_ddb_b_color'] = hm_ck_ddb_b_color
    jsonData['hm_ck_dck_b_color'] = hm_ck_dck_b_color
    jsonData['hm_ck_djy_b_color'] = hm_ck_djy_b_color
    jsonData['tx_ck_dld_j_color'] = tx_ck_dld_j_color
    jsonData['tx_ck_djh_j_color'] = tx_ck_djh_j_color
    jsonData['tx_ck_ddb_j_color'] = tx_ck_ddb_j_color
    jsonData['tx_ck_dck_j_color'] = tx_ck_dck_j_color
    jsonData['tx_ck_djy_j_color'] = tx_ck_djy_j_color
    jsonData['tx_ck_dld_b_color'] = tx_ck_dld_b_color
    jsonData['tx_ck_djh_b_color'] = tx_ck_djh_b_color
    jsonData['tx_ck_ddb_b_color'] = tx_ck_ddb_b_color
    jsonData['tx_ck_dck_b_color'] = tx_ck_dck_b_color
    jsonData['tx_ck_djy_b_color'] = tx_ck_djy_b_color

    hm_order_id = []
    hm_status = []
    hm_num = []
    hm_s = []
    tx_order_id = []
    tx_status = []
    tx_num = []
    tx_s = []
    for i in range(len(warehouse)):
        if warehouse[i] == 'HM_AA':
            hm_order_id.append(order_id[i])
            hm_status.append(status[i])
            hm_num.append(num[i])
            hm_s.append(s[i])
    for i in range(len(warehouse)):
        if warehouse[i] == 'SZ_AA':
            tx_order_id.append(order_id[i])
            tx_status.append(status[i])
            tx_num.append(num[i])
            tx_s.append(s[i])
    print(tx_s)
    hm_data = np.dstack((hm_order_id, hm_status, hm_num, hm_s))
    tx_data = np.dstack((tx_order_id, tx_status, tx_num, tx_s))
    hm_drk_order = []
    hm_drk_s = []
    hm_rkz_s = []
    hm_drk_num = []
    hm_rkz_num = []
    tx_drk_s = []
    tx_rkz_s = []
    tx_drk_num = []
    tx_rkz_num = []
    for i in range(len(hm_data[0])):
        if (hm_data[0][i][1] == 1):
            hm_drk_num.append(hm_data[0][i][2])
            hm_drk_s.append(hm_data[0][i][3])
            hm_drk_order.append(hm_data[0][i][0])
    for i in range(len(hm_data[0])):
        if (hm_data[0][i][1] == 2):
            hm_rkz_num.append(hm_data[0][i][2])
            hm_rkz_s.append(hm_data[0][i][3])
    for i in range(len(tx_data[0])):
        if (tx_data[0][i][1] == 1):
            tx_drk_num.append(tx_data[0][i][2])
            tx_drk_s.append(tx_data[0][i][3])
    for i in range(len(tx_data[0])):
        if (tx_data[0][i][1] == 2):
            tx_rkz_num.append(tx_data[0][i][2])
            tx_rkz_s.append(tx_data[0][i][3])
    # 去重
    a1 = []
    a2 = []
    hm_drk_order = []
    hm_drk_s2 = []

    for i in range(len(hm_data[0])):
        if hm_data[0][i][0] not in a2 and hm_data[0][i][1] == 1:
            a1.append(hm_data[0][i])
        a2.append(hm_data[0][i][0])
    for i in range(len(a1)):
        hm_drk_order.append(a1[i][0])
        hm_drk_s2.append(a1[i][3])
    # print(hm_drk_order)

    a1 = []
    a2 = []
    hm_rkz_order = []
    hm_rkz_s2 = []
    for i in range(len(hm_data[0])):
        if hm_data[0][i][0] not in a2 and hm_data[0][i][1] == 2:
            a1.append(hm_data[0][i])
        a2.append(hm_data[0][i][0])
    for i in range(len(a1)):
        hm_rkz_order.append(a1[i][0])
        hm_rkz_s2.append(a1[i][3])
    # 去重
    a1 = []
    a2 = []
    tx_drk_order = []
    tx_drk_s2 = []
    for i in range(len(tx_data[0])):
        if tx_data[0][i][0] not in a2 and tx_data[0][i][1] == 1:
            a1.append(tx_data[0][i])
        a2.append(tx_data[0][i][0])
    for i in range(len(a1)):
        tx_drk_order.append(a1[i][0])
        tx_drk_s2.append(a1[i][3])
    a1 = []
    a2 = []
    tx_rkz_order = []
    tx_rkz_s2 = []
    for i in range(len(tx_data[0])):
        if tx_data[0][i][0] not in a2 and tx_data[0][i][1] == 2:
            a1.append(tx_data[0][i])
        a2.append(tx_data[0][i][0])
    for i in range(len(a1)):
        tx_rkz_order.append(a1[i][0])
        tx_rkz_s2.append(a1[i][3])
    hm_drk = np.dstack((hm_drk_num, hm_drk_s))
    hm_drk2 = np.dstack((hm_drk_order, hm_drk_s2))
    hm_rkz = np.dstack((hm_rkz_num, hm_rkz_s))
    hm_rkz2 = np.dstack((hm_rkz_order, hm_rkz_s2))
    tx_drk = np.dstack((tx_drk_num, tx_drk_s))
    tx_rkz = np.dstack((tx_rkz_num, tx_rkz_s))
    tx_drk2 = np.dstack((tx_drk_order, tx_drk_s2))
    tx_rkz2 = np.dstack((tx_rkz_order, tx_rkz_s2))
    hm_drk_b = [0, 0, 0, 0, 0, 0, 0]
    hm_drk_j = [0, 0, 0, 0, 0, 0, 0]
    hm_rkz_b = [0, 0, 0, 0, 0, 0, 0]
    hm_rkz_j = [0, 0, 0, 0, 0, 0, 0]
    tx_drk_b = [0, 0, 0, 0, 0, 0, 0]
    tx_drk_j = [0, 0, 0, 0, 0, 0, 0]
    tx_rkz_b = [0, 0, 0, 0, 0, 0, 0]
    tx_rkz_j = [0, 0, 0, 0, 0, 0, 0]

    for i in range(len(hm_drk[0])):
        if float(hm_drk_s[i]) > 0 and float(hm_drk_s[i]) <= 12:
            hm_drk_j[0] = hm_drk_j[0] + hm_drk[0][i][0]
        if float(hm_drk_s[i]) > 12 and float(hm_drk_s[i]) <= 24:
            hm_drk_j[1] = hm_drk_j[1] + hm_drk[0][i][0]
        if float(hm_drk_s[i]) > 24 and float(hm_drk_s[i]) <= 168:
            hm_drk_j[2] = hm_drk_j[2] + hm_drk[0][i][0]
        if float(hm_drk_s[i]) > 168 and float(hm_drk_s[i]) <= 360:
            hm_drk_j[3] = hm_drk_j[3] + hm_drk[0][i][0]
        if float(hm_drk_s[i]) > 360 and float(hm_drk_s[i]) <= 720:
            hm_drk_j[4] = hm_drk_j[4] + hm_drk[0][i][0]
        if float(hm_drk_s[i]) > 720:
            hm_drk_j[5] = hm_drk_j[5] + hm_drk[0][i][0]
        hm_drk_j[6] = hm_drk_j[6] + hm_drk[0][i][0]
    for i in range(len(hm_drk2[0])):
        if float(hm_drk_s2[i]) > 0 and float(hm_drk_s2[i]) <= 12:
            hm_drk_b[0] = hm_drk_b[0] + 1
        if float(hm_drk_s2[i]) > 12 and float(hm_drk_s2[i]) <= 24:
            hm_drk_b[1] = hm_drk_b[1] + 1
        if float(hm_drk_s2[i]) > 24 and float(hm_drk_s2[i]) <= 168:
            hm_drk_b[2] = hm_drk_b[2] + 1
        if float(hm_drk_s2[i]) > 168 and float(hm_drk_s2[i]) <= 360:
            hm_drk_b[3] = hm_drk_b[3] + 1
        if float(hm_drk_s2[i]) > 360 and float(hm_drk_s2[i]) <= 720:
            hm_drk_b[4] = hm_drk_b[4] + 1
        if float(hm_drk_s2[i]) > 720:
            hm_drk_b[5] = hm_drk_b[5] + 1
        hm_drk_b[6] = hm_drk_b[6] + 1
    for i in range(len(hm_rkz[0])):
        if float(hm_rkz_s[i]) > 0 and float(hm_rkz_s[i]) <= 12:
            hm_rkz_j[0] = hm_rkz_j[0] + hm_rkz[0][i][0]
        if float(hm_rkz_s[i]) > 12 and float(hm_rkz_s[i]) <= 24:
            hm_rkz_j[1] = hm_rkz_j[1] + hm_rkz[0][i][0]
        if float(hm_rkz_s[i]) > 24 and float(hm_rkz_s[i]) <= 168:
            hm_rkz_j[2] = hm_rkz_j[2] + hm_rkz[0][i][0]
        if float(hm_rkz_s[i]) > 168 and float(hm_rkz_s[i]) <= 360:
            hm_rkz_j[3] = hm_rkz_j[3] + hm_rkz[0][i][0]
        if float(hm_rkz_s[i]) > 360 and float(hm_rkz_s[i]) <= 720:
            hm_rkz_j[4] = hm_rkz_j[4] + hm_rkz[0][i][0]
        if float(hm_rkz_s[i]) > 720:
            hm_rkz_j[5] = hm_rkz_j[5] + hm_rkz[0][i][0]
        hm_rkz_j[6] = hm_rkz_j[6] + hm_rkz[0][i][0]

    for i in range(len(hm_rkz2[0])):
        if float(hm_rkz_s2[i]) > 0 and float(hm_rkz_s2[i]) <= 12:
            hm_rkz_b[0] = hm_rkz_b[0] + 1
        if float(hm_rkz_s2[i]) > 12 and float(hm_rkz_s2[i]) <= 24:
            hm_rkz_b[1] = hm_rkz_b[1] + 1
        if float(hm_rkz_s2[i]) > 24 and float(hm_rkz_s2[i]) <= 168:
            hm_rkz_b[2] = hm_rkz_b[2] + 1
        if float(hm_rkz_s2[i]) > 168 and float(hm_rkz_s2[i]) <= 360:
            hm_rkz_b[3] = hm_rkz_b[3] + 1
        if float(hm_rkz_s2[i]) > 360 and float(hm_rkz_s2[i]) <= 720:
            hm_rkz_b[4] = hm_rkz_b[4] + 1
        if float(hm_rkz_s2[i]) > 720:
            hm_rkz_b[5] = hm_rkz_b[5] + 1
        hm_rkz_b[6] = hm_rkz_b[6] + 1
    for i in range(len(tx_drk[0])):
        if float(tx_drk_s[i]) > 0 and float(tx_drk_s[i]) <= 12:
            tx_drk_j[0] = tx_drk_j[0] + tx_drk[0][i][0]
        if float(tx_drk_s[i]) > 12 and float(tx_drk_s[i]) <= 24:
            tx_drk_j[1] = tx_drk_j[1] + tx_drk[0][i][0]
        if float(tx_drk_s[i]) > 24 and float(tx_drk_s[i]) <= 168:
            tx_drk_j[2] = tx_drk_j[2] + tx_drk[0][i][0]
        if float(tx_drk_s[i]) > 168 and float(tx_drk_s[i]) <= 360:
            tx_drk_j[3] = tx_drk_j[3] + tx_drk[0][i][0]
        if float(tx_drk_s[i]) > 360 and float(tx_drk_s[i]) <= 720:
            tx_drk_j[4] = tx_drk_j[4] + tx_drk[0][i][0]
        if float(tx_drk_s[i]) > 720:
            tx_drk_j[5] = tx_drk_j[5] + tx_drk[0][i][0]
        tx_drk_j[6] = tx_drk_j[6] + tx_drk[0][i][0]
    for i in range(len(tx_drk2[0])):
        if float(tx_drk_s2[i]) > 0 and float(tx_drk_s2[i]) <= 12:
            tx_drk_b[0] = tx_drk_b[0] + 1
        if float(tx_drk_s2[i]) > 12 and float(tx_drk_s2[i]) <= 24:
            tx_drk_b[1] = tx_drk_b[1] + 1
        if float(tx_drk_s2[i]) > 24 and float(tx_drk_s2[i]) <= 168:
            tx_drk_b[2] = tx_drk_b[2] + 1
        if float(tx_drk_s2[i]) > 168 and float(tx_drk_s2[i]) <= 360:
            tx_drk_b[3] = tx_drk_b[3] + 1
        if float(tx_drk_s2[i]) > 360 and float(tx_drk_s2[i]) <= 720:
            tx_drk_b[4] = tx_drk_b[4] + 1
        if float(tx_drk_s2[i]) > 720:
            tx_drk_b[5] = tx_drk_b[5] + 1
        tx_drk_b[6] = tx_drk_b[6] + 1
    for i in range(len(tx_rkz[0])):
        if float(tx_rkz_s[i]) > 0 and float(tx_rkz_s[i]) <= 12:
            tx_rkz_j[0] = tx_rkz_j[0] + tx_rkz[0][i][0]
        if float(tx_rkz_s[i]) > 12 and float(tx_rkz_s[i]) <= 24:
            tx_rkz_j[1] = tx_rkz_j[1] + tx_rkz[0][i][0]
        if float(tx_rkz_s[i]) > 24 and float(tx_rkz_s[i]) <= 168:
            tx_rkz_j[2] = tx_rkz_j[2] + tx_rkz[0][i][0]
        if float(tx_rkz_s[i]) > 168 and float(tx_rkz_s[i]) <= 360:
            tx_rkz_j[3] = tx_rkz_j[3] + tx_rkz[0][i][0]
        if float(tx_rkz_s[i]) > 360 and float(tx_rkz_s[i]) <= 720:
            tx_rkz_j[4] = tx_rkz_j[4] + tx_rkz[0][i][0]
        if float(tx_rkz_s[i]) > 720:
            tx_rkz_j[5] = tx_rkz_j[5] + tx_rkz[0][i][0]
        tx_rkz_j[6] = tx_rkz_j[6] + tx_rkz[0][i][0]
    for i in range(len(tx_rkz2[0])):
        if float(tx_rkz_s2[i]) > 0 and float(tx_rkz_s2[i]) <= 12:
            tx_rkz_b[0] = tx_rkz_b[0] + 1
        if float(tx_rkz_s2[i]) > 12 and float(tx_rkz_s2[i]) <= 24:
            tx_rkz_b[1] = tx_rkz_b[1] + 1
        if float(tx_rkz_s2[i]) > 24 and float(tx_rkz_s2[i]) <= 168:
            tx_rkz_b[2] = tx_rkz_b[2] + 1
        if float(tx_rkz_s2[i]) > 168 and float(tx_rkz_s2[i]) <= 360:
            tx_rkz_b[3] = tx_rkz_b[3] + 1
        if float(tx_rkz_s2[i]) > 360 and float(tx_rkz_s2[i]) <= 720:
            tx_rkz_b[4] = tx_rkz_b[4] + 1
        if float(tx_rkz_s2[i]) > 720:
            tx_rkz_b[5] = tx_rkz_b[5] + 1
        tx_rkz_b[6] = tx_rkz_b[6] + 1
    hm_drk_b_color = []
    hm_drk_j_color = []
    hm_rkz_b_color = []
    hm_rkz_j_color = []
    tx_drk_b_color = []
    tx_drk_j_color = []
    tx_rkz_b_color = []
    tx_rkz_j_color = []

    arrayA = np.divide(hm_drk_b, max(hm_drk_b), out=np.zeros_like(hm_drk_b, dtype=np.float64),
                       where=max(hm_drk_b) != 0)
    for i in range(len(hm_drk_b)):
        hm_drk_b_color.append("%.2f%%" % (arrayA[i] * 100))
    if hm_drk_b[0] == 'nan%':
        a = 0
        for i in range(len(hm_drk_b)):
            hm_drk_b[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_drk_j, max(hm_drk_j), out=np.zeros_like(hm_drk_j, dtype=np.float64),
                       where=max(hm_drk_j) != 0,casting="unsafe")
    for i in range(len(hm_drk_j)):
        hm_drk_j_color.append("%.2f%%" % (arrayA[i] * 100))
    if hm_drk_j[0] == 'nan%':
        a = 0
        for i in range(len(hm_drk_j)):
            hm_drk_j[i] = '{:.2%}'.format(a)
    print(hm_drk_j_color)
    arrayA = np.divide(hm_rkz_b, max(hm_rkz_b), out=np.zeros_like(hm_rkz_b, dtype=np.float64),
                       where=max(hm_rkz_b) != 0)
    for i in range(len(hm_rkz_b)):
        hm_rkz_b_color.append("%.2f%%" % (arrayA[i] * 100))
    if hm_rkz_b[0] == 'nan%':
        a = 0
        for i in range(len(hm_rkz_b)):
            hm_rkz_b[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_rkz_j, max(hm_rkz_j), out=np.zeros_like(hm_rkz_j, dtype=np.float64),
                       where=max(hm_rkz_j) != 0 ,casting="unsafe")
    for i in range(len(hm_rkz_j)):
        hm_rkz_j_color.append("%.2f%%" % (arrayA[i] * 100))
    if hm_rkz_j[0] == 'nan%':
        a = 0
        for i in range(len(hm_rkz_j)):
            hm_rkz_j[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_drk_b, max(tx_drk_b), out=np.zeros_like(tx_drk_b, dtype=np.float64),
                       where=max(tx_drk_b) != 0)
    for i in range(len(tx_drk_b)):
        tx_drk_b_color.append("%.2f%%" % (arrayA[i] * 100))
    if tx_drk_b[0] == 'nan%':
        a = 0
        for i in range(len(tx_drk_b)):
            tx_drk_b[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_drk_j, max(tx_drk_j), out=np.zeros_like(tx_drk_j, dtype=np.float64),
                       where=max(tx_drk_j) != 0,casting="unsafe")
    for i in range(len(tx_drk_j)):
        tx_drk_j_color.append("%.2f%%" % (arrayA[i] * 100))
    if tx_drk_j[0] == 'nan%':
        a = 0
        for i in range(len(tx_drk_j)):
            tx_drk_j[i] = '{:.2%}'.format(a)

    arrayA = np.divide(tx_rkz_b, max(tx_rkz_b), out=np.zeros_like(tx_rkz_b, dtype=np.float64),
                       where=max(tx_rkz_b) != 0)
    for i in range(len(tx_rkz_b)):
        tx_rkz_b_color.append("%.2f%%" % (arrayA[i] * 100))
    if tx_rkz_b[0] == 'nan%':
        a = 0
        for i in range(len(tx_rkz_b)):
            tx_rkz_b[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_rkz_j, max(tx_rkz_j), out=np.zeros_like(tx_rkz_j, dtype=np.float64),
                       where=max(tx_rkz_j) != 0,casting="unsafe")
    for i in range(len(tx_rkz_j)):
        tx_rkz_j_color.append("%.2f%%" % (arrayA[i] * 100))
    if tx_rkz_j[0] == 'nan%':
        a = 0
        for i in range(len(tx_rkz_j)):
            tx_rkz_j[i] = '{:.2%}'.format(a)
    # 看这里
    arrayA = np.divide(tx_rkz_b, max(tx_rkz_b), out=np.zeros_like(tx_rkz_b, dtype=np.float64), where=max(tx_rkz_b) != 0)
    for i in range(len(tx_rkz_b)):
        tx_rkz_b_color.append("%.2f%%" % (arrayA[i] * 100))
    if tx_rkz_b[0] == 'nan%':
        a = 0
        for i in range(len(tx_rkz_b)):
            tx_rkz_b[i] = '{:.2%}'.format(a)

    arrayA = np.divide(tx_rkz_j, max(tx_rkz_j),casting="unsafe", out=np.zeros_like(tx_rkz_j, dtype=np.float64), where=max(tx_rkz_j) != 0)
    for i in range(len(tx_rkz_j)):
        tx_rkz_j_color.append("%.2f%%" % (arrayA[i] * 100))
    if tx_rkz_j[0] == 'nan%':
        a = 0
        for i in range(len(tx_rkz_j)):
            tx_rkz_j[i] = '{:.2%}'.format(a)
    jsonData['hm_drk_j'] = hm_drk_j
    jsonData['hm_drk_b'] = hm_drk_b
    jsonData['tx_drk_j'] = tx_drk_j
    jsonData['tx_drk_b'] = tx_drk_b
    jsonData['hm_rkz_j'] = hm_rkz_j
    jsonData['hm_rkz_b'] = hm_rkz_b
    jsonData['tx_rkz_j'] = tx_rkz_j
    jsonData['tx_rkz_b'] = tx_rkz_b
    jsonData['hm_drk_b_color'] = hm_drk_b_color
    jsonData['hm_drk_j_color'] = hm_drk_j_color
    jsonData['hm_rkz_b_color'] = hm_rkz_b_color
    jsonData['hm_rkz_j_color'] = hm_rkz_j_color
    jsonData['tx_drk_b_color'] = tx_drk_b_color
    jsonData['tx_drk_j_color'] = tx_drk_j_color
    jsonData['tx_rkz_b_color'] = tx_rkz_b_color
    jsonData['tx_rkz_j_color'] = tx_rkz_j_color
    jsonData['hm_drk_order'] = hm_drk_order
    jsonData['tx_drk_order'] = tx_drk_order
    jsonData['hm_drk_s2'] = hm_drk_s2
    jsonData['tx_drk_s2'] = tx_drk_s2
    jsonData['hm_ck_dld_order'] = hm_ck_dld_order
    jsonData['hm_ck_dld_s'] = hm_ck_dld_s
    jsonData['hm_ck_djh_order'] = hm_ck_djh_order
    jsonData['hm_ck_djh_s'] = hm_ck_djh_s
    jsonData['hm_ck_ddb_order'] = hm_ck_ddb_order
    jsonData['hm_ck_ddb_s'] = hm_ck_ddb_s
    jsonData['hm_ck_dck_order'] = hm_ck_dck_order
    jsonData['hm_ck_dck_s'] = hm_ck_dck_s
    jsonData['tx_ck_dld_order'] = tx_ck_dld_order
    jsonData['tx_ck_dld_s'] = tx_ck_dld_s
    jsonData['tx_ck_djh_order'] = tx_ck_djh_order
    jsonData['tx_ck_djh_s'] = tx_ck_djh_s
    jsonData['tx_ck_ddb_order'] = tx_ck_ddb_order
    jsonData['tx_ck_ddb_s'] = tx_ck_ddb_s
    jsonData['tx_ck_dck_order'] = tx_ck_dck_order
    jsonData['tx_ck_dck_s'] = tx_ck_dck_s
    # print(tx_drk_s2)
    j = json.dumps(jsonData, cls=DecimalEncoder)
    return (j)

@app.route('/采购日报.html')
def index_cg():
    return render_template("采购日报.html")


@app.route('/仓库日报.html')
def index_ck():
    return render_template('仓库日报.html')
@app.route('/仓库日报备份.html')
def index_ck23():
    return render_template('仓库日报备份.html')

@app.route('/daily1', methods=['POST'])
def index_jy_daily():
    # sql_jy = 'SELECT  warehouse_code,	sum(quality_num),	case	when paragraph in(1,3,4) then "DSJ"	when paragraph =11 then "DGNZJ" ELSE "ELSE" END a 	FROM	ueb_quality_warehousing_record WHERE	paragraph IN ( -1, 0, 1, 2, 3, 4, 11 ) 	AND type = 1  group by a,warehouse_code union		SELECT  warehouse_code,	sum(quality_num),	"DTM" as a FROM	ueb_quality_warehousing_record WHERE	paragraph IN ( -1, 0, 1, 2, 3, 4, 11 ) 	AND type = 1  and post_code =1	 group by warehouse_code UNION SELECT warehouse_code,count(order_id) as num , case when wh_order_status=-1 then "DPK" when wh_order_status IN(1,2) then "DLD" when wh_order_status=3 then "DJH" when wh_order_status=4 then "JHZ" when wh_order_status=7 then "DDB" when wh_order_status=8 then "DCK" ELSE "ELSE" END type FROM ueb_order WHERE batch_type != 6 and wh_order_status < 9  group by type,warehouse_code UNION SELECT warehouse_code,sum(order_product_number) num , case when wh_order_status=-1 then "FDPK" when wh_order_status IN(1) then "FDFPLD" when wh_order_status IN(2) then "FDLD" when wh_order_status=3 then "FDJH" when wh_order_status=4 then "FJHZ" when wh_order_status=7 then "FDDB" when wh_order_status=8 then "FDCK" when wh_order_status IN (9,19,20) then "FDJY"  ELSE "ELSE" END type FROM ueb_order WHERE batch_type = 6 and wh_order_status not in (10,11,14,13)  group by warehouse_code,type  union SELECT	real_warehouse_code,	count(DISTINCT  purchase_order_no ) AS num,CASE		WHEN `status` = 1 THEN	"DBDRK" 	WHEN `status` = 2 THEN	"DBRKZ" ELSE "else" 	END AS type FROM	ueb_purchase WHERE	is_del = 1 	AND warehouse_type = 1 	AND purchase_type IN ( 3, 4 ) 	AND real_warehouse_code IN ( "HM_AA", "SZ_AA" ) GROUP BY	real_warehouse_code,	type UNION SELECT warehouse_code,count(DISTINCT order_id), case when wh_order_status=-1 then "DBDPK" when wh_order_status IN(1,2) then "DBDLD" when wh_order_status=3 then "DBDJH"  when wh_order_status IN (4,7) then "DBDDB" when wh_order_status=8 then "DBDCK"  when wh_order_status IN (9,19,20) then "DBDJY" ELSE "ELSE" END type FROM ueb_order WHERE order_id LIKE "ALLOT%"   group by type,warehouse_code union SELECT	a.warehouse_code,	sum( a.quality_num ),	a.type AS num FROM	(SELECT	warehouse_code,	"RK" AS purchase_order_no,	car_no AS storage_position,	"RK" AS sku,	box_number AS quality_num,	"DRK" AS type,	cast( ROUND( ( unix_timestamp( now( ) ) - unix_timestamp( add_time ) ) / 3600, 2 ) AS DECIMAL ) AS s FROM	ueb_express_receipt WHERE	STATUS = 1 	AND warehouse_type = 1 	AND is_abnormal = "2" 	AND is_quality = "2" 	AND is_end = "1" 	) a GROUP BY	a.warehouse_code,	a.type ;'
    #sql_zl = 'SELECT	a.warehouse_code,	round(sum( a.available_qty * b.product_cost )/10000,2) AS total_cost,CASE				WHEN ROUND( ( unix_timestamp( now()) - unix_timestamp( a.update_time ) ) / 3600, 2 ) <= 24 THEN		"24" 		WHEN ROUND( ( unix_timestamp( now()) - unix_timestamp( a.update_time ) ) / 3600, 2 ) <= 48 AND ROUND( ( unix_timestamp( now()) - unix_timestamp( a.update_time ) ) / 3600, 2 ) > 24 THEN		"48" 		WHEN ROUND( ( unix_timestamp( now()) - unix_timestamp( a.update_time ) ) / 3600, 2 ) > 48 THEN		"48<" ELSE "" 	END AS s FROM	ueb_warehouse_shelf_sku_map a,	ueb_product b WHERE	a.warehouse_code IN ( "HM_AA", "SZ_AA" ) 	AND a.shelf_type NOT IN ( 11, 1, 20 ) 	AND b.product_cost > 0 	AND a.shelf NOT IN ( "MV0102", "MV0150", "WT0002", "WT0001", "MV0028", "MV0015", "MV0054" ) 	AND a.available_qty > 0 	AND a.sku = b.sku GROUP BY	a.warehouse_code,	s'
    # sql_sx = 'SELECT	a.Date,	a.warehouse_code,	"in" AS type,	round(	a.avg_delevery_time + a.avg_postcode_time + a.avg_quality_time +IF	( a.avg_quality_all_time IS NOT NULL, a.avg_quality_all_time, 0.0000 ) + a.avg_upper_end_time,	2 	) `total` FROM	(SELECT	date_format( upper_end_time, "%m-%d" ) Date,	warehouse_code,	avg( IF ( add_time > quality_start_time, timestampdiff( HOUR, quality_start_time, add_time ), NULL ) ) avg_delevery_time,	avg( IF ( post_code_end_time > add_time, timestampdiff( HOUR, add_time, post_code_end_time ), NULL ) ) avg_postcode_time,	avg( IF ( quality_time > post_code_end_time, timestampdiff( HOUR, post_code_end_time, quality_time ), timestampdiff( HOUR, quality_time, post_code_end_time ) ) ) avg_quality_time,	avg( IF ( quality_all_time > quality_time, timestampdiff( HOUR, quality_time, quality_all_time ), NULL ) ) avg_quality_all_time,	avg(IF	(	upper_end_time > quality_all_time 	AND quality_all_time > "2000-01-01",	timestampdiff( HOUR, quality_all_time, upper_end_time ),IF	(	upper_end_time > quality_time 	AND quality_time > post_code_end_time,	timestampdiff( HOUR, quality_time, upper_end_time ),IF	( upper_end_time > post_code_end_time AND post_code_end_time > quality_time, timestampdiff( HOUR, quality_time, upper_end_time ), NULL ) 	) 	) 	) avg_upper_end_time FROM	ueb_quality_warehousing_record WHERE	type = 1 	AND paragraph = 5 	AND quality_start_time > 0 	AND add_time > 0 	AND post_code_end_time > 0 	AND upper_end_time > "2020-01-01" 	AND TO_DAYS( NOW( ) ) - TO_DAYS( upper_end_time ) IN ( 1, 2, 3, 4, 5, 6, 7 ) GROUP BY	warehouse_code,	date_format( upper_end_time, "%m-%d" ) 	) a UNION	 SELECT date ,	CASE						WHEN a.warehouse_code = "HM_AA" THEN			"HM_AA" 			WHEN a.warehouse_code = "SZ_AA" THEN			"SZ_AA" ELSE "1" 		END AS warehouse_code,"out" as type, round((pull_time - wait_pull_time)/3600,2)+round((pick_time - pull_time)/3600,2)+round((scaner_time - pick_time)/3600,2)+round((scaner_last_time - scaner_time)/3600,2)as total FROM (		SELECT  date_format( from_unixtime( outstock_time ), "%m-%d" ) date,  warehouse_code,	avg( wait_pull_time) AS wait_pull_time,	avg( pull_time ) AS pull_time,	avg( pick_time ) AS pick_time,	avg( pack_time ) AS scaner_time,	avg( outstock_time ) AS scaner_last_time,	avg( abnormal_time ) AS abnormal_time,	avg( choice_time ) AS collected_time FROM	`ueb_order_operate_time` WHERE	TO_DAYS( NOW( ) ) - TO_DAYS( date_format( from_unixtime( outstock_time ), "%Y-%m-%d" ) ) in (1,2,3,4,5,6,7)	AND `wait_pull_time` > 0 	AND `pull_time` > 0 	AND `pick_time` > 0 	AND `pack_time` > 0 	AND `outstock_time` > 0 	AND `delivery_time` > 0 	AND `pick_time` > 0 	AND `pack_time` > 0 	AND `batch_no` NOT LIKE "%-6-%"group by warehouse_code,date_format( from_unixtime( outstock_time ), "%Y-%m-%d" ) )a UNION	SELECT		a.`date`,	CASE						WHEN a.warehouse = "HM_AA" THEN			"HM_AA" 			WHEN a.warehouse = "SZ_AA" THEN			"SZ_AA" ELSE "1" 		END AS warehouse_code,    "FBA" as type, 		a.avg_pull_time + a.avg_pick_time + a.avg_post_time+a.avg_pack_time + a.avg_outstock_time AS total 	FROM		(		SELECT			date_format( from_unixtime( outstock_time ), "%m-%d" ) AS date,			warehouse_code AS warehouse,		IF			( wait_pull_time != 0 AND pull_time != 0, ROUND(( avg( pull_time )- avg( wait_pull_time ))/ 3600, 2 ), NULL ) AS avg_pull_time,			ROUND(( avg( pick_time )- avg( pull_time ))/ 3600, 2 ) AS avg_pick_time,			ROUND( avg(( choice_time ) - ( pick_time ))/ 3600, 2 ) AS avg_post_time,			ROUND( avg(( pack_time ) - ( choice_time ))/ 3600, 2 ) AS avg_pack_time,		IF			(				pack_time != 0 				AND outstock_time != 0,				ROUND( ( avg( outstock_time ) - avg( pack_time ) ) / 3600, 2 ),			NULL 			) AS avg_outstock_time 		FROM			ueb_order_operate_time 		WHERE			order_is_cancel = 0 			AND order_id LIKE "FB%" 			AND pick_time != 0 			and choice_time != 0			AND TO_DAYS( NOW( ) ) - TO_DAYS( date_format( from_unixtime( outstock_time ), "%Y-%m-%d" ) ) in (1,2,3,4,5,6,7)		GROUP BY			warehouse_code,		date_format( from_unixtime( outstock_time ), "%m-%d" )) a;							'
    #sql_rk = 'SELECT	CASE 	WHEN warehouse_code = "AFN"  THEN "HM_AA"  WHEN warehouse_code = "HM_AA" THEN "HM_AA"	WHEN warehouse_code = "SZ_AA" THEN "SZ_AA"	ELSE "ELSE" END AS `仓库`,	add_time AS `日期`,	"in" as type ,	IFNULL( sum( JSON_UNQUOTE( JSON_EXTRACT( work_parme_num, "$.delivery.delivery.piece_total" ))), 0 ) AS `num`	FROM	`ueb_work_num_log_history` WHERE	add_time NOT IN ( "num", "user_name", "warehouse_code" ) and TO_DAYS(NOW( )) - TO_DAYS( add_time) = 1 GROUP BY	仓库,	add_time  union  	SELECT	CASE 	WHEN warehouse_code = "AFN"  THEN "HM_AA"  WHEN warehouse_code = "HM_AA" THEN "HM_AA"	WHEN warehouse_code = "SZ_AA" THEN "SZ_AA"	ELSE "ELSE" END AS `仓库`,	add_time AS `日期`,	"out" as type ,	IFNULL(sum(	JSON_UNQUOTE(JSON_EXTRACT( work_parme_num,"$.pack.pack_sku_bao.piece_total" ))),0) +	IFNULL(sum( JSON_UNQUOTE(JSON_EXTRACT( work_parme_num,"$.pack.pack_single.piece_total" ))),0) +	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_multi.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_zf.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_ex_order.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_singl_more.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_express.piece_total"))),0) +	IFNULL(sum(	JSON_UNQUOTE(JSON_EXTRACT( work_parme_num,"$.pack.pack_sku_bao.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE( JSON_EXTRACT( work_parme_num, "$.FBA.FBA.piece_total" ))),0) AS `num`	FROM	`ueb_work_num_log_history` WHERE	add_time NOT IN ( "num", "user_name", "warehouse_code" )  and TO_DAYS( NOW( ) ) - TO_DAYS( add_time ) = 1 GROUP BY	仓库,	add_time  union	  SELECT	a.warehouse_code,	date_format( from_unixtime( a.pull_time ), "%Y-%m-%d" ) AS date,	"LD" AS `type`,	count( a.order_id ) AS num FROM	ueb_order_operate_time a WHERE	a.pack_time IS NOT NULL 	AND TO_DAYS( NOW( ) ) - TO_DAYS( date_format(from_unixtime( a.pull_time ), "%Y-%m-%d" ) ) = 1 GROUP BY	a.warehouse_code,	date'
    # sql_tph = 'select DATE_FORMAT(a.date,"%m-%d") date,a.warehouse, round(a.`work`/b.`hour`,1) AS TPH ,round(a.`work2`/b.`hour`,1) AS UPH from(SELECT 	DATE_FORMAT(add_time,"%Y-%m-%d") AS `date`,	case	when warehouse_code = "HM_AA" THEN "HM_AA"	when warehouse_code = "AFN" Then "HM_AA"	when warehouse_code = "SZ_AA" then "SZ_AA"	else "else" end  as 	warehouse,	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "	$.instock.question_instock.piece_total"))),0) +	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.instock.instock.piece_total" ))),0) +	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.instock.return_instock.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num,"$.pack.pack_single.piece_total" ))),0) +	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_multi.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_zf.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_ex_order.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_singl_more.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_express.piece_total"))),0) +	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num,"$.pack.pack_sku_bao.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.FBA.FBA.piece_total" ))),0) AS `work`,	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num,"$.pack.pack_single.piece_total" ))),0) +	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_multi.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_zf.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_ex_order.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_singl_more.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_express.piece_total"))),0) +	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num,"$.pack.pack_sku_bao.piece_total" ))),0)+	IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.FBA.FBA.piece_total" ))),0) as `work2`FROM	`ueb_work_num_log_history` WHERE	add_time NOT IN ( "num", "user_name", "warehouse_code" ) and TO_DAYS( NOW( ) ) - TO_DAYS( add_time ) in (1,2,3,4,5,6,7) and warehouse_code not in ("shzz","CX")GROUP BY DATE_FORMAT(add_time,"%Y-%m-%d")	,warehouse )a ,(select date,warehouse_code,sum(`hour`) as `hour` from (SELECT	warehouse_code,	date,	`group`,	sum( HOUR ) `hour` FROM	((SELECT	a.warehouse_code,	a.date,	a.`group`,	(	a.temporary_hour +	a.group_leader + 	a.receive_hour + 	a.instock_hour + 	a.return_deal + 	a.allocate_instock + 	a.working_hour + 	a.all_quality + 	a.instock_putaway + 	a.return_putaway + 	a.problem_putaway +	a.pick_hour +	a.move_hour +	a.inventory_hour +	a.check_hour + 	a.second_pick + 	a.pack_hour + 	a.channel_pick + 	a.scan_weigh + 	a.delivery_hour +	a.fba_change + 	a.fba_pack + 	a.fba_delivery +	a.iqc_hour + 	a.confirm_exception +	a.instock_exception +	a.warehouse_exception + 	a.order_exception + 	a.transit_receive +	a.transit_pack + 	a.transit_send + 	a.transit_manage + 	a.other_hour 	) + (case when a.`group`="manage" then a.actual_work *8 else 0 end)AS HOUR FROM	yb_daily_report a GROUP BY	a.`group`,	a.warehouse_code,	a.date) UNION	(SELECT	warehouse_code,	date,	`group`,	sum( `hour` ) AS `hour` FROM	(SELECT	date,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[0].warehouse" ) ) AS warehouse_code,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[0].group" ) ) AS `group`,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[0].hour" ) ) AS `hour` FROM	yb_daily_report WHERE	support_out IS NOT NULL  UNION SELECT	date,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[1].warehouse" ) ) AS warehouse_code,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[1].group" ) ) AS `group`,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[1].hour" ) ) AS `hour` FROM	yb_daily_report WHERE	support_out IS NOT NULL UNION SELECT	date,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[2].warehouse" ) ) AS warehouse_code,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[2].group" ) ) AS `group`,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[2].hour" ) ) AS `hour` FROM	yb_daily_report WHERE	support_out IS NOT NULL UNION SELECT	date,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[3].warehouse" ) ) AS warehouse_code,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[3].group" ) ) AS `group`,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[3].hour" ) ) AS `hour` FROM	yb_daily_report WHERE	support_out IS NOT NULL UNION SELECT	date,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[4].warehouse" ) ) AS warehouse_code,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[4].group" ) ) AS `group`,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[4].hour" ) ) AS `hour` FROM	yb_daily_report WHERE	support_out IS NOT NULL UNION SELECT	date,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[5].warehouse" ) ) AS warehouse_code,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[5].group" ) ) AS `group`,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[5].hour" ) ) AS `hour` FROM	yb_daily_report WHERE	support_out IS NOT NULL UNION SELECT	date,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[6].warehouse" ) ) AS warehouse_code,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[6].group" ) ) AS `group`,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[6].hour" ) ) AS `hour` FROM	yb_daily_report WHERE	support_out IS NOT NULL UNION SELECT	date,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[7].warehouse" ) ) AS warehouse_code,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[7].group" ) ) AS `group`,	JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[7].hour" ) ) AS `hour` FROM	yb_daily_report WHERE	 support_out IS NOT NULL 	) a WHERE	a.warehouse_code IS NOT NULL GROUP BY	date,	warehouse_code,	`group` 	) 	 )d 	 where warehouse_code  in ("HM_AA","SZ_AA") and `group` not in ("iqc") GROUP BY	warehouse_code,	date,	`group`)a 	group  by warehouse_code,date)	b where a.date = b.date and a.warehouse = b.warehouse_code  	AND TO_DAYS( NOW( ) ) - TO_DAYS( a.date ) in (1,2,3,4,5,6,7)	group by date,warehouse_code order by warehouse_code;'
    # sql_ry = 'select a.warehouse_code, IFNULL(b.date,0),IFNULL(b.now_staff,0),IFNULL(b.enter_staff,0),IFNULL(b.actual_work,0),IFNULL(b.actual_last,0),IFNULL(b.temporary_people,0),IFNULL(b.temporary_last,0),IFNULL(b.temporary_hour,0),IFNULL(b.t_hour_last,0),IFNULL(b.now_hour,0),IFNULL(b.n_hour_last,0),IFNULL(b.work2,0),IFNULL(b.hour2,0)from (select "AFN" AS warehouse_code union  select "HM_AA" AS warehouse_code union select "SZ_AA" AS warehouse_code union select "shzz" AS warehouse_code) a left join (select a.warehouse_code,a.date,a.now_staff,a.enter_staff,a.actual_work,a.actual_work-b.actual_work as actual_last,a.temporary_people,a.temporary_people-b.temporary_people as temporary_last,a.temporary_hour,a.temporary_hour-b.temporary_hour as t_hour_last ,a.now_hour,a.now_hour-b.now_hour as n_hour_last,b.actual_work as work2,b.now_hour as hour2 from (select * from (	SELECT a.warehouse_code,		a.date ,		sum( a.now_staff ) AS now_staff,		sum( a.actual_work ) AS actual_work,		sum( a.enter_staff ) AS enter_staff,		sum( a.leave_staff ) AS leave_staff,		sum( a.normal_rest ) AS normal_rest,		sum( a.temporary_people ) AS temporary_people,		sum( a.temporary_hour ) AS temporary_hour,		sum(			(				a.group_leader + a.receive_hour + a.instock_hour + a.return_deal + a.allocate_instock + a.working_hour + a.all_quality + a.instock_putaway + a.return_putaway + a.problem_putaway + a.pick_hour + a.move_hour + a.inventory_hour + a.check_hour + a.second_pick + a.pack_hour + a.channel_pick + a.scan_weigh + a.delivery_hour + a.fba_change + a.fba_pack + a.fba_delivery + a.iqc_hour + a.confirm_exception + a.instock_exception + a.warehouse_exception + a.order_exception + a.transit_receive + a.transit_pack + a.transit_send + a.transit_manage + a.other_hour 			) 		) AS now_hour,		sum(			(				a.temporary_hour + a.group_leader + a.receive_hour + a.instock_hour + a.return_deal + a.allocate_instock + a.working_hour + a.all_quality + a.instock_putaway + a.return_putaway + a.problem_putaway + a.pick_hour + a.move_hour + a.inventory_hour + a.check_hour + a.second_pick + a.pack_hour + a.channel_pick + a.scan_weigh + a.delivery_hour + a.fba_change + a.fba_pack + a.fba_delivery + a.iqc_hour + a.confirm_exception + a.instock_exception + a.warehouse_exception + a.order_exception + a.transit_receive + a.transit_pack + a.transit_send + a.transit_manage + a.other_hour 			) 		) AS total_hour 	FROM		yb_daily_report a 	WHERE		a.`group` NOT IN ( "iqc", "general_manage" ) 		AND TO_DAYS( NOW( ) ) - TO_DAYS( a.date ) in (1)	GROUP BY	a.warehouse_code,a.date)a)a  , (select warehouse_code,date_add(date,interval 1 day)date,now_staff,actual_work,temporary_people,temporary_hour,now_hour from (	SELECT a.warehouse_code,		a.date ,		sum( a.now_staff ) AS now_staff,		sum( a.actual_work ) AS actual_work,		sum( a.enter_staff ) AS enter_staff,		sum( a.leave_staff ) AS leave_staff,		sum( a.normal_rest ) AS normal_rest,		sum( a.temporary_people ) AS temporary_people,		sum( a.temporary_hour ) AS temporary_hour,		sum(			(				a.group_leader + a.receive_hour + a.instock_hour + a.return_deal + a.allocate_instock + a.working_hour + a.all_quality + a.instock_putaway + a.return_putaway + a.problem_putaway + a.pick_hour + a.move_hour + a.inventory_hour + a.check_hour + a.second_pick + a.pack_hour + a.channel_pick + a.scan_weigh + a.delivery_hour + a.fba_change + a.fba_pack + a.fba_delivery + a.iqc_hour + a.confirm_exception + a.instock_exception + a.warehouse_exception + a.order_exception + a.transit_receive + a.transit_pack + a.transit_send + a.transit_manage + a.other_hour 			) 		) AS now_hour,		sum(			(				a.temporary_hour + a.group_leader + a.receive_hour + a.instock_hour + a.return_deal + a.allocate_instock + a.working_hour + a.all_quality + a.instock_putaway + a.return_putaway + a.problem_putaway + a.pick_hour + a.move_hour + a.inventory_hour + a.check_hour + a.second_pick + a.pack_hour + a.channel_pick + a.scan_weigh + a.delivery_hour + a.fba_change + a.fba_pack + a.fba_delivery + a.iqc_hour + a.confirm_exception + a.instock_exception + a.warehouse_exception + a.order_exception + a.transit_receive + a.transit_pack + a.transit_send + a.transit_manage + a.other_hour 			) 		) AS total_hour 	FROM		yb_daily_report a 	WHERE		a.`group` NOT IN ( "iqc", "general_manage" ) 		AND TO_DAYS( NOW( ) ) - TO_DAYS( a.date ) in (2)	GROUP BY	a.warehouse_code,a.date)a )b where a.warehouse_code = b.warehouse_code and a.date = b.date  group by a.warehouse_code,a.date order by a.warehouse_code)b on a.warehouse_code = b.warehouse_code'
    # sql_ry2 = 'select a.*,ifnull(b.date,0),ifnull(b.now_staff,0),ifnull(b.actual_work,0),ifnull(b.enter_staff,0),ifnull(b.leave_staff,0),ifnull(b.normal_rest,0),ifnull(b.temporary_people,0),ifnull(b.temporary_hour,0),ifnull(b.now_hour,0),ifnull(b.total_hour,0)from (select "AFN" as warehouse_code union select "HM_AA" as warehouse_code union select "SZ_AA" as warehouse_code union select "shzz" as warehouse_code ) a left join (SELECT	a.warehouse_code,	DATE_FORMAT(a.date,"%v") date ,	sum( a.now_staff ) AS now_staff,	sum( a.actual_work ) AS actual_work,	sum( a.enter_staff ) AS enter_staff,	sum( a.leave_staff ) AS leave_staff,	sum( a.normal_rest ) AS normal_rest,	sum( a.temporary_people ) AS temporary_people,	sum( a.temporary_hour ) AS temporary_hour,	sum(	(	a.group_leader + a.receive_hour + a.instock_hour + a.return_deal + a.allocate_instock + a.working_hour + a.all_quality + a.instock_putaway + a.return_putaway + a.problem_putaway + a.pick_hour + a.move_hour + a.inventory_hour + a.check_hour + a.second_pick + a.pack_hour + a.channel_pick + a.scan_weigh + a.delivery_hour + a.fba_change + a.fba_pack + a.fba_delivery + a.iqc_hour + a.confirm_exception + a.instock_exception + a.warehouse_exception + a.order_exception + a.transit_receive + a.transit_pack + a.transit_send + a.transit_manage + a.other_hour 	) 	) AS now_hour,	sum(	(	a.temporary_hour + a.group_leader + a.receive_hour + a.instock_hour + a.return_deal + a.allocate_instock + a.working_hour + a.all_quality + a.instock_putaway + a.return_putaway + a.problem_putaway + a.pick_hour + a.move_hour + a.inventory_hour + a.check_hour + a.second_pick + a.pack_hour + a.channel_pick + a.scan_weigh + a.delivery_hour + a.fba_change + a.fba_pack + a.fba_delivery + a.iqc_hour + a.confirm_exception + a.instock_exception + a.warehouse_exception + a.order_exception + a.transit_receive + a.transit_pack + a.transit_send + a.transit_manage + a.other_hour 	) 	) AS total_hour FROM	yb_daily_report a WHERE	a.`group` NOT IN ( "iqc", "general_manage" ) 	AND DATE_FORMAT(now(),"%v")-DATE_FORMAT(a.date,"%v")=0 and a.date>"2021-01-01"GROUP BY	a.warehouse_code,	DATE_FORMAT(a.date,"%v") order by a.warehouse_code) b on a.warehouse_code = b.warehouse_code'
    # sql_zt = 'SELECT    case    when warehouse_code = "AFN" then "HM_AA"  else warehouse_code end  AS `warehouse`,    DATE_FORMAT(add_time,"%m-%d") AS `日期`,  IFNULL(  sum( JSON_UNQUOTE( JSON_EXTRACT( work_parme_num, "$.delivery.delivery.piece_total" )) ),0) AS `点数总件数`,  IFNULL(sum( JSON_UNQUOTE(JSON_EXTRACT( work_parme_num,"$.pack.pack_single.piece_total" ))),0) +  IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_multi.piece_total" ))),0)+  IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_zf.piece_total" ))),0)+  IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_ex_order.piece_total" ))),0)+  IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_singl_more.piece_total" ))),0)+  IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack.piece_total" ))),0)+  IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_express.piece_total"))),0) +  IFNULL(sum(  JSON_UNQUOTE(JSON_EXTRACT( work_parme_num,"$.pack.pack_sku_bao.piece_total" ))),0) AS `打包总件数`,	IFNULL(sum( JSON_UNQUOTE(JSON_EXTRACT( work_parme_num,"$.pack.pack_single.order_total" ))),0) +  IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_multi.order_total" ))),0)+  IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_zf.order_total" ))),0)+  IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_ex_order.order_total" ))),0)+  IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_singl_more.order_total" ))),0)+  IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack.order_total" ))),0)+  IFNULL(sum(JSON_UNQUOTE(JSON_EXTRACT( work_parme_num, "$.pack.pack_express.order_total"))),0) +  IFNULL(sum(  JSON_UNQUOTE(JSON_EXTRACT( work_parme_num,"$.pack.pack_sku_bao.order_total" ))),0) AS `打包单数`,  IFNULL(sum(JSON_UNQUOTE( JSON_EXTRACT( work_parme_num, "$.FBA.FBA.piece_total" ))),0) AS `FBA打包件数`,	IFNULL(sum(JSON_UNQUOTE( JSON_EXTRACT( work_parme_num, "$.FBA.FBA.order_total" ))),0) AS `FBA打包单数`  FROM    `ueb_work_num_log_history`   WHERE    warehouse_code in ("HM_AA","SZ_AA","AFN")    and    TO_DAYS( NOW( ) ) - TO_DAYS( add_time ) <= 7   GROUP BY    warehouse,    add_time;'
    # sql_dcl = 'select a.warehouse_code,ifnull(b.type,a.type),ifnull(b.date,0),ifnull(b.rk,0) ,ifnull(b.tm,0),ifnull(b.zj,0) ,ifnull(b.sj,0)from (select "HM_AA" as warehouse_code , "1" as type union select "HM_AA" as warehouse_code , "2" as type union select "HM_AA" as warehouse_code , "3" as type union select "SZ_AA" as warehouse_code , "1" as type union select "SZ_AA" as warehouse_code , "2" as type union select "SZ_AA" as warehouse_code , "3" as type ) a  left join (SELECT			warehouse_code, "1" as type,			date_format( upper_end_time, "%Y-%m-%d") date,			avg( IF ( add_time > quality_start_time, timestampdiff( HOUR, quality_start_time, add_time ), NULL ) ) as rk,			avg( IF ( post_code_end_time > add_time, timestampdiff( HOUR, add_time, post_code_end_time ), NULL ) ) as tm,			avg( IF ( quality_time > post_code_end_time, timestampdiff( HOUR, post_code_end_time, quality_time ), timestampdiff( HOUR, quality_time, post_code_end_time ) ) ) as zj,			avg(			IF				(					upper_end_time > quality_all_time 					AND quality_all_time > "2000-01-01",					timestampdiff( HOUR, quality_all_time, upper_end_time ),				IF					(						upper_end_time > quality_time 						AND quality_time > post_code_end_time,						timestampdiff( HOUR, quality_time, upper_end_time ),					IF					( upper_end_time > post_code_end_time AND post_code_end_time > quality_time, timestampdiff( HOUR, quality_time, upper_end_time ), NULL )))) as sj		FROM			ueb_quality_warehousing_record		WHERE			type = 1 			AND paragraph = 5 			AND quality_start_time > 0 			AND add_time > 0 		  and TO_DAYS( NOW( ) ) - TO_DAYS( upper_end_time ) = 1 			AND upper_end_time is not null 		GROUP BY			warehouse_code,			date_format( upper_end_time, "%Y-%m-%d" ) union 											SELECT				warehouse_code AS warehouse,"2"as type,				date_format( from_unixtime( outstock_time ), "%Y-%m-%d") AS date,			IF				( wait_pull_time != 0 AND pull_time != 0, ROUND(( avg( pull_time )- avg( wait_pull_time ))/ 3600, 2 ), NULL ) AS ld,					ROUND(( avg( pick_time )- avg( pull_time ))/ 3600, 2 ) AS jh,			ROUND( avg(( pack_time ) - ( pick_time ))/ 3600, 2 ) AS db,				IF				(					pack_time != 0 					AND outstock_time != 0,					ROUND( ( avg( outstock_time ) - avg( pack_time ) ) / 3600, 2 ),				NULL 				) AS ck 			FROM				ueb_order_operate_time			WHERE				order_is_cancel = 0 				AND order_id NOT LIKE "FB%" 				and 	TO_DAYS( NOW( ) ) - TO_DAYS( date_format( from_unixtime( outstock_time ), "%Y-%m-%d" ) ) = 1 				AND pick_time != 0 AND  batch_no not like "%-6-%" 			GROUP BY				warehouse_code,			date_format( from_unixtime( outstock_time ), "%Y-%m-%d" ) union		 				SELECT			warehouse_code AS warehouse,"3"as type ,			date_format( from_unixtime( outstock_time ), "%Y-%m-%d" ) AS date,		IF			( wait_pull_time != 0 AND pull_time != 0, ROUND(( avg( pull_time )- avg( wait_pull_time ))/ 3600, 2 ), NULL ) AS ld,				ROUND(( avg( pick_time )- avg( pull_time ))/ 3600, 2 )  AS jh,				ROUND( avg(( pack_time ) - ( pick_time ))/ 3600, 2 )  AS db,						IF			(				pack_time != 0 				AND outstock_time != 0,				ROUND( ( avg( outstock_time ) - avg( pack_time ) ) / 3600, 2 ),			NULL 			)  AS ck			FROM			ueb_order_operate_time		WHERE			order_is_cancel = 0 			and 	TO_DAYS( NOW( ) ) - TO_DAYS( date_format( from_unixtime( outstock_time ), "%Y-%m-%d" ) ) = 1 			AND order_id LIKE "FB%" 			AND pick_time != 0 		GROUP BY			warehouse_code,		date_format( from_unixtime( outstock_time ),"%Y-%m-%d") 	order by warehouse_code,type	) b on a.warehouse_code = b.warehouse_code and a.type = b.type  		'
    # sql_db = 'select a.date,a.warehouse,IFNULL(b.`in`,0) `in` ,IFNULL(c.`out`,0)`out`,IFNULL(b.`in`,0)+IFNULL(c.`out`,0) as `total` from (select DATE_FORMAT(Date,"%m-%d") date,"HM_AA"as warehouse from date where `year` ="2021" and TO_DAYS( NOW( ) ) - TO_DAYS( `Date` ) in (0,1,2,3,4,5,6)union select DATE_FORMAT(Date,"%m-%d") date,"SZ_AA"as warehouse from date where `year` ="2021" and TO_DAYS( NOW( ) ) - TO_DAYS( `Date` ) in (0,1,2,3,4,5,6))a left join (SELECT	case	when warehouse_code = "AFN" then "HM_AA" else warehouse_code end 	warehouse,	DATE_FORMAT( upper_end_time, "%m-%d" ) date  ,	count(DISTINCT purchase_order_no) as `in`FROM	ueb_quality_warehousing_record WHERE	purchase_order_no LIKE "ALLOT%" 	AND TO_DAYS( NOW( ) ) - TO_DAYS( upper_end_time )<= 6 GROUP BY warehouse,	DATE_FORMAT( upper_end_time, "%m-%d" )) b on a.warehouse=b.warehouse and a.date = b.date left join(select warehouse_code,FROM_UNIXTIME(delivery_time,"%m-%d") date,count(DISTINCT IFNULL(order_id,0)) `out` from ueb_order_operate_time where order_id like "ALLOT%" and order_is_cancel = 0  and TO_DAYS( NOW( ) ) - TO_DAYS( FROM_UNIXTIME(delivery_time,"%Y-%m-%d")  ) <= 6 group by FROM_UNIXTIME(delivery_time,"%m-%d"),warehouse_code )c on  a.date = c.date  and a.warehouse = c.warehouse_code'
    # sql_dcl2 = 'SELECT  a.*,ifnull(round(b.`fba`,3),0) fba,ifnull(round(c.`out`,3),0) `out`, ifnull(round(d.`in`,3),0) `in` from (SELECT  "HM_AA" AS warehouse_code,"1" as use_hours   union SELECT  "HM_AA" AS warehouse_code,"2" as use_hours  union  SELECT  "SZ_AA" AS warehouse_code,"1" as use_hours  union SELECT  "SZ_AA" AS warehouse_code,"2" as use_hours   union  SELECT  "HM_AA" AS warehouse_code,"1" as use_hours   union SELECT  "HM_AA" AS warehouse_code,"2" as use_hours union SELECT  "SZ_AA" AS warehouse_code,"1" as use_hours union SELECT  "SZ_AA" AS warehouse_code,"2" as use_hours  union  SELECT  "HM_AA" AS warehouse_code,"1" as use_hours  union SELECT  "HM_AA" AS warehouse_code,"2" as use_hours union SELECT  "SZ_AA" AS warehouse_code,"1" as use_hours union SELECT  "SZ_AA" AS warehouse_code,"2" as use_hours union SELECT  "HM_AA" AS warehouse_code,"3" as use_hours   union SELECT  "SZ_AA" AS warehouse_code,"3" as use_hours) a  LEFT JOIN (SELECT a.warehouse_code,ceil((if((if(a.pick_time > a.pull_time, a.pick_time - a.pull_time, 0) + if(a.choice_time > a.pick_time, a.choice_time - a.pick_time, 0) + if(a.choice_time and a.pack_time > a.choice_time, a.pack_time - a.choice_time, a.pack_time - a.pick_time)) > 0 , if(a.pick_time > a.pull_time, a.pick_time - a.pull_time, 0) + if(a.choice_time > a.pick_time, a.choice_time - a.pick_time, 0) + if(a.choice_time and a.pack_time > a.choice_time, a.pack_time - a.choice_time, a.pack_time - a.pick_time), 0))/43200) as use_hours,count(*)as num, b.total as total, count(*)/b.total as fba  FROM ueb_order_operate_time as a left join(SELECT  warehouse_code,count(*) as total FROM ueb_order_operate_time WHERE 	TO_DAYS( NOW( ) ) - TO_DAYS( date_format( from_unixtime( outstock_time ), "%Y-%m-%d" ) ) in (1) and wait_pull_time > 0 and pull_time > 0 and pick_time > 0 and pack_time > 0 and outstock_time > 0 and delivery_time > 0 and batch_no like "%-6-%" and order_id not like "HW%" and order_id not like "ALLOT%" and order_id not like "PTH%" and choice_time > 0 group by warehouse_code ORDER BY warehouse_code asc  ) as  b on a.warehouse_code = b.warehouse_code WHERE 	TO_DAYS( NOW( ) ) - TO_DAYS( date_format( from_unixtime( outstock_time ), "%Y-%m-%d" ) ) in (1) and wait_pull_time > 0 and pull_time > 0 and pick_time > 0 and pack_time > 0 and outstock_time > 0 and delivery_time > 0 and batch_no like "%-6-%" and order_id not like "HW%" and order_id not like "ALLOT%" and order_id not like "PTH%" and choice_time > 0 group by use_hours,warehouse_code )b on a.warehouse_code=b.warehouse_code  and a.use_hours =b.use_hours  left join (SELECT  a.warehouse_code,ceil((if((if(a.pull_time > a.wait_pull_time, a.pull_time - a.wait_pull_time, 0) + if(a.pick_time > a.pull_time, a.pick_time - a.pull_time, 0) + if(a.choice_time > a.pick_time, a.choice_time - a.pick_time, 0) + if(a.choice_time and a.pack_time > a.choice_time, a.pack_time - a.choice_time, a.pack_time - a.pick_time) + if(a.outstock_time > a.pack_time, a.outstock_time - a.pack_time, 0) - if(a.abnormal_time > 0, a.abnormal_time, 0)) > 0 , if(a.pull_time > a.wait_pull_time, a.pull_time - a.wait_pull_time, 0) + if(a.pick_time > a.pull_time, a.pick_time - a.pull_time, 0) +if(a.choice_time > a.pick_time, a.choice_time - a.pick_time, 0) + if(a.choice_time and a.pack_time > a.choice_time, a.pack_time - a.choice_time, a.pack_time - a.pick_time) + if(a.outstock_time > a.pack_time, a.outstock_time - a.pack_time, 0) - if(a.abnormal_time > 0, a.abnormal_time, 0), 0))/43200) as use_hours,count(*),b.total,count(*)/b.total as   `out` FROM ueb_order_operate_time a left join (SELECT  a.warehouse_code,count(*) as total FROM ueb_order_operate_time a WHERE TO_DAYS( NOW( ) ) - TO_DAYS( date_format( from_unixtime( outstock_time ), "%Y-%m-%d" ) ) in (1)  and wait_pull_time > 0 and pull_time > 0 and pick_time > 0 and pack_time > 0 and outstock_time > 0 and delivery_time > 0  and batch_no not like "%-6-%" group by warehouse_code)b on a.warehouse_code=b.warehouse_code WHERE TO_DAYS( NOW( ) ) - TO_DAYS( date_format( from_unixtime( outstock_time ), "%Y-%m-%d" ) ) in (1)  and wait_pull_time > 0 and pull_time > 0 and pick_time > 0 and pack_time > 0 and outstock_time > 0 and delivery_time > 0  and batch_no not like "%-6-%" group by warehouse_code,use_hours )c on a.warehouse_code=c.warehouse_code and a.use_hours =c.use_hours  left join (		SELECT a.warehouse_code 	,	CASE								WHEN a.time <= 12 THEN "1" WHEN a.time > 12 				AND a.time <= 24 THEN "2" WHEN a.time > 24 					AND a.time <= 36 THEN "3" WHEN a.time > 36 						AND a.time <= 48 THEN "4" WHEN a.time > 48 							AND a.time <= 60 THEN "5" WHEN a.time > 60 								AND a.time <= 108 THEN									"6" ELSE "7" 									END AS `use_hours`,								count( a.time ) AS num,								b.time,								round( count( a.time )/ b.time ,4 ) "in" 							FROM								(								SELECT 									warehouse_code,									date_format( upper_end_time, "%Y-%m-%d" ) AS Date,									ROUND(( unix_timestamp( upper_end_time ) - unix_timestamp( quality_start_time )) / 3600, 2 ) AS time 								FROM									ueb_quality_warehousing_record a 								WHERE									type = 1 									AND paragraph = 5 									AND quality_start_time > 0 									AND add_time > 0 									AND post_code_end_time > 0 												AND TO_DAYS( NOW( ) ) - TO_DAYS( upper_end_time ) IN ( 1) 								) a,								(								SELECT 									a.warehouse_code,									"in" AS `way`,									count( a.time ) AS time 								FROM									(									SELECT 										warehouse_code,										date_format( upper_end_time, "%Y-%m-%d" ) AS Date,										ROUND(( unix_timestamp( upper_end_time ) - unix_timestamp( quality_start_time )) / 3600, 2 ) AS time 									FROM										ueb_quality_warehousing_record 									WHERE										type = 1 										AND paragraph = 5 										AND quality_start_time > 0 										AND add_time > 0 										AND post_code_end_time > 0 			AND TO_DAYS( NOW( ) ) - TO_DAYS( upper_end_time ) IN ( 1) 																		) a 								GROUP BY									a.warehouse_code,									a.Date 								) b 							WHERE								a.warehouse_code = b.warehouse_code 							GROUP BY								a.warehouse_code,									`use_hours`)d on a.warehouse_code = d.warehouse_code and a.use_hours = d.use_hours group by a.warehouse_code,a.use_hours order by a.warehouse_code,a.use_hours'

    input = pd.read_excel('daily1_jy.xlsx')
    see_jy=save(input)
    input = pd.read_excel('daily1_zl.xlsx')
    see_zl=save(input)
    input = pd.read_excel('daily1_sx.xlsx')
    see_sx=save(input)
    input = pd.read_excel('daily1_rk.xlsx')
    see_rk=save(input)
    input = pd.read_excel('daily1_tph.xlsx')
    see_tph=save(input)
    input = pd.read_excel('daily1_ry.xlsx')
    see_ry=save(input)
    input = pd.read_excel('daily1_ry2.xlsx')
    see_ry2=save(input)
    input = pd.read_excel('daily1_zt.xlsx')
    see_zt=save(input)
    input = pd.read_excel('daily1_dcl.xlsx')
    see_dcl=save(input)
    input = pd.read_excel('daily1_db.xlsx')
    see_db=save(input)
    input = pd.read_excel('daily1_dcl2.xlsx')
    see_dcl2=save(input)

    dcl2_in = []
    dcl2_out = []
    dcl2_fba = []
    for data_dcl2 in see_dcl2:
        dcl2_in.append(data_dcl2[4])
        dcl2_out.append(data_dcl2[3])
        dcl2_fba.append(data_dcl2[2])

    dcl2_in.append(sum(dcl2_in[0:2]))
    dcl2_in.append(sum(dcl2_in[3:5]))
    dcl2_out.append(sum(dcl2_out[0:2]))
    dcl2_out.append(sum(dcl2_out[3:5]))
    dcl2_fba.append(sum(dcl2_fba[0:2]))
    dcl2_fba.append(sum(dcl2_fba[0:3]))
    dcl2_fba.append(sum(dcl2_fba[3:5]))
    dcl2_fba.append(sum(dcl2_fba[3:6]))

    db_in = []
    db_out = []
    db_total = []
    db_date = []
    for data_db in see_db:
        db_in.append(data_db[2])
        db_out.append(data_db[3])
        db_total.append(data_db[4])
        db_date.append(data_db[0])
    db_date = db_date[0:7]
    db_in.append(max(db_in[0:7] + db_out[0:7]) + 100)
    db_in.append(max(db_in[7:15] + db_out[7:15]) + 100)
    db_in.append(max(db_total[0:7]) + 100)
    db_in.append(max(db_total[7:15]) + 100)

    dcl_1 = []
    dcl_2 = []
    dcl_3 = []
    dcl_4 = []
    for data_dcl in see_dcl:
        dcl_1.append(round(data_dcl[3], 2))
        dcl_2.append(round(data_dcl[4], 2))
        dcl_3.append(round(data_dcl[5], 2))
        dcl_4.append(round(data_dcl[6], 2))

    zt_warehouse = []
    zt_date = []
    zt_1 = []
    zt_2 = []
    zt_3 = []
    zt_4 = []
    zt_5 = []
    for data_zt in see_zt:
        zt_warehouse.append(data_zt[0])
        zt_date.append(data_zt[1])
        zt_1.append(data_zt[2])
        zt_2.append(data_zt[3])
        zt_3.append(data_zt[4])
        zt_4.append(data_zt[5])
        zt_5.append(data_zt[6])
    zt_1.append(max(zt_1[0:4]) + max(zt_2[0:4]) + max(zt_4[0:4]) + 40000)
    zt_1.append(max(zt_1[5:9]) + max(zt_2[5:9]) + max(zt_4[5:9]) + 40000)
    zt_1.append(max(zt_3[0:4]) + 10000)
    zt_1.append(max(zt_3[5:9]) + 10000)

    ry_warehouse = []
    ry_date = []
    ry_1 = []
    ry_2 = []
    ry_3 = []
    ry_4 = []
    ry_5 = []
    ry_6 = []
    ry_7 = []
    ry_8 = []
    ry_9 = []
    ry_10 = []
    ry_11 = []
    ry_12 = []
    ry_13 = []
    ry_14 = []

    for data_ry in see_ry:
        ry_warehouse.append(data_ry[0])
        ry_date.append(data_ry[1])
        ry_1.append(data_ry[2])
        ry_2.append(data_ry[3])
        ry_3.append(data_ry[4])
        ry_4.append(data_ry[5])
        ry_5.append(data_ry[6])
        ry_6.append(data_ry[7])
        ry_7.append(data_ry[8])
        ry_8.append(data_ry[9])
        ry_9.append(data_ry[10])
        ry_10.append(data_ry[11])
        ry_11.append(data_ry[12])
        ry_12.append(data_ry[13])


    for data_ry in see_ry2:
        ry_13.append(data_ry[4])
        ry_14.append(data_ry[5])
    if ry_13:
        print('1')
    else:
        ry_13 = [0, 0, 0, 0]

    if ry_14:
        print('1')
    else:
        ry_14 = [0, 0, 0, 0]

    ##需语句修正
    hm_total = []
    tx_total = []
    hm_change = []
    tx_change = []
    hm_total.append(float(ry_1[1]))
    hm_total.append(float(ry_1[0]))
    hm_total.append(float(ry_3[0] + ry_3[1]))
    hm_total.append(float(ry_5[0] + ry_5[1]))
    hm_total.append(float(ry_7[0] + ry_7[1]))
    hm_total.append(float(ry_9[0] + ry_9[1]))
    try:
        hm_total.append(round(hm_total[5] / hm_total[2], 2))
    except ZeroDivisionError:
        hm_total.append(0)

    hm_total.append(float(ry_13[0] + ry_13[1]))
    hm_total.append(float(ry_14[0] + ry_14[1]))

    tx_total.append(float(ry_1[2]))
    tx_total.append(float(ry_1[3]))
    tx_total.append(float(ry_3[3] + ry_3[2]))
    tx_total.append(float(ry_5[3] + ry_5[2]))
    tx_total.append(float(ry_7[3] + ry_7[2]))
    tx_total.append(float(ry_9[3] + ry_9[2]))
    try:
        tx_total.append(round(tx_total[5] / tx_total[2], 2))
    except ZeroDivisionError:
        tx_total.append(0)
    tx_total.append(float(ry_13[2] + ry_13[3]))
    tx_total.append(float(ry_14[2] + ry_14[3]))

    hm_change.append(float(ry_2[1]))
    hm_change.append(float(ry_2[0]))
    hm_change.append(float(ry_4[0]) + float(ry_4[1]))
    hm_change.append(float(ry_6[0]) + float(ry_6[1]))
    hm_change.append(round(float(ry_8[0]) + float(ry_8[1]), 0))
    hm_change.append(round(float(ry_10[0]) + float(ry_10[1]), 0))
    try:
        hm_change.append(
            round(float(hm_total[6]) - ((float(ry_12[0]) + float(ry_12[1])) / (float(ry_11[0]) + float(ry_11[1]))), 2))
    except ZeroDivisionError:
        hm_change.append(0)
    tx_change.append(float(ry_2[3]))
    tx_change.append(float(ry_2[2]))
    tx_change.append(float(ry_4[3]) + float(ry_4[2]))
    tx_change.append(float(ry_6[3]) + float(ry_6[2]))
    tx_change.append(round(float(ry_8[3]) + float(ry_8[2]), 0))
    tx_change.append(round(float(ry_10[3]) + float(ry_10[2]), 0))
    try:
        tx_change.append(
            round(tx_total[6] - ((float(ry_12[3]) + float(ry_12[2])) / (float(ry_11[3]) + float(ry_11[2]))), 2))
    except ZeroDivisionError:
        tx_change.append(0)
    warehouse_tph = []
    tph_date = []
    tph = []
    uph = []
    for data_tph in see_tph:
        tph_date.append(data_tph[0])
        warehouse_tph.append(data_tph[1])
        tph.append(data_tph[2])
        uph.append(data_tph[3])
    hm_tph_date = []
    hm_tph = []
    hm_uph = []
    tx_tph_date = []
    tx_tph = []
    tx_uph = []
    for i in range(len(warehouse_tph)):
        if warehouse_tph[i] == 'HM_AA':
            hm_tph_date.append(tph_date[i])
            hm_tph.append(tph[i])
            hm_uph.append(uph[i])
    for i in range(len(warehouse_tph)):
        if warehouse_tph[i] == 'SZ_AA':
            tx_tph_date.append(tph_date[i])
            tx_tph.append(tph[i])
            tx_uph.append(uph[i])
    a = round(max(hm_tph), 0) + 10
    b = round(min(hm_uph), 0) - 10
    hm_tph.append(a)
    hm_tph.append(b)
    a = round(max(tx_tph), 0) + 10
    b = round(min(tx_uph), 0) - 10
    hm_uph.append(a)
    hm_uph.append(b)


    warehouse_jy = []
    num_jy = []
    type_jy = []
    for data_jy in see_jy:
        warehouse_jy.append(data_jy[0])
        num_jy.append(data_jy[1])
        type_jy.append(data_jy[2])

    warehouse_zl = []
    cost_zl = []
    time_zl = []
    jsonData = {}
    for data_zl in see_zl:
        warehouse_zl.append(data_zl[0])
        cost_zl.append(data_zl[1])
        time_zl.append(data_zl[2])

    warehouse_sx = []
    type_sx = []
    time_sx = []
    date_sx = []

    for data_sx in see_sx:
        date_sx.append(data_sx[0])
        warehouse_sx.append(data_sx[1])
        type_sx.append(data_sx[2])
        time_sx.append(data_sx[3])

    warehouse_rk = []
    type_rk = []
    num_rk = []

    for data_rk in see_rk:
        warehouse_rk.append(data_rk[0])
        type_rk.append(data_rk[2])
        num_rk.append(data_rk[3])

    hm_rk_in = []
    hm_rk_out = []
    hm_rk_ld = []
    tx_rk_in = []
    tx_rk_out = []
    tx_rk_ld = []

    for i in range(len(warehouse_rk)):
        if warehouse_rk[i] == 'HM_AA' and type_rk[i] == 'in':
            hm_rk_in.append(num_rk[i])
    for i in range(len(warehouse_rk)):
        if warehouse_rk[i] == 'HM_AA' and type_rk[i] == 'out':
            hm_rk_out.append(num_rk[i])
    for i in range(len(warehouse_rk)):
        if warehouse_rk[i] == 'HM_AA' and type_rk[i] == 'LD':
            hm_rk_ld.append(num_rk[i])
    for i in range(len(warehouse_rk)):
        if warehouse_rk[i] == 'SZ_AA' and type_rk[i] == 'in':
            tx_rk_in.append(num_rk[i])
    for i in range(len(warehouse_rk)):
        if warehouse_rk[i] == 'SZ_AA' and type_rk[i] == 'out':
            tx_rk_out.append(num_rk[i])
    for i in range(len(warehouse_rk)):
        if warehouse_rk[i] == 'SZ_AA' and type_rk[i] == 'LD':
            tx_rk_ld.append(num_rk[i])

    hm_sx_date = []
    tx_sx_date = []
    hm_sx_in = []
    hm_sx_out = []
    hm_sx_fba = []
    tx_sx_in = []
    tx_sx_out = []
    tx_sx_fba = []
    for i in range(len(warehouse_sx)):
        if warehouse_sx[i] == 'HM_AA' and type_sx[i] == 'in':
            hm_sx_date.append(date_sx[i])

    for i in range(len(warehouse_sx)):
        if warehouse_sx[i] == 'HM_AA' and type_sx[i] == 'in':
            hm_sx_in.append(time_sx[i])
    for i in range(len(warehouse_sx)):
        if warehouse_sx[i] == 'HM_AA' and type_sx[i] == 'out':
            hm_sx_out.append(time_sx[i])
    for i in range(len(warehouse_sx)):
        if warehouse_sx[i] == 'HM_AA' and type_sx[i] == 'FBA':
            hm_sx_fba.append(time_sx[i])

    for i in range(len(warehouse_sx)):
        if warehouse_sx[i] == 'SZ_AA' and type_sx[i] == 'in':
            tx_sx_date.append(date_sx[i])
    for i in range(len(warehouse_sx)):
        if warehouse_sx[i] == 'SZ_AA' and type_sx[i] == 'in':
            tx_sx_in.append(time_sx[i])
    for i in range(len(warehouse_sx)):
        if warehouse_sx[i] == 'SZ_AA' and type_sx[i] == 'out':
            tx_sx_out.append(time_sx[i])
    for i in range(len(warehouse_sx)):
        if warehouse_sx[i] == 'SZ_AA' and type_sx[i] == 'FBA':
            tx_sx_fba.append(time_sx[i])

    num_jy_hm = []
    type_jy_hm = []
    num_jy_tx = []
    type_jy_tx = []
    for i in range(len(warehouse_jy)):
        if warehouse_jy[i] == 'HM_AA':
            num_jy_hm.append(num_jy[i])
            type_jy_hm.append(type_jy[i])
    for i in range(len(warehouse_jy)):
        if warehouse_jy[i] == 'SZ_AA':
            num_jy_tx.append(num_jy[i])
            type_jy_tx.append(type_jy[i])

    hm_zl_cost = []
    hm_zl_time = []
    tx_zl_cost = []
    tx_zl_time = []

    for i in range(len(warehouse_zl)):
        if warehouse_zl[i] == "HM_AA":
            hm_zl_cost.append(cost_zl[i])
            hm_zl_time.append(time_zl[i])
    for i in range(len(warehouse_zl)):
        if warehouse_zl[i] == "SZ_AA":
            tx_zl_cost.append(cost_zl[i])
            tx_zl_time.append(time_zl[i])

    hm_jy_data = np.dstack((num_jy_hm, type_jy_hm))
    tx_jy_data = np.dstack((num_jy_tx, type_jy_tx))

    hm_jy_DLD_num = [0]
    hm_jy_DCK_num = [0]
    hm_jy_DDB_num = [0]
    hm_jy_DGNZJ_num = [0]
    hm_jy_DJH_num = [0]
    hm_jy_DRK_num = [0]
    hm_jy_DSJ_num = [0]
    hm_jy_DTM_num = [0]
    hm_jy_FDCK_num = [0]
    hm_jy_FDDB_num = [0]
    hm_jy_FDJH_num = [0]
    hm_jy_FDJY_num = [0]
    hm_jy_FJHZ_num = [0]
    hm_jy_FDLD_num = [0]
    hm_jy_DBDRK_num = [0]
    hm_jy_DBRKZ_num = [0]
    hm_jy_DBDLD_num = [0]
    hm_jy_DBDJH_num = [0]
    hm_jy_DBDDB_num = [0]
    hm_jy_DBDCK_num = [0]
    hm_jy_DBDJY_num = [0]
    hm_jy_DPK_num = [0]
    hm_jy_FDPK_num = [0]
    hm_jy_FDFPLD_num = [0]
    tx_jy_FDFPLD_num = [0]

    tx_jy_DPK_num = [0]
    tx_jy_FDPK_num = [0]
    tx_jy_DBDRK_num = [0]
    tx_jy_DBRKZ_num = [0]
    tx_jy_DBDLD_num = [0]
    tx_jy_DBDJH_num = [0]
    tx_jy_DBDDB_num = [0]
    tx_jy_DBDCK_num = [0]
    tx_jy_DBDJY_num = [0]
    tx_jy_DLD_num = [0]
    tx_jy_DCK_num = [0]
    tx_jy_DDB_num = [0]
    tx_jy_DGNZJ_num = [0]
    tx_jy_DJH_num = [0]
    tx_jy_DRK_num = [0]
    tx_jy_DSJ_num = [0]
    tx_jy_DTM_num = [0]
    tx_jy_FDCK_num = [0]
    tx_jy_FDDB_num = [0]
    tx_jy_FDJH_num = [0]
    tx_jy_FDJY_num = [0]
    tx_jy_FJHZ_num = [0]
    tx_jy_FDLD_num = [0]

    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DCK':
            hm_jy_DCK_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DLD':
            hm_jy_DLD_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DDB':
            hm_jy_DDB_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DGNZJ':
            hm_jy_DGNZJ_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DRK':
            hm_jy_DRK_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DSJ':
            hm_jy_DSJ_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DTM':
            hm_jy_DTM_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'FDCK':
            hm_jy_FDCK_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'FDDB':
            hm_jy_FDDB_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'FDJH':
            hm_jy_FDJH_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'FDJY':
            hm_jy_FDJY_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'FJHZ':
            hm_jy_FJHZ_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'FDLD':
            hm_jy_FDLD_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DJH':
            hm_jy_DJH_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DBDRK':
            hm_jy_DBDRK_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DBRKZ':
            hm_jy_DBRKZ_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DBDLD':
            hm_jy_DBDLD_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DBDJH':
            hm_jy_DBDJH_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DBDDB':
            hm_jy_DBDDB_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DBDCK':
            hm_jy_DBDCK_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DBDJY':
            hm_jy_DBDJY_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'DPK':
            hm_jy_DPK_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'FDPK':
            hm_jy_FDPK_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_hm)):
        if hm_jy_data[0][i][1] == 'FDFPLD':
            hm_jy_FDFPLD_num[0] = (hm_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'FDFPLD':
            tx_jy_FDFPLD_num[0] = (tx_jy_data[0][i][0])

    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DPK':
            tx_jy_DPK_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'FDPK':
            tx_jy_FDPK_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DLD':
            tx_jy_DLD_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DCK':
            tx_jy_DCK_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DDB':
            tx_jy_DDB_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DGNZJ':
            tx_jy_DGNZJ_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DRK':
            tx_jy_DRK_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DSJ':
            tx_jy_DSJ_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DTM':
            tx_jy_DTM_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'FDCK':
            tx_jy_FDCK_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'FDDB':
            tx_jy_FDDB_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'FDJH':
            tx_jy_FDJH_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'FDJY':
            tx_jy_FDJY_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'FJHZ':
            tx_jy_FJHZ_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'FDLD':
            tx_jy_FDLD_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DJH':
            tx_jy_DJH_num[0] = tx_jy_data[0][i][0]
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DBDRK':
            tx_jy_DBDRK_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DBRKZ':
            tx_jy_DBRKZ_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DBDLD':
            tx_jy_DBDLD_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DBDJH':
            tx_jy_DBDJH_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DBDDB':
            tx_jy_DBDDB_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DBDCK':
            tx_jy_DBDCK_num[0] = (tx_jy_data[0][i][0])
    for i in range(len(num_jy_tx)):
        if tx_jy_data[0][i][1] == 'DBDJY':
            tx_jy_DBDJY_num[0] = (tx_jy_data[0][i][0])
    hm_jy_XB_totoal = []
    hm_jy_FB_totoal = []
    tx_jy_XB_totoal = []
    tx_jy_FB_totoal = []
    hm_jy_DB_totoal = []
    tx_jy_DB_totoal = []

    hm_jy_XB_totoal.append(float(hm_jy_DCK_num[0]))
    hm_jy_XB_totoal.append(float(hm_jy_DDB_num[0]))
    hm_jy_XB_totoal.append(float(hm_jy_DJH_num[0]))
    hm_jy_XB_totoal.append(float(hm_jy_DLD_num[0]))
    hm_jy_XB_totoal.append(float(hm_jy_DPK_num[0]))
    hm_jy_XB_totoal.append(float(hm_jy_DSJ_num[0]))
    hm_jy_XB_totoal.append(float(hm_jy_DTM_num[0]))
    hm_jy_XB_totoal.append(float(hm_jy_DGNZJ_num[0]))
    hm_jy_XB_totoal.append(float(hm_jy_DRK_num[0]))

    hm_jy_DB_totoal.append(float(hm_jy_DBDJY_num[0]))
    hm_jy_DB_totoal.append(float(hm_jy_DBDCK_num[0]))
    hm_jy_DB_totoal.append(float(hm_jy_DBDDB_num[0]))
    hm_jy_DB_totoal.append(float(hm_jy_DBDJH_num[0]))
    hm_jy_DB_totoal.append(float(hm_jy_DBDLD_num[0]))
    hm_jy_DB_totoal.append(float(hm_jy_DBRKZ_num[0]))
    hm_jy_DB_totoal.append(float(hm_jy_DBDRK_num[0]))

    tx_jy_DB_totoal.append(float(tx_jy_DBDJY_num[0]))
    tx_jy_DB_totoal.append(float(tx_jy_DBDCK_num[0]))
    tx_jy_DB_totoal.append(float(tx_jy_DBDDB_num[0]))
    tx_jy_DB_totoal.append(float(tx_jy_DBDJH_num[0]))
    tx_jy_DB_totoal.append(float(tx_jy_DBDLD_num[0]))
    tx_jy_DB_totoal.append(float(tx_jy_DBRKZ_num[0]))
    tx_jy_DB_totoal.append(float(tx_jy_DBDRK_num[0]))

    tx_jy_XB_totoal.append(float(tx_jy_DCK_num[0]))
    tx_jy_XB_totoal.append(float(tx_jy_DDB_num[0]))
    tx_jy_XB_totoal.append(float(tx_jy_DJH_num[0]))
    tx_jy_XB_totoal.append(float(tx_jy_DLD_num[0]))
    tx_jy_XB_totoal.append(float(tx_jy_DPK_num[0]))
    tx_jy_XB_totoal.append(float(tx_jy_DSJ_num[0]))
    tx_jy_XB_totoal.append(float(tx_jy_DTM_num[0]))
    tx_jy_XB_totoal.append(float(tx_jy_DGNZJ_num[0]))
    tx_jy_XB_totoal.append(float(tx_jy_DRK_num[0]))

    hm_jy_FB_totoal.append(float(hm_jy_FDJY_num[0]))
    hm_jy_FB_totoal.append(float(hm_jy_FDCK_num[0]))
    hm_jy_FB_totoal.append(float(hm_jy_FDDB_num[0]))
    hm_jy_FB_totoal.append(float(hm_jy_FJHZ_num[0]))
    hm_jy_FB_totoal.append(float(hm_jy_FDJH_num[0]))
    hm_jy_FB_totoal.append(float(hm_jy_FDLD_num[0]))
    hm_jy_FB_totoal.append(float(hm_jy_FDFPLD_num[0]))
    hm_jy_FB_totoal.append(float(hm_jy_FDPK_num[0]))

    tx_jy_FB_totoal.append(float(tx_jy_FDJY_num[0]))
    tx_jy_FB_totoal.append(float(tx_jy_FDCK_num[0]))
    tx_jy_FB_totoal.append(float(tx_jy_FDDB_num[0]))
    tx_jy_FB_totoal.append(float(tx_jy_FJHZ_num[0]))
    tx_jy_FB_totoal.append(float(tx_jy_FDJH_num[0]))
    tx_jy_FB_totoal.append(float(tx_jy_FDLD_num[0]))
    tx_jy_FB_totoal.append(float(tx_jy_FDFPLD_num[0]))
    tx_jy_FB_totoal.append(float(tx_jy_FDPK_num[0]))

    hm_jy_XB_totoal_color = []
    hm_jy_FB_totoal_color = []
    hm_jy_DB_totoal_color = []
    tx_jy_XB_totoal_color = []
    tx_jy_FB_totoal_color = []
    tx_jy_DB_totoal_color = []
    for i in range(len(hm_jy_XB_totoal)):
        hm_jy_XB_totoal_color.append('{:.2%}'.format(hm_jy_XB_totoal[i] / max(hm_jy_XB_totoal)))
    if hm_jy_XB_totoal_color[0] == 'nan%':
        a = 0
        for i in range(len(hm_jy_XB_totoal)):
            hm_jy_XB_totoal_color[i] = '{:.2%}'.format(a)
    for i in range(len(hm_jy_FB_totoal)):
        hm_jy_FB_totoal_color.append('{:.2%}'.format(hm_jy_FB_totoal[i] / max(hm_jy_FB_totoal)))
    if hm_jy_FB_totoal_color[0] == 'nan%':
        a = 0
        for i in range(len(hm_jy_FB_totoal)):
            hm_jy_FB_totoal_color[i] = '{:.2%}'.format(a)
    for i in range(len(hm_jy_DB_totoal)):
        hm_jy_DB_totoal_color.append('{:.2%}'.format(hm_jy_DB_totoal[i] / max(hm_jy_DB_totoal)))
    if hm_jy_DB_totoal_color[0] == 'nan%':
        a = 0
        for i in range(len(hm_jy_DB_totoal)):
            hm_jy_DB_totoal_color[i] = '{:.2%}'.format(a)
    for i in range(len(tx_jy_XB_totoal)):
        tx_jy_XB_totoal_color.append('{:.2%}'.format(tx_jy_XB_totoal[i] / max(tx_jy_XB_totoal)))
    if tx_jy_XB_totoal_color[0] == 'nan%':
        a = 0
        for i in range(len(tx_jy_XB_totoal)):
            tx_jy_XB_totoal_color[i] = '{:.2%}'.format(a)
    for i in range(len(tx_jy_FB_totoal)):
        tx_jy_FB_totoal_color.append('{:.2%}'.format(tx_jy_FB_totoal[i] / max(tx_jy_FB_totoal)))
    if tx_jy_FB_totoal_color[0] == 'nan%':
        a = 0
        for i in range(len(tx_jy_FB_totoal)):
            tx_jy_FB_totoal_color[i] = '{:.2%}'.format(a)
    for i in range(len(tx_jy_DB_totoal)):
        tx_jy_DB_totoal_color.append('{:.2%}'.format(tx_jy_DB_totoal[i] / max(tx_jy_DB_totoal)))
    if tx_jy_DB_totoal_color[0] == 'nan%':
        a = 0
        for i in range(len(tx_jy_DB_totoal)):
            tx_jy_DB_totoal_color[i] = '{:.2%}'.format(a)

    jsonData['dcl2_in'] = dcl2_in
    jsonData['dcl2_out'] = dcl2_out
    jsonData['dcl2_fba'] = dcl2_fba

    jsonData['db_in'] = db_in
    jsonData['db_out'] = db_out
    jsonData['db_total'] = db_total
    jsonData['db_date'] = db_date
    jsonData['dcl_1'] = dcl_1
    jsonData['dcl_2'] = dcl_2
    jsonData['dcl_3'] = dcl_3
    jsonData['dcl_4'] = dcl_4
    jsonData['zt_date'] = zt_date
    jsonData['zt_1'] = zt_1
    jsonData['zt_2'] = zt_2
    jsonData['zt_3'] = zt_3
    jsonData['zt_4'] = zt_4
    jsonData['zt_5'] = zt_5

    jsonData['hm_change'] = hm_change
    jsonData['tx_change'] = tx_change
    jsonData['hm_total'] = hm_total
    jsonData['tx_total'] = tx_total
    jsonData['hm_jy_XB_totoal'] = hm_jy_XB_totoal
    jsonData['hm_jy_FB_totoal'] = hm_jy_FB_totoal
    jsonData['tx_jy_XB_totoal'] = tx_jy_XB_totoal
    jsonData['tx_jy_FB_totoal'] = tx_jy_FB_totoal
    jsonData['hm_jy_DB_totoal'] = hm_jy_DB_totoal
    jsonData['tx_jy_DB_totoal'] = tx_jy_DB_totoal
    jsonData['hm_jy_XB_totoal_color'] = hm_jy_XB_totoal_color
    jsonData['hm_jy_FB_totoal_color'] = hm_jy_FB_totoal_color
    jsonData['hm_jy_DB_totoal_color'] = hm_jy_DB_totoal_color
    jsonData['tx_jy_XB_totoal_color'] = tx_jy_XB_totoal_color
    jsonData['tx_jy_FB_totoal_color'] = tx_jy_FB_totoal_color
    jsonData['tx_jy_DB_totoal_color'] = tx_jy_DB_totoal_color
    jsonData['hm_zl_cost'] = hm_zl_cost
    jsonData['hm_zl_time'] = hm_zl_time
    jsonData['tx_zl_cost'] = tx_zl_cost
    jsonData['tx_zl_time'] = tx_zl_time

    jsonData['tx_sx_date'] = tx_sx_date
    jsonData['hm_sx_date'] = hm_sx_date
    jsonData['hm_sx_in'] = hm_sx_in
    jsonData['hm_sx_out'] = hm_sx_out
    jsonData['hm_sx_fba'] = hm_sx_fba
    jsonData['tx_sx_in'] = tx_sx_in
    jsonData['tx_sx_out'] = tx_sx_out
    jsonData['tx_sx_fba'] = tx_sx_fba
    jsonData['hm_rk_in'] = hm_rk_in
    jsonData['hm_rk_out'] = hm_rk_out
    jsonData['hm_rk_ld'] = hm_rk_ld
    jsonData['tx_rk_in'] = tx_rk_in
    jsonData['tx_rk_out'] = tx_rk_out
    jsonData['tx_rk_ld'] = tx_rk_ld
    jsonData['hm_tph_date'] = hm_tph_date
    jsonData['hm_tph'] = hm_tph
    jsonData['hm_uph'] = hm_uph
    jsonData['tx_tph_date'] = tx_tph_date
    jsonData['tx_tph'] = tx_tph
    jsonData['tx_uph'] = tx_uph
    j = json.dumps(jsonData, cls=DecimalEncoder)
    return (j)


@app.route('/daily2', methods=['POST'])
def diaobo_daily():
   # sql = 'SELECT	real_warehouse_code,	purchase_order_no,	status,	sku,	purchase_qty,  cast( ROUND( ( unix_timestamp( now( ) ) - unix_timestamp( create_time ) ) / 3600, 2 ) AS DECIMAL ) AS s FROM	ueb_purchase WHERE	is_del = 1 	AND warehouse_type = 1 	AND purchase_type IN ( 3, 4 ) GROUP BY	purchase_order_no ,SKU,real_warehouse_code,status order by s DESC'
   # sql2 = 'select * from (select warehouse_code,order_id,case when pay_time >0 and wait_pull_time >0 and pick_time >0 and  pack_time >0 and outstock_time > 0 and delivery_time = 0  then "DJY"when pay_time >0 and wait_pull_time >0 and pick_time >0 and ((choice_time =0 and pack_time>0) or (choice_time >0 and pack_time >0)) and outstock_time = 0  then "DCK"when pay_time >0 and wait_pull_time >0 and pick_time >0 and pack_time = 0  then "DDB"when pay_time >0 and wait_pull_time >0 and pick_time =0  then "DJH"when pay_time >0 and wait_pull_time =0  then "DLD"ELSE "else" end as `status`,order_product_number,ROUND(( unix_timestamp(now()) - greatest(pay_time,wait_pull_time,pick_time,choice_time,pack_time) ) / 3600, 2 ) AS time from ueb_order_operate_time where order_is_cancel =0 and delivery_time = 0 and order_id like "ALLOT%"  union    select warehouse_code,order_id,"DLD" as `status`,sum(order_product_number) as `order_product_number`,ROUND(( unix_timestamp(now()) - wait_pull_time) / 3600, 2 ) AS time       from ueb_order where order_id like "ALLOT%" and wh_order_status in(1,2)  group by warehouse_code,order_id) a  order by time  DESC'

    warehouse = []
    order_id = []
    status = []
    num = []
    s = []
    jsonData = {}

    input = pd.read_excel('daily2_sql.xlsx')
    see=save(input)
    input = pd.read_excel('daily2_sql2.xlsx')
    see_ck=save(input)



    for data in see:
        warehouse.append(data[0])
        order_id.append(data[1])
        status.append(data[2])
        num.append(decimal.Decimal(data[4]))
        s.append(decimal.Decimal(data[5]))

    warehouse_ck = []
    order_id_ck = []
    status_ck = []
    num_ck = []
    s_ck = []

    for data_ck in see_ck:
        warehouse_ck.append(data_ck[0])
        order_id_ck.append(data_ck[1])
        status_ck.append(data_ck[2])
        num_ck.append(decimal.Decimal(data_ck[3]))
        s_ck.append(decimal.Decimal(data_ck[4]))

    hm_order_id_ck = []
    hm_status_ck = []
    hm_num_ck = []
    hm_s_ck = []

    tx_order_id_ck = []
    tx_status_ck = []
    tx_num_ck = []
    tx_s_ck = []

    for i in range(len(warehouse_ck)):
        if warehouse_ck[i] == "HM_AA":
            hm_order_id_ck.append(order_id_ck[i])
            hm_status_ck.append(status_ck[i])
            hm_num_ck.append(num_ck[i])
            hm_s_ck.append(s_ck[i])
    for i in range(len(warehouse_ck)):
        if warehouse_ck[i] == "SZ_AA":
            tx_order_id_ck.append(order_id_ck[i])
            tx_status_ck.append(status_ck[i])
            tx_num_ck.append(num_ck[i])
            tx_s_ck.append(s_ck[i])
    hm_data_ck = np.dstack((hm_order_id_ck, hm_status_ck, hm_num_ck, hm_s_ck))
    tx_data_ck = np.dstack((tx_order_id_ck, tx_status_ck, tx_num_ck, tx_s_ck))

    hm_ck_dld_order = []
    hm_ck_dld_num = []
    hm_ck_dld_s = []
    hm_ck_djh_order = []
    hm_ck_djh_num = []
    hm_ck_djh_s = []
    hm_ck_ddb_order = []
    hm_ck_ddb_num = []
    hm_ck_ddb_s = []
    hm_ck_dck_order = []
    hm_ck_dck_num = []
    hm_ck_dck_s = []
    hm_ck_djy_order = []
    hm_ck_djy_num = []
    hm_ck_djy_s = []
    tx_ck_dld_order = []
    tx_ck_dld_num = []
    tx_ck_dld_s = []
    tx_ck_djh_order = []
    tx_ck_djh_num = []
    tx_ck_djh_s = []
    tx_ck_ddb_order = []
    tx_ck_ddb_num = []
    tx_ck_ddb_s = []
    tx_ck_dck_order = []
    tx_ck_dck_num = []
    tx_ck_dck_s = []
    tx_ck_djy_order = []
    tx_ck_djy_num = []
    tx_ck_djy_s = []
    for i in range(len(hm_data_ck[0])):
        if (hm_data_ck[0][i][1] == "DLD"):
            hm_ck_dld_order.append(hm_data_ck[0][i][0])
            hm_ck_dld_num.append(hm_data_ck[0][i][2])
            hm_ck_dld_s.append(hm_data_ck[0][i][3])

    for i in range(len(hm_data_ck[0])):
        if (hm_data_ck[0][i][1] == "DJH"):
            hm_ck_djh_order.append(hm_data_ck[0][i][0])
            hm_ck_djh_num.append(hm_data_ck[0][i][2])
            hm_ck_djh_s.append(hm_data_ck[0][i][3])

    for i in range(len(hm_data_ck[0])):
        if (hm_data_ck[0][i][1] == "DDB"):
            hm_ck_ddb_order.append(hm_data_ck[0][i][0])
            hm_ck_ddb_num.append(hm_data_ck[0][i][2])
            hm_ck_ddb_s.append(hm_data_ck[0][i][3])
    for i in range(len(hm_data_ck[0])):
        if (hm_data_ck[0][i][1] == "DCK"):
            hm_ck_dck_order.append(hm_data_ck[0][i][0])
            hm_ck_dck_num.append(hm_data_ck[0][i][2])
            hm_ck_dck_s.append(hm_data_ck[0][i][3])
    for i in range(len(hm_data_ck[0])):
        if (hm_data_ck[0][i][1] == "DJY"):
            hm_ck_djy_order.append(hm_data_ck[0][i][0])
            hm_ck_djy_num.append(hm_data_ck[0][i][2])
            hm_ck_djy_s.append(hm_data_ck[0][i][3])

    for i in range(len(tx_data_ck[0])):
        if (tx_data_ck[0][i][1] == "DLD"):
            tx_ck_dld_order.append(tx_data_ck[0][i][0])
            tx_ck_dld_num.append(tx_data_ck[0][i][2])
            tx_ck_dld_s.append(tx_data_ck[0][i][3])

    for i in range(len(tx_data_ck[0])):
        if (tx_data_ck[0][i][1] == "DJH"):
            tx_ck_djh_order.append(tx_data_ck[0][i][0])
            tx_ck_djh_num.append(tx_data_ck[0][i][2])
            tx_ck_djh_s.append(tx_data_ck[0][i][3])
    for i in range(len(tx_data_ck[0])):
        if (tx_data_ck[0][i][1] == "DDB"):
            tx_ck_ddb_order.append(tx_data_ck[0][i][0])
            tx_ck_ddb_num.append(tx_data_ck[0][i][2])
            tx_ck_ddb_s.append(tx_data_ck[0][i][3])
    for i in range(len(tx_data_ck[0])):
        if (tx_data_ck[0][i][1] == "DCK"):
            tx_ck_dck_order.append(tx_data_ck[0][i][0])
            tx_ck_dck_num.append(tx_data_ck[0][i][2])
            tx_ck_dck_s.append(tx_data_ck[0][i][3])
    for i in range(len(tx_data_ck[0])):
        if (tx_data_ck[0][i][1] == "DJY"):
            tx_ck_djy_order.append(tx_data_ck[0][i][0])
            tx_ck_djy_num.append(tx_data_ck[0][i][2])
            tx_ck_djy_s.append(tx_data_ck[0][i][3])
    hm_dld = np.dstack((hm_ck_dld_order, hm_ck_dld_num, hm_ck_dld_s))
    hm_djh = np.dstack((hm_ck_djh_order, hm_ck_djh_num, hm_ck_djh_s))
    hm_ddb = np.dstack((hm_ck_ddb_order, hm_ck_ddb_num, hm_ck_ddb_s))
    hm_dck = np.dstack((hm_ck_dck_order, hm_ck_dck_num, hm_ck_dck_s))
    hm_djy = np.dstack((hm_ck_djy_order, hm_ck_djy_num, hm_ck_djy_s))
    tx_dld = np.dstack((tx_ck_dld_order, tx_ck_dld_num, tx_ck_dld_s))
    tx_djh = np.dstack((tx_ck_djh_order, tx_ck_djh_num, tx_ck_djh_s))
    tx_ddb = np.dstack((tx_ck_ddb_order, tx_ck_ddb_num, tx_ck_ddb_s))
    tx_dck = np.dstack((tx_ck_dck_order, tx_ck_dck_num, tx_ck_dck_s))
    tx_djy = np.dstack((tx_ck_djy_order, tx_ck_djy_num, tx_ck_djy_s))
    hm_dld_j = [0, 0, 0, 0, 0, 0, 0]
    hm_dld_b = [0, 0, 0, 0, 0, 0, 0]
    hm_djh_j = [0, 0, 0, 0, 0, 0, 0]
    hm_djh_b = [0, 0, 0, 0, 0, 0, 0]
    hm_ddb_j = [0, 0, 0, 0, 0, 0, 0]
    hm_ddb_b = [0, 0, 0, 0, 0, 0, 0]
    hm_dck_j = [0, 0, 0, 0, 0, 0, 0]
    hm_dck_b = [0, 0, 0, 0, 0, 0, 0]
    hm_djy_j = [0, 0, 0, 0, 0, 0, 0]
    hm_djy_b = [0, 0, 0, 0, 0, 0, 0]
    tx_dld_j = [0, 0, 0, 0, 0, 0, 0]
    tx_dld_b = [0, 0, 0, 0, 0, 0, 0]
    tx_djh_j = [0, 0, 0, 0, 0, 0, 0]
    tx_djh_b = [0, 0, 0, 0, 0, 0, 0]
    tx_ddb_j = [0, 0, 0, 0, 0, 0, 0]
    tx_ddb_b = [0, 0, 0, 0, 0, 0, 0]
    tx_dck_j = [0, 0, 0, 0, 0, 0, 0]
    tx_dck_b = [0, 0, 0, 0, 0, 0, 0]
    tx_djy_j = [0, 0, 0, 0, 0, 0, 0]
    tx_djy_b = [0, 0, 0, 0, 0, 0, 0]
    for i in range(len(hm_dld[0])):
        if float(hm_ck_dld_s[i]) > 0 and float(hm_ck_dld_s[i]) < 2:
            hm_dld_j[0] = hm_dld_j[0] + hm_dld[0][i][1]
        if float(hm_ck_dld_s[i]) > 2 and float(hm_ck_dld_s[i]) < 4:
            hm_dld_j[1] = hm_dld_j[1] + hm_dld[0][i][1]
        if float(hm_ck_dld_s[i]) > 4 and float(hm_ck_dld_s[i]) < 6:
            hm_dld_j[2] = hm_dld_j[2] + hm_dld[0][i][1]
        if float(hm_ck_dld_s[i]) > 6 and float(hm_ck_dld_s[i]) < 8:
            hm_dld_j[3] = hm_dld_j[3] + hm_dld[0][i][1]
        if float(hm_ck_dld_s[i]) > 8 and float(hm_ck_dld_s[i]) < 12:
            hm_dld_j[4] = hm_dld_j[4] + hm_dld[0][i][1]
        if float(hm_ck_dld_s[i]) > 12 and float(hm_ck_dld_s[i]) < 24:
            hm_dld_j[5] = hm_dld_j[5] + hm_dld[0][i][1]
        if float(hm_ck_dld_s[i]) > 24:
            hm_dld_j[6] = hm_dld_j[6] + hm_dld[0][i][1]
    for i in range(len(hm_dld[0])):
        if float(hm_ck_dld_s[i]) > 0 and float(hm_ck_dld_s[i]) < 2:
            hm_dld_b[0] = hm_dld_b[0] + 1
        if float(hm_ck_dld_s[i]) > 2 and float(hm_ck_dld_s[i]) < 4:
            hm_dld_b[1] = hm_dld_b[1] + 1
        if float(hm_ck_dld_s[i]) > 4 and float(hm_ck_dld_s[i]) < 6:
            hm_dld_b[2] = hm_dld_b[2] + 1
        if float(hm_ck_dld_s[i]) > 6 and float(hm_ck_dld_s[i]) < 8:
            hm_dld_b[3] = hm_dld_b[3] + 1
        if float(hm_ck_dld_s[i]) > 8 and float(hm_ck_dld_s[i]) < 12:
            hm_dld_b[4] = hm_dld_b[4] + 1
        if float(hm_ck_dld_s[i]) > 12 and float(hm_ck_dld_s[i]) < 24:
            hm_dld_b[5] = hm_dld_b[5] + 1
        if float(hm_ck_dld_s[i]) > 24:
            hm_dld_b[6] = hm_dld_b[6] + 1

    for i in range(len(hm_djh[0])):
        if float(hm_ck_djh_s[i]) > 0 and float(hm_ck_djh_s[i]) < 2:
            hm_djh_j[0] = hm_djh_j[0] + hm_djh[0][i][1]
        if float(hm_ck_djh_s[i]) > 2 and float(hm_ck_djh_s[i]) < 4:
            hm_djh_j[1] = hm_djh_j[1] + hm_djh[0][i][1]
        if float(hm_ck_djh_s[i]) > 4 and float(hm_ck_djh_s[i]) < 6:
            hm_djh_j[2] = hm_djh_j[2] + hm_djh[0][i][1]
        if float(hm_ck_djh_s[i]) > 6 and float(hm_ck_djh_s[i]) < 8:
            hm_djh_j[3] = hm_djh_j[3] + hm_djh[0][i][1]
        if float(hm_ck_djh_s[i]) > 8 and float(hm_ck_djh_s[i]) < 12:
            hm_djh_j[4] = hm_djh_j[4] + hm_djh[0][i][1]
        if float(hm_ck_djh_s[i]) > 12 and float(hm_ck_djh_s[i]) < 24:
            hm_djh_j[5] = hm_djh_j[5] + hm_djh[0][i][1]
        if float(hm_ck_djh_s[i]) > 24:
            hm_djh_j[6] = hm_djh_j[6] + hm_djh[0][i][1]
    for i in range(len(hm_djh[0])):
        if float(hm_ck_djh_s[i]) > 0 and float(hm_ck_djh_s[i]) < 2:
            hm_djh_b[0] = hm_djh_b[0] + 1
        if float(hm_ck_djh_s[i]) > 2 and float(hm_ck_djh_s[i]) < 4:
            hm_djh_b[1] = hm_djh_b[1] + 1
        if float(hm_ck_djh_s[i]) > 4 and float(hm_ck_djh_s[i]) < 6:
            hm_djh_b[2] = hm_djh_b[2] + 1
        if float(hm_ck_djh_s[i]) > 6 and float(hm_ck_djh_s[i]) < 8:
            hm_djh_b[3] = hm_djh_b[3] + 1
        if float(hm_ck_djh_s[i]) > 8 and float(hm_ck_djh_s[i]) < 12:
            hm_djh_b[4] = hm_djh_b[4] + 1
        if float(hm_ck_djh_s[i]) > 12 and float(hm_ck_djh_s[i]) < 24:
            hm_djh_b[5] = hm_djh_b[5] + 1
        if float(hm_ck_djh_s[i]) > 24:
            hm_djh_b[6] = hm_djh_b[6] + 1

    for i in range(len(hm_ddb[0])):
        if float(hm_ck_ddb_s[i]) > 0 and float(hm_ck_ddb_s[i]) < 2:
            hm_ddb_j[0] = hm_ddb_j[0] + hm_ddb[0][i][1]
        if float(hm_ck_ddb_s[i]) > 2 and float(hm_ck_ddb_s[i]) < 4:
            hm_ddb_j[1] = hm_ddb_j[1] + hm_ddb[0][i][1]
        if float(hm_ck_ddb_s[i]) > 4 and float(hm_ck_ddb_s[i]) < 6:
            hm_ddb_j[2] = hm_ddb_j[2] + hm_ddb[0][i][1]
        if float(hm_ck_ddb_s[i]) > 6 and float(hm_ck_ddb_s[i]) < 8:
            hm_ddb_j[3] = hm_ddb_j[3] + hm_ddb[0][i][1]
        if float(hm_ck_ddb_s[i]) > 8 and float(hm_ck_ddb_s[i]) < 12:
            hm_ddb_j[4] = hm_ddb_j[4] + hm_ddb[0][i][1]
        if float(hm_ck_ddb_s[i]) > 12 and float(hm_ck_ddb_s[i]) < 24:
            hm_ddb_j[5] = hm_ddb_j[5] + hm_ddb[0][i][1]
        if float(hm_ck_ddb_s[i]) > 24:
            hm_ddb_j[6] = hm_ddb_j[6] + hm_ddb[0][i][1]
    for i in range(len(hm_ddb[0])):
        if float(hm_ck_ddb_s[i]) > 0 and float(hm_ck_ddb_s[i]) < 2:
            hm_ddb_b[0] = hm_ddb_b[0] + 1
        if float(hm_ck_ddb_s[i]) > 2 and float(hm_ck_ddb_s[i]) < 4:
            hm_ddb_b[1] = hm_ddb_b[1] + 1
        if float(hm_ck_ddb_s[i]) > 4 and float(hm_ck_ddb_s[i]) < 6:
            hm_ddb_b[2] = hm_ddb_b[2] + 1
        if float(hm_ck_ddb_s[i]) > 6 and float(hm_ck_ddb_s[i]) < 8:
            hm_ddb_b[3] = hm_ddb_b[3] + 1
        if float(hm_ck_ddb_s[i]) > 8 and float(hm_ck_ddb_s[i]) < 12:
            hm_ddb_b[4] = hm_ddb_b[4] + 1
        if float(hm_ck_ddb_s[i]) > 12 and float(hm_ck_ddb_s[i]) < 24:
            hm_ddb_b[5] = hm_ddb_b[5] + 1
        if float(hm_ck_ddb_s[i]) > 24:
            hm_ddb_b[6] = hm_ddb_b[6] + 1
    for i in range(len(hm_dck[0])):
        if float(hm_ck_dck_s[i]) > 0 and float(hm_ck_dck_s[i]) < 2:
            hm_dck_j[0] = hm_dck_j[0] + hm_dck[0][i][1]
        if float(hm_ck_dck_s[i]) > 2 and float(hm_ck_dck_s[i]) < 4:
            hm_dck_j[1] = hm_dck_j[1] + hm_dck[0][i][1]
        if float(hm_ck_dck_s[i]) > 4 and float(hm_ck_dck_s[i]) < 6:
            hm_dck_j[2] = hm_dck_j[2] + hm_dck[0][i][1]
        if float(hm_ck_dck_s[i]) > 6 and float(hm_ck_dck_s[i]) < 8:
            hm_dck_j[3] = hm_dck_j[3] + hm_dck[0][i][1]
        if float(hm_ck_dck_s[i]) > 8 and float(hm_ck_dck_s[i]) < 12:
            hm_dck_j[4] = hm_dck_j[4] + hm_dck[0][i][1]
        if float(hm_ck_dck_s[i]) > 12 and float(hm_ck_dck_s[i]) < 24:
            hm_dck_j[5] = hm_dck_j[5] + hm_dck[0][i][1]
        if float(hm_ck_dck_s[i]) > 24:
            hm_dck_j[6] = hm_dck_j[6] + hm_dck[0][i][1]
    for i in range(len(hm_dck[0])):
        if float(hm_ck_dck_s[i]) > 0 and float(hm_ck_dck_s[i]) < 2:
            hm_dck_b[0] = hm_dck_b[0] + 1
        if float(hm_ck_dck_s[i]) > 2 and float(hm_ck_dck_s[i]) < 4:
            hm_dck_b[1] = hm_dck_b[1] + 1
        if float(hm_ck_dck_s[i]) > 4 and float(hm_ck_dck_s[i]) < 6:
            hm_dck_b[2] = hm_dck_b[2] + 1
        if float(hm_ck_dck_s[i]) > 6 and float(hm_ck_dck_s[i]) < 8:
            hm_dck_b[3] = hm_dck_b[3] + 1
        if float(hm_ck_dck_s[i]) > 8 and float(hm_ck_dck_s[i]) < 12:
            hm_dck_b[4] = hm_dck_b[4] + 1
        if float(hm_ck_dck_s[i]) > 12 and float(hm_ck_dck_s[i]) < 24:
            hm_dck_b[5] = hm_dck_b[5] + 1
        if float(hm_ck_dck_s[i]) > 24:
            hm_dck_b[6] = hm_dck_b[6] + 1
    for i in range(len(hm_djy[0])):
        if float(hm_ck_djy_s[i]) > 0 and float(hm_ck_djy_s[i]) < 2:
            hm_djy_j[0] = hm_djy_j[0] + hm_djy[0][i][1]
        if float(hm_ck_djy_s[i]) > 2 and float(hm_ck_djy_s[i]) < 4:
            hm_djy_j[1] = hm_djy_j[1] + hm_djy[0][i][1]
        if float(hm_ck_djy_s[i]) > 4 and float(hm_ck_djy_s[i]) < 6:
            hm_djy_j[2] = hm_djy_j[2] + hm_djy[0][i][1]
        if float(hm_ck_djy_s[i]) > 6 and float(hm_ck_djy_s[i]) < 8:
            hm_djy_j[3] = hm_djy_j[3] + hm_djy[0][i][1]
        if float(hm_ck_djy_s[i]) > 8 and float(hm_ck_djy_s[i]) < 12:
            hm_djy_j[4] = hm_djy_j[4] + hm_djy[0][i][1]
        if float(hm_ck_djy_s[i]) > 12 and float(hm_ck_djy_s[i]) < 24:
            hm_djy_j[5] = hm_djy_j[5] + hm_djy[0][i][1]
        if float(hm_ck_djy_s[i]) > 24:
            hm_djy_j[6] = hm_djy_j[6] + hm_djy[0][i][1]
    for i in range(len(hm_djy[0])):
        if float(hm_ck_djy_s[i]) > 0 and float(hm_ck_djy_s[i]) < 2:
            hm_djy_b[0] = hm_djy_b[0] + 1
        if float(hm_ck_djy_s[i]) > 2 and float(hm_ck_djy_s[i]) < 4:
            hm_djy_b[1] = hm_djy_b[1] + 1
        if float(hm_ck_djy_s[i]) > 4 and float(hm_ck_djy_s[i]) < 6:
            hm_djy_b[2] = hm_djy_b[2] + 1
        if float(hm_ck_djy_s[i]) > 6 and float(hm_ck_djy_s[i]) < 8:
            hm_djy_b[3] = hm_djy_b[3] + 1
        if float(hm_ck_djy_s[i]) > 8 and float(hm_ck_djy_s[i]) < 12:
            hm_djy_b[4] = hm_djy_b[4] + 1
        if float(hm_ck_djy_s[i]) > 12 and float(hm_ck_djy_s[i]) < 24:
            hm_djy_b[5] = hm_djy_b[5] + 1
        if float(hm_ck_djy_s[i]) > 24:
            hm_djy_b[6] = hm_djy_b[6] + 1
    for i in range(len(tx_dld[0])):
        if float(tx_ck_dld_s[i]) > 0 and float(tx_ck_dld_s[i]) < 2:
            tx_dld_j[0] = tx_dld_j[0] + tx_dld[0][i][1]
        if float(tx_ck_dld_s[i]) > 2 and float(tx_ck_dld_s[i]) < 4:
            tx_dld_j[1] = tx_dld_j[1] + tx_dld[0][i][1]
        if float(tx_ck_dld_s[i]) > 4 and float(tx_ck_dld_s[i]) < 6:
            tx_dld_j[2] = tx_dld_j[2] + tx_dld[0][i][1]
        if float(tx_ck_dld_s[i]) > 6 and float(tx_ck_dld_s[i]) < 8:
            tx_dld_j[3] = tx_dld_j[3] + tx_dld[0][i][1]
        if float(tx_ck_dld_s[i]) > 8 and float(tx_ck_dld_s[i]) < 12:
            tx_dld_j[4] = tx_dld_j[4] + tx_dld[0][i][1]
        if float(tx_ck_dld_s[i]) > 12 and float(tx_ck_dld_s[i]) < 24:
            tx_dld_j[5] = tx_dld_j[5] + tx_dld[0][i][1]
        if float(tx_ck_dld_s[i]) > 24:
            tx_dld_j[6] = tx_dld_j[6] + tx_dld[0][i][1]
    for i in range(len(tx_dld[0])):
        if float(tx_ck_dld_s[i]) > 0 and float(tx_ck_dld_s[i]) < 2:
            tx_dld_b[0] = tx_dld_b[0] + 1
        if float(tx_ck_dld_s[i]) > 2 and float(tx_ck_dld_s[i]) < 4:
            tx_dld_b[1] = tx_dld_b[1] + 1
        if float(tx_ck_dld_s[i]) > 4 and float(tx_ck_dld_s[i]) < 6:
            tx_dld_b[2] = tx_dld_b[2] + 1
        if float(tx_ck_dld_s[i]) > 6 and float(tx_ck_dld_s[i]) < 8:
            tx_dld_b[3] = tx_dld_b[3] + 1
        if float(tx_ck_dld_s[i]) > 8 and float(tx_ck_dld_s[i]) < 12:
            tx_dld_b[4] = tx_dld_b[4] + 1
        if float(tx_ck_dld_s[i]) > 12 and float(tx_ck_dld_s[i]) < 24:
            tx_dld_b[5] = tx_dld_b[5] + 1
        if float(tx_ck_dld_s[i]) > 24:
            tx_dld_b[6] = tx_dld_b[6] + 1
    for i in range(len(tx_djh[0])):
        if float(tx_ck_djh_s[i]) > 0 and float(tx_ck_djh_s[i]) < 2:
            tx_djh_j[0] = tx_djh_j[0] + tx_djh[0][i][1]
        if float(tx_ck_djh_s[i]) > 2 and float(tx_ck_djh_s[i]) < 4:
            tx_djh_j[1] = tx_djh_j[1] + tx_djh[0][i][1]
        if float(tx_ck_djh_s[i]) > 4 and float(tx_ck_djh_s[i]) < 6:
            tx_djh_j[2] = tx_djh_j[2] + tx_djh[0][i][1]
        if float(tx_ck_djh_s[i]) > 6 and float(tx_ck_djh_s[i]) < 8:
            tx_djh_j[3] = tx_djh_j[3] + tx_djh[0][i][1]
        if float(tx_ck_djh_s[i]) > 8 and float(tx_ck_djh_s[i]) < 12:
            tx_djh_j[4] = tx_djh_j[4] + tx_djh[0][i][1]
        if float(tx_ck_djh_s[i]) > 12 and float(tx_ck_djh_s[i]) < 24:
            tx_djh_j[5] = tx_djh_j[5] + tx_djh[0][i][1]
        if float(tx_ck_djh_s[i]) > 24:
            tx_djh_j[6] = tx_djh_j[6] + tx_djh[0][i][1]
    for i in range(len(tx_djh[0])):
        if float(tx_ck_djh_s[i]) > 0 and float(tx_ck_djh_s[i]) < 2:
            tx_djh_b[0] = tx_djh_b[0] + 1
        if float(tx_ck_djh_s[i]) > 2 and float(tx_ck_djh_s[i]) < 4:
            tx_djh_b[1] = tx_djh_b[1] + 1
        if float(tx_ck_djh_s[i]) > 4 and float(tx_ck_djh_s[i]) < 6:
            tx_djh_b[2] = tx_djh_b[2] + 1
        if float(tx_ck_djh_s[i]) > 6 and float(tx_ck_djh_s[i]) < 8:
            tx_djh_b[3] = tx_djh_b[3] + 1
        if float(tx_ck_djh_s[i]) > 8 and float(tx_ck_djh_s[i]) < 12:
            tx_djh_b[4] = tx_djh_b[4] + 1
        if float(tx_ck_djh_s[i]) > 12 and float(tx_ck_djh_s[i]) < 24:
            tx_djh_b[5] = tx_djh_b[5] + 1
        if float(tx_ck_djh_s[i]) > 24:
            tx_djh_b[6] = tx_djh_b[6] + 1

    for i in range(len(tx_ddb[0])):
        if float(tx_ck_ddb_s[i]) > 0 and float(tx_ck_ddb_s[i]) < 2:
            tx_ddb_j[0] = tx_ddb_j[0] + tx_ddb[0][i][1]
        if float(tx_ck_ddb_s[i]) > 2 and float(tx_ck_ddb_s[i]) < 4:
            tx_ddb_j[1] = tx_ddb_j[1] + tx_ddb[0][i][1]
        if float(tx_ck_ddb_s[i]) > 4 and float(tx_ck_ddb_s[i]) < 6:
            tx_ddb_j[2] = tx_ddb_j[2] + tx_ddb[0][i][1]
        if float(tx_ck_ddb_s[i]) > 6 and float(tx_ck_ddb_s[i]) < 8:
            tx_ddb_j[3] = tx_ddb_j[3] + tx_ddb[0][i][1]
        if float(tx_ck_ddb_s[i]) > 8 and float(tx_ck_ddb_s[i]) < 12:
            tx_ddb_j[4] = tx_ddb_j[4] + tx_ddb[0][i][1]
        if float(tx_ck_ddb_s[i]) > 12 and float(tx_ck_ddb_s[i]) < 24:
            tx_ddb_j[5] = tx_ddb_j[5] + tx_ddb[0][i][1]
        if float(tx_ck_ddb_s[i]) > 24:
            tx_ddb_j[6] = tx_ddb_j[6] + tx_ddb[0][i][1]
    for i in range(len(tx_ddb[0])):
        if float(tx_ck_ddb_s[i]) > 0 and float(tx_ck_ddb_s[i]) < 2:
            tx_ddb_b[0] = tx_ddb_b[0] + 1
        if float(tx_ck_ddb_s[i]) > 2 and float(tx_ck_ddb_s[i]) < 4:
            tx_ddb_b[1] = tx_ddb_b[1] + 1
        if float(tx_ck_ddb_s[i]) > 4 and float(tx_ck_ddb_s[i]) < 6:
            tx_ddb_b[2] = tx_ddb_b[2] + 1
        if float(tx_ck_ddb_s[i]) > 6 and float(tx_ck_ddb_s[i]) < 8:
            tx_ddb_b[3] = tx_ddb_b[3] + 1
        if float(tx_ck_ddb_s[i]) > 8 and float(tx_ck_ddb_s[i]) < 12:
            tx_ddb_b[4] = tx_ddb_b[4] + 1
        if float(tx_ck_ddb_s[i]) > 12 and float(tx_ck_ddb_s[i]) < 24:
            tx_ddb_b[5] = tx_ddb_b[5] + 1
        if float(tx_ck_ddb_s[i]) > 24:
            tx_ddb_b[6] = tx_ddb_b[6] + 1
    for i in range(len(tx_dck[0])):
        if float(tx_ck_dck_s[i]) > 0 and float(tx_ck_dck_s[i]) < 2:
            tx_dck_j[0] = tx_dck_j[0] + tx_dck[0][i][1]
        if float(tx_ck_dck_s[i]) > 2 and float(tx_ck_dck_s[i]) < 4:
            tx_dck_j[1] = tx_dck_j[1] + tx_dck[0][i][1]
        if float(tx_ck_dck_s[i]) > 4 and float(tx_ck_dck_s[i]) < 6:
            tx_dck_j[2] = tx_dck_j[2] + tx_dck[0][i][1]
        if float(tx_ck_dck_s[i]) > 6 and float(tx_ck_dck_s[i]) < 8:
            tx_dck_j[3] = tx_dck_j[3] + tx_dck[0][i][1]
        if float(tx_ck_dck_s[i]) > 8 and float(tx_ck_dck_s[i]) < 12:
            tx_dck_j[4] = tx_dck_j[4] + tx_dck[0][i][1]
        if float(tx_ck_dck_s[i]) > 12 and float(tx_ck_dck_s[i]) < 24:
            tx_dck_j[5] = tx_dck_j[5] + tx_dck[0][i][1]
        if float(tx_ck_dck_s[i]) > 24:
            tx_dck_j[6] = tx_dck_j[6] + tx_dck[0][i][1]
    for i in range(len(tx_dck[0])):
        if float(tx_ck_dck_s[i]) > 0 and float(tx_ck_dck_s[i]) < 2:
            tx_dck_b[0] = tx_dck_b[0] + 1
        if float(tx_ck_dck_s[i]) > 2 and float(tx_ck_dck_s[i]) < 4:
            tx_dck_b[1] = tx_dck_b[1] + 1
        if float(tx_ck_dck_s[i]) > 4 and float(tx_ck_dck_s[i]) < 6:
            tx_dck_b[2] = tx_dck_b[2] + 1
        if float(tx_ck_dck_s[i]) > 6 and float(tx_ck_dck_s[i]) < 8:
            tx_dck_b[3] = tx_dck_b[3] + 1
        if float(tx_ck_dck_s[i]) > 8 and float(tx_ck_dck_s[i]) < 12:
            tx_dck_b[4] = tx_dck_b[4] + 1
        if float(tx_ck_dck_s[i]) > 12 and float(tx_ck_dck_s[i]) < 24:
            tx_dck_b[5] = tx_dck_b[5] + 1
        if float(tx_ck_dck_s[i]) > 24:
            tx_dck_b[6] = tx_dck_b[6] + 1
    for i in range(len(tx_djy[0])):
        if float(tx_ck_djy_s[i]) > 0 and float(tx_ck_djy_s[i]) < 2:
            tx_djy_j[0] = tx_djy_j[0] + tx_djy[0][i][1]
        if float(tx_ck_djy_s[i]) > 2 and float(tx_ck_djy_s[i]) < 4:
            tx_djy_j[1] = tx_djy_j[1] + tx_djy[0][i][1]
        if float(tx_ck_djy_s[i]) > 4 and float(tx_ck_djy_s[i]) < 6:
            tx_djy_j[2] = tx_djy_j[2] + tx_djy[0][i][1]
        if float(tx_ck_djy_s[i]) > 6 and float(tx_ck_djy_s[i]) < 8:
            tx_djy_j[3] = tx_djy_j[3] + tx_djy[0][i][1]
        if float(tx_ck_djy_s[i]) > 8 and float(tx_ck_djy_s[i]) < 12:
            tx_djy_j[4] = tx_djy_j[4] + tx_djy[0][i][1]
        if float(tx_ck_djy_s[i]) > 12 and float(tx_ck_djy_s[i]) < 24:
            tx_djy_j[5] = tx_djy_j[5] + tx_djy[0][i][1]
        if float(tx_ck_djy_s[i]) > 24:
            tx_djy_j[6] = tx_djy_j[6] + tx_djy[0][i][1]
    for i in range(len(tx_djy[0])):
        if float(tx_ck_djy_s[i]) > 0 and float(tx_ck_djy_s[i]) < 2:
            tx_djy_b[0] = tx_djy_b[0] + 1
        if float(tx_ck_djy_s[i]) > 2 and float(tx_ck_djy_s[i]) < 4:
            tx_djy_b[1] = tx_djy_b[1] + 1
        if float(tx_ck_djy_s[i]) > 4 and float(tx_ck_djy_s[i]) < 6:
            tx_djy_b[2] = tx_djy_b[2] + 1
        if float(tx_ck_djy_s[i]) > 6 and float(tx_ck_djy_s[i]) < 8:
            tx_djy_b[3] = tx_djy_b[3] + 1
        if float(tx_ck_djy_s[i]) > 8 and float(tx_ck_djy_s[i]) < 12:
            tx_djy_b[4] = tx_djy_b[4] + 1
        if float(tx_ck_djy_s[i]) > 12 and float(tx_ck_djy_s[i]) < 24:
            tx_djy_b[5] = tx_djy_b[5] + 1
        if float(tx_ck_djy_s[i]) > 24:
            tx_djy_b[6] = tx_djy_b[6] + 1
    hm_ck_dld_j_color = []
    hm_ck_djh_j_color = []
    hm_ck_ddb_j_color = []
    hm_ck_dck_j_color = []
    hm_ck_djy_j_color = []
    hm_ck_dld_b_color = []
    hm_ck_djh_b_color = []
    hm_ck_ddb_b_color = []
    hm_ck_dck_b_color = []
    hm_ck_djy_b_color = []
    tx_ck_dld_j_color = []
    tx_ck_djh_j_color = []
    tx_ck_ddb_j_color = []
    tx_ck_dck_j_color = []
    tx_ck_djy_j_color = []
    tx_ck_dld_b_color = []
    tx_ck_djh_b_color = []
    tx_ck_ddb_b_color = []
    tx_ck_dck_b_color = []
    tx_ck_djy_b_color = []

    arrayA = np.divide(hm_dld_j, max(hm_dld_j), out=np.zeros_like(hm_dld_j, dtype=np.float64), where=max(hm_dld_j) != 0,
                       casting="unsafe")
    for i in range(len(hm_dld_j)):
        hm_ck_dld_j_color.append("%.2f%%" % (arrayA[i] * 100))
    if hm_dld_j[0] == 'nan%':
        a = 0
        for i in range(len(hm_dld_j)):
            hm_dld_j[i] = '{:.2%}'.format(a)

    arrayA = np.divide(hm_djh_j, max(hm_djh_j), out=np.zeros_like(hm_djh_j, dtype=np.float64), casting="unsafe",
                       where=max(hm_djh_j) != 0)
    for i in range(len(hm_djh_j)):
        hm_ck_djh_j_color.append("%.2f%%" % (arrayA[i] * 100))
    if hm_djh_j[0] == 'nan%':
        a = 0
        for i in range(len(hm_djh_j)):
            hm_djh_j[i] = '{:.2%}'.format(a)

    arrayA = np.divide(hm_ddb_j, max(hm_ddb_j), out=np.zeros_like(hm_ddb_j, dtype=np.float64), casting="unsafe",
                       where=max(hm_ddb_j) != 0)
    for i in range(len(hm_ddb_j)):
        hm_ck_ddb_j_color.append("%.2f%%" % (arrayA[i] * 100))
    if hm_ddb_j[0] == 'nan%':
        a = 0
        for i in range(len(hm_ddb_j)):
            hm_ddb_j[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_dck_j, max(hm_dck_j), out=np.zeros_like(hm_dck_j, dtype=np.float64), casting="unsafe",
                       where=max(hm_dck_j) != 0)
    for i in range(len(hm_dck_j)):
        hm_ck_dck_j_color.append("%.2f%%" % (arrayA[i] * 100))
    if hm_dck_j[0] == 'nan%':
        a = 0
        for i in range(len(hm_dck_j)):
            hm_dck_j[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_djy_j, max(hm_djy_j), out=np.zeros_like(hm_djy_j, dtype=np.float64), casting="unsafe",
                       where=max(hm_djy_j) != 0)
    for i in range(len(hm_djy_j)):
        hm_ck_djy_j_color.append("%.2f%%" % (arrayA[i] * 100))
    if hm_djy_j[0] == 'nan%':
        a = 0
        for i in range(len(hm_djy_j)):
            hm_djy_j[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_dld_b, max(hm_dld_b), out=np.zeros_like(hm_dld_b, dtype=np.float64), casting="unsafe",
                       where=max(hm_dld_b) != 0)
    for i in range(len(hm_dld_b)):
        hm_ck_dld_b_color.append("%.2f%%" % (arrayA[i] * 100))
    if hm_dld_b[0] == 'nan%':
        a = 0
        for i in range(len(hm_dld_b)):
            hm_dld_b[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_djh_b, max(hm_djh_b), out=np.zeros_like(hm_djh_b, dtype=np.float64), casting="unsafe",
                       where=max(hm_djh_b) != 0)
    for i in range(len(hm_djh_b)):
        hm_ck_djh_b_color.append("%.2f%%" % (arrayA[i] * 100))
    if hm_djh_b[0] == 'nan%':
        a = 0
        for i in range(len(hm_djh_b)):
            hm_djh_b[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_ddb_b, max(hm_ddb_b), out=np.zeros_like(hm_ddb_b, dtype=np.float64), casting="unsafe",
                       where=max(hm_ddb_b) != 0)
    for i in range(len(hm_ddb_b)):
        hm_ck_ddb_b_color.append("%.2f%%" % (arrayA[i] * 100))
    if hm_ddb_b[0] == 'nan%':
        a = 0
        for i in range(len(hm_ddb_b)):
            hm_ddb_b[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_dck_b, max(hm_dck_b), out=np.zeros_like(hm_dck_b, dtype=np.float64), casting="unsafe",
                       where=max(hm_dck_b) != 0)
    for i in range(len(hm_dck_b)):
        hm_ck_dck_b_color.append("%.2f%%" % (arrayA[i] * 100))
    if hm_dck_b[0] == 'nan%':
        a = 0
        for i in range(len(hm_dck_b)):
            hm_dck_b[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_djy_b, max(hm_djy_b), out=np.zeros_like(hm_djy_b, dtype=np.float64), casting="unsafe",
                       where=max(hm_djy_b) != 0)
    for i in range(len(hm_djy_b)):
        hm_ck_djy_b_color.append("%.2f%%" % (arrayA[i] * 100))
    if hm_djy_b[0] == 'nan%':
        a = 0
        for i in range(len(hm_djy_b)):
            hm_djy_b[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_dld_j, max(tx_dld_j), out=np.zeros_like(tx_dld_j, dtype=np.float64), casting="unsafe",
                       where=max(tx_dld_j) != 0)
    for i in range(len(tx_dld_j)):
        tx_ck_dld_j_color.append("%.2f%%" % (arrayA[i] * 100))
    if tx_dld_j[0] == 'nan%':
        a = 0
        for i in range(len(tx_dld_j)):
            tx_dld_j[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_djh_j, max(tx_djh_j), out=np.zeros_like(tx_djh_j, dtype=np.float64), casting="unsafe",
                       where=max(tx_djh_j) != 0)
    for i in range(len(tx_djh_j)):
        tx_ck_djh_j_color.append("%.2f%%" % (arrayA[i] * 100))
    if tx_djh_j[0] == 'nan%':
        a = 0
        for i in range(len(tx_djh_j)):
            tx_djh_j[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_ddb_j, max(tx_ddb_j), out=np.zeros_like(tx_ddb_j, dtype=np.float64), casting="unsafe",
                       where=max(tx_ddb_j) != 0)
    for i in range(len(tx_ddb_j)):
        tx_ck_ddb_j_color.append("%.2f%%" % (arrayA[i] * 100))
    if tx_ddb_j[0] == 'nan%':
        a = 0
        for i in range(len(tx_ddb_j)):
            tx_ddb_j[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_dck_j, max(tx_dck_j), out=np.zeros_like(tx_dck_j, dtype=np.float64), casting="unsafe",
                       where=max(tx_dck_j) != 0)
    for i in range(len(tx_dck_j)):
        tx_ck_dck_j_color.append("%.2f%%" % (arrayA[i] * 100))
    if tx_dck_j[0] == 'nan%':
        a = 0
        for i in range(len(tx_dck_j)):
            tx_dck_j[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_djy_j, max(tx_djy_j), out=np.zeros_like(tx_djy_j, dtype=np.float64), casting="unsafe",
                       where=max(tx_djy_j) != 0)
    for i in range(len(tx_djy_j)):
        tx_ck_djy_j_color.append("%.2f%%" % (arrayA[i] * 100))
    if tx_djy_j[0] == 'nan%':
        a = 0
        for i in range(len(tx_djy_j)):
            tx_djy_j[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_dld_b, max(tx_dld_b), out=np.zeros_like(tx_dld_b, dtype=np.float64), casting="unsafe",
                       where=max(tx_dld_b) != 0)
    for i in range(len(tx_dld_b)):
        tx_ck_dld_b_color.append("%.2f%%" % (arrayA[i] * 100))
    if tx_dld_b[0] == 'nan%':
        a = 0
        for i in range(len(tx_dld_b)):
            tx_dld_b[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_djh_b, max(tx_djh_b), out=np.zeros_like(tx_djh_b, dtype=np.float64), casting="unsafe",
                       where=max(tx_djh_b) != 0)
    for i in range(len(tx_djh_b)):
        tx_ck_djh_b_color.append("%.2f%%" % (arrayA[i] * 100))
    if tx_djh_b[0] == 'nan%':
        a = 0
        for i in range(len(tx_djh_b)):
            tx_djh_b[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_ddb_b, max(tx_ddb_b), out=np.zeros_like(tx_ddb_b, dtype=np.float64), casting="unsafe",
                       where=max(tx_ddb_b) != 0)
    for i in range(len(tx_ddb_b)):
        tx_ck_ddb_b_color.append("%.2f%%" % (arrayA[i] * 100))
    if tx_ddb_b[0] == 'nan%':
        a = 0
        for i in range(len(tx_ddb_b)):
            tx_ddb_b[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_dck_b, max(tx_dck_b), out=np.zeros_like(tx_dck_b, dtype=np.float64), casting="unsafe",
                       where=max(tx_dck_b) != 0)
    for i in range(len(tx_dck_b)):
        tx_ck_dck_b_color.append("%.2f%%" % (arrayA[i] * 100))
    if tx_dck_b[0] == 'nan%':
        a = 0
        for i in range(len(tx_dck_b)):
            tx_dck_b[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_djy_b, max(tx_djy_b), out=np.zeros_like(tx_djy_b, dtype=np.float64), casting="unsafe",
                       where=max(tx_djy_b) != 0)
    for i in range(len(tx_djy_b)):
        tx_ck_djy_b_color.append("%.2f%%" % (arrayA[i] * 100))
    if tx_djy_b[0] == 'nan%':
        a = 0
        for i in range(len(tx_djy_b)):
            tx_djy_b[i] = '{:.2%}'.format(a)

    jsonData['hm_dld_j'] = hm_dld_j
    jsonData['hm_dld_b'] = hm_dld_b
    jsonData['hm_djh_j'] = hm_djh_j
    jsonData['hm_djh_b'] = hm_djh_b
    jsonData['hm_ddb_j'] = hm_ddb_j
    jsonData['hm_ddb_b'] = hm_ddb_b
    jsonData['hm_dck_j'] = hm_dck_j
    jsonData['hm_dck_b'] = hm_dck_b
    jsonData['hm_djy_j'] = hm_djy_j
    jsonData['hm_djy_b'] = hm_djy_b
    jsonData['tx_dld_j'] = tx_dld_j
    jsonData['tx_dld_b'] = tx_dld_b
    jsonData['tx_djh_j'] = tx_djh_j
    jsonData['tx_djh_b'] = tx_djh_b
    jsonData['tx_ddb_j'] = tx_ddb_j
    jsonData['tx_ddb_b'] = tx_ddb_b
    jsonData['tx_dck_j'] = tx_dck_j
    jsonData['tx_dck_b'] = tx_dck_b
    jsonData['tx_djy_j'] = tx_djy_j
    jsonData['tx_djy_b'] = tx_djy_b
    jsonData['hm_ck_dld_j_color'] = hm_ck_dld_j_color
    jsonData['hm_ck_djh_j_color'] = hm_ck_djh_j_color
    jsonData['hm_ck_ddb_j_color'] = hm_ck_ddb_j_color
    jsonData['hm_ck_dck_j_color'] = hm_ck_dck_j_color
    jsonData['hm_ck_djy_j_color'] = hm_ck_djy_j_color
    jsonData['hm_ck_dld_b_color'] = hm_ck_dld_b_color
    jsonData['hm_ck_djh_b_color'] = hm_ck_djh_b_color
    jsonData['hm_ck_ddb_b_color'] = hm_ck_ddb_b_color
    jsonData['hm_ck_dck_b_color'] = hm_ck_dck_b_color
    jsonData['hm_ck_djy_b_color'] = hm_ck_djy_b_color
    jsonData['tx_ck_dld_j_color'] = tx_ck_dld_j_color
    jsonData['tx_ck_djh_j_color'] = tx_ck_djh_j_color
    jsonData['tx_ck_ddb_j_color'] = tx_ck_ddb_j_color
    jsonData['tx_ck_dck_j_color'] = tx_ck_dck_j_color
    jsonData['tx_ck_djy_j_color'] = tx_ck_djy_j_color
    jsonData['tx_ck_dld_b_color'] = tx_ck_dld_b_color
    jsonData['tx_ck_djh_b_color'] = tx_ck_djh_b_color
    jsonData['tx_ck_ddb_b_color'] = tx_ck_ddb_b_color
    jsonData['tx_ck_dck_b_color'] = tx_ck_dck_b_color
    jsonData['tx_ck_djy_b_color'] = tx_ck_djy_b_color

    hm_order_id = []
    hm_status = []
    hm_num = []
    hm_s = []
    tx_order_id = []
    tx_status = []
    tx_num = []
    tx_s = []
    for i in range(len(warehouse)):
        if warehouse[i] == 'HM_AA':
            hm_order_id.append(order_id[i])
            hm_status.append(status[i])
            hm_num.append(num[i])
            hm_s.append(s[i])
    for i in range(len(warehouse)):
        if warehouse[i] == 'SZ_AA':
            tx_order_id.append(order_id[i])
            tx_status.append(status[i])
            tx_num.append(num[i])
            tx_s.append(s[i])
    print(tx_s)
    hm_data = np.dstack((hm_order_id, hm_status, hm_num, hm_s))
    tx_data = np.dstack((tx_order_id, tx_status, tx_num, tx_s))
    hm_drk_order = []
    hm_drk_s = []
    hm_rkz_s = []
    hm_drk_num = []
    hm_rkz_num = []
    tx_drk_s = []
    tx_rkz_s = []
    tx_drk_num = []
    tx_rkz_num = []
    for i in range(len(hm_data[0])):
        if (hm_data[0][i][1] == 1):
            hm_drk_num.append(hm_data[0][i][2])
            hm_drk_s.append(hm_data[0][i][3])
            hm_drk_order.append(hm_data[0][i][0])
    for i in range(len(hm_data[0])):
        if (hm_data[0][i][1] == 2):
            hm_rkz_num.append(hm_data[0][i][2])
            hm_rkz_s.append(hm_data[0][i][3])
    for i in range(len(tx_data[0])):
        if (tx_data[0][i][1] == 1):
            tx_drk_num.append(tx_data[0][i][2])
            tx_drk_s.append(tx_data[0][i][3])
    for i in range(len(tx_data[0])):
        if (tx_data[0][i][1] == 2):
            tx_rkz_num.append(tx_data[0][i][2])
            tx_rkz_s.append(tx_data[0][i][3])
    # 去重
    a1 = []
    a2 = []
    hm_drk_order = []
    hm_drk_s2 = []

    for i in range(len(hm_data[0])):
        if hm_data[0][i][0] not in a2 and hm_data[0][i][1] == 1:
            a1.append(hm_data[0][i])
        a2.append(hm_data[0][i][0])
    for i in range(len(a1)):
        hm_drk_order.append(a1[i][0])
        hm_drk_s2.append(a1[i][3])
    # print(hm_drk_order)

    a1 = []
    a2 = []
    hm_rkz_order = []
    hm_rkz_s2 = []
    for i in range(len(hm_data[0])):
        if hm_data[0][i][0] not in a2 and hm_data[0][i][1] == 2:
            a1.append(hm_data[0][i])
        a2.append(hm_data[0][i][0])
    for i in range(len(a1)):
        hm_rkz_order.append(a1[i][0])
        hm_rkz_s2.append(a1[i][3])
    # 去重
    a1 = []
    a2 = []
    tx_drk_order = []
    tx_drk_s2 = []
    for i in range(len(tx_data[0])):
        if tx_data[0][i][0] not in a2 and tx_data[0][i][1] == 1:
            a1.append(tx_data[0][i])
        a2.append(tx_data[0][i][0])
    for i in range(len(a1)):
        tx_drk_order.append(a1[i][0])
        tx_drk_s2.append(a1[i][3])
    a1 = []
    a2 = []
    tx_rkz_order = []
    tx_rkz_s2 = []
    for i in range(len(tx_data[0])):
        if tx_data[0][i][0] not in a2 and tx_data[0][i][1] == 2:
            a1.append(tx_data[0][i])
        a2.append(tx_data[0][i][0])
    for i in range(len(a1)):
        tx_rkz_order.append(a1[i][0])
        tx_rkz_s2.append(a1[i][3])
    hm_drk = np.dstack((hm_drk_num, hm_drk_s))
    hm_drk2 = np.dstack((hm_drk_order, hm_drk_s2))
    hm_rkz = np.dstack((hm_rkz_num, hm_rkz_s))
    hm_rkz2 = np.dstack((hm_rkz_order, hm_rkz_s2))
    tx_drk = np.dstack((tx_drk_num, tx_drk_s))
    tx_rkz = np.dstack((tx_rkz_num, tx_rkz_s))
    tx_drk2 = np.dstack((tx_drk_order, tx_drk_s2))
    tx_rkz2 = np.dstack((tx_rkz_order, tx_rkz_s2))
    hm_drk_b = [0, 0, 0, 0, 0, 0, 0]
    hm_drk_j = [0, 0, 0, 0, 0, 0, 0]
    hm_rkz_b = [0, 0, 0, 0, 0, 0, 0]
    hm_rkz_j = [0, 0, 0, 0, 0, 0, 0]
    tx_drk_b = [0, 0, 0, 0, 0, 0, 0]
    tx_drk_j = [0, 0, 0, 0, 0, 0, 0]
    tx_rkz_b = [0, 0, 0, 0, 0, 0, 0]
    tx_rkz_j = [0, 0, 0, 0, 0, 0, 0]

    for i in range(len(hm_drk[0])):
        if float(hm_drk_s[i]) > 0 and float(hm_drk_s[i]) <= 12:
            hm_drk_j[0] = hm_drk_j[0] + hm_drk[0][i][0]
        if float(hm_drk_s[i]) > 12 and float(hm_drk_s[i]) <= 24:
            hm_drk_j[1] = hm_drk_j[1] + hm_drk[0][i][0]
        if float(hm_drk_s[i]) > 24 and float(hm_drk_s[i]) <= 168:
            hm_drk_j[2] = hm_drk_j[2] + hm_drk[0][i][0]
        if float(hm_drk_s[i]) > 168 and float(hm_drk_s[i]) <= 360:
            hm_drk_j[3] = hm_drk_j[3] + hm_drk[0][i][0]
        if float(hm_drk_s[i]) > 360 and float(hm_drk_s[i]) <= 720:
            hm_drk_j[4] = hm_drk_j[4] + hm_drk[0][i][0]
        if float(hm_drk_s[i]) > 720:
            hm_drk_j[5] = hm_drk_j[5] + hm_drk[0][i][0]
        hm_drk_j[6] = hm_drk_j[6] + hm_drk[0][i][0]
    for i in range(len(hm_drk2[0])):
        if float(hm_drk_s2[i]) > 0 and float(hm_drk_s2[i]) <= 12:
            hm_drk_b[0] = hm_drk_b[0] + 1
        if float(hm_drk_s2[i]) > 12 and float(hm_drk_s2[i]) <= 24:
            hm_drk_b[1] = hm_drk_b[1] + 1
        if float(hm_drk_s2[i]) > 24 and float(hm_drk_s2[i]) <= 168:
            hm_drk_b[2] = hm_drk_b[2] + 1
        if float(hm_drk_s2[i]) > 168 and float(hm_drk_s2[i]) <= 360:
            hm_drk_b[3] = hm_drk_b[3] + 1
        if float(hm_drk_s2[i]) > 360 and float(hm_drk_s2[i]) <= 720:
            hm_drk_b[4] = hm_drk_b[4] + 1
        if float(hm_drk_s2[i]) > 720:
            hm_drk_b[5] = hm_drk_b[5] + 1
        hm_drk_b[6] = hm_drk_b[6] + 1
    for i in range(len(hm_rkz[0])):
        if float(hm_rkz_s[i]) > 0 and float(hm_rkz_s[i]) <= 12:
            hm_rkz_j[0] = hm_rkz_j[0] + hm_rkz[0][i][0]
        if float(hm_rkz_s[i]) > 12 and float(hm_rkz_s[i]) <= 24:
            hm_rkz_j[1] = hm_rkz_j[1] + hm_rkz[0][i][0]
        if float(hm_rkz_s[i]) > 24 and float(hm_rkz_s[i]) <= 168:
            hm_rkz_j[2] = hm_rkz_j[2] + hm_rkz[0][i][0]
        if float(hm_rkz_s[i]) > 168 and float(hm_rkz_s[i]) <= 360:
            hm_rkz_j[3] = hm_rkz_j[3] + hm_rkz[0][i][0]
        if float(hm_rkz_s[i]) > 360 and float(hm_rkz_s[i]) <= 720:
            hm_rkz_j[4] = hm_rkz_j[4] + hm_rkz[0][i][0]
        if float(hm_rkz_s[i]) > 720:
            hm_rkz_j[5] = hm_rkz_j[5] + hm_rkz[0][i][0]
        hm_rkz_j[6] = hm_rkz_j[6] + hm_rkz[0][i][0]

    for i in range(len(hm_rkz2[0])):
        if float(hm_rkz_s2[i]) > 0 and float(hm_rkz_s2[i]) <= 12:
            hm_rkz_b[0] = hm_rkz_b[0] + 1
        if float(hm_rkz_s2[i]) > 12 and float(hm_rkz_s2[i]) <= 24:
            hm_rkz_b[1] = hm_rkz_b[1] + 1
        if float(hm_rkz_s2[i]) > 24 and float(hm_rkz_s2[i]) <= 168:
            hm_rkz_b[2] = hm_rkz_b[2] + 1
        if float(hm_rkz_s2[i]) > 168 and float(hm_rkz_s2[i]) <= 360:
            hm_rkz_b[3] = hm_rkz_b[3] + 1
        if float(hm_rkz_s2[i]) > 360 and float(hm_rkz_s2[i]) <= 720:
            hm_rkz_b[4] = hm_rkz_b[4] + 1
        if float(hm_rkz_s2[i]) > 720:
            hm_rkz_b[5] = hm_rkz_b[5] + 1
        hm_rkz_b[6] = hm_rkz_b[6] + 1
    for i in range(len(tx_drk[0])):
        if float(tx_drk_s[i]) > 0 and float(tx_drk_s[i]) <= 12:
            tx_drk_j[0] = tx_drk_j[0] + tx_drk[0][i][0]
        if float(tx_drk_s[i]) > 12 and float(tx_drk_s[i]) <= 24:
            tx_drk_j[1] = tx_drk_j[1] + tx_drk[0][i][0]
        if float(tx_drk_s[i]) > 24 and float(tx_drk_s[i]) <= 168:
            tx_drk_j[2] = tx_drk_j[2] + tx_drk[0][i][0]
        if float(tx_drk_s[i]) > 168 and float(tx_drk_s[i]) <= 360:
            tx_drk_j[3] = tx_drk_j[3] + tx_drk[0][i][0]
        if float(tx_drk_s[i]) > 360 and float(tx_drk_s[i]) <= 720:
            tx_drk_j[4] = tx_drk_j[4] + tx_drk[0][i][0]
        if float(tx_drk_s[i]) > 720:
            tx_drk_j[5] = tx_drk_j[5] + tx_drk[0][i][0]
        tx_drk_j[6] = tx_drk_j[6] + tx_drk[0][i][0]
    for i in range(len(tx_drk2[0])):
        if float(tx_drk_s2[i]) > 0 and float(tx_drk_s2[i]) <= 12:
            tx_drk_b[0] = tx_drk_b[0] + 1
        if float(tx_drk_s2[i]) > 12 and float(tx_drk_s2[i]) <= 24:
            tx_drk_b[1] = tx_drk_b[1] + 1
        if float(tx_drk_s2[i]) > 24 and float(tx_drk_s2[i]) <= 168:
            tx_drk_b[2] = tx_drk_b[2] + 1
        if float(tx_drk_s2[i]) > 168 and float(tx_drk_s2[i]) <= 360:
            tx_drk_b[3] = tx_drk_b[3] + 1
        if float(tx_drk_s2[i]) > 360 and float(tx_drk_s2[i]) <= 720:
            tx_drk_b[4] = tx_drk_b[4] + 1
        if float(tx_drk_s2[i]) > 720:
            tx_drk_b[5] = tx_drk_b[5] + 1
        tx_drk_b[6] = tx_drk_b[6] + 1
    for i in range(len(tx_rkz[0])):
        if float(tx_rkz_s[i]) > 0 and float(tx_rkz_s[i]) <= 12:
            tx_rkz_j[0] = tx_rkz_j[0] + tx_rkz[0][i][0]
        if float(tx_rkz_s[i]) > 12 and float(tx_rkz_s[i]) <= 24:
            tx_rkz_j[1] = tx_rkz_j[1] + tx_rkz[0][i][0]
        if float(tx_rkz_s[i]) > 24 and float(tx_rkz_s[i]) <= 168:
            tx_rkz_j[2] = tx_rkz_j[2] + tx_rkz[0][i][0]
        if float(tx_rkz_s[i]) > 168 and float(tx_rkz_s[i]) <= 360:
            tx_rkz_j[3] = tx_rkz_j[3] + tx_rkz[0][i][0]
        if float(tx_rkz_s[i]) > 360 and float(tx_rkz_s[i]) <= 720:
            tx_rkz_j[4] = tx_rkz_j[4] + tx_rkz[0][i][0]
        if float(tx_rkz_s[i]) > 720:
            tx_rkz_j[5] = tx_rkz_j[5] + tx_rkz[0][i][0]
        tx_rkz_j[6] = tx_rkz_j[6] + tx_rkz[0][i][0]
    for i in range(len(tx_rkz2[0])):
        if float(tx_rkz_s2[i]) > 0 and float(tx_rkz_s2[i]) <= 12:
            tx_rkz_b[0] = tx_rkz_b[0] + 1
        if float(tx_rkz_s2[i]) > 12 and float(tx_rkz_s2[i]) <= 24:
            tx_rkz_b[1] = tx_rkz_b[1] + 1
        if float(tx_rkz_s2[i]) > 24 and float(tx_rkz_s2[i]) <= 168:
            tx_rkz_b[2] = tx_rkz_b[2] + 1
        if float(tx_rkz_s2[i]) > 168 and float(tx_rkz_s2[i]) <= 360:
            tx_rkz_b[3] = tx_rkz_b[3] + 1
        if float(tx_rkz_s2[i]) > 360 and float(tx_rkz_s2[i]) <= 720:
            tx_rkz_b[4] = tx_rkz_b[4] + 1
        if float(tx_rkz_s2[i]) > 720:
            tx_rkz_b[5] = tx_rkz_b[5] + 1
        tx_rkz_b[6] = tx_rkz_b[6] + 1
    hm_drk_b_color = []
    hm_drk_j_color = []
    hm_rkz_b_color = []
    hm_rkz_j_color = []
    tx_drk_b_color = []
    tx_drk_j_color = []
    tx_rkz_b_color = []
    tx_rkz_j_color = []

    arrayA = np.divide(hm_drk_b, max(hm_drk_b), out=np.zeros_like(hm_drk_b, dtype=np.float64),
                       where=max(hm_drk_b) != 0)
    for i in range(len(hm_drk_b)):
        hm_drk_b_color.append("%.2f%%" % (arrayA[i] * 100))
    if hm_drk_b[0] == 'nan%':
        a = 0
        for i in range(len(hm_drk_b)):
            hm_drk_b[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_drk_j, max(hm_drk_j), out=np.zeros_like(hm_drk_j, dtype=np.float64),
                       where=max(hm_drk_j) != 0,casting="unsafe")
    for i in range(len(hm_drk_j)):
        hm_drk_j_color.append("%.2f%%" % (arrayA[i] * 100))
    if hm_drk_j[0] == 'nan%':
        a = 0
        for i in range(len(hm_drk_j)):
            hm_drk_j[i] = '{:.2%}'.format(a)
    print(hm_drk_j_color)
    arrayA = np.divide(hm_rkz_b, max(hm_rkz_b), out=np.zeros_like(hm_rkz_b, dtype=np.float64),
                       where=max(hm_rkz_b) != 0)
    for i in range(len(hm_rkz_b)):
        hm_rkz_b_color.append("%.2f%%" % (arrayA[i] * 100))
    if hm_rkz_b[0] == 'nan%':
        a = 0
        for i in range(len(hm_rkz_b)):
            hm_rkz_b[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_rkz_j, max(hm_rkz_j), out=np.zeros_like(hm_rkz_j, dtype=np.float64),
                       where=max(hm_rkz_j) != 0 ,casting="unsafe")
    for i in range(len(hm_rkz_j)):
        hm_rkz_j_color.append("%.2f%%" % (arrayA[i] * 100))
    if hm_rkz_j[0] == 'nan%':
        a = 0
        for i in range(len(hm_rkz_j)):
            hm_rkz_j[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_drk_b, max(tx_drk_b), out=np.zeros_like(tx_drk_b, dtype=np.float64),
                       where=max(tx_drk_b) != 0)
    for i in range(len(tx_drk_b)):
        tx_drk_b_color.append("%.2f%%" % (arrayA[i] * 100))
    if tx_drk_b[0] == 'nan%':
        a = 0
        for i in range(len(tx_drk_b)):
            tx_drk_b[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_drk_j, max(tx_drk_j), out=np.zeros_like(tx_drk_j, dtype=np.float64),
                       where=max(tx_drk_j) != 0,casting="unsafe")
    for i in range(len(tx_drk_j)):
        tx_drk_j_color.append("%.2f%%" % (arrayA[i] * 100))
    if tx_drk_j[0] == 'nan%':
        a = 0
        for i in range(len(tx_drk_j)):
            tx_drk_j[i] = '{:.2%}'.format(a)

    arrayA = np.divide(tx_rkz_b, max(tx_rkz_b), out=np.zeros_like(tx_rkz_b, dtype=np.float64),
                       where=max(tx_rkz_b) != 0)
    for i in range(len(tx_rkz_b)):
        tx_rkz_b_color.append("%.2f%%" % (arrayA[i] * 100))
    if tx_rkz_b[0] == 'nan%':
        a = 0
        for i in range(len(tx_rkz_b)):
            tx_rkz_b[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_rkz_j, max(tx_rkz_j), out=np.zeros_like(tx_rkz_j, dtype=np.float64),
                       where=max(tx_rkz_j) != 0,casting="unsafe")
    for i in range(len(tx_rkz_j)):
        tx_rkz_j_color.append("%.2f%%" % (arrayA[i] * 100))
    if tx_rkz_j[0] == 'nan%':
        a = 0
        for i in range(len(tx_rkz_j)):
            tx_rkz_j[i] = '{:.2%}'.format(a)
    # 看这里
    arrayA = np.divide(tx_rkz_b, max(tx_rkz_b), out=np.zeros_like(tx_rkz_b, dtype=np.float64), where=max(tx_rkz_b) != 0)
    for i in range(len(tx_rkz_b)):
        tx_rkz_b_color.append("%.2f%%" % (arrayA[i] * 100))
    if tx_rkz_b[0] == 'nan%':
        a = 0
        for i in range(len(tx_rkz_b)):
            tx_rkz_b[i] = '{:.2%}'.format(a)

    arrayA = np.divide(tx_rkz_j, max(tx_rkz_j),casting="unsafe", out=np.zeros_like(tx_rkz_j, dtype=np.float64), where=max(tx_rkz_j) != 0)
    for i in range(len(tx_rkz_j)):
        tx_rkz_j_color.append("%.2f%%" % (arrayA[i] * 100))
    if tx_rkz_j[0] == 'nan%':
        a = 0
        for i in range(len(tx_rkz_j)):
            tx_rkz_j[i] = '{:.2%}'.format(a)

    jsonData['hm_drk_j'] = hm_drk_j
    jsonData['hm_drk_b'] = hm_drk_b
    jsonData['tx_drk_j'] = tx_drk_j
    jsonData['tx_drk_b'] = tx_drk_b
    jsonData['hm_rkz_j'] = hm_rkz_j
    jsonData['hm_rkz_b'] = hm_rkz_b
    jsonData['tx_rkz_j'] = tx_rkz_j
    jsonData['tx_rkz_b'] = tx_rkz_b
    jsonData['hm_drk_b_color'] = hm_drk_b_color
    jsonData['hm_drk_j_color'] = hm_drk_j_color
    jsonData['hm_rkz_b_color'] = hm_rkz_b_color
    jsonData['hm_rkz_j_color'] = hm_rkz_j_color
    jsonData['tx_drk_b_color'] = tx_drk_b_color
    jsonData['tx_drk_j_color'] = tx_drk_j_color
    jsonData['tx_rkz_b_color'] = tx_rkz_b_color
    jsonData['tx_rkz_j_color'] = tx_rkz_j_color
    jsonData['hm_drk_order'] = hm_drk_order
    jsonData['tx_drk_order'] = tx_drk_order
    jsonData['hm_drk_s2'] = hm_drk_s2
    jsonData['tx_drk_s2'] = tx_drk_s2
    jsonData['hm_ck_dld_order'] = hm_ck_dld_order
    jsonData['hm_ck_dld_s'] = hm_ck_dld_s
    jsonData['hm_ck_djh_order'] = hm_ck_djh_order
    jsonData['hm_ck_djh_s'] = hm_ck_djh_s
    jsonData['hm_ck_ddb_order'] = hm_ck_ddb_order
    jsonData['hm_ck_ddb_s'] = hm_ck_ddb_s
    jsonData['hm_ck_dck_order'] = hm_ck_dck_order
    jsonData['hm_ck_dck_s'] = hm_ck_dck_s
    jsonData['tx_ck_dld_order'] = tx_ck_dld_order
    jsonData['tx_ck_dld_s'] = tx_ck_dld_s
    jsonData['tx_ck_djh_order'] = tx_ck_djh_order
    jsonData['tx_ck_djh_s'] = tx_ck_djh_s
    jsonData['tx_ck_ddb_order'] = tx_ck_ddb_order
    jsonData['tx_ck_ddb_s'] = tx_ck_ddb_s
    jsonData['tx_ck_dck_order'] = tx_ck_dck_order
    jsonData['tx_ck_dck_s'] = tx_ck_dck_s
    # print(tx_drk_s2)
    j = json.dumps(jsonData, cls=DecimalEncoder)
    return (j)


@app.route('/daily3', methods=['POST'])
def montor_daily():
    # sql_updata='UPDATE ueb_warehouse_shelf_sku_map  SET shelf_type = 99 WHERE shelf LIKE "%BGA%";'
    #sql = 'SELECT	warehouse_code,	purchase_order_no,	storage_position,	sku,	actual_num,	CASE		WHEN post_code_start_time IS NOT NULL 		AND post_code_end_time IS NOT NULL 		AND quality_time IS NOT NULL 		AND upper_start_time IS NOT NULL 		AND upper_end_time IS NULL THEN			"SJZ" 			WHEN post_code_start_time IS NOT NULL 			AND post_code_end_time IS NOT NULL 			AND quality_time IS NOT NULL 			AND paragraph != 11 			AND upper_start_time IS NULL THEN				"DSJ" 				WHEN post_code_start_time IS NOT NULL 				AND post_code_end_time IS NOT NULL 				AND quality_time IS NOT NULL 				AND paragraph = 11 				AND upper_start_time IS NULL THEN					"DGNZJ" 					WHEN post_code_start_time IS NULL THEN					"DTM" ELSE "else" 				END AS type,				cast(ROUND( ( unix_timestamp( now()) - unix_timestamp( quality_start_time ) ) / 3600, 2 ) as DECIMAL  ) AS s 			FROM				ueb_quality_warehousing_record 			WHERE				paragraph != 5 				AND purchase_order_no NOT LIKE "ABD%" 				AND warehouse_code IN ( "HM_AA", "SZ_AA" ) 			GROUP BY				purchase_order_no,				sku,				warehouse_code UNION			SELECT				warehouse_code,				"RK" AS purchase_order_no,				car_no AS storage_position,				"RK" AS sku,				box_number AS quality_num,				"DRK" AS type,				cast(ROUND( ( unix_timestamp( now()) - unix_timestamp( add_time ) ) / 3600, 2 ) as DECIMAL   )AS s 			FROM				ueb_express_receipt 			WHERE				STATUS = 1 				AND warehouse_type = 1 				AND is_abnormal = "2" 			AND is_quality = "2" 	AND is_end = "1"'
    #sql_fba = 'select * from (select warehouse_code,order_id,case when pay_time >0 and wait_pull_time >0 and pick_time >0 and  pack_time >0 and outstock_time > 0 and delivery_time = 0  then "DJY"when pay_time >0 and wait_pull_time >0 and pick_time >0 and ((choice_time =0 and pack_time>0) or (choice_time >0 and pack_time >0)) and outstock_time = 0  then "DCK"when pay_time >0 and wait_pull_time >0 and pick_time >0 and pack_time = 0  then "DDB"when pay_time >0 and wait_pull_time >0 and pick_time =0  then "DJH"when pay_time >0 and wait_pull_time =0  then "DLD"ELSE "else" end as `status`,CAST(order_product_number AS SIGNED) as `order_product_number`,ROUND(( unix_timestamp(now()) - greatest(pay_time,wait_pull_time,pick_time,choice_time,pack_time) ) / 3600, 2 ) AS time from ueb_order_operate_time where order_is_cancel =0 and delivery_time = 0 and order_id like "FB%"  union    select warehouse_code,order_id,case when wh_order_status=-1 then "DPK" when wh_order_status in (1)then  "DFPLD" when wh_order_status in (2)then  "DLD" else "else" end  as `status`,CAST(sum(order_product_number) AS SIGNED) as `order_product_number`,case  when wh_order_status=-1 then ROUND(( unix_timestamp(now()) - paytime_int) / 3600, 2 )  when wh_order_status in (1,2) then     ROUND(( unix_timestamp(now()) - wait_pull_time) / 3600, 2 ) else "else" end  AS time       from ueb_order where order_id like "FB%" and wh_order_status in(-1,1,2)  group by warehouse_code,order_id) a  order by time  DESC'
    #sql_xb = 'select * from (select warehouse_code,order_id,case when pay_time >0 and wait_pull_time >0 and pick_time >0 and  pack_time >0 and outstock_time > 0 and delivery_time = 0  then "DJY"when pay_time >0 and wait_pull_time >0 and pick_time >0 and ((choice_time =0 and pack_time>0) or (choice_time >0 and pack_time >0)) and outstock_time = 0  then "DCK"when pay_time >0 and wait_pull_time >0 and pick_time >0 and pack_time = 0  then "DDB"when pay_time >0 and wait_pull_time >0 and pick_time =0  then "DJH"when pay_time >0 and wait_pull_time =0  then "DLD"ELSE "else" end as `status`,CAST(order_product_number AS SIGNED) as `order_product_number`,ROUND(( unix_timestamp(now()) - greatest(pay_time,wait_pull_time,pick_time,choice_time,pack_time) ) / 3600, 2 ) AS time from ueb_order_operate_time where order_is_cancel =0 and delivery_time = 0 and 	 batch_no NOT LIKE "%-6-%"  union   select warehouse_code,order_id,case when wh_order_status=-1 then "DPK" when wh_order_status in (1)then  "DFPLD" when wh_order_status in (2)then  "DLD" else "else" end  as `status`,CAST(sum(order_product_number) AS SIGNED) as `order_product_number`,case  when wh_order_status=-1 then ROUND(( unix_timestamp(now()) - paytime_int) / 3600, 2 )  when wh_order_status in (1,2) then     ROUND(( unix_timestamp(now()) - wait_pull_time) / 3600, 2 ) else "else" end  AS time       from ueb_order  WHERE batch_type != 6 and wh_order_status < 9  group by warehouse_code,order_id) a  order by time  DESC'

    input = pd.read_excel('daily3_xb.xlsx')
    see_xb=save(input)
    input = pd.read_excel('daily3_fba.xlsx')
    see_fba=save(input)
    input = pd.read_excel('daily3_sql.xlsx')
    see=save(input)

    warehouse_xb = []
    type_xb = []
    order_xb = []
    num_xb = []
    s_xb = []
    for data_xb in see_xb:
        warehouse_xb.append(data_xb[0])
        type_xb.append(data_xb[2])
        order_xb.append(data_xb[1])
        num_xb.append(data_xb[3])
        s_xb.append(data_xb[4])
    print(num_xb)
    hm_type_xb = []
    hm_order_xb = []
    hm_num_xb = []
    hm_s_xb = []
    tx_type_xb = []
    tx_order_xb = []
    tx_num_xb = []
    tx_s_xb = []
    for i in range(len(warehouse_xb)):
        if warehouse_xb[i] == 'HM_AA':
            hm_type_xb.append(type_xb[i])
            hm_order_xb.append(order_xb[i])
            hm_num_xb.append(num_xb[i])
            hm_s_xb.append(s_xb[i])
    for i in range(len(warehouse_xb)):
        if warehouse_xb[i] == 'SZ_AA':
            tx_type_xb.append(type_xb[i])
            tx_order_xb.append(order_xb[i])
            tx_num_xb.append(num_xb[i])
            tx_s_xb.append(s_xb[i])
    hm_xb_data = np.dstack((hm_type_xb, hm_order_xb, hm_num_xb, hm_s_xb))
    tx_xb_data = np.dstack((tx_type_xb, tx_order_xb, tx_num_xb, tx_s_xb))
    hm_xb_djy_b_num = []
    hm_xb_djy_j_num = []
    hm_xb_djy_time = []
    hm_xb_dfpld_b_num = []
    hm_xb_dfpld_j_num = []
    hm_xb_dfpld_time = []
    hm_xb_dpk_b_num = []
    hm_xb_dpk_j_num = []
    hm_xb_dpk_time = []
    hm_xb_dld_b_num = []
    hm_xb_dld_j_num = []
    hm_xb_dld_time = []
    hm_xb_djh_b_num = []
    hm_xb_djh_j_num = []
    hm_xb_djh_time = []
    hm_xb_ddb_b_num = []
    hm_xb_ddb_j_num = []
    hm_xb_ddb_time = []
    hm_xb_dck_b_num = []
    hm_xb_dck_j_num = []
    hm_xb_dck_time = []
    tx_xb_djy_b_num = []
    tx_xb_djy_j_num = []
    tx_xb_djy_time = []
    tx_xb_dfpld_b_num = []
    tx_xb_dfpld_j_num = []
    tx_xb_dfpld_time = []
    tx_xb_dpk_b_num = []
    tx_xb_dpk_j_num = []
    tx_xb_dpk_time = []
    tx_xb_dld_b_num = []
    tx_xb_dld_j_num = []
    tx_xb_dld_time = []
    tx_xb_djh_b_num = []
    tx_xb_djh_j_num = []
    tx_xb_djh_time = []
    tx_xb_ddb_b_num = []
    tx_xb_ddb_j_num = []
    tx_xb_ddb_time = []
    tx_xb_dck_b_num = []
    tx_xb_dck_j_num = []
    tx_xb_dck_time = []
    for i in range(len(hm_s_xb)):
        if (hm_xb_data[0][i][0] == 'DJY'):
            hm_xb_djy_b_num.append(1)
            hm_xb_djy_j_num.append(hm_xb_data[0][i][2])
            hm_xb_djy_time.append(hm_xb_data[0][i][3])
    for i in range(len(hm_s_xb)):
        if (hm_xb_data[0][i][0] == 'DFPLD'):
            hm_xb_dfpld_b_num.append(1)
            hm_xb_dfpld_j_num.append(hm_xb_data[0][i][2])
            hm_xb_dfpld_time.append(hm_xb_data[0][i][3])
    for i in range(len(hm_s_xb)):
        if (hm_xb_data[0][i][0] == 'DPK'):
            hm_xb_dpk_b_num.append(1)
            hm_xb_dpk_j_num.append(hm_xb_data[0][i][2])
            hm_xb_dpk_time.append(hm_xb_data[0][i][3])

    for i in range(len(hm_s_xb)):
        if (hm_xb_data[0][i][0] == 'DLD'):
            hm_xb_dld_b_num.append(1)
            hm_xb_dld_j_num.append(hm_xb_data[0][i][2])
            hm_xb_dld_time.append(hm_xb_data[0][i][3])
    for i in range(len(hm_s_xb)):
        if (hm_xb_data[0][i][0] == 'DJH'):
            hm_xb_djh_b_num.append(1)
            hm_xb_djh_j_num.append(hm_xb_data[0][i][2])
            hm_xb_djh_time.append(hm_xb_data[0][i][3])
    for i in range(len(hm_s_xb)):
        if (hm_xb_data[0][i][0] == 'DDB'):
            hm_xb_ddb_b_num.append(1)
            hm_xb_ddb_j_num.append(hm_xb_data[0][i][2])
            hm_xb_ddb_time.append(hm_xb_data[0][i][3])
    for i in range(len(hm_s_xb)):
        if (hm_xb_data[0][i][0] == 'DCK'):
            hm_xb_dck_b_num.append(1)
            hm_xb_dck_j_num.append(hm_xb_data[0][i][2])
            hm_xb_dck_time.append(hm_xb_data[0][i][3])
    for i in range(len(tx_s_xb)):
        if (tx_xb_data[0][i][0] == 'DJY'):
            tx_xb_djy_b_num.append(1)
            tx_xb_djy_j_num.append(tx_xb_data[0][i][2])
            tx_xb_djy_time.append(tx_xb_data[0][i][3])
    for i in range(len(tx_s_xb)):
        if (tx_xb_data[0][i][0] == 'DFPLD'):
            tx_xb_dfpld_b_num.append(1)
            tx_xb_dfpld_j_num.append(tx_xb_data[0][i][2])
            tx_xb_dfpld_time.append(tx_xb_data[0][i][3])
    for i in range(len(tx_s_xb)):
        if (tx_xb_data[0][i][0] == 'DPK'):
            tx_xb_dpk_b_num.append(1)
            tx_xb_dpk_j_num.append(tx_xb_data[0][i][2])
            tx_xb_dpk_time.append(tx_xb_data[0][i][3])
    for i in range(len(tx_s_xb)):
        if (tx_xb_data[0][i][0] == 'DLD'):
            tx_xb_dld_b_num.append(1)
            tx_xb_dld_j_num.append(tx_xb_data[0][i][2])
            tx_xb_dld_time.append(tx_xb_data[0][i][3])
    for i in range(len(tx_s_xb)):
        if (tx_xb_data[0][i][0] == 'DJH'):
            tx_xb_djh_b_num.append(1)
            tx_xb_djh_j_num.append(tx_xb_data[0][i][2])
            tx_xb_djh_time.append(tx_xb_data[0][i][3])
    for i in range(len(tx_s_xb)):
        if (tx_xb_data[0][i][0] == 'DDB'):
            tx_xb_ddb_b_num.append(1)
            tx_xb_ddb_j_num.append(tx_xb_data[0][i][2])
            tx_xb_ddb_time.append(tx_xb_data[0][i][3])
    for i in range(len(tx_s_xb)):
        if (tx_xb_data[0][i][0] == 'DCK'):
            tx_xb_dck_b_num.append(1)
            tx_xb_dck_j_num.append(tx_xb_data[0][i][2])
            tx_xb_dck_time.append(tx_xb_data[0][i][3])

    hm_xb_djy = np.dstack((hm_xb_djy_b_num, hm_xb_djy_j_num, hm_xb_djy_time))
    hm_xb_dfpld = np.dstack((hm_xb_dfpld_b_num, hm_xb_dfpld_j_num, hm_xb_dfpld_time))
    hm_xb_dpk = np.dstack((hm_xb_dpk_b_num, hm_xb_dpk_j_num, hm_xb_dpk_time))
    hm_xb_dld = np.dstack((hm_xb_dld_b_num, hm_xb_dld_j_num, hm_xb_dld_time))
    hm_xb_djh = np.dstack((hm_xb_djh_b_num, hm_xb_djh_j_num, hm_xb_djh_time))
    hm_xb_ddb = np.dstack((hm_xb_ddb_b_num, hm_xb_ddb_j_num, hm_xb_ddb_time))
    hm_xb_dck = np.dstack((hm_xb_dck_b_num, hm_xb_dck_j_num, hm_xb_dck_time))
    tx_xb_djy = np.dstack((tx_xb_djy_b_num, tx_xb_djy_j_num, tx_xb_djy_time))
    tx_xb_dfpld = np.dstack((tx_xb_dfpld_b_num, tx_xb_dfpld_j_num, tx_xb_dfpld_time))
    tx_xb_dpk = np.dstack((tx_xb_dpk_b_num, tx_xb_dpk_j_num, tx_xb_dpk_time))
    tx_xb_dld = np.dstack((tx_xb_dld_b_num, tx_xb_dld_j_num, tx_xb_dld_time))
    tx_xb_djh = np.dstack((tx_xb_djh_b_num, tx_xb_djh_j_num, tx_xb_djh_time))
    tx_xb_ddb = np.dstack((tx_xb_ddb_b_num, tx_xb_ddb_j_num, tx_xb_ddb_time))
    tx_xb_dck = np.dstack((tx_xb_dck_b_num, tx_xb_dck_j_num, tx_xb_dck_time))

    hm_xb_djy_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_xb_djy_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_xb_dfpld_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_xb_dfpld_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_xb_djy_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_xb_djy_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_xb_dfpld_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_xb_dfpld_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_xb_dpk_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_xb_dld_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_xb_djh_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_xb_ddb_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_xb_dck_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_xb_dpk_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_xb_dld_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_xb_djh_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_xb_ddb_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_xb_dck_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_xb_dpk_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_xb_dld_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_xb_djh_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_xb_ddb_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_xb_dck_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_xb_dpk_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_xb_dld_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_xb_djh_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_xb_ddb_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_xb_dck_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]

    hm_xb_b_2 = []
    hm_xb_b_4 = []
    hm_xb_b_6 = []
    hm_xb_b_8 = []
    hm_xb_b_10 = []
    hm_xb_b_12 = []
    hm_xb_b_24 = []
    hm_xb_b_24_ = []
    tx_xb_b_2 = []
    tx_xb_b_4 = []
    tx_xb_b_6 = []
    tx_xb_b_8 = []
    tx_xb_b_10 = []
    tx_xb_b_12 = []
    tx_xb_b_24 = []
    tx_xb_b_24_ = []
    # hm_j_12 = []
    # hm_j_24 = []
    # hm_j_48 = []
    # hm_j_72 = []
    # hm_j_120 = []
    # hm_j_240 = []
    # hm_j_360 = []
    # hm_j_361 = []
    #
    # tx_j_12 = []
    # tx_j_24 = []
    # tx_j_48 = []
    # tx_j_72 = []
    # tx_j_120 = []
    # tx_j_240 = []
    # tx_j_360 = []
    # tx_j_361 = []

    for i in range(len(hm_xb_djy[0])):
        if float(hm_xb_djy[0][i][2]) > 0 and float(hm_xb_djy[0][i][2]) <= 2:
            hm_xb_djy_b_num1[0] = hm_xb_djy_b_num1[0] + 1
            hm_xb_djy_j_num1[0] = hm_xb_djy_j_num1[0] + float(hm_xb_djy[0][i][1])
        if float(hm_xb_djy[0][i][2]) > 2 and float(hm_xb_djy[0][i][2]) <= 4:
            hm_xb_djy_b_num1[1] = hm_xb_djy_b_num1[1] + 1
            hm_xb_djy_j_num1[1] = hm_xb_djy_j_num1[1] + float(hm_xb_djy[0][i][1])
        if float(hm_xb_djy[0][i][2]) > 4 and float(hm_xb_djy[0][i][2]) <= 6:
            hm_xb_djy_b_num1[2] = hm_xb_djy_b_num1[2] + 1
            hm_xb_djy_j_num1[2] = hm_xb_djy_j_num1[2] + float(hm_xb_djy[0][i][1])
        if float(hm_xb_djy[0][i][2]) > 6 and float(hm_xb_djy[0][i][2]) <= 8:
            hm_xb_djy_b_num1[3] = hm_xb_djy_b_num1[3] + 1
            hm_xb_djy_j_num1[3] = hm_xb_djy_j_num1[3] + float(hm_xb_djy[0][i][1])
        if float(hm_xb_djy[0][i][2]) > 8 and float(hm_xb_djy[0][i][2]) <= 10:
            hm_xb_djy_b_num1[4] = hm_xb_djy_b_num1[4] + 1
            hm_xb_djy_j_num1[4] = hm_xb_djy_j_num1[4] + float(hm_xb_djy[0][i][1])
        if float(hm_xb_djy[0][i][2]) > 10 and float(hm_xb_djy[0][i][2]) <= 12:
            hm_xb_djy_b_num1[5] = hm_xb_djy_b_num1[5] + 1
            hm_xb_djy_j_num1[5] = hm_xb_djy_j_num1[5] + float(hm_xb_djy[0][i][1])
        if float(hm_xb_djy[0][i][2]) > 12 and float(hm_xb_djy[0][i][2]) <= 24:
            hm_xb_djy_b_num1[6] = hm_xb_djy_b_num1[6] + 1
            hm_xb_djy_j_num1[6] = hm_xb_djy_j_num1[6] + float(hm_xb_djy[0][i][1])
        if float(hm_xb_djy[0][i][2]) > 24:
            hm_xb_djy_b_num1[7] = hm_xb_djy_b_num1[7] + 1
            hm_xb_djy_j_num1[7] = hm_xb_djy_j_num1[7] + float(hm_xb_djy[0][i][1])

    for i in range(len(hm_xb_dfpld[0])):
        if float(hm_xb_dfpld[0][i][2]) > 0 and float(hm_xb_dfpld[0][i][2]) <= 2:
            hm_xb_dfpld_b_num1[0] = hm_xb_dfpld_b_num1[0] + 1
            hm_xb_dfpld_j_num1[0] = hm_xb_dfpld_j_num1[0] + float(hm_xb_dfpld[0][i][1])
        if float(hm_xb_dfpld[0][i][2]) > 2 and float(hm_xb_dfpld[0][i][2]) <= 4:
            hm_xb_dfpld_b_num1[1] = hm_xb_dfpld_b_num1[1] + 1
            hm_xb_dfpld_j_num1[1] = hm_xb_dfpld_j_num1[1] + float(hm_xb_dfpld[0][i][1])
        if float(hm_xb_dfpld[0][i][2]) > 4 and float(hm_xb_dfpld[0][i][2]) <= 6:
            hm_xb_dfpld_b_num1[2] = hm_xb_dfpld_b_num1[2] + 1
            hm_xb_dfpld_j_num1[2] = hm_xb_dfpld_j_num1[2] + float(hm_xb_dfpld[0][i][1])
        if float(hm_xb_dfpld[0][i][2]) > 6 and float(hm_xb_dfpld[0][i][2]) <= 8:
            hm_xb_dfpld_b_num1[3] = hm_xb_dfpld_b_num1[3] + 1
            hm_xb_dfpld_j_num1[3] = hm_xb_dfpld_j_num1[3] + float(hm_xb_dfpld[0][i][1])
        if float(hm_xb_dfpld[0][i][2]) > 8 and float(hm_xb_dfpld[0][i][2]) <= 10:
            hm_xb_dfpld_b_num1[4] = hm_xb_dfpld_b_num1[4] + 1
            hm_xb_dfpld_j_num1[4] = hm_xb_dfpld_j_num1[4] + float(hm_xb_dfpld[0][i][1])
        if float(hm_xb_dfpld[0][i][2]) > 10 and float(hm_xb_dfpld[0][i][2]) <= 12:
            hm_xb_dfpld_b_num1[5] = hm_xb_dfpld_b_num1[5] + 1
            hm_xb_dfpld_j_num1[5] = hm_xb_dfpld_j_num1[5] + float(hm_xb_dfpld[0][i][1])
        if float(hm_xb_dfpld[0][i][2]) > 12 and float(hm_xb_dfpld[0][i][2]) <= 24:
            hm_xb_dfpld_b_num1[6] = hm_xb_dfpld_b_num1[6] + 1
            hm_xb_dfpld_j_num1[6] = hm_xb_dfpld_j_num1[6] + float(hm_xb_dfpld[0][i][1])
        if float(hm_xb_dfpld[0][i][2]) > 24:
            hm_xb_dfpld_b_num1[7] = hm_xb_dfpld_b_num1[7] + 1
            hm_xb_dfpld_j_num1[7] = hm_xb_dfpld_j_num1[7] + float(hm_xb_dfpld[0][i][1])
    for i in range(len(hm_xb_dpk[0])):
        if float(hm_xb_dpk[0][i][2]) > 0 and float(hm_xb_dpk[0][i][2]) <= 2:
            hm_xb_dpk_b_num1[0] = hm_xb_dpk_b_num1[0] + 1
            hm_xb_dpk_j_num1[0] = hm_xb_dpk_j_num1[0] + float(hm_xb_dpk[0][i][1])
        if float(hm_xb_dpk[0][i][2]) > 2 and float(hm_xb_dpk[0][i][2]) <= 4:
            hm_xb_dpk_b_num1[1] = hm_xb_dpk_b_num1[1] + 1
            hm_xb_dpk_j_num1[1] = hm_xb_dpk_j_num1[1] + float(hm_xb_dpk[0][i][1])
        if float(hm_xb_dpk[0][i][2]) > 4 and float(hm_xb_dpk[0][i][2]) <= 6:
            hm_xb_dpk_b_num1[2] = hm_xb_dpk_b_num1[2] + 1
            hm_xb_dpk_j_num1[2] = hm_xb_dpk_j_num1[2] + float(hm_xb_dpk[0][i][1])
        if float(hm_xb_dpk[0][i][2]) > 6 and float(hm_xb_dpk[0][i][2]) <= 8:
            hm_xb_dpk_b_num1[3] = hm_xb_dpk_b_num1[3] + 1
            hm_xb_dpk_j_num1[3] = hm_xb_dpk_j_num1[3] + float(hm_xb_dpk[0][i][1])
        if float(hm_xb_dpk[0][i][2]) > 8 and float(hm_xb_dpk[0][i][2]) <= 10:
            hm_xb_dpk_b_num1[4] = hm_xb_dpk_b_num1[4] + 1
            hm_xb_dpk_j_num1[4] = hm_xb_dpk_j_num1[4] + float(hm_xb_dpk[0][i][1])
        if float(hm_xb_dpk[0][i][2]) > 10 and float(hm_xb_dpk[0][i][2]) <= 12:
            hm_xb_dpk_b_num1[5] = hm_xb_dpk_b_num1[5] + 1
            hm_xb_dpk_j_num1[5] = hm_xb_dpk_j_num1[5] + float(hm_xb_dpk[0][i][1])
        if float(hm_xb_dpk[0][i][2]) > 12 and float(hm_xb_dpk[0][i][2]) <= 24:
            hm_xb_dpk_b_num1[6] = hm_xb_dpk_b_num1[6] + 1
            hm_xb_dpk_j_num1[6] = hm_xb_dpk_j_num1[6] + float(hm_xb_dpk[0][i][1])
        if float(hm_xb_dpk[0][i][2]) > 24:
            hm_xb_dpk_b_num1[7] = hm_xb_dpk_b_num1[7] + 1
            hm_xb_dpk_j_num1[7] = hm_xb_dpk_j_num1[7] + float(hm_xb_dpk[0][i][1])
    for i in range(len(hm_xb_dld[0])):
        if float(hm_xb_dld[0][i][2]) > 0 and float(hm_xb_dld[0][i][2]) <= 2:
            hm_xb_dld_b_num1[0] = hm_xb_dld_b_num1[0] + 1
            hm_xb_dld_j_num1[0] = hm_xb_dld_j_num1[0] + float(hm_xb_dld[0][i][1])
        if float(hm_xb_dld[0][i][2]) > 2 and float(hm_xb_dld[0][i][2]) <= 4:
            hm_xb_dld_b_num1[1] = hm_xb_dld_b_num1[1] + 1
            hm_xb_dld_j_num1[1] = hm_xb_dld_j_num1[1] + float(hm_xb_dld[0][i][1])
        if float(hm_xb_dld[0][i][2]) > 4 and float(hm_xb_dld[0][i][2]) <= 6:
            hm_xb_dld_b_num1[2] = hm_xb_dld_b_num1[2] + 1
            hm_xb_dld_j_num1[2] = hm_xb_dld_j_num1[2] + float(hm_xb_dld[0][i][1])
        if float(hm_xb_dld[0][i][2]) > 6 and float(hm_xb_dld[0][i][2]) <= 8:
            hm_xb_dld_b_num1[3] = hm_xb_dld_b_num1[3] + 1
            hm_xb_dld_j_num1[3] = hm_xb_dld_j_num1[3] + float(hm_xb_dld[0][i][1])
        if float(hm_xb_dld[0][i][2]) > 8 and float(hm_xb_dld[0][i][2]) <= 10:
            hm_xb_dld_b_num1[4] = hm_xb_dld_b_num1[4] + 1
            hm_xb_dld_j_num1[4] = hm_xb_dld_j_num1[4] + float(hm_xb_dld[0][i][1])
        if float(hm_xb_dld[0][i][2]) > 10 and float(hm_xb_dld[0][i][2]) <= 12:
            hm_xb_dld_b_num1[5] = hm_xb_dld_b_num1[5] + 1
            hm_xb_dld_j_num1[5] = hm_xb_dld_j_num1[5] + float(hm_xb_dld[0][i][1])
        if float(hm_xb_dld[0][i][2]) > 12 and float(hm_xb_dld[0][i][2]) <= 24:
            hm_xb_dld_b_num1[6] = hm_xb_dld_b_num1[6] + 1
            hm_xb_dld_j_num1[6] = hm_xb_dld_j_num1[6] + float(hm_xb_dld[0][i][1])
        if float(hm_xb_dld[0][i][2]) > 24:
            hm_xb_dld_b_num1[7] = hm_xb_dld_b_num1[7] + 1
            hm_xb_dld_j_num1[7] = hm_xb_dld_j_num1[7] + float(hm_xb_dld[0][i][1])

    for i in range(len(hm_xb_djh[0])):
        if float(hm_xb_djh[0][i][2]) > 0 and float(hm_xb_djh[0][i][2]) <= 2:
            hm_xb_djh_b_num1[0] = hm_xb_djh_b_num1[0] + 1
            hm_xb_djh_j_num1[0] = hm_xb_djh_j_num1[0] + float(hm_xb_djh[0][i][1])
        if float(hm_xb_djh[0][i][2]) > 2 and float(hm_xb_djh[0][i][2]) <= 4:
            hm_xb_djh_b_num1[1] = hm_xb_djh_b_num1[1] + 1
            hm_xb_djh_j_num1[1] = hm_xb_djh_j_num1[1] + float(hm_xb_djh[0][i][1])
        if float(hm_xb_djh[0][i][2]) > 4 and float(hm_xb_djh[0][i][2]) <= 6:
            hm_xb_djh_b_num1[2] = hm_xb_djh_b_num1[2] + 1
            hm_xb_djh_j_num1[2] = hm_xb_djh_j_num1[2] + float(hm_xb_djh[0][i][1])
        if float(hm_xb_djh[0][i][2]) > 6 and float(hm_xb_djh[0][i][2]) <= 8:
            hm_xb_djh_b_num1[3] = hm_xb_djh_b_num1[3] + 1
            hm_xb_djh_j_num1[3] = hm_xb_djh_j_num1[3] + float(hm_xb_djh[0][i][1])
        if float(hm_xb_djh[0][i][2]) > 8 and float(hm_xb_djh[0][i][2]) <= 10:
            hm_xb_djh_b_num1[4] = hm_xb_djh_b_num1[4] + 1
            hm_xb_djh_j_num1[4] = hm_xb_djh_j_num1[4] + float(hm_xb_djh[0][i][1])
        if float(hm_xb_djh[0][i][2]) > 10 and float(hm_xb_djh[0][i][2]) <= 12:
            hm_xb_djh_b_num1[5] = hm_xb_djh_b_num1[5] + 1
            hm_xb_djh_j_num1[5] = hm_xb_djh_j_num1[5] + float(hm_xb_djh[0][i][1])
        if float(hm_xb_djh[0][i][2]) > 12 and float(hm_xb_djh[0][i][2]) <= 24:
            hm_xb_djh_b_num1[6] = hm_xb_djh_b_num1[6] + 1
            hm_xb_djh_j_num1[6] = hm_xb_djh_j_num1[6] + float(hm_xb_djh[0][i][1])
        if float(hm_xb_djh[0][i][2]) > 24:
            hm_xb_djh_b_num1[7] = hm_xb_djh_b_num1[7] + 1
            hm_xb_djh_j_num1[7] = hm_xb_djh_j_num1[7] + float(hm_xb_djh[0][i][1])

    for i in range(len(hm_xb_ddb[0])):
        if float(hm_xb_ddb[0][i][2]) > 0 and float(hm_xb_ddb[0][i][2]) <= 2:
            hm_xb_ddb_b_num1[0] = hm_xb_ddb_b_num1[0] + 1
            hm_xb_ddb_j_num1[0] = hm_xb_ddb_j_num1[0] + float(hm_xb_ddb[0][i][1])
        if float(hm_xb_ddb[0][i][2]) > 2 and float(hm_xb_ddb[0][i][2]) <= 4:
            hm_xb_ddb_b_num1[1] = hm_xb_ddb_b_num1[1] + 1
            hm_xb_ddb_j_num1[1] = hm_xb_ddb_j_num1[1] + float(hm_xb_ddb[0][i][1])
        if float(hm_xb_ddb[0][i][2]) > 4 and float(hm_xb_ddb[0][i][2]) <= 6:
            hm_xb_ddb_b_num1[2] = hm_xb_ddb_b_num1[2] + 1
            hm_xb_ddb_j_num1[2] = hm_xb_ddb_j_num1[2] + float(hm_xb_ddb[0][i][1])
        if float(hm_xb_ddb[0][i][2]) > 6 and float(hm_xb_ddb[0][i][2]) <= 8:
            hm_xb_ddb_b_num1[3] = hm_xb_ddb_b_num1[3] + 1
            hm_xb_ddb_j_num1[3] = hm_xb_ddb_j_num1[3] + float(hm_xb_ddb[0][i][1])
        if float(hm_xb_ddb[0][i][2]) > 8 and float(hm_xb_ddb[0][i][2]) <= 10:
            hm_xb_ddb_b_num1[4] = hm_xb_ddb_b_num1[4] + 1
            hm_xb_ddb_j_num1[4] = hm_xb_ddb_j_num1[4] + float(hm_xb_ddb[0][i][1])
        if float(hm_xb_ddb[0][i][2]) > 10 and float(hm_xb_ddb[0][i][2]) <= 12:
            hm_xb_ddb_b_num1[5] = hm_xb_ddb_b_num1[5] + 1
            hm_xb_ddb_j_num1[5] = hm_xb_ddb_j_num1[5] + float(hm_xb_ddb[0][i][1])
        if float(hm_xb_ddb[0][i][2]) > 12 and float(hm_xb_ddb[0][i][2]) <= 24:
            hm_xb_ddb_b_num1[6] = hm_xb_ddb_b_num1[6] + 1
            hm_xb_ddb_j_num1[6] = hm_xb_ddb_j_num1[6] + float(hm_xb_ddb[0][i][1])
        if float(hm_xb_ddb[0][i][2]) > 24:
            hm_xb_ddb_b_num1[7] = hm_xb_ddb_b_num1[7] + 1
            hm_xb_ddb_j_num1[7] = hm_xb_ddb_j_num1[7] + float(hm_xb_ddb[0][i][1])

    for i in range(len(hm_xb_dck[0])):
        if float(hm_xb_dck[0][i][2]) > 0 and float(hm_xb_dck[0][i][2]) <= 2:
            hm_xb_dck_b_num1[0] = hm_xb_dck_b_num1[0] + 1
            hm_xb_dck_j_num1[0] = hm_xb_dck_j_num1[0] + float(hm_xb_dck[0][i][1])
        if float(hm_xb_dck[0][i][2]) > 2 and float(hm_xb_dck[0][i][2]) <= 4:
            hm_xb_dck_b_num1[1] = hm_xb_dck_b_num1[1] + 1
            hm_xb_dck_j_num1[1] = hm_xb_dck_j_num1[1] + float(hm_xb_dck[0][i][1])
        if float(hm_xb_dck[0][i][2]) > 4 and float(hm_xb_dck[0][i][2]) <= 6:
            hm_xb_dck_b_num1[2] = hm_xb_dck_b_num1[2] + 1
            hm_xb_dck_j_num1[2] = hm_xb_dck_j_num1[2] + float(hm_xb_dck[0][i][1])
        if float(hm_xb_dck[0][i][2]) > 6 and float(hm_xb_dck[0][i][2]) <= 8:
            hm_xb_dck_b_num1[3] = hm_xb_dck_b_num1[3] + 1
            hm_xb_dck_j_num1[3] = hm_xb_dck_j_num1[3] + float(hm_xb_dck[0][i][1])
        if float(hm_xb_dck[0][i][2]) > 8 and float(hm_xb_dck[0][i][2]) <= 10:
            hm_xb_dck_b_num1[4] = hm_xb_dck_b_num1[4] + 1
            hm_xb_dck_j_num1[4] = hm_xb_dck_j_num1[4] + float(hm_xb_dck[0][i][1])
        if float(hm_xb_dck[0][i][2]) > 10 and float(hm_xb_dck[0][i][2]) <= 12:
            hm_xb_dck_b_num1[5] = hm_xb_dck_b_num1[5] + 1
            hm_xb_dck_j_num1[5] = hm_xb_dck_j_num1[5] + float(hm_xb_dck[0][i][1])
        if float(hm_xb_dck[0][i][2]) > 12 and float(hm_xb_dck[0][i][2]) <= 24:
            hm_xb_dck_b_num1[6] = hm_xb_dck_b_num1[6] + 1
            hm_xb_dck_j_num1[6] = hm_xb_dck_j_num1[6] + float(hm_xb_dck[0][i][1])
        if float(hm_xb_dck[0][i][2]) > 24:
            hm_xb_dck_b_num1[7] = hm_xb_dck_b_num1[7] + 1
            hm_xb_dck_j_num1[7] = hm_xb_dck_j_num1[7] + float(hm_xb_dck[0][i][1])

    for i in range(len(tx_xb_djy[0])):
        if float(tx_xb_djy[0][i][2]) > 0 and float(tx_xb_djy[0][i][2]) <= 2:
            tx_xb_djy_b_num1[0] = tx_xb_djy_b_num1[0] + 1
            tx_xb_djy_j_num1[0] = tx_xb_djy_j_num1[0] + float(tx_xb_djy[0][i][1])
        if float(tx_xb_djy[0][i][2]) > 2 and float(tx_xb_djy[0][i][2]) <= 4:
            tx_xb_djy_b_num1[1] = tx_xb_djy_b_num1[1] + 1
            tx_xb_djy_j_num1[1] = tx_xb_djy_j_num1[1] + float(tx_xb_djy[0][i][1])
        if float(tx_xb_djy[0][i][2]) > 4 and float(tx_xb_djy[0][i][2]) <= 6:
            tx_xb_djy_b_num1[2] = tx_xb_djy_b_num1[2] + 1
            tx_xb_djy_j_num1[2] = tx_xb_djy_j_num1[2] + float(tx_xb_djy[0][i][1])
        if float(tx_xb_djy[0][i][2]) > 6 and float(tx_xb_djy[0][i][2]) <= 8:
            tx_xb_djy_b_num1[3] = tx_xb_djy_b_num1[3] + 1
            tx_xb_djy_j_num1[3] = tx_xb_djy_j_num1[3] + float(tx_xb_djy[0][i][1])
        if float(tx_xb_djy[0][i][2]) > 8 and float(tx_xb_djy[0][i][2]) <= 10:
            tx_xb_djy_b_num1[4] = tx_xb_djy_b_num1[4] + 1
            tx_xb_djy_j_num1[4] = tx_xb_djy_j_num1[4] + float(tx_xb_djy[0][i][1])
        if float(tx_xb_djy[0][i][2]) > 10 and float(tx_xb_djy[0][i][2]) <= 12:
            tx_xb_djy_b_num1[5] = tx_xb_djy_b_num1[5] + 1
            tx_xb_djy_j_num1[5] = tx_xb_djy_j_num1[5] + float(tx_xb_djy[0][i][1])
        if float(tx_xb_djy[0][i][2]) > 12 and float(tx_xb_djy[0][i][2]) <= 24:
            tx_xb_djy_b_num1[6] = tx_xb_djy_b_num1[6] + 1
            tx_xb_djy_j_num1[6] = tx_xb_djy_j_num1[6] + float(tx_xb_djy[0][i][1])
        if float(tx_xb_djy[0][i][2]) > 24:
            tx_xb_djy_b_num1[7] = tx_xb_djy_b_num1[7] + 1
            tx_xb_djy_j_num1[7] = tx_xb_djy_j_num1[7] + float(tx_xb_djy[0][i][1])
    for i in range(len(tx_xb_dfpld[0])):
        if float(tx_xb_dfpld[0][i][2]) > 0 and float(tx_xb_dfpld[0][i][2]) <= 2:
            tx_xb_dfpld_b_num1[0] = tx_xb_dfpld_b_num1[0] + 1
            tx_xb_dfpld_j_num1[0] = tx_xb_dfpld_j_num1[0] + float(tx_xb_dfpld[0][i][1])
        if float(tx_xb_dfpld[0][i][2]) > 2 and float(tx_xb_dfpld[0][i][2]) <= 4:
            tx_xb_dfpld_b_num1[1] = tx_xb_dfpld_b_num1[1] + 1
            tx_xb_dfpld_j_num1[1] = tx_xb_dfpld_j_num1[1] + float(tx_xb_dfpld[0][i][1])
        if float(tx_xb_dfpld[0][i][2]) > 4 and float(tx_xb_dfpld[0][i][2]) <= 6:
            tx_xb_dfpld_b_num1[2] = tx_xb_dfpld_b_num1[2] + 1
            tx_xb_dfpld_j_num1[2] = tx_xb_dfpld_j_num1[2] + float(tx_xb_dfpld[0][i][1])
        if float(tx_xb_dfpld[0][i][2]) > 6 and float(tx_xb_dfpld[0][i][2]) <= 8:
            tx_xb_dfpld_b_num1[3] = tx_xb_dfpld_b_num1[3] + 1
            tx_xb_dfpld_j_num1[3] = tx_xb_dfpld_j_num1[3] + float(tx_xb_dfpld[0][i][1])
        if float(tx_xb_dfpld[0][i][2]) > 8 and float(tx_xb_dfpld[0][i][2]) <= 10:
            tx_xb_dfpld_b_num1[4] = tx_xb_dfpld_b_num1[4] + 1
            tx_xb_dfpld_j_num1[4] = tx_xb_dfpld_j_num1[4] + float(tx_xb_dfpld[0][i][1])
        if float(tx_xb_dfpld[0][i][2]) > 10 and float(tx_xb_dfpld[0][i][2]) <= 12:
            tx_xb_dfpld_b_num1[5] = tx_xb_dfpld_b_num1[5] + 1
            tx_xb_dfpld_j_num1[5] = tx_xb_dfpld_j_num1[5] + float(tx_xb_dfpld[0][i][1])
        if float(tx_xb_dfpld[0][i][2]) > 12 and float(tx_xb_dfpld[0][i][2]) <= 24:
            tx_xb_dfpld_b_num1[6] = tx_xb_dfpld_b_num1[6] + 1
            tx_xb_dfpld_j_num1[6] = tx_xb_dfpld_j_num1[6] + float(tx_xb_dfpld[0][i][1])
        if float(tx_xb_dfpld[0][i][2]) > 24:
            tx_xb_dfpld_b_num1[7] = tx_xb_dfpld_b_num1[7] + 1
            tx_xb_dfpld_j_num1[7] = tx_xb_dfpld_j_num1[7] + float(tx_xb_dfpld[0][i][1])
    for i in range(len(tx_xb_dpk[0])):
        if float(tx_xb_dpk[0][i][2]) > 0 and float(tx_xb_dpk[0][i][2]) <= 2:
            tx_xb_dpk_b_num1[0] = tx_xb_dpk_b_num1[0] + 1
            tx_xb_dpk_j_num1[0] = tx_xb_dpk_j_num1[0] + float(tx_xb_dpk[0][i][1])
        if float(tx_xb_dpk[0][i][2]) > 2 and float(tx_xb_dpk[0][i][2]) <= 4:
            tx_xb_dpk_b_num1[1] = tx_xb_dpk_b_num1[1] + 1
            tx_xb_dpk_j_num1[1] = tx_xb_dpk_j_num1[1] + float(tx_xb_dpk[0][i][1])
        if float(tx_xb_dpk[0][i][2]) > 4 and float(tx_xb_dpk[0][i][2]) <= 6:
            tx_xb_dpk_b_num1[2] = tx_xb_dpk_b_num1[2] + 1
            tx_xb_dpk_j_num1[2] = tx_xb_dpk_j_num1[2] + float(tx_xb_dpk[0][i][1])
        if float(tx_xb_dpk[0][i][2]) > 6 and float(tx_xb_dpk[0][i][2]) <= 8:
            tx_xb_dpk_b_num1[3] = tx_xb_dpk_b_num1[3] + 1
            tx_xb_dpk_j_num1[3] = tx_xb_dpk_j_num1[3] + float(tx_xb_dpk[0][i][1])
        if float(tx_xb_dpk[0][i][2]) > 8 and float(tx_xb_dpk[0][i][2]) <= 10:
            tx_xb_dpk_b_num1[4] = tx_xb_dpk_b_num1[4] + 1
            tx_xb_dpk_j_num1[4] = tx_xb_dpk_j_num1[4] + float(tx_xb_dpk[0][i][1])
        if float(tx_xb_dpk[0][i][2]) > 10 and float(tx_xb_dpk[0][i][2]) <= 12:
            tx_xb_dpk_b_num1[5] = tx_xb_dpk_b_num1[5] + 1
            tx_xb_dpk_j_num1[5] = tx_xb_dpk_j_num1[5] + float(tx_xb_dpk[0][i][1])
        if float(tx_xb_dpk[0][i][2]) > 12 and float(tx_xb_dpk[0][i][2]) <= 24:
            tx_xb_dpk_b_num1[6] = tx_xb_dpk_b_num1[6] + 1
            tx_xb_dpk_j_num1[6] = tx_xb_dpk_j_num1[6] + float(tx_xb_dpk[0][i][1])
        if float(tx_xb_dpk[0][i][2]) > 24:
            tx_xb_dpk_b_num1[7] = tx_xb_dpk_b_num1[7] + 1
            tx_xb_dpk_j_num1[7] = tx_xb_dpk_j_num1[7] + float(tx_xb_dpk[0][i][1])

    for i in range(len(tx_xb_dld[0])):
        if float(tx_xb_dld[0][i][2]) > 0 and float(tx_xb_dld[0][i][2]) <= 2:
            tx_xb_dld_b_num1[0] = tx_xb_dld_b_num1[0] + 1
            tx_xb_dld_j_num1[0] = tx_xb_dld_j_num1[0] + float(tx_xb_dld[0][i][1])
        if float(tx_xb_dld[0][i][2]) > 2 and float(tx_xb_dld[0][i][2]) <= 4:
            tx_xb_dld_b_num1[1] = tx_xb_dld_b_num1[1] + 1
            tx_xb_dld_j_num1[1] = tx_xb_dld_j_num1[1] + float(tx_xb_dld[0][i][1])
        if float(tx_xb_dld[0][i][2]) > 4 and float(tx_xb_dld[0][i][2]) <= 6:
            tx_xb_dld_b_num1[2] = tx_xb_dld_b_num1[2] + 1
            tx_xb_dld_j_num1[2] = tx_xb_dld_j_num1[2] + float(tx_xb_dld[0][i][1])
        if float(tx_xb_dld[0][i][2]) > 6 and float(tx_xb_dld[0][i][2]) <= 8:
            tx_xb_dld_b_num1[3] = tx_xb_dld_b_num1[3] + 1
            tx_xb_dld_j_num1[3] = tx_xb_dld_j_num1[3] + float(tx_xb_dld[0][i][1])
        if float(tx_xb_dld[0][i][2]) > 8 and float(tx_xb_dld[0][i][2]) <= 10:
            tx_xb_dld_b_num1[4] = tx_xb_dld_b_num1[4] + 1
            tx_xb_dld_j_num1[4] = tx_xb_dld_j_num1[4] + float(tx_xb_dld[0][i][1])
        if float(tx_xb_dld[0][i][2]) > 10 and float(tx_xb_dld[0][i][2]) <= 12:
            tx_xb_dld_b_num1[5] = tx_xb_dld_b_num1[5] + 1
            tx_xb_dld_j_num1[5] = tx_xb_dld_j_num1[5] + float(tx_xb_dld[0][i][1])
        if float(tx_xb_dld[0][i][2]) > 12 and float(tx_xb_dld[0][i][2]) <= 24:
            tx_xb_dld_b_num1[6] = tx_xb_dld_b_num1[6] + 1
            tx_xb_dld_j_num1[6] = tx_xb_dld_j_num1[6] + float(tx_xb_dld[0][i][1])
        if float(tx_xb_dld[0][i][2]) > 24:
            tx_xb_dld_b_num1[7] = tx_xb_dld_b_num1[7] + 1
            tx_xb_dld_j_num1[7] = tx_xb_dld_j_num1[7] + float(tx_xb_dld[0][i][1])

    for i in range(len(tx_xb_djh[0])):
        if float(tx_xb_djh[0][i][2]) > 0 and float(tx_xb_djh[0][i][2]) <= 2:
            tx_xb_djh_b_num1[0] = tx_xb_djh_b_num1[0] + 1
            tx_xb_djh_j_num1[0] = tx_xb_djh_j_num1[0] + float(tx_xb_djh[0][i][1])
        if float(tx_xb_djh[0][i][2]) > 2 and float(tx_xb_djh[0][i][2]) <= 4:
            tx_xb_djh_b_num1[1] = tx_xb_djh_b_num1[1] + 1
            tx_xb_djh_j_num1[1] = tx_xb_djh_j_num1[1] + float(tx_xb_djh[0][i][1])
        if float(tx_xb_djh[0][i][2]) > 4 and float(tx_xb_djh[0][i][2]) <= 6:
            tx_xb_djh_b_num1[2] = tx_xb_djh_b_num1[2] + 1
            tx_xb_djh_j_num1[2] = tx_xb_djh_j_num1[2] + float(tx_xb_djh[0][i][1])
        if float(tx_xb_djh[0][i][2]) > 6 and float(tx_xb_djh[0][i][2]) <= 8:
            tx_xb_djh_b_num1[3] = tx_xb_djh_b_num1[3] + 1
            tx_xb_djh_j_num1[3] = tx_xb_djh_j_num1[3] + float(tx_xb_djh[0][i][1])
        if float(tx_xb_djh[0][i][2]) > 8 and float(tx_xb_djh[0][i][2]) <= 10:
            tx_xb_djh_b_num1[4] = tx_xb_djh_b_num1[4] + 1
            tx_xb_djh_j_num1[4] = tx_xb_djh_j_num1[4] + float(tx_xb_djh[0][i][1])
        if float(tx_xb_djh[0][i][2]) > 10 and float(tx_xb_djh[0][i][2]) <= 12:
            tx_xb_djh_b_num1[5] = tx_xb_djh_b_num1[5] + 1
            tx_xb_djh_j_num1[5] = tx_xb_djh_j_num1[5] + float(tx_xb_djh[0][i][1])
        if float(tx_xb_djh[0][i][2]) > 12 and float(tx_xb_djh[0][i][2]) <= 24:
            tx_xb_djh_b_num1[6] = tx_xb_djh_b_num1[6] + 1
            tx_xb_djh_j_num1[6] = tx_xb_djh_j_num1[6] + float(tx_xb_djh[0][i][1])
        if float(tx_xb_djh[0][i][2]) > 24:
            tx_xb_djh_b_num1[7] = tx_xb_djh_b_num1[7] + 1
            tx_xb_djh_j_num1[7] = tx_xb_djh_j_num1[7] + float(tx_xb_djh[0][i][1])

    for i in range(len(tx_xb_ddb[0])):
        if float(tx_xb_ddb[0][i][2]) > 0 and float(tx_xb_ddb[0][i][2]) <= 2:
            tx_xb_ddb_b_num1[0] = tx_xb_ddb_b_num1[0] + 1
            tx_xb_ddb_j_num1[0] = tx_xb_ddb_j_num1[0] + float(tx_xb_ddb[0][i][1])
        if float(tx_xb_ddb[0][i][2]) > 2 and float(tx_xb_ddb[0][i][2]) <= 4:
            tx_xb_ddb_b_num1[1] = tx_xb_ddb_b_num1[1] + 1
            tx_xb_ddb_j_num1[1] = tx_xb_ddb_j_num1[1] + float(tx_xb_ddb[0][i][1])
        if float(tx_xb_ddb[0][i][2]) > 4 and float(tx_xb_ddb[0][i][2]) <= 6:
            tx_xb_ddb_b_num1[2] = tx_xb_ddb_b_num1[2] + 1
            tx_xb_ddb_j_num1[2] = tx_xb_ddb_j_num1[2] + float(tx_xb_ddb[0][i][1])
        if float(tx_xb_ddb[0][i][2]) > 6 and float(tx_xb_ddb[0][i][2]) <= 8:
            tx_xb_ddb_b_num1[3] = tx_xb_ddb_b_num1[3] + 1
            tx_xb_ddb_j_num1[3] = tx_xb_ddb_j_num1[3] + float(tx_xb_ddb[0][i][1])
        if float(tx_xb_ddb[0][i][2]) > 8 and float(tx_xb_ddb[0][i][2]) <= 10:
            tx_xb_ddb_b_num1[4] = tx_xb_ddb_b_num1[4] + 1
            tx_xb_ddb_j_num1[4] = tx_xb_ddb_j_num1[4] + float(tx_xb_ddb[0][i][1])
        if float(tx_xb_ddb[0][i][2]) > 10 and float(tx_xb_ddb[0][i][2]) <= 12:
            tx_xb_ddb_b_num1[5] = tx_xb_ddb_b_num1[5] + 1
            tx_xb_ddb_j_num1[5] = tx_xb_ddb_j_num1[5] + float(tx_xb_ddb[0][i][1])
        if float(tx_xb_ddb[0][i][2]) > 12 and float(tx_xb_ddb[0][i][2]) <= 24:
            tx_xb_ddb_b_num1[6] = tx_xb_ddb_b_num1[6] + 1
            tx_xb_ddb_j_num1[6] = tx_xb_ddb_j_num1[6] + float(tx_xb_ddb[0][i][1])
        if float(tx_xb_ddb[0][i][2]) > 24:
            tx_xb_ddb_b_num1[7] = tx_xb_ddb_b_num1[7] + 1
            tx_xb_ddb_j_num1[7] = tx_xb_ddb_j_num1[7] + float(tx_xb_ddb[0][i][1])

    for i in range(len(tx_xb_dck[0])):
        if float(tx_xb_dck[0][i][2]) > 0 and float(tx_xb_dck[0][i][2]) <= 2:
            tx_xb_dck_b_num1[0] = tx_xb_dck_b_num1[0] + 1
            tx_xb_dck_j_num1[0] = tx_xb_dck_j_num1[0] + float(tx_xb_dck[0][i][1])
        if float(tx_xb_dck[0][i][2]) > 2 and float(tx_xb_dck[0][i][2]) <= 4:
            tx_xb_dck_b_num1[1] = tx_xb_dck_b_num1[1] + 1
            tx_xb_dck_j_num1[1] = tx_xb_dck_j_num1[1] + float(tx_xb_dck[0][i][1])
        if float(tx_xb_dck[0][i][2]) > 4 and float(tx_xb_dck[0][i][2]) <= 6:
            tx_xb_dck_b_num1[2] = tx_xb_dck_b_num1[2] + 1
            tx_xb_dck_j_num1[2] = tx_xb_dck_j_num1[2] + float(tx_xb_dck[0][i][1])
        if float(tx_xb_dck[0][i][2]) > 6 and float(tx_xb_dck[0][i][2]) <= 8:
            tx_xb_dck_b_num1[3] = tx_xb_dck_b_num1[3] + 1
            tx_xb_dck_j_num1[3] = tx_xb_dck_j_num1[3] + float(tx_xb_dck[0][i][1])
        if float(tx_xb_dck[0][i][2]) > 8 and float(tx_xb_dck[0][i][2]) <= 10:
            tx_xb_dck_b_num1[4] = tx_xb_dck_b_num1[4] + 1
            tx_xb_dck_j_num1[4] = tx_xb_dck_j_num1[4] + float(tx_xb_dck[0][i][1])
        if float(tx_xb_dck[0][i][2]) > 10 and float(tx_xb_dck[0][i][2]) <= 12:
            tx_xb_dck_b_num1[5] = tx_xb_dck_b_num1[5] + 1
            tx_xb_dck_j_num1[5] = tx_xb_dck_j_num1[5] + float(tx_xb_dck[0][i][1])
        if float(tx_xb_dck[0][i][2]) > 12 and float(tx_xb_dck[0][i][2]) <= 24:
            tx_xb_dck_b_num1[6] = tx_xb_dck_b_num1[6] + 1
            tx_xb_dck_j_num1[6] = tx_xb_dck_j_num1[6] + float(tx_xb_dck[0][i][1])
        if float(tx_xb_dck[0][i][2]) > 24:
            tx_xb_dck_b_num1[7] = tx_xb_dck_b_num1[7] + 1
            tx_xb_dck_j_num1[7] = tx_xb_dck_j_num1[7] + float(tx_xb_dck[0][i][1])

    hm_b_xb_num_2 = np.r_[
        hm_xb_dpk_b_num1[0], hm_xb_dfpld_b_num1[0], hm_xb_dld_b_num1[0], hm_xb_djh_b_num1[0], hm_xb_ddb_b_num1[0],
        hm_xb_dck_b_num1[0],
        hm_xb_djy_b_num1[0]]

    hm_b_xb_num_4 = np.r_[
        hm_xb_dpk_b_num1[1], hm_xb_dfpld_b_num1[1], hm_xb_dld_b_num1[1], hm_xb_djh_b_num1[1], hm_xb_ddb_b_num1[1],
        hm_xb_dck_b_num1[1],
        hm_xb_djy_b_num1[1]]
    hm_b_xb_num_6 = np.r_[
        hm_xb_dpk_b_num1[2], hm_xb_dfpld_b_num1[2], hm_xb_dld_b_num1[2], hm_xb_djh_b_num1[2], hm_xb_ddb_b_num1[2],
        hm_xb_dck_b_num1[2],
        hm_xb_djy_b_num1[2]]
    hm_b_xb_num_8 = np.r_[
        hm_xb_dpk_b_num1[3], hm_xb_dfpld_b_num1[3], hm_xb_dld_b_num1[3], hm_xb_djh_b_num1[3], hm_xb_ddb_b_num1[3],
        hm_xb_dck_b_num1[3],
        hm_xb_djy_b_num1[3]]
    hm_b_xb_num_10 = np.r_[
        hm_xb_dpk_b_num1[4], hm_xb_dfpld_b_num1[4], hm_xb_dld_b_num1[4], hm_xb_djh_b_num1[4], hm_xb_ddb_b_num1[4],
        hm_xb_dck_b_num1[4],
        hm_xb_djy_b_num1[4]]
    hm_b_xb_num_12 = np.r_[
        hm_xb_dpk_b_num1[5], hm_xb_dfpld_b_num1[5], hm_xb_dld_b_num1[5], hm_xb_djh_b_num1[5], hm_xb_ddb_b_num1[5],
        hm_xb_dck_b_num1[5],
        hm_xb_djy_b_num1[5]]
    hm_b_xb_num_24 = np.r_[
        hm_xb_dpk_b_num1[6], hm_xb_dfpld_b_num1[6], hm_xb_dld_b_num1[6], hm_xb_djh_b_num1[6], hm_xb_ddb_b_num1[6],
        hm_xb_dck_b_num1[6],
        hm_xb_djy_b_num1[6]]
    hm_b_xb_num_24_ = np.r_[
        hm_xb_dpk_b_num1[7], hm_xb_dfpld_b_num1[7], hm_xb_dld_b_num1[7], hm_xb_djh_b_num1[7], hm_xb_ddb_b_num1[7],
        hm_xb_dck_b_num1[7],
        hm_xb_djy_b_num1[7]]

    tx_b_xb_num_2 = np.r_[
        tx_xb_dpk_b_num1[0], tx_xb_dfpld_b_num1[0], tx_xb_dld_b_num1[0], tx_xb_djh_b_num1[0], tx_xb_ddb_b_num1[0],
        tx_xb_dck_b_num1[0],
        tx_xb_djy_b_num1[0]]

    tx_b_xb_num_4 = np.r_[
        tx_xb_dpk_b_num1[1], tx_xb_dfpld_b_num1[1], tx_xb_dld_b_num1[1], tx_xb_djh_b_num1[1], tx_xb_ddb_b_num1[1],
        tx_xb_dck_b_num1[1],
        tx_xb_djy_b_num1[1]]
    tx_b_xb_num_6 = np.r_[
        tx_xb_dpk_b_num1[2], tx_xb_dfpld_b_num1[2], tx_xb_dld_b_num1[2], tx_xb_djh_b_num1[2], tx_xb_ddb_b_num1[2],
        tx_xb_dck_b_num1[2],
        tx_xb_djy_b_num1[2]]
    tx_b_xb_num_8 = np.r_[
        tx_xb_dpk_b_num1[3], tx_xb_dfpld_b_num1[3], tx_xb_dld_b_num1[3], tx_xb_djh_b_num1[3], tx_xb_ddb_b_num1[3],
        tx_xb_dck_b_num1[3],
        tx_xb_djy_b_num1[3]]
    tx_b_xb_num_10 = np.r_[
        tx_xb_dpk_b_num1[4], tx_xb_dfpld_b_num1[4], tx_xb_dld_b_num1[4], tx_xb_djh_b_num1[4], tx_xb_ddb_b_num1[4],
        tx_xb_dck_b_num1[4],
        tx_xb_djy_b_num1[4]]
    tx_b_xb_num_12 = np.r_[
        tx_xb_dpk_b_num1[5], tx_xb_dfpld_b_num1[5], tx_xb_dld_b_num1[5], tx_xb_djh_b_num1[5], tx_xb_ddb_b_num1[5],
        tx_xb_dck_b_num1[5],
        tx_xb_djy_b_num1[5]]
    tx_b_xb_num_24 = np.r_[
        tx_xb_dpk_b_num1[6], tx_xb_dfpld_b_num1[6], tx_xb_dld_b_num1[6], tx_xb_djh_b_num1[6], tx_xb_ddb_b_num1[6],
        tx_xb_dck_b_num1[6],
        tx_xb_djy_b_num1[6]]
    tx_b_xb_num_24_ = np.r_[
        tx_xb_dpk_b_num1[7], tx_xb_dfpld_b_num1[7], tx_xb_dld_b_num1[7], tx_xb_djh_b_num1[7], tx_xb_ddb_b_num1[7],
        tx_xb_dck_b_num1[7],
        tx_xb_djy_b_num1[7]]
    print(hm_b_xb_num_2)

    arrayA = np.divide(hm_b_xb_num_2, max(hm_b_xb_num_2), out=np.zeros_like(hm_b_xb_num_2, dtype=np.float64),
                       where=max(hm_b_xb_num_2) != 0)
    for i in range(len(hm_b_xb_num_2)):
        hm_xb_b_2.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_xb_num_2[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_xb_num_2)):
            hm_b_xb_num_2[i] = '{:.2%}'.format(a)

    arrayA = np.divide(hm_b_xb_num_4, max(hm_b_xb_num_4), out=np.zeros_like(hm_b_xb_num_4, dtype=np.float64),
                       where=max(hm_b_xb_num_4) != 0)
    for i in range(len(hm_b_xb_num_4)):
        hm_xb_b_4.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_xb_num_4[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_xb_num_4)):
            hm_b_xb_num_4[i] = '{:.2%}'.format(a)

    arrayA = np.divide(hm_b_xb_num_6, max(hm_b_xb_num_6), out=np.zeros_like(hm_b_xb_num_6, dtype=np.float64),
                       where=max(hm_b_xb_num_6) != 0)
    for i in range(len(hm_b_xb_num_6)):
        hm_xb_b_6.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_xb_num_6[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_xb_num_6)):
            hm_b_xb_num_6[i] = '{:.2%}'.format(a)

    arrayA = np.divide(hm_b_xb_num_8, max(hm_b_xb_num_8), out=np.zeros_like(hm_b_xb_num_8, dtype=np.float64),
                       where=max(hm_b_xb_num_8) != 0)
    for i in range(len(hm_b_xb_num_8)):
        hm_xb_b_8.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_xb_num_8[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_xb_num_8)):
            hm_b_xb_num_8[i] = '{:.2%}'.format(a)

    arrayA = np.divide(hm_b_xb_num_10, max(hm_b_xb_num_10), out=np.zeros_like(hm_b_xb_num_10, dtype=np.float64),
                       where=max(hm_b_xb_num_10) != 0)
    for i in range(len(hm_b_xb_num_10)):
        hm_xb_b_10.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_xb_num_10[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_xb_num_10)):
            hm_b_xb_num_10[i] = '{:.2%}'.format(a)

    arrayA = np.divide(hm_b_xb_num_12, max(hm_b_xb_num_12), out=np.zeros_like(hm_b_xb_num_12, dtype=np.float64),
                       where=max(hm_b_xb_num_12) != 0)
    for i in range(len(hm_b_xb_num_12)):
        hm_xb_b_12.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_xb_num_12[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_xb_num_12)):
            hm_b_xb_num_12[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_b_xb_num_24, max(hm_b_xb_num_24), out=np.zeros_like(hm_b_xb_num_24, dtype=np.float64),
                       where=max(hm_b_xb_num_24) != 0)
    for i in range(len(hm_b_xb_num_24)):
        hm_xb_b_24.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_xb_num_24[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_xb_num_24)):
            hm_b_xb_num_24[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_b_xb_num_24_, max(hm_b_xb_num_24_), out=np.zeros_like(hm_b_xb_num_24_, dtype=np.float64),
                       where=max(hm_b_xb_num_24_) != 0)
    for i in range(len(hm_b_xb_num_24_)):
        hm_xb_b_24_.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_xb_num_24_[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_xb_num_24_)):
            hm_b_xb_num_24_[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_b_xb_num_2, max(tx_b_xb_num_2), out=np.zeros_like(tx_b_xb_num_2, dtype=np.float64),
                       where=max(tx_b_xb_num_2) != 0)
    for i in range(len(tx_b_xb_num_2)):
        tx_xb_b_2.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_xb_num_2[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_xb_num_2)):
            tx_b_xb_num_2[i] = '{:.2%}'.format(a)

    arrayA = np.divide(tx_b_xb_num_4, max(tx_b_xb_num_4), out=np.zeros_like(tx_b_xb_num_4, dtype=np.float64),
                       where=max(tx_b_xb_num_4) != 0)
    for i in range(len(tx_b_xb_num_4)):
        tx_xb_b_4.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_xb_num_4[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_xb_num_4)):
            tx_b_xb_num_4[i] = '{:.2%}'.format(a)

    arrayA = np.divide(tx_b_xb_num_6, max(tx_b_xb_num_6), out=np.zeros_like(tx_b_xb_num_6, dtype=np.float64),
                       where=max(tx_b_xb_num_6) != 0)
    for i in range(len(tx_b_xb_num_6)):
        tx_xb_b_6.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_xb_num_6[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_xb_num_6)):
            tx_b_xb_num_6[i] = '{:.2%}'.format(a)

    arrayA = np.divide(tx_b_xb_num_8, max(tx_b_xb_num_8), out=np.zeros_like(tx_b_xb_num_8, dtype=np.float64),
                       where=max(tx_b_xb_num_8) != 0)
    for i in range(len(tx_b_xb_num_8)):
        tx_xb_b_8.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_xb_num_8[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_xb_num_8)):
            tx_b_xb_num_8[i] = '{:.2%}'.format(a)

    arrayA = np.divide(tx_b_xb_num_10, max(tx_b_xb_num_10), out=np.zeros_like(tx_b_xb_num_10, dtype=np.float64),
                       where=max(tx_b_xb_num_10) != 0)
    for i in range(len(tx_b_xb_num_10)):
        tx_xb_b_10.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_xb_num_10[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_xb_num_10)):
            tx_b_xb_num_10[i] = '{:.2%}'.format(a)

    arrayA = np.divide(tx_b_xb_num_12, max(tx_b_xb_num_12), out=np.zeros_like(tx_b_xb_num_12, dtype=np.float64),
                       where=max(tx_b_xb_num_12) != 0)
    for i in range(len(tx_b_xb_num_12)):
        tx_xb_b_12.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_xb_num_12[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_xb_num_12)):
            tx_b_xb_num_12[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_b_xb_num_24, max(tx_b_xb_num_24), out=np.zeros_like(tx_b_xb_num_24, dtype=np.float64),
                       where=max(tx_b_xb_num_24) != 0)
    for i in range(len(tx_b_xb_num_24)):
        tx_xb_b_24.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_xb_num_24[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_xb_num_24)):
            tx_b_xb_num_24[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_b_xb_num_24_, max(tx_b_xb_num_24_), out=np.zeros_like(tx_b_xb_num_24_, dtype=np.float64),
                       where=max(tx_b_xb_num_24_) != 0)
    for i in range(len(tx_b_xb_num_24_)):
        tx_xb_b_24_.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_xb_num_24_[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_xb_num_24_)):
            tx_b_xb_num_24_[i] = '{:.2%}'.format(a)

    warehouse_fba = []
    type_fba = []
    order_fba = []
    num_fba = []
    s_fba = []

    for data_fba in see_fba:
        warehouse_fba.append(data_fba[0])
        type_fba.append(data_fba[2])
        order_fba.append(data_fba[1])
        num_fba.append(data_fba[3])
        s_fba.append(data_fba[4])
    print(num_fba)
    hm_type_fba = []
    hm_order_fba = []
    hm_num_fba = []
    hm_s_fba = []
    tx_type_fba = []
    tx_order_fba = []
    tx_num_fba = []
    tx_s_fba = []
    for i in range(len(warehouse_fba)):
        if warehouse_fba[i] == 'HM_AA':
            hm_type_fba.append(type_fba[i])
            hm_order_fba.append(order_fba[i])
            hm_num_fba.append(num_fba[i])
            hm_s_fba.append(s_fba[i])
    for i in range(len(warehouse_fba)):
        if warehouse_fba[i] == 'SZ_AA':
            tx_type_fba.append(type_fba[i])
            tx_order_fba.append(order_fba[i])
            tx_num_fba.append(num_fba[i])
            tx_s_fba.append(s_fba[i])
    hm_fba_data = np.dstack((hm_type_fba, hm_order_fba, hm_num_fba, hm_s_fba))
    tx_fba_data = np.dstack((tx_type_fba, tx_order_fba, tx_num_fba, tx_s_fba))

    hm_djy_b_num = []
    hm_djy_j_num = []
    hm_djy_time = []
    hm_dfpld_b_num = []
    hm_dfpld_j_num = []
    hm_dfpld_time = []
    hm_dpk_b_num = []
    hm_dpk_j_num = []
    hm_dpk_time = []
    hm_dld_b_num = []
    hm_dld_j_num = []
    hm_dld_time = []
    hm_djh_b_num = []
    hm_djh_j_num = []
    hm_djh_time = []
    hm_ddb_b_num = []
    hm_ddb_j_num = []
    hm_ddb_time = []
    hm_dck_b_num = []
    hm_dck_j_num = []
    hm_dck_time = []
    tx_djy_b_num = []
    tx_djy_j_num = []
    tx_djy_time = []
    tx_dfpld_b_num = []
    tx_dfpld_j_num = []
    tx_dfpld_time = []
    tx_dpk_b_num = []
    tx_dpk_j_num = []
    tx_dpk_time = []
    tx_dld_b_num = []
    tx_dld_j_num = []
    tx_dld_time = []
    tx_djh_b_num = []
    tx_djh_j_num = []
    tx_djh_time = []
    tx_ddb_b_num = []
    tx_ddb_j_num = []
    tx_ddb_time = []
    tx_dck_b_num = []
    tx_dck_j_num = []
    tx_dck_time = []

    for i in range(len(hm_s_fba)):
        if (hm_fba_data[0][i][0] == 'DJY'):
            hm_djy_b_num.append(1)
            hm_djy_j_num.append(hm_fba_data[0][i][2])
            hm_djy_time.append(hm_fba_data[0][i][3])
    for i in range(len(hm_s_fba)):
        if (hm_fba_data[0][i][0] == 'DFPLD'):
            hm_dfpld_b_num.append(1)
            hm_dfpld_j_num.append(hm_fba_data[0][i][2])
            hm_dfpld_time.append(hm_fba_data[0][i][3])
    for i in range(len(hm_s_fba)):
        if (hm_fba_data[0][i][0] == 'DPK'):
            hm_dpk_b_num.append(1)
            hm_dpk_j_num.append(hm_fba_data[0][i][2])
            hm_dpk_time.append(hm_fba_data[0][i][3])

    for i in range(len(hm_s_fba)):
        if (hm_fba_data[0][i][0] == 'DLD'):
            hm_dld_b_num.append(1)
            hm_dld_j_num.append(hm_fba_data[0][i][2])
            hm_dld_time.append(hm_fba_data[0][i][3])
    for i in range(len(hm_s_fba)):
        if (hm_fba_data[0][i][0] == 'DJH'):
            hm_djh_b_num.append(1)
            hm_djh_j_num.append(hm_fba_data[0][i][2])
            hm_djh_time.append(hm_fba_data[0][i][3])
    for i in range(len(hm_s_fba)):
        if (hm_fba_data[0][i][0] == 'DDB'):
            hm_ddb_b_num.append(1)
            hm_ddb_j_num.append(hm_fba_data[0][i][2])
            hm_ddb_time.append(hm_fba_data[0][i][3])
    for i in range(len(hm_s_fba)):
        if (hm_fba_data[0][i][0] == 'DCK'):
            hm_dck_b_num.append(1)
            hm_dck_j_num.append(hm_fba_data[0][i][2])
            hm_dck_time.append(hm_fba_data[0][i][3])
    for i in range(len(tx_s_fba)):
        if (tx_fba_data[0][i][0] == 'DJY'):
            tx_djy_b_num.append(1)
            tx_djy_j_num.append(tx_fba_data[0][i][2])
            tx_djy_time.append(tx_fba_data[0][i][3])
    for i in range(len(tx_s_fba)):
        if (tx_fba_data[0][i][0] == 'DFPLD'):
            tx_dfpld_b_num.append(1)
            tx_dfpld_j_num.append(tx_fba_data[0][i][2])
            tx_dfpld_time.append(tx_fba_data[0][i][3])
    for i in range(len(tx_s_fba)):
        if (tx_fba_data[0][i][0] == 'DPK'):
            tx_dpk_b_num.append(1)
            tx_dpk_j_num.append(tx_fba_data[0][i][2])
            tx_dpk_time.append(tx_fba_data[0][i][3])
    for i in range(len(tx_s_fba)):
        if (tx_fba_data[0][i][0] == 'DLD'):
            tx_dld_b_num.append(1)
            tx_dld_j_num.append(tx_fba_data[0][i][2])
            tx_dld_time.append(tx_fba_data[0][i][3])
    for i in range(len(tx_s_fba)):
        if (tx_fba_data[0][i][0] == 'DJH'):
            tx_djh_b_num.append(1)
            tx_djh_j_num.append(tx_fba_data[0][i][2])
            tx_djh_time.append(tx_fba_data[0][i][3])
    for i in range(len(tx_s_fba)):
        if (tx_fba_data[0][i][0] == 'DDB'):
            tx_ddb_b_num.append(1)
            tx_ddb_j_num.append(tx_fba_data[0][i][2])
            tx_ddb_time.append(tx_fba_data[0][i][3])
    for i in range(len(tx_s_fba)):
        if (tx_fba_data[0][i][0] == 'DCK'):
            tx_dck_b_num.append(1)
            tx_dck_j_num.append(tx_fba_data[0][i][2])
            tx_dck_time.append(tx_fba_data[0][i][3])

    hm_djy = np.dstack((hm_djy_b_num, hm_djy_j_num, hm_djy_time))
    hm_dfpld = np.dstack((hm_dfpld_b_num, hm_dfpld_j_num, hm_dfpld_time))
    hm_dpk = np.dstack((hm_dpk_b_num, hm_dpk_j_num, hm_dpk_time))
    hm_dld = np.dstack((hm_dld_b_num, hm_dld_j_num, hm_dld_time))
    hm_djh = np.dstack((hm_djh_b_num, hm_djh_j_num, hm_djh_time))
    hm_ddb = np.dstack((hm_ddb_b_num, hm_ddb_j_num, hm_ddb_time))
    hm_dck = np.dstack((hm_dck_b_num, hm_dck_j_num, hm_dck_time))
    tx_djy = np.dstack((tx_djy_b_num, tx_djy_j_num, tx_djy_time))
    tx_dfpld = np.dstack((tx_dfpld_b_num, tx_dfpld_j_num, tx_dfpld_time))
    tx_dpk = np.dstack((tx_dpk_b_num, tx_dpk_j_num, tx_dpk_time))
    tx_dld = np.dstack((tx_dld_b_num, tx_dld_j_num, tx_dld_time))
    tx_djh = np.dstack((tx_djh_b_num, tx_djh_j_num, tx_djh_time))
    tx_ddb = np.dstack((tx_ddb_b_num, tx_ddb_j_num, tx_ddb_time))
    tx_dck = np.dstack((tx_dck_b_num, tx_dck_j_num, tx_dck_time))

    hm_djy_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_djy_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_dfpld_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_dfpld_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_djy_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_djy_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_dfpld_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_dfpld_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_dpk_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_dld_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_djh_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_ddb_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_dck_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_dpk_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_dld_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_djh_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_ddb_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_dck_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_dpk_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_dld_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_djh_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_ddb_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_dck_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_dpk_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_dld_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_djh_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_ddb_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_dck_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]

    hm_b_12 = []
    hm_b_24 = []
    hm_b_48 = []
    hm_b_72 = []
    hm_b_120 = []
    hm_b_240 = []
    hm_b_360 = []
    hm_b_361 = []
    tx_b_12 = []
    tx_b_24 = []
    tx_b_48 = []
    tx_b_72 = []
    tx_b_120 = []
    tx_b_240 = []
    tx_b_360 = []
    tx_b_361 = []

    hm_j_12 = []
    hm_j_24 = []
    hm_j_48 = []
    hm_j_72 = []
    hm_j_120 = []
    hm_j_240 = []
    hm_j_360 = []
    hm_j_361 = []

    tx_j_12 = []
    tx_j_24 = []
    tx_j_48 = []
    tx_j_72 = []
    tx_j_120 = []
    tx_j_240 = []
    tx_j_360 = []
    tx_j_361 = []

    for i in range(len(hm_djy[0])):
        if float(hm_djy[0][i][2]) > 0 and float(hm_djy[0][i][2]) <= 12:
            hm_djy_b_num1[0] = hm_djy_b_num1[0] + 1
            hm_djy_j_num1[0] = hm_djy_j_num1[0] + float(hm_djy[0][i][1])
        if float(hm_djy[0][i][2]) > 12 and float(hm_djy[0][i][2]) <= 24:
            hm_djy_b_num1[1] = hm_djy_b_num1[1] + 1
            hm_djy_j_num1[1] = hm_djy_j_num1[1] + float(hm_djy[0][i][1])
        if float(hm_djy[0][i][2]) > 24 and float(hm_djy[0][i][2]) <= 48:
            hm_djy_b_num1[2] = hm_djy_b_num1[2] + 1
            hm_djy_j_num1[2] = hm_djy_j_num1[2] + float(hm_djy[0][i][1])
        if float(hm_djy[0][i][2]) > 48 and float(hm_djy[0][i][2]) <= 72:
            hm_djy_b_num1[3] = hm_djy_b_num1[3] + 1
            hm_djy_j_num1[3] = hm_djy_j_num1[3] + float(hm_djy[0][i][1])
        if float(hm_djy[0][i][2]) > 72 and float(hm_djy[0][i][2]) <= 120:
            hm_djy_b_num1[4] = hm_djy_b_num1[4] + 1
            hm_djy_j_num1[4] = hm_djy_j_num1[4] + float(hm_djy[0][i][1])
        if float(hm_djy[0][i][2]) > 120 and float(hm_djy[0][i][2]) <= 240:
            hm_djy_b_num1[5] = hm_djy_b_num1[5] + 1
            hm_djy_j_num1[5] = hm_djy_j_num1[5] + float(hm_djy[0][i][1])
        if float(hm_djy[0][i][2]) > 240 and float(hm_djy[0][i][2]) <= 360:
            hm_djy_b_num1[6] = hm_djy_b_num1[6] + 1
            hm_djy_j_num1[6] = hm_djy_j_num1[6] + float(hm_djy[0][i][1])
        if float(hm_djy[0][i][2]) > 360:
            hm_djy_b_num1[7] = hm_djy_b_num1[7] + 1
            hm_djy_j_num1[7] = hm_djy_j_num1[7] + float(hm_djy[0][i][1])

    for i in range(len(hm_dfpld[0])):
        if float(hm_dfpld[0][i][2]) > 0 and float(hm_dfpld[0][i][2]) <= 12:
            hm_dfpld_b_num1[0] = hm_dfpld_b_num1[0] + 1
            hm_dfpld_j_num1[0] = hm_dfpld_j_num1[0] + float(hm_dfpld[0][i][1])
        if float(hm_dfpld[0][i][2]) > 12 and float(hm_dfpld[0][i][2]) <= 24:
            hm_dfpld_b_num1[1] = hm_dfpld_b_num1[1] + 1
            hm_dfpld_j_num1[1] = hm_dfpld_j_num1[1] + float(hm_dfpld[0][i][1])
        if float(hm_dfpld[0][i][2]) > 24 and float(hm_dfpld[0][i][2]) <= 48:
            hm_dfpld_b_num1[2] = hm_dfpld_b_num1[2] + 1
            hm_dfpld_j_num1[2] = hm_dfpld_j_num1[2] + float(hm_dfpld[0][i][1])
        if float(hm_dfpld[0][i][2]) > 48 and float(hm_dfpld[0][i][2]) <= 72:
            hm_dfpld_b_num1[3] = hm_dfpld_b_num1[3] + 1
            hm_dfpld_j_num1[3] = hm_dfpld_j_num1[3] + float(hm_dfpld[0][i][1])
        if float(hm_dfpld[0][i][2]) > 72 and float(hm_dfpld[0][i][2]) <= 120:
            hm_dfpld_b_num1[4] = hm_dfpld_b_num1[4] + 1
            hm_dfpld_j_num1[4] = hm_dfpld_j_num1[4] + float(hm_dfpld[0][i][1])
        if float(hm_dfpld[0][i][2]) > 120 and float(hm_dfpld[0][i][2]) <= 240:
            hm_dfpld_b_num1[5] = hm_dfpld_b_num1[5] + 1
            hm_dfpld_j_num1[5] = hm_dfpld_j_num1[5] + float(hm_dfpld[0][i][1])
        if float(hm_dfpld[0][i][2]) > 240 and float(hm_dfpld[0][i][2]) <= 360:
            hm_dfpld_b_num1[6] = hm_dfpld_b_num1[6] + 1
            hm_dfpld_j_num1[6] = hm_dfpld_j_num1[6] + float(hm_dfpld[0][i][1])
        if float(hm_dfpld[0][i][2]) > 360:
            hm_dfpld_b_num1[7] = hm_dfpld_b_num1[7] + 1
            hm_dfpld_j_num1[7] = hm_dfpld_j_num1[7] + float(hm_dfpld[0][i][1])
    for i in range(len(hm_dpk[0])):
        if float(hm_dpk[0][i][2]) > 0 and float(hm_dpk[0][i][2]) <= 12:
            hm_dpk_b_num1[0] = hm_dpk_b_num1[0] + 1
            hm_dpk_j_num1[0] = hm_dpk_j_num1[0] + float(hm_dpk[0][i][1])
        if float(hm_dpk[0][i][2]) > 12 and float(hm_dpk[0][i][2]) <= 24:
            hm_dpk_b_num1[1] = hm_dpk_b_num1[1] + 1
            hm_dpk_j_num1[1] = hm_dpk_j_num1[1] + float(hm_dpk[0][i][1])
        if float(hm_dpk[0][i][2]) > 24 and float(hm_dpk[0][i][2]) <= 48:
            hm_dpk_b_num1[2] = hm_dpk_b_num1[2] + 1
            hm_dpk_j_num1[2] = hm_dpk_j_num1[2] + float(hm_dpk[0][i][1])
        if float(hm_dpk[0][i][2]) > 48 and float(hm_dpk[0][i][2]) <= 72:
            hm_dpk_b_num1[3] = hm_dpk_b_num1[3] + 1
            hm_dpk_j_num1[3] = hm_dpk_j_num1[3] + float(hm_dpk[0][i][1])
        if float(hm_dpk[0][i][2]) > 72 and float(hm_dpk[0][i][2]) <= 120:
            hm_dpk_b_num1[4] = hm_dpk_b_num1[4] + 1
            hm_dpk_j_num1[4] = hm_dpk_j_num1[4] + float(hm_dpk[0][i][1])
        if float(hm_dpk[0][i][2]) > 120 and float(hm_dpk[0][i][2]) <= 240:
            hm_dpk_b_num1[5] = hm_dpk_b_num1[5] + 1
            hm_dpk_j_num1[5] = hm_dpk_j_num1[5] + float(hm_dpk[0][i][1])
        if float(hm_dpk[0][i][2]) > 240 and float(hm_dpk[0][i][2]) <= 360:
            hm_dpk_b_num1[6] = hm_dpk_b_num1[6] + 1
            hm_dpk_j_num1[6] = hm_dpk_j_num1[6] + float(hm_dpk[0][i][1])
        if float(hm_dpk[0][i][2]) > 360:
            hm_dpk_b_num1[7] = hm_dpk_b_num1[7] + 1
            hm_dpk_j_num1[7] = hm_dpk_j_num1[7] + float(hm_dpk[0][i][1])
    for i in range(len(hm_dld[0])):
        if float(hm_dld[0][i][2]) > 0 and float(hm_dld[0][i][2]) <= 12:
            hm_dld_b_num1[0] = hm_dld_b_num1[0] + 1
            hm_dld_j_num1[0] = hm_dld_j_num1[0] + float(hm_dld[0][i][1])
        if float(hm_dld[0][i][2]) > 12 and float(hm_dld[0][i][2]) <= 24:
            hm_dld_b_num1[1] = hm_dld_b_num1[1] + 1
            hm_dld_j_num1[1] = hm_dld_j_num1[1] + float(hm_dld[0][i][1])
        if float(hm_dld[0][i][2]) > 24 and float(hm_dld[0][i][2]) <= 48:
            hm_dld_b_num1[2] = hm_dld_b_num1[2] + 1
            hm_dld_j_num1[2] = hm_dld_j_num1[2] + float(hm_dld[0][i][1])
        if float(hm_dld[0][i][2]) > 48 and float(hm_dld[0][i][2]) <= 72:
            hm_dld_b_num1[3] = hm_dld_b_num1[3] + 1
            hm_dld_j_num1[3] = hm_dld_j_num1[3] + float(hm_dld[0][i][1])
        if float(hm_dld[0][i][2]) > 72 and float(hm_dld[0][i][2]) <= 120:
            hm_dld_b_num1[4] = hm_dld_b_num1[4] + 1
            hm_dld_j_num1[4] = hm_dld_j_num1[4] + float(hm_dld[0][i][1])
        if float(hm_dld[0][i][2]) > 120 and float(hm_dld[0][i][2]) <= 240:
            hm_dld_b_num1[5] = hm_dld_b_num1[5] + 1
            hm_dld_j_num1[5] = hm_dld_j_num1[5] + float(hm_dld[0][i][1])
        if float(hm_dld[0][i][2]) > 240 and float(hm_dld[0][i][2]) <= 360:
            hm_dld_b_num1[6] = hm_dld_b_num1[6] + 1
            hm_dld_j_num1[6] = hm_dld_j_num1[6] + float(hm_dld[0][i][1])
        if float(hm_dld[0][i][2]) > 360:
            hm_dld_b_num1[7] = hm_dld_b_num1[7] + 1
            hm_dld_j_num1[7] = hm_dld_j_num1[7] + float(hm_dld[0][i][1])

    for i in range(len(hm_djh[0])):
        if float(hm_djh[0][i][2]) > 0 and float(hm_djh[0][i][2]) <= 12:
            hm_djh_b_num1[0] = hm_djh_b_num1[0] + 1
            hm_djh_j_num1[0] = hm_djh_j_num1[0] + float(hm_djh[0][i][1])
        if float(hm_djh[0][i][2]) > 12 and float(hm_djh[0][i][2]) <= 24:
            hm_djh_b_num1[1] = hm_djh_b_num1[1] + 1
            hm_djh_j_num1[1] = hm_djh_j_num1[1] + float(hm_djh[0][i][1])
        if float(hm_djh[0][i][2]) > 24 and float(hm_djh[0][i][2]) <= 48:
            hm_djh_b_num1[2] = hm_djh_b_num1[2] + 1
            hm_djh_j_num1[2] = hm_djh_j_num1[2] + float(hm_djh[0][i][1])
        if float(hm_djh[0][i][2]) > 48 and float(hm_djh[0][i][2]) <= 72:
            hm_djh_b_num1[3] = hm_djh_b_num1[3] + 1
            hm_djh_j_num1[3] = hm_djh_j_num1[3] + float(hm_djh[0][i][1])
        if float(hm_djh[0][i][2]) > 72 and float(hm_djh[0][i][2]) <= 120:
            hm_djh_b_num1[4] = hm_djh_b_num1[4] + 1
            hm_djh_j_num1[4] = hm_djh_j_num1[4] + float(hm_djh[0][i][1])
        if float(hm_djh[0][i][2]) > 120 and float(hm_djh[0][i][2]) <= 240:
            hm_djh_b_num1[5] = hm_djh_b_num1[5] + 1
            hm_djh_j_num1[5] = hm_djh_j_num1[5] + float(hm_djh[0][i][1])
        if float(hm_djh[0][i][2]) > 240 and float(hm_djh[0][i][2]) <= 360:
            hm_djh_b_num1[6] = hm_djh_b_num1[6] + 1
            hm_djh_j_num1[6] = hm_djh_j_num1[6] + float(hm_djh[0][i][1])
        if float(hm_djh[0][i][2]) > 360:
            hm_djh_b_num1[7] = hm_djh_b_num1[7] + 1
            hm_djh_j_num1[7] = hm_djh_j_num1[7] + float(hm_djh[0][i][1])

    for i in range(len(hm_ddb[0])):
        if float(hm_ddb[0][i][2]) > 0 and float(hm_ddb[0][i][2]) <= 12:
            hm_ddb_b_num1[0] = hm_ddb_b_num1[0] + 1
            hm_ddb_j_num1[0] = hm_ddb_j_num1[0] + float(hm_ddb[0][i][1])
        if float(hm_ddb[0][i][2]) > 12 and float(hm_ddb[0][i][2]) <= 24:
            hm_ddb_b_num1[1] = hm_ddb_b_num1[1] + 1
            hm_ddb_j_num1[1] = hm_ddb_j_num1[1] + float(hm_ddb[0][i][1])
        if float(hm_ddb[0][i][2]) > 24 and float(hm_ddb[0][i][2]) <= 48:
            hm_ddb_b_num1[2] = hm_ddb_b_num1[2] + 1
            hm_ddb_j_num1[2] = hm_ddb_j_num1[2] + float(hm_ddb[0][i][1])
        if float(hm_ddb[0][i][2]) > 48 and float(hm_ddb[0][i][2]) <= 72:
            hm_ddb_b_num1[3] = hm_ddb_b_num1[3] + 1
            hm_ddb_j_num1[3] = hm_ddb_j_num1[3] + float(hm_ddb[0][i][1])
        if float(hm_ddb[0][i][2]) > 72 and float(hm_ddb[0][i][2]) <= 120:
            hm_ddb_b_num1[4] = hm_ddb_b_num1[4] + 1
            hm_ddb_j_num1[4] = hm_ddb_j_num1[4] + float(hm_ddb[0][i][1])
        if float(hm_ddb[0][i][2]) > 120 and float(hm_ddb[0][i][2]) <= 240:
            hm_ddb_b_num1[5] = hm_ddb_b_num1[5] + 1
            hm_ddb_j_num1[5] = hm_ddb_j_num1[5] + float(hm_ddb[0][i][1])
        if float(hm_ddb[0][i][2]) > 240 and float(hm_ddb[0][i][2]) <= 360:
            hm_ddb_b_num1[6] = hm_ddb_b_num1[6] + 1
            hm_ddb_j_num1[6] = hm_ddb_j_num1[6] + float(hm_ddb[0][i][1])
        if float(hm_ddb[0][i][2]) > 360:
            hm_ddb_b_num1[7] = hm_ddb_b_num1[7] + 1
            hm_ddb_j_num1[7] = hm_ddb_j_num1[7] + float(hm_ddb[0][i][1])

    for i in range(len(hm_dck[0])):
        if float(hm_dck[0][i][2]) > 0 and float(hm_dck[0][i][2]) <= 12:
            hm_dck_b_num1[0] = hm_dck_b_num1[0] + 1
            hm_dck_j_num1[0] = hm_dck_j_num1[0] + float(hm_dck[0][i][1])
        if float(hm_dck[0][i][2]) > 12 and float(hm_dck[0][i][2]) <= 24:
            hm_dck_b_num1[1] = hm_dck_b_num1[1] + 1
            hm_dck_j_num1[1] = hm_dck_j_num1[1] + float(hm_dck[0][i][1])
        if float(hm_dck[0][i][2]) > 24 and float(hm_dck[0][i][2]) <= 48:
            hm_dck_b_num1[2] = hm_dck_b_num1[2] + 1
            hm_dck_j_num1[2] = hm_dck_j_num1[2] + float(hm_dck[0][i][1])
        if float(hm_dck[0][i][2]) > 48 and float(hm_dck[0][i][2]) <= 72:
            hm_dck_b_num1[3] = hm_dck_b_num1[3] + 1
            hm_dck_j_num1[3] = hm_dck_j_num1[3] + float(hm_dck[0][i][1])
        if float(hm_dck[0][i][2]) > 72 and float(hm_dck[0][i][2]) <= 120:
            hm_dck_b_num1[4] = hm_dck_b_num1[4] + 1
            hm_dck_j_num1[4] = hm_dck_j_num1[4] + float(hm_dck[0][i][1])
        if float(hm_dck[0][i][2]) > 120 and float(hm_dck[0][i][2]) <= 240:
            hm_dck_b_num1[5] = hm_dck_b_num1[5] + 1
            hm_dck_j_num1[5] = hm_dck_j_num1[5] + float(hm_dck[0][i][1])
        if float(hm_dck[0][i][2]) > 240 and float(hm_dck[0][i][2]) <= 360:
            hm_dck_b_num1[6] = hm_dck_b_num1[6] + 1
            hm_dck_j_num1[6] = hm_dck_j_num1[6] + float(hm_dck[0][i][1])
        if float(hm_dck[0][i][2]) > 360:
            hm_dck_b_num1[7] = hm_dck_b_num1[7] + 1
            hm_dck_j_num1[7] = hm_dck_j_num1[7] + float(hm_dck[0][i][1])

    for i in range(len(tx_djy[0])):
        if float(tx_djy[0][i][2]) > 0 and float(tx_djy[0][i][2]) <= 12:
            tx_djy_b_num1[0] = tx_djy_b_num1[0] + 1
            tx_djy_j_num1[0] = tx_djy_j_num1[0] + float(tx_djy[0][i][1])
        if float(tx_djy[0][i][2]) > 12 and float(tx_djy[0][i][2]) <= 24:
            tx_djy_b_num1[1] = tx_djy_b_num1[1] + 1
            tx_djy_j_num1[1] = tx_djy_j_num1[1] + float(tx_djy[0][i][1])
        if float(tx_djy[0][i][2]) > 24 and float(tx_djy[0][i][2]) <= 48:
            tx_djy_b_num1[2] = tx_djy_b_num1[2] + 1
            tx_djy_j_num1[2] = tx_djy_j_num1[2] + float(tx_djy[0][i][1])
        if float(tx_djy[0][i][2]) > 48 and float(tx_djy[0][i][2]) <= 72:
            tx_djy_b_num1[3] = tx_djy_b_num1[3] + 1
            tx_djy_j_num1[3] = tx_djy_j_num1[3] + float(tx_djy[0][i][1])
        if float(tx_djy[0][i][2]) > 72 and float(tx_djy[0][i][2]) <= 120:
            tx_djy_b_num1[4] = tx_djy_b_num1[4] + 1
            tx_djy_j_num1[4] = tx_djy_j_num1[4] + float(tx_djy[0][i][1])
        if float(tx_djy[0][i][2]) > 120 and float(tx_djy[0][i][2]) <= 240:
            tx_djy_b_num1[5] = tx_djy_b_num1[5] + 1
            tx_djy_j_num1[5] = tx_djy_j_num1[5] + float(tx_djy[0][i][1])
        if float(tx_djy[0][i][2]) > 240 and float(tx_djy[0][i][2]) <= 360:
            tx_djy_b_num1[6] = tx_djy_b_num1[6] + 1
            tx_djy_j_num1[6] = tx_djy_j_num1[6] + float(tx_djy[0][i][1])
        if float(tx_djy[0][i][2]) > 360:
            tx_djy_b_num1[7] = tx_djy_b_num1[7] + 1
            tx_djy_j_num1[7] = tx_djy_j_num1[7] + float(tx_djy[0][i][1])
    for i in range(len(tx_dfpld[0])):
        if float(tx_dfpld[0][i][2]) > 0 and float(tx_dfpld[0][i][2]) <= 12:
            tx_dfpld_b_num1[0] = tx_dfpld_b_num1[0] + 1
            tx_dfpld_j_num1[0] = tx_dfpld_j_num1[0] + float(tx_dfpld[0][i][1])
        if float(tx_dfpld[0][i][2]) > 12 and float(tx_dfpld[0][i][2]) <= 24:
            tx_dfpld_b_num1[1] = tx_dfpld_b_num1[1] + 1
            tx_dfpld_j_num1[1] = tx_dfpld_j_num1[1] + float(tx_dfpld[0][i][1])
        if float(tx_dfpld[0][i][2]) > 24 and float(tx_dfpld[0][i][2]) <= 48:
            tx_dfpld_b_num1[2] = tx_dfpld_b_num1[2] + 1
            tx_dfpld_j_num1[2] = tx_dfpld_j_num1[2] + float(tx_dfpld[0][i][1])
        if float(tx_dfpld[0][i][2]) > 48 and float(tx_dfpld[0][i][2]) <= 72:
            tx_dfpld_b_num1[3] = tx_dfpld_b_num1[3] + 1
            tx_dfpld_j_num1[3] = tx_dfpld_j_num1[3] + float(tx_dfpld[0][i][1])
        if float(tx_dfpld[0][i][2]) > 72 and float(tx_dfpld[0][i][2]) <= 120:
            tx_dfpld_b_num1[4] = tx_dfpld_b_num1[4] + 1
            tx_dfpld_j_num1[4] = tx_dfpld_j_num1[4] + float(tx_dfpld[0][i][1])
        if float(tx_dfpld[0][i][2]) > 120 and float(tx_dfpld[0][i][2]) <= 240:
            tx_dfpld_b_num1[5] = tx_dfpld_b_num1[5] + 1
            tx_dfpld_j_num1[5] = tx_dfpld_j_num1[5] + float(tx_dfpld[0][i][1])
        if float(tx_dfpld[0][i][2]) > 240 and float(tx_dfpld[0][i][2]) <= 360:
            tx_dfpld_b_num1[6] = tx_dfpld_b_num1[6] + 1
            tx_dfpld_j_num1[6] = tx_dfpld_j_num1[6] + float(tx_dfpld[0][i][1])
        if float(tx_dfpld[0][i][2]) > 360:
            tx_dfpld_b_num1[7] = tx_dfpld_b_num1[7] + 1
            tx_dfpld_j_num1[7] = tx_dfpld_j_num1[7] + float(tx_dfpld[0][i][1])
    for i in range(len(tx_dpk[0])):
        if float(tx_dpk[0][i][2]) > 0 and float(tx_dpk[0][i][2]) <= 12:
            tx_dpk_b_num1[0] = tx_dpk_b_num1[0] + 1
            tx_dpk_j_num1[0] = tx_dpk_j_num1[0] + float(tx_dpk[0][i][1])
        if float(tx_dpk[0][i][2]) > 12 and float(tx_dpk[0][i][2]) <= 24:
            tx_dpk_b_num1[1] = tx_dpk_b_num1[1] + 1
            tx_dpk_j_num1[1] = tx_dpk_j_num1[1] + float(tx_dpk[0][i][1])
        if float(tx_dpk[0][i][2]) > 24 and float(tx_dpk[0][i][2]) <= 48:
            tx_dpk_b_num1[2] = tx_dpk_b_num1[2] + 1
            tx_dpk_j_num1[2] = tx_dpk_j_num1[2] + float(tx_dpk[0][i][1])
        if float(tx_dpk[0][i][2]) > 48 and float(tx_dpk[0][i][2]) <= 72:
            tx_dpk_b_num1[3] = tx_dpk_b_num1[3] + 1
            tx_dpk_j_num1[3] = tx_dpk_j_num1[3] + float(tx_dpk[0][i][1])
        if float(tx_dpk[0][i][2]) > 72 and float(tx_dpk[0][i][2]) <= 120:
            tx_dpk_b_num1[4] = tx_dpk_b_num1[4] + 1
            tx_dpk_j_num1[4] = tx_dpk_j_num1[4] + float(tx_dpk[0][i][1])
        if float(tx_dpk[0][i][2]) > 120 and float(tx_dpk[0][i][2]) <= 240:
            tx_dpk_b_num1[5] = tx_dpk_b_num1[5] + 1
            tx_dpk_j_num1[5] = tx_dpk_j_num1[5] + float(tx_dpk[0][i][1])
        if float(tx_dpk[0][i][2]) > 240 and float(tx_dpk[0][i][2]) <= 360:
            tx_dpk_b_num1[6] = tx_dpk_b_num1[6] + 1
            tx_dpk_j_num1[6] = tx_dpk_j_num1[6] + float(tx_dpk[0][i][1])
        if float(tx_dpk[0][i][2]) > 360:
            tx_dpk_b_num1[7] = tx_dpk_b_num1[7] + 1
            tx_dpk_j_num1[7] = tx_dpk_j_num1[7] + float(tx_dpk[0][i][1])

    for i in range(len(tx_dld[0])):
        if float(tx_dld[0][i][2]) > 0 and float(tx_dld[0][i][2]) <= 12:
            tx_dld_b_num1[0] = tx_dld_b_num1[0] + 1
            tx_dld_j_num1[0] = tx_dld_j_num1[0] + float(tx_dld[0][i][1])
        if float(tx_dld[0][i][2]) > 12 and float(tx_dld[0][i][2]) <= 24:
            tx_dld_b_num1[1] = tx_dld_b_num1[1] + 1
            tx_dld_j_num1[1] = tx_dld_j_num1[1] + float(tx_dld[0][i][1])
        if float(tx_dld[0][i][2]) > 24 and float(tx_dld[0][i][2]) <= 48:
            tx_dld_b_num1[2] = tx_dld_b_num1[2] + 1
            tx_dld_j_num1[2] = tx_dld_j_num1[2] + float(tx_dld[0][i][1])
        if float(tx_dld[0][i][2]) > 48 and float(tx_dld[0][i][2]) <= 72:
            tx_dld_b_num1[3] = tx_dld_b_num1[3] + 1
            tx_dld_j_num1[3] = tx_dld_j_num1[3] + float(tx_dld[0][i][1])
        if float(tx_dld[0][i][2]) > 72 and float(tx_dld[0][i][2]) <= 120:
            tx_dld_b_num1[4] = tx_dld_b_num1[4] + 1
            tx_dld_j_num1[4] = tx_dld_j_num1[4] + float(tx_dld[0][i][1])
        if float(tx_dld[0][i][2]) > 120 and float(tx_dld[0][i][2]) <= 240:
            tx_dld_b_num1[5] = tx_dld_b_num1[5] + 1
            tx_dld_j_num1[5] = tx_dld_j_num1[5] + float(tx_dld[0][i][1])
        if float(tx_dld[0][i][2]) > 240 and float(tx_dld[0][i][2]) <= 360:
            tx_dld_b_num1[6] = tx_dld_b_num1[6] + 1
            tx_dld_j_num1[6] = tx_dld_j_num1[6] + float(tx_dld[0][i][1])
        if float(tx_dld[0][i][2]) > 360:
            tx_dld_b_num1[7] = tx_dld_b_num1[7] + 1
            tx_dld_j_num1[7] = tx_dld_j_num1[7] + float(tx_dld[0][i][1])

    for i in range(len(tx_djh[0])):
        if float(tx_djh[0][i][2]) > 0 and float(tx_djh[0][i][2]) <= 12:
            tx_djh_b_num1[0] = tx_djh_b_num1[0] + 1
            tx_djh_j_num1[0] = tx_djh_j_num1[0] + float(tx_djh[0][i][1])
        if float(tx_djh[0][i][2]) > 12 and float(tx_djh[0][i][2]) <= 24:
            tx_djh_b_num1[1] = tx_djh_b_num1[1] + 1
            tx_djh_j_num1[1] = tx_djh_j_num1[1] + float(tx_djh[0][i][1])
        if float(tx_djh[0][i][2]) > 24 and float(tx_djh[0][i][2]) <= 48:
            tx_djh_b_num1[2] = tx_djh_b_num1[2] + 1
            tx_djh_j_num1[2] = tx_djh_j_num1[2] + float(tx_djh[0][i][1])
        if float(tx_djh[0][i][2]) > 48 and float(tx_djh[0][i][2]) <= 72:
            tx_djh_b_num1[3] = tx_djh_b_num1[3] + 1
            tx_djh_j_num1[3] = tx_djh_j_num1[3] + float(tx_djh[0][i][1])
        if float(tx_djh[0][i][2]) > 72 and float(tx_djh[0][i][2]) <= 120:
            tx_djh_b_num1[4] = tx_djh_b_num1[4] + 1
            tx_djh_j_num1[4] = tx_djh_j_num1[4] + float(tx_djh[0][i][1])
        if float(tx_djh[0][i][2]) > 120 and float(tx_djh[0][i][2]) <= 240:
            tx_djh_b_num1[5] = tx_djh_b_num1[5] + 1
            tx_djh_j_num1[5] = tx_djh_j_num1[5] + float(tx_djh[0][i][1])
        if float(tx_djh[0][i][2]) > 240 and float(tx_djh[0][i][2]) <= 360:
            tx_djh_b_num1[6] = tx_djh_b_num1[6] + 1
            tx_djh_j_num1[6] = tx_djh_j_num1[6] + float(tx_djh[0][i][1])
        if float(tx_djh[0][i][2]) > 360:
            tx_djh_b_num1[7] = tx_djh_b_num1[7] + 1
            tx_djh_j_num1[7] = tx_djh_j_num1[7] + float(tx_djh[0][i][1])

    for i in range(len(tx_ddb[0])):
        if float(tx_ddb[0][i][2]) > 0 and float(tx_ddb[0][i][2]) <= 12:
            tx_ddb_b_num1[0] = tx_ddb_b_num1[0] + 1
            tx_ddb_j_num1[0] = tx_ddb_j_num1[0] + float(tx_ddb[0][i][1])
        if float(tx_ddb[0][i][2]) > 12 and float(tx_ddb[0][i][2]) <= 24:
            tx_ddb_b_num1[1] = tx_ddb_b_num1[1] + 1
            tx_ddb_j_num1[1] = tx_ddb_j_num1[1] + float(tx_ddb[0][i][1])
        if float(tx_ddb[0][i][2]) > 24 and float(tx_ddb[0][i][2]) <= 48:
            tx_ddb_b_num1[2] = tx_ddb_b_num1[2] + 1
            tx_ddb_j_num1[2] = tx_ddb_j_num1[2] + float(tx_ddb[0][i][1])
        if float(tx_ddb[0][i][2]) > 48 and float(tx_ddb[0][i][2]) <= 72:
            tx_ddb_b_num1[3] = tx_ddb_b_num1[3] + 1
            tx_ddb_j_num1[3] = tx_ddb_j_num1[3] + float(tx_ddb[0][i][1])
        if float(tx_ddb[0][i][2]) > 72 and float(tx_ddb[0][i][2]) <= 120:
            tx_ddb_b_num1[4] = tx_ddb_b_num1[4] + 1
            tx_ddb_j_num1[4] = tx_ddb_j_num1[4] + float(tx_ddb[0][i][1])
        if float(tx_ddb[0][i][2]) > 120 and float(tx_ddb[0][i][2]) <= 240:
            tx_ddb_b_num1[5] = tx_ddb_b_num1[5] + 1
            tx_ddb_j_num1[5] = tx_ddb_j_num1[5] + float(tx_ddb[0][i][1])
        if float(tx_ddb[0][i][2]) > 240 and float(tx_ddb[0][i][2]) <= 360:
            tx_ddb_b_num1[6] = tx_ddb_b_num1[6] + 1
            tx_ddb_j_num1[6] = tx_ddb_j_num1[6] + float(tx_ddb[0][i][1])
        if float(tx_ddb[0][i][2]) > 360:
            tx_ddb_b_num1[7] = tx_ddb_b_num1[7] + 1
            tx_ddb_j_num1[7] = tx_ddb_j_num1[7] + float(tx_ddb[0][i][1])

    for i in range(len(tx_dck[0])):
        if float(tx_dck[0][i][2]) > 0 and float(tx_dck[0][i][2]) <= 12:
            tx_dck_b_num1[0] = tx_dck_b_num1[0] + 1
            tx_dck_j_num1[0] = tx_dck_j_num1[0] + float(tx_dck[0][i][1])
        if float(tx_dck[0][i][2]) > 12 and float(tx_dck[0][i][2]) <= 24:
            tx_dck_b_num1[1] = tx_dck_b_num1[1] + 1
            tx_dck_j_num1[1] = tx_dck_j_num1[1] + float(tx_dck[0][i][1])
        if float(tx_dck[0][i][2]) > 24 and float(tx_dck[0][i][2]) <= 48:
            tx_dck_b_num1[2] = tx_dck_b_num1[2] + 1
            tx_dck_j_num1[2] = tx_dck_j_num1[2] + float(tx_dck[0][i][1])
        if float(tx_dck[0][i][2]) > 48 and float(tx_dck[0][i][2]) <= 72:
            tx_dck_b_num1[3] = tx_dck_b_num1[3] + 1
            tx_dck_j_num1[3] = tx_dck_j_num1[3] + float(tx_dck[0][i][1])
        if float(tx_dck[0][i][2]) > 72 and float(tx_dck[0][i][2]) <= 120:
            tx_dck_b_num1[4] = tx_dck_b_num1[4] + 1
            tx_dck_j_num1[4] = tx_dck_j_num1[4] + float(tx_dck[0][i][1])
        if float(tx_dck[0][i][2]) > 120 and float(tx_dck[0][i][2]) <= 240:
            tx_dck_b_num1[5] = tx_dck_b_num1[5] + 1
            tx_dck_j_num1[5] = tx_dck_j_num1[5] + float(tx_dck[0][i][1])
        if float(tx_dck[0][i][2]) > 240 and float(tx_dck[0][i][2]) <= 360:
            tx_dck_b_num1[6] = tx_dck_b_num1[6] + 1
            tx_dck_j_num1[6] = tx_dck_j_num1[6] + float(tx_dck[0][i][1])
        if float(tx_dck[0][i][2]) > 360:
            tx_dck_b_num1[7] = tx_dck_b_num1[7] + 1
            tx_dck_j_num1[7] = tx_dck_j_num1[7] + float(tx_dck[0][i][1])

    hm_b_fba_num_12 = np.r_[
        hm_dpk_b_num1[0], hm_dfpld_b_num1[0], hm_dld_b_num1[0], hm_djh_b_num1[0], hm_ddb_b_num1[0], hm_dck_b_num1[0],
        hm_djy_b_num1[0]]

    hm_b_fba_num_24 = np.r_[
        hm_dpk_b_num1[1], hm_dfpld_b_num1[1], hm_dld_b_num1[1], hm_djh_b_num1[1], hm_ddb_b_num1[1], hm_dck_b_num1[1],
        hm_djy_b_num1[1]]
    hm_b_fba_num_48 = np.r_[
        hm_dpk_b_num1[2], hm_dfpld_b_num1[2], hm_dld_b_num1[2], hm_djh_b_num1[2], hm_ddb_b_num1[2], hm_dck_b_num1[2],
        hm_djy_b_num1[2]]
    hm_b_fba_num_72 = np.r_[
        hm_dpk_b_num1[3], hm_dfpld_b_num1[3], hm_dld_b_num1[3], hm_djh_b_num1[3], hm_ddb_b_num1[3], hm_dck_b_num1[3],
        hm_djy_b_num1[3]]
    hm_b_fba_num_120 = np.r_[
        hm_dpk_b_num1[4], hm_dfpld_b_num1[4], hm_dld_b_num1[4], hm_djh_b_num1[4], hm_ddb_b_num1[4], hm_dck_b_num1[4],
        hm_djy_b_num1[4]]
    hm_b_fba_num_240 = np.r_[
        hm_dpk_b_num1[5], hm_dfpld_b_num1[5], hm_dld_b_num1[5], hm_djh_b_num1[5], hm_ddb_b_num1[5], hm_dck_b_num1[5],
        hm_djy_b_num1[5]]
    hm_b_fba_num_360 = np.r_[
        hm_dpk_b_num1[6], hm_dfpld_b_num1[6], hm_dld_b_num1[6], hm_djh_b_num1[6], hm_ddb_b_num1[6], hm_dck_b_num1[6],
        hm_djy_b_num1[6]]
    hm_b_fba_num_361 = np.r_[
        hm_dpk_b_num1[7], hm_dfpld_b_num1[7], hm_dld_b_num1[7], hm_djh_b_num1[7], hm_ddb_b_num1[7], hm_dck_b_num1[7],
        hm_djy_b_num1[7]]
    hm_j_fba_num_12 = np.r_[
        hm_dpk_j_num1[0], hm_dfpld_j_num1[0], hm_dld_j_num1[0], hm_djh_j_num1[0], hm_ddb_j_num1[0], hm_dck_j_num1[0],
        hm_djy_j_num1[0]]

    hm_j_fba_num_24 = np.r_[
        hm_dpk_j_num1[1], hm_dfpld_j_num1[1], hm_dld_j_num1[1], hm_djh_j_num1[1], hm_ddb_j_num1[1], hm_dck_j_num1[1],
        hm_djy_j_num1[1]]
    hm_j_fba_num_48 = np.r_[
        hm_dpk_j_num1[2], hm_dfpld_j_num1[2], hm_dld_j_num1[2], hm_djh_j_num1[2], hm_ddb_j_num1[2], hm_dck_j_num1[2],
        hm_djy_j_num1[2]]
    hm_j_fba_num_72 = np.r_[
        hm_dpk_j_num1[3], hm_dfpld_j_num1[3], hm_dld_j_num1[3], hm_djh_j_num1[3], hm_ddb_j_num1[3], hm_dck_j_num1[3],
        hm_djy_j_num1[3]]
    hm_j_fba_num_120 = np.r_[
        hm_dpk_j_num1[4], hm_dfpld_j_num1[4], hm_dld_j_num1[4], hm_djh_j_num1[4], hm_ddb_j_num1[4], hm_dck_j_num1[4],
        hm_djy_j_num1[4]]
    hm_j_fba_num_240 = np.r_[
        hm_dpk_j_num1[5], hm_dfpld_j_num1[5], hm_dld_j_num1[5], hm_djh_j_num1[5], hm_ddb_j_num1[5], hm_dck_j_num1[5],
        hm_djy_j_num1[5]]
    hm_j_fba_num_360 = np.r_[
        hm_dpk_j_num1[6], hm_dfpld_j_num1[6], hm_dld_j_num1[6], hm_djh_j_num1[6], hm_ddb_j_num1[6], hm_dck_j_num1[6],
        hm_djy_j_num1[6]]
    hm_j_fba_num_361 = np.r_[
        hm_dpk_j_num1[7], hm_dfpld_j_num1[7], hm_dld_j_num1[7], hm_djh_j_num1[7], hm_ddb_j_num1[7], hm_dck_j_num1[7],
        hm_djy_j_num1[7]]

    tx_b_fba_num_12 = np.r_[
        tx_dpk_b_num1[0], tx_dfpld_b_num1[0], tx_dld_b_num1[0], tx_djh_b_num1[0], tx_ddb_b_num1[0], tx_dck_b_num1[0],
        tx_djy_b_num1[0]]

    tx_b_fba_num_24 = np.r_[
        tx_dpk_b_num1[1], tx_dfpld_b_num1[1], tx_dld_b_num1[1], tx_djh_b_num1[1], tx_ddb_b_num1[1], tx_dck_b_num1[1],
        tx_djy_b_num1[1]]
    tx_b_fba_num_48 = np.r_[
        tx_dpk_b_num1[2], tx_dfpld_b_num1[2], tx_dld_b_num1[2], tx_djh_b_num1[2], tx_ddb_b_num1[2], tx_dck_b_num1[2],
        tx_djy_b_num1[2]]
    tx_b_fba_num_72 = np.r_[
        tx_dpk_b_num1[3], tx_dfpld_b_num1[3], tx_dld_b_num1[3], tx_djh_b_num1[3], tx_ddb_b_num1[3], tx_dck_b_num1[3],
        tx_djy_b_num1[3]]
    tx_b_fba_num_120 = np.r_[
        tx_dpk_b_num1[4], tx_dfpld_b_num1[4], tx_dld_b_num1[4], tx_djh_b_num1[4], tx_ddb_b_num1[4], tx_dck_b_num1[4],
        tx_djy_b_num1[4]]
    tx_b_fba_num_240 = np.r_[
        tx_dpk_b_num1[5], tx_dfpld_b_num1[5], tx_dld_b_num1[5], tx_djh_b_num1[5], tx_ddb_b_num1[5], tx_dck_b_num1[5],
        tx_djy_b_num1[5]]
    tx_b_fba_num_360 = np.r_[
        tx_dpk_b_num1[6], tx_dfpld_b_num1[6], tx_dld_b_num1[6], tx_djh_b_num1[6], tx_ddb_b_num1[6], tx_dck_b_num1[6],
        tx_djy_b_num1[6]]
    tx_b_fba_num_361 = np.r_[
        tx_dpk_b_num1[7], tx_dfpld_b_num1[7], tx_dld_b_num1[7], tx_djh_b_num1[7], tx_ddb_b_num1[7], tx_dck_b_num1[7],
        tx_djy_b_num1[7]]
    tx_j_fba_num_12 = np.r_[
        tx_dpk_j_num1[0], tx_dfpld_j_num1[0], tx_dld_j_num1[0], tx_djh_j_num1[0], tx_ddb_j_num1[0], tx_dck_j_num1[0],
        tx_djy_j_num1[0]]

    tx_j_fba_num_24 = np.r_[
        tx_dpk_j_num1[1], tx_dfpld_j_num1[1], tx_dld_j_num1[1], tx_djh_j_num1[1], tx_ddb_j_num1[1], tx_dck_j_num1[1],
        tx_djy_j_num1[1]]
    tx_j_fba_num_48 = np.r_[
        tx_dpk_j_num1[2], tx_dfpld_j_num1[2], tx_dld_j_num1[2], tx_djh_j_num1[2], tx_ddb_j_num1[2], tx_dck_j_num1[2],
        tx_djy_j_num1[2]]
    tx_j_fba_num_72 = np.r_[
        tx_dpk_j_num1[3], tx_dfpld_j_num1[3], tx_dld_j_num1[3], tx_djh_j_num1[3], tx_ddb_j_num1[3], tx_dck_j_num1[3],
        tx_djy_j_num1[3]]
    tx_j_fba_num_120 = np.r_[
        tx_dpk_j_num1[4], tx_dfpld_j_num1[4], tx_dld_j_num1[4], tx_djh_j_num1[4], tx_ddb_j_num1[4], tx_dck_j_num1[4],
        tx_djy_j_num1[4]]
    tx_j_fba_num_240 = np.r_[
        tx_dpk_j_num1[5], tx_dfpld_j_num1[5], tx_dld_j_num1[5], tx_djh_j_num1[5], tx_ddb_j_num1[5], tx_dck_j_num1[5],
        tx_djy_j_num1[5]]
    tx_j_fba_num_360 = np.r_[
        tx_dpk_j_num1[6], tx_dfpld_j_num1[6], tx_dld_j_num1[6], tx_djh_j_num1[6], tx_ddb_j_num1[6], tx_dck_j_num1[6],
        tx_djy_j_num1[6]]
    tx_j_fba_num_361 = np.r_[
        tx_dpk_j_num1[7], tx_dfpld_j_num1[7], tx_dld_j_num1[7], tx_djh_j_num1[7], tx_ddb_j_num1[7], tx_dck_j_num1[7],
        tx_djy_j_num1[7]]

    arrayA = np.divide(hm_b_fba_num_12, max(hm_b_fba_num_12), out=np.zeros_like(hm_b_fba_num_12, dtype=np.float64),
                       where=max(hm_b_fba_num_12) != 0)
    for i in range(len(hm_b_fba_num_12)):
        hm_b_12.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_fba_num_12[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_fba_num_12)):
            hm_b_fba_num_12[i] = '{:.2%}'.format(a)

    arrayA = np.divide(hm_j_fba_num_12, max(hm_j_fba_num_12), out=np.zeros_like(hm_j_fba_num_12, dtype=np.float64),
                       where=max(hm_j_fba_num_12) != 0)
    for i in range(len(hm_j_fba_num_12)):
        hm_j_12.append("%.2f%%" % (arrayA[i] * 100))
    if hm_j_fba_num_12[0] == 'nan%':
        a = 0
        for i in range(len(hm_j_fba_num_12)):
            hm_j_fba_num_12[i] = '{:.2%}'.format(a)
    print(hm_j_12)
    arrayA = np.divide(hm_b_fba_num_24, max(hm_b_fba_num_24), out=np.zeros_like(hm_b_fba_num_24, dtype=np.float64),
                       where=max(hm_b_fba_num_24) != 0)
    for i in range(len(hm_b_fba_num_24)):
        hm_b_24.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_fba_num_24[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_fba_num_24)):
            hm_b_fba_num_24[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_j_fba_num_24, max(hm_j_fba_num_24), out=np.zeros_like(hm_j_fba_num_24, dtype=np.float64),
                       where=max(hm_j_fba_num_24) != 0)
    for i in range(len(hm_j_fba_num_24)):
        hm_j_24.append("%.2f%%" % (arrayA[i] * 100))
    if hm_j_fba_num_24[0] == 'nan%':
        a = 0
        for i in range(len(hm_j_fba_num_24)):
            hm_j_fba_num_24[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_b_fba_num_48, max(hm_b_fba_num_48), out=np.zeros_like(hm_b_fba_num_48, dtype=np.float64),
                       where=max(hm_b_fba_num_48) != 0)
    for i in range(len(hm_b_fba_num_48)):
        hm_b_48.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_fba_num_48[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_fba_num_48)):
            hm_b_fba_num_48[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_j_fba_num_48, max(hm_j_fba_num_48), out=np.zeros_like(hm_j_fba_num_48, dtype=np.float64),
                       where=max(hm_j_fba_num_48) != 0)
    for i in range(len(hm_j_fba_num_48)):
        hm_j_48.append("%.2f%%" % (arrayA[i] * 100))
    if hm_j_fba_num_48[0] == 'nan%':
        a = 0
        for i in range(len(hm_j_fba_num_48)):
            hm_j_fba_num_48[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_b_fba_num_72, max(hm_b_fba_num_72), out=np.zeros_like(hm_b_fba_num_72, dtype=np.float64),
                       where=max(hm_b_fba_num_72) != 0)
    for i in range(len(hm_b_fba_num_72)):
        hm_b_72.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_fba_num_72[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_fba_num_72)):
            hm_b_fba_num_72[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_j_fba_num_72, max(hm_j_fba_num_72), out=np.zeros_like(hm_j_fba_num_72, dtype=np.float64),
                       where=max(hm_j_fba_num_72) != 0)
    for i in range(len(hm_j_fba_num_72)):
        hm_j_72.append("%.2f%%" % (arrayA[i] * 100))
    if hm_j_fba_num_72[0] == 'nan%':
        a = 0
        for i in range(len(hm_j_fba_num_72)):
            hm_j_fba_num_72[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_b_fba_num_120, max(hm_b_fba_num_120), out=np.zeros_like(hm_b_fba_num_120, dtype=np.float64),
                       where=max(hm_b_fba_num_120) != 0)
    for i in range(len(hm_b_fba_num_120)):
        hm_b_120.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_fba_num_120[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_fba_num_120)):
            hm_b_fba_num_120[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_j_fba_num_120, max(hm_j_fba_num_120), out=np.zeros_like(hm_j_fba_num_120, dtype=np.float64),
                       where=max(hm_j_fba_num_120) != 0)
    for i in range(len(hm_j_fba_num_120)):
        hm_j_120.append("%.2f%%" % (arrayA[i] * 100))
    if hm_j_fba_num_120[0] == 'nan%':
        a = 0
        for i in range(len(hm_j_fba_num_120)):
            hm_j_fba_num_120[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_b_fba_num_240, max(hm_b_fba_num_240), out=np.zeros_like(hm_b_fba_num_240, dtype=np.float64),
                       where=max(hm_b_fba_num_240) != 0)
    for i in range(len(hm_b_fba_num_240)):
        hm_b_240.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_fba_num_240[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_fba_num_240)):
            hm_b_fba_num_240[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_j_fba_num_240, max(hm_j_fba_num_240), out=np.zeros_like(hm_j_fba_num_240, dtype=np.float64),
                       where=max(hm_j_fba_num_240) != 0)
    for i in range(len(hm_j_fba_num_240)):
        hm_j_240.append("%.2f%%" % (arrayA[i] * 100))
    if hm_j_fba_num_240[0] == 'nan%':
        a = 0
        for i in range(len(hm_j_fba_num_240)):
            hm_j_fba_num_240[i] = '{:.2%}'.format(a)  # print(hm_j_240)
    arrayA = np.divide(hm_b_fba_num_360, max(hm_b_fba_num_360), out=np.zeros_like(hm_b_fba_num_360, dtype=np.float64),
                       where=max(hm_b_fba_num_360) != 0)
    for i in range(len(hm_b_fba_num_360)):
        hm_b_360.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_fba_num_360[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_fba_num_360)):
            hm_b_fba_num_360[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_j_fba_num_360, max(hm_j_fba_num_360), out=np.zeros_like(hm_j_fba_num_360, dtype=np.float64),
                       where=max(hm_j_fba_num_360) != 0)
    for i in range(len(hm_j_fba_num_360)):
        hm_j_360.append("%.2f%%" % (arrayA[i] * 100))
    if hm_j_fba_num_360[0] == 'nan%':
        a = 0
        for i in range(len(hm_j_fba_num_360)):
            hm_j_fba_num_360[i] = '{:.2%}'.format(a)

    arrayA = np.divide(hm_b_fba_num_361, max(hm_b_fba_num_361), out=np.zeros_like(hm_b_fba_num_361, dtype=np.float64),
                       where=max(hm_b_fba_num_361) != 0)
    for i in range(len(hm_b_fba_num_361)):
        hm_b_361.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_fba_num_361[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_fba_num_361)):
            hm_b_fba_num_361[i] = '{:.2%}'.format(a)
    # print(hm_b_361)
    arrayA = np.divide(hm_j_fba_num_361, max(hm_j_fba_num_361), out=np.zeros_like(hm_j_fba_num_361, dtype=np.float64),
                       where=max(hm_j_fba_num_361) != 0)
    for i in range(len(hm_j_fba_num_361)):
        hm_j_361.append("%.2f%%" % (arrayA[i] * 100))
    if hm_j_fba_num_361[0] == 'nan%':
        a = 0
        for i in range(len(hm_j_fba_num_361)):
            hm_j_fba_num_361[i] = '{:.2%}'.format(a)
    # print(hm_j_361)
    arrayA = np.divide(tx_b_fba_num_12, max(tx_b_fba_num_12), out=np.zeros_like(tx_b_fba_num_12, dtype=np.float64),
                       where=max(tx_b_fba_num_12) != 0)
    for i in range(len(tx_b_fba_num_12)):
        tx_b_12.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_fba_num_12[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_fba_num_12)):
            tx_b_fba_num_12[i] = '{:.2%}'.format(a)
    # print(tx_b_12)
    arrayA = np.divide(tx_j_fba_num_12, max(tx_j_fba_num_12), out=np.zeros_like(tx_j_fba_num_12, dtype=np.float64),
                       where=max(tx_j_fba_num_12) != 0)
    for i in range(len(tx_j_fba_num_12)):
        tx_j_12.append("%.2f%%" % (arrayA[i] * 100))
    if tx_j_fba_num_12[0] == 'nan%':
        a = 0
        for i in range(len(tx_j_fba_num_12)):
            tx_j_fba_num_12[i] = '{:.2%}'.format(a)
    # print(tx_j_12)
    arrayA = np.divide(tx_b_fba_num_24, max(tx_b_fba_num_24), out=np.zeros_like(tx_b_fba_num_24, dtype=np.float64),
                       where=max(tx_b_fba_num_24) != 0)
    for i in range(len(tx_b_fba_num_24)):
        tx_b_24.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_fba_num_24[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_fba_num_24)):
            tx_b_fba_num_24[i] = '{:.2%}'.format(a)
    # print(tx_b_24)
    arrayA = np.divide(tx_j_fba_num_24, max(tx_j_fba_num_24), out=np.zeros_like(tx_j_fba_num_24, dtype=np.float64),
                       where=max(tx_j_fba_num_24) != 0)
    for i in range(len(tx_j_fba_num_24)):
        tx_j_24.append("%.2f%%" % (arrayA[i] * 100))
    if tx_j_fba_num_24[0] == 'nan%':
        a = 0
        for i in range(len(tx_j_fba_num_24)):
            tx_j_fba_num_24[i] = '{:.2%}'.format(a)
    # print(tx_j_24)
    arrayA = np.divide(tx_b_fba_num_48, max(tx_b_fba_num_48), out=np.zeros_like(tx_b_fba_num_48, dtype=np.float64),
                       where=max(tx_b_fba_num_48) != 0)
    for i in range(len(tx_b_fba_num_48)):
        tx_b_48.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_fba_num_48[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_fba_num_48)):
            tx_b_fba_num_48[i] = '{:.2%}'.format(a)
    # print(tx_b_48)
    arrayA = np.divide(tx_j_fba_num_48, max(tx_j_fba_num_48), out=np.zeros_like(tx_j_fba_num_48, dtype=np.float64),
                       where=max(tx_j_fba_num_48) != 0)
    for i in range(len(tx_j_fba_num_48)):
        tx_j_48.append("%.2f%%" % (arrayA[i] * 100))
    if tx_j_fba_num_48[0] == 'nan%':
        a = 0
        for i in range(len(tx_j_fba_num_48)):
            tx_j_fba_num_48[i] = '{:.2%}'.format(a)
    # print(tx_j_48)
    arrayA = np.divide(tx_b_fba_num_72, max(tx_b_fba_num_72), out=np.zeros_like(tx_b_fba_num_72, dtype=np.float64),
                       where=max(tx_b_fba_num_72) != 0)
    for i in range(len(tx_b_fba_num_72)):
        tx_b_72.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_fba_num_72[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_fba_num_72)):
            tx_b_fba_num_72[i] = '{:.2%}'.format(a)
    # print(tx_b_72)
    arrayA = np.divide(tx_j_fba_num_72, max(tx_j_fba_num_72), out=np.zeros_like(tx_j_fba_num_72, dtype=np.float64),
                       where=max(tx_j_fba_num_72) != 0)
    for i in range(len(tx_j_fba_num_72)):
        tx_j_72.append("%.2f%%" % (arrayA[i] * 100))
    if tx_j_fba_num_72[0] == 'nan%':
        a = 0
        for i in range(len(tx_j_fba_num_72)):
            tx_j_fba_num_72[i] = '{:.2%}'.format(a)
    # print(tx_j_72)
    arrayA = np.divide(tx_b_fba_num_120, max(tx_b_fba_num_120), out=np.zeros_like(tx_b_fba_num_120, dtype=np.float64),
                       where=max(tx_b_fba_num_120) != 0)
    for i in range(len(tx_b_fba_num_120)):
        tx_b_120.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_fba_num_120[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_fba_num_120)):
            tx_b_fba_num_120[i] = '{:.2%}'.format(a)
    # print(tx_b_120)
    arrayA = np.divide(tx_j_fba_num_120, max(tx_j_fba_num_120), out=np.zeros_like(tx_j_fba_num_120, dtype=np.float64),
                       where=max(tx_j_fba_num_120) != 0)
    for i in range(len(tx_j_fba_num_120)):
        tx_j_120.append("%.2f%%" % (arrayA[i] * 100))
    if tx_j_fba_num_120[0] == 'nan%':
        a = 0
        for i in range(len(tx_j_fba_num_120)):
            tx_j_fba_num_120[i] = '{:.2%}'.format(a)
    # print(tx_j_120)
    arrayA = np.divide(tx_b_fba_num_240, max(tx_b_fba_num_240), out=np.zeros_like(tx_b_fba_num_240, dtype=np.float64),
                       where=max(tx_b_fba_num_240) != 0)
    for i in range(len(tx_b_fba_num_240)):
        tx_b_240.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_fba_num_240[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_fba_num_240)):
            tx_b_fba_num_240[i] = '{:.2%}'.format(a)
    # print(tx_b_240)
    arrayA = np.divide(tx_j_fba_num_240, max(tx_j_fba_num_240), out=np.zeros_like(tx_j_fba_num_240, dtype=np.float64),
                       where=max(tx_j_fba_num_240) != 0)
    for i in range(len(tx_j_fba_num_240)):
        tx_j_240.append("%.2f%%" % (arrayA[i] * 100))
    if tx_j_fba_num_240[0] == 'nan%':
        a = 0
        for i in range(len(tx_j_fba_num_240)):
            tx_j_fba_num_240[i] = '{:.2%}'.format(a)
    # print(tx_j_240)
    arrayA = np.divide(tx_b_fba_num_360, max(tx_b_fba_num_360), out=np.zeros_like(tx_b_fba_num_360, dtype=np.float64),
                       where=max(tx_b_fba_num_360) != 0)
    for i in range(len(tx_b_fba_num_360)):
        tx_b_360.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_fba_num_360[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_fba_num_360)):
            tx_b_fba_num_360[i] = '{:.2%}'.format(a)
    # print(tx_b_360)
    arrayA = np.divide(tx_j_fba_num_360, max(tx_j_fba_num_360), out=np.zeros_like(tx_j_fba_num_360, dtype=np.float64),
                       where=max(tx_j_fba_num_360) != 0)
    for i in range(len(tx_j_fba_num_360)):
        tx_j_360.append("%.2f%%" % (arrayA[i] * 100))
    if tx_j_fba_num_360[0] == 'nan%':
        a = 0
        for i in range(len(tx_j_fba_num_360)):
            tx_j_fba_num_360[i] = '{:.2%}'.format(a)
    # print(tx_j_360)    cur.execute(sql)
    arrayA = np.divide(tx_b_fba_num_361, max(tx_b_fba_num_361), out=np.zeros_like(tx_b_fba_num_361, dtype=np.float64),
                       where=max(tx_b_fba_num_361) != 0)
    for i in range(len(tx_b_fba_num_361)):
        tx_b_361.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_fba_num_361[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_fba_num_361)):
            tx_b_fba_num_361[i] = '{:.2%}'.format(a)
    # print(tx_b_361)
    arrayA = np.divide(tx_j_fba_num_361, max(tx_j_fba_num_361), out=np.zeros_like(tx_j_fba_num_361, dtype=np.float64),
                       where=max(tx_j_fba_num_361) != 0)
    for i in range(len(tx_j_fba_num_361)):
        tx_j_361.append("%.2f%%" % (arrayA[i] * 100))
    if tx_j_fba_num_361[0] == 'nan%':
        a = 0
        for i in range(len(tx_j_fba_num_361)):
            tx_j_fba_num_361[i] = '{:.2%}'.format(a)
    # print(tx_j_361)


    warehouse = []
    type = []
    num = []
    time = []
    storage = []
    jsonData = {}
    for data in see:
        warehouse.append(data[0])
        type.append(data[5])
        num.append(data[4])
        time.append(data[6])
        storage.append(data[2])
    hm_type = []
    hm_num = []
    hm_time = []
    hm_storage = []
    tx_type = []
    tx_num = []
    tx_time = []
    tx_storage = []
    for i in range(len(warehouse)):
        if warehouse[i] == 'HM_AA':
            hm_type.append(type[i])
            hm_num.append(num[i])
            hm_time.append(time[i])
            hm_storage.append(storage[i])
    for i in range(len(warehouse)):
        if warehouse[i] == 'SZ_AA':
            tx_type.append(type[i])
            tx_num.append(num[i])
            tx_time.append(time[i])
            tx_storage.append(storage[i])

    hm_data = np.dstack((hm_type, hm_num, hm_time, hm_storage))
    tx_data = np.dstack((tx_type, tx_num, tx_time, tx_storage))

    hm_drk_b_num = []
    hm_drk_j_num = []
    hm_drk_time = []

    hm_dtm_b_num = []
    hm_dtm_j_num = []
    hm_dtm_time = []

    hm_dgnzj_b_num = []
    hm_dgnzj_j_num = []
    hm_dgnzj_time = []

    hm_dsj_b_num = []
    hm_dsj_j_num = []
    hm_dsj_time = []

    hm_sjz_b_num = []
    hm_sjz_j_num = []
    hm_sjz_time = []

    tx_drk_b_num = []
    tx_drk_j_num = []
    tx_drk_time = []

    tx_dtm_b_num = []
    tx_dtm_j_num = []
    tx_dtm_time = []

    tx_dgnzj_b_num = []
    tx_dgnzj_j_num = []
    tx_dgnzj_time = []

    tx_dsj_b_num = []
    tx_dsj_j_num = []
    tx_dsj_time = []

    tx_sjz_b_num = []
    tx_sjz_j_num = []
    tx_sjz_time = []

    hm_data_shelf = np.vstack((hm_storage, hm_time, hm_type)).T
    hm_data_shelf = hm_data_shelf[np.argsort(-hm_data_shelf[:, 1])]
    tx_data_shelf = np.vstack((tx_storage, tx_time, tx_type)).T
    tx_data_shelf = tx_data_shelf[np.argsort(-tx_data_shelf[:, 1])]

    hm_drk_shelf = []
    hm_drk_shelf_time = []
    hm_dtm_shelf = []
    hm_dtm_shelf_time = []
    hm_dgnzj_shelf = []
    hm_dgnzj_shelf_time = []
    hm_dsj_shelf = []
    hm_dsj_shelf_time = []
    hm_sjz_shelf = []
    hm_sjz_shelf_time = []

    tx_drk_shelf = []
    tx_drk_shelf_time = []
    tx_dtm_shelf = []
    tx_dtm_shelf_time = []
    tx_dgnzj_shelf = []
    tx_dgnzj_shelf_time = []
    tx_dsj_shelf = []
    tx_dsj_shelf_time = []
    tx_sjz_shelf = []
    tx_sjz_shelf_time = []
    for i in range(len(hm_data_shelf)):
        if (hm_data_shelf[i][2] == 'DRK'):
            hm_drk_shelf.append(hm_data_shelf[i][0])
            hm_drk_shelf_time.append(hm_data_shelf[i][1])
    hm_drk_all = np.dstack((hm_drk_shelf, hm_drk_shelf_time))

    for i in range(len(hm_data_shelf)):
        if (hm_data_shelf[i][2] == 'DTM'):
            hm_dtm_shelf.append(hm_data_shelf[i][0])
            hm_dtm_shelf_time.append(hm_data_shelf[i][1])
    hm_dtm_all = np.dstack((hm_dtm_shelf, hm_dtm_shelf_time))

    for i in range(len(hm_data_shelf)):
        if (hm_data_shelf[i][2] == 'DGNZJ'):
            hm_dgnzj_shelf.append(hm_data_shelf[i][0])
            hm_dgnzj_shelf_time.append(hm_data_shelf[i][1])
    hm_dgnzj_all = np.dstack((hm_dgnzj_shelf, hm_dgnzj_shelf_time))

    for i in range(len(hm_data_shelf)):
        if (hm_data_shelf[i][2] == 'DSJ'):
            hm_dsj_shelf.append(hm_data_shelf[i][0])
            hm_dsj_shelf_time.append(hm_data_shelf[i][1])
    hm_dsj_all = np.dstack((hm_dsj_shelf, hm_dsj_shelf_time))

    for i in range(len(hm_data_shelf)):
        if (hm_data_shelf[i][2] == 'SJZ'):
            hm_sjz_shelf.append(hm_data_shelf[i][0])
            hm_sjz_shelf_time.append(hm_data_shelf[i][1])
    hm_sjz_all = np.dstack((hm_sjz_shelf, hm_sjz_shelf_time))

    for i in range(len(tx_data_shelf)):
        if (tx_data_shelf[i][2] == 'DRK'):
            tx_drk_shelf.append(tx_data_shelf[i][0])
            tx_drk_shelf_time.append(tx_data_shelf[i][1])
    tx_drk_all = np.dstack((tx_drk_shelf, tx_drk_shelf_time))

    for i in range(len(tx_data_shelf)):
        if (tx_data_shelf[i][2] == 'DTM'):
            tx_dtm_shelf.append(tx_data_shelf[i][0])
            tx_dtm_shelf_time.append(tx_data_shelf[i][1])
    tx_dtm_all = np.dstack((tx_dtm_shelf, tx_dtm_shelf_time))

    for i in range(len(tx_data_shelf)):
        if (tx_data_shelf[i][2] == 'DGNZJ'):
            tx_dgnzj_shelf.append(tx_data_shelf[i][0])
            tx_dgnzj_shelf_time.append(tx_data_shelf[i][1])
    tx_dgnzj_all = np.dstack((tx_dgnzj_shelf, tx_dgnzj_shelf_time))

    for i in range(len(tx_data_shelf)):
        if (tx_data_shelf[i][2] == 'DSJ'):
            tx_dsj_shelf.append(tx_data_shelf[i][0])
            tx_dsj_shelf_time.append(tx_data_shelf[i][1])
    tx_dsj_all = np.dstack((tx_dsj_shelf, tx_dsj_shelf_time))

    for i in range(len(tx_data_shelf)):
        if (tx_data_shelf[i][2] == 'SJZ'):
            tx_sjz_shelf.append(tx_data_shelf[i][0])
            tx_sjz_shelf_time.append(tx_data_shelf[i][1])
    tx_sjz_all = np.dstack((tx_sjz_shelf, tx_sjz_shelf_time))

    ###数组去重
    #########################################################
    a1 = []
    a2 = []
    tx_drk_shelf = []
    tx_drk_shelf_time = []
    for i in range(len(tx_drk_all[0])):
        if tx_drk_all[0][i][0] not in a2:
            a1.append(tx_drk_all[0][i])
        a2.append(tx_drk_all[0][i][0])
    for i in range(len(a1)):
        tx_drk_shelf.append(a1[i][0])
        tx_drk_shelf_time.append(a1[i][1])
    #########################################################
    a1 = []
    a2 = []
    tx_dtm_shelf = []
    tx_dtm_shelf_time = []
    for i in range(len(tx_dtm_all[0])):
        if tx_dtm_all[0][i][0] not in a2:
            a1.append(tx_dtm_all[0][i])
        a2.append(tx_dtm_all[0][i][0])
    for i in range(len(a1)):
        tx_dtm_shelf.append(a1[i][0])
        tx_dtm_shelf_time.append(a1[i][1])
    #########################################################
    a1 = []
    a2 = []
    tx_dgnzj_shelf = []
    tx_dgnzj_shelf_time = []
    for i in range(len(tx_dgnzj_all[0])):
        if tx_dgnzj_all[0][i][0] not in a2:
            a1.append(tx_dgnzj_all[0][i])
        a2.append(tx_dgnzj_all[0][i][0])
    for i in range(len(a1)):
        tx_dgnzj_shelf.append(a1[i][0])
        tx_dgnzj_shelf_time.append(a1[i][1])
    #########################################################
    a1 = []
    a2 = []
    tx_dsj_shelf = []
    tx_dsj_shelf_time = []
    for i in range(len(tx_dsj_all[0])):
        if tx_dsj_all[0][i][0] not in a2:
            a1.append(tx_dsj_all[0][i])
        a2.append(tx_dsj_all[0][i][0])
    for i in range(len(a1)):
        tx_dsj_shelf.append(a1[i][0])
        tx_dsj_shelf_time.append(a1[i][1])
    #########################################################
    a1 = []
    a2 = []
    tx_sjz_shelf = []
    tx_sjz_shelf_time = []
    for i in range(len(tx_sjz_all[0])):
        if tx_sjz_all[0][i][0] not in a2:
            a1.append(tx_sjz_all[0][i])
        a2.append(tx_sjz_all[0][i][0])
    for i in range(len(a1)):
        tx_sjz_shelf.append(a1[i][0])
        tx_sjz_shelf_time.append(a1[i][1])

    tx_drk_shelf_num = np.r_[tx_drk_shelf_time[0:10]]
    tx_dtm_shelf_num = np.r_[tx_dtm_shelf_time[0:10]]
    tx_dgnzj_shelf_num = np.r_[tx_dgnzj_shelf_time[0:10]]
    tx_dsj_shelf_num = np.r_[tx_dsj_shelf_time[0:10]]
    tx_sjz_shelf_num = np.r_[tx_sjz_shelf_time[0:10]]
    tx_drk_shelf_num1 = []
    tx_dtm_shelf_num1 = []
    tx_dgnzj_shelf_num1 = []
    tx_dsj_shelf_num1 = []
    tx_sjz_shelf_num1 = []

    for i in range(len(tx_drk_shelf_num)):
        a = tx_drk_shelf_num[i] / max(tx_drk_shelf_num)
        tx_drk_shelf_num1.append('{:.2%}'.format(a))

    for i in range(len(tx_dtm_shelf_num)):
        a = tx_dtm_shelf_num[i] / max(tx_dtm_shelf_num)
        tx_dtm_shelf_num1.append('{:.2%}'.format(a))

    for i in range(len(tx_dgnzj_shelf_num)):
        a = tx_dgnzj_shelf_num[i] / max(tx_dgnzj_shelf_num)
        tx_dgnzj_shelf_num1.append('{:.2%}'.format(a))

    for i in range(len(tx_dsj_shelf_num)):
        a = tx_dsj_shelf_num[i] / max(tx_dsj_shelf_num)
        tx_dsj_shelf_num1.append('{:.2%}'.format(a))

    for i in range(len(tx_sjz_shelf_num)):
        a = tx_sjz_shelf_num[i] / max(tx_sjz_shelf_num)
        tx_sjz_shelf_num1.append('{:.2%}'.format(a))

    a1 = []
    a2 = []
    hm_drk_shelf = []
    hm_drk_shelf_time = []
    for i in range(len(hm_drk_all[0])):
        if hm_drk_all[0][i][0] not in a2:
            a1.append(hm_drk_all[0][i])
        a2.append(hm_drk_all[0][i][0])
    for i in range(len(a1)):
        hm_drk_shelf.append(a1[i][0])
        hm_drk_shelf_time.append(a1[i][1])
    #########################################################
    a1 = []
    a2 = []
    hm_dtm_shelf = []
    hm_dtm_shelf_time = []
    for i in range(len(hm_dtm_all[0])):
        if hm_dtm_all[0][i][0] not in a2:
            a1.append(hm_dtm_all[0][i])
        a2.append(hm_dtm_all[0][i][0])
    for i in range(len(a1)):
        hm_dtm_shelf.append(a1[i][0])
        hm_dtm_shelf_time.append(a1[i][1])
    #########################################################
    a1 = []
    a2 = []
    hm_dgnzj_shelf = []
    hm_dgnzj_shelf_time = []
    for i in range(len(hm_dgnzj_all[0])):
        if hm_dgnzj_all[0][i][0] not in a2:
            a1.append(hm_dgnzj_all[0][i])
        a2.append(hm_dgnzj_all[0][i][0])
    for i in range(len(a1)):
        hm_dgnzj_shelf.append(a1[i][0])
        hm_dgnzj_shelf_time.append(a1[i][1])
    #########################################################
    a1 = []
    a2 = []
    hm_dsj_shelf = []
    hm_dsj_shelf_time = []
    for i in range(len(hm_dsj_all[0])):
        if hm_dsj_all[0][i][0] not in a2:
            a1.append(hm_dsj_all[0][i])
        a2.append(hm_dsj_all[0][i][0])
    for i in range(len(a1)):
        hm_dsj_shelf.append(a1[i][0])
        hm_dsj_shelf_time.append(a1[i][1])
    #########################################################
    a1 = []
    a2 = []
    hm_sjz_shelf = []
    hm_sjz_shelf_time = []
    for i in range(len(hm_sjz_all[0])):
        if hm_sjz_all[0][i][0] not in a2:
            a1.append(hm_sjz_all[0][i])
        a2.append(hm_sjz_all[0][i][0])
    for i in range(len(a1)):
        hm_sjz_shelf.append(a1[i][0])
        hm_sjz_shelf_time.append(a1[i][1])

    hm_drk_shelf_num = np.r_[hm_drk_shelf_time[0:10]]
    hm_dtm_shelf_num = np.r_[hm_dtm_shelf_time[0:10]]
    hm_dgnzj_shelf_num = np.r_[hm_dgnzj_shelf_time[0:10]]
    hm_dsj_shelf_num = np.r_[hm_dsj_shelf_time[0:10]]
    hm_sjz_shelf_num = np.r_[hm_sjz_shelf_time[0:10]]
    hm_drk_shelf_num1 = []
    hm_dtm_shelf_num1 = []
    hm_dgnzj_shelf_num1 = []
    hm_dsj_shelf_num1 = []
    hm_sjz_shelf_num1 = []

    for i in range(len(hm_drk_shelf_num)):
        a = hm_drk_shelf_num[i] / max(hm_drk_shelf_num)
        hm_drk_shelf_num1.append('{:.2%}'.format(a))

    for i in range(len(hm_dtm_shelf_num)):
        a = hm_dtm_shelf_num[i] / max(hm_dtm_shelf_num)
        hm_dtm_shelf_num1.append('{:.2%}'.format(a))

    for i in range(len(hm_dgnzj_shelf_num)):
        a = hm_dgnzj_shelf_num[i] / max(hm_dgnzj_shelf_num)
        hm_dgnzj_shelf_num1.append('{:.2%}'.format(a))

    for i in range(len(hm_dsj_shelf_num)):
        a = hm_dsj_shelf_num[i] / max(hm_dsj_shelf_num)
        hm_dsj_shelf_num1.append('{:.2%}'.format(a))

    for i in range(len(hm_sjz_shelf_num)):
        a = hm_sjz_shelf_num[i] / max(hm_sjz_shelf_num)
        hm_sjz_shelf_num1.append('{:.2%}'.format(a))

    for i in range(len(hm_time)):
        if (hm_data[0][i][0] == 'DRK'):
            hm_drk_b_num.append(1)
            hm_drk_j_num.append(hm_data[0][i][1])
            hm_drk_time.append(hm_data[0][i][2])
    for i in range(len(hm_time)):
        if (hm_data[0][i][0] == 'DTM'):
            hm_dtm_b_num.append(1)
            hm_dtm_j_num.append(hm_data[0][i][1])
            hm_dtm_time.append(hm_data[0][i][2])
    for i in range(len(hm_time)):
        if (hm_data[0][i][0] == 'DGNZJ'):
            hm_dgnzj_b_num.append(1)
            hm_dgnzj_j_num.append(hm_data[0][i][1])
            hm_dgnzj_time.append(hm_data[0][i][2])
    for i in range(len(hm_time)):
        if (hm_data[0][i][0] == 'DSJ'):
            hm_dsj_b_num.append(1)
            hm_dsj_j_num.append(hm_data[0][i][1])
            hm_dsj_time.append(hm_data[0][i][2])
    for i in range(len(hm_time)):
        if (hm_data[0][i][0] == 'SJZ'):
            hm_sjz_b_num.append(1)
            hm_sjz_j_num.append(hm_data[0][i][1])
            hm_sjz_time.append(hm_data[0][i][2])

    for i in range(len(tx_time)):
        if (tx_data[0][i][0] == 'DRK'):
            tx_drk_b_num.append(1)
            tx_drk_j_num.append(tx_data[0][i][1])
            tx_drk_time.append(tx_data[0][i][2])
    for i in range(len(tx_time)):
        if (tx_data[0][i][0] == 'DTM'):
            tx_dtm_b_num.append(1)
            tx_dtm_j_num.append(tx_data[0][i][1])
            tx_dtm_time.append(tx_data[0][i][2])
    for i in range(len(tx_time)):
        if (tx_data[0][i][0] == 'DGNZJ'):
            tx_dgnzj_b_num.append(1)
            tx_dgnzj_j_num.append(tx_data[0][i][1])
            tx_dgnzj_time.append(tx_data[0][i][2])
    for i in range(len(tx_time)):
        if (tx_data[0][i][0] == 'DSJ'):
            tx_dsj_b_num.append(1)
            tx_dsj_j_num.append(tx_data[0][i][1])
            tx_dsj_time.append(tx_data[0][i][2])
    for i in range(len(tx_time)):
        if (tx_data[0][i][0] == 'SJZ'):
            tx_sjz_b_num.append(1)
            tx_sjz_j_num.append(tx_data[0][i][1])
            tx_sjz_time.append(tx_data[0][i][2])

    hm_drk = np.dstack((hm_drk_b_num, hm_drk_j_num, hm_drk_time))
    hm_dtm = np.dstack((hm_dtm_b_num, hm_dtm_j_num, hm_dtm_time))
    hm_dgnzj = np.dstack((hm_dgnzj_b_num, hm_dgnzj_j_num, hm_dgnzj_time))
    hm_dsj = np.dstack((hm_dsj_b_num, hm_dsj_j_num, hm_dsj_time))
    hm_sjz = np.dstack((hm_sjz_b_num, hm_sjz_j_num, hm_sjz_time))

    tx_drk = np.dstack((tx_drk_b_num, tx_drk_j_num, tx_drk_time))
    tx_dtm = np.dstack((tx_dtm_b_num, tx_dtm_j_num, tx_dtm_time))
    tx_dgnzj = np.dstack((tx_dgnzj_b_num, tx_dgnzj_j_num, tx_dgnzj_time))
    tx_dsj = np.dstack((tx_dsj_b_num, tx_dsj_j_num, tx_dsj_time))
    tx_sjz = np.dstack((tx_sjz_b_num, tx_sjz_j_num, tx_sjz_time))

    hm_drk_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_dtm_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_dgnzj_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_dsj_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_sjz_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]

    tx_drk_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_dtm_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_dgnzj_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_dsj_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_sjz_b_num1 = [0, 0, 0, 0, 0, 0, 0, 0]

    hm_drk_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_dtm_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_dgnzj_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_dsj_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    hm_sjz_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]

    tx_drk_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_dtm_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_dgnzj_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_dsj_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]
    tx_sjz_j_num1 = [0, 0, 0, 0, 0, 0, 0, 0]

    for i in range(len(hm_drk[0])):
        if float(hm_drk[0][i][2]) > 0 and float(hm_drk[0][i][2]) <= 6:
            hm_drk_b_num1[0] = hm_drk_b_num1[0] + 1
            hm_drk_j_num1[0] = hm_drk_j_num1[0] + hm_drk[0][i][1]
        if float(hm_drk[0][i][2]) > 6 and float(hm_drk[0][i][2]) <= 12:
            hm_drk_b_num1[1] = hm_drk_b_num1[1] + 1
            hm_drk_j_num1[1] = hm_drk_j_num1[1] + hm_drk[0][i][1]
        if float(hm_drk[0][i][2]) > 12 and float(hm_drk[0][i][2]) <= 24:
            hm_drk_b_num1[2] = hm_drk_b_num1[2] + 1
            hm_drk_j_num1[2] = hm_drk_j_num1[2] + hm_drk[0][i][1]
        if float(hm_drk[0][i][2]) > 24 and float(hm_drk[0][i][2]) <= 36:
            hm_drk_b_num1[3] = hm_drk_b_num1[3] + 1
            hm_drk_j_num1[3] = hm_drk_j_num1[3] + hm_drk[0][i][1]
        if float(hm_drk[0][i][2]) > 36 and float(hm_drk[0][i][2]) <= 48:
            hm_drk_b_num1[4] = hm_drk_b_num1[4] + 1
            hm_drk_j_num1[4] = hm_drk_j_num1[4] + hm_drk[0][i][1]
        if float(hm_drk[0][i][2]) > 48 and float(hm_drk[0][i][2]) <= 72:
            hm_drk_b_num1[5] = hm_drk_b_num1[5] + 1
            hm_drk_j_num1[5] = hm_drk_j_num1[5] + hm_drk[0][i][1]
        if float(hm_drk[0][i][2]) > 72 and float(hm_drk[0][i][2]) <= 96:
            hm_drk_b_num1[6] = hm_drk_b_num1[6] + 1
            hm_drk_j_num1[6] = hm_drk_j_num1[6] + hm_drk[0][i][1]
        if float(hm_drk[0][i][2]) > 96:
            hm_drk_b_num1[7] = hm_drk_b_num1[7] + 1
            hm_drk_j_num1[7] = hm_drk_j_num1[7] + hm_drk[0][i][1]

    for i in range(len(hm_dtm[0])):
        if float(hm_dtm[0][i][2]) > 0 and float(hm_dtm[0][i][2]) <= 6:
            hm_dtm_b_num1[0] = hm_dtm_b_num1[0] + 1
            hm_dtm_j_num1[0] = hm_dtm_j_num1[0] + hm_dtm[0][i][1]
        if float(hm_dtm[0][i][2]) > 6 and float(hm_dtm[0][i][2]) <= 12:
            hm_dtm_b_num1[1] = hm_dtm_b_num1[1] + 1
            hm_dtm_j_num1[1] = hm_dtm_j_num1[1] + hm_dtm[0][i][1]
        if float(hm_dtm[0][i][2]) > 12 and float(hm_dtm[0][i][2]) <= 24:
            hm_dtm_b_num1[2] = hm_dtm_b_num1[2] + 1
            hm_dtm_j_num1[2] = hm_dtm_j_num1[2] + hm_dtm[0][i][1]
        if float(hm_dtm[0][i][2]) > 24 and float(hm_dtm[0][i][2]) <= 36:
            hm_dtm_b_num1[3] = hm_dtm_b_num1[3] + 1
            hm_dtm_j_num1[3] = hm_dtm_j_num1[3] + hm_dtm[0][i][1]
        if float(hm_dtm[0][i][2]) > 36 and float(hm_dtm[0][i][2]) <= 48:
            hm_dtm_b_num1[4] = hm_dtm_b_num1[4] + 1
            hm_dtm_j_num1[4] = hm_dtm_j_num1[4] + hm_dtm[0][i][1]
        if float(hm_dtm[0][i][2]) > 48 and float(hm_dtm[0][i][2]) <= 72:
            hm_dtm_b_num1[5] = hm_dtm_b_num1[5] + 1
            hm_dtm_j_num1[5] = hm_dtm_j_num1[5] + hm_dtm[0][i][1]
        if float(hm_dtm[0][i][2]) > 72 and float(hm_dtm[0][i][2]) <= 96:
            hm_dtm_b_num1[6] = hm_dtm_b_num1[6] + 1
            hm_dtm_j_num1[6] = hm_dtm_j_num1[6] + hm_dtm[0][i][1]
        if float(hm_dtm[0][i][2]) > 96:
            hm_dtm_b_num1[7] = hm_dtm_b_num1[7] + 1
            hm_dtm_j_num1[7] = hm_dtm_j_num1[7] + hm_dtm[0][i][1]

    for i in range(len(hm_dgnzj[0])):
        if float(hm_dgnzj[0][i][2]) > 0 and float(hm_dgnzj[0][i][2]) <= 6:
            hm_dgnzj_b_num1[0] = hm_dgnzj_b_num1[0] + 1
            hm_dgnzj_j_num1[0] = hm_dgnzj_j_num1[0] + hm_dgnzj[0][i][1]
        if float(hm_dgnzj[0][i][2]) > 6 and float(hm_dgnzj[0][i][2]) <= 12:
            hm_dgnzj_b_num1[1] = hm_dgnzj_b_num1[1] + 1
            hm_dgnzj_j_num1[1] = hm_dgnzj_j_num1[1] + hm_dgnzj[0][i][1]
        if float(hm_dgnzj[0][i][2]) > 12 and float(hm_dgnzj[0][i][2]) <= 24:
            hm_dgnzj_b_num1[2] = hm_dgnzj_b_num1[2] + 1
            hm_dgnzj_j_num1[2] = hm_dgnzj_j_num1[2] + hm_dgnzj[0][i][1]
        if float(hm_dgnzj[0][i][2]) > 24 and float(hm_dgnzj[0][i][2]) <= 36:
            hm_dgnzj_b_num1[3] = hm_dgnzj_b_num1[3] + 1
            hm_dgnzj_j_num1[3] = hm_dgnzj_j_num1[3] + hm_dgnzj[0][i][1]
        if float(hm_dgnzj[0][i][2]) > 36 and float(hm_dgnzj[0][i][2]) <= 48:
            hm_dgnzj_b_num1[4] = hm_dgnzj_b_num1[4] + 1
            hm_dgnzj_j_num1[4] = hm_dgnzj_j_num1[4] + hm_dgnzj[0][i][1]
        if float(hm_dgnzj[0][i][2]) > 48 and float(hm_dgnzj[0][i][2]) <= 72:
            hm_dgnzj_b_num1[5] = hm_dgnzj_b_num1[5] + 1
            hm_dgnzj_j_num1[5] = hm_dgnzj_j_num1[5] + hm_dgnzj[0][i][1]
        if float(hm_dgnzj[0][i][2]) > 72 and float(hm_dgnzj[0][i][2]) <= 96:
            hm_dgnzj_b_num1[6] = hm_dgnzj_b_num1[6] + 1
            hm_dgnzj_j_num1[6] = hm_dgnzj_j_num1[6] + hm_dgnzj[0][i][1]
        if float(hm_dgnzj[0][i][2]) > 96:
            hm_dgnzj_b_num1[7] = hm_dgnzj_b_num1[7] + 1
            hm_dgnzj_j_num1[7] = hm_dgnzj_j_num1[7] + hm_dgnzj[0][i][1]

    for i in range(len(hm_dsj[0])):
        if float(hm_dsj[0][i][2]) > 0 and float(hm_dsj[0][i][2]) <= 6:
            hm_dsj_b_num1[0] = hm_dsj_b_num1[0] + 1
            hm_dsj_j_num1[0] = hm_dsj_j_num1[0] + hm_dsj[0][i][1]
        if float(hm_dsj[0][i][2]) > 6 and float(hm_dsj[0][i][2]) <= 12:
            hm_dsj_b_num1[1] = hm_dsj_b_num1[1] + 1
            hm_dsj_j_num1[1] = hm_dsj_j_num1[1] + hm_dsj[0][i][1]
        if float(hm_dsj[0][i][2]) > 12 and float(hm_dsj[0][i][2]) <= 24:
            hm_dsj_b_num1[2] = hm_dsj_b_num1[2] + 1
            hm_dsj_j_num1[2] = hm_dsj_j_num1[2] + hm_dsj[0][i][1]
        if float(hm_dsj[0][i][2]) > 24 and float(hm_dsj[0][i][2]) <= 36:
            hm_dsj_b_num1[3] = hm_dsj_b_num1[3] + 1
            hm_dsj_j_num1[3] = hm_dsj_j_num1[3] + hm_dsj[0][i][1]
        if float(hm_dsj[0][i][2]) > 36 and float(hm_dsj[0][i][2]) <= 48:
            hm_dsj_b_num1[4] = hm_dsj_b_num1[4] + 1
            hm_dsj_j_num1[4] = hm_dsj_j_num1[4] + hm_dsj[0][i][1]
        if float(hm_dsj[0][i][2]) > 48 and float(hm_dsj[0][i][2]) <= 72:
            hm_dsj_b_num1[5] = hm_dsj_b_num1[5] + 1
            hm_dsj_j_num1[5] = hm_dsj_j_num1[5] + hm_dsj[0][i][1]
        if float(hm_dsj[0][i][2]) > 72 and float(hm_dsj[0][i][2]) <= 96:
            hm_dsj_b_num1[6] = hm_dsj_b_num1[6] + 1
            hm_dsj_j_num1[6] = hm_dsj_j_num1[6] + hm_dsj[0][i][1]
        if float(hm_dsj[0][i][2]) > 96:
            hm_dsj_b_num1[7] = hm_dsj_b_num1[7] + 1
            hm_dsj_j_num1[7] = hm_dsj_j_num1[7] + hm_dsj[0][i][1]

    for i in range(len(hm_sjz[0])):
        if float(hm_sjz[0][i][2]) > 0 and float(hm_sjz[0][i][2]) <= 6:
            hm_sjz_b_num1[0] = hm_sjz_b_num1[0] + 1
            hm_sjz_j_num1[0] = hm_sjz_j_num1[0] + hm_sjz[0][i][1]
        if float(hm_sjz[0][i][2]) > 6 and float(hm_sjz[0][i][2]) <= 12:
            hm_sjz_b_num1[1] = hm_sjz_b_num1[1] + 1
            hm_sjz_j_num1[1] = hm_sjz_j_num1[1] + hm_sjz[0][i][1]
        if float(hm_sjz[0][i][2]) > 12 and float(hm_sjz[0][i][2]) <= 24:
            hm_sjz_b_num1[2] = hm_sjz_b_num1[2] + 1
            hm_sjz_j_num1[2] = hm_sjz_j_num1[2] + hm_sjz[0][i][1]
        if float(hm_sjz[0][i][2]) > 24 and float(hm_sjz[0][i][2]) <= 36:
            hm_sjz_b_num1[3] = hm_sjz_b_num1[3] + 1
            hm_sjz_j_num1[3] = hm_sjz_j_num1[3] + hm_sjz[0][i][1]
        if float(hm_sjz[0][i][2]) > 36 and float(hm_sjz[0][i][2]) <= 48:
            hm_sjz_b_num1[4] = hm_sjz_b_num1[4] + 1
            hm_sjz_j_num1[4] = hm_sjz_j_num1[4] + hm_sjz[0][i][1]
        if float(hm_sjz[0][i][2]) > 48 and float(hm_sjz[0][i][2]) <= 72:
            hm_sjz_b_num1[5] = hm_sjz_b_num1[5] + 1
            hm_sjz_j_num1[5] = hm_sjz_j_num1[5] + hm_sjz[0][i][1]
        if float(hm_sjz[0][i][2]) > 72 and float(hm_sjz[0][i][2]) <= 96:
            hm_sjz_b_num1[6] = hm_sjz_b_num1[6] + 1
            hm_sjz_j_num1[6] = hm_sjz_j_num1[6] + hm_sjz[0][i][1]
        if float(hm_sjz[0][i][2]) > 96:
            hm_sjz_b_num1[7] = hm_sjz_b_num1[7] + 1
            hm_sjz_j_num1[7] = hm_sjz_j_num1[7] + hm_sjz[0][i][1]

    for i in range(len(tx_drk[0])):
        if float(tx_drk[0][i][2]) > 0 and float(tx_drk[0][i][2]) <= 6:
            tx_drk_b_num1[0] = tx_drk_b_num1[0] + 1
            tx_drk_j_num1[0] = tx_drk_j_num1[0] + tx_drk[0][i][1]
        if float(tx_drk[0][i][2]) > 6 and float(tx_drk[0][i][2]) <= 12:
            tx_drk_b_num1[1] = tx_drk_b_num1[1] + 1
            tx_drk_j_num1[1] = tx_drk_j_num1[1] + tx_drk[0][i][1]
        if float(tx_drk[0][i][2]) > 12 and float(tx_drk[0][i][2]) <= 24:
            tx_drk_b_num1[2] = tx_drk_b_num1[2] + 1
            tx_drk_j_num1[2] = tx_drk_j_num1[2] + tx_drk[0][i][1]
        if float(tx_drk[0][i][2]) > 24 and float(tx_drk[0][i][2]) <= 36:
            tx_drk_b_num1[3] = tx_drk_b_num1[3] + 1
            tx_drk_j_num1[3] = tx_drk_j_num1[3] + tx_drk[0][i][1]
        if float(tx_drk[0][i][2]) > 36 and float(tx_drk[0][i][2]) <= 48:
            tx_drk_b_num1[4] = tx_drk_b_num1[4] + 1
            tx_drk_j_num1[4] = tx_drk_j_num1[4] + tx_drk[0][i][1]
        if float(tx_drk[0][i][2]) > 48 and float(tx_drk[0][i][2]) <= 72:
            tx_drk_b_num1[5] = tx_drk_b_num1[5] + 1
            tx_drk_j_num1[5] = tx_drk_j_num1[5] + tx_drk[0][i][1]
        if float(tx_drk[0][i][2]) > 72 and float(tx_drk[0][i][2]) <= 96:
            tx_drk_b_num1[6] = tx_drk_b_num1[6] + 1
            tx_drk_j_num1[6] = tx_drk_j_num1[6] + tx_drk[0][i][1]
        if float(tx_drk[0][i][2]) > 96:
            tx_drk_b_num1[7] = tx_drk_b_num1[7] + 1
            tx_drk_j_num1[7] = tx_drk_j_num1[7] + tx_drk[0][i][1]

    for i in range(len(tx_dtm[0])):
        if float(tx_dtm[0][i][2]) > 0 and float(tx_dtm[0][i][2]) <= 6:
            tx_dtm_b_num1[0] = tx_dtm_b_num1[0] + 1
            tx_dtm_j_num1[0] = tx_dtm_j_num1[0] + tx_dtm[0][i][1]
        if float(tx_dtm[0][i][2]) > 6 and float(tx_dtm[0][i][2]) <= 12:
            tx_dtm_b_num1[1] = tx_dtm_b_num1[1] + 1
            tx_dtm_j_num1[1] = tx_dtm_j_num1[1] + tx_dtm[0][i][1]
        if float(tx_dtm[0][i][2]) > 12 and float(tx_dtm[0][i][2]) <= 24:
            tx_dtm_b_num1[2] = tx_dtm_b_num1[2] + 1
            tx_dtm_j_num1[2] = tx_dtm_j_num1[2] + tx_dtm[0][i][1]
        if float(tx_dtm[0][i][2]) > 24 and float(tx_dtm[0][i][2]) <= 36:
            tx_dtm_b_num1[3] = tx_dtm_b_num1[3] + 1
            tx_dtm_j_num1[3] = tx_dtm_j_num1[3] + tx_dtm[0][i][1]
        if float(tx_dtm[0][i][2]) > 36 and float(tx_dtm[0][i][2]) <= 48:
            tx_dtm_b_num1[4] = tx_dtm_b_num1[4] + 1
            tx_dtm_j_num1[4] = tx_dtm_j_num1[4] + tx_dtm[0][i][1]
        if float(tx_dtm[0][i][2]) > 48 and float(tx_dtm[0][i][2]) <= 72:
            tx_dtm_b_num1[5] = tx_dtm_b_num1[5] + 1
            tx_dtm_j_num1[5] = tx_dtm_j_num1[5] + tx_dtm[0][i][1]
        if float(tx_dtm[0][i][2]) > 72 and float(tx_dtm[0][i][2]) <= 96:
            tx_dtm_b_num1[6] = tx_dtm_b_num1[6] + 1
            tx_dtm_j_num1[6] = tx_dtm_j_num1[6] + tx_dtm[0][i][1]
        if float(tx_dtm[0][i][2]) > 96:
            tx_dtm_b_num1[7] = tx_dtm_b_num1[7] + 1
            tx_dtm_j_num1[7] = tx_dtm_j_num1[7] + tx_dtm[0][i][1]

    for i in range(len(tx_dgnzj[0])):
        if float(tx_dgnzj[0][i][2]) > 0 and float(tx_dgnzj[0][i][2]) <= 6:
            tx_dgnzj_b_num1[0] = tx_dgnzj_b_num1[0] + 1
            tx_dgnzj_j_num1[0] = tx_dgnzj_j_num1[0] + tx_dgnzj[0][i][1]
        if float(tx_dgnzj[0][i][2]) > 6 and float(tx_dgnzj[0][i][2]) <= 12:
            tx_dgnzj_b_num1[1] = tx_dgnzj_b_num1[1] + 1
            tx_dgnzj_j_num1[1] = tx_dgnzj_j_num1[1] + tx_dgnzj[0][i][1]
        if float(tx_dgnzj[0][i][2]) > 12 and float(tx_dgnzj[0][i][2]) <= 24:
            tx_dgnzj_b_num1[2] = tx_dgnzj_b_num1[2] + 1
            tx_dgnzj_j_num1[2] = tx_dgnzj_j_num1[2] + tx_dgnzj[0][i][1]
        if float(tx_dgnzj[0][i][2]) > 24 and float(tx_dgnzj[0][i][2]) <= 36:
            tx_dgnzj_b_num1[3] = tx_dgnzj_b_num1[3] + 1
            tx_dgnzj_j_num1[3] = tx_dgnzj_j_num1[3] + tx_dgnzj[0][i][1]
        if float(tx_dgnzj[0][i][2]) > 36 and float(tx_dgnzj[0][i][2]) <= 48:
            tx_dgnzj_b_num1[4] = tx_dgnzj_b_num1[4] + 1
            tx_dgnzj_j_num1[4] = tx_dgnzj_j_num1[4] + tx_dgnzj[0][i][1]
        if float(tx_dgnzj[0][i][2]) > 48 and float(tx_dgnzj[0][i][2]) <= 72:
            tx_dgnzj_b_num1[5] = tx_dgnzj_b_num1[5] + 1
            tx_dgnzj_j_num1[5] = tx_dgnzj_j_num1[5] + tx_dgnzj[0][i][1]
        if float(tx_dgnzj[0][i][2]) > 72 and float(tx_dgnzj[0][i][2]) <= 96:
            tx_dgnzj_b_num1[6] = tx_dgnzj_b_num1[6] + 1
            tx_dgnzj_j_num1[6] = tx_dgnzj_j_num1[6] + tx_dgnzj[0][i][1]
        if float(tx_dgnzj[0][i][2]) > 96:
            tx_dgnzj_b_num1[7] = tx_dgnzj_b_num1[7] + 1
            tx_dgnzj_j_num1[7] = tx_dgnzj_j_num1[7] + tx_dgnzj[0][i][1]

    for i in range(len(tx_dsj[0])):
        if float(tx_dsj[0][i][2]) > 0 and float(tx_dsj[0][i][2]) <= 6:
            tx_dsj_b_num1[0] = tx_dsj_b_num1[0] + 1
            tx_dsj_j_num1[0] = tx_dsj_j_num1[0] + tx_dsj[0][i][1]
        if float(tx_dsj[0][i][2]) > 6 and float(tx_dsj[0][i][2]) <= 12:
            tx_dsj_b_num1[1] = tx_dsj_b_num1[1] + 1
            tx_dsj_j_num1[1] = tx_dsj_j_num1[1] + tx_dsj[0][i][1]
        if float(tx_dsj[0][i][2]) > 12 and float(tx_dsj[0][i][2]) <= 24:
            tx_dsj_b_num1[2] = tx_dsj_b_num1[2] + 1
            tx_dsj_j_num1[2] = tx_dsj_j_num1[2] + tx_dsj[0][i][1]
        if float(tx_dsj[0][i][2]) > 24 and float(tx_dsj[0][i][2]) <= 36:
            tx_dsj_b_num1[3] = tx_dsj_b_num1[3] + 1
            tx_dsj_j_num1[3] = tx_dsj_j_num1[3] + tx_dsj[0][i][1]
        if float(tx_dsj[0][i][2]) > 36 and float(tx_dsj[0][i][2]) <= 48:
            tx_dsj_b_num1[4] = tx_dsj_b_num1[4] + 1
            tx_dsj_j_num1[4] = tx_dsj_j_num1[4] + tx_dsj[0][i][1]
        if float(tx_dsj[0][i][2]) > 48 and float(tx_dsj[0][i][2]) <= 72:
            tx_dsj_b_num1[5] = tx_dsj_b_num1[5] + 1
            tx_dsj_j_num1[5] = tx_dsj_j_num1[5] + tx_dsj[0][i][1]
        if float(tx_dsj[0][i][2]) > 72 and float(tx_dsj[0][i][2]) <= 96:
            tx_dsj_b_num1[6] = tx_dsj_b_num1[6] + 1
            tx_dsj_j_num1[6] = tx_dsj_j_num1[6] + tx_dsj[0][i][1]
        if float(tx_dsj[0][i][2]) > 96:
            tx_dsj_b_num1[7] = tx_dsj_b_num1[7] + 1
            tx_dsj_j_num1[7] = tx_dsj_j_num1[7] + tx_dsj[0][i][1]

    for i in range(len(tx_sjz[0])):
        if float(tx_sjz[0][i][2]) > 0 and float(tx_sjz[0][i][2]) <= 6:
            tx_sjz_b_num1[0] = tx_sjz_b_num1[0] + 1
            tx_sjz_j_num1[0] = tx_sjz_j_num1[0] + tx_sjz[0][i][1]
        if float(tx_sjz[0][i][2]) > 6 and float(tx_sjz[0][i][2]) <= 12:
            tx_sjz_b_num1[1] = tx_sjz_b_num1[1] + 1
            tx_sjz_j_num1[1] = tx_sjz_j_num1[1] + tx_sjz[0][i][1]
        if float(tx_sjz[0][i][2]) > 12 and float(tx_sjz[0][i][2]) <= 24:
            tx_sjz_b_num1[2] = tx_sjz_b_num1[2] + 1
            tx_sjz_j_num1[2] = tx_sjz_j_num1[2] + tx_sjz[0][i][1]
        if float(tx_sjz[0][i][2]) > 24 and float(tx_sjz[0][i][2]) <= 36:
            tx_sjz_b_num1[3] = tx_sjz_b_num1[3] + 1
            tx_sjz_j_num1[3] = tx_sjz_j_num1[3] + tx_sjz[0][i][1]
        if float(tx_sjz[0][i][2]) > 36 and float(tx_sjz[0][i][2]) <= 48:
            tx_sjz_b_num1[4] = tx_sjz_b_num1[4] + 1
            tx_sjz_j_num1[4] = tx_sjz_j_num1[4] + tx_sjz[0][i][1]
        if float(tx_sjz[0][i][2]) > 48 and float(tx_sjz[0][i][2]) <= 72:
            tx_sjz_b_num1[5] = tx_sjz_b_num1[5] + 1
            tx_sjz_j_num1[5] = tx_sjz_j_num1[5] + tx_sjz[0][i][1]
        if float(tx_sjz[0][i][2]) > 72 and float(tx_sjz[0][i][2]) <= 96:
            tx_sjz_b_num1[6] = tx_sjz_b_num1[6] + 1
            tx_sjz_j_num1[6] = tx_sjz_j_num1[6] + tx_sjz[0][i][1]
        if float(tx_sjz[0][i][2]) > 96:
            tx_sjz_b_num1[7] = tx_sjz_b_num1[7] + 1
            tx_sjz_j_num1[7] = tx_sjz_j_num1[7] + tx_sjz[0][i][1]

    hm_b_num_6 = np.r_[
        hm_drk_b_num1[0], hm_dtm_b_num1[0], hm_dgnzj_b_num1[0], hm_dsj_b_num1[0], hm_sjz_b_num1[0]]
    hm_b_num_12 = np.r_[
        hm_drk_b_num1[1], hm_dtm_b_num1[1], hm_dgnzj_b_num1[1], hm_dsj_b_num1[1], hm_sjz_b_num1[1]]
    hm_b_num_24 = np.r_[
        hm_drk_b_num1[2], hm_dtm_b_num1[2], hm_dgnzj_b_num1[2], hm_dsj_b_num1[2], hm_sjz_b_num1[2]]
    hm_b_num_36 = np.r_[
        hm_drk_b_num1[3], hm_dtm_b_num1[3], hm_dgnzj_b_num1[3], hm_dsj_b_num1[3], hm_sjz_b_num1[3]]
    hm_b_num_48 = np.r_[
        hm_drk_b_num1[4], hm_dtm_b_num1[4], hm_dgnzj_b_num1[4], hm_dsj_b_num1[4], hm_sjz_b_num1[4]]
    hm_b_num_72 = np.r_[
        hm_drk_b_num1[5], hm_dtm_b_num1[5], hm_dgnzj_b_num1[5], hm_dsj_b_num1[5], hm_sjz_b_num1[5]]
    hm_b_num_96 = np.r_[
        hm_drk_b_num1[6], hm_dtm_b_num1[6], hm_dgnzj_b_num1[6], hm_dsj_b_num1[6], hm_sjz_b_num1[6]]
    hm_b_num_96_ = np.r_[
        hm_drk_b_num1[7], hm_dtm_b_num1[7], hm_dgnzj_b_num1[7], hm_dsj_b_num1[7], hm_sjz_b_num1[7]]
    hm_j_num_6 = np.r_[
        hm_drk_j_num1[0], hm_dtm_j_num1[0], hm_dgnzj_j_num1[0], hm_dsj_j_num1[0], hm_sjz_j_num1[0]]
    hm_j_num_12 = np.r_[
        hm_drk_j_num1[1], hm_dtm_j_num1[1], hm_dgnzj_j_num1[1], hm_dsj_j_num1[1], hm_sjz_j_num1[1]]
    hm_j_num_24 = np.r_[
        hm_drk_j_num1[2], hm_dtm_j_num1[2], hm_dgnzj_j_num1[2], hm_dsj_j_num1[2], hm_sjz_j_num1[2]]
    hm_j_num_36 = np.r_[
        hm_drk_j_num1[3], hm_dtm_j_num1[3], hm_dgnzj_j_num1[3], hm_dsj_j_num1[3], hm_sjz_j_num1[3]]
    hm_j_num_48 = np.r_[
        hm_drk_j_num1[4], hm_dtm_j_num1[4], hm_dgnzj_j_num1[4], hm_dsj_j_num1[4], hm_sjz_j_num1[4]]
    hm_j_num_72 = np.r_[
        hm_drk_j_num1[5], hm_dtm_j_num1[5], hm_dgnzj_j_num1[5], hm_dsj_j_num1[5], hm_sjz_j_num1[5]]
    hm_j_num_96 = np.r_[
        hm_drk_j_num1[6], hm_dtm_j_num1[6], hm_dgnzj_j_num1[6], hm_dsj_j_num1[6], hm_sjz_j_num1[6]]
    hm_j_num_96_ = np.r_[
        hm_drk_j_num1[7], hm_dtm_j_num1[7], hm_dgnzj_j_num1[7], hm_dsj_j_num1[7], hm_sjz_j_num1[7]]
    tx_b_num_6 = np.r_[
        tx_drk_b_num1[0], tx_dtm_b_num1[0], tx_dgnzj_b_num1[0], tx_dsj_b_num1[0], tx_sjz_b_num1[0]]
    tx_b_num_12 = np.r_[
        tx_drk_b_num1[1], tx_dtm_b_num1[1], tx_dgnzj_b_num1[1], tx_dsj_b_num1[1], tx_sjz_b_num1[1]]
    tx_b_num_24 = np.r_[
        tx_drk_b_num1[2], tx_dtm_b_num1[2], tx_dgnzj_b_num1[2], tx_dsj_b_num1[2], tx_sjz_b_num1[2]]
    tx_b_num_36 = np.r_[
        tx_drk_b_num1[3], tx_dtm_b_num1[3], tx_dgnzj_b_num1[3], tx_dsj_b_num1[3], tx_sjz_b_num1[3]]
    tx_b_num_48 = np.r_[
        tx_drk_b_num1[4], tx_dtm_b_num1[4], tx_dgnzj_b_num1[4], tx_dsj_b_num1[4], tx_sjz_b_num1[4]]
    tx_b_num_72 = np.r_[
        tx_drk_b_num1[5], tx_dtm_b_num1[5], tx_dgnzj_b_num1[5], tx_dsj_b_num1[5], tx_sjz_b_num1[5]]
    tx_b_num_96 = np.r_[
        tx_drk_b_num1[6], tx_dtm_b_num1[6], tx_dgnzj_b_num1[6], tx_dsj_b_num1[6], tx_sjz_b_num1[6]]
    tx_b_num_96_ = np.r_[
        tx_drk_b_num1[7], tx_dtm_b_num1[7], tx_dgnzj_b_num1[7], tx_dsj_b_num1[7], tx_sjz_b_num1[7]]
    tx_j_num_6 = np.r_[
        tx_drk_j_num1[0], tx_dtm_j_num1[0], tx_dgnzj_j_num1[0], tx_dsj_j_num1[0], tx_sjz_j_num1[0]]
    tx_j_num_12 = np.r_[
        tx_drk_j_num1[1], tx_dtm_j_num1[1], tx_dgnzj_j_num1[1], tx_dsj_j_num1[1], tx_sjz_j_num1[1]]
    tx_j_num_24 = np.r_[
        tx_drk_j_num1[2], tx_dtm_j_num1[2], tx_dgnzj_j_num1[2], tx_dsj_j_num1[2], tx_sjz_j_num1[2]]
    tx_j_num_36 = np.r_[
        tx_drk_j_num1[3], tx_dtm_j_num1[3], tx_dgnzj_j_num1[3], tx_dsj_j_num1[3], tx_sjz_j_num1[3]]
    tx_j_num_48 = np.r_[
        tx_drk_j_num1[4], tx_dtm_j_num1[4], tx_dgnzj_j_num1[4], tx_dsj_j_num1[4], tx_sjz_j_num1[4]]
    tx_j_num_72 = np.r_[
        tx_drk_j_num1[5], tx_dtm_j_num1[5], tx_dgnzj_j_num1[5], tx_dsj_j_num1[5], tx_sjz_j_num1[5]]
    tx_j_num_96 = np.r_[
        tx_drk_j_num1[6], tx_dtm_j_num1[6], tx_dgnzj_j_num1[6], tx_dsj_j_num1[6], tx_sjz_j_num1[6]]
    tx_j_num_96_ = np.r_[
        tx_drk_j_num1[7], tx_dtm_j_num1[7], tx_dgnzj_j_num1[7], tx_dsj_j_num1[7], tx_sjz_j_num1[7]]

    hm_b_p_6 = []
    hm_b_p_12 = []
    hm_b_p_24 = []
    hm_b_p_36 = []
    hm_b_p_48 = []
    hm_b_p_72 = []
    hm_b_p_96 = []
    hm_b_p_96_ = []

    hm_j_p_6 = []
    hm_j_p_12 = []
    hm_j_p_24 = []
    hm_j_p_36 = []
    hm_j_p_48 = []
    hm_j_p_72 = []
    hm_j_p_96 = []
    hm_j_p_96_ = []

    tx_b_p_6 = []
    tx_b_p_12 = []
    tx_b_p_24 = []
    tx_b_p_36 = []
    tx_b_p_48 = []
    tx_b_p_72 = []
    tx_b_p_96 = []
    tx_b_p_96_ = []

    tx_j_p_6 = []
    tx_j_p_12 = []
    tx_j_p_24 = []
    tx_j_p_36 = []
    tx_j_p_48 = []
    tx_j_p_72 = []
    tx_j_p_96 = []
    tx_j_p_96_ = []

    arrayA = np.divide(hm_b_num_6, max(hm_b_num_6), out=np.zeros_like(hm_b_num_6, dtype=np.float64), casting="unsafe",
                       where=max(hm_b_num_6) != 0)
    for i in range(len(hm_b_num_6)):
        hm_b_p_6.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_p_6[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_p_6)):
            hm_b_p_6[i] = '{:.2%}'.format(a)

    arrayA = np.divide(hm_b_num_12, max(hm_b_num_12), out=np.zeros_like(hm_b_num_12, dtype=np.float64),
                       casting="unsafe", where=max(hm_b_num_12) != 0)
    for i in range(len(hm_b_num_12)):
        hm_b_p_12.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_p_12[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_p_12)):
            hm_b_p_12[i] = '{:.2%}'.format(a)

    arrayA = np.divide(hm_b_num_24, max(hm_b_num_24), out=np.zeros_like(hm_b_num_24, dtype=np.float64),
                       casting="unsafe", where=max(hm_b_num_24) != 0)
    for i in range(len(hm_b_num_24)):
        hm_b_p_24.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_p_24[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_p_24)):
            hm_b_p_24[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_b_num_36, max(hm_b_num_36), out=np.zeros_like(hm_b_num_36, dtype=np.float64),
                       casting="unsafe", where=max(hm_b_num_36) != 0)
    for i in range(len(hm_b_num_36)):
        hm_b_p_36.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_p_36[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_p_36)):
            hm_b_p_36[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_b_num_48, max(hm_b_num_48), out=np.zeros_like(hm_b_num_48, dtype=np.float64),
                       casting="unsafe", where=max(hm_b_num_48) != 0)
    for i in range(len(hm_b_num_48)):
        hm_b_p_48.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_p_48[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_p_48)):
            hm_b_p_48[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_b_num_72, max(hm_b_num_72), out=np.zeros_like(hm_b_num_72, dtype=np.float64),
                       casting="unsafe", where=max(hm_b_num_72) != 0)
    for i in range(len(hm_b_num_72)):
        hm_b_p_72.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_p_72[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_p_72)):
            hm_b_p_72[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_b_num_96, max(hm_b_num_96), out=np.zeros_like(hm_b_num_96, dtype=np.float64),
                       casting="unsafe", where=max(hm_b_num_96) != 0)
    for i in range(len(hm_b_num_96)):
        hm_b_p_96.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_p_96[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_p_96)):
            hm_b_p_96[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_b_num_96_, max(hm_b_num_96_), out=np.zeros_like(hm_b_num_96_, dtype=np.float64),
                       casting="unsafe", where=max(hm_b_num_96_) != 0)
    for i in range(len(hm_b_num_96_)):
        hm_b_p_96_.append("%.2f%%" % (arrayA[i] * 100))
    if hm_b_p_96_[0] == 'nan%':
        a = 0
        for i in range(len(hm_b_p_96_)):
            hm_b_p_96_[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_j_num_6, max(hm_j_num_6), out=np.zeros_like(hm_j_num_6, dtype=np.float64),
                       casting="unsafe", where=max(hm_j_num_6) != 0)
    for i in range(len(hm_j_num_6)):
        hm_j_p_6.append("%.2f%%" % (arrayA[i] * 100))
    if hm_j_p_6[0] == 'nan%':
        a = 0
        for i in range(len(hm_j_p_6)):
            hm_j_p_6[i] = '{:.2%}'.format(a)

    arrayA = np.divide(hm_j_num_12, max(hm_j_num_12), out=np.zeros_like(hm_j_num_12, dtype=np.float64),
                       casting="unsafe", where=max(hm_j_num_12) != 0)
    for i in range(len(hm_j_num_12)):
        hm_j_p_12.append("%.2f%%" % (arrayA[i] * 100))
    if hm_j_p_12[0] == 'nan%':
        a = 0
        for i in range(len(hm_j_p_12)):
            hm_j_p_12[i] = '{:.2%}'.format(a)

    arrayA = np.divide(hm_j_num_24, max(hm_j_num_24), out=np.zeros_like(hm_j_num_24, dtype=np.float64),
                       casting="unsafe", where=max(hm_j_num_24) != 0)
    for i in range(len(hm_j_num_24)):
        hm_j_p_24.append("%.2f%%" % (arrayA[i] * 100))
    if hm_j_p_24[0] == 'nan%':
        a = 0
        for i in range(len(hm_j_p_24)):
            hm_j_p_24[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_j_num_36, max(hm_j_num_36), out=np.zeros_like(hm_j_num_36, dtype=np.float64),
                       casting="unsafe", where=max(hm_j_num_36) != 0)
    for i in range(len(hm_j_num_36)):
        hm_j_p_36.append("%.2f%%" % (arrayA[i] * 100))
    if hm_j_p_36[0] == 'nan%':
        a = 0
        for i in range(len(hm_j_p_36)):
            hm_j_p_36[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_j_num_48, max(hm_j_num_48), out=np.zeros_like(hm_j_num_48, dtype=np.float64),
                       casting="unsafe", where=max(hm_j_num_48) != 0)
    for i in range(len(hm_j_num_48)):
        hm_j_p_48.append("%.2f%%" % (arrayA[i] * 100))
    if hm_j_p_48[0] == 'nan%':
        a = 0
        for i in range(len(hm_j_p_48)):
            hm_j_p_48[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_j_num_72, max(hm_j_num_72), out=np.zeros_like(hm_j_num_72, dtype=np.float64),
                       casting="unsafe", where=max(hm_j_num_72) != 0)
    for i in range(len(hm_j_num_72)):
        hm_j_p_72.append("%.2f%%" % (arrayA[i] * 100))
    if hm_j_p_72[0] == 'nan%':
        a = 0
        for i in range(len(hm_j_p_72)):
            hm_j_p_72[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_j_num_96, max(hm_j_num_96), out=np.zeros_like(hm_j_num_96, dtype=np.float64),
                       casting="unsafe", where=max(hm_j_num_96) != 0)
    for i in range(len(hm_j_num_96)):
        hm_j_p_96.append("%.2f%%" % (arrayA[i] * 100))
    if hm_j_p_96[0] == 'nan%':
        a = 0
        for i in range(len(hm_j_p_96)):
            hm_j_p_96[i] = '{:.2%}'.format(a)
    arrayA = np.divide(hm_j_num_96_, max(hm_j_num_96_), out=np.zeros_like(hm_j_num_96_, dtype=np.float64),
                       casting="unsafe", where=max(hm_j_num_96_) != 0)
    for i in range(len(hm_j_num_96_)):
        hm_j_p_96_.append("%.2f%%" % (arrayA[i] * 100))
    if hm_j_p_96_[0] == 'nan%':
        a = 0
        for i in range(len(hm_j_p_96_)):
            hm_j_p_96_[i] = '{:.2%}'.format(a)

    arrayA = np.divide(tx_b_num_6, max(tx_b_num_6), out=np.zeros_like(tx_b_num_6, dtype=np.float64), casting="unsafe",
                       where=max(tx_b_num_6) != 0)
    for i in range(len(tx_b_num_6)):
        tx_b_p_6.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_p_6[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_p_6)):
            tx_b_p_6[i] = '{:.2%}'.format(a)

    arrayA = np.divide(tx_b_num_12, max(tx_b_num_12), out=np.zeros_like(tx_b_num_12, dtype=np.float64),
                       casting="unsafe", where=max(tx_b_num_12) != 0)
    for i in range(len(tx_b_num_12)):
        tx_b_p_12.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_p_12[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_p_12)):
            tx_b_p_12[i] = '{:.2%}'.format(a)

    arrayA = np.divide(tx_b_num_24, max(tx_b_num_24), out=np.zeros_like(tx_b_num_24, dtype=np.float64),
                       casting="unsafe", where=max(tx_b_num_24) != 0)
    for i in range(len(tx_b_num_24)):
        tx_b_p_24.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_p_24[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_p_24)):
            tx_b_p_24[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_b_num_36, max(tx_b_num_36), out=np.zeros_like(tx_b_num_36, dtype=np.float64),
                       casting="unsafe", where=max(tx_b_num_36) != 0)
    for i in range(len(tx_b_num_36)):
        tx_b_p_36.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_p_36[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_p_36)):
            tx_b_p_36[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_b_num_48, max(tx_b_num_48), out=np.zeros_like(tx_b_num_48, dtype=np.float64),
                       casting="unsafe", where=max(tx_b_num_48) != 0)
    for i in range(len(tx_b_num_48)):
        tx_b_p_48.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_p_48[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_p_48)):
            tx_b_p_48[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_b_num_72, max(tx_b_num_72), out=np.zeros_like(tx_b_num_72, dtype=np.float64),
                       casting="unsafe", where=max(tx_b_num_72) != 0)
    for i in range(len(tx_b_num_72)):
        tx_b_p_72.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_p_72[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_p_72)):
            tx_b_p_72[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_b_num_96, max(tx_b_num_96), out=np.zeros_like(tx_b_num_96, dtype=np.float64),
                       casting="unsafe", where=max(tx_b_num_96) != 0)
    for i in range(len(tx_b_num_96)):
        tx_b_p_96.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_p_96[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_p_96)):
            tx_b_p_96[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_b_num_96_, max(tx_b_num_96_), out=np.zeros_like(tx_b_num_96_, dtype=np.float64),
                       casting="unsafe", where=max(tx_b_num_96_) != 0)
    for i in range(len(tx_b_num_96_)):
        tx_b_p_96_.append("%.2f%%" % (arrayA[i] * 100))
    if tx_b_p_96_[0] == 'nan%':
        a = 0
        for i in range(len(tx_b_p_96_)):
            tx_b_p_96_[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_j_num_6, max(tx_j_num_6), out=np.zeros_like(tx_j_num_6, dtype=np.float64),
                       casting="unsafe", where=max(tx_j_num_6) != 0)
    for i in range(len(tx_j_num_6)):
        tx_j_p_6.append("%.2f%%" % (arrayA[i] * 100))
    if tx_j_p_6[0] == 'nan%':
        a = 0
        for i in range(len(tx_j_p_6)):
            tx_j_p_6[i] = '{:.2%}'.format(a)

    arrayA = np.divide(tx_j_num_12, max(tx_j_num_12), out=np.zeros_like(tx_j_num_12, dtype=np.float64),
                       casting="unsafe", where=max(tx_j_num_12) != 0)
    for i in range(len(tx_j_num_12)):
        tx_j_p_12.append("%.2f%%" % (arrayA[i] * 100))
    if tx_j_p_12[0] == 'nan%':
        a = 0
        for i in range(len(tx_j_p_12)):
            tx_j_p_12[i] = '{:.2%}'.format(a)

    arrayA = np.divide(tx_j_num_24, max(tx_j_num_24), out=np.zeros_like(tx_j_num_24, dtype=np.float64),
                       casting="unsafe", where=max(tx_j_num_24) != 0)
    for i in range(len(tx_j_num_24)):
        tx_j_p_24.append("%.2f%%" % (arrayA[i] * 100))
    if tx_j_p_24[0] == 'nan%':
        a = 0
        for i in range(len(tx_j_p_24)):
            tx_j_p_24[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_j_num_36, max(tx_j_num_36), out=np.zeros_like(tx_j_num_36, dtype=np.float64),
                       casting="unsafe", where=max(tx_j_num_36) != 0)
    for i in range(len(tx_j_num_36)):
        tx_j_p_36.append("%.2f%%" % (arrayA[i] * 100))
    if tx_j_p_36[0] == 'nan%':
        a = 0
        for i in range(len(tx_j_p_36)):
            tx_j_p_36[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_j_num_48, max(tx_j_num_48), out=np.zeros_like(tx_j_num_48, dtype=np.float64),
                       casting="unsafe", where=max(tx_j_num_48) != 0)
    for i in range(len(tx_j_num_48)):
        tx_j_p_48.append("%.2f%%" % (arrayA[i] * 100))
    if tx_j_p_48[0] == 'nan%':
        a = 0
        for i in range(len(tx_j_p_48)):
            tx_j_p_48[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_j_num_72, max(tx_j_num_72), out=np.zeros_like(tx_j_num_72, dtype=np.float64),
                       casting="unsafe", where=max(tx_j_num_72) != 0)
    for i in range(len(tx_j_num_72)):
        tx_j_p_72.append("%.2f%%" % (arrayA[i] * 100))
    if tx_j_p_72[0] == 'nan%':
        a = 0
        for i in range(len(tx_j_p_72)):
            tx_j_p_72[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_j_num_96, max(tx_j_num_96), out=np.zeros_like(tx_j_num_96, dtype=np.float64),
                       casting="unsafe", where=max(tx_j_num_96) != 0)
    for i in range(len(tx_j_num_96)):
        tx_j_p_96.append("%.2f%%" % (arrayA[i] * 100))
    if tx_j_p_96[0] == 'nan%':
        a = 0
        for i in range(len(tx_j_p_96)):
            tx_j_p_96[i] = '{:.2%}'.format(a)
    arrayA = np.divide(tx_j_num_96_, max(tx_j_num_96_), out=np.zeros_like(tx_j_num_96_, dtype=np.float64),
                       casting="unsafe", where=max(tx_j_num_96_) != 0)
    for i in range(len(tx_j_num_96_)):
        tx_j_p_96_.append("%.2f%%" % (arrayA[i] * 100))
    if tx_j_p_96_[0] == 'nan%':
        a = 0
        for i in range(len(tx_j_p_96_)):
            tx_j_p_96_[i] = '{:.2%}'.format(a)

    jsonData['tx_xb_b_2'] = tx_xb_b_2
    jsonData['tx_xb_b_4'] = tx_xb_b_4
    jsonData['tx_xb_b_6'] = tx_xb_b_6
    jsonData['tx_xb_b_8'] = tx_xb_b_8
    jsonData['tx_xb_b_10'] = tx_xb_b_10
    jsonData['tx_xb_b_12'] = tx_xb_b_12
    jsonData['tx_xb_b_24'] = tx_xb_b_24
    jsonData['tx_xb_b_24_'] = tx_xb_b_24_
    jsonData['hm_xb_b_2'] = hm_xb_b_2
    jsonData['hm_xb_b_4'] = hm_xb_b_4
    jsonData['hm_xb_b_6'] = hm_xb_b_6
    jsonData['hm_xb_b_8'] = hm_xb_b_8
    jsonData['hm_xb_b_10'] = hm_xb_b_10
    jsonData['hm_xb_b_12'] = hm_xb_b_12
    jsonData['hm_xb_b_24'] = hm_xb_b_24
    jsonData['hm_xb_b_24_'] = hm_xb_b_24_

    jsonData['hm_j_12'] = hm_j_12
    jsonData['hm_j_24'] = hm_j_24
    jsonData['hm_j_48'] = hm_j_48
    jsonData['hm_j_72'] = hm_j_72
    jsonData['hm_j_120'] = hm_j_120
    jsonData['hm_j_240'] = hm_j_240
    jsonData['hm_j_360'] = hm_j_360
    jsonData['hm_j_361'] = hm_j_361
    jsonData['tx_j_12'] = tx_j_12
    jsonData['tx_j_24'] = tx_j_24
    jsonData['tx_j_48'] = tx_j_48
    jsonData['tx_j_72'] = tx_j_72
    jsonData['tx_j_120'] = tx_j_120
    jsonData['tx_j_240'] = tx_j_240
    jsonData['tx_j_360'] = tx_j_360
    jsonData['tx_j_361'] = tx_j_361
    jsonData['hm_b_12'] = hm_b_12
    jsonData['hm_b_24'] = hm_b_24
    jsonData['hm_b_48'] = hm_b_48
    jsonData['hm_b_72'] = hm_b_72
    jsonData['hm_b_120'] = hm_b_120
    jsonData['hm_b_240'] = hm_b_240
    jsonData['hm_b_360'] = hm_b_360
    jsonData['hm_b_361'] = hm_b_361
    jsonData['tx_b_12'] = tx_b_12
    jsonData['tx_b_24'] = tx_b_24
    jsonData['tx_b_48'] = tx_b_48
    jsonData['tx_b_72'] = tx_b_72
    jsonData['tx_b_120'] = tx_b_120
    jsonData['tx_b_240'] = tx_b_240
    jsonData['tx_b_360'] = tx_b_360
    jsonData['tx_b_361'] = tx_b_361
    jsonData['hm_b_xb_num_2'] = hm_b_xb_num_2.tolist()
    jsonData['hm_b_xb_num_4'] = hm_b_xb_num_4.tolist()
    jsonData['hm_b_xb_num_6'] = hm_b_xb_num_6.tolist()
    jsonData['hm_b_xb_num_8'] = hm_b_xb_num_8.tolist()
    jsonData['hm_b_xb_num_10'] = hm_b_xb_num_10.tolist()
    jsonData['hm_b_xb_num_12'] = hm_b_xb_num_12.tolist()
    jsonData['hm_b_xb_num_24'] = hm_b_xb_num_24.tolist()
    jsonData['hm_b_xb_num_24_'] = hm_b_xb_num_24_.tolist()
    jsonData['tx_b_xb_num_2'] = tx_b_xb_num_2.tolist()
    jsonData['tx_b_xb_num_4'] = tx_b_xb_num_4.tolist()
    jsonData['tx_b_xb_num_6'] = tx_b_xb_num_6.tolist()
    jsonData['tx_b_xb_num_8'] = tx_b_xb_num_8.tolist()
    jsonData['tx_b_xb_num_10'] = tx_b_xb_num_10.tolist()
    jsonData['tx_b_xb_num_12'] = tx_b_xb_num_12.tolist()
    jsonData['tx_b_xb_num_24'] = tx_b_xb_num_24.tolist()
    jsonData['tx_b_xb_num_24_'] = tx_b_xb_num_24_.tolist()
    jsonData['hm_b_fba_num_12'] = hm_b_fba_num_12.tolist()
    jsonData['hm_b_fba_num_24'] = hm_b_fba_num_24.tolist()
    jsonData['hm_b_fba_num_48'] = hm_b_fba_num_48.tolist()
    jsonData['hm_b_fba_num_72'] = hm_b_fba_num_72.tolist()
    jsonData['hm_b_fba_num_120'] = hm_b_fba_num_120.tolist()
    jsonData['hm_b_fba_num_240'] = hm_b_fba_num_240.tolist()
    jsonData['hm_b_fba_num_360'] = hm_b_fba_num_360.tolist()
    jsonData['hm_b_fba_num_361'] = hm_b_fba_num_361.tolist()
    jsonData['tx_b_fba_num_12'] = tx_b_fba_num_12.tolist()
    jsonData['tx_b_fba_num_24'] = tx_b_fba_num_24.tolist()
    jsonData['tx_b_fba_num_48'] = tx_b_fba_num_48.tolist()
    jsonData['tx_b_fba_num_72'] = tx_b_fba_num_72.tolist()
    jsonData['tx_b_fba_num_120'] = tx_b_fba_num_120.tolist()
    jsonData['tx_b_fba_num_240'] = tx_b_fba_num_240.tolist()
    jsonData['tx_b_fba_num_360'] = tx_b_fba_num_360.tolist()
    jsonData['tx_b_fba_num_361'] = tx_b_fba_num_361.tolist()
    jsonData['hm_j_fba_num_12'] = hm_j_fba_num_12.tolist()
    jsonData['hm_j_fba_num_24'] = hm_j_fba_num_24.tolist()
    jsonData['hm_j_fba_num_48'] = hm_j_fba_num_48.tolist()
    jsonData['hm_j_fba_num_72'] = hm_j_fba_num_72.tolist()
    jsonData['hm_j_fba_num_120'] = hm_j_fba_num_120.tolist()
    jsonData['hm_j_fba_num_240'] = hm_j_fba_num_240.tolist()
    jsonData['hm_j_fba_num_360'] = hm_j_fba_num_360.tolist()
    jsonData['hm_j_fba_num_361'] = hm_j_fba_num_361.tolist()
    jsonData['tx_j_fba_num_12'] = tx_j_fba_num_12.tolist()
    jsonData['tx_j_fba_num_24'] = tx_j_fba_num_24.tolist()
    jsonData['tx_j_fba_num_48'] = tx_j_fba_num_48.tolist()
    jsonData['tx_j_fba_num_72'] = tx_j_fba_num_72.tolist()
    jsonData['tx_j_fba_num_120'] = tx_j_fba_num_120.tolist()
    jsonData['tx_j_fba_num_240'] = tx_j_fba_num_240.tolist()
    jsonData['tx_j_fba_num_360'] = tx_j_fba_num_360.tolist()
    jsonData['tx_j_fba_num_361'] = tx_j_fba_num_361.tolist()

    jsonData['hm_drk_b_num1'] = hm_drk_b_num1
    jsonData['hm_drk_j_num1'] = hm_drk_j_num1

    jsonData['hm_dtm_b_num1'] = hm_dtm_b_num1
    jsonData['hm_dtm_j_num1'] = hm_dtm_j_num1

    jsonData['hm_dgnzj_b_num1'] = hm_dgnzj_b_num1
    jsonData['hm_dgnzj_j_num1'] = hm_dgnzj_j_num1

    jsonData['hm_dsj_b_num1'] = hm_dsj_b_num1
    jsonData['hm_dsj_j_num1'] = hm_dsj_j_num1

    jsonData['hm_sjz_b_num1'] = hm_sjz_b_num1
    jsonData['hm_sjz_j_num1'] = hm_sjz_j_num1

    jsonData['tx_drk_b_num1'] = tx_drk_b_num1
    jsonData['tx_drk_j_num1'] = tx_drk_j_num1

    jsonData['tx_dtm_b_num1'] = tx_dtm_b_num1
    jsonData['tx_dtm_j_num1'] = tx_dtm_j_num1

    jsonData['tx_dgnzj_b_num1'] = tx_dgnzj_b_num1
    jsonData['tx_dgnzj_j_num1'] = tx_dgnzj_j_num1

    jsonData['tx_dsj_b_num1'] = tx_dsj_b_num1
    jsonData['tx_dsj_j_num1'] = tx_dsj_j_num1

    jsonData['tx_sjz_b_num1'] = tx_sjz_b_num1
    jsonData['tx_sjz_j_num1'] = tx_sjz_j_num1

    jsonData['hm_b_p_6'] = hm_b_p_6
    jsonData['hm_b_p_12'] = hm_b_p_12
    jsonData['hm_b_p_24'] = hm_b_p_24
    jsonData['hm_b_p_36'] = hm_b_p_36
    jsonData['hm_b_p_48'] = hm_b_p_48
    jsonData['hm_b_p_72'] = hm_b_p_72
    jsonData['hm_b_p_96'] = hm_b_p_96
    jsonData['hm_b_p_96_'] = hm_b_p_96_

    jsonData['hm_j_p_6'] = hm_j_p_6
    jsonData['hm_j_p_12'] = hm_j_p_12
    jsonData['hm_j_p_24'] = hm_j_p_24
    jsonData['hm_j_p_36'] = hm_j_p_36
    jsonData['hm_j_p_48'] = hm_j_p_48
    jsonData['hm_j_p_72'] = hm_j_p_72
    jsonData['hm_j_p_96'] = hm_j_p_96
    jsonData['hm_j_p_96_'] = hm_j_p_96_

    jsonData['tx_b_p_6'] = tx_b_p_6
    jsonData['tx_b_p_12'] = tx_b_p_12
    jsonData['tx_b_p_24'] = tx_b_p_24
    jsonData['tx_b_p_36'] = tx_b_p_36
    jsonData['tx_b_p_48'] = tx_b_p_48
    jsonData['tx_b_p_72'] = tx_b_p_72
    jsonData['tx_b_p_96'] = tx_b_p_96
    jsonData['tx_b_p_96_'] = tx_b_p_96_

    jsonData['tx_j_p_6'] = tx_j_p_6
    jsonData['tx_j_p_12'] = tx_j_p_12
    jsonData['tx_j_p_24'] = tx_j_p_24
    jsonData['tx_j_p_36'] = tx_j_p_36
    jsonData['tx_j_p_48'] = tx_j_p_48
    jsonData['tx_j_p_72'] = tx_j_p_72
    jsonData['tx_j_p_96'] = tx_j_p_96
    jsonData['tx_j_p_96_'] = tx_j_p_96_

    jsonData['tx_drk_shelf'] = tx_drk_shelf
    jsonData['tx_dtm_shelf'] = tx_dtm_shelf
    jsonData['tx_dgnzj_shelf'] = tx_dgnzj_shelf
    jsonData['tx_dsj_shelf'] = tx_dsj_shelf
    jsonData['tx_sjz_shelf'] = tx_sjz_shelf

    jsonData['hm_drk_shelf'] = hm_drk_shelf

    jsonData['hm_dtm_shelf'] = hm_dtm_shelf
    jsonData['hm_dgnzj_shelf'] = hm_dgnzj_shelf
    jsonData['hm_dsj_shelf'] = hm_dsj_shelf
    jsonData['hm_sjz_shelf'] = hm_sjz_shelf
    jsonData['tx_drk_shelf_time'] = tx_drk_shelf_time
    jsonData['tx_dtm_shelf_time'] = tx_dtm_shelf_time
    jsonData['tx_dgnzj_shelf_time'] = tx_dgnzj_shelf_time
    jsonData['tx_dsj_shelf_time'] = tx_dsj_shelf_time
    jsonData['tx_sjz_shelf_time'] = tx_sjz_shelf_time

    jsonData['hm_drk_shelf_time'] = hm_drk_shelf_time
    jsonData['hm_dtm_shelf_time'] = hm_dtm_shelf_time
    jsonData['hm_dgnzj_shelf_time'] = hm_dgnzj_shelf_time
    jsonData['hm_dsj_shelf_time'] = hm_dsj_shelf_time
    jsonData['hm_sjz_shelf_time'] = hm_sjz_shelf_time

    jsonData['tx_drk_shelf_num1'] = tx_drk_shelf_num1
    jsonData['tx_dtm_shelf_num1'] = tx_dtm_shelf_num1
    jsonData['tx_dgnzj_shelf_num1'] = tx_dgnzj_shelf_num1
    jsonData['tx_dsj_shelf_num1'] = tx_dsj_shelf_num1
    jsonData['tx_sjz_shelf_num1'] = tx_sjz_shelf_num1
    jsonData['hm_drk_shelf_num1'] = hm_drk_shelf_num1
    jsonData['hm_dtm_shelf_num1'] = hm_dtm_shelf_num1
    jsonData['hm_dgnzj_shelf_num1'] = hm_dgnzj_shelf_num1
    jsonData['hm_dsj_shelf_num1'] = hm_dsj_shelf_num1
    jsonData['hm_sjz_shelf_num1'] = hm_sjz_shelf_num1

    j = json.dumps(jsonData, cls=DecimalEncoder)
    return (j)


@app.route('/daily4', methods=['POST'])
def xiaoneng_daily():
   # sql = 'SELECT  DATE_FORMAT(now(),"%Y-%m-%d")date,	a.warehouse_code,	a.group_w,	ifnull( round( avg( a.act_num ), 0 ), 0 ) act_num,	ifnull( round( avg( a.act_hour ), 2 ), 0 ) act_hour,	ifnull( round( avg( b.num ), 2 ), 0 ) act_work_num,	ifnull( round( avg( a.temp_num ), 0 ), 0 ) temp_num,	ifnull( round( avg( a.temp_hour ), 2 ), 0 ) temp_hour,	ifnull( round( avg( c.num ), 2 ), 0 ) temp_work_num,	round(ifnull( round( avg( b.num ), 2 ), 0 ) / ifnull( round( avg( a.act_num ), 2 ), 0 ),2) act_ef,	round(ifnull( round( avg( c.num ), 2 ), 0 ) / ifnull( round( avg( a.temp_num ), 2 ), 0 ),2) temp_ef FROM	(SELECT	a.warehouse_code,	a.date,CASE		WHEN a.`group` = "working" THEN	"receive" ELSE a.`group` 	END group_w,	sum( a.act_num ) act_num,	a.act_hour + a.sup_hour `act_hour`,	a.temp_num,	a.temp_hour FROM	(	SELECT		a.warehouse_code,		a.`group`,		a.date,		a.actual_work AS act_num,		a.group_leader + a.receive_hour + a.instock_hour + a.return_deal + a.allocate_instock + a.working_hour + a.all_quality + a.instock_putaway + a.return_putaway + a.problem_putaway + a.pick_hour + a.move_hour + a.inventory_hour + a.check_hour + a.second_pick + a.pack_hour + a.channel_pick + a.scan_weigh + a.delivery_hour + a.fba_change + a.fba_pack + a.fba_delivery + a.iqc_hour + a.confirm_exception + a.instock_exception + a.warehouse_exception + a.order_exception + a.transit_receive + a.transit_pack + a.transit_send + a.transit_manage + a.other_hour AS act_hour,		a.temporary_people AS temp_num,		a.temporary_hour AS temp_hour,		ifnull( b.`hour`, 0 ) sup_hour,		a.temporary_hour + a.group_leader + a.receive_hour + a.instock_hour + a.return_deal + a.allocate_instock + a.working_hour + a.all_quality + a.instock_putaway + a.return_putaway + a.problem_putaway + a.pick_hour + a.move_hour + a.inventory_hour + a.check_hour + a.second_pick + a.pack_hour + a.channel_pick + a.scan_weigh + a.delivery_hour + a.fba_change + a.fba_pack + a.fba_delivery + a.iqc_hour + a.confirm_exception + a.instock_exception + a.warehouse_exception + a.order_exception + a.transit_receive + a.transit_pack + a.transit_send + a.transit_manage + a.other_hour AS total_hour 	FROM		yb_daily_report a		LEFT JOIN (		SELECT			date,			warehouse_code,			`group`,			sum( `hour` ) AS `hour` 		FROM			(			SELECT				date,				JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[0].warehouse" ) ) AS warehouse_code,				JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[0].group" ) ) AS `group`,				JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[0].hour" ) ) AS `hour` 			FROM				yb_daily_report 			WHERE				support_out IS NOT NULL UNION			SELECT				date,				JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[1].warehouse" ) ) AS warehouse_code,				JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[1].group" ) ) AS `group`,				JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[1].hour" ) ) AS `hour` 			FROM				yb_daily_report 			WHERE				support_out IS NOT NULL UNION			SELECT				date,				JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[2].warehouse" ) ) AS warehouse_code,				JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[2].group" ) ) AS `group`,				JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[2].hour" ) ) AS `hour` 			FROM				yb_daily_report 			WHERE				support_out IS NOT NULL UNION			SELECT				date,				JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[3].warehouse" ) ) AS warehouse_code,				JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[3].group" ) ) AS `group`,				JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[3].hour" ) ) AS `hour` 			FROM				yb_daily_report 			WHERE				support_out IS NOT NULL UNION			SELECT				date,				JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[4].warehouse" ) ) AS warehouse_code,				JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[4].group" ) ) AS `group`,				JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[4].hour" ) ) AS `hour` 			FROM				yb_daily_report 			WHERE				support_out IS NOT NULL UNION			SELECT				date,				JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[5].warehouse" ) ) AS warehouse_code,				JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[5].group" ) ) AS `group`,				JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[5].hour" ) ) AS `hour` 			FROM				yb_daily_report 			WHERE				support_out IS NOT NULL UNION			SELECT				date,				JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[6].warehouse" ) ) AS warehouse_code,				JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[6].group" ) ) AS `group`,				JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[6].hour" ) ) AS `hour` 			FROM				yb_daily_report 			WHERE				support_out IS NOT NULL UNION			SELECT				date,				JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[7].warehouse" ) ) AS warehouse_code,				JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[7].group" ) ) AS `group`,				JSON_UNQUOTE ( JSON_EXTRACT ( support_out, "$[7].hour" ) ) AS `hour` 			FROM				yb_daily_report 			WHERE				support_out IS NOT NULL 			) a 		WHERE			a.warehouse_code IS NOT NULL 		GROUP BY			date,			warehouse_code,			`group` 		) b ON a.date = b.date 		AND a.warehouse_code = b.warehouse_code 		AND a.`group` = b.`group` 	WHERE		TO_DAYS( NOW( ) ) - TO_DAYS( a.date ) <= 31 		AND TO_DAYS( NOW( ) ) - TO_DAYS( a.date ) NOT IN ( 0, 1 ) 		AND a.`group` IN ( "fba_change", "fba_pack", "receive", "working", "putaway", "pick" ) 	GROUP BY		a.warehouse_code,		`group`,		a.date 	) a GROUP BY	a.warehouse_code,	group_w,	a.date 	) a	LEFT JOIN (		SELECT		warehouse_code AS warehouse,		"receive" group_w,		DATE_FORMAT( quality_time, "%Y-%m-%d" ) date,		sum( box_number ) num 	FROM		ueb_express_receipt 	WHERE		TO_DAYS( NOW( ) ) - TO_DAYS( quality_time ) <= 31 		AND TO_DAYS( NOW( ) ) - TO_DAYS( quality_time ) NOT IN ( 0, 1 ) 		AND quality_time IS NOT NULL 		AND warehouse_code IN ( "HM_AA", "SZ_AA" ) 		AND (			add_username NOT LIKE "L%" 			OR add_username NOT LIKE "RK%" 			OR add_username NOT LIKE "DB%" 			OR add_username NOT LIKE "R%" 			OR add_username NOT LIKE "TX%" 			OR add_username NOT LIKE "FB%" 								) 	GROUP BY		warehouse_code,		date UNION	SELECT	CASE					WHEN			warehouse_code = "AFN" THEN				"HM_AA" ELSE warehouse_code 			END AS `warehouse`,			"putaway" AS group_w,			add_time date,			round(				(					IFNULL( sum( JSON_UNQUOTE ( JSON_EXTRACT ( work_parme_num, "$.instock.instock.piece_total" ) ) ), 0 ) + IFNULL( sum( JSON_UNQUOTE ( JSON_EXTRACT ( work_parme_num, "$.instock.return_instock.piece_total" ) ) ), 0 ) + IFNULL( sum( JSON_UNQUOTE ( JSON_EXTRACT ( work_parme_num, "$.instock.move_instock.piece_total" ) ) ), 0 ) + IFNULL( sum( JSON_UNQUOTE ( JSON_EXTRACT ( work_parme_num, "$.instock.instock_sku_allot.piece_total" ) ) ), 0 ) + IFNULL( sum( JSON_UNQUOTE ( JSON_EXTRACT ( work_parme_num, "$.instock.question_instock.piece_total" ) ) ), 0 ) 				),				2 			) AS `num` 		FROM			`ueb_work_num_log_history` 		WHERE			add_time NOT IN ( "num", "user_name", "warehouse_code" ) 			AND warehouse_code NOT IN ( "CX", "shzz", "AFN" ) 			AND (				user_name NOT LIKE "L%" 				OR user_name NOT LIKE "RK%" 				OR user_name NOT LIKE "DB%" 				OR user_name NOT LIKE "R%" 				OR user_name NOT LIKE "TX%" 				OR user_name NOT LIKE "FB%" 			) 			AND TO_DAYS( NOW( ) ) - TO_DAYS( add_time ) <= 31 			AND TO_DAYS( NOW( ) ) - TO_DAYS( add_time ) NOT IN ( 0, 1 ) 		GROUP BY			`warehouse`,			add_time UNION		SELECT		CASE							WHEN				warehouse_code = "AFN" THEN					"HM_AA" ELSE warehouse_code 				END AS `warehouse`,				"pick" AS group_w,				add_time,				round(					(						IFNULL( sum( JSON_UNQUOTE ( JSON_EXTRACT ( work_parme_num, "$.pick.pick_single.piece_total" ) ) ), 0 ) + IFNULL( sum( JSON_UNQUOTE ( JSON_EXTRACT ( work_parme_num, "$.pick.pick_order.piece_total" ) ) ), 0 ) + IFNULL( sum( JSON_UNQUOTE ( JSON_EXTRACT ( work_parme_num, "$.pick.pick_multi.piece_total" ) ) ), 0 ) + IFNULL( sum( JSON_UNQUOTE ( JSON_EXTRACT ( work_parme_num, "$.pick.pick_sku_bao.piece_total" ) ) ), 0 ) + IFNULL( sum( JSON_UNQUOTE ( JSON_EXTRACT ( work_parme_num, "$.pick.pick_move.piece_total" ) ) ), 0 ) + IFNULL( sum( JSON_UNQUOTE ( JSON_EXTRACT ( work_parme_num, "$.pick.pick_single_more.piece_total" ) ) ), 0 ) 					),					2 				) AS `num` 			FROM				`ueb_work_num_log_history` 			WHERE				add_time NOT IN ( "num", "user_name", "warehouse_code" ) 				AND warehouse_code NOT IN ( "CX", "shzz", "AFN" ) 				AND (					user_name NOT LIKE "L%" 					OR user_name NOT LIKE "RK%" 					OR user_name NOT LIKE "DB%" 					OR user_name NOT LIKE "R%" 					OR user_name NOT LIKE "TX%" 					OR user_name NOT LIKE "FB%" 				) 				AND TO_DAYS( NOW( ) ) - TO_DAYS( add_time ) <= 31 				AND TO_DAYS( NOW( ) ) - TO_DAYS( add_time ) NOT IN ( 0, 1 ) 			GROUP BY				add_time,				`warehouse` UNION			SELECT			CASE									WHEN					warehouse_code = "AFN" THEN						"HM_AA" ELSE warehouse_code 					END AS `warehouse`,					"fba_pack" AS group_w,					add_time,					round( IFNULL( sum( JSON_UNQUOTE ( JSON_EXTRACT ( work_parme_num, "$.FBA.FBA.piece_total" ) ) ), 0 ), 2 ) AS `num` 				FROM					`ueb_work_num_log_history` 				WHERE					add_time NOT IN ( "num", "user_name", "warehouse_code" ) 					AND warehouse_code NOT IN ( "CX", "shzz", "AFN" ) 					AND (						user_name NOT LIKE "L%" 						OR user_name NOT LIKE "RK%" 						OR user_name NOT LIKE "DB%" 						OR user_name NOT LIKE "R%" 						OR user_name NOT LIKE "TX%" 						OR user_name NOT LIKE "FB%" 					) 					AND TO_DAYS( NOW( ) ) - TO_DAYS( add_time ) <= 31 					AND TO_DAYS( NOW( ) ) - TO_DAYS( add_time ) NOT IN ( 0, 1 ) 				GROUP BY					add_time,					`warehouse` UNION				SELECT				CASE											WHEN						warehouse_code = "AFN" THEN							"HM_AA" ELSE warehouse_code 						END AS `warehouse`,						"fba_change" AS group_w,						add_time,						round(							(								IFNULL( sum( JSON_UNQUOTE ( JSON_EXTRACT ( work_parme_num, "$.FBAPostCode.singlebatch_print_label.piece_total" ) ) ), 0 ) + IFNULL( sum( JSON_UNQUOTE ( JSON_EXTRACT ( work_parme_num, "$.FBAPostCode.singlebatch_print_label_FBC.piece_total" ) ) ), 0 ) + IFNULL( sum( JSON_UNQUOTE ( JSON_EXTRACT ( work_parme_num, "$.FBAPostCode.singlebatch_print_label_FBW.piece_total" ) ) ), 0 ) 							),							2 						) AS `num` 					FROM						`ueb_work_num_log_history` 					WHERE						add_time NOT IN ( "num", "user_name", "warehouse_code" ) 						AND warehouse_code NOT IN ( "CX", "shzz", "AFN" ) 						AND (							user_name NOT LIKE "L%" 							OR user_name NOT LIKE "RK%" 							OR user_name NOT LIKE "DB%" 							OR user_name NOT LIKE "R%" 							OR user_name NOT LIKE "TX%" 							OR user_name NOT LIKE "FB%" 						) 						AND TO_DAYS( NOW( ) ) - TO_DAYS( add_time ) <= 31 						AND TO_DAYS( NOW( ) ) - TO_DAYS( add_time ) NOT IN ( 0, 1 ) 					GROUP BY						add_time,						`warehouse` 					) b ON a.warehouse_code = b.warehouse 					AND a.group_w = b.group_w 					AND a.date = b.date					LEFT JOIN (					SELECT						warehouse_code AS warehouse,						"receive" group_w,						DATE_FORMAT( quality_time, "%Y-%m-%d" ) date,						sum( box_number ) num 					FROM						ueb_express_receipt 					WHERE						TO_DAYS( NOW( ) ) - TO_DAYS( quality_time ) <= 31 						AND TO_DAYS( NOW( ) ) - TO_DAYS( quality_time ) NOT IN ( 0, 1 ) 						AND quality_time IS NOT NULL 						AND warehouse_code IN ( "HM_AA", "SZ_AA" ) 						AND ( add_username LIKE "L%" OR add_username LIKE "RK%" OR add_username LIKE "DB%" OR add_username LIKE "R%" OR add_username LIKE "TX%" OR add_username LIKE "FB%" ) 					GROUP BY						warehouse_code,						date UNION					SELECT					CASE													WHEN							warehouse_code = "AFN" THEN								"HM_AA" ELSE warehouse_code 							END AS `warehouse`,							"putaway" AS group_w,							add_time date,							round(								(									IFNULL( sum( JSON_UNQUOTE ( JSON_EXTRACT ( work_parme_num, "$.instock.instock.piece_total" ) ) ), 0 ) + IFNULL( sum( JSON_UNQUOTE ( JSON_EXTRACT ( work_parme_num, "$.instock.return_instock.piece_total" ) ) ), 0 ) + IFNULL( sum( JSON_UNQUOTE ( JSON_EXTRACT ( work_parme_num, "$.instock.move_instock.piece_total" ) ) ), 0 ) + IFNULL( sum( JSON_UNQUOTE ( JSON_EXTRACT ( work_parme_num, "$.instock.instock_sku_allot.piece_total" ) ) ), 0 ) + IFNULL( sum( JSON_UNQUOTE ( JSON_EXTRACT ( work_parme_num, "$.instock.question_instock.piece_total" ) ) ), 0 ) 								),								2 							) AS `num` 						FROM							`ueb_work_num_log_history` 						WHERE							add_time NOT IN ( "num", "user_name", "warehouse_code" ) 							AND warehouse_code NOT IN ( "CX", "shzz", "AFN" ) 							AND ( user_name LIKE "L%" OR user_name LIKE "RK%" OR user_name LIKE "DB%" OR user_name LIKE "R%" OR user_name LIKE "TX%" OR user_name LIKE "FB%" ) 							AND TO_DAYS( NOW( ) ) - TO_DAYS( add_time ) <= 31 							AND TO_DAYS( NOW( ) ) - TO_DAYS( add_time ) NOT IN ( 0, 1 ) 						GROUP BY							`warehouse`,							add_time UNION						SELECT						CASE															WHEN								warehouse_code = "AFN" THEN									"HM_AA" ELSE warehouse_code 								END AS `warehouse`,								"pick" AS group_w,								add_time,								round(									(										IFNULL( sum( JSON_UNQUOTE ( JSON_EXTRACT ( work_parme_num, "$.pick.pick_single.piece_total" ) ) ), 0 ) + IFNULL( sum( JSON_UNQUOTE ( JSON_EXTRACT ( work_parme_num, "$.pick.pick_order.piece_total" ) ) ), 0 ) + IFNULL( sum( JSON_UNQUOTE ( JSON_EXTRACT ( work_parme_num, "$.pick.pick_multi.piece_total" ) ) ), 0 ) + IFNULL( sum( JSON_UNQUOTE ( JSON_EXTRACT ( work_parme_num, "$.pick.pick_sku_bao.piece_total" ) ) ), 0 ) + IFNULL( sum( JSON_UNQUOTE ( JSON_EXTRACT ( work_parme_num, "$.pick.pick_move.piece_total" ) ) ), 0 ) + IFNULL( sum( JSON_UNQUOTE ( JSON_EXTRACT ( work_parme_num, "$.pick.pick_single_more.piece_total" ) ) ), 0 ) 									),									2 								) AS `num` 							FROM								`ueb_work_num_log_history` 							WHERE								add_time NOT IN ( "num", "user_name", "warehouse_code" ) 								AND warehouse_code NOT IN ( "CX", "shzz", "AFN" ) 								AND ( user_name LIKE "L%" OR user_name LIKE "RK%" OR user_name LIKE "DB%" OR user_name LIKE "R%" OR user_name LIKE "TX%" OR user_name LIKE "FB%" ) 								AND TO_DAYS( NOW( ) ) - TO_DAYS( add_time ) <= 31 								AND TO_DAYS( NOW( ) ) - TO_DAYS( add_time ) NOT IN ( 0, 1 ) 							GROUP BY								add_time,								`warehouse` UNION							SELECT							CASE																	WHEN									warehouse_code = "AFN" THEN										"HM_AA" ELSE warehouse_code 									END AS `warehouse`,									"fba_pack" AS group_w,									add_time,									round( IFNULL( sum( JSON_UNQUOTE ( JSON_EXTRACT ( work_parme_num, "$.FBA.FBA.piece_total" ) ) ), 0 ), 2 ) AS `num` 								FROM									`ueb_work_num_log_history` 								WHERE									add_time NOT IN ( "num", "user_name", "warehouse_code" ) 									AND warehouse_code NOT IN ( "CX", "shzz", "AFN" ) 									AND ( user_name LIKE "L%" OR user_name LIKE "RK%" OR user_name LIKE "DB%" OR user_name LIKE "R%" OR user_name LIKE "TX%" OR user_name LIKE "FB%" ) 									AND TO_DAYS( NOW( ) ) - TO_DAYS( add_time ) <= 31 									AND TO_DAYS( NOW( ) ) - TO_DAYS( add_time ) NOT IN ( 0, 1 ) 								GROUP BY									add_time,									`warehouse` UNION								SELECT								CASE																			WHEN										warehouse_code = "AFN" THEN											"HM_AA" ELSE warehouse_code 										END AS `warehouse`,										"fba_change" AS group_w,										add_time,										round(											(												IFNULL( sum( JSON_UNQUOTE ( JSON_EXTRACT ( work_parme_num, "$.FBAPostCode.singlebatch_print_label.piece_total" ) ) ), 0 ) + IFNULL( sum( JSON_UNQUOTE ( JSON_EXTRACT ( work_parme_num, "$.FBAPostCode.singlebatch_print_label_FBC.piece_total" ) ) ), 0 ) + IFNULL( sum( JSON_UNQUOTE ( JSON_EXTRACT ( work_parme_num, "$.FBAPostCode.singlebatch_print_label_FBW.piece_total" ) ) ), 0 ) 											),											2 										) AS `num` 									FROM										`ueb_work_num_log_history` 									WHERE										add_time NOT IN ( "num", "user_name", "warehouse_code" ) 										AND warehouse_code NOT IN ( "CX", "shzz", "AFN" ) 										AND ( user_name LIKE "L%" OR user_name LIKE "RK%" OR user_name LIKE "DB%" OR user_name LIKE "R%" OR user_name LIKE "TX%" OR user_name LIKE "FB%" ) 										AND TO_DAYS( NOW( ) ) - TO_DAYS( add_time ) <= 31 										AND TO_DAYS( NOW( ) ) - TO_DAYS( add_time ) NOT IN ( 0, 1 ) 									GROUP BY										add_time,										`warehouse` 									) c ON a.warehouse_code = c.warehouse 									AND a.group_w = c.group_w 									AND a.date = c.date 								GROUP BY								a.warehouse_code,a.group_w'

    input = pd.read_excel('daily4.xlsx')
    see=save(input)
    act_1 = []
    act_2 = []
    act_3 = []
    act_4 = []
    temp_1 = []
    temp_2 = []
    temp_3 = []
    temp_4 = []
    jsonData = {}
    for data in see:
        act_1.append(data[3])
        act_2.append(data[4])
        act_3.append(data[5])
        act_4.append(data[9])
        temp_1.append(data[6])
        temp_2.append(data[7])
        temp_3.append(data[8])
        temp_4.append(data[10])

    jsonData['act_4'] = act_4
    j = json.dumps(jsonData, cls=DecimalEncoder)
    return (j)

@app.route('/daily5', methods=['POST'])
def fenbu_daily():
    #备用sql = 'select DATE_FORMAT(a.Date,"%m-%d"),a.warehouse_code 仓库,ifnull(b.num,0)未调拨,ifnull(c.num,0)调拨中,ifnull(d.num,0)待配库,ifnull(e.num,0)待分配拉单,ifnull(f.num,0)待拉单,ifnull(g.num,0)待拣货,ifnull(h.num,0)拣货中,ifnull(i.num,0)待打包,ifnull(j.num,0)待出库,ifnull(k.num,0)待交运,ifnull(l.num,0)待打印箱唛,ifnull(m.num,0)已打印箱唛,ifnull(n.num,0)待上传箱唛 from (select Date ,"HM_AA" as warehouse_code from date  where TO_DAYS(now())- TO_DAYS(date) <=10 and TO_DAYS(now())- TO_DAYS(date) >=0 union select Date ,"SZ_AA" as warehouse_code from date  where TO_DAYS(now())- TO_DAYS(date) <=10 and TO_DAYS(now())- TO_DAYS(date) >=0 )a left join(SELECT	warehouse_code,	DATE_FORMAT(greatest(created_time,paytime,order_pull_time,FROM_UNIXTIME(wait_pull_time)),"%Y-%m-%d")date,count( DISTINCT order_id )num FROM	ueb_order where  	order_id LIKE "ALLOT%" 	AND from_order_id LIKE "FB%"  and wh_order_status IN ( 1, 2 ) group by warehouse_code,date)b on a.warehouse_code = b.warehouse_code and a.Date = b.date left join(SELECT	warehouse_code,	DATE_FORMAT(greatest(created_time,paytime,order_pull_time,FROM_UNIXTIME(wait_pull_time)),"%Y-%m-%d")date,count( DISTINCT order_id )num FROM	ueb_order where  	order_id LIKE "ALLOT%" 	AND from_order_id LIKE "FB%"  and wh_order_status IN ( 3,4,7,8 ) and order_id not LIKE "ALLOT%"  group by warehouse_code,date)c on a.warehouse_code = c.warehouse_code and a.Date = c.date left join (SELECT	warehouse_code,	DATE_FORMAT(greatest(created_time,paytime,order_pull_time,FROM_UNIXTIME(wait_pull_time)),"%Y-%m-%d")date,count( DISTINCT order_id )num FROM	ueb_order where	batch_type = 6  and wh_order_status IN ( -1 ) and order_id not LIKE "ALLOT%"group by warehouse_code,date)d on a.warehouse_code = d.warehouse_code and a.Date = d.date  left join(SELECT	warehouse_code,	DATE_FORMAT(greatest(created_time,paytime,order_pull_time,FROM_UNIXTIME(wait_pull_time)),"%Y-%m-%d")date,count( DISTINCT order_id )num FROM	ueb_order where	batch_type = 6  and wh_order_status IN ( 1 ) and order_id not LIKE "ALLOT%"group by warehouse_code,date)e on a.warehouse_code = e.warehouse_code and a.Date = e.date  left join(SELECT	warehouse_code,	DATE_FORMAT(greatest(created_time,paytime,order_pull_time,FROM_UNIXTIME(wait_pull_time)),"%Y-%m-%d")date,count( DISTINCT order_id )num FROM	ueb_order where	batch_type = 6  and wh_order_status IN ( 2 )and order_id not LIKE "ALLOT%" group by warehouse_code,date)f on a.warehouse_code = f.warehouse_code and a.Date = f.date  left join (SELECT	warehouse_code,	DATE_FORMAT(greatest(created_time,paytime,order_pull_time,FROM_UNIXTIME(wait_pull_time)),"%Y-%m-%d")date,count( DISTINCT order_id )num FROM	ueb_order where	batch_type = 6  and wh_order_status IN ( 3 )and order_id not LIKE "ALLOT%" group by warehouse_code,date)g on a.warehouse_code = g.warehouse_code and a.Date = g.date  left join(SELECT	warehouse_code,	DATE_FORMAT(greatest(created_time,paytime,order_pull_time,FROM_UNIXTIME(wait_pull_time)),"%Y-%m-%d")date,count( DISTINCT order_id )num FROM	ueb_order where	batch_type = 6  and wh_order_status IN ( 4 )and order_id not LIKE "ALLOT%" group by warehouse_code,date)h on a.warehouse_code = h.warehouse_code and a.Date = h.date  left join (SELECT	warehouse_code,	DATE_FORMAT(greatest(created_time,paytime,order_pull_time,FROM_UNIXTIME(wait_pull_time)),"%Y-%m-%d")date,count( DISTINCT order_id )num FROM	ueb_order where	batch_type = 6  and wh_order_status IN ( 7 )and order_id not LIKE "ALLOT%" group by warehouse_code,date)i on a.warehouse_code = i.warehouse_code and a.Date = i.date  left join (SELECT	warehouse_code,	DATE_FORMAT(greatest(created_time,paytime,order_pull_time,FROM_UNIXTIME(wait_pull_time)),"%Y-%m-%d")date,count( DISTINCT order_id )num FROM	ueb_order where	batch_type = 6  and wh_order_status IN ( 8 )and order_id not LIKE "ALLOT%" group by warehouse_code,date)j on a.warehouse_code = j.warehouse_code and a.Date = j.date  left join (SELECT	warehouse_code,	DATE_FORMAT(greatest(created_time,paytime,order_pull_time,FROM_UNIXTIME(wait_pull_time)),"%Y-%m-%d")date,count( DISTINCT order_id )num FROM	ueb_order where	batch_type = 6  and wh_order_status IN ( 9 )and order_id not LIKE "ALLOT%" group by warehouse_code,date)k on a.warehouse_code = k.warehouse_code and a.Date = k.date  left join(SELECT	warehouse_code,	DATE_FORMAT(greatest(created_time,paytime,order_pull_time,FROM_UNIXTIME(wait_pull_time)),"%Y-%m-%d")date,count( DISTINCT order_id )num FROM	ueb_order where	batch_type = 6  and wh_order_status IN ( 17,19 )and order_id not LIKE "ALLOT%" group by warehouse_code,date)l on a.warehouse_code = l.warehouse_code and a.Date = l.date   left join (SELECT	warehouse_code,	DATE_FORMAT(created_time,"%Y-%m-%d")date,count( DISTINCT order_id )num FROM	ueb_order where	batch_type = 6  and wh_order_status IN ( 20 ) and order_id not LIKE "ALLOT%"group by warehouse_code,date)m on a.warehouse_code = m.warehouse_code and a.Date = m.date   left join (SELECT	warehouse_code,	DATE_FORMAT(created_time,"%Y-%m-%d")date,count( DISTINCT order_id )num FROM	ueb_order where	batch_type = 6  and wh_order_status IN ( 54 ) and order_id not LIKE "ALLOT%"group by warehouse_code,date)n on a.warehouse_code = n.warehouse_code and a.Date = n.date   '
    sql = ' select case when TO_DAYS(now())- TO_DAYS(a.Date) >=10 then  DATE_FORMAT(DATE_SUB(DATE_FORMAT(now(),"%Y-%m-%d"), interval "10 1:1:1" day) ,"%m-%d")  else DATE_FORMAT(a.Date,"%m-%d") end  as d,a.warehouse_code 仓库,sum(ifnull(o.num,0))待物流审核,sum(ifnull(b.num,0))未调拨,sum(ifnull(c.num,0))调拨中,sum(ifnull(d.num,0))待配库,sum(ifnull(e.num,0))待分配拉单,sum(ifnull(f.num,0))待拉单,sum(ifnull(g.num,0))待拣货,sum(ifnull(h.num,0))拣货中,sum(ifnull(i.num,0))待打包,sum(ifnull(j.num,0))待出库,sum(ifnull(k.num,0))待交运,sum(ifnull(l.num,0))待打印箱唛,sum(ifnull(m.num,0))已打印箱唛,sum(ifnull(n.num,0))待上传箱唛 from(select Date ,"HM_AA" as warehouse_code from date  where  TO_DAYS(now())- TO_DAYS(date) >=0 union select Date ,"SZ_AA" as warehouse_code from date  where  TO_DAYS(now())- TO_DAYS(date) >=0 )a left join(SELECT	warehouse_code,	DATE_FORMAT(greatest(created_time,paytime,order_pull_time,FROM_UNIXTIME(wait_pull_time)),"%Y-%m-%d")date,count( DISTINCT order_id )num FROM	ueb_order where  	order_id LIKE "ALLOT%" 	AND from_order_id LIKE "FB%"  and wh_order_status IN ( 1, 2 ) group by warehouse_code,date)b on a.warehouse_code = b.warehouse_code and a.Date = b.date left join(SELECT	warehouse_code,	DATE_FORMAT(greatest(created_time,paytime,order_pull_time,FROM_UNIXTIME(wait_pull_time)),"%Y-%m-%d")date,count( DISTINCT order_id )num FROM	ueb_order where  	order_id LIKE "ALLOT%" 	AND from_order_id LIKE "FB%"  and wh_order_status IN ( 3,4,7,8 ) and order_id not LIKE "ALLOT%"  group by warehouse_code,date)c on a.warehouse_code = c.warehouse_code and a.Date = c.date left join (SELECT	warehouse_code,	DATE_FORMAT(greatest(created_time,paytime,order_pull_time,FROM_UNIXTIME(wait_pull_time)),"%Y-%m-%d")date,count( DISTINCT order_id )num FROM	ueb_order where	batch_type = 6  and wh_order_status IN ( -1 ) and order_id not LIKE "ALLOT%"group by warehouse_code,date)d on a.warehouse_code = d.warehouse_code and a.Date = d.date  left join(SELECT	warehouse_code,	DATE_FORMAT(greatest(created_time,paytime,order_pull_time,FROM_UNIXTIME(wait_pull_time)),"%Y-%m-%d")date,count( DISTINCT order_id )num FROM	ueb_order where	batch_type = 6  and wh_order_status IN ( 1 ) and order_id not LIKE "ALLOT%"group by warehouse_code,date)e on a.warehouse_code = e.warehouse_code and a.Date = e.date  left join(SELECT	warehouse_code,	DATE_FORMAT(greatest(created_time,paytime,order_pull_time,FROM_UNIXTIME(wait_pull_time)),"%Y-%m-%d")date,count( DISTINCT order_id )num FROM	ueb_order where	batch_type = 6  and wh_order_status IN ( 2 )and order_id not LIKE "ALLOT%" group by warehouse_code,date)f on a.warehouse_code = f.warehouse_code and a.Date = f.date  left join (SELECT	warehouse_code,	DATE_FORMAT(greatest(created_time,paytime,order_pull_time,FROM_UNIXTIME(wait_pull_time)),"%Y-%m-%d")date,count( DISTINCT order_id )num FROM	ueb_order where	batch_type = 6  and wh_order_status IN ( 3 )and order_id not LIKE "ALLOT%" group by warehouse_code,date)g on a.warehouse_code = g.warehouse_code and a.Date = g.date  left join(SELECT	warehouse_code,	DATE_FORMAT(greatest(created_time,paytime,order_pull_time,FROM_UNIXTIME(wait_pull_time)),"%Y-%m-%d")date,count( DISTINCT order_id )num FROM	ueb_order where	batch_type = 6  and wh_order_status IN ( 4 )and order_id not LIKE "ALLOT%" group by warehouse_code,date)h on a.warehouse_code = h.warehouse_code and a.Date = h.date  left join (SELECT	warehouse_code,	DATE_FORMAT(greatest(created_time,paytime,order_pull_time,FROM_UNIXTIME(wait_pull_time)),"%Y-%m-%d")date,count( DISTINCT order_id )num FROM	ueb_order where	batch_type = 6  and wh_order_status IN ( 7 )and order_id not LIKE "ALLOT%" group by warehouse_code,date)i on a.warehouse_code = i.warehouse_code and a.Date = i.date  left join (SELECT	warehouse_code,	DATE_FORMAT(greatest(created_time,paytime,order_pull_time,FROM_UNIXTIME(wait_pull_time)),"%Y-%m-%d")date,count( DISTINCT order_id )num FROM	ueb_order where	batch_type = 6  and wh_order_status IN ( 8 )and order_id not LIKE "ALLOT%" group by warehouse_code,date)j on a.warehouse_code = j.warehouse_code and a.Date = j.date  left join (SELECT	warehouse_code,	DATE_FORMAT(greatest(created_time,paytime,order_pull_time,FROM_UNIXTIME(wait_pull_time)),"%Y-%m-%d")date,count( DISTINCT order_id )num FROM	ueb_order where	batch_type = 6  and wh_order_status IN ( 9 )and order_id not LIKE "ALLOT%" group by warehouse_code,date)k on a.warehouse_code = k.warehouse_code and a.Date = k.date  left join(SELECT	warehouse_code,	DATE_FORMAT(greatest(created_time,paytime,order_pull_time,FROM_UNIXTIME(wait_pull_time)),"%Y-%m-%d")date,count( DISTINCT order_id )num FROM	ueb_order where	batch_type = 6  and wh_order_status IN ( 17,19 )and order_id not LIKE "ALLOT%" group by warehouse_code,date)l on a.warehouse_code = l.warehouse_code and a.Date = l.date   left join (SELECT	warehouse_code,	DATE_FORMAT(created_time,"%Y-%m-%d")date,count( DISTINCT order_id )num FROM	ueb_order where	batch_type = 6  and wh_order_status IN ( 20 ) and order_id not LIKE "ALLOT%"group by warehouse_code,date)m on a.warehouse_code = m.warehouse_code and a.Date = m.date   left join (SELECT	warehouse_code,	DATE_FORMAT(created_time,"%Y-%m-%d")date,count( DISTINCT order_id )num FROM	ueb_order where	batch_type = 6  and wh_order_status IN ( 54 ) and order_id not LIKE "ALLOT%"group by warehouse_code,date)n on a.warehouse_code = n.warehouse_code and a.Date = n.date  left join (SELECT	warehouse_code,	DATE_FORMAT(created_time,"%Y-%m-%d")date,count( DISTINCT order_id )num FROM	ueb_order where	batch_type = 6  and is_pass_logistics=0 and order_id not LIKE "ALLOT%" and created_time >"2020-01-01" and complete_status=13 group by warehouse_code,date)o on a.warehouse_code = o.warehouse_code and a.Date = o.date group by a.warehouse_code,d'
    sql2 = 'SELECT CASE WHEN	TO_DAYS( now( ) ) - TO_DAYS( a.Date ) >= 10 THEN	DATE_FORMAT( DATE_SUB( DATE_FORMAT( now( ), "%Y-%m-%d" ), INTERVAL "10 1:1:1" DAY ), "%m-%d" ) ELSE DATE_FORMAT( a.Date, "%m-%d" ) 		END AS d,	a.warehouse_code 仓库,	sum( ifnull( b.num, 0 ) ) 遗留箱数,		sum( ifnull( c.num, 0 ) ) 遗留贴码,		sum( ifnull( e.num, 0 ) ) 遗留质检,			sum( ifnull( f.num, 0 ) )遗留上架 FROM	(	SELECT		Date,		"HM_AA" AS warehouse_code 	FROM		date 	WHERE		TO_DAYS( now( ) ) - TO_DAYS( date ) >=0  UNION	SELECT		Date,		"SZ_AA" AS warehouse_code 	FROM		date 	WHERE		TO_DAYS( now( ) ) - TO_DAYS( date ) >=0 	) a	LEFT JOIN (							select warehouse_code,DATE_FORMAT(add_time,"%Y-%m-%d")date ,sum(box_number) num											FROM						ueb_express_receipt 					where	STATUS = 1 	AND warehouse_type = 1 	AND is_abnormal = "2" 	AND is_quality = "2" 	AND is_end = "1" 	and quality_time is null	group by warehouse_code,date	) b ON a.warehouse_code = b.warehouse_code 	AND a.Date = b.date			LEFT JOIN (			SELECT	warehouse_code,	DATE_FORMAT(quality_start_time,"%Y-%m-%d")date,	count(DISTINCT purchase_order_no)num FROM	ueb_quality_warehousing_record WHERE	paragraph != 5 	and post_code_start_time IS NULL	AND purchase_order_no NOT LIKE "ABD%" 	AND warehouse_code IN ( "HM_AA", "SZ_AA" ) GROUP BY warehouse_code,date	) c ON a.warehouse_code = c.warehouse_code 	AND a.Date = c.date				LEFT JOIN (SELECT	warehouse_code,	DATE_FORMAT(quality_start_time,"%Y-%m-%d")date,	count(DISTINCT purchase_order_no)num FROM	ueb_quality_warehousing_record WHERE	paragraph != 5 and  post_code_start_time IS NOT NULL AND post_code_end_time IS NOT NULL AND quality_time IS NOT NULL AND paragraph = 11 AND upper_start_time IS NULL 	AND purchase_order_no NOT LIKE "ABD%" 	AND warehouse_code IN ( "HM_AA", "SZ_AA" ) GROUP BY warehouse_code,date	) e ON a.warehouse_code = e.warehouse_code 	AND a.Date = e.date				LEFT JOIN (SELECT	warehouse_code,	DATE_FORMAT(quality_start_time,"%Y-%m-%d")date,	count(DISTINCT purchase_order_no)num FROM	ueb_quality_warehousing_record WHERE	paragraph != 5 and post_code_start_time IS NOT NULL AND post_code_end_time IS NOT NULL AND quality_time IS NOT NULL AND paragraph != 11 AND upper_start_time IS NULL	AND purchase_order_no NOT LIKE "ABD%" 	AND warehouse_code IN ( "HM_AA", "SZ_AA" ) GROUP BY warehouse_code,date	) f ON a.warehouse_code = f.warehouse_code 	AND a.Date = f.date													 group by 	a.warehouse_code,d'

    input = pd.read_excel('daily5_sql.xlsx')
    see=save(input)

    jsonData = {}
    see = pd.DataFrame(see)
    hm_fba_1 = see[0][(see[1]=='HM_AA')]
    hm_fba_1 = np.array(hm_fba_1).tolist()
    hm_fba_2 = see[2][(see[1]=='HM_AA')]
    hm_fba_2 = np.array(hm_fba_2).tolist()
    hm_fba_3 = see[3][(see[1]=='HM_AA')]
    hm_fba_3 = np.array(hm_fba_3).tolist()
    hm_fba_4 = see[4][(see[1]=='HM_AA')]
    hm_fba_4 = np.array(hm_fba_4).tolist()
    hm_fba_5 = see[6][(see[1]=='HM_AA')]
    hm_fba_5 = np.array(hm_fba_5).tolist()
    hm_fba_6 = see[7][(see[1]=='HM_AA')]
    hm_fba_6 = np.array(hm_fba_6).tolist()
    hm_fba_7 = see[9][(see[1]=='HM_AA')]
    hm_fba_7 = np.array(hm_fba_7).tolist()
    hm_fba_8 = see[10][(see[1]=='HM_AA')]
    hm_fba_8 = np.array(hm_fba_8).tolist()
    hm_fba_9 = see[12][(see[1]=='HM_AA')]
    hm_fba_9 = np.array(hm_fba_9).tolist()
    hm_fba_10 = see[13][(see[1]=='HM_AA')]
    hm_fba_10 = np.array(hm_fba_10).tolist()
    hm_fba_11 = see[14][(see[1]=='HM_AA')]
    hm_fba_11 = np.array(hm_fba_11).tolist()
    hm_fba_12 = see[15][(see[1]=='HM_AA')]
    hm_fba_12 = np.array(hm_fba_12).tolist()
    tx_fba_1 = see[0][(see[1]=='SZ_AA')]
    tx_fba_1 = np.array(tx_fba_1).tolist()
    tx_fba_2 = see[2][(see[1]=='SZ_AA')]
    tx_fba_2 = np.array(tx_fba_2).tolist()
    tx_fba_3 = see[3][(see[1]=='SZ_AA')]
    tx_fba_3 = np.array(tx_fba_3).tolist()
    tx_fba_4 = see[4][(see[1]=='SZ_AA')]
    tx_fba_4 = np.array(tx_fba_4).tolist()
    tx_fba_5 = see[6][(see[1]=='SZ_AA')]
    tx_fba_5 = np.array(tx_fba_5).tolist()
    tx_fba_6 = see[7][(see[1]=='SZ_AA')]
    tx_fba_6 = np.array(tx_fba_6).tolist()
    tx_fba_7 = see[9][(see[1]=='SZ_AA')]
    tx_fba_7 = np.array(tx_fba_7).tolist()
    tx_fba_8 = see[10][(see[1]=='SZ_AA')]
    tx_fba_8 = np.array(tx_fba_8).tolist()
    tx_fba_9 = see[12][(see[1]=='SZ_AA')]
    tx_fba_9 = np.array(tx_fba_9).tolist()
    tx_fba_10 = see[13][(see[1]=='SZ_AA')]
    tx_fba_10 = np.array(tx_fba_10).tolist()
    tx_fba_11 = see[14][(see[1]=='SZ_AA')]
    tx_fba_11 = np.array(tx_fba_11).tolist()
    tx_fba_12 = see[15][(see[1]=='SZ_AA')]
    tx_fba_12 = np.array(tx_fba_12).tolist()
    jsonData['hm_fba_1']=hm_fba_1
    jsonData['hm_fba_2']=hm_fba_2
    jsonData['hm_fba_3']=hm_fba_3
    jsonData['hm_fba_4']=hm_fba_4
    jsonData['hm_fba_5']=hm_fba_5
    jsonData['hm_fba_6']=hm_fba_6
    jsonData['hm_fba_7']=hm_fba_7
    jsonData['hm_fba_8']=hm_fba_8
    jsonData['hm_fba_9']=hm_fba_9
    jsonData['hm_fba_10']=hm_fba_10
    jsonData['hm_fba_11']=hm_fba_11
    jsonData['hm_fba_12']=hm_fba_12
    jsonData['tx_fba_1']=tx_fba_1
    jsonData['tx_fba_2']=tx_fba_2
    jsonData['tx_fba_3']=tx_fba_3
    jsonData['tx_fba_4']=tx_fba_4
    jsonData['tx_fba_5']=tx_fba_5
    jsonData['tx_fba_6']=tx_fba_6
    jsonData['tx_fba_7']=tx_fba_7
    jsonData['tx_fba_8']=tx_fba_8
    jsonData['tx_fba_9']=tx_fba_9
    jsonData['tx_fba_10']=tx_fba_10
    jsonData['tx_fba_11']=tx_fba_11
    jsonData['tx_fba_12'] = tx_fba_12

    input = pd.read_excel('daily5_sql2.xlsx')
    see=save(input)
    see = pd.DataFrame(see)
    hm_xb_1 = see[0][(see[1]=='HM_AA')]
    hm_xb_1 = np.array(hm_xb_1).tolist()
    hm_xb_2 = see[2][(see[1]=='HM_AA')]
    hm_xb_2 = np.array(hm_xb_2).tolist()
    hm_xb_3 = see[3][(see[1]=='HM_AA')]
    hm_xb_3 = np.array(hm_xb_3).tolist()
    hm_xb_4 = see[4][(see[1]=='HM_AA')]
    hm_xb_4 = np.array(hm_xb_4).tolist()
    hm_xb_5 = see[5][(see[1]=='HM_AA')]
    hm_xb_5 = np.array(hm_xb_5).tolist()
    tx_xb_1 = see[0][(see[1]=='SZ_AA')]
    tx_xb_1 = np.array(tx_xb_1).tolist()
    tx_xb_2 = see[2][(see[1]=='SZ_AA')]
    tx_xb_2 = np.array(tx_xb_2).tolist()
    tx_xb_3 = see[3][(see[1]=='SZ_AA')]
    tx_xb_3 = np.array(tx_xb_3).tolist()
    tx_xb_4 = see[4][(see[1]=='SZ_AA')]
    tx_xb_4 = np.array(tx_xb_4).tolist()
    tx_xb_5 = see[5][(see[1]=='SZ_AA')]
    tx_xb_5 = np.array(tx_xb_5).tolist()

    jsonData['hm_xb_1']=hm_xb_1
    jsonData['hm_xb_2']=hm_xb_2
    jsonData['hm_xb_3']=hm_xb_3
    jsonData['hm_xb_4']=hm_xb_4
    jsonData['hm_xb_5']=hm_xb_5

    jsonData['tx_xb_1']=tx_xb_1
    jsonData['tx_xb_2']=tx_xb_2
    jsonData['tx_xb_3']=tx_xb_3
    jsonData['tx_xb_4']=tx_xb_4
    jsonData['tx_xb_5']=tx_xb_5

    j = json.dumps(jsonData, cls=DecimalEncoder)
    return (j)



# url_for,修改静态文件（js,css,image)时，网页同步修改
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    filename = None
    if endpoint == 'static':
        filename = values.get('filename', None)
    if filename:
        file_path = path.join(app.root_path, endpoint, filename)
        values['v'] = int(stat(file_path).st_mtime)
    return url_for(endpoint, **values)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
