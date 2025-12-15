def register(self):
    username = username1.get()
    password = password1.get()
    if not username:
        return False, print("Username required")

    if len(password) < 8:
        return False, print("Password must be at least 8 character")
    elif not re.search(r"[A-Z]", password):
        return False, print("Password must at least contain a upper letter")
    elif not re.search(r"[a-z]", password):
        return False, print("Password must at least contain a lower letter")
    elif not re.search(r"\d", password):
        return False, print("Password must contain at least one number")
    else:
        try:
            password = "password".encode()
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
            c.execute("INSERT INTO users(username, password) VALUES(?,?)", (username, hashed_password))
            conn.commit()
            print("Registered successfully")
        except sqlite3.IntegrityError:
            print("Username already exists")
        except sqlite3.OperationalError:
            print("Database is locked, try again:")
        finally:
            con.close()


def login(self):
    username = username1.get()

    try:
        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        c.execute("SELECT password FROM users WHERE username = ?", (username,))
        row = c.fetchone()

        if not row:
            print("Invalid username")
            return False
        else:
            print("Logged in successfully")

    except sqlite3.OperationalError:
        print("Database is locked, try again:")
    finally:
        conn.close()