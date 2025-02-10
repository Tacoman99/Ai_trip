from google.maps import routeoptimization_v1 as ro
from datetime import datetime

client = ro.RouteOptimizationClient(credentials="credentials")
request = ro.OptimizeToursRequest(
    parent="projects/project",
    model={
      "shipments": [
         {
          "pickups": [
            {
              "arrival_location": {
                "latitude": 37.738818,
                "longitude": -122.4161
              }
            }
          ],
          "deliveries": [
            {
              "arrival_location": {
                "latitude": 37.79581,
                "longitude": -122.4218856
              }
            }
          ]
        }
      ],
      "vehicles": [
        {
          "start_location": {
            "latitude": 37.738818,
            "longitude": -122.4161
          },
          "end_location": {
            "latitude": 37.738818,
            "longitude": -122.4161
          },
          "cost_per_kilometer": 1.0
        }
      ],
      "global_start_time": datetime.fromisoformat("2024-02-13T00:00:00.000Z"),
      "global_end_time": datetime.fromisoformat("2024-02-14T06:00:00.000Z")
    }
)
response = client.optimize_tours(request=request)
print(response)