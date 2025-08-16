@echo off
SETLOCAL

:: Проверяем наличие venv
if not exist "venv\Scripts\python.exe" (
    echo Создаем виртуальное окружение...
    python -m venv venv || (
        echo Ошибка при создании venv. Убедитесь что Python установлен.
        pause
        exit /b 1
    )
)

:: Активируем venv
call venv\Scripts\activate.bat || (
    echo Ошибка активации виртуального окружения
    pause
    exit /b 1
)

:: Устанавливаем зависимости если есть requirements.txt
if exist "requirements.txt" (
    echo Устанавливаем зависимости...
    pip install -r requirements.txt || (
        echo Ошибка установки зависимостей
        pause
        exit /b 1
    )
)

:: Запускаем игру
echo Запускаем игру...
python the_snake.py || (
    echo Ошибка запуска игры
    pause
    exit /b 1
)

pause