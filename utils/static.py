from config import settings


class StaticURL:
    static_urls = {}
    static_paths = [
        'icons/icon_object_off.png',
        'icons/icon_data_source.png',
        'icons/icon_people_person.png',
        'icons/icon_relationship_hover.png',
        'icons/icon_technologies_off.png',
    ]

    def __init__(self, host=None, static_path=None):
        self.host = host or settings.BASE_URL
        self.static_path = static_path or 'static'
        self.build()

    def get_static(self, filepath=''):
        return f'{self.host}/{self.static_path}/{filepath}'

    def build(self):
        self.static_urls = {path: self.get_static(filepath=path) for path in self.static_paths}

    def url_for(self, path):
        return self.static_urls.get(path)


static = StaticURL()
