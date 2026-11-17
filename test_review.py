import unittest

from review import Source, draft_answer, review_and_export


class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.source = Source("Example policy §2", frozenset({"backups"}), "Backups are retained for 14 days.")

    def test_supported_answer_requires_approval(self):
        draft = draft_answer("How long do you keep backups?", (self.source,))
        with self.assertRaisesRegex(ValueError, "reviewer"):
            review_and_export(draft, approved=False)
        self.assertEqual(review_and_export(draft, approved=True)["citation"], "Example policy §2")

    def test_missing_or_conflicting_evidence_blocks_export(self):
        alternative = Source("Example policy §3", frozenset({"backups"}), "Backups are retained for 30 days.")
        for sources in ((), (self.source, alternative)):
            with self.subTest(sources=sources), self.assertRaisesRegex(ValueError, "evidence"):
                review_and_export(draft_answer("How long do you keep backups?", sources), approved=True)


if __name__ == "__main__":
    unittest.main()
