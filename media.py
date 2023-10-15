

class Image:
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return f'<one-social media.image object at "{self.path}">'

    def copy_to_clipboard(self):
        from libs.clipboard import copy_img
        copy_img(self.path)

