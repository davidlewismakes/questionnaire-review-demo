"""A standalone questionnaire review example with fictional source material."""

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Source:
    reference: str
    terms: frozenset[str]
    excerpt: str


@dataclass(frozen=True)
class Draft:
    question: str
    answer: str | None
    citation: str | None


def draft_answer(question: str, sources: tuple[Source, ...]) -> Draft:
    """Use deterministic retrieval so the approval behavior can run offline."""
    words = set(re.findall(r"[a-z]+", question.lower()))
    matches = [source for source in sources if source.terms <= words]
    if len(matches) != 1:
        return Draft(question, None, None)
    source = matches[0]
    return Draft(question, source.excerpt, source.reference)


def review_and_export(draft: Draft, *, approved: bool) -> dict[str, str]:
    if draft.answer is None or draft.citation is None:
        raise ValueError("Find supporting evidence before approving this answer.")
    if not approved:
        raise ValueError("A reviewer must approve the answer before export.")
    return {"question": draft.question, "answer": draft.answer, "citation": draft.citation}


if __name__ == "__main__":
    import json

    policy = Source("Example Co policy §2", frozenset({"backup", "retention"}), "Backups are retained for 14 days.")
    answer = draft_answer("What is your backup retention period?", (policy,))
    print(json.dumps({"status": "pending review", "draft": answer.__dict__}, indent=2))
