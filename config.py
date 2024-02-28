""" Настройки приложения """

DB = {
    'engine': 'postgresql+psycopg2',
    'host': 'analytics.maximum-auto.ru',
    'port': 15432,
    'user': 'kuznecovar',
    'password': '7hjSHx6OU3yK',
    'schema': 'data'
}
engine = "{engine}://{user}:{password}@{host}:{port}/{schema}".format(**DB)
