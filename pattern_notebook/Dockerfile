FROM quay.io/jupyter/minimal-notebook:hub-5.2.1

# Копируем файл зависимостей
COPY requirements.txt /tmp/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r /tmp/requirements.txt