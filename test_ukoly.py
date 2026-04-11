import pytest
from Task_manager import *


@pytest.fixture
def conn():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Kthf1010",
        database="test_test"   
    )

    vytvoreni_tabulky(conn) 

    yield conn

    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE ukoly")
    conn.commit()
    conn.close()


# pridani ukolu

def test_pridat_ukol_pozitivni(conn):
    pridat_ukol(conn, "Test", "Popis")

    cursor = conn.cursor()
    cursor.execute("SELECT nazev, popis FROM ukoly WHERE nazev=%s", ("Test",))
    result = cursor.fetchone()

    assert result == ("Test", "Popis")


def test_pridat_ukol_negativni(conn):
    with pytest.raises(ValueError):
        pridat_ukol(conn, "", "")


# aktualizaci ukolu

def test_aktualizovat_ukol_pozitivni(conn):
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO ukoly (nazev, popis, stav) VALUES (%s, %s, %s)",
        ("Test", "Popis", "Nezahájeno")
    )
    conn.commit()

    cursor.execute(
        "SELECT id FROM ukoly WHERE nazev=%s",
        ("Test",)
    )
    ukol_id = cursor.fetchone()[0]

    aktualizovat_ukol(conn, ukol_id, "Dokončeno")

    cursor.execute(
        "SELECT stav FROM ukoly WHERE id=%s",
        (ukol_id,)
    )
    stav = cursor.fetchone()[0]

    assert stav == "Dokončeno"


def test_aktualizovat_ukol_negativni(conn):
    with pytest.raises(ValueError):
        aktualizovat_ukol(conn, 9999, "Hotovo")


# odstareni ukolu

def test_odstranit_ukol_pozitivni(conn):
    pridat_ukol(conn, "Test", "Popis")

    cursor = conn.cursor()
    cursor.execute("SELECT id FROM ukoly WHERE nazev=%s", ("Test",))
    ukol_id = cursor.fetchone()[0]

    odstranit_ukol(conn, ukol_id)

    cursor.execute("SELECT * FROM ukoly WHERE id=%s", (ukol_id,))
    result = cursor.fetchone()

    assert result is None


def test_odstranit_ukol_negativni(conn):
    with pytest.raises(ValueError):
        odstranit_ukol(conn, 9999)

if __name__ == "__main__":
    conn = pripojeni_db()

    if conn:  
        vytvoreni_tabulky(conn)
        hlavni_menu(conn)
        conn.close()
    else:
        print("Nepodařilo se připojit k databázi")