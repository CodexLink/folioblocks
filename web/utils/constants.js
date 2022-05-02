export const nodeUrl = process.env.TARGET_MASTER_NODE_ADDRESS
export const nodePort = process.env.TARGET_MASTER_NODE_PORT
export const resolvedNodeAPIURL = `${nodeUrl}:${nodePort}`

// # # Adapted from the core/utils/constants.py.
export const TransactionActions = Object.freeze(
	{	// - Node-based Transactions: General
		NODE_GENERAL_CONSENSUS_INIT: 1,
		NODE_GENERAL_REGISTER_INIT: 2,
		NODE_GENERAL_GENESIS_BLOCK_INIT: 3,

		// - Node-based Transaction: Consensus (Consensus)
		NODE_GENERAL_CONSENSUS_BLOCK_SYNC: 4,
		NODE_GENERAL_CONSENSUS_CONFIRM_NEGOTIATION_START: 5,
		NODE_GENERAL_CONSENSUS_CONCLUDE_NEGOTIATION_PROCESSING: 6,

		// # Note that anything below from this context requires assistance from `models.block_context_mappings`.
		// - For Institutions / Organization.
		INSTITUTION_ORG_GENERATE_APPLICANT: 7,
		INSTITUTION_ORG_REFER_NEW_DOCUMENT_OR_IMPORTANT_INFO: 8,
		INSTITUTION_ORG_APPLICANT_REFER_EXTRA_INFO: 9,

		// - For Organization, in general.
		ORGANIZATION_USER_REGISTER: 10,
		ORGANIZATION_REFER_EXTRA_INFO: 11,
	}
)