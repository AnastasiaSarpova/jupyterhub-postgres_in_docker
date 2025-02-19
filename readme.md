
# **JupyterHub-PostgreSQL in Docker**

**Оглавление**:  
1. [Описание проекта](#описание-проекта)  
2. [Требования](#требования)  
3. [Установка и запуск](#установка-и-запуск)  
    [Шаг 1: Клонирование репозитория](#шаг-1-клонирование-репозитория)  
    [Шаг 2: Настройка переменных окружения](#шаг-2-запуск-мониторинга)  
    [Шаг 3: Запуск сервисов](#шаг-3-запуск-сервисов)  
4. [Мониторинг](#шаг-4-мониторинг-опционально)  
    [Настройка мониторинга](#настройка-мониторинга)  
    [Доступ к интерфейсам мониторинга](#доступ-к-интерфейсам-мониторинга)  
5. [Использование](#использование)  
    [Регистрация пользователей](#регистрация-пользователей)  
    [Настройка алертов](#установка-алертов)  
    [Дашборды в Grafana](#дашборды-в-grafana)  
6. [Структура проекта](#структура-проекта)  

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
### **Мониторинг (опционально)**

Пошаговое описание процесса:
1. Сбор логов (Fluent Bit → Loki):  
Fluent Bit собирает логи из различных источников (например, контейнеров, системных журналов и т.д.). На данный момент организован сбор логов о подключения по SSH и syslog. Для добавления нового источника логов редактировать файл - docker-compose.yml
Логи передаются в Loki , который хранит их в виде меток (labels) для эффективного поиска и анализа.
2. Сбор метрик (Prometheus → Grafana):  
Prometheus собирает метрики с различных экспортеров (Node Exporter, cAdvisor, Postgres Expotrer, Notebook_Exporter).
Метрики передаются в Grafana через datasource для создания дашбордов и графиков.
3. Визуализация логов (Loki → Grafana):  
Grafana подключается к Loki через datasource.
В Grafana можно создавать дашборды для анализа и мониторинга логов, собранных Loki.
4. Настройка алертов (Grafana → Alertmanager):  
В Grafana настраиваются правила алертинга (alerting rules) на основе данных из Prometheus или Loki.
Когда условие алерта выполняется, Grafana отправляет уведомление в Alertmanager .
5. Обработка алертов (Alertmanager):  
Alertmanager обрабатывает алерты, группирует их и отправляет уведомления на различные каналы (например, email, Telegram).                                                      

#### Настройка мониторинга
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
  - job_name: "jupyter"
    static_configs:
      - targets: ["jupyter-skilltech-jupyterhub-1:8000"]
    scheme: "http"
    authorization:
      type: Bearer
      credentials: "JUPYTER_ADMIN_TOKEN"
   ```
   Здесь:
   - `type: Bearer` указывает, что используется токен.
   - `credentials` — ваш токен администратора.
#### Как настроить почту для алертинга**
1. в файле alertmanager.yml настройте поля:
```
| Переменная          | Описание                             |
|---------------------|--------------------------------------|
| EMAIL_FROM        | Отправитель                          |
| EMAIL_USERNAME    | Имя пользователя для аутентификации  |
| EMAIL_PASSWORD    | Пароль                               |
| EMAIL_TO          | Хост базы данных                     |
```
По умолчанию, почта установлена на хосте gmail.com, 
при использовании другого хоста изменить поле - `smtp.gmail.com:587`

### **Запуск мониторинга**
Запустите мониторинг с помощью Docker Compose:

```bash
docker-compose docker-compose.yml up -d
```
#### **Доступ к интерфейсам мониторинга**  
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

### **Установка алертов** 
1. Для настройки алера через Grafana, необходимо подключить alertmanager в качестве контакта.
![setting_ssh_alert](/monitoring/screenshot/setting_contact_for_alert.png)

2. Настройка алерта входа пользователя по SSH:
![setting_ssh_alert](/monitoring/screenshot/setting_ssh_alert.png)
![email_aler_ssh](/monitoring/screenshot/email_aler_ssh.png)

3. Настройка алерта о потереблении Docker контейнером более > 80% оперативной памяти, установленной лимитом:
![setting_memory_alert](/monitoring/screenshot/setting_memory_alert.png)
![email_alert_cont_memory](/monitoring/screenshot/email_alert_cont_memory.png)

Страница алертов в Grafana:
![grafana_alert](/monitoring/screenshot/grafana_alert.png)

### Дашборды в Grafana
Составленно 5 дашбородов:
1. Мониторинг JupyerHub - Количество пользователей, размер пользовательских ноутбуков, динамика изменения потребляемой памяти пользователями
![Dashbord_jupyterhub](/monitoring/screenshot/Dashbord_jupyterhub.png)
2. Мониторинг БД Postgres - Работа сервера, размер бд, размер таблиц и их владельце, динамика изменения количества строк в таблицах.
![Dashbord_postgres](/monitoring/screenshot/Dashbord_postgres.png)
3. Мониторинг входа пользователей по SSH - на основе 17514 дашборда Grafana. Позволяет отслешивать количество активных соединений по SSH.
![Dashbord_shh](/monitoring/screenshot/Dashbord_shh.png)
4. Мониторинг системных ресурсов и контейнеров Docker - на основе 16310 дашборда Grafana.
![Dashbord_docker](/monitoring/screenshot/Dashbord_docker.png)
5. Логи Syslog - Удобный вывод системных логов, с быстрым поиском по слову и отслеживанием динамики количества логов.
![Dashbord_syslog](/monitoring/screenshot/Dashbord%20syslog.png)

## **Структура проекта**

Проект имеет следующую структуру:
```
jupyterhub-postgres_in_docker/
├─ pattern_notebook/
│   ├── Dockerfile         # Файл для сборки контейнера jupyter-notebook.
│   └── requirements.txt   # Список предустановленных библиотек Python в пользовательский jupyter-notebook.
├─ monitoring/
│   ├── docker-compose.yml # Конфигурация для мониторинга.
│   ├── prometheus.yml     # Конфигурация Prometheus.
│   ├── queries.yaml       # Пользовательские запросы для Postgres Exporter.
│   ├── alertmanager.yml   # Конфигурация Alertmanager.
│   ├── fluent-bit.conf    # Конфигурация Fluent Bit для сбора логов.
│   ├── loki-config.yaml   # Конфигурация Loki для хранения логов.
│   ├── dasbords_json/     # JSON файлы дашбордов для Grafana.
│   ├── notebook-exporter/
│   │   ├── Dockerfile     # Файл для сборки контейнера Notebook Exporter.
│   │   └── notebook_exporter.py # Скрипт для сбора метрик.
│   └── screenshot/        # Скриншоты настроек и дашбордов.
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