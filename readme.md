
# **JupyterHub-PostgreSQL in Docker**

## **Описание проекта**

Этот проект предоставляет готовое решение для развертывания **JupyterHub** с использованием **Docker Compose**. Основные особенности:
- **Автоматическое создание контейнеров**: Каждый пользователь получает свой собственный контейнер.
- **Интеграция с PostgreSQL**: Хранение данных в базе данных.
- **Поддержка регистрации**: Пользователи могут регистрироваться самостоятельно, но их учетные записи требуют одобрения администратора.
- **Масштабируемость**: Легко добавлять новые сервисы или изменять конфигурацию.
- **Мониторинг** (опционально) : Интеграция с Prometheus, Grafana, Postgres Exporter, Cadvisor, Node Exporter, Jupyter metrics и Notebook Exporter для сбора метрик использования ресурсов.

---

## **Требования**

Для работы с этим проектом вам понадобится:
- **Docker** ([установка](https://docs.docker.com/get-docker/))
- **Docker Compose** ([установка](https://docs.docker.com/compose/install/))
---

## **Установка и запуск**

### **Шаг 1: Клонирование репозитория**
```bash
git clone https://github.com/AnastasiaSarpova/jupyterhub-postgres_in_docker.git
cd jupyterhub-postgres_in_docker
```

### **Шаг 2: Настройка переменных окружения**
Создайте новый файл с именем .env, скопировав содержимое из .env.example. Это можно сделать через терминал: ```cp .env.example .env```
или вручную, создав пустой файл .env и вставив туда содержимое .env.example.
Откройте созданный файл .env в вашем любимом редакторе и замените все значения-заглушки на ваши данные при необходимости. Файл `.env` содержит следующие переменные:

| Переменная          | Описание                                  | Пример значения       |
|---------------------|-------------------------------------------|-----------------------|
| `POSTGRES_USER`     | Имя пользователя PostgreSQL               | `postgres`            |
| `POSTGRES_PASSWORD` | Пароль пользователя PostgreSQL            | `1234qwe`             |
| `POSTGRES_DB`       | Имя базы данных                           | `jupyter_db`          |
| `DB_HOST`           | Хост базы данных                          | `db`                  |
| `DB_PORT`           | Порт базы данных                          | `5432`                |


### **Шаг 3: Запуск сервисов**
Запустите JupyterHub и PostgreSQL с помощью Docker Compose:
```bash
docker-compose up -d
```
### **Шаг 4: Мониторинг (опционально)**

Шаг 1: Настройка мониторинга
Перейдите в папку monitoring:  
```bash
cd monitoring
```  
Настройте переменные окружения для мониторинга. Убедитесь, что файл .env в корневой директории содержит правильные значения для подключения к PostgreSQL.

Проверьте конфигурацию Prometheus (prometheus.yml) и Postgres Exporter (queries.yaml). При необходимости измените их для сбора дополнительных метрик.

#### Как настроить доступ к метрикам JupyterHub?**

Чтобы Prometheus мог собирать метрики, нужно:
1. Настроить аутентификацию для Prometheus.
2. Убедиться, что эндпоинт `/metrics` доступен на правильном порту.

 **Создайте токен администратора:**
   Запустите команду внутри контейнера JupyterHub:
   ```bash
   docker exec -it jupyter-skilltech-jupyterhub-1 jupyterhub token admin
   ```
   Эта команда создаст токен для пользователя `admin`. Сохраните его.

 **Настройте Prometheus для использования токена:**
   В конфигурации Prometheus обновите строку credentials:

   ```yaml
   scrape_configs:
     - job_name: "jupyter"
       static_configs:
         - targets: ["jupyter-skilltech-jupyterhub-1:8000"]
       metrics_path: "/metrics"
       scheme: "http"
       authorization:
         type: Bearer
         credentials: "<your-admin-token>"
   ```
   Здесь:
   - `type: Bearer` указывает, что используется токен.
   - `credentials` — ваш токен администратора.

### **Шаг 2: Запуск мониторинга**
Запустите мониторинг с помощью Docker Compose:

```bash
docker-compose docker-compose.yml up -d
```
**Доступ к интерфейсам мониторинга**  
- Prometheus: http://localhost:17909.
- Grafana: http://localhost:17300 .
- Postgres Exporter: http://localhost:9187/metrics 
- Cadvisor: http://localhost:17808
- Node Exporter: http://localhost:17910/metrics
- JupyterHub: http://localhost:17000/hub/metrics


## **Использование**

### **Регистрация пользователей** 
1. Откройте JupyterHub в браузере по адресу: http://localhost:17000.
2. При первом запуске зайдите под admin и задайте пароль
2. Нажмите "Sign Up" и зарегистрируйтесь.
3. Администратор должен одобрить учетную запись через интерфейс администратора.


## **Структура проекта**

Проект имеет следующую структуру:
```
jupyterhub-postgres_in_docker/
├─ pattern_notebook/
│   ├── Dockerfile         # Файл для сборки контейнера jupyter-notebook.
│   └── requirements.txt   # Список предустановленных библиотек Python в пользователький jupyter-notebook.
├─ monitoring/
│   ├── docker-compose.yml # Конфигурация для мониторинга.
│   ├── prometheus.yml     # Конфигурация Prometheus.
│   ├── queries.yaml       # Пользовательские запросы для Postgres Exporter.
│   └── notebook-exporter/
│       ├── Dockerfile     # Файл для сборки контейнера Notebook Exporter.
│       ├── metrics_server.py # Скрипт для сбора метрик.
│       └── notebook-exporter.sh # Скрипт для запуска экспортера.
├─ .env.example            # Пример файла с переменными окружения для конфигурации.
├─ docker-compose.yml      # Основной файл для запуска JupyterHub и PostgreSQL.
├─ jupyterhub_config.py    # Конфигурационный файл JupyterHub.
├─ Dockerfile              # Файл для сборки контейнера JupyterHub.
└─ README.md               # Документация проекта.
```
---
Авториация пользователей:
![Снимок экрана от 2025-02-05 17-02-35](https://github.com/user-attachments/assets/74a043bb-b9bc-4b7f-ac35-33d2b150f5be)
Подключение к PostgreSQL:
![Снимок экрана от 2025-02-05 17-03-12](https://github.com/user-attachments/assets/816f465e-89a9-4e3c-b1d5-93f8cd40a105)
Prometheus:
![alt text](/monitoring/screenshot/prometheus.png)
Мониторинг JupyterHub:
![alt text](/monitoring/screenshot/monitoring%20jupyterhub.png
)
Мониторинг Potgres:
![alt text](/monitoring/screenshot/moitoring%20postgres.png
)
