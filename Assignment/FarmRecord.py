import math


def validateFarmID(farm_id):
    """Check the source ID format without trimming or changing the ID."""
    if (not isinstance(farm_id, str) or not farm_id
            or not farm_id.isascii() or not farm_id.isalnum()):
        raise ValueError("FarmID must contain ASCII letters/digits only")
    return farm_id


class FarmRecord:
    def __init__(self, farm_id, name, species, latitude, longitude,
                 street_num, street, suburb, state, postcode, country,
                 map_url="", profile_url="", status=""):
        self.farm_id = validateFarmID(farm_id)
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Farm name must not be empty")
        self.name = name.strip()
        try:
            if isinstance(latitude, bool) or isinstance(longitude, bool):
                raise ValueError("Coordinates must be numerical")
            self.latitude = float(latitude)
            self.longitude = float(longitude)
        except (ValueError, TypeError, OverflowError) as error:
            raise ValueError("Coordinates must be numerical") from error
        if not math.isfinite(self.latitude) or not -90 <= self.latitude <= 90:
            raise ValueError("Latitude must be finite and between -90 and 90")
        if not math.isfinite(self.longitude) or not -180 <= self.longitude <= 180:
            raise ValueError("Longitude must be finite and between -180 and 180")
        # Empty source address/species fields remain empty; never invent values.
        self.species = species
        self.street_num = street_num
        self.street = street
        self.suburb = suburb
        self.state = state
        self.postcode = postcode
        self.country = country
        self.map_url = map_url
        self.profile_url = profile_url
        self.status = status

    def __str__(self):
        return (f"FarmID={self.farm_id}, Name={self.name}, Species={self.species}, "
                f"Lat={self.latitude}, Lng={self.longitude}, "
                f"Street Num={self.street_num}, Street={self.street}, "
                f"Suburb={self.suburb}, State={self.state}, "
                f"Postcode={self.postcode}, Country={self.country}, "
                f"Status={self.status}, Map={self.map_url}, Profile={self.profile_url}")
