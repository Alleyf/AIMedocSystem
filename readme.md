# AIMedocSystem

This is a project related to query databases docs using elasticsearch and ocr.

# 效果展示

![效果图1](https://amedoc.fcsy.fit/static/images/illusion/PCquery.webp)
![效果图2](https://amedoc.fcsy.fit/static/images/illusion/3end.webp)
![效果图3](https://amedoc.fcsy.fit/static/images/illusion/tablet1.webp)
![效果图4](https://amedoc.fcsy.fit/static/images/illusion/mobile1.webp)
![效果图5](https://amedoc.fcsy.fit/static/images/illusion/AIassistant.webp)
![效果图6](https://amedoc.fcsy.fit/static/images/illusion/imagepreview.webp)

# 文件说明

1. AIMeDocSys：项目配置文件夹
2. media：媒体文件夹
3. medocsys：项目主要内容文件夹
4. ppgan：AI模型文件夹
5. static：压缩后的静态文件文件夹
6. docker-compose.yml：docker-compose配置文件
7. Dockerfile：docker配置文件
8. manage.py：项目管理文件
9. pip.conf：pip配置文件
10. requirements.txt：项目依赖文件

# 部署教程

1. 打包项目文件上传至服务器
2. 拉库es、redis和neo4j进行docker部署
3. 为es配置ik分词器
4. 设置es、redis和neo4j的host和port
5. 修改query函数中的es的host和port

> [演示网址](https://amedoc.fcsy.fit)


> Total : 2695 files, 721262 codes, 23566 comments, 74911 blanks, all 819739 lines
