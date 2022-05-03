export const nodeUrl = process.env.TARGET_MASTER_NODE_ADDRESS
export const nodePort = process.env.TARGET_MASTER_NODE_PORT
export const resolvedNodeAPIURL = `${nodeUrl}:${nodePort}`
export const TABLE_DEFAULT_ROW_COUNT = 100

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

export function resolveTransactionActions(action) {

	switch (action) {
		case TransactionActions.NODE_GENERAL_CONSENSUS_INIT:
			return 'Consensus Initialization'
		case TransactionActions.NODE_GENERAL_REGISTER_INIT:
			return 'Node Registration'
		case TransactionActions.NODE_GENERAL_GENESIS_BLOCK_INIT:
			return 'Node Genesis Block Creation'
		case TransactionActions.NODE_GENERAL_CONSENSUS_BLOCK_SYNC:
			return 'Node Block Sync via Consensus'
		case TransactionActions.NODE_GENERAL_CONSENSUS_CONFIRM_NEGOTIATION_START:
			return 'Node Consensus Negotiation Confirmed Start'
		case TransactionActions.NODE_GENERAL_CONSENSUS_CONCLUDE_NEGOTIATION_PROCESSING:
			return 'Node Consensus Negotiation Conclusion of Processing'
		case TransactionActions.INSTITUTION_ORG_GENERATE_APPLICANT:
			return 'Institution Applicant Generation'
		case TransactionActions.INSTITUTION_ORG_REFER_NEW_DOCUMENT_OR_IMPORTANT_INFO:
			return 'Institution New Document / Important Info to Applicant Reference'
		case TransactionActions.INSTITUTION_ORG_APPLICANT_REFER_EXTRA_INFO:
			return 'Institution Refer Extra Info to Applicant'
		case TransactionActions.ORGANIZATION_USER_REGISTER:
			return 'Organization Registration'
		case TransactionActions.ORGANIZATION_REFER_EXTRA_INFO:
			return 'Extra Info Referral to Organization'

		default:
			return 'Unidentified Action.'
	}
}