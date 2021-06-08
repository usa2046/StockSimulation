from pyecharts import options as opts
from pyecharts.charts import Kline

data = [
    [2320.26, 2320.26, 2287.3, 2362.94],
    [2300, 2291.3, 2288.26, 2308.38],
    [2295.35, 2346.5, 2295.35, 2345.92],
    [2347.22, 2358.98, 2337.35, 2363.8],
    [2360.75, 2382.48, 2347.89, 2383.76],
    [2383.43, 2385.42, 2371.23, 2391.82],
    [2377.41, 2419.02, 2369.57, 2421.15],
    [2425.92, 2428.15, 2417.58, 2440.38],
    [2411, 2433.13, 2403.3, 2437.42],
    [2432.68, 2334.48, 2427.7, 2441.73],
    [2430.69, 2418.53, 2394.22, 2433.89],
    [2416.62, 2432.4, 2414.4, 2443.03],
    [2441.91, 2421.56, 2418.43, 2444.8],
    [2420.26, 2382.91, 2373.53, 2427.07],
    [2383.49, 2397.18, 2370.61, 2397.94],
    [2378.82, 2325.95, 2309.17, 2378.82],
    [2322.94, 2314.16, 2308.76, 2330.88],
    [2320.62, 2325.82, 2315.01, 2338.78],
    [2313.74, 2293.34, 2289.89, 2340.71],
    [2297.77, 2313.22, 2292.03, 2324.63],
    [2322.32, 2365.59, 2308.92, 2366.16],
    [2364.54, 2359.51, 2330.86, 2369.65],
    [2332.08, 2273.4, 2259.25, 2333.54],
    [2274.81, 2326.31, 2270.1, 2328.14],
    [2333.61, 2347.18, 2321.6, 2351.44],
    [2340.44, 2324.29, 2304.27, 2352.02],
    [2326.42, 2318.61, 2314.59, 2333.67],
    [2314.68, 2310.59, 2296.58, 2320.96],
    [2309.16, 2286.6, 2264.83, 2333.29],
    [2282.17, 2263.97, 2253.25, 2286.33],
    [2255.77, 2270.28, 2253.31, 2276.22],
]

c = (
#    Kline(
#		init_opts=opts.InitOpts(
#			width="750px", # 画布宽度
#			height="500px", # 画布高度
#			js_host="http://www.tamray.cn/" # js资源加载地址，可以不用这行，它有默认地址
#		)
#    )
    Kline()
    .add_xaxis(["2017/7/{}".format(i + 1) for i in range(31)])
    .add_yaxis("kline", data)
    .set_global_opts(
        xaxis_opts=opts.AxisOpts(is_scale=True),
        yaxis_opts=opts.AxisOpts(
            is_scale=True,
            splitarea_opts=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1) # 根据坐标刻度来高亮图表背景
            ),
        ),
        datazoom_opts=[opts.DataZoomOpts(pos_bottom="-2%")], # 缩放功能
        title_opts=opts.TitleOpts(title="Kline-DataZoom-slider-Position"), # 设置主标题
    )
    .render("data.html") # 生成的 html 文件名
)

# 叠加图表
#line = (
#        Line()
#        .add_xaxis(time)
#        .add_yaxis("", data3, color="#bf0500", label_opts=opts.LabelOpts(is_show=False))
#    )
#c.overlap(line)
#c.render("render.html")


class KLineHtml():
    def __init__(self):
        return

    def creat(self, xaxis, yaxis, save_path, width=750, height=500):
        x = []
        y = []
        for index in reversed(range(len(xaxis))):
            x.append(xaxis[index])
            y.append(yaxis[index])
        k = (
            Kline(
                init_opts=opts.InitOpts(
                    #width="800px", # 画布宽度
                    #height="500px", # 画布高度
                    width="{}px".format(width),  # 画布宽度
                    height="{}px".format(height),  # 画布高度
                )
            )
            .add_xaxis(["{}".format(i) for i in x])
            .add_yaxis("kline",
                y,
            )
            .set_global_opts(
                xaxis_opts=opts.AxisOpts(is_scale=True),
                yaxis_opts=opts.AxisOpts(
                    is_scale=True,
                    splitarea_opts=opts.SplitAreaOpts(
                        is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)  # 根据坐标刻度来高亮图表背景
                    ),
                ),
                datazoom_opts=[opts.DataZoomOpts(pos_bottom="-2%")],  # 缩放功能
                #datazoom_opts=[opts.DataZoomOpts(pos_bottom="-2%")],  # 缩放功能
                title_opts=opts.TitleOpts(title="Kline"),  # 设置主标题
            )
            .set_series_opts(
                label_opts=opts.LabelOpts(is_show=False),
                # MarkLineOpts：标记线配置项
                markline_opts=opts.MarkLineOpts(
                    data=[
                        opts.MarkLineItem(
                            name="自定义线",
                            y=10,
                        )],
                    label_opts=opts.LabelOpts(),

                    #linestyle_opts=opts.LineStyleOpts(width=3, color='#FFFF00', )
                ),
            )
        )
        print(save_path)
        k.render(save_path)