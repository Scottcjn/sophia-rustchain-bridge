"""Regression tests for the governance transaction ledger.

`send_blockchain_transaction()` used to load its own copy of the state file and
save it, while the request handler that called it saved a copy loaded *before*
the transaction existed. The handler's save always won, so every transaction
belonging to a successful request was dropped from `governance_state.json`.

These tests drive the real Flask apps through their real routes and assert
against what actually lands on disk / comes back from the read endpoints.
"""

import importlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


class LedgerTestMixin:
    """Shared assertions; MODULE_NAME is set by the concrete test cases."""

    MODULE_NAME = None

    def setUp(self):
        self.module = importlib.import_module(self.MODULE_NAME)
        self.tmpdir = tempfile.mkdtemp()
        self._original_state_file = self.module.STATE_FILE
        self.module.STATE_FILE = str(Path(self.tmpdir) / "governance_state.json")
        self.client = self.module.app.test_client()

    def tearDown(self):
        self.module.STATE_FILE = self._original_state_file
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    # helpers -----------------------------------------------------------------

    def on_disk(self):
        with open(self.module.STATE_FILE) as handle:
            return json.load(handle)

    def ledger(self):
        return self.on_disk().get("transactions", [])

    def create_proposal(self, title="Increase Antiquity Multiplier Cap to 5x"):
        response = self.client.post(
            "/api/governance/create_proposal",
            json={"title": title, "proposer": "RTCOLD_HARDWARE_LOVER"},
        )
        self.assertEqual(200, response.status_code)
        return response.get_json()["proposal_id"]

    # tests -------------------------------------------------------------------

    def test_create_proposal_transaction_reaches_the_ledger(self):
        response = self.client.post(
            "/api/governance/create_proposal", json={"title": "Add PowerPC G5 Support"}
        )

        tx_hash = response.get_json()["tx_hash"]
        ledger = self.ledger()
        self.assertEqual(1, len(ledger))
        self.assertEqual(tx_hash, ledger[0]["hash"])
        self.assertEqual("createProposal", ledger[0]["method"])

    def test_recorded_transaction_is_confirmed(self):
        self.create_proposal()

        record = self.ledger()[0]
        self.assertEqual("confirmed", record["status"])
        self.assertEqual(1, record["confirmations"])

    def test_every_mutating_endpoint_appends_exactly_one_transaction(self):
        self.client.post("/api/governance/deploy")
        self.assertEqual(["deploy"], [tx["method"] for tx in self.ledger()])

        proposal_id = self.create_proposal()
        self.assertEqual(
            ["deploy", "createProposal"], [tx["method"] for tx in self.ledger()]
        )

        self.client.post(
            "/api/governance/vote",
            json={"proposal_id": proposal_id, "vote": True, "voter": "RTCG5_ENTHUSIAST"},
        )
        self.client.post(
            "/api/governance/sophia/endorse", json={"proposal_id": proposal_id}
        )
        self.client.post(
            "/api/governance/sophia/veto",
            json={"proposal_id": proposal_id, "reason": "not now"},
        )

        self.assertEqual(
            ["deploy", "createProposal", "castVote", "sophiaEndorse", "sophiaVeto"],
            [tx["method"] for tx in self.ledger()],
        )

    def test_transactions_endpoint_reports_the_recorded_transactions(self):
        proposal_id = self.create_proposal()
        self.client.post(
            "/api/governance/vote",
            json={"proposal_id": proposal_id, "vote": True, "voter": "RTCG5_ENTHUSIAST"},
        )

        data = self.client.get("/api/governance/transactions").get_json()

        self.assertTrue(data["success"])
        self.assertEqual(2, data["total"])
        self.assertEqual(2, len(data["transactions"]))

    def test_health_transaction_count_matches_the_ledger(self):
        self.create_proposal()
        self.create_proposal("Reduce Voting Period to 500 Blocks")

        health = self.client.get("/health").get_json()

        self.assertEqual(len(self.ledger()), health["total_transactions"])
        self.assertEqual(2, health["total_transactions"])

    def test_ledger_survives_a_restart(self):
        self.create_proposal()
        hashes_before = [tx["hash"] for tx in self.ledger()]
        self.assertTrue(hashes_before, "nothing was written to the ledger")

        # A fresh client stands in for a restarted process: state comes back
        # from governance_state.json, nothing is kept in memory.
        restarted = self.module.app.test_client()
        data = restarted.get("/api/governance/transactions").get_json()

        self.assertEqual(hashes_before, [tx["hash"] for tx in data["transactions"]])

    def test_duplicate_vote_is_rejected_but_its_transaction_is_kept(self):
        proposal_id = self.create_proposal()
        payload = {"proposal_id": proposal_id, "vote": True, "voter": "RTCG5_ENTHUSIAST"}
        self.client.post("/api/governance/vote", json=payload)

        second = self.client.post("/api/governance/vote", json=payload)

        self.assertEqual(400, second.status_code)
        self.assertEqual("Already voted", second.get_json()["error"])
        self.assertEqual(
            ["createProposal", "castVote", "castVote"],
            [tx["method"] for tx in self.ledger()],
        )

    def test_demo_setup_records_all_four_transactions(self):
        response = self.client.post("/api/governance/demo/setup")

        self.assertEqual(200, response.status_code)
        self.assertEqual(
            ["createProposal", "createProposal", "createProposal", "sophiaEndorse"],
            [tx["method"] for tx in self.ledger()],
        )

    # the fix must not disturb the state the handlers themselves write

    def test_proposal_and_tally_still_persist(self):
        proposal_id = self.create_proposal()
        vote = self.client.post(
            "/api/governance/vote",
            json={"proposal_id": proposal_id, "vote": True, "voter": "RTCG5_ENTHUSIAST"},
        ).get_json()

        state = self.on_disk()
        proposal = state["proposals"][str(proposal_id)]
        self.assertEqual(1, state["proposal_count"])
        self.assertEqual(vote["vote_weight"], proposal["yes_votes"])
        self.assertEqual(0, proposal["no_votes"])
        self.assertEqual(1, state["sophia_stats"]["total_proposals"])

    def test_veto_still_marks_the_proposal(self):
        proposal_id = self.create_proposal()

        self.client.post(
            "/api/governance/sophia/veto",
            json={"proposal_id": proposal_id, "reason": "hurts vintage miners"},
        )

        proposal = self.on_disk()["proposals"][str(proposal_id)]
        self.assertEqual("Vetoed", proposal["status"])
        self.assertEqual("hurts vintage miners", proposal["veto_reason"])
        self.assertEqual(1, self.on_disk()["sophia_stats"]["vetoed_count"])


class GovernanceApiLedgerTest(LedgerTestMixin, unittest.TestCase):
    MODULE_NAME = "sophia_governance_api"


class GovernanceApiRealLedgerTest(LedgerTestMixin, unittest.TestCase):
    MODULE_NAME = "sophia_governance_api_real"


if __name__ == "__main__":
    unittest.main()
