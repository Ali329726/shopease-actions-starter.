
import os
from flask import Flask, jsonify
import redis

app = Flask(__name__)

PRICES = {
    "laptop": 55000,
    "headphones": 2500,
    "keyboard": 1200,
}

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=6379,
    decode_responses=True,
)

@app.route("/")
def home():
    return jsonify(message="Welcome to ShopEase!")

@app.route("/prices")
def prices():
    return jsonify(PRICES)

@app.route("/health")
def health():
    try:
        redis_client.ping()
        return jsonify(status="healthy", redis="connected"), 200
    except redis.RedisError:
        return jsonify(status="degraded", redis="disconnected"), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
