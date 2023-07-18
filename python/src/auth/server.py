import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL

# create a flask app object
print(__name__)
server = Flask(__name__)

# pass the flask app object to mysql
mysql = MySQL(server)

# config
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = int(os.environ.get("MYSQL_PORT"))


# Create a basic login route
@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "Missing credentials", 401
    else:
        # create a cursor to execute queries
        cur = mysql.connection.cursor()

        # raw queries
        res = cur.execute("SELECT email,password FROM user WHERE email=%s", (auth.username,))

        if res > 0:
            # user exists
            user_row = cur.fetchone()
            email = user_row[0]
            password = user_row[1]

            # check for credentials if valid then create a JWT token and send
            if auth.username != email or auth.password != password:
                return "invalid credentials", 401
            else:
                return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
        else:
            return "Invalid credentials", 401


def createJWT(username, secret, authz):
    """
    this method creates the jwt tokoen that will be sent ot the requesting user after validation of username & password.
    this jwt token will be used by the user for subsequent requests.
    jwt token comprises header, payload

    :param username:
    :param secret:
    :param authz:
    :return:
    """
    jwt.encode(
        # Payload
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "admin": authz,
        },
        # JWT secret Key
        secret,
        algorithm="HS256",
    )


@server.route("/validate")
def validate():
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return "missing credentials", 401

    encoded_jwt = encoded_jwt.split(" ")[1]

    try:
        decoded = jwt.decode(encoded_jwt, os.environ.get("JWT_SECRET"), algorithms="HS256")
    except:
        return "Not authorized"

    return decoded


@server.route("/test")
def test():
    return "hello world"


if __name__ == "__main__":
    server.run(host="0.0.0.0", port="8000")
