from app.adjudicator.engine import Adjudicator
from app.schemas.critic import CriticResult


def test_adjudicator():

    critic_results = {
        "accuracy": CriticResult(
            score=9,
            reasoning="Correct facts",
            strengths=["Factually accurate"],
            issues=[],
            suggestions=[]
        ),
        "logic": CriticResult(
            score=8,
            reasoning="Logical reasoning",
            strengths=["Well structured"],
            issues=["Minor reasoning gap"],
            suggestions=["Explain one step more clearly"]
        ),
        "completeness": CriticResult(
            score=10,
            reasoning="Complete answer",
            strengths=["Covered all requested points"],
            issues=[],
            suggestions=[]
        )
    }

    adjudicator = Adjudicator()

    verdict = adjudicator.evaluate(critic_results)

    assert verdict.overall_score == 9.0
    assert verdict.verdict == "Excellent"
    assert verdict.summary == "The response achieved an overall score of 9.0/10."

    assert verdict.strengths == [
        "Factually accurate",
        "Well structured",
        "Covered all requested points"
    ]

    assert verdict.weaknesses == [
        "Minor reasoning gap"
    ]

    assert verdict.improvements == [
        "Explain one step more clearly"
    ]