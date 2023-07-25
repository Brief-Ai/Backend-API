class SearchRouter:
    def db_for_read(self, model, **hints):
        if model == Search:
            return 'search_database'
        return None

    def db_for_write(self, model, **hints):
        if model == Search:
            return 'search_database'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name == 'Search':
            return db == 'search_database'
        return None