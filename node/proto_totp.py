from os import environ as env
from dotenv import load_dotenv
from core.dependencies import PasscodeTOTP
from time import time

from core.constants import AUTH_CODE_APP_NAME, AUTH_CODE_ISSUER_NAME

load_dotenv("node-env.vars")  # ! Adjust this as possible.
otp_interval: int = 30

AUTH_KEY: str | None = env.get("AUTH_KEY", None)
SECRET_KEY: str | None = env.get("SECRET_KEY", None)

if AUTH_KEY is not None and SECRET_KEY is not None:
    totp_instance: PasscodeTOTP = PasscodeTOTP(
        base_code=[AUTH_KEY, SECRET_KEY],
        name=AUTH_CODE_APP_NAME,
        issuer=AUTH_CODE_ISSUER_NAME,
    )

else:
    print("`AUTH_KEY` or `SECRET_KEY` is missing.")
    exit(-1)

nth: int = 1
start = time()
stored_passcode = None

while True:
    if totp_instance.get_code() != stored_passcode:
        print(
            f"Time Elapsed: {time() - start} | Current OTP: {totp_instance.get_code()} | Passcode will refresh after {otp_interval} seconds."
        )
        stored_passcode = totp_instance.get_code()
