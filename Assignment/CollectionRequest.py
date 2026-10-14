import math
from FarmRecord import validateFarmID


class CollectionRequest:
    def __init__(self, request_id, farm_id, feedstock):
        if (not isinstance(request_id, str) or not request_id.strip()
                or request_id != request_id.strip()):
            raise ValueError("Request ID must be non-empty without outer whitespace")
        self.request_id = request_id
        self.farm_id = validateFarmID(farm_id)
        try:
            if isinstance(feedstock, bool):
                raise ValueError("Invalid feedstock")
            self.feedstock = float(feedstock)
        except (TypeError, ValueError, OverflowError) as error:
            raise ValueError("Feedstock must be numerical") from error
        if not math.isfinite(self.feedstock) or self.feedstock <= 0:
            raise ValueError("Feedstock must be positive and finite")
        self.transport_time = None
        self.priority = None
        self.path = None
        self.status = "MODELLED"

    def __str__(self):
        return (f"{self.request_id} FarmID={self.farm_id} "
                f"F={self.feedstock:.2f} model tonnes "
                f"T={self.transport_time:.2f} min P={self.priority:.6f}")
