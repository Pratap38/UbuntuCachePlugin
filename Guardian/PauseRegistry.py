import json
import os
import tempfile
from datetime import datetime
import psutil
from Guardian.models.PausedProcess import PauseProcess


class PauseRegistry:

    def __init__(self, stateFile: str = "guardian_state.json"):

        self.processes: dict[int, PauseProcess] = {}
        self.stateFile = stateFile

        self._load()

    def add(self, process: PauseProcess) -> bool:

        if process is None:
            return False

        if process.pid <= 0:
            return False

        if process.pid in self.processes:
            return False

        self.processes[process.pid] = process

        if not self._save():
            del self.processes[process.pid]
            return False

        return True

    def remove(self, pid: int) -> bool:

        if pid not in self.processes:
            return False

        process = self.processes[pid]

        del self.processes[pid]

        if not self._save():
            self.processes[pid] = process
            return False

        return True

    def contains(self, pid: int) -> bool:
        return pid in self.processes

    def get(self, pid: int) -> PauseProcess | None:
        return self.processes.get(pid)

    def getAll(self) -> list[PauseProcess]:
        return list(self.processes.values())

    def count(self) -> int:
        return len(self.processes)

    def clear(self) -> None:

        if not self.processes:
            return

        oldProcesses = self.processes.copy()

        self.processes.clear()

        if not self._save():
            self.processes = oldProcesses
            raise RuntimeError(
                "Failed to persist cleared PauseRegistry."
            )

    def _serialize(self) -> dict:

        return {
            "version": 1,
            "processes": [
                {
                    "pid": process.pid,
                    "name": process.name,
                    "pausedAt": process.pausedAt.isoformat(),
                    "reason": process.reason,
                    "processStartTime": process.processStartTime,
                }
                for process in self.processes.values()
            ],
        }

    def _save(self) -> bool:

        directory = os.path.dirname(
            os.path.abspath(self.stateFile)
        )

        try:

            os.makedirs(
                directory,
                exist_ok=True
            )

            data = self._serialize()

            fd, tempPath = tempfile.mkstemp(
                prefix=".guardian_state_",
                suffix=".tmp",
                dir=directory,
                text=True
            )

            try:

                with os.fdopen(
                    fd,
                    "w",
                    encoding="utf-8"
                ) as file:

                    json.dump(
                        data,
                        file,
                        indent=2
                    )

                    file.write("\n")

                    file.flush()

                    os.fsync(
                        file.fileno()
                    )

                os.replace(
                    tempPath,
                    self.stateFile
                )

                return True

            finally:

                if os.path.exists(tempPath):

                    try:
                        os.remove(tempPath)
                    except OSError:
                        pass

        except (
            OSError,
            TypeError,
            ValueError
        ):

            return False

    def _load(self) -> None:

        if not os.path.exists(self.stateFile):
            return

        try:

            with open(
                self.stateFile,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            if not isinstance(data, dict):
                return

            if data.get("version") != 1:
                return

            processes = data.get(
                "processes",
                []
            )

            if not isinstance(
                processes,
                list
            ):
                return

            loaded = {}

            for item in processes:

                if not isinstance(
                    item,
                    dict
                ):
                    continue

                pid = item.get("pid")
                name = item.get("name")
                pausedAt = item.get("pausedAt")
                reason = item.get("reason")
                processStartTime = item.get(
                    "processStartTime"
                )

                if not isinstance(
                    pid,
                    int
                ) or pid <= 0:
                    continue

                if not isinstance(
                    name,
                    str
                ) or not name:
                    continue

                if not isinstance(
                    pausedAt,
                    str
                ):
                    continue

                if not isinstance(
                    reason,
                    str
                ):
                    continue

                if not isinstance(
                    processStartTime,
                    (int, float)
                ):
                    continue

                try:

                    pausedAtValue = (
                        datetime.fromisoformat(
                            pausedAt
                        )
                    )

                except ValueError:

                    continue

                if pid in loaded:
                    continue

                loaded[pid] = PauseProcess(
                    pid=pid,
                    name=name,
                    pausedAt=pausedAtValue,
                    reason=reason,
                    processStartTime=float(
                        processStartTime
                    )
                )

            self.processes = loaded

        except (
            OSError,
            json.JSONDecodeError,
            TypeError,
            ValueError
        ):

            self.processes = {}
    def isSameProcess(self, pid: int) -> bool:

        process = self.processes.get(pid)

        if process is None:
            return False

        try:

            current = psutil.Process(pid)

            currentStartTime = current.create_time()

            return (
                abs(
                    currentStartTime
                    - process.processStartTime
                )
                < 0.001
            )

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):

            return False