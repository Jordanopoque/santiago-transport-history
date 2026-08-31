import csv
from pathlib import Path

from django.core.management.base import BaseCommand
from transit.models import Agency, Route, Stop


class Command(BaseCommand):
    help = "Importa datos GTFS a la base de datos"

    def handle(self, *args, **options):

        gtfs_path = Path("/project/gtfs/GTFS_20260829")

        # =========================
        # AGENCIES
        # =========================

        agency_file = gtfs_path / "agency.txt"

        self.stdout.write("Importando agencies...")

        with open(agency_file, "r", encoding="utf-8-sig") as file:

            reader = csv.DictReader(file)

            for row in reader:

                Agency.objects.update_or_create(
                    agency_id=row["agency_id"],
                    defaults={
                        "agency_name": row["agency_name"],
                        "agency_url": row.get("agency_url") or None,
                        "agency_timezone": row["agency_timezone"],
                    },
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Agencies importadas correctamente."
            )
        )

        # =========================
        # ROUTES
        # =========================

        route_file = gtfs_path / "routes.txt"

        self.stdout.write("Importando routes...")

        with open(route_file, "r", encoding="utf-8-sig") as file:

            reader = csv.DictReader(file)

            for row in reader:

                agency = Agency.objects.get(
                    agency_id=row["agency_id"]
                )

                Route.objects.update_or_create(
                    route_id=row["route_id"],
                    defaults={
                        "agency": agency,
                        "route_short_name": row["route_short_name"],
                        "route_long_name": row["route_long_name"],
                        "route_desc": row.get("route_desc") or None,
                        "route_type": int(row["route_type"]),
                        "route_url": row.get("route_url") or None,
                        "route_color": row.get("route_color") or None,
                        "route_text_color": row.get("route_text_color") or None,
                    },
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Routes importadas correctamente."
            )
        )

        # =========================
        # STOPS
        # =========================

        stop_file = gtfs_path / "stops.txt"

        self.stdout.write("Importando stops...")

        stops = []
        skipped_stops = 0

        with open(stop_file, "r", encoding="utf-8-sig") as file:

            reader = csv.DictReader(file)

            for row in reader:

                stop_lat = row.get("stop_lat", "").strip()
                stop_lon = row.get("stop_lon", "").strip()

                # Ignorar registros sin coordenadas
                if not stop_lat or not stop_lon:

                    skipped_stops += 1

                    self.stdout.write(
                        self.style.WARNING(
                            f"Stop omitida por coordenadas vacías: "
                            f"{row.get('stop_id')}"
                        )
                    )

                    continue

                stops.append(
                    Stop(
                        stop_id=row["stop_id"],
                        stop_code=row.get("stop_code") or None,
                        stop_name=row["stop_name"],
                        stop_lat=stop_lat,
                        stop_lon=stop_lon,
                        stop_url=row.get("stop_url") or None,

                        wheelchair_boarding=(
                            int(row["wheelchair_boarding"])
                            if row.get("wheelchair_boarding")
                            else None
                        ),

                        location_type=(
                            int(row["location_type"])
                            if row.get("location_type")
                            else None
                        ),

                        parent_station=(
                            row.get("parent_station") or None
                        ),

                        level_id=(
                            row.get("level_id") or None
                        ),
                    )
                )

        Stop.objects.bulk_create(
            stops,
            batch_size=1000,
            ignore_conflicts=True
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"{len(stops)} stops procesadas correctamente."
            )
        )

        if skipped_stops:

            self.stdout.write(
                self.style.WARNING(
                    f"{skipped_stops} stops fueron omitidas "
                    f"por falta de coordenadas."
                )
            )

        # =========================
        # FIN
        # =========================

        self.stdout.write(
            self.style.SUCCESS(
                "Importación completada."
            )
        )