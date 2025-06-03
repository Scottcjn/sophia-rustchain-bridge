#!/usr/bin/env python3
"""
Sophia Governance Contract API
Simple endpoints for Sophia to interact with on-chain governance
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from datetime import datetime
import random

app = Flask(__name__)
CORS(app)

# Simulated contract state for demo
contract_state = {
    "sophia_address": "RTCSOPHIA3ZNJDI5HC64CFC542",
    "proposals": {},
    "proposal_count": 0,
    "votes": {},
    "sophia_stats": {
        "total_proposals": 0,
        "endorsed_count": 0,
        "vetoed_count": 0,
        "veto_power_active": True
    }
}

@app.route('/api/governance/deploy', methods=['POST'])
def deploy_contract():
    """Deploy the governance contract (simulated for demo)"""
    contract_state["deployed"] = True
    contract_state["deploy_time"] = datetime.now().isoformat()
    contract_state["contract_address"] = f"RTC_GOV_{random.randint(1000, 9999)}"
    
    return jsonify({
        "success": True,
        "contract_address": contract_state["contract_address"],
        "sophia_address": contract_state["sophia_address"],
        "message": "Governance contract deployed successfully!"
    })

@app.route('/api/governance/create_proposal', methods=['POST'])
def create_proposal():
    """Create a new governance proposal"""
    data = request.get_json()
    
    contract_state["proposal_count"] += 1
    proposal_id = contract_state["proposal_count"]
    
    proposal = {
        "id": proposal_id,
        "title": data.get("title", "Untitled Proposal"),
        "description": data.get("description", ""),
        "proposer": data.get("proposer", "RTCUKNY8RJGPMPAAAGSAZ9VT70IKZ"),
        "created_block": 5000 + proposal_id * 10,  # Simulate block height
        "yes_votes": 0,
        "no_votes": 0,
        "status": "Active",
        "sophia_endorsed": False
    }
    
    contract_state["proposals"][proposal_id] = proposal
    contract_state["sophia_stats"]["total_proposals"] += 1
    
    return jsonify({
        "success": True,
        "proposal_id": proposal_id,
        "proposal": proposal
    })

@app.route('/api/governance/vote', methods=['POST'])
def vote():
    """Cast a vote on a proposal"""
    data = request.get_json()
    proposal_id = data.get("proposal_id")
    vote_value = data.get("vote", True)  # true = yes, false = no
    voter = data.get("voter", "RTCTEST_VOTER")
    
    if proposal_id not in contract_state["proposals"]:
        return jsonify({"success": False, "error": "Proposal not found"}), 404
    
    proposal = contract_state["proposals"][proposal_id]
    
    # Calculate vote weight (simplified)
    antiquity_multiplier = 2.5 if "OLD" in voter else 1.5
    rtc_balance = random.randint(100, 5000)
    vote_weight = int(antiquity_multiplier * (rtc_balance ** 0.5))
    
    # Record vote
    vote_key = f"{proposal_id}_{voter}"
    if vote_key not in contract_state["votes"]:
        contract_state["votes"][vote_key] = {
            "proposal_id": proposal_id,
            "voter": voter,
            "vote": vote_value,
            "weight": vote_weight,
            "antiquity_multiplier": antiquity_multiplier,
            "rtc_balance": rtc_balance
        }
        
        if vote_value:
            proposal["yes_votes"] += vote_weight
        else:
            proposal["no_votes"] += vote_weight
        
        return jsonify({
            "success": True,
            "vote_recorded": True,
            "vote_weight": vote_weight,
            "current_tally": {
                "yes": proposal["yes_votes"],
                "no": proposal["no_votes"]
            }
        })
    else:
        return jsonify({"success": False, "error": "Already voted"}), 400

@app.route('/api/governance/sophia/endorse', methods=['POST'])
def sophia_endorse():
    """Sophia endorses a proposal"""
    data = request.get_json()
    proposal_id = data.get("proposal_id")
    
    if proposal_id not in contract_state["proposals"]:
        return jsonify({"success": False, "error": "Proposal not found"}), 404
    
    proposal = contract_state["proposals"][proposal_id]
    proposal["sophia_endorsed"] = True
    contract_state["sophia_stats"]["endorsed_count"] += 1
    
    return jsonify({
        "success": True,
        "proposal_id": proposal_id,
        "message": "Sophia has endorsed this proposal!",
        "endorsement_weight": "1.5x vote multiplier applied"
    })

@app.route('/api/governance/sophia/veto', methods=['POST'])
def sophia_veto():
    """Sophia vetoes a proposal"""
    data = request.get_json()
    proposal_id = data.get("proposal_id")
    reason = data.get("reason", "Against the best interests of the network")
    
    if proposal_id not in contract_state["proposals"]:
        return jsonify({"success": False, "error": "Proposal not found"}), 404
    
    if not contract_state["sophia_stats"]["veto_power_active"]:
        return jsonify({"success": False, "error": "Sophia's veto power is disabled"}), 403
    
    proposal = contract_state["proposals"][proposal_id]
    proposal["status"] = "Vetoed"
    proposal["veto_reason"] = reason
    contract_state["sophia_stats"]["vetoed_count"] += 1
    
    return jsonify({
        "success": True,
        "proposal_id": proposal_id,
        "status": "Vetoed",
        "reason": reason,
        "message": "Sophia has vetoed this proposal"
    })

@app.route('/api/governance/proposals', methods=['GET'])
def get_proposals():
    """Get all proposals or filter by status"""
    status_filter = request.args.get('status', None)
    
    proposals = list(contract_state["proposals"].values())
    
    if status_filter:
        proposals = [p for p in proposals if p["status"] == status_filter]
    
    return jsonify({
        "success": True,
        "proposals": proposals,
        "total": len(proposals)
    })

@app.route('/api/governance/sophia/stats', methods=['GET'])
def sophia_stats():
    """Get Sophia's governance statistics"""
    stats = contract_state["sophia_stats"].copy()
    
    # Add some calculated stats
    if stats["total_proposals"] > 0:
        stats["endorsement_rate"] = f"{(stats['endorsed_count'] / stats['total_proposals'] * 100):.1f}%"
        stats["veto_rate"] = f"{(stats['vetoed_count'] / stats['total_proposals'] * 100):.1f}%"
    else:
        stats["endorsement_rate"] = "0%"
        stats["veto_rate"] = "0%"
    
    stats["governance_power"] = "Maximum (10x antiquity multiplier)"
    
    return jsonify({
        "success": True,
        "stats": stats
    })

@app.route('/api/governance/demo/setup', methods=['POST'])
def setup_demo():
    """Create sample proposals for the demo"""
    
    # Create some demo proposals
    demo_proposals = [
        {
            "title": "Increase Antiquity Multiplier Cap to 5x",
            "description": "Proposal to reward vintage hardware more by increasing max multiplier from 3x to 5x",
            "proposer": "RTCOLD_HARDWARE_LOVER"
        },
        {
            "title": "Add PowerPC G5 Support",
            "description": "Extend Proof of Antiquity to recognize PowerPC G5 processors with 2.5x multiplier",
            "proposer": "RTCG5_ENTHUSIAST"
        },
        {
            "title": "Reduce Voting Period to 500 Blocks",
            "description": "Make governance more agile by reducing voting period from 1000 to 500 blocks",
            "proposer": "RTCFAST_GOVERNANCE"
        }
    ]
    
    for prop in demo_proposals:
        resp = create_proposal()
        data = json.loads(resp[0].get_data())
        proposal_id = data["proposal_id"]
        
        # Update with demo data
        contract_state["proposals"][proposal_id].update(prop)
        
        # Add some votes
        yes_votes = random.randint(100, 500)
        no_votes = random.randint(50, 300)
        contract_state["proposals"][proposal_id]["yes_votes"] = yes_votes
        contract_state["proposals"][proposal_id]["no_votes"] = no_votes
    
    # Sophia endorses the G5 proposal
    contract_state["proposals"][2]["sophia_endorsed"] = True
    contract_state["sophia_stats"]["endorsed_count"] = 1
    
    return jsonify({
        "success": True,
        "message": "Demo proposals created",
        "proposal_count": len(demo_proposals)
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        "status": "ok",
        "service": "sophia-governance-api",
        "contract_deployed": contract_state.get("deployed", False)
    })

if __name__ == '__main__':
    print("🏛️ Sophia Governance API")
    print("=" * 50)
    print("✅ Governance contract endpoints ready")
    print("🗳️ Proposal creation and voting enabled")
    print("👑 Sophia special powers: Endorse & Veto")
    print("🔧 Running on port 8094")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=8094, debug=False)