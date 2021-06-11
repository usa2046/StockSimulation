import requests
from typing import List, Union

from pyecharts import options as opts
from pyecharts.charts import Kline, Line, Bar, Grid
from pyecharts.globals import ThemeType

class saveToHtml():
    def __init__(self):
        return

    def get_data(self):
        response = requests.get(
            url="https://echarts.apache.org/examples/data/asset/data/stock-DJI.json"
        )
        json_response = response.json()
        # 解析数据
        return self.split_data(data=json_response)


    def split_data(self, data):
        category_data = []
        values = []
        volumes = []
        stock_cost = [] # 股票成本
        money_market = [] # 市值
        money_distr = [] # 可支配金额

        for i, tick in (enumerate(data)):
            category_data.append(tick[0])
            values.append(tick)
            volumes.append([i, tick[5], 1 if tick[1] > tick[2] else -1])
            if tick[6] > 1.15 * tick[2]:
                tick[6] = 1.15 * tick[2]
            elif tick[6] < 0.85 * tick[2]:
                tick[6] = 0.85 * tick[2]
            stock_cost.append(tick[6])
            money_market.append([i, tick[7], 1])
            money_distr.append([i, tick[8], -1])
        return {"categoryData": category_data,
                "values": values,
                "volumes": volumes,
                "stock_cost": stock_cost,
                "money_market": money_market,
                "money_distr": money_distr}


    def calculate_ma(self, day_count: int, data):
        result: List[Union[float, str]] = []
        for i in range(len(data["values"])):
            if i < day_count:
                result.append("-")
                continue
            sum_total = 0.0
            for j in range(day_count):
                sum_total += float(data["values"][i - j][1])
            result.append(abs(float("%.3f" % (sum_total / day_count))))
        return result


    def draw_charts(self, chart_data):
        l = len(chart_data['categoryData'])
        slider_progress = 100 * (l - 20) / l
        kline_data = [data[1:-1] for data in chart_data["values"]]
        kline = (
            Kline()
            .add_xaxis(xaxis_data=chart_data["categoryData"])
            .add_yaxis(
                series_name="Dow-Jones index",
                y_axis=kline_data,
                itemstyle_opts=opts.ItemStyleOpts(color="#ec0000", color0="#00da3c"),
            )
            .set_global_opts(
                legend_opts=opts.LegendOpts(
                    is_show=False, pos_bottom=10, pos_left="center"
                ),
                datazoom_opts=[
                    opts.DataZoomOpts(
                        is_show=False,
                        type_="inside",
                        xaxis_index=[0, 1],
                        range_start=slider_progress,
                        range_end=100,
                    ),
                    opts.DataZoomOpts(
                        is_show=True,
                        xaxis_index=[0, 1],
                        type_="slider",
                        pos_top="85%",
                        range_start=98,
                        range_end=100,
                    ),
                ],
                yaxis_opts=opts.AxisOpts(
                    is_scale=True,
                    splitarea_opts=opts.SplitAreaOpts(
                        is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                    ),
                ),
                tooltip_opts=opts.TooltipOpts(
                    trigger="axis",
                    axis_pointer_type="cross",
                    background_color="rgba(245, 245, 245, 0.8)",
                    border_width=1,
                    border_color="#ccc",
                    textstyle_opts=opts.TextStyleOpts(color="#000"),
                ),
                visualmap_opts=opts.VisualMapOpts(
                    is_show=False,
                    dimension=2,
                    series_index=5,
                    is_piecewise=True,
                    pieces=[
                        {"value": 1, "color": "#00da3c"},
                        {"value": -1, "color": "#ec0000"},
                    ],
                ),
                axispointer_opts=opts.AxisPointerOpts(
                    is_show=True,
                    link=[{"xAxisIndex": "all"}],
                    label=opts.LabelOpts(background_color="#777"),
                ),
                brush_opts=opts.BrushOpts(
                    x_axis_index="all",
                    brush_link="all",
                    out_of_brush={"colorAlpha": 0.1},
                    brush_type="lineX",
                ),
            )
        )

        line = (
            Line()
            .add_xaxis(xaxis_data=chart_data["categoryData"])
            #.add_yaxis(
            #    series_name="MA5",
            #    y_axis=self.calculate_ma(day_count=5, data=chart_data),
            #    is_smooth=True,
            #    is_hover_animation=False,
            #    linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
            #    label_opts=opts.LabelOpts(is_show=False),
            #)
            #.add_yaxis(
            #    series_name="MA10",
            #    y_axis=self.calculate_ma(day_count=10, data=chart_data),
            #    is_smooth=True,
            #    is_hover_animation=False,
            #    linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
            #    label_opts=opts.LabelOpts(is_show=False),
            #)
            #.add_yaxis(
            #    series_name="MA20",
            #    y_axis=self.calculate_ma(day_count=20, data=chart_data),
            #    is_smooth=True,
            #    is_hover_animation=False,
            #    linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
            #    label_opts=opts.LabelOpts(is_show=False),
            #)
            #.add_yaxis(
            #    series_name="MA30",
            #    y_axis=self.calculate_ma(day_count=30, data=chart_data),
            #    is_smooth=True,
            #    is_hover_animation=False,
            #    linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
            #    label_opts=opts.LabelOpts(is_show=False),
            #)
            .add_yaxis(
                series_name="STOCK",
                y_axis=chart_data["stock_cost"],
                is_smooth=True,
                is_hover_animation=False,
                linestyle_opts=opts.LineStyleOpts(width=5, opacity=0.5),
                label_opts=opts.LabelOpts(is_show=False),
            )
            .set_global_opts(xaxis_opts=opts.AxisOpts(type_="category"))
        )

        bar_0 = (
            Bar()
            .add_xaxis(xaxis_data=chart_data["categoryData"])
            .add_yaxis(
                series_name="market",
                y_axis=chart_data["money_market"],
                stack='stack0',
                #category_gap="50%",
                label_opts=opts.LabelOpts(is_show=False),
            )
            .add_yaxis(
                series_name="distr",
                y_axis=chart_data["money_distr"],
                stack='stack0',
                #category_gap="50%",
                label_opts=opts.LabelOpts(is_show=False),
            )
            .set_global_opts(
                xaxis_opts=opts.AxisOpts(
                    type_="category",
                    is_scale=True,
                    grid_index=1,
                    boundary_gap=False,
                    axisline_opts=opts.AxisLineOpts(is_on_zero=False),
                    axistick_opts=opts.AxisTickOpts(is_show=False),
                    splitline_opts=opts.SplitLineOpts(is_show=False),
                    axislabel_opts=opts.LabelOpts(is_show=False),
                    split_number=20,
                    min_="dataMin",
                    max_="dataMax",
                ),
                yaxis_opts=opts.AxisOpts(
                    grid_index=1,
                    is_scale=True,
                    split_number=2,
                    axislabel_opts=opts.LabelOpts(is_show=False),
                    axisline_opts=opts.AxisLineOpts(is_show=False),
                    axistick_opts=opts.AxisTickOpts(is_show=False),
                    splitline_opts=opts.SplitLineOpts(is_show=False),
                ),
                legend_opts=opts.LegendOpts(is_show=False),
            )
        )

        bar = (
            Bar()
            .add_xaxis(xaxis_data=chart_data["categoryData"])
            .add_yaxis(
                series_name="Volume",
                y_axis=chart_data["volumes"],
                xaxis_index=1,
                yaxis_index=1,
                label_opts=opts.LabelOpts(is_show=False),
            )
            .set_global_opts(
                xaxis_opts=opts.AxisOpts(
                    type_="category",
                    is_scale=True,
                    grid_index=1,
                    boundary_gap=False,
                    axisline_opts=opts.AxisLineOpts(is_on_zero=False),
                    axistick_opts=opts.AxisTickOpts(is_show=False),
                    splitline_opts=opts.SplitLineOpts(is_show=False),
                    axislabel_opts=opts.LabelOpts(is_show=False),
                    split_number=20,
                    min_="dataMin",
                    max_="dataMax",
                ),
                yaxis_opts=opts.AxisOpts(
                    grid_index=1,
                    is_scale=True,
                    split_number=2,
                    axislabel_opts=opts.LabelOpts(is_show=False),
                    axisline_opts=opts.AxisLineOpts(is_show=False),
                    axistick_opts=opts.AxisTickOpts(is_show=False),
                    splitline_opts=opts.SplitLineOpts(is_show=False),
                ),
                legend_opts=opts.LegendOpts(is_show=False),
            )
        )

        # Kline And Line
        overlap_kline_line = kline.overlap(line)

        # Grid Overlap + Bar
        grid_chart = Grid(
            init_opts=opts.InitOpts(
                #width="1000px",
                #height="800px",
                width="1850px",
                height="850px",
                animation_opts=opts.AnimationOpts(animation=False),
            )
        )
        grid_chart.add(
            overlap_kline_line,
            grid_opts=opts.GridOpts(pos_left="10%", pos_right="8%", height="50%"),
        )
        grid_chart.add(
            bar_0,
            grid_opts=opts.GridOpts(
                pos_left="10%", pos_right="8%", pos_top="63%", height="16%"
            ),
        )
        #grid_chart.add(
        #    bar,
        #    grid_opts=opts.GridOpts(
        #        pos_left="10%", pos_right="8%", pos_top="63%", height="16%"
        #    ),
        #)

        grid_chart.render("data.html")


if __name__ == "__main__":
    a = saveToHtml()
    data = a.get_data()
    a.draw_charts(chart_data=data)
