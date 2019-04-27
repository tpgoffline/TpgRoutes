# tpgroutes.py
# Created by Rémy Da Costa Faro
# Formatted with Blake
#
# Informatique et Sciences du Numérique - Baccalauréat 2019
# Peut-être executé avec Python 3.6 ou une version supérieure

import sqlite3
import logging
from logging.handlers import RotatingFileHandler
import sys
from array import array

MAX_STATIONS = 10_000_000
MAX_INT = 2 ** 32 - 1


class EarliestArrival:
    time: int
    trip_id: str
    connection: int

    def __init__(self, time, trip_id, connection):
        self.time = time
        self.trip_id = trip_id
        self.connection = connection


class ConnectionRow:
    id: int
    departure_stop: int
    arrival_stop: int
    departure_time: int
    arrival_time: int
    line: str
    trip_id: int
    destination_stop: int

    def __init__(self, c):
        self.id = c[0]
        self.departure_stop = c[1]
        self.arrival_stop = c[2]
        self.departure_time = c[3]
        self.arrival_time = c[4]
        self.line = c[5]
        self.trip_id = c[6]
        self.destination_stop = c[7]


class TpgRoutes:
    def __init__(self, logger=None):
        super(TpgRoutes, self).__init__()
        if logger == None:
            self.configure_logs()
        else:
            self.logger = logger
            # Si un logger existe déjà,
            # par exemple en cas d'utilisation de l'algorithme en tant que module,
            # on évite d'initialiser un nouveau logger, et on utilise celui existant

    def runTest(self):
        self.load_database("tpgoffline-data/timetables.sqlite")
        self.logger.info(
            "(row_id, departure_stop, arrival_stop, departure_time, arrival_time, line, trip_id, direction)"
        )  # Cette ligne affiche un en-tête pour mieux comprendre la sortie de l'itinéraire
        for x in self.compute_route(8_587_057, 8_595_324, 31800, 1):
            self.logger.info(x)

    def configure_logs(self):
        """
        Avoir les sorties du programme est crucial, et la fonction print est quasiment inutilisable si le programme est exécuté par un démon.
        C'est pourquoi nous initialisons ici la librairie logging, qui fait partie de la bibliothèque de librairie standard à Python.
        """

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter("%(asctime)s :: %(levelname)s :: %(message)s")
        file_handler = RotatingFileHandler("activity.log", "a", 1_000_000, 1)

        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(stream_handler)

    def load_database(self, path):
        """
        Initialiser les données d'itinéraires avec une base SQLite

        :param path: Chemin vers la base de données SQLite
        """
        self.logger.info("Loading database...")
        try:
            self.database = sqlite3.connect(path)
            self.logger.info("Database loaded")
        except:
            self.logger.exception("Loading database failed")

    def compute_route(
        self, departure_station: int, arrival_stop: int, departure_time: int, day: int
    ):
        """
        Calcul un itinéraire depuis un arrêt A vers un arrêt B avec le temps de trajet le plus court possible, et au plus proche de l'heure de départ

        :param departure_station: Identifiant de l'arrêt de départ dans la base de données, habituellement l'identifiant CFF
        :param arrival_stop: Identifiant de l'arrêt d'arrivée dans la base de données, habituellement l'identifiant CFF
        :param departure_time: Heure minimum de départ, en secondes depuis minuit
        :param day: Jour de la semaine, peut-être un entier en 0 et 6, de dimanche à samedi
        """

        try:
            self.cursor = self.database.cursor()
        except:
            self.logger.exception(
                "Access to database failed. Please, check you had loaded the database with load_database."
            )
            return

        assert departure_time > 0, "departure_time is less than 0 seconds"
        assert (
            departure_time < 86400
        ), "departure_time is greater than 86400 seconds, also known as the number of seconds in a day"

        if day == 0:
            dayString = "sunday"
        elif day == 6:
            dayString = "saturday"
        elif day == 5:
            dayString = (
                "friday"
            )  # Les horaires de vendredi sont différents de ceux des jours entre lundi et vendredi, en raison de la présence des horaires des lignes Noctambus.
        elif day > 0 and day < 5:
            dayString = "monday"
        else:
            self.logger.exception(
                "Day is incorrect, it should be an integer between 0 and 6 included"
            )
            return

        in_connection = array("I", [MAX_INT for _ in range(MAX_STATIONS)])
        earliest_arrival = [
            EarliestArrival(MAX_INT, "", 0) for _ in range(MAX_STATIONS)
        ]

        earliest_arrival[departure_station].time = departure_time

        # Juste au cas où, nous vérifions que les arrêts de départs et les arrêts d'arrivée sont dans l'écart des identifiants autorisés
        if departure_station <= MAX_STATIONS and arrival_stop <= MAX_STATIONS:
            earliest = MAX_INT

            # Nous prenons ici dans la base de données tous les départs étant postérieur à l'heure minimum de départ, ordonné par l'heure de départ
            self.cursor.execute(
                f"SELECT * FROM {dayString} WHERE departure_time >= {departure_time} and departure_time < arrival_time ORDER BY departure_time"
            )
            for c in self.cursor.fetchall():
                connection = ConnectionRow(
                    c
                )  # Initialiser avec une classe permet de rendre le code plus lisible, et de rendre le débogage plus simple
                minimum_connection_time = 120  # en secondes
                if not earliest_arrival[connection.departure_stop].trip_id:
                    # Si nous sommes à l'arrêt de départ, alors il n'y a pas besoin d'un délai de connexion
                    minimum_connection_time = 0
                elif c[6] == earliest_arrival[c[1]].trip_id:
                    # Si nous continuons notre trajet avec le même véhicule, alors il n'y a pas besoin d'un délai de connexion
                    minimum_connection_time = 0

                # Pour de futures améliorations, nous calculons le nombres de lignes différentes
                differents_lines = 0
                if (
                    connection.trip_id
                    != earliest_arrival[connection.departure_stop].trip_id
                ):
                    differents_lines = 1

                if (
                    connection.departure_time
                    > (
                        earliest_arrival[connection.departure_stop].time
                        + minimum_connection_time
                    )
                    and connection.arrival_time
                    < earliest_arrival[connection.arrival_stop].time
                ):
                    # Si cette connexion est un meilleur choix que celui utilisé précédamment, alors nous allons enregistrer celui-ci
                    earliest_arrival[
                        connection.arrival_stop
                    ].time = connection.arrival_time
                    earliest_arrival[connection.arrival_stop].connection = (
                        earliest_arrival[connection.departure_stop].connection
                        + differents_lines
                    )
                    earliest_arrival[
                        connection.arrival_stop
                    ].trip_id = connection.trip_id
                    in_connection[connection.arrival_stop] = connection.id

                    if connection.arrival_stop == arrival_stop:
                        # Nous sommes à l'arrêt d'arrivée, il faut enregistrer le parcours le plus court
                        earliest = min(earliest, connection.arrival_time)
                elif connection.departure_time > earliest:
                    # Parce que les départs sont déjà ordonnés par heure de départ,
                    # si le présent départ à une heure de départ postérieur à l'heure d'arrivée minimum,
                    # nous pouvons arrêter la boucle, nous avons trouvé le meilleur itinéraire
                    continue

            # Maintenant que l'itinéraire est calculé dans deux tableaux, nous pouvons donc le reconstruire

            if in_connection[arrival_stop] == MAX_INT:
                # Si l'arrêt d'arrivée n'a pas de connexion, alors aucun itinéraire n'a été trouvé
                # Cela peut arriver parfois, notamment lorsque l'heure de départ est proche de l'heure de fin de service
                self.logger.info("No solution was found")
            else:
                route = []

                # Nous devons reconstruire l'itinéraire depuis l'arrêt d'arrivée
                last_connection_index = in_connection[arrival_stop]

                while last_connection_index != MAX_INT:
                    self.cursor.execute(
                        f"SELECT * FROM {dayString} WHERE id = {last_connection_index}"
                    )
                    connection = self.cursor.fetchall()[0]
                    route.append(connection)
                    last_connection_index = in_connection[connection[1]]

                # Et nous pouvons retourner le résultat dans le bon ordre
                return reversed(route)
        else:
            return []


if __name__ == "__main__":
    # Si le fichier est appelé directement, nous pouvons lancer un test de fonctionnement de l'algorithme.
    tpgRoutes = TpgRoutes()
    tpgRoutes.runTest()
