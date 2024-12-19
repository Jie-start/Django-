# Django博客系统
基于Django开发的博客系统

## 激活conda环境
```bash
conda create --name Django python=3.8 django django-taggit
```

```bash
conda activate Django
```

## 启动开发服务器

```bash
python manage.py runserver
```

## 重置数据

删除数据库

```bash
del db.sqlite3
```

删除所有迁移文件（除了 init.py)

```bash
del blog\migrations\0*.py
```

重新创建迁移文件

```bash
python manage.py makemigrations
```

应用迁移

```bash
python manage.py migrate
```

重启开发服务器

```bash
python manage.py runserver
```
