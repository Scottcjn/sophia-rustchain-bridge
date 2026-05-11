import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import rustchain_contract_explorer as explorer


class ContractExplorerTest(unittest.TestCase):
    def setUp(self):
        self.client = explorer.app.test_client()

    def test_generate_tx_hash_is_deterministic_and_hex_sized(self):
        payload = {"call": "vote", "proposal_id": 2}

        first = explorer.generate_tx_hash(payload)
        second = explorer.generate_tx_hash(payload)

        self.assertEqual(first, second)
        self.assertEqual(64, len(first))
        int(first, 16)

    def test_generate_tx_hash_changes_with_payload(self):
        first = explorer.generate_tx_hash({"call": "vote", "proposal_id": 2})
        second = explorer.generate_tx_hash({"call": "vote", "proposal_id": 3})

        self.assertNotEqual(first, second)

    def test_governance_contract_status_response(self):
        response = self.client.get("/api/explorer/contract/RTC_GOV_5923")

        self.assertEqual(200, response.status_code)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertEqual("RTC_GOV_5923", data["contract"]["address"])
        self.assertEqual("RustChain Governance Contract", data["contract"]["type"])
        self.assertTrue(data["contract"]["storage"]["sophia_veto_power"])

    def test_unknown_contract_returns_404(self):
        response = self.client.get("/api/explorer/contract/RTC_UNKNOWN")

        self.assertEqual(404, response.status_code)
        data = response.get_json()
        self.assertFalse(data["success"])
        self.assertEqual("Contract not found", data["error"])

    def test_transaction_endpoint_requires_64_character_hash(self):
        response = self.client.get("/api/explorer/tx/abc")

        self.assertEqual(400, response.status_code)
        data = response.get_json()
        self.assertFalse(data["success"])
        self.assertEqual("Invalid transaction hash", data["error"])

    def test_transaction_endpoint_returns_confirmed_contract_call(self):
        tx_hash = "a" * 64
        response = self.client.get(f"/api/explorer/tx/{tx_hash}")

        self.assertEqual(200, response.status_code)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(tx_hash, data["transaction"]["hash"])
        self.assertEqual("Confirmed", data["transaction"]["status"])
        self.assertEqual("vote", data["transaction"]["contract_method"])


if __name__ == "__main__":
    unittest.main()
