class NotImage(Exception):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def __str__(self) -> str:
        return f'{self.path} Não é uma imagem válida'
