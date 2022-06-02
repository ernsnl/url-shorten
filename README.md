# url-shorten

This is a basic url shortener web service and it has been implemented within 2 hours. To correctly install the necessary interaction, please run the following command. This project assumes that you already installed python 3 in your local machine. If not, please follow the instructions for installing python3 by visiting [here](https://www.python.org/downloads/)

```
pip install -r project/requirements.txt
```

After the necessary requirements are installed, please run the following command to initialize Django

```
python manage.py migrate && python manage.py runserver
```

After everything is migrated, you should be able to interact with the web service in http://127.0.0.1:8000/
