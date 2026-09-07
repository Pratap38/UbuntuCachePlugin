from Guardian.GuardianEngine import GuardianEngine


class FakeConfig:

    def __init__(self, enabled=True, autoPause=True):
        self.values = {
            "enabled": enabled,
            "autoPause": autoPause,
        }

    def get(self, key, default=None):
        return self.values.get(key, default)


class FakeMemory:

    ramPercent = 95


class FakePressureCheck:

    def analyze(self, memory):
        return "CRITICAL"


class FakeDecisionEngine:

    def decide(self, pressure):
        return True


class FakeRAMMonitor:

    def collect(self):
        return FakeMemory()


class FakeNotificationManager:

    def notify(self, pressure, ramPercent):
        return False


class FakeResumeCandidateSelector:

    def select(self, ramPercent):
        return []


class FakeCandidateSelector:

    def getCandidates(self):
        raise AssertionError(
            "CandidateSelector should not be called when autoPause=False"
        )


class FakeMemoryRanker:

    def rank(self, candidates):
        raise AssertionError(
            "MemoryRanker should not be called when autoPause=False"
        )


class FakeOrchestrator:

    def __init__(self):
        self.ramMonitor = FakeRAMMonitor()
        self.pressureCheck = FakePressureCheck()
        self.decisionEngine = FakeDecisionEngine()
        self.notificationManager = FakeNotificationManager()
        self.resumeCandidateSelector = (
            FakeResumeCandidateSelector()
        )
        self.candidateSelector = FakeCandidateSelector()
        self.memoryRanker = FakeMemoryRanker()


def run_tests():

    print(
        "\n========== Auto Pause Disabled Test ==========\n"
    )

    engine = GuardianEngine(
        orchestrator=FakeOrchestrator(),
        interval=1.0,
    )

    engine.config = FakeConfig(
        enabled=True,
        autoPause=False,
    )

    result = engine.runCycle()

    assert result["actionTaken"] is False
    assert result["pausedProcess"] is None
    assert result["resumedProcess"] is None
    assert result["actionReason"] == "No action required"

    print("PASS")

    print("\nALL TESTS PASSED\n")


if __name__ == "__main__":
    run_tests()