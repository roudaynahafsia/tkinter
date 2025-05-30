from connection import CONNECTION

class Categorie:
    """
    Cette classe représente la table 'categories' et permet les opérations CRUD.
    """

    @staticmethod
    def create(nom):
        """
        Enregistre une catégorie dans la base de données.
        Retourne le nombre de lignes affectées (0 ou 1).
        """
        ligne = 0
        try:
            CONNECTION.ping(reconnect=True)
            with CONNECTION.cursor() as cursor:
                sql = "INSERT INTO `categories` (`nom`) VALUES (%s)"
                ligne = cursor.execute(sql, (nom,))
            CONNECTION.commit()
        except Exception as e:
            print('Une erreur est survenue lors de la création :', e)
            CONNECTION.rollback()
        return ligne

    @staticmethod
    def getAll():
        """
        Récupère toutes les catégories sous forme de liste de dictionnaires.
        """
        categories = []
        try:
            CONNECTION.ping(reconnect=True)
            with CONNECTION.cursor() as cursor:
                sql = "SELECT * FROM `categories`"
                cursor.execute(sql)
                categories = cursor.fetchall()
        except Exception as e:
            print('Une erreur est survenue lors de la récupération :', e)
        return categories

    @staticmethod
    def update(id, nom):
        """
        Met à jour le nom de la catégorie identifiée par son id.
        Retourne le nombre de lignes affectées.
        """
        rows = 0
        try:
            CONNECTION.ping(reconnect=True)
            with CONNECTION.cursor() as cursor:
                sql = "UPDATE `categories` SET nom=%s WHERE id=%s"
                rows = cursor.execute(sql, (nom, id))
            CONNECTION.commit()
        except Exception as e:
            print('Une erreur est survenue lors de la mise à jour :', e)
            CONNECTION.rollback()
        return rows

    @staticmethod
    def delete(id):
        """
        Supprime la catégorie identifiée par son id.
        Retourne le nombre de lignes affectées.
        """
        rows = 0
        try:
            CONNECTION.ping(reconnect=True)
            with CONNECTION.cursor() as cursor:
                sql = "DELETE FROM `categories` WHERE id=%s"
                rows = cursor.execute(sql, (id,))
            CONNECTION.commit()
        except Exception as e:
            print('Une erreur est survenue lors de la suppression :', e)
            CONNECTION.rollback()
        return rows

    @staticmethod
    def getByName(nom):
        """
        Récupère une catégorie par son nom (retourne un dictionnaire ou None).
        """
        categorie = None
        try:
            CONNECTION.ping(reconnect=True)
            with CONNECTION.cursor() as cursor:
                sql = "SELECT * FROM `categories` WHERE nom=%s"
                cursor.execute(sql, (nom,))
                categorie = cursor.fetchone()
        except Exception as e:
            print('Une erreur est survenue lors de la recherche par nom :', e)
        return categorie
