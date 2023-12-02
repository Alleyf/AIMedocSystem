# AIMedocSystem

<div align="center">
  <img src="https://img.shields.io/badge/branch-master-brightgreen.svg">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg">
  <img src="https://jaywcjlove.github.io/sb/lang/chinese.svg">
</div>
This is a project related to query databases docs using elasticsearch and ocr.

![team](https://github.com/Alleyf/AIMedocSystem/blob/master/medocsys/static/images/landing/brand.png?raw=true)

# 效果展示

<img src="https://raw.githubusercontent.com/Alleyf/AIMedocSystem/master/medocsys/static/images/illusion/3end.webp?token=GHSAT0AAAAAACKWYECXGP3CN4UJOR2YOAFSZLK7T5A" alt="效果图2" style="zoom:50%;" />
![效果图3](https://raw.githubusercontent.com/Alleyf/AIMedocSystem/master/medocsys/static/images/illusion/AIassistant.webp?token=GHSAT0AAAAAACKWYECXALTATNOQBFWK73OQZLK7UZA)
![效果图4](https://raw.githubusercontent.com/Alleyf/AIMedocSystem/master/medocsys/static/images/illusion/PCquery.webp?token=GHSAT0AAAAAACKWYECXWLIAQHYSCGMOMBVIZLK7VIA)
![效果图5](https://raw.githubusercontent.com/Alleyf/AIMedocSystem/master/medocsys/static/images/illusion/imagepreview.webp?token=GHSAT0AAAAAACKWYECWW3VQPGZZ2FEOCCQWZLK7WEQ)
![效果图6](https://raw.githubusercontent.com/Alleyf/AIMedocSystem/master/medocsys/static/images/illusion/mobile1.webp?token=GHSAT0AAAAAACKWYECXGD5OKMQVKOQIVRREZLK7W6A)

![](https://raw.githubusercontent.com/Alleyf/AIMedocSystem/master/medocsys/static/images/illusion/tablet1.webp?token=GHSAT0AAAAAACKWYECXTKKGMW6BDICCDB54ZLK7XJA)



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
# 未来计划

1. 将知识图谱与GPT结合，让GPT随知识图谱联动
2. 采用Go语言重构项目
3. 采用Vue+Go前后端分离设计
4. 实现神经网络检索，支持图片检索
5. 采用OSS云存储，减小服务器存储压力
