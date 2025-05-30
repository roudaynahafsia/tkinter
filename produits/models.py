from connection import CONNECTION

class Produit:

    @staticmethod
    def create(nom, quantite, prix, date_expiration, id_categorie):
        'Enregistrement d\'une ligne de produit dans la base de données'
        val = 0
        try:
            CONNECTION.ping()
            with CONNECTION.cursor() as cursor:
                SQL = '''INSERT INTO produits (nom, quantite, prix, date_expiration, id_categorie) 
                         VALUES (%s, %s, %s, %s, %s)'''
                val = cursor.execute(SQL, (nom, quantite, prix, date_expiration, id_categorie))
        except Exception as ex:
            print('Erreur lors de la création :', ex)
            CONNECTION.rollback()
        else:
            CONNECTION.commit()
        finally:
            CONNECTION.close()
        return val

    @staticmethod
    def all():
        'Retourner tous les enregistrements de produits'
        pts = []
        try:
            CONNECTION.ping()
            with CONNECTION.cursor() as cursor:
                SQL = '''SELECT * FROM produits'''
                cursor.execute(SQL)
                pts = cursor.fetchall()
        except Exception as ex:
            print('Erreur lors de la récupération des produits :', ex)
        finally:
            CONNECTION.close()
        return pts

    @staticmethod
    def getById(id):
        'Retourne un produit par son ID'
        produit = None
        try:
            CONNECTION.ping()
            with CONNECTION.cursor() as cursor:
                SQL = '''SELECT * FROM produits WHERE id = %s'''
                cursor.execute(SQL, (id,))
                produit = cursor.fetchone()
        except Exception as ex:
            print('Erreur lors de la récupération du produit :', ex)
        finally:
            CONNECTION.close()
        return produit

    @staticmethod
    def update(id, nom, quantite, prix, date_expiration, id_categorie):
        'Met à jour un produit existant'
        rows = 0
        try:
            CONNECTION.ping()
            with CONNECTION.cursor() as cursor:
                SQL = '''UPDATE produits 
                         SET nom=%s, quantite=%s, prix=%s, date_expiration=%s, id_categorie=%s 
                         WHERE id=%s'''
                rows = cursor.execute(SQL, (nom, quantite, prix, date_expiration, id_categorie, id))
        except Exception as ex:
            print('Erreur lors de la mise à jour :', ex)
            CONNECTION.rollback()
        else:
            CONNECTION.commit()
        finally:
            CONNECTION.close()
        return rows

    @staticmethod
    def delete(id):
        'Supprime un produit par son ID'
        rows = 0
        try:
            CONNECTION.ping()
            with CONNECTION.cursor() as cursor:
                SQL = '''DELETE FROM produits WHERE id = %s'''
                rows = cursor.execute(SQL, (id,))
        except Exception as ex:
            print('Erreur lors de la suppression :', ex)
            CONNECTION.rollback()
        else:
            CONNECTION.commit()
        finally:
            CONNECTION.close()
        return rows
