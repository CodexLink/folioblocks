"""
Events (events.py) | Functions to Execute during FastAPI Events.
[1] FastAPI has an event handler which allows us to run code before the actual instantiation of the FastAPI in the uvicorn instance. [2] Other than that, an extension module for the FastAPI named as 'fastapi-utils' provide us an event function that can run on the loop at a certain time. The decorator named '@repeat_every' will be utilized to run some blockchain-based actions along with the API endpoints.
This file contains functions that is under event category. This means they run exclusively at a certain time or at a certain phase.

This file is part of FolioBlocks.

FolioBlocks is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
FolioBlocks is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with FolioBlocks. If not, see <https://www.gnu.org/licenses/>.
"""

if __name__ == "__main__":
    raise SystemExit(
        f"This {__file__} (module) should not be executed as an entrypoint code! It only contains event functions that is exclusively used in the entrypoint code (main.py)!"
    )

from fastapi_utils.tasks import repeat_every

# from fastapi import Body, Depends, FastAPI, Query, Router


"""
Preparation

Before everything starts. Any instance of this API will search for a set of ports on a corresponding IP address or vice-versa.

Evaluation:
1. Are there any other available nodes?
- If not, set its own instance to be the master node. Otherwise, be a master node.
"""


@node.on_event("startup")
async def system_checks():
    # Should contain the node lookup.
    # Should check for the credentials.
    # Should check for the database. Create if it doesn't exists.
    # Ensure permissions of the file. Also note, that on shutdown it should be protected.

    # ! NOTE: The idea for the available nodes is dangerous. But this is just the setbacks. Just use SSL for HTTPS.

    # Should check for the file of the JSON if still the same as before via database. Or should hash or rehash the file. Also set the permission to undeletable, IF POSSIBLE.
    pass


"""
Shutdown

Before we kill the cameras, we need to ensure that everything is saved and the files for blockchain is saved.

TODO
Shutdown SQL Session
Remove or finish any request or finish the consensus.
Put all other JWT on expiration or on blacklist.

What else?
"""


@node.on_event("shutdown")
async def perform_shutdown():  # TODO: Should we seperate this along with other shutdown thing since this was asnyc?
    pass


"""
Repeated Tasks

These are the tasks that needs to be executed at certain amount of time to evaluate the blockchain consensus mechanism. Sooner or later, we have to do something on this one.

TODO
JWT Invalidation (Invalidate them if they did something or that node is inactive. This act will start when the JWT token is way past the deadline.)
Consensus Method (Remember, that we need the consensus dependency.)

"""


@repeat_every(seconds=60)
async def jwt_invalidation():
    pass


@repeat_every(seconds=10)  # unconfirmed.
async def consensus_with_side_nodes():
    pass
