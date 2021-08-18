
# TeamCityApi
Простейшая обертка над TeamCity Rest API, которая содержит набор функций для скачивания .apk артефакта из проектов

Пример использования

    import teamcity
    api = teamcity.TeamCityApi(domain='your tc domain, project='your base tc project', token='your token for tc')
	
	# получить список всех подпроектов
	api.get_projects()
	
	# получить список типов билдов для проекта
	# projectId - айди проекта для которого нужно получить
	api.get_buildTypes(projectId)
	
	# получить все успешные сборки нужного типа
	# idBuildType - айди типа сборки
	api.get_all_builds(idBuildType)
	
	# получить информацию о сборке
	# buildId - номер сборки
	api.get_build(buildId)
	
	# получить .apk файл
	# buildId - айди сборки
	api.get_artifacts(buildId)
	
	# скачать файл по ссылке
	api.download_file(url)
	

