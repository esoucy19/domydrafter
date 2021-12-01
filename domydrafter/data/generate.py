"""
This script coordinates the generating functions to generate and dump game data.
"""
import unit
import nation
import site

from typing import Dict, Any

if __name__ == "__main__":
    units: Dict[str, ] = unit.generate_units()
    sites = site.generate_sites()
    nations = nation.generate_nations()