# Базовый образ
FROM alpine:latest

# Установка необходимых пакетов
RUN apk add --no-cache bash netcat-openbsd docker-cli python3

# Копирование скрипта combined_exporter.sh в контейнер
COPY notebook-exporter.sh /notebook-exporter.sh

# Копирование Python-скрипта для HTTP-сервера
COPY metrics_server.py /usr/local/bin/metrics_server.py

# Делаем скрипт исполняемым
RUN chmod +x /notebook-exporter.sh

# Порт, на котором будет работать Exporter
EXPOSE 17666

# Команда для запуска Exporter
CMD ["/notebook-exporter.sh"]