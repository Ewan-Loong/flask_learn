# flask_learn
A universal backend framework built on libraries such as Python 3. x, Flask 3. x, and Celery 5. x;  

基于`python3.x + flask3.x + celery5.x`等库构建的通用后端框架； 

---

## 用法
clone 代码到python编译器、IDEA或其他可以运行python脚本的环境中，然后run  
项目涉及的包请根据import自行pip install


## 文件夹含义
* core 底层核心工具类
* instance 配置文件(已废弃 现通过settings管理)
* models 数据库实体模型,使用SqlAlchemy框架管理
* models_extend 实体模型方法拓展(暂未实现)
* service 由flask管理的具体后端服务目录,按文件夹分隔不同系统后端
* settings 框架配置项
* static 前端模板静态目录(现已做成前后端分离 vue_learn)
* templates 前面模板文件(现已做成前后端分离 vue_learn)
## 主要项目负责人
[@Ewan](https://github.com/Ewan-Loong)
