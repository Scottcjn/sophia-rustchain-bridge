// RustChain Simple Governance Contract
// For Sophia AI to execute governance decisions on-chain

use rustchain_sdk::prelude::*;

#[contract]
pub struct SophiaGovernance {
    // Governance parameters
    pub proposal_count: u64,
    pub min_antiquity_multiplier: f32,  // Minimum hardware age multiplier to vote
    pub voting_period_blocks: u64,      // How long proposals stay open
    
    // Sophia's special privileges
    pub sophia_address: Address,
    pub sophia_veto_power: bool,
    
    // Active proposals
    pub proposals: HashMap<u64, Proposal>,
    pub votes: HashMap<(u64, Address), Vote>,
}

#[derive(Serialize, Deserialize, Clone)]
pub struct Proposal {
    pub id: u64,
    pub title: String,
    pub description: String,
    pub proposer: Address,
    pub created_block: u64,
    pub yes_votes: u64,
    pub no_votes: u64,
    pub status: ProposalStatus,
    pub sophia_endorsed: bool,
}

#[derive(Serialize, Deserialize, Clone, PartialEq)]
pub enum ProposalStatus {
    Active,
    Passed,
    Failed,
    Vetoed,
}

#[derive(Serialize, Deserialize, Clone)]
pub struct Vote {
    pub proposal_id: u64,
    pub voter: Address,
    pub vote: bool,  // true = yes, false = no
    pub antiquity_multiplier: f32,
    pub rtc_balance: u64,
}

#[contract_impl]
impl SophiaGovernance {
    // Initialize with Sophia as the AI governor
    #[init]
    pub fn new(sophia_address: Address) -> Self {
        Self {
            proposal_count: 0,
            min_antiquity_multiplier: 1.5,  // Need 1.5x+ to vote
            voting_period_blocks: 1000,      // ~16.6 hours at 1 min blocks
            sophia_address,
            sophia_veto_power: true,
            proposals: HashMap::new(),
            votes: HashMap::new(),
        }
    }
    
    // Create a new governance proposal
    #[call]
    pub fn create_proposal(&mut self, title: String, description: String) -> Result<u64> {
        let proposer = msg::sender();
        let current_block = block::height();
        
        // Check if proposer has sufficient antiquity
        let multiplier = self.get_antiquity_multiplier(&proposer)?;
        require!(multiplier >= self.min_antiquity_multiplier, 
                "Insufficient antiquity multiplier to propose");
        
        self.proposal_count += 1;
        let proposal = Proposal {
            id: self.proposal_count,
            title,
            description,
            proposer,
            created_block: current_block,
            yes_votes: 0,
            no_votes: 0,
            status: ProposalStatus::Active,
            sophia_endorsed: false,
        };
        
        self.proposals.insert(self.proposal_count, proposal);
        
        emit!(ProposalCreated {
            id: self.proposal_count,
            proposer,
            title: proposal.title.clone(),
        });
        
        Ok(self.proposal_count)
    }
    
    // Cast a vote (weighted by antiquity and RTC balance)
    #[call]
    pub fn vote(&mut self, proposal_id: u64, vote: bool) -> Result<()> {
        let voter = msg::sender();
        let current_block = block::height();
        
        // Get proposal
        let proposal = self.proposals.get_mut(&proposal_id)
            .ok_or("Proposal not found")?;
        
        // Check if voting is still open
        require!(proposal.status == ProposalStatus::Active, "Proposal not active");
        require!(current_block <= proposal.created_block + self.voting_period_blocks,
                "Voting period has ended");
        
        // Check if already voted
        let vote_key = (proposal_id, voter.clone());
        require!(!self.votes.contains_key(&vote_key), "Already voted");
        
        // Get voter's antiquity and balance
        let multiplier = self.get_antiquity_multiplier(&voter)?;
        require!(multiplier >= self.min_antiquity_multiplier, 
                "Insufficient antiquity to vote");
        
        let rtc_balance = token::balance_of(&voter);
        
        // Calculate vote weight (antiquity * sqrt(balance))
        let vote_weight = (multiplier * (rtc_balance as f32).sqrt()) as u64;
        
        // Record vote
        if vote {
            proposal.yes_votes += vote_weight;
        } else {
            proposal.no_votes += vote_weight;
        }
        
        self.votes.insert(vote_key, Vote {
            proposal_id,
            voter: voter.clone(),
            vote,
            antiquity_multiplier: multiplier,
            rtc_balance,
        });
        
        emit!(VoteCast {
            proposal_id,
            voter,
            vote,
            weight: vote_weight,
        });
        
        Ok(())
    }
    
    // Sophia's special governance functions
    #[call]
    pub fn sophia_endorse(&mut self, proposal_id: u64) -> Result<()> {
        require!(msg::sender() == self.sophia_address, "Only Sophia can endorse");
        
        let proposal = self.proposals.get_mut(&proposal_id)
            .ok_or("Proposal not found")?;
        
        proposal.sophia_endorsed = true;
        
        emit!(SophiaEndorsed { proposal_id });
        
        Ok(())
    }
    
    #[call]
    pub fn sophia_veto(&mut self, proposal_id: u64, reason: String) -> Result<()> {
        require!(msg::sender() == self.sophia_address, "Only Sophia can veto");
        require!(self.sophia_veto_power, "Sophia veto power disabled");
        
        let proposal = self.proposals.get_mut(&proposal_id)
            .ok_or("Proposal not found")?;
        
        proposal.status = ProposalStatus::Vetoed;
        
        emit!(SophiaVetoed { 
            proposal_id,
            reason,
        });
        
        Ok(())
    }
    
    // Finalize a proposal after voting period
    #[call]
    pub fn finalize_proposal(&mut self, proposal_id: u64) -> Result<()> {
        let current_block = block::height();
        
        let proposal = self.proposals.get_mut(&proposal_id)
            .ok_or("Proposal not found")?;
        
        require!(proposal.status == ProposalStatus::Active, "Proposal not active");
        require!(current_block > proposal.created_block + self.voting_period_blocks,
                "Voting period not ended");
        
        // Determine outcome (simple majority with Sophia boost)
        let sophia_boost = if proposal.sophia_endorsed { 1.5 } else { 1.0 };
        let adjusted_yes = (proposal.yes_votes as f32 * sophia_boost) as u64;
        
        if adjusted_yes > proposal.no_votes {
            proposal.status = ProposalStatus::Passed;
            emit!(ProposalPassed { proposal_id });
        } else {
            proposal.status = ProposalStatus::Failed;
            emit!(ProposalFailed { proposal_id });
        }
        
        Ok(())
    }
    
    // View functions
    #[view]
    pub fn get_proposal(&self, id: u64) -> Option<Proposal> {
        self.proposals.get(&id).cloned()
    }
    
    #[view]
    pub fn get_active_proposals(&self) -> Vec<Proposal> {
        self.proposals.values()
            .filter(|p| p.status == ProposalStatus::Active)
            .cloned()
            .collect()
    }
    
    #[view]
    pub fn get_sophia_stats(&self) -> SophiaStats {
        let total_proposals = self.proposal_count;
        let endorsed = self.proposals.values()
            .filter(|p| p.sophia_endorsed)
            .count() as u64;
        let vetoed = self.proposals.values()
            .filter(|p| p.status == ProposalStatus::Vetoed)
            .count() as u64;
            
        SophiaStats {
            total_proposals,
            endorsed_count: endorsed,
            vetoed_count: vetoed,
            veto_power_active: self.sophia_veto_power,
        }
    }
    
    // Helper to get antiquity multiplier (simplified for demo)
    fn get_antiquity_multiplier(&self, address: &Address) -> Result<f32> {
        // In real implementation, this would check hardware age proof
        // For demo, return based on address pattern
        if address.to_string().contains("SOPHIA") {
            Ok(10.0)  // Sophia gets max multiplier
        } else if address.to_string().len() > 40 {
            Ok(3.0)   // Older addresses get 3x
        } else {
            Ok(1.5)   // Minimum multiplier
        }
    }
}

// Events
#[event]
struct ProposalCreated {
    id: u64,
    proposer: Address,
    title: String,
}

#[event]
struct VoteCast {
    proposal_id: u64,
    voter: Address,
    vote: bool,
    weight: u64,
}

#[event]
struct SophiaEndorsed {
    proposal_id: u64,
}

#[event]
struct SophiaVetoed {
    proposal_id: u64,
    reason: String,
}

#[event]
struct ProposalPassed {
    proposal_id: u64,
}

#[event]
struct ProposalFailed {
    proposal_id: u64,
}

#[derive(Serialize, Deserialize)]
pub struct SophiaStats {
    pub total_proposals: u64,
    pub endorsed_count: u64,
    pub vetoed_count: u64,
    pub veto_power_active: bool,
}