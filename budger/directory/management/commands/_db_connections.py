"""
Читает конфиг и возвращает два connection: (job, database)
"""


import psycopg2
from configparser import ConfigParser


__all__ = ['get']


def process_section(parser, section):
    if parser.has_section(section):
        parser_items = parser.items(section)
        params = {}
        for param in parser_items:
            params[param[0]] = param[1]
        return params

    return None


def get(filename='database.ini'):
    parser = ConfigParser()
    parser.read(filename)

    params = process_section(parser, 'jobs')
    conn_jobs = psycopg2.connect(**params)

    params = process_section(parser, 'django')
    conn_django = psycopg2.connect(**params)

    return conn_jobs, conn_django
