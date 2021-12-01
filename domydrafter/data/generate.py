"""
This script coordinates the generating functions to generate and dump game data.
"""
from .unit import generate_units
from .nation import generate_nations
from .site import generate_sites
from .nation_sites import nation_sites

from typing import Dict, Any

def generate():
    units = generate_units()
    nations = generate_nations()
    sites = generate_sites()
    nations, sites = nation_sites(nations, sites)