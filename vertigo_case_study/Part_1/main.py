from flask import Flask, request, jsonify
import uuid
import psycopg2
import os

app = Flask(__name__)

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

def get_conn():
    return psycopg2.connect(**DB_CONFIG)

@app.route("/clans", methods=["POST"])
def create_clan():
    data = request.get_json()
    clan_id = str(uuid.uuid4())
    name = data["name"]
    region = data.get("region")

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO clans (id, name, region) VALUES (%s, %s, %s)",
                (clan_id, name, region)
            )
        conn.commit()

    return jsonify({"id": clan_id, "message": "Clan created successfully."})

@app.route("/clans", methods=["GET"])
def list_clans():
    region = request.args.get("region")
    query = "SELECT id, name, region, created_at FROM clans"
    params = []

    if region:
        query += " WHERE region = %s"
        params.append(region)

    query += " ORDER BY created_at DESC"

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            results = cur.fetchall()

    clans = [
        {
            "id": row[0],
            "name": row[1],
            "region": row[2],
            "created_at": row[3].isoformat() if row[3] else None
        }
        for row in results
    ]
    return jsonify(clans)

@app.route("/clans/<id>", methods=["DELETE"])
def delete_clan(id):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM clans WHERE id = %s", (id,))
            deleted = cur.rowcount
        conn.commit()

    if deleted:
        return jsonify({"message": f"Clan {id} deleted successfully."})
    else:
        return jsonify({"message": "Clan not found"}), 404

@app.route("/", methods=["GET"])
def health_check():
    return "API is running!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)