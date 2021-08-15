import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import preprocessing

import pandas as pd
from TushareData import TuShareData
from PyechartsData2 import saveMutStockToHtlm

# 核心代码，设置显示的最大列、宽等参数，消掉打印不完全中间的省略号
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

cnames = [
    '#F0F8FF',
    '#FAEBD7',
    '#00FFFF',
    '#7FFFD4',
    '#F0FFFF',
    '#F5F5DC',
    '#FFE4C4',
    '#000000',
    '#FFEBCD',
    '#0000FF',
    '#8A2BE2',
    '#A52A2A',
    '#DEB887',
    '#5F9EA0',
    '#7FFF00',
    '#D2691E',
    '#FF7F50',
    '#6495ED',
    '#FFF8DC',
    '#DC143C',
    '#00FFFF',
    '#00008B',
    '#008B8B',
    '#B8860B',
    '#A9A9A9',
    '#006400',
    '#BDB76B',
    '#8B008B',
    '#556B2F',
    '#FF8C00',
    '#9932CC',
    '#8B0000',
    '#E9967A',
    '#8FBC8F',
    '#483D8B',
    '#2F4F4F',
    '#00CED1',
    '#9400D3',
    '#FF1493',
    '#00BFFF',
    '#696969',
    '#1E90FF',
    '#B22222',
    '#FFFAF0',
    '#228B22',
    '#FF00FF',
    '#DCDCDC',
    '#F8F8FF',
    '#FFD700',
    '#DAA520',
    '#808080',
    '#008000',
    '#ADFF2F',
    '#F0FFF0',
    '#FF69B4',
    '#CD5C5C',
    '#4B0082',
    '#FFFFF0',
    '#F0E68C',
    '#E6E6FA',
    '#FFF0F5',
    '#7CFC00',
    '#FFFACD',
    '#ADD8E6',
    '#F08080',
    '#E0FFFF',
    '#FAFAD2',
    '#90EE90',
    '#D3D3D3',
    '#FFB6C1',
    '#FFA07A',
    '#20B2AA',
    '#87CEFA',
    '#778899',
    '#B0C4DE',
    '#FFFFE0',
    '#00FF00',
    '#32CD32',
    '#FAF0E6',
    '#FF00FF',
    '#800000',
    '#66CDAA',
    '#0000CD',
    '#BA55D3',
    '#9370DB',
    '#3CB371',
    '#7B68EE',
    '#00FA9A',
    '#48D1CC',
    '#C71585',
    '#191970',
    '#F5FFFA',
    '#FFE4E1',
    '#FFE4B5',
    '#FFDEAD',
    '#000080',
    '#FDF5E6',
    '#808000',
    '#6B8E23',
    '#FFA500',
    '#FF4500',
    '#DA70D6',
    '#EEE8AA',
    '#98FB98',
    '#AFEEEE',
    '#DB7093',
    '#FFEFD5',
    '#FFDAB9',
    '#CD853F',
    '#FFC0CB',
    '#DDA0DD',
    '#B0E0E6',
    '#800080',
    '#FF0000',
    '#BC8F8F',
    '#4169E1',
    '#8B4513',
    '#FA8072',
    '#FAA460',
    '#2E8B57',
    '#FFF5EE',
    '#A0522D',
    '#C0C0C0',
    '#87CEEB',
    '#6A5ACD',
    '#708090',
    '#FFFAFA',
    '#00FF7F',
    '#4682B4',
    '#D2B48C',
    '#008080',
    '#D8BFD8',
    '#FF6347',
    '#40E0D0',
    '#EE82EE',
    '#F5DEB3',
    '#FFFFFF',
    '#F5F5F5',
    '#FFFF00',
    '#9ACD32'
]


cnames_ = {
'aliceblue':            '#F0F8FF',
'antiquewhite':         '#FAEBD7',
'aqua':                 '#00FFFF',
'aquamarine':           '#7FFFD4',
'azure':                '#F0FFFF',
'beige':                '#F5F5DC',
'bisque':               '#FFE4C4',
'black':                '#000000',
'blanchedalmond':       '#FFEBCD',
'blue':                 '#0000FF',
'blueviolet':           '#8A2BE2',
'brown':                '#A52A2A',
'burlywood':            '#DEB887',
'cadetblue':            '#5F9EA0',
'chartreuse':           '#7FFF00',
'chocolate':            '#D2691E',
'coral':                '#FF7F50',
'cornflowerblue':       '#6495ED',
'cornsilk':             '#FFF8DC',
'crimson':              '#DC143C',
'cyan':                 '#00FFFF',
'darkblue':             '#00008B',
'darkcyan':             '#008B8B',
'darkgoldenrod':        '#B8860B',
'darkgray':             '#A9A9A9',
'darkgreen':            '#006400',
'darkkhaki':            '#BDB76B',
'darkmagenta':          '#8B008B',
'darkolivegreen':       '#556B2F',
'darkorange':           '#FF8C00',
'darkorchid':           '#9932CC',
'darkred':              '#8B0000',
'darksalmon':           '#E9967A',
'darkseagreen':         '#8FBC8F',
'darkslateblue':        '#483D8B',
'darkslategray':        '#2F4F4F',
'darkturquoise':        '#00CED1',
'darkviolet':           '#9400D3',
'deeppink':             '#FF1493',
'deepskyblue':          '#00BFFF',
'dimgray':              '#696969',
'dodgerblue':           '#1E90FF',
'firebrick':            '#B22222',
'floralwhite':          '#FFFAF0',
'forestgreen':          '#228B22',
'fuchsia':              '#FF00FF',
'gainsboro':            '#DCDCDC',
'ghostwhite':           '#F8F8FF',
'gold':                 '#FFD700',
'goldenrod':            '#DAA520',
'gray':                 '#808080',
'green':                '#008000',
'greenyellow':          '#ADFF2F',
'honeydew':             '#F0FFF0',
'hotpink':              '#FF69B4',
'indianred':            '#CD5C5C',
'indigo':               '#4B0082',
'ivory':                '#FFFFF0',
'khaki':                '#F0E68C',
'lavender':             '#E6E6FA',
'lavenderblush':        '#FFF0F5',
'lawngreen':            '#7CFC00',
'lemonchiffon':         '#FFFACD',
'lightblue':            '#ADD8E6',
'lightcoral':           '#F08080',
'lightcyan':            '#E0FFFF',
'lightgoldenrodyellow': '#FAFAD2',
'lightgreen':           '#90EE90',
'lightgray':            '#D3D3D3',
'lightpink':            '#FFB6C1',
'lightsalmon':          '#FFA07A',
'lightseagreen':        '#20B2AA',
'lightskyblue':         '#87CEFA',
'lightslategray':       '#778899',
'lightsteelblue':       '#B0C4DE',
'lightyellow':          '#FFFFE0',
'lime':                 '#00FF00',
'limegreen':            '#32CD32',
'linen':                '#FAF0E6',
'magenta':              '#FF00FF',
'maroon':               '#800000',
'mediumaquamarine':     '#66CDAA',
'mediumblue':           '#0000CD',
'mediumorchid':         '#BA55D3',
'mediumpurple':         '#9370DB',
'mediumseagreen':       '#3CB371',
'mediumslateblue':      '#7B68EE',
'mediumspringgreen':    '#00FA9A',
'mediumturquoise':      '#48D1CC',
'mediumvioletred':      '#C71585',
'midnightblue':         '#191970',
'mintcream':            '#F5FFFA',
'mistyrose':            '#FFE4E1',
'moccasin':             '#FFE4B5',
'navajowhite':          '#FFDEAD',
'navy':                 '#000080',
'oldlace':              '#FDF5E6',
'olive':                '#808000',
'olivedrab':            '#6B8E23',
'orange':               '#FFA500',
'orangered':            '#FF4500',
'orchid':               '#DA70D6',
'palegoldenrod':        '#EEE8AA',
'palegreen':            '#98FB98',
'paleturquoise':        '#AFEEEE',
'palevioletred':        '#DB7093',
'papayawhip':           '#FFEFD5',
'peachpuff':            '#FFDAB9',
'peru':                 '#CD853F',
'pink':                 '#FFC0CB',
'plum':                 '#DDA0DD',
'powderblue':           '#B0E0E6',
'purple':               '#800080',
'red':                  '#FF0000',
'rosybrown':            '#BC8F8F',
'royalblue':            '#4169E1',
'saddlebrown':          '#8B4513',
'salmon':               '#FA8072',
'sandybrown':           '#FAA460',
'seagreen':             '#2E8B57',
'seashell':             '#FFF5EE',
'sienna':               '#A0522D',
'silver':               '#C0C0C0',
'skyblue':              '#87CEEB',
'slateblue':            '#6A5ACD',
'slategray':            '#708090',
'snow':                 '#FFFAFA',
'springgreen':          '#00FF7F',
'steelblue':            '#4682B4',
'tan':                  '#D2B48C',
'teal':                 '#008080',
'thistle':              '#D8BFD8',
'tomato':               '#FF6347',
'turquoise':            '#40E0D0',
'violet':               '#EE82EE',
'wheat':                '#F5DEB3',
'white':                '#FFFFFF',
'whitesmoke':           '#F5F5F5',
'yellow':               '#FFFF00',
'yellowgreen':          '#9ACD32'
}

class FilterStock():
    def __init__(self):
        pass

    def filter_close_data(self, table, basic):
        '''
        过滤出所有股票的收盘数据
        '''
        basic_list = []
        data_list = []
        for key in sorted(table.keys()):
            #name = []
            filter_data = []
            data = table[key]
            for line in data:
                #name.append(line[0])
                filter_data.append(line[5])
            # 归一化
            filter_data = preprocessing.minmax_scale(filter_data)

            data_list.append(filter_data)
            basic_list.append(basic[key])
        data_list = np.array(data_list)
        basic_list = np.array(basic_list)
        return data_list, basic_list

    def filter_rate_data(self, table, basic):
        '''
        过滤出涨幅数据
        '''
        basic_list = []
        data_list = []
        for key in sorted(table.keys()):
            filter_data = []
            data = table[key]
            price_last = 0
            for line in data:
                if price_last == 0:
                    price_last = line[5]
                rate = (line[5] - price_last) / price_last # 计算涨幅
                filter_data.append(rate)
            # 归一化
            filter_data = preprocessing.minmax_scale(filter_data)
            data_list.append(filter_data)
            basic_list.append(basic[key])
        data_list = np.array(data_list)
        basic_list = np.array(basic_list)
        return data_list, basic_list


    def do_kmeans(self, data_list, basic_list, clusters):
        estimator = KMeans(n_clusters=clusters)
        estimator.fit(data_list)
        label_pred = estimator.labels_
        label_pred = np.array(label_pred)
        sort_list = [] # 分类后的 basic_list，比它高一个维度
        for i in range(clusters):
            n = basic_list[label_pred == int(i)]
            d = data_list[label_pred == int(i)]
            #np.savetxt("./output/%d.txt"%(i), n[:, 0], fmt='%s')
            sort_list.append(n)
            try:
                np.savetxt("./output/%d.txt"%(i), n, fmt='%s')
            except:
                pass
            #plt.scatter(d[:, 1], d[:,2], c=cnames[i])
        #plt.xlabel('x')
        #plt.ylabel('y')
        #plt.legend(loc=2)
        #plt.show()
        print("KMean Done!")
        return sort_list

    def save_sort_to_html(self, table, sort_list):
        '''
        将计算得到的分类数据保存为 html
        '''
        draw = saveMutStockToHtlm()
        for index, sort in enumerate(sort_list):
            html_mut_stock_input = [] # 一组的股票数据
            for line in sort:
                html_one_stock_input = {"title": None, "data": None}
                try:
                    title = line[0] + "_" + line[2] + "_" + line[3] + "_" + line[4]
                except:
                    continue
                html_one_stock_input["title"] = title

                code = line[0] # 股票代码
                all_day = table[code] # 股票数据
                data = []
                for one_day in all_day: # 日数据
                    d = []
                    d.append(one_day[1]) # date
                    d.append(one_day[2]) # open
                    d.append(one_day[5]) # close
                    d.append(one_day[4]) # low
                    d.append(one_day[3]) # high
                    data.append(d)
                html_one_stock_input["data"] = np.array(data)
                html_mut_stock_input.append(html_one_stock_input)
            draw.drawMutStock("output/%d.html" % (index), html_mut_stock_input)


if __name__ == "__main__":
    tu = TuShareData()
    table, basic = tu.getAllStockByDate(start_date='20190701', end_date='20210722')
    filter = FilterStock()
    data_list, basic_list = filter.filter_close_data(table, basic)
    sort_list = filter.do_kmeans(data_list=data_list, basic_list=basic_list, clusters=500)
    filter.save_sort_to_html(table, sort_list)
    #print(name_list)
    #print(data_list)