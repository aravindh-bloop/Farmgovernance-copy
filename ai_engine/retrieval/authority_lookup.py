"""
Resolves a scheme's officer "designation" (e.g. "AAO") plus the user's query text
into a specific officer contact from officer_directory.json.

Flow:
  1. Scan the query for any district/block name mentioned.
  2. If none found -> return a "need_location" result (can't pick one person out of many).
  3. If found -> filter officer_directory.json by designation + district (+ block if given).
  4. Return the matched officer's contact, or "not_found_in_directory" if that
     specific combination isn't in the data yet.
"""
import os
import json
from typing import Optional, Dict, Any, List
from config.settings import settings


class AuthorityLookup:
    def __init__(self):
        self.officers: List[Dict[str, Any]] = []
        self._districts = set()
        self._blocks = set()
        self._load()

    def _load(self):
        path = settings.OFFICER_DIRECTORY_PATH
        if not os.path.exists(path):
            print(f"[!] Officer directory not found at {path}")
            return
        with open(path, "r", encoding="utf-8") as f:
            self.officers = json.load(f)
        for o in self.officers:
            if o.get("district"):
                self._districts.add(o["district"])
            if o.get("block_name"):
                self._blocks.add(o["block_name"])

    def _find_location_in_query(self, query: str):
        q = query.lower()
        district = next((d for d in self._districts if d.lower() in q), None)
        block = next((b for b in self._blocks if b.lower() in q), None)
        return district, block

    def lookup(self, designation: Optional[str], query: str) -> Optional[Dict[str, Any]]:
        if not designation or not self.officers:
            return None

        district, block = self._find_location_in_query(query)

        if not district:
            covered = ", ".join(sorted(self._districts)) if self._districts else "none yet"
            return {
                "designation": designation,
                "status": "need_location",
                "note": (
                    f"Please share your district (and block, if known) so I can give you the exact contact. "
                    f"Our officer directory currently covers: {covered}. If your district isn't in this list, "
                    f"I won't have a specific contact yet — please check with your nearest cooperative office directly."
                ),
            }

        candidates = [
            o for o in self.officers
            if o.get("designation") == designation and o.get("district") == district
        ]

        if block:
            block_matches = [o for o in candidates if o.get("block_name") == block]
            if block_matches:
                candidates = block_matches

        if not candidates:
            location = f"{district} / {block}" if block else district
            return {
                "designation": designation,
                "status": "not_found_in_directory",
                "note": f"No {designation} record found for {location} in our directory yet.",
            }

        officer = candidates[0]
        return {
            "designation": designation,
            "status": "found",
            "name": officer.get("name"),
            "district": officer.get("district"),
            "block_name": officer.get("block_name"),
            "mobile": officer.get("mobile"),
            "landline": officer.get("landline"),
            "email": officer.get("email"),
        }
