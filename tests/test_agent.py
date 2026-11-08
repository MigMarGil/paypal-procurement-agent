import unittest
from src.agent import ProcurementAgent

class TestProcurementAgent(unittest.TestCase):
    def setUp(self):
        self.agent = ProcurementAgent()

    def test_fallback_evaluation(self):
        # Force fallback behavior by disabling AI
        self.agent.use_ai = False
        result = self.agent.evaluate_intent("Test Server Purchase")
        
        self.assertIn("item", result)
        self.assertIn("amount", result)
        self.assertTrue(result["approved"])
        self.assertEqual(result["risk_level"], "LOW")

if __name__ == "__main__":
    unittest.main()
