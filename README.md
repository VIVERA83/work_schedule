# Сервис по работе с графиком работы водительского состава и автопарка

## Оглавление

- [Описание проекта](#описание-проекта)
- [Цели проекта](#цели-проекта)
- [Функциональность](#функциональность)
  - [Реализованные модули API](#реализованные-модули-api)
  - [Планы](#планы)
- [Используемый стек](#используемый-стек)
- [Демонстрация MVP](#демонстрация-MVP)
- [Установка и запуск](#установка-и-запуск)


## Описание проекта

Сервис предназначен для автоматизации и оптимизации процессов управления графиками работы водителей и автопарка. Он позволяет сократить время на подготовку нарядов, визуализировать текущее состояние автопарка и водительского состава, а также прогнозировать будущие потребности в ресурсах.

## Цели проекта

1. **Сокращение времени на подготовку нарядов**: Упрощение и ускорение процесса формирования нарядов по машинам на будущий день.
2. **Визуализация состояния автопарка и водителей**: Наглядное отображение текущего состояния автопарка и водительского состава.
3. **Прогнозирование**: Возможность прогнозирования будущих нарядов, ремонтов и выявления возможных нехваток водителей или машин.

## Функциональность

### Реализованные модули API

- **Водитель**: Поддержка операций CRUD (создание, чтение, обновление, удаление).
- **Машина**: Поддержка операций CRUD.
- **Тип графика**: 
  - Создание и управление типами графиков (например, 4/2 — четыре рабочих и два выходных дня).
  - Используется для формирования графиков работы водителей и машин.
- **История изменений графиков**:
  - Ведение истории смены графиков.
  - Учет истории при составлении графиков на длительный период.
- **Экипаж**:
  - Закрепление водителей и машин за определенным экипажем.
  - Формирование графика работы на основе графика водителей и приписанных машин.
  - Ограничения на уровне БД: в экипаже не может быть более 2 машин и 3 водителей.
- **График работы**:
  - Просмотр графика работы водителя за определенный период.
  - Формирование общего графика работы автоколонны за заданный период с экспортом в Excel.

### Планы

1. **Доработка API**:
   - Добавление новых статусов для водителей и машин:
     - Больничный
     - Отпуск
     - Ремонт
2. **Добавление статистики по наряду в Excel**:
   - Машины без наряда
   - Машины в ремонте
   - Незадействованные водители
   - Незадействованные машины
3. **Добавление интерактивности в Excel**:
   - Переход на отдельные страницы при нажатии на водителя или машину.
   - На странице будет отображаться подробная информация: график работы, экипаж, контактные данные.
4. **Разработка фронтенд-части**:
   - Создание интерфейса для работы начальника автоколонны.
   - Возможность в интерактивном режиме изменять и планировать текущий и будущий наряд.

## Используемый стек

1. **FastAPI** — для создания API.
2. **Postgres** — в качестве базы данных.
3. **SQLAlchemy** — для работы с базой данных.
4. **Alembic** — для управления миграциями базы данных.

## Демонстрация MVP

Вы можете ознакомиться с текущей версией проекта по ссылке:  
[MVP проекта](http://79.133.181.74:8008/docs)

Обратите внимание, что это ранняя версия, и функциональность может быть ограничена.

## Установка и запуск

Инструкции по установке и запуску проекта:
 
Создайте в корневом каталоге проекта файл `env` как в примере [example.env](example.env)
```bash
# Клонируйте репозиторий
git clone https://github.com/ваш-username/ваш-репозиторий.git

# Перейдите в директорию проекта
cd ваш-репозиторий

# Установите зависимости
pip install -r requirements.txt

# Установка миграций 
alembic upgrade head

# Запустите сервер
uvicorn main:app --reload  
```
Либо с помощью Docker:
```bash
docker compose up --build -d
```
