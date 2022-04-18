from os import environ as env
from dotenv import load_dotenv
from datetime import datetime
from core.dependencies import PasscodeTOTP
from time import sleep

load_dotenv("node-env.vars")  # ! Adjust this as possible.
otp_interval: int = 15

AUTH_KEY: str | None = env.get("AUTH_KEY", None)
SECRET_KEY: str | None = env.get("SECRET_KEY", None)

if AUTH_KEY is not None and SECRET_KEY is not None:
    totp_instance: PasscodeTOTP = PasscodeTOTP(
        base_code=[AUTH_KEY, SECRET_KEY], interval=otp_interval, issuer="local"
    )
else:
    print("`AUTH_KEY` or `SECRET_KEY` is missing.")
    exit(-1)

nth: int = 1
while True:
    print(
        f"Iteration #{nth} | Date: {datetime.now()} | Current OTP: {totp_instance.get_code()} | Passcode will refresh after {otp_interval} seconds."
    )
    nth += 1
    sleep(otp_interval)
