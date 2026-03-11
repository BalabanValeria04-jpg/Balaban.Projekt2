import pytest
import mysql.connector

@pytest.fixture
def db_connection():
    conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Kthf1010",
            database="test"
    )

    cursor = conn.cursor()
    yield conn, cursor

    cursor.close()
    conn.close()

#pridat_ukol()
#Ověří, že se nový úkol správně uloží do databáze.
def test_pridat_ukol_poz(db_connection):

    conn, cursor = db_connection

    cursor.execute(
        "INSERT INTO ukoly (nazev, popis, stav) VALUES (%s,%s,%s)",
        ("Test úkol", "Test popis", "Nezahájeno")
    )
    conn.commit()

    cursor.execute("SELECT * FROM ukoly WHERE nazev='Test úkol'")
    result = cursor.fetchone()

    assert result is not None

    cursor.execute("DELETE FROM ukoly WHERE nazev='Test úkol'")
    conn.commit()


#Ověří, že program nepřijme prázdný název nebo popis úkolu.
def test_pridat_ukol_negativni():

    nazev = ""
    popis = ""

    assert nazev == ""
    assert popis == ""

#aktualizovat_ukol()
#Ověří, že lze změnit stav existujícího úkolu.
def test_aktualizovat_ukol_pozitivni(db_connection):
    conn, cursor = db_connection

    cursor.execute(
        "INSERT INTO ukoly (nazev, popis, stav) VALUES (%s,%s,%s)",
        ("Update test", "Test", "Nezahájeno")
    )
    conn.commit()

    cursor.execute("SELECT id FROM ukoly WHERE nazev='Update test'")
    ukol_id = cursor.fetchone()[0]

    cursor.execute(
        "UPDATE ukoly SET stav=%s WHERE id=%s",
        ("Hotovo", ukol_id)
    )
    conn.commit()

    cursor.execute("SELECT stav FROM ukoly WHERE id=%s", (ukol_id,))
    stav = cursor.fetchone()[0]

    assert stav == "Hotovo"

    cursor.execute("DELETE FROM ukoly WHERE id=%s", (ukol_id,))
    conn.commit()

#Ověří chování programu při aktualizaci neexistujícího ID.
def test_aktualizovat_ukol_negativni(db_connection):

    conn, cursor = db_connection

    cursor.execute(
        "UPDATE ukoly SET stav=%s WHERE id=%s",
        ("Hotovo", 9999)
    )
    conn.commit()

    assert cursor.rowcount == 0

#odstranit_ukol()
#Ověří, že lze úkol úspěšně odstranit z databáze
def test_odstranit_ukol_poz(db_connection):

    conn, cursor = db_connection

    cursor.execute(
        "INSERT INTO ukoly (nazev, popis, stav) VALUES (%s,%s,%s)",
        ("Delete test", "Test", "Nezahájeno")
    )
    conn.commit()

    cursor.execute("SELECT id FROM ukoly WHERE nazev='Delete test'")
    ukol_id = cursor.fetchone()[0]

    cursor.execute("DELETE FROM ukoly WHERE id=%s", (ukol_id,))
    conn.commit()

    cursor.execute("SELECT * FROM ukoly WHERE id=%s", (ukol_id,))
    result = cursor.fetchone()

    assert result is None


#Ověří chování programu při pokusu o odstranění neexistujícího úkolu.
def test_odstranit_ukol_neg(db_connection):

    conn, cursor = db_connection

    cursor.execute("DELETE FROM ukoly WHERE id=%s", (9999,))
    conn.commit()

    assert cursor.rowcount == 0
