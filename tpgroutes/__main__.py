from . import TpgRoutes

# Si le fichier est appelé directement, nous pouvons lancer un test de fonctionnement de l'algorithme.
tpgRoutes = TpgRoutes()
departure_time = 43200
for x in range(1):
    tpgRoutes.logger.info(
        "row_id / departure_stop / arrival_stop / departure_time / arrival_time / line / trip_id / direction)"
    )  # Cette ligne affiche un en-tête pour mieux comprendre la sortie de l'itinéraire
    route = tpgRoutes.compute_route(8_587_907, 8_595_327, departure_time, 1)
    for x in route:
        tpgRoutes.logger.info(x)
    departure_time = route[0].departure_time + 1

