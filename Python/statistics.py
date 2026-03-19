class StatisticsCollector:
    def __init__(self):
        self.completed_trips = 0
        self.total_wait_time = 0.0
        self.total_travel_time = 0.0
        self.total_system_time = 0.0

    def record_completed_trip(self, person: dict) -> None:
        request_time = person.get("request_time")
        board_time = person.get("board_time")
        exit_time = person.get("exit_time")

        if request_time is None or board_time is None or exit_time is None:
            return

        wait_time = board_time - request_time
        travel_time = exit_time - board_time
        system_time = exit_time - request_time

        self.completed_trips += 1
        self.total_wait_time += wait_time
        self.total_travel_time += travel_time
        self.total_system_time += system_time

    def get_average_wait_time(self) -> float:
        if self.completed_trips == 0:
            return 0.0
        return self.total_wait_time / self.completed_trips

    def get_average_travel_time(self) -> float:
        if self.completed_trips == 0:
            return 0.0
        return self.total_travel_time / self.completed_trips

    def get_average_system_time(self) -> float:
        if self.completed_trips == 0:
            return 0.0
        return self.total_system_time / self.completed_trips