import random
import string

from .console import Render
from .config import C

console = Render()


def get_random_str(length: int = 15) -> str:
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def console_wrapper(func):
    """Clears screen + renders ASCII art before calling the function."""
    def inner(*args, **kwargs):
        console.clear()
        console.render_ascii()
        return func(*args, **kwargs)
    return inner


class MemberListUtils:
    @staticmethod
    def range_corrector(ranges):
        if [0, 99] not in ranges:
            ranges.insert(0, [0, 99])
        return ranges

    @staticmethod
    def get_ranges(index: int, multiplier: int, member_count: int):
        start = index * multiplier
        ranges = [[start, start + 99]]
        if member_count > start + 99:
            ranges.append([start + 100, start + 199])
        return MemberListUtils.range_corrector(ranges)

    @staticmethod
    def parse_member_list_update(payload):
        data = payload["d"]
        result = {
            "online_count": data["online_count"],
            "member_count": data["member_count"],
            "id": data["id"],
            "guild_id": data["guild_id"],
            "hoisted_roles": data["groups"],
            "types": [op["op"] for op in data["ops"]],
            "locations": [],
            "updates": [],
        }

        for op in data["ops"]:
            optype = op["op"]
            if optype in ("SYNC", "INVALIDATE"):
                result["locations"].append(op["range"])
                result["updates"].append(op["items"] if optype == "SYNC" else [])
            elif optype in ("INSERT", "UPDATE", "DELETE"):
                result["locations"].append(op["index"])
                result["updates"].append(op["item"] if optype != "DELETE" else [])

        return result