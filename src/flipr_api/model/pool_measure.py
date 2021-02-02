# -*- coding: utf-8 -*-
"""Pool measure Python model for the Flipr REST API."""
from datetime import datetime
from typing import Any
from typing import Dict

from dateutil.parser import parse


class PoolMeasure:
    """Class to access the results of a pool measure request.

    Attributes:
        temperature: A float representing the temperature of the pool.
        ph: A float representing the ph of the pool.
        chlore: A float representing the chlore of the pool.
        red_ox: A float representing the oxydo reduction level of the pool.
        date_measure: The date time when the measure was taken.
    """

    temperature: float
    ph: float
    chlore: float
    date_measure: datetime

    def __init__(self, raw_data: Dict[str, Any]) -> None:
        """Initialize a PoolMeasure object.

        Args:
            raw_data: A dictionary representing the JSON response
                from 'get_pool_measure_latest' REST.
        """
        self.raw_data = raw_data

        self.temperature = float(self.raw_data["Temperature"])
        self.ph = float(self.raw_data["PH"]["Value"])
        self.chlore = float(self.raw_data["Desinfectant"]["Value"])
        self.red_ox = float(self.raw_data["OxydoReductionPotentiel"]["Value"])
        self.date_mesure = parse(self.raw_data["DateTime"])
