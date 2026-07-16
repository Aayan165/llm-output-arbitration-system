from app.schemas.verdict import FinalVerdict

class Adjudicator:
    def evaluate(self, critic_results: dict) -> FinalVerdict:
        scores = [
            result.score
            for result in critic_results.values()
        ]

        overall_score = round(sum(scores) / len(scores), 2)

        strengths = []
        weaknesses = []
        improvements = []


        for result in critic_results.values():
            strengths.extend(result.strengths)
            weaknesses.extend(result.issues)
            improvements.extend(result.suggestions)

        if overall_score >= 9:
            verdict = "Excellent"
        elif overall_score >= 7:
            verdict = "Good"
        elif overall_score >= 5:
            verdict = "Average"
        else:
            verdict = "Poor"

        summary = (
            "The response achieved an overall score of " +
            f"{overall_score}/10."
        )

        return FinalVerdict(
            overall_score=overall_score,
            verdict=verdict,
            summary=summary,
            strengths=strengths,
            weaknesses=weaknesses,
            improvements=improvements
        )
