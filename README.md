Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:MidasMr/yacut.git
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Команда запуска
```
flask run
```

Настройка режима
работы:
Linux и MacOS
```
export FLASK_ENV=development
```

Windows
```
set FLASK_ENV=development
```

Создать репозиторий с миграциями
```
flask db init 
```

Создать миграции
```
flask db migrate
```

Применить изменения к базе данных
```
flask db upgrade
```


Стек технологий:
```
Python 3.9
flask= 2.0.2
sqlalchemy 1.4
```


Автор:
[Александр Вязников(MidasMr)](https://github.com/MidasMr)