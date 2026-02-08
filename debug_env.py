#debug_env.py
from pathlib import Path
from dotenv import load_dotenv, dotenv_values
import os, sys, urllib.parse
import certifi
from pymongo import MongoClient
from pymongo.errors import PyMongoError

BASE_DIR = Path(__file__).resolve().parent
print("cwd:", Path.cwd())
print(".env path:", (BASE_DIR / ".env").resolve())
print(".env parsed (raw):", dotenv_values(BASE_DIR / ".env"))

# load .env from this script folder explicitly
load_dotenv(BASE_DIR / ".env")

USER = os.getenv("MY_USERNAME")
PWD = os.getenv("MY_PASSWORD")
DBNAME = os.getenv("MY_DB", "flamingo")

print("MY_USERNAME repr:", repr(USER))
print("MY_PASSWORD present:", bool(PWD))
print("MY_DB:", DBNAME)

if not USER or not PWD:
    print("ERROR: Missing MY_USERNAME or MY_PASSWORD. Fix .env formatting or path.")
    sys.exit(1)

pwd_enc = urllib.parse.quote_plus(PWD)
uri = f"mongodb+srv://{USER}:{pwd_enc}@cluster0.ze8mjac.mongodb.net/{DBNAME}?retryWrites=true&w=majority"
print("Using URI (trimmed):", uri[:80] + "...")

try:
    client = MongoClient(uri, tls=True, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=10000)
    print("Attempting ping...")
    print("Ping result:", client.admin.command("ping"))
    print("SUCCESS: MongoDB reachable and authenticated.")
except PyMongoError as e:
    print("MongoDB error:", e)
finally:
    try: client.close()
    except: pass
