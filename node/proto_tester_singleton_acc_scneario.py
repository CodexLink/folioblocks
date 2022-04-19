"""
# Prototype Internal Tester

- This script tests the internals regarding user-based transactions.
- Note that this is the automate version of a single set of accounts to assert that everything is working before integrating it to the frontend.
"""
from asyncio import run as asyncio_run
from os import environ as env
from typing import Any, Final
from zoneinfo import available_timezones

from dotenv import load_dotenv
from pydantic import EmailStr

from core.constants import HTTPQueueMethods, URLAddress
from core.constants import UserEntity
from core.dependencies import PasscodeTOTP, get_totp_instance
from utils.http import get_http_client_instance
from faker import Faker

# # Constants.
target_node: str = "127.0.0.1"
target_port: int = 6001

"""
# # Scenario.
* A certain company is interested on hiring certain individuals from the certain organization (whether it would be an organization (educational) or an institution).
* With that, the company posted their interests on the certain applicants who is under `Computer Engineering`.
* As a response, some organization or institution will setup an account for the applicants, as well as documents to be referred to them to show the individuals' past experience from projects, activities and recognitions.
* [1] | Any interested applications should be able to apply, with that, the company will look at the requests by looking at their credentials (in exposed-form, but no sensitive information) [2] and should contact for potential interview to reveal the individual under addresses.

* [3] At this point, a particular company seem to be too fishy on this one particular transaction where its credentials seem to be uneven, with that they contacted the administrator to validate the integrity if the content given is real and the origin is from someone inside of the institution. By comparing the signature of the raw and processed hash, we can validate it and ensure that the content displayed is right.

# # Scenario Constraints

* There 3 objectives in the paper, and each objective requires 20 tests.
* Therefore, 3 objectives * 20 tests = 60 tests overall.
* Each scenario must have two entities wherein each entity must do the 10 tests as well as the other one.

# # Previous (May still be used) Constraints
* [1] For each scenario, (5 with documents, 5 without documents) or both 10 with documents. Extra info varies. Applies from remaining constraints given below.
* [2] View the inserted credentials. (5 with documents, 5 without documents (with addresses reference))
* [3] Look up at the blockchain and technical. (Will video or setup a mechanics sooner or later)

# # Concluding Requirements
! Production Testing Scenario (REQUIRE FRONTEND)
- We may need 10 temporary emails for each scenario (2 for the organizer, 2 for the employer, 6 for the students) + 5 personal email, 1 for the master, 4 for the archival miner.

! Local Testing Scenario
- We may need 3 personal email for the credentials (1 for the organizer, 1 for the student, and 1 employer).
"""

institution_account: dict[str, Any] = {}
org_account: dict[str, Any] = {}
student_account: dict[str, Any] = {}

available_courses: Final[list[str]] = [  # # Not sure how much but, 5 courses is enough.
    "Computer Engineering",
    "Information Technology",
    "Nursing",
    "Electronics and Commmunications Engineering",
    "Computer Science",
]
chosen_courses: list[str] = []

faker: Faker = Faker()

# - Setup institution, student and another organization account.
for each_account in range(0, 3):  # - 1.
    account: dict = {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "username": faker.user_name(),
        "password": faker.password(),
        "type": UserEntity.INSTITUTION_DASHBOARD_USER
        if not each_account
        else UserEntity.APPLICANT_DASHBOARD_USER
        if each_account == 1
        else UserEntity.ORGANIZATION_DASHBOARD_USER,
    }  # type: ignore

    email_address: EmailStr = EmailStr(
        input(
            f"Please provide email address for {account['username']}. (Type: {account['type']}) |> "
        )
    )

    account["email"] = email_address

    if not each_account:
        org_account = account
    elif each_account == 1:
        student_account = account
    else:
        institution_account = account


async def main() -> None:
    """
    ! A method that tests all user-based transactions declared under `TransactionActions`.
    @o That file was located under `/node/core/constants.py`.
    """

    # # Initialize TOTP to instant fetch.
    load_dotenv("node-env.vars")  # ! Adjust this as possible.
    otp_interval: int = 15

    AUTH_KEY: str | None = env.get("AUTH_KEY", None)
    SECRET_KEY: str | None = env.get("SECRET_KEY", None)

    totp_instance: PasscodeTOTP
    if AUTH_KEY is not None and SECRET_KEY is not None:
        totp_instance = PasscodeTOTP(
            base_code=[AUTH_KEY, SECRET_KEY], interval=otp_interval, issuer="local"
        )
    else:
        print("`AUTH_KEY` or `SECRET_KEY` is missing.")
        exit(-1)

    # # Initialize HTTP instance.
    http = get_http_client_instance()
    await http.initialize()

    # !!! Ensure that we hit the `reload-master-chain` if we want to test this as a starting point.

    # - [1] Register as a 'DASHBOARD_USER' first.
    path_to_master: str = f"{target_node}:{target_port}"

    # - Pre-req for the Registration, fetch an auth code from the master.

    fetched_auth_code = await http.enqueue_request(
        url=URLAddress(f"{path_to_master}/admin/generate_auth"),
        method=HTTPQueueMethods.POST,
        data={
            "email": institution_account["email"],
            "role": "Institution Dashboard User",
        },
        headers={"x-passcode": totp_instance.get_code()},
        await_result_immediate=True,
        retry_attempts=99,
    )

    if fetched_auth_code.ok:
        print(
            f"Got auth code: {fetched_auth_code} for {institution_account['email']} | {institution_account['type']}"
        )

        # - Check email and input the `auth_code`.
        auth_code_from_email_institution: str = input(
            f"Require `auth_code`, please check email of {institution_account['email']} and input its value. |> "
        )

        # - Register the institution first.
        register_institution_acc = await http.enqueue_request(
            url=URLAddress(f"{path_to_master}/entity/register"),
            method=HTTPQueueMethods.POST,
            data={
                "username": institution_account["username"],
                "password": institution_account["password"],
                "email": institution_account["email"],
                "first_name": institution_account["first_name"],
                "last_name": institution_account["last_name"],
                "auth_code": auth_code_from_email_institution,
            },
            await_result_immediate=True,
            retry_attempts=99,
        )

        if register_institution_acc.ok:
            print(
                f"Registration of {institution_account['email']} ({institution_account['type']}) went okay!"
            )

            # - Login institution user.

            login_institution = await http.enqueue_request(
                url=URLAddress(f"{path_to_master}/entity/login"),
                method=HTTPQueueMethods.POST,
                data={
                    "username": institution_account["username"],
                    "password": institution_account["password"],
                },
                await_result_immediate=True,
                retry_attempts=99,
            )

            if login_institution.ok:
                print(
                    f"Institution sign in as {institution_account['username']} or {institution_account['email']}! Ready to insert some student."
                )

            # ! Create 2 applicants/students here.

            # ! Insert documents from these applicants. (Activities and stuff)

            # ! Add extra information from these applicants.

            # ! Create a new organization as a company or organization.

            # ! Add extra info from this organization.

            # ! Do attempt apply from these applicants/students.

            # ! Reject the first one and accept the new one. (On accept create an extra log from that applicant).
            # - This may need show registered. Then we may need revoke.

            # ! Wait to validate events via Explorer API.
            input()

            # ! Attempt to decode these.


asyncio_run(main())
