const PROTOCOL_USAGE = `${process.env.BUILT_LOCALLY ? 'http' : 'https'}://`
export const MASTER_NODE_BACKEND_URL = `${PROTOCOL_USAGE}${process.env.BUILT_LOCALLY ? process.env.TARGET_MASTER_NODE_ADDRESS_DEV : process.env.TARGET_MASTER_NODE_ADDRESS_PROD}`
export const FRONTEND_WEBAPP_URL = `${PROTOCOL_USAGE}${process.env.BUILT_LOCALLY ? process.env.FRONTEND_ADDRESS_DEV : process.env.FRONTEND_ADDRESS_PROD}`

export const TABLE_DEFAULT_ROW_COUNT = 100
export const QR_CODE_METADATA_AUTH_FOR_ORGS = 'otpauth://totp/Organization%20Creator:Folioblocks-Web?secret=MNMDQX32IREXQQLIM4YHMYSYLFUHASCBMJFF63TCMU4UY5TNJBTVMWC7OMWTSQLUNJEVCPJRGZQTOZJTMYYDAOLFMJRGMMJWMVSWCOJWGM2TMOBTHBTGMYZTGMZDOZTDGI2TEOJYGM2DMYRRGE3DCYZVGNRTSYRRMQ3WKNZSGAZDG%3D%3D%3D&issuer=Organization%20Creator'

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
		INSTITUTION_ORG_GENERATE_STUDENT: 7,
		INSTITUTION_ORG_REFER_NEW_DOCUMENT_OR_IMPORTANT_INFO: 8,
		INSTITUTION_ORG_STUDENT_REFER_EXTRA_INFO: 9,

		// - For Organization, in general.
		ORGANIZATION_USER_REGISTER: 10,
		ORGANIZATION_REFER_EXTRA_INFO: 11,
	}
)
export const TransactionContentMappingType = Object.freeze(
	{
		STUDENT_BASE: 1,
		STUDENT_LOG: 2,
		STUDENT_ADDITIONAL: 3,
		ORGANIZATION_BASE: 4
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
		case TransactionActions.INSTITUTION_ORG_GENERATE_STUDENT:
			return 'Institution Student Generation'
		case TransactionActions.INSTITUTION_ORG_REFER_NEW_DOCUMENT_OR_IMPORTANT_INFO:
			return 'Institution New Document / Important Info to Student Reference'
		case TransactionActions.INSTITUTION_ORG_STUDENT_REFER_EXTRA_INFO:
			return 'Institution Refer Extra Info to Student'
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
			case TransactionContentMappingType.STUDENT_BASE:
				resolvedTypeValue = 'Student Base Portfolio'
				break
			case TransactionContentMappingType.STUDENT_LOG:
				resolvedTypeValue = 'Student Log from Orgs'
				break
			case TransactionContentMappingType.STUDENT_ADDITIONAL:
				resolvedTypeValue = 'Student Additional Info / Remarks'
				break
			case TransactionContentMappingType.ORGANIZATION_BASE:
				resolvedTypeValue = 'Organization Base Registration'
				break
			default:
				resolvedTypeValue = 'Unidentified'
				break
		}
	} else {
		switch (typeField.action) {
			case NodeTransactionInternalActions.CONSENSUS:
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
	return { identifiedType, resolvedTypeValue }
}