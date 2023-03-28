// 基于准备好的dom，初始化echarts实例
const myChart1 = echarts.init(document.getElementById('main1'));
const myChart2 = echarts.init(document.getElementById('main2'));
const myChart5 = echarts.init(document.getElementById('main5'));

getNowFormatDate();
init_myChart1();
init_myChart2();
init_myChart5();

// 线图2
function init_myChart2() {
    const chartDom = document.getElementById('main2');
    const myChart = echarts.init(chartDom);
    let option;
    $.ajax({
        url: '/chart/bar/',
        type: 'GET',
        dataType: 'json',
        success: function (res) {
            // console.log(res);
            // let data = [];
            let data = [res.data1[0], res.data1[1], res.data1[2]]
            // console.log(data);
            let dataAxis = ['文献总量', '中文', '英文'];
            let yMax = 500;
            let dataShadow = [];
            for (let i = 0; i < data.length; i++) {
                dataShadow.push(yMax);
            }
            option = {
                xAxis: {
                    data: dataAxis,
                    axisLabel: {
                        inside: true,
                        color: '#fff'
                    },
                    axisTick: {
                        show: false
                    },
                    axisLine: {
                        show: true
                    },
                    z: 10
                },
                yAxis: {
                    axisLine: {
                        show: true
                    },
                    axisTick: {
                        show: false
                    },
                    axisLabel: {
                        color: '#ffffff'
                    },
                    splitLine: { //网格线
                        show: false
                    },
                },
                dataZoom: [
                    {
                        type: 'inside'
                    }
                ],
                series: [
                    {
                        type: 'bar',
                        showBackground: false,
                        itemStyle: {
                            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                                {offset: 0, color: '#83bff6'},
                                {offset: 0.5, color: '#188df0'},
                                {offset: 1, color: '#188df0'}
                            ])
                        },
                        emphasis: {
                            itemStyle: {
                                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                                    {offset: 0, color: '#2378f7'},
                                    {offset: 0.7, color: '#2378f7'},
                                    {offset: 1, color: '#83bff6'}
                                ])
                            }
                        },
                        data: data
                    }
                ]
            };
            const zoomSize = 6;
            myChart.on('click', function (params) {
                // console.log(dataAxis[Math.max(params.dataIndex - zoomSize / 2, 0)]);
                myChart.dispatchAction({
                    type: 'dataZoom',
                    startValue: dataAxis[Math.max(params.dataIndex - zoomSize / 2, 0)],
                    endValue:
                        dataAxis[Math.min(params.dataIndex + zoomSize / 2, data.length - 1)]
                });
            });
            myChart2.setOption(option);
        }
    })


}

// 饼图
function init_myChart1() {
    var chartDom = document.getElementById('main1');
    var myChart = echarts.init(chartDom);
    var option;

    option = {
        legend: [{
            x: 'left',      //可设定图例在左、右、居中
            y: 'center',     //可设定图例在上、下、居中
            itemGap: 10,//图例图标与文字间的间距
            textStyle: {
                //图例字体大小
                fontSize: 12,
                color: '#ffffff'//图例文字颜色
            },
            //图例大小
            itemHeight: 15,
            //图例滚动显示
            type: 'scroll',
            //图例纵向显示
            orient: 'vertical',
        }],
        toolbox: {
            show: true,
            feature: {
                mark: {show: true},
                dataView: {show: true, readOnly: false},
                restore: {show: true},
                saveAsImage: {show: true}
            }
        },
        series: [
            {
                name: '文献数量',
                type: 'pie',
                radius: [20, 80],
                center: ['60%', '50%'],
                roseType: 'area',
                itemStyle: {
                    borderRadius: 8,
                    fontSize: 12,//图例文字字体大小
                },
                data: []
            }
        ]
    };
    $.ajax({
        url: '/chart/pie/',
        type: 'GET',
        dataType: 'json',
        success: function (res) {
            // console.log(res.data, typeof (res.data));
            $.each(res.data, function (name, value) {
                // console.log(name, value)
                // console.log(option.series[0].data, typeof (option.series[0].data))
                option.series[0].data.push({value: value, name: name})
                myChart1.setOption(option);
            })
        }
    })
// 使用刚指定的配置项和数据显示图表。
}

// 柱状图
function init_myChart5() {
    const XData = ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"];

    $.ajax({
        url: '/chart/bar/',
        type: 'GET',
        dataType: 'json',
        success: function (res) {
            // console.log(res);
            // let data = [];
            let yData = [res.data2[0], res.data2[1], res.data2[2], res.data2[3], res.data2[4], res.data2[5], res.data2[6], res.data2[7], res.data2[8], res.data2[9], res.data2[10], res.data2[11]]
            // console.log(data);
            let option = {
                backgroundColor: "",
                xAxis: {
                    axisTick: {
                        show: false
                    },
                    splitLine: {
                        show: false
                    },
                    splitArea: {
                        show: false
                    },
                    data: XData,
                    axisLabel: {
                        formatter: function (value) {
                            var ret = ""; //拼接加\n返回的类目项
                            var maxLength = 1; //每项显示文字个数
                            var valLength = value.length; //X轴类目项的文字个数
                            var rowN = Math.ceil(valLength / maxLength); //类目项需要换行的行数
                            if (rowN > 1) //如果类目项的文字大于3,
                            {
                                for (var i = 0; i < rowN; i++) {
                                    var temp = ""; //每次截取的字符串
                                    var start = i * maxLength; //开始截取的位置
                                    var end = start + maxLength; //结束截取的位置
                                    //这里也可以加一个是否是最后一行的判断，但是不加也没有影响，那就不加吧
                                    temp = value.substring(start, end) + "\n";
                                    ret += temp; //凭借最终的字符串
                                }
                                return ret;
                            } else {
                                return value;
                            }
                        },
                        interval: 0,
                        fontSize: 14,
                        fontWeight: 100,
                        textStyle: {
                            color: '#9faeb5',

                        }
                    },
                    axisLine: {
                        lineStyle: {
                            color: '#4d4d4d'
                        }
                    }
                },
                yAxis: {
                    axisTick: {
                        show: false
                    },
                    splitLine: {
                        show: false
                    },
                    splitArea: {
                        show: false
                    },

                    axisLabel: {
                        textStyle: {
                            color: '#9faeb5',
                            fontSize: 16,
                        }
                    },
                    axisLine: {
                        lineStyle: {
                            color: '#4d4d4d'
                        }
                    }
                },
                tooltip: {
                    "trigger": "axis",
                    transitionDuration: 0,
                    backgroundColor: 'rgba(83,93,105,0.8)',
                    borderColor: '#535b69',
                    borderRadius: 8,
                    borderWidth: 2,
                    padding: [5, 10],
                    formatter: function (params, ticket, callback) {
                        var res = '';
                        for (var i = 0, l = params.length; i < l; i++) {
                            res += '' + params[i].seriesName + ' : ' + params[i].value + '<br>';
                        }
                        return res;
                    },
                    axisPointer: {
                        type: 'line',
                        lineStyle: {
                            type: 'dashed',
                            color: '#ffff00'
                        }
                    }
                },
                series: [{
                    name: '月份上传量',
                    type: "bar",
                    itemStyle: {
                        normal: {
                            color: {
                                type: 'linear',
                                x: 0,
                                y: 0,
                                x2: 0,
                                y2: 1,
                                colorStops: [{
                                    offset: 0,
                                    color: '#00d386' // 0% 处的颜色
                                }, {
                                    offset: 1,
                                    color: '#0076fc' // 100% 处的颜色
                                }],
                                globalCoord: false // 缺省为 false
                            },
                            barBorderRadius: 15,
                        }
                    },
                    label: {
                        normal: {
                            show: true,
                            position: "top",
                            textStyle: {
                                color: "#ffc72b",
                                fontSize: 10
                            }
                        }
                    },
                    data: yData,
                    barWidth: 16,
                }, {
                    name: '折线',
                    type: 'line',
                    itemStyle: {  /*设置折线颜色*/
                        normal: {
                            // color: '#c4cddc'
                        }
                    },
                    data: yData
                }]
            };
            myChart5.setOption(option);
        }
    })

}

//获取当前时间
function getNowFormatDate() {
    const date = new Date();
    const year = date.getFullYear();
    let month = date.getMonth() + 1;
    let strDate = date.getDate();
    let Hour = date.getHours();       // 获取当前小时数(0-23)
    let Minute = date.getMinutes();     // 获取当前分钟数(0-59)
    let Second = date.getSeconds();     // 获取当前秒数(0-59)
    const show_day = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'];
    const day = date.getDay();
    if (Hour < 10) {
        Hour = "0" + Hour;
    }
    if (Minute < 10) {
        Minute = "0" + Minute;
    }
    if (Second < 10) {
        Second = "0" + Second;
    }
    if (month >= 1 && month <= 9) {
        month = "0" + month;
    }
    if (strDate >= 0 && strDate <= 9) {
        strDate = "0" + strDate;
    }
    const currentdate = '<div><p>' + year + '年' + month + '月' + strDate + '号</p><p>' + show_day[day] + '</p></div>';
    const HMS = Hour + ':' + Minute + ':' + Second;
    const temp_time = year + '-' + month + '-' + strDate + ' ' + HMS;
    $('.nowTime li:nth-child(1)').html(HMS);
    $('.nowTime li:nth-child(2)').html(currentdate);
    //$('.topRec_List li div:nth-child(3)').html(temp_time);
    setTimeout(getNowFormatDate, 1000);//每隔1秒重新调用一次该函数
}

// setInterval(function () {
//     window.onresize = function () {
//         this.myChart1.resize;
//         this.myChart2.resize;
//         this.myChart3.resize;
//         this.myChart5.resize;
//     }
// }, 200)

