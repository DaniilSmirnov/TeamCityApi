"""
Оставь надежду всяк сюда входящий, сий файл является отборным сборником костылей и страшных неоптимальных решений
"""

import getpass
import os
from shutil import copy

import requests


class TeamCityApi:
    def __init__(self, domain, project, token):
        self.domain = domain
        self.project = project
        self.headers = {'Accept': 'application/json',
                        'Authorization': 'Bearer ' + token}

    def perform_request(self, subparams):
        return requests.get(self.domain + subparams, headers=self.headers).json()

    def get_projects(self):
        return self.perform_request('/app/rest/projects/' + self.project).get('projects').get('project')

    def get_buildTypes(self, project):
        return self.perform_request('/app/rest/projects/' + project).get('buildTypes').get('buildType')

    def get_all_builds(self, buildTypeId):
        return self.perform_request('/app/rest/buildTypes/id:' + buildTypeId + '/builds/?status=SUCCESS')

    def get_build(self, buildId):
        return self.perform_request('/app/rest/builds/id:' + buildId)

    # Прошло минуты 3 с момента написания функции ниже, но я уже не помню как она работает
    def get_artifacts(self, buildId):
        artifact = self.perform_request('/app/rest/builds/id:' + str(buildId) + '/artifacts/children/')
        files_artifact = artifact.get('file')
        if len(files_artifact) > 1:
            for i in range(0, len(files_artifact)):
                content_artifact = artifact.get('file')[i].get('content')
                if content_artifact.get('href').find('.apk') != -1:
                    break
        else:
            content_artifact = artifact.get('file')[0].get('content')
        if content_artifact is None:
            while content_artifact is None:
                artifact = self.perform_request(artifact.get('file')[0].get('children').get('href'))
                content_artifact = artifact.get('file')[0].get('content')

        file_index = 1
        content_artifact = content_artifact.get('href')
        while content_artifact.find('.apk') == -1:
            content_artifact = artifact.get('file')[file_index].get('content').get('href')
            file_index += 1

        return self.download_file(self.domain + content_artifact)

    def download_file(self, url):
        local_filename = url.split('/')[-1]
        with requests.get(url, stream=True, headers=self.headers) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        copy(local_filename, '/Users/' + getpass.getuser() + '/Downloads')
        os.remove(local_filename)
        return '~/Downloads/' + local_filename
