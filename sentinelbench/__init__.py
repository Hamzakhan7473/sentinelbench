"""SentinelBench: benchmarking for evidence-grounded security AI agents."""

from sentinelbench.models import MockProvider, get_provider
from sentinelbench.types import AgentPrediction, IncidentResult, ScoreResult

__version__ = "0.1.0"

__all__ = [
    "AgentPrediction",
    "IncidentResult",
    "MockProvider",
    "ScoreResult",
    "__version__",
    "get_provider",
]
