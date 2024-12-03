# 运行流程
## 数据库初始化或更新
- rm -rf migrations nano_enzyme.db
- flask db init && flask db migrate && flask db upgrade
## 网站运行
- flask run
## 浏览器打开http://127.0.0.1:5000/即可