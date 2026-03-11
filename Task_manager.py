import mysql.connector

# Připojení k databázi
def pripojeni_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Kthf1010",
            database="test"
        )
        cursor = conn.cursor()
        print("Připojení k databázi bylo úspěšné.")
    except mysql.connector.Error as err:
        print(f"Chyba při připojování: {err}")
    return conn, cursor
conn, cursor = pripojeni_db()


def vytvoreni_tabulky():
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ukoly (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nazev VARCHAR(100),
                popis TEXT,
                stav VARCHAR(50) DEFAULT 'Nezahájeno',   
                datum_vytvoreni TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("Tabulka 'ukoly' byla vytvořena.")
    except mysql.connector.Error as err:
        print(f"Chyba při vytváření tabulky: {err}")
        
    print("Připojení k databázi bylo uzavřeno.")

def hlavni_menu():
    while True:
        print ("\nSprávce úkolú - Hlavní menu\n\n"+"1. Pridat nový úkol\n"+"2. Zobrazit vsechny úkoly\n"+"3. Aktualizovat_ukol\n"+ "4. Odstranit úkol\n"+ "5. Konec programu\n")
        user_input = input("Vyberte moznost (1-5): ")
        while user_input not in ["1","2","3","4","5"]:
            print("Je to chybná hodnota.")
            user_input = input("Vyberte moznost (1-5): ")

        if user_input == "1":
            pridat_ukol()

        elif user_input == "2":
            zobrazit_ukoly()

        elif user_input == "3":
            aktualizovat_ukol()

        elif user_input == "4":
            odstranit_ukol()

        elif user_input == "5":
            print("\n\nKonec programu.")
            break

def pridat_ukol():
    nazev_ukolu = input("\nZadejte název úkolu: ").strip()

    while nazev_ukolu == "":
        print("Je to prázdná hodnota. Zadejte název úkolu.")
        nazev_ukolu = input("Zadejte název úkolu: ").strip()
            
    popis_ukolu = input("Zadejte popis úkolu:").strip()
    while popis_ukolu == "":
        print("Je to prazdná hodnota. Zadejte popis úkolu.")
        popis_ukolu = input("Zadejte popis úkolu: ").strip()

   
    try:
        cursor.execute("INSERT INTO ukoly (nazev, popis, stav) VALUES (%s, %s, %s)",
        (nazev_ukolu, popis_ukolu, "Nezahájeno"))
        conn.commit()
        print("Ukol byl vložen.")
    except mysql.connector.Error as err:
        print(f"Chyba při vkládání dat: {err}\n")
    

def zobrazit_ukoly():

    try:
        cursor.execute("""
    SELECT id, nazev, popis, stav
    FROM ukoly
    WHERE stav IN ('Nezahájeno','Probíhá')
    """)

        ukoly = cursor.fetchall()

        if len(ukoly) == 0:
            print("\nNemáte ještě žádné úkoly. Přidejte úkol. Vyberte č.1.\n")
            return

        print("\nSeznam úkolů:")
        print("ID | Název | Popis | Stav" )
        print("-" * 40)

        for ukol in ukoly:
            print(f"{ukol[0]} | {ukol[1]} | {ukol[2]} | {ukol[3]}")

    except mysql.connector.Error as err:
        print(f"Chyba při načítání dat: {err}")

def aktualizovat_ukol():

    cursor.execute("""
        SELECT id, nazev, popis, stav
        FROM ukoly
        WHERE stav IN ('Nezahájeno','Probíhá')
    """)

    ukoly = cursor.fetchall()

    if len(ukoly) == 0:
        print("\nNemáte žádné úkoly ke změně. Přidejte úkol. Vyberte č.1.\n")
        return

    zobrazit_ukoly()

    while True:
        id_ukolu = input("\nZadejte ID úkolu, který chcete změnit: ")

        cursor.execute("SELECT * FROM ukoly WHERE id=%s", (id_ukolu,))
        ukol = cursor.fetchone()

        if ukol is None:
            print("Úkol s tímto ID neexistuje. Zadejte ID znovu.")
        else:
            break

    print("\nNový stav:")
    print("1 - Probíhá")
    print("2 - Hotovo")

    volba = input("Vyberte: ")

    if volba == "1":
        stav = "Probíhá"
    elif volba == "2":
        stav = "Hotovo"
    else:
        print("Neplatná volba.")
        return

    try:
        cursor.execute(
            "UPDATE ukoly SET stav=%s WHERE id=%s",
            (stav, id_ukolu)
        )
        conn.commit()

        print("Stav úkolu byl aktualizován.")

    except mysql.connector.Error as err:
        print(f"Chyba při aktualizaci: {err}")

def odstranit_ukol():

    try:
        cursor.execute(""" SELECT id, nazev, popis, stav FROM ukoly """)

        ukoly = cursor.fetchall()

        if len(ukoly) == 0:
            print("\nNemáte ještě žádné úkoly. Přidejte úkol. Vyberte č.1.\n")
            return

        print("\nSeznam úkolů:")
        print("ID | Název | Popis | Stav" )
        print("-" * 40)

        for ukol in ukoly:
            print(f"{ukol[0]} | {ukol[1]} | {ukol[2]} | {ukol[3]}")
    except mysql.connector.Error as err:
        print(f"Chyba při načítání dat: {err}")
    while True:
        id_ukolu = input("\nZadejte ID úkolu, který chcete odstranit: ")

        if not id_ukolu.isdigit():
                    print("ID musí být číslo.")
                    continue
        try:
            cursor.execute("DELETE FROM ukoly WHERE id=%s", (id_ukolu,))
            conn.commit()

            if cursor.rowcount == 0:
                print("\nÚkol s tímto ID neexistuje.")
            
            else:
                print("\nÚkol byl úspěšně odstraněn.")
                break
        except mysql.connector.Error as err:
            print(f"Chyba při mazání dat: {err}") 

pripojeni_db()
vytvoreni_tabulky()
hlavni_menu()

