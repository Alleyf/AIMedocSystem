# AIMedocSystem

<div align="center">
  <img src="https://img.shields.io/badge/branch-master-brightgreen.svg">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg">
  <img src="https://jaywcjlove.github.io/sb/lang/chinese.svg">
</div>
<div align="center">
<img alt="GitHub followers" src="https://img.shields.io/github/followers/Alleyf">
<img alt="GitHub watchers" src="https://img.shields.io/github/watchers/Alleyf/AIMedocSystem">
<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/Alleyf/AIMedocSystem">
<img alt="GitHub forks" src="https://img.shields.io/github/forks/Alleyf/AIMedocSystem">
</div>

# 项目介绍

当前医疗行业需要大量专业性强的医学文献资料，但传统检索方法效率低且消耗人力物力。为此，本团队打造了一款基于ElasticSearch和OCR技术的医学文献智能识别检索系统，建立本地文献库并支持在线检索、阅览、删除和下载文献。采用生成预训练模型进行文献分类，使用Laplacian矩阵卷积法和NAFNet图像去模糊复原模型分类处理模糊图像提高识别准确率和速度。光学字符识别技术能够准确提取图片中的文字内容，并精确到PDF中的页数和摘要命中段落。结合大数据可视化技术、智能问答助手、医学知识图谱、文献推送等特色功能。采用Docker容器化部署至云服务器上，实现了方便快速并且与平台解耦的自动化部署方式，为医护人员提供一站式文献系统管理和快速且精准的医学信息与文献检索服务。系统整体业务流程如下图所示：
![](http://qnpicmap.fcsluck.top/pics/202312021910732.png)

# 团队介绍

**智检慧医-开发团队** 旨在利用人工智能技术和图像文字识别技术，打造一款医学文献智能识别检索系统，对于推进医疗行业的数字化转型具有重要意义！
<div >
  <img src="http://qnpicmap.fcsluck.top/pics/202312021909563.png">
</div>

# 效果展示

  <video controls src="http://qnpicmap.fcsluck.top/files/%E4%BD%9C%E5%93%81%E4%BB%8B%E7%BB%8D%E8%A7%86%E9%A2%91.mp4" muted="true"></video>
  [观看视频演示](http://qnpicmap.fcsluck.top/files/%E4%BD%9C%E5%93%81%E4%BB%8B%E7%BB%8D%E8%A7%86%E9%A2%91.mp4)


---


![](http://qnpicmap.fcsluck.top/pics/202312021847392.webp)

<div align="center">
  <img src="http://qnpicmap.fcsluck.top/pics/202312021847390.webp" alt="效果图2" style="zoom:50%;" />
  <img src="http://qnpicmap.fcsluck.top/pics/202312021847391.webp">
</div>
<div align="center">
  <img src="http://qnpicmap.fcsluck.top/pics/202312021847386.webp">
  <img src="http://qnpicmap.fcsluck.top/pics/202312021847384.webp">
</div>
<div align="center">
  <img src="http://qnpicmap.fcsluck.top/pics/202312021847385.webp">
  <img src="http://qnpicmap.fcsluck.top/pics/202312021847388.png">
</div>

# 技术栈

- Django
- Git
- MySQL
- Neo4j
- Node.js
- Nginx
- Docker
- Elasticsearch
- Vue
- Bootstrap
- Jquery
- Echarts
- Swagger
- Redis
- Selenium

技术架构图如下图所示：
<br>
![](http://qnpicmap.fcsluck.top/pics/202312021910539.png)

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

1. 拉取项目至本地修改各中间件的参数配置
2. ```shell
    pip install -r requirements.txt
   ```
3. 安装es、redis和neo4j等中间件进行配置
4. 为es配置ik分词器
5. 启动Django项目（**自带docker文件可进行docker自动化部署**）

> [演示网址（受服务资源限制已停止服务）](https://amedoc.fcsy.fit)

# 未来计划

- [ ] 将知识图谱与GPT结合，让GPT随知识图谱联动
- [ ] 采用Go语言重构项目
- [ ] 采用Vue+Go前后端分离设计
- [ ] 实现神经网络检索，支持图片检索
- [ ] 采用OSS云存储，减小服务器存储压力

# 致谢

1. 在此特别感谢刘焕勇老师整理的医学知识图谱相关数据，本项目知识图谱检索部分采用该数据进行检索
2. 感谢团队成员：[chuiyugin](https://github.com/chuiyugin) 等的团结协作才有此结果
3. 本项目一切文档资源（pdf）来自于开源文档，如有侵权请及时告知处理
4. 该项目用于仅供学习，切勿滥用于其他用途
