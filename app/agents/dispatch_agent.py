from app.models.schemas import CargoIntakeSchema
from app.services.fleet_db import search_available_fleet, book_dispatch_window


class DispatchAgent:
    """
    Executes automated route evaluations and schedules carriers based
    on validated structural data definitions.
    """

    async def process_assignment_loop(self, validated_cargo: CargoIntakeSchema) -> dict:
        # Step 2 Tool Execution Call: Query Fleet Registry
        fleet_match = search_available_fleet(validated_cargo.weight_lbs)

        if fleet_match["status"] == "Failure":
            return {
                "assigned": False,
                "reason": fleet_match["reason"],
                "manifest_id": None
            }

        driver_details = fleet_match["driver"]

        # Step 2 Tool Execution Call: Dispatch & Book Scheduling Engine
        manifest_id = book_dispatch_window(
            driver_id=driver_details["driver_id"],
            destination=validated_cargo.destination_city,
            target_date=validated_cargo.pickup_date
        )

        return {
            "assigned": True,
            "manifest_id": manifest_id,
            "driver_name": driver_details["name"],
            "driver_id": driver_details["driver_id"],
            "route": f"{validated_cargo.origin_city} -> {validated_cargo.destination_city}"
        }