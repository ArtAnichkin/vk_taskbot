# vk_taskbot
Вк бот для домашек в формате картинка - ответ

В обучении очень важно соблюдать баланс между хорошими задачами и задачами на запоминание. Данный бот хорошо справляется задачками на запоминание, где ответом служит число или слово. Данный бот призван облегчить жизнь преподавателю и автоматизировать проверку таких заданий.

## Функционал бота
Бот-МШ берет из заранее заготовленных заданий картинку и отправляет ее ученику ожидая на нее ответ. Если ответ верный - высылается следующее задание, если нет - бот сообщает об этом и дает еще попытку. Цикл завершается если все задачки решены, о чем бот сообщает ученику.

## Настройка
1. Скрипт отправляет сообщение через ВК бота по API, потребуется его создать, разрешить отправку им сообщений, создать токен и внести его в строку vk = vk_api.VkApi(token = 'mytoken') не убирая ковычек.
2. Загрузка заданий происходит из папки tasks. Поместите туда пронумерованные задания в формате bmp, jpg или jpeg, например 1.bmp
3. Чтобы задать ответы на вопросы необходимо запустить скрипт, после чего будет предложенно загрузить ответы. Вносите их по одному, разделяя клавишей enter.
4. После загрузки ответов будет предложено запустить бота, после чего можно будет с ним работать. Напишите ему что-нибудь в личные сообщения ВК и и он пришлет первое задание.
