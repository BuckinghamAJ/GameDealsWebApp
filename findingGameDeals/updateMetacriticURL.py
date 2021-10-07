import pymysql



def main():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='22ehH0C2!View2011!',
                                 db='Game_Deals',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        cursor.execute("SELECT id,title,metacriticURL FROM deals WHERE imageURL IS NULL;")
        wrongMetaCriticURLs = cursor.fetchall()

        for wrongURL in wrongMetaCriticURLs:
            id = wrongURL["id"]
            metacriticURL = wrongURL["metacriticURL"]

            print(f"Current Metacritic URL: {metacriticURL}")
            newURL = input("Please Enter the correct URL: ").rstrip()
            print()

            if newURL.lower() == "delete":
                cursor.execute(f"DELETE FROM deals WHERE id={id}")
                connection.commit()
            else:
                cursor.execute(f"UPDATE deals SET metacriticURL='{newURL}' WHERE id={id}")
                connection.commit()


    connection.commit()

if __name__ == "__main__":
    main()