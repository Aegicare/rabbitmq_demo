RabbitMQ官方教程加一些个人学习的备注

安装环境:
```bash
$ pip install -r requirements.txt
```

启动worker:
```bash
$ celery -A celery_try worker -l info
```

初始化Django并运行：

```bash
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```
