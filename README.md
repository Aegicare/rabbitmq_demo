生信分析流程异步调用并限流的Demo
====

# 功能说明：

* 客户端生产者发布长时间任务（任务A）到X队列
* 服务端消费者从X队列获取msg处理任务，一次最多处理N个任务(worker设置concurrency)
* 消费者处理任务时，将任务进度和结果更新到N百分比，数据永久存储到redis
* 客户端从redis获取任务进度实时展示进度
* 当任务完成后，客户端将服务端生成的结果文件(路径)异步处理（另一个长时间任务B）
* 防止任务B多次提交，用celery-once实现

# 环境需求:
```bash
$ pip install -r requirements.txt
```

# 启动worker:
```bash
$ celery -A celery_try worker -l info
```

# 初始化Django并运行：
```bash
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```
