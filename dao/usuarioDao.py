from model.usuario import Usuario

SQL_USUARIO_POR_ID = 'SELECT id, nome, senha from usuario where id = %s'

class UsuarioDao:
    def __init__(self, db):
        self.__db = db

    def buscar_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_USUARIO_POR_ID, (id,))
        dados = cursor.fetchone()
        usuario = self.__traduz_usuario(dados) if dados else None
        return usuario

    @classmethod
    def __traduz_usuario(self, tupla):
        return Usuario(tupla[0], tupla[1], tupla[2])
