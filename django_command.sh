# 仮想環境でプロジェクトフォルダを作成する
python -m venv youtube-channel-app

# 仮想環境の中でDjangoをインストールする
pip install django

# Djangoのプロジェクトフォルダを作成する
django-admin startproject config .

# Djangoのアプリを作成する
django-admin startapp channels

# 画像を扱う場合に必要
pip install Pillow

# Google APIをインストールする
pip install google-api-python-client

# ウィジェット用ライブラリ
pip install django-widget-tweaks


# postgreSQLをインストールする
pip install psycopg2

# config/settings.pyを編集する
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "youtube_channel_db",
        "USER": "postgres",
        "PASSWORD": "password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

### マイグレーションコマンド ###
# モデルのマイグレーションファイルを作成する
python manage.py makemigrations

# マイグレーションを実行する
python manage.py migrate

# 下記エラーが発生(下記に個所をコメントアウトして実行する)
django.db.migrations.exceptions.InconsistentMigrationHistory: Migration admin.0001_initial is applied before its dependency users.0001_initial on database 'default'.

# setting.py
INSTALLED_APPS = [
    # "django.contrib.admin",

# urls.py
urlpatterns = [
    # path('admin/', admin.site.urls),
### migrateが完了したらコメントアウトを外して再度migrate実行 ###


# CORS ポリシー用
pip install django-cors-headers

# トークン用Migrations
python manage.py makemigrations authtoken