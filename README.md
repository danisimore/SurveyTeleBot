# SurveyTeleBot
Telegram bot for surveys. This Telegram bot is created using Telebot Python library.
Телеграм бот для проведения опросов. Создан с помощью библиотеки Telebot

## Применение. :bulb:
Первый вариант применения бота - реализация какого-либо сценария в зависимости от выборов пользователя. Для этого есть ветка `main`. В этой версии ответы пользователя никуда не записываются, соответсвенно она подходит для обработки ответов пользователя в интерактивном режиме.
Например вы можете изменять какие-то данные, в зависимости от его ответов.

Второй вариант применения - опрос. Версия, которая реализована в ветке `survey_with_saving_data` позволяет сохранять ответы пользователя. В данной реализации существует 2 сценария ответов пользователя. В зависимости от первого ответа будут формироваться данные об ответах.
Сценариев может быть неограниченное количество. Добавление сценариев реализуется путем дополнения кода.

## Схема работы. :construction:
![Scheme](https://i.imgur.com/jZkXazF.png)