class Info(object):
    __db = None
    __image_store_service = None

    def __init__(self):
        pass

    @staticmethod
    def set_db(db):
        # This if is here to make sure there's
        # only one db instance
        if Info.__db is None:
            Info.__db = db

    @staticmethod
    def get_db():
        return Info.__db

    @staticmethod
    def set_image_store_service(s):
        # This if is here to make sure there's
        # only one image store service instance
        if Info.__image_store_service is None:
            Info.__image_store_service = s

    @staticmethod
    def get_image_store_service():
        return Info.__image_store_service