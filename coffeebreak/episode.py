import re

class Episode:
    def __init__(self , episode):
        self._episode = episode

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'{self.id}: {self.guests}'

    @property
    def id(self):
        if (self.title.lower().find('ep') < 0):
            return self.title
        try:
            return re.findall('(ep\s*[0-9a-z_]+)', self.title, re.I)[0].replace(' ', '').upper()
        except IndexError:
            return self.title

    @property
    def number(self):
        try:
            return int(self.id[2:])
        except ValueError:
            return -1

    @property
    def duration(self):
        return self._convert_to_seconds(self._episode['itunes_duration'])

    @property
    def summary(self):
        return self._episode['summary']

    @property
    def title(self):
        return self._episode['title']

    @property
    def length(self):
        for link in self._episode['links']:
            if link['type'] == 'audio/mpeg':
                return int(link['length'])
        return 0

    @property
    def guests(self):
        if self.summary.find('n la foto') >= 0:
            return self._parse_guests('n la foto')
        if self.summary.find('n las fotos') >= 0:
            return self._parse_guests('n las fotos')
        if self.summary.find('n el selfie') >= 0:
            return self._parse_guests('n el selfie')
        if self.summary.find('Contertulios de hoy') >= 0:
            return self._parse_guests('Contertulios de hoy')
        return []


    def _parse_guests(self, prefix):
        return re.split('\s*(?:,|;|:)\s*', re.findall(f'{prefix}[^A-Z]*:?\s*([^.]*)', self._cleanup_summary(self.summary), re.S)[0].strip())

    def _cleanup_summary(self, s):
        s = s.replace('J.', 'Jose')
        s = re.sub('\(.*?\)', '', s)
        s = s.replace(' y ', ', ')
        s = s.replace('Ángel López-Sánchez', 'Angel López')
        s = s.replace('Ángel López por videoconferencia', 'Angel López')
        s = s.replace('Ángel López', 'Angel López')
        s = s.replace('su Ibuprofeno;', '')
        s = s.replace('Serghey +', '')
        s = s.replace('Francisco Villatoro', 'Francis Villatoro')
        s = s.replace('Francis Villatoro Machuca', 'Francis Villatoro')
        s = s.replace('Hector Socas', 'Héctor Socas')
        s = s.replace('Ignacion', 'Ignacio')
        s = s.replace('Jose Alberto Rubiño Martín', 'Jose Alberto Rubiño')
        s = s.replace('Joserra Arévalo', 'Jose Ramón Arévalo')
        s = s.replace('Julio Castro Almazán', 'Julio Castro')
        s = s.replace('Ignacio Trujillo', 'Nacho Trujillo')
        s = s.replace('Nayra Rodríguez Eugenio', 'Nayra Rodríguez')
        s = s.replace('Noemí Pinilla Alonso', 'Noemí Pinilla')
        s = s.replace('Valentín Martínez Pillet', 'Valentín Martínez')
        s = s.replace('Alicia López Oramas', 'Alicia López')
        s = s.replace('Carlos González Fernández', 'Carlos González')
        s = s.replace('Andres Asensio', 'Andrés Asensio')
        s = s.replace('Bea Ruiz', 'Beatriz Ruiz')
        s = s.replace('Carlos Westendorp Plaza', 'Carlos Westendorp')
        s = s.replace('Ricardo García Soto', 'Ricardo García')
        return s

    def _convert_to_seconds(self, s):
        pieces = [int(t) for t in s.split(':')]
        if len(pieces) == 2:
            return pieces[1] + pieces[0] * 60
        else:
            return pieces[2] + pieces[1] * 60 + pieces[0] * 3600

