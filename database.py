import sqlite3
from pathlib import Path
from datetime import datetime, timedelta  


DB_PATH = Path("data") / "bibliotheque.db"


# --- Connection helper ---
def get_connection():
    """Create the DB if needed and return a connection."""
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# --- Initialize DB ---
def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Table des livres
    cur.execute("""
        CREATE TABLE IF NOT EXISTS livres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            auteur TEXT,
            categorie TEXT,
            proprietaire TEXT,
            proprietaire_email TEXT,
            disponibilite TEXT DEFAULT 'Disponible',
            emprunte_par TEXT,
            resume TEXT,
            couverture TEXT,
            date_ajout TEXT
        );
    """)

    # Table historique des emprunts
    cur.execute("""
        CREATE TABLE IF NOT EXISTS historique (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_livre INTEGER NOT NULL,
            emprunteur TEXT NOT NULL,
            emprunteur_email TEXT,
            date_emprunt TEXT NOT NULL,
            date_retour_prevue TEXT NOT NULL,
            date_retour TEXT,
            commentaire TEXT,
            FOREIGN KEY (id_livre) REFERENCES livres(id)
        );
    """)

    conn.commit()
    conn.close()
    conn = get_connection()
    cur = conn.cursor()

    # Table des livres
    cur.execute("""
        CREATE TABLE IF NOT EXISTS livres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            auteur TEXT,
            categorie TEXT,
            proprietaire TEXT,
            disponibilite TEXT DEFAULT 'Disponible',
            emprunte_par TEXT,
            resume TEXT,
            couverture TEXT,
            date_ajout TEXT
        );
    """)

    # Table historique des emprunts
    cur.execute("""
        CREATE TABLE IF NOT EXISTS historique (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_livre INTEGER NOT NULL,
            emprunteur TEXT NOT NULL,
            date_emprunt TEXT NOT NULL,
            date_retour TEXT,
            commentaire TEXT,
            FOREIGN KEY (id_livre) REFERENCES livres(id)
        );
    """)

    conn.commit()
    conn.close()


# --- Add a book ---

def ajouter_livre(titre, auteur, categorie, proprietaire, proprietaire_email, resume, couverture):
    conn = get_connection()
    cur = conn.cursor()

    date_ajout = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cur.execute("""
        INSERT INTO livres (titre, auteur, categorie, proprietaire, proprietaire_email, resume, couverture, date_ajout)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (titre, auteur, categorie, proprietaire, proprietaire_email, resume, couverture, date_ajout))

    conn.commit()
    conn.close()
    conn = get_connection()
    cur = conn.cursor()

    date_ajout = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cur.execute("""
        INSERT INTO livres (titre, auteur, categorie, proprietaire, resume, couverture, date_ajout)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (titre, auteur, categorie, proprietaire, resume, couverture, date_ajout))

    conn.commit()
    conn.close()


# --- Get all books ---
def get_livres():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM livres ORDER BY titre ASC")
    rows = cur.fetchall()

    conn.close()
    return rows


# --- Emprunter un livre ---
def emprunter_livre(id_livre, emprunteur, emprunteur_email, commentaire=""):
    conn = get_connection()
    cur = conn.cursor()

    # Date actuelle
    date_emprunt = datetime.now()
    date_emprunt_str = date_emprunt.strftime("%Y-%m-%d %H:%M:%S")

    # Date de retour prévue : + 30 jours
    date_retour_prevue = (date_emprunt + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")

    # Mise à jour du livre
    cur.execute("""
        UPDATE livres
        SET disponibilite = 'Indisponible', emprunte_par = ?
        WHERE id = ?
    """, (emprunteur, id_livre))

    # Ajout dans l'historique — NOTE : on met aussi emprunteur_email + date_retour_prevue
    cur.execute("""
        INSERT INTO historique (
            id_livre,
            emprunteur,
            emprunteur_email,
            date_emprunt,
            date_retour_prevue,
            commentaire
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (id_livre, emprunteur, emprunteur_email, date_emprunt_str, date_retour_prevue, commentaire))

    conn.commit()
    conn.close()    
# --- Rendre un livre ---
def rendre_livre(id_livre, commentaire=""):
    conn = get_connection()
    cur = conn.cursor()

    date_retour = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Remettre disponible
    cur.execute("""
        UPDATE livres
        SET disponibilite = 'Disponible', emprunte_par = NULL
        WHERE id = ?
    """, (id_livre,))

    # Compléter l’historique (dernier emprunt du livre)
    cur.execute("""
        UPDATE historique
        SET date_retour = ?, commentaire = ?
        WHERE id_livre = ? AND date_retour IS NULL
    """, (date_retour, commentaire, id_livre))

    conn.commit()
    conn.close()


# --- Historique complet ---
def get_historique():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT h.*, l.titre, l.proprietaire, l.proprietaire_email
        FROM historique h
        JOIN livres l ON l.id = h.id_livre
        ORDER BY date_emprunt DESC
    """)

    rows = cur.fetchall()
    conn.close()
    return rows
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT h.*, l.titre
        FROM historique h
        JOIN livres l ON l.id = h.id_livre
        ORDER BY date_emprunt DESC
    """)

    rows = cur.fetchall()
    conn.close()
    return rows

# --- Récupérer un livre par id ---
def get_livre(id_livre: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM livres WHERE id = ?", (id_livre,))
    row = cur.fetchone()
    conn.close()
    return row


# --- Mettre à jour un livre ---
def mettre_a_jour_livre(id_livre, titre, auteur, categorie, proprietaire, resume, couverture, disponibilite, emprunte_par):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE livres
        SET titre = ?,
            auteur = ?,
            categorie = ?,
            proprietaire = ?,
            resume = ?,
            couverture = ?,
            disponibilite = ?,
            emprunte_par = ?
        WHERE id = ?
    """, (titre, auteur, categorie, proprietaire, resume, couverture,
          disponibilite, emprunte_par, id_livre))

    conn.commit()
    conn.close()


# --- Supprimer un livre (et son historique associé) ---
def supprimer_livre(id_livre: int):
    conn = get_connection()
    cur = conn.cursor()

    # On supprime d'abord l'historique lié à ce livre
    cur.execute("DELETE FROM historique WHERE id_livre = ?", (id_livre,))
    # Puis le livre lui-même
    cur.execute("DELETE FROM livres WHERE id = ?", (id_livre,))

    conn.commit()
    conn.close()

def archiver_livre(id_livre: int):
    """Marque un livre comme archivé (il n'apparaîtra plus dans l'app)."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE livres
        SET disponibilite = 'Archivé',
            emprunte_par = NULL
        WHERE id = ?
        """,
        (id_livre,),
    )

    conn.commit()
    conn.close()
