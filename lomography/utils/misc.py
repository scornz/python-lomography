from __future__ import annotations

import asyncio

# Typing
from typing import TYPE_CHECKING, TypeVar, Coroutine

if TYPE_CHECKING:
    from lomography.base import Lomography


# Define a type variable that can be any type.
T = TypeVar("T")


def run_async(lomo: Lomography, coroutine: Coroutine[None, None, T]) -> T:
    """Run the coroutine in loop and return the result synchronously."""
    if not lomo.loop.is_running():
        # If the loop is not running, it's safe to run the coroutine to completion.
        return lomo.loop.run_until_complete(coroutine)
    else:
        # If the loop is already running, it's improper to use run_until_complete.
        # Instead, create a new task in the existing loop and wait for it.
        # This branch is typically not expected in synchronous functions but is provided for safety.
        future = asyncio.run_coroutine_threadsafe(coroutine, lomo.loop)
        return future.result()
