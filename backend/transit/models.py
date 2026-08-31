from django.db import models


class Agency(models.Model):
    agency_id = models.CharField(max_length=50, primary_key=True)
    agency_name = models.CharField(max_length=255)
    agency_url = models.URLField(blank=True, null=True)
    agency_timezone = models.CharField(max_length=100)

    def __str__(self):
        return self.agency_name


class Route(models.Model):
    route_id = models.CharField(max_length=50, primary_key=True)
    agency = models.ForeignKey(
        Agency,
        on_delete=models.PROTECT,
        related_name="routes"
    )
    route_short_name = models.CharField(max_length=50)
    route_long_name = models.CharField(max_length=255)
    route_desc = models.TextField(blank=True, null=True)
    route_type = models.IntegerField()
    route_url = models.URLField(blank=True, null=True)
    route_color = models.CharField(max_length=6, blank=True, null=True)
    route_text_color = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return f"{self.route_short_name} - {self.route_long_name}"


class Stop(models.Model):
    stop_id = models.CharField(max_length=50, primary_key=True)
    stop_code = models.CharField(max_length=50, blank=True, null=True)
    stop_name = models.CharField(max_length=255)
    stop_lat = models.DecimalField(max_digits=10, decimal_places=7)
    stop_lon = models.DecimalField(max_digits=10, decimal_places=7)
    stop_url = models.URLField(blank=True, null=True)
    wheelchair_boarding = models.IntegerField(blank=True, null=True)
    location_type = models.IntegerField(blank=True, null=True)
    parent_station = models.CharField(max_length=50, blank=True, null=True)
    level_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.stop_name


class Trip(models.Model):
    trip_id = models.CharField(max_length=100, primary_key=True)
    route = models.ForeignKey(
        Route,
        on_delete=models.PROTECT,
        related_name="trips"
    )
    service_id = models.CharField(max_length=50)
    trip_headsign = models.CharField(max_length=255, blank=True, null=True)
    direction_id = models.IntegerField(blank=True, null=True)
    shape_id = models.CharField(max_length=100, blank=True, null=True)
    trip_short_name = models.CharField(max_length=100, blank=True, null=True)
    wheelchair_accessible = models.IntegerField(blank=True, null=True)
    bikes_allowed = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.trip_id


class StopTime(models.Model):
    trip = models.ForeignKey(
        Trip,
        on_delete=models.CASCADE,
        related_name="stop_times"
    )
    stop = models.ForeignKey(
        Stop,
        on_delete=models.PROTECT,
        related_name="stop_times"
    )
    arrival_time = models.TimeField()
    departure_time = models.TimeField()
    stop_sequence = models.IntegerField()
    pickup_type = models.IntegerField(blank=True, null=True)
    drop_off_type = models.IntegerField(blank=True, null=True)
    timepoint = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ["trip", "stop_sequence"]
        constraints = [
            models.UniqueConstraint(
                fields=["trip", "stop_sequence"],
                name="unique_trip_stop_sequence"
            )
        ]

    def __str__(self):
        return f"{self.trip_id} - {self.stop_sequence}"