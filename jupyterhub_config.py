from dockerspawner import DockerSpawner
import os, nativeauthenticator


c.JupyterHub.log_level = "DEBUG" # подробные логи
c.JupyterHub.hub_ip = "0.0.0.0" # слушает все порты
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner' # каждому пользователю по контейнеру

c.DockerSpawner.network_name = "jupyterhub"
c.DockerSpawner.remove = True # контейнеры пользователей будут автоматически удаляться после завершения работы

c.DockerSpawner.volumes = {"jupyterhub-user-{username}": "/home/jovyan/work"}

c.JupyterHub.db_url = "sqlite:////srv/jupyterhub/data/jupyterhub.sqlite" # сохраняет бд, в т.ч. пользователей
c.DockerSpawner.notebook_dir = "/home/jovyan/work"
c.DockerSpawner.image = "pattern_notebook:v1" # образ для ноутбука
c.DockerSpawner.http_timeout = 300 # определяет максимальное время, которое хаб будет ждать ответа от пользовательского контейнера при попытке подключиться к нему

c.JupyterHub.authenticator_class = 'native' # позволяет регистрироваться пользователям
c.Authenticator.admin_users = {"admin"}
c.Authenticator.allowed_users = {"admin"} # список разрешенных пользователей 

c.Authenticator.allow_all = True #  разрешает вход зарегистрированным пользователям.
c.NativeAuthenticator.open_signup = False # требуется одобрение администратора
c.NativeAuthenticator.create_system_users = False # не создает системных пользователей на хосте.

#c.NativeAuthenticator.check_common_password = True # проверка пароля 
#c.NativeAuthenticator.minimum_password_length = 5

c.NativeAuthenticator.allowed_failed_logins = 3 # блокировка пользователей после нескольких неудачных попыток входа в систему
c.NativeAuthenticator.seconds_before_next_try = 1200

c.Authenticator.delete_invalid_users = True
c.Authenticator.registration_expiration_days = 7  # удалить неодобренных пользователей через 7 дней

c.NotebookApp.autosave = True # включение автосохранения
c.ContentsManager.autosave_interval = 30000  # 30 секунд

# Время ожидания перед отключением сервера (в секундах)
c.JupyterHub.shutdown_idle_servers = True
c.JupyterHub.idle_timeout = 1800  # 30 минут

# добавляет к админке возможность менять пароли и подтверждать регистрацию пользователей
c.JupyterHub.template_paths = [f"{os.path.dirname(nativeauthenticator.__file__)}/templates/"]

c.DockerSpawner.environment = {
    "TEST_VAR": "test_value",
    "DB_HOST": os.environ.get("DB_HOST"),
    "DB_PORT": os.environ.get("DB_PORT"),
    "POSTGRES_USER": os.environ.get("POSTGRES_USER"),
    "POSTGRES_PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
    "POSTGRES_DB": os.environ.get("POSTGRES_DB"),
}
