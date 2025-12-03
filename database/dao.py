from database.DB_connect import DBConnect
from model.rifugio import Rifugio
from model.sentiero import Sentiero


class DAO:
    """
        Implementare tutte le funzioni necessarie a interrogare il database.
        """
    # TODO
    @staticmethod
    def get_rifugi(year:int) -> list:
        """
            Interroga il database e restituisce una lista di tutti gli oggetti rifugio
            relativi all'anno param:year
            """
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """SELECT r.id , r.nome
                 FROM connessione c , rifugio r 
                 WHERE c.anno <= %s AND ( c.id_rifugio1 = r.id OR c.id_rifugio2 = r.id )
                 GROUP BY r.id """
        cursor.execute(query, (year,))
        result = cursor.fetchall()

        lista_rifugi = []
        for rifugio in result:
            rifugio = Rifugio(
                id=rifugio['id'],
                nome=rifugio['nome'],
            )
            lista_rifugi.append(rifugio)

        conn.close()
        cursor.close()
        return lista_rifugi

    @staticmethod
    def read_sentieri(year:int) -> list:
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT c.id , c.id_rifugio1 , c.id_rifugio2 
                FROM connessione c , rifugio r 
                WHERE c.anno <= %s AND ( c.id_rifugio1 = r.id OR c.id_rifugio2 = r.id )
                GROUP BY c.id_rifugio1 , c.id_rifugio2"""
        cursor.execute(query, (year,))
        result = cursor.fetchall()
        lista_sentieri = []
        for sentiero in result:
            sentiero = Sentiero(
                idSentiero=sentiero['id'],
                id1=sentiero['id_rifugio1'],
                id2=sentiero['id_rifugio2'],

            )
            lista_sentieri.append(sentiero)
        return lista_sentieri

