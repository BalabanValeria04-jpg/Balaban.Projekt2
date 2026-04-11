import mysql.connector
from mysql.connector import Error

def pripojeni_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Kthf1010",
            database="test"
        )

        if conn.is_connected():
            return conn

    except Error as e:
        print(f"Chyba při připojení k databázi: {e}")
        return None

def vytvoreni_tabulky(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ukoly (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nazev VARCHAR(255) NOT NULL,
            popis TEXT NOT NULL,
            stav ENUM('Nezahájeno', 'Probíhá', 'Dokončeno') DEFAULT 'Nezahájeno',
            datum_vytvoreni DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

def pridat_ukol(conn, nazev, popis):
    if not nazev or not popis:
        raise ValueError("Název a popis nesmí být prázdné")

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO ukoly (nazev, popis, stav) VALUES (%s, %s, %s)",
        (nazev, popis, "Nezahájeno"))
    conn.commit()
    

def zobrazit_ukoly(conn, stav=None):
    cursor = conn.cursor()

    if stav:
        cursor.execute("""
            SELECT id, nazev, popis, stav, datum_vytvoreni
            FROM ukoly
            WHERE stav = %s
        """, (stav,))
    else:
        cursor.execute("""
            SELECT id, nazev, popis, stav, datum_vytvoreni
            FROM ukoly
        """)

    return cursor.fetchall()

def aktualizovat_ukol(conn, ukol_id, stav):
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM ukoly WHERE id=%s", (ukol_id,))
    if cursor.fetchone() is None:
        raise ValueError("Ukol neexistuje")

    cursor.execute(
        "UPDATE ukoly SET stav=%s WHERE id=%s",
        (stav, ukol_id))
    conn.commit()


def odstranit_ukol(conn, ukol_id):
    cursor = conn.cursor()

    cursor.execute("DELETE FROM ukoly WHERE id=%s", (ukol_id,))
    conn.commit()

    if cursor.rowcount == 0:
        raise ValueError("Úkol neexistuje")
    
def hlavni_menu(conn):
    while True:
        print("\nHlavní menu:")
        print("\n1. Přidat úkol")
        print("2. Zobrazit úkoly")
        print("3. Aktualizovat úkol")
        print("4. Odstranit úkol")
        print("5. Konec")

        volba = input("Vyberte: ")

        if volba == "1":
            nazev = input("Zadejte název: ")
            popis = input("Zadejte popis: ")

            try:
                pridat_ukol(conn, nazev, popis)
                print("Úkol přidán")
            except ValueError as e:
                print(e)

        elif volba == "2":
            ukoly = zobrazit_ukoly(conn)
            if not ukoly:
                print("Žádné úkoly")
            else:
                for u in ukoly:
                    print(u)

        elif volba == "3":
            try:
                ukol_id = int(input("Zadejte ID: "))
                print("1 - Probíhá")
                print("2 - Hotovo")

                stav_volba = input("Vyberte stav: ")

                if stav_volba == "1":
                    stav = "Probíhá"
                elif stav_volba == "2":
                    stav = "Hotovo"
                else:
                    print("Neplatná volba")
                    continue

                aktualizovat_ukol(conn, ukol_id, stav)
                print("Úkol aktualizován")

            except ValueError as e:
                print(e)

        elif volba == "4":
            try:
                ukol_id = int(input("Zadejte ID: "))
                odstranit_ukol(conn, ukol_id)
                print("Úkol odstraněn")

            except ValueError as e:
                print(e)

        elif volba == "5":
            print("Konec programu")
            break

        else:
            print("Neplatná volba")


if __name__ == "__main__":
    conn = pripojeni_db()
    vytvoreni_tabulky(conn)
    hlavni_menu(conn)
    conn.close()

