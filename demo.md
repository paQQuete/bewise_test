### Запрос на обработку новых вопросов
Первая итерация (в ответе пустой объект - т.к. это первый запрос на эндпоинт).
<img src="https://github.com/paQQuete/bewise_test/raw/master/media/questions_first.png" width="90%" alt="Первая итерация">
Вторая итерация (в ответе получаем вопросы, сохраненные с последнего успешного запроса)
<img src="https://github.com/paQQuete/bewise_test/raw/master/media/questions_second.png" width="90%" alt="Вторая итерация">

### Регистрация пользователя
<img src="https://github.com/paQQuete/bewise_test/raw/master/media/user%20register.png" width="90%" alt="Регистрация пользователя">

### Загрузка и конвертация файла
В ответе получаем ссылку на скачивание файла.
<img src="https://github.com/paQQuete/bewise_test/raw/master/media/upload_convert%20file.png" width="90%" alt="Загрузка файла">

### Следуем по полученной ссылке
<img src="https://github.com/paQQuete/bewise_test/raw/master/media/follow%20link.png" width="90%" alt="Следуем по ссылке">

<img src="https://github.com/paQQuete/bewise_test/raw/master/media/redirect%20to%20download%20link.png" width="90%" alt="Браузер получил http 303, перешел по ссылке, получил файл">

<img src="https://github.com/paQQuete/bewise_test/raw/master/media/play%20mp3%20audio.png" width="90%" alt="И начал воспроизводить полученный файл">

<img src="https://github.com/paQQuete/bewise_test/raw/master/media/download%20file.png" width="90%" alt="Но так как в задании указано что файл надо скачать - добавим заголовок для этого пути через nginx и браузер скачает файл">
