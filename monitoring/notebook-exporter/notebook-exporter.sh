#!/bin/bash

# Путь к файлу с метриками
METRICS_FILE_JUPYTER="/tmp/notebook_metrics_jupyter.prom"

# Функция для сбора метрик
collect_metrics() {
    # Очищаем файл перед началом работы
    > "$METRICS_FILE_JUPYTER"

    # Поиск контейнеров с подходящим образом"
    for var in $(docker ps | grep "pattern_notebook:v1" | awk '{print $15}')
    do
        echo "Обработка контейнера: $var"

        # Получаем список файлов .ipynb и .py в директории ~/work
        docker exec $var bash -c "
            cd /home/jovyan/work &&
            ls -l | grep -E '\.(ipynb|py)$'
        " | while read -r line; do
            # Парсим данные из вывода ls -l
            file_size=$(echo "$line" | awk '{print $5}')  # Размер файла
            file_name=$(echo "$line" | awk '{print $9}')  # Имя файла

            # Проверяем существование файла
            if docker exec $var test -f "/home/jovyan/work/$file_name"; then
                # Подсчитываем количество строк в файле
                line_count=$(docker exec $var wc -l "/home/jovyan/work/$file_name" | awk '{print $1}')

                # Формируем метрики в формате Prometheus
                echo "# HELP notebook_file_size_bytes Size of the notebook file in bytes" >> "$METRICS_FILE_JUPYTER"
                echo "# TYPE notebook_file_size_bytes gauge" >> "$METRICS_FILE_JUPYTER"
                echo "notebook_file_size_bytes{container=\"$var\", file=\"$file_name\"} $file_size" >> "$METRICS_FILE_JUPYTER"

                echo "# HELP notebook_file_char_count Number of characters in the notebook file" >> "$METRICS_FILE_JUPYTER"
                echo "# TYPE notebook_file_line_count gauge" >> "$METRICS_FILE_JUPYTER"
                echo "notebook_file_line_count{container=\"$var\", file=\"$file_name\"} $line_count" >> "$METRICS_FILE_JUPYTER"
            else
                echo "Файл /home/jovyan/work/$file_name не найден в контейнере $var"
            fi
        done
    done

    echo "Метрики сохранены в $METRICS_FILE_JUPYTER"
}

# Функция для предоставления метрик через HTTP-сервер
serve_metrics() {
    python3 /usr/local/bin/metrics_server.py
}
# Запускаем сбор метрик каждые 5 минут
while true; do
    collect_metrics
    sleep 300  # Интервал между сборами метрик (5 минут)
done &

# Запускаем HTTP-сервер для предоставления метрик
serve_metrics