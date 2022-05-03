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
export const TransactionContentMappingType = Object.freeze(
	{
		APPLICANT_BASE: 1,
		APPLICANT_LOG: 2,
		APPLICANT_ADDITIONAL: 3,
	}
)

export const NodeTransactionInternalActions = Object.freeze(
	{
		CONSENSUS: 1,
		INIT: 2,
		SYNC: 3,
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

export function resolveContextType(typeField) {
	let identifiedType = typeField.hasOwnProperty('content_type') ? 'User Transaction' : 'Internal Transaction'
	let resolvedTypeValue = null


	// ! Resolve this content type from the `User Transaction Content Mapping`.
	if (typeField.hasOwnProperty('content_type')) {
		switch (typeField.content_type) {
			case TransactionContentMappingType.APPLICANT_BASE:
				resolvedTypeValue = 'Applicant Base Portfolio'
				break
			case TransactionContentMappingType.APPLICANT_LOG:
				resolvedTypeValue = 'Applicant Log from Orgs'
				break
			case TransactionContentMappingType.APPLICANT_ADDITIONAL:
				resolvedTypeValue = 'Applicant Additional Info / Remarks'
				break
			default:
				resolvedTypeValue = 'Unidentified'
				break
		}
	} else {
		console.log('cxz')
		switch (typeField.action) {
			case NodeTransactionInternalActions.CONSENSUS: ;
				resolvedTypeValue = 'Internal: Consensus Context'
				break
			case NodeTransactionInternalActions.INIT:
				resolvedTypeValue = 'Internal: Context Initialization'
				break
			case NodeTransactionInternalActions.SYNC:
				resolvedTypeValue = 'Internal: Sync from Communication'
				break
			default:
				resolvedTypeValue = 'Unidentified'
				break
		}
	}

	console.log(identifiedType, resolveContextType)

	return { identifiedType, resolvedTypeValue }

}