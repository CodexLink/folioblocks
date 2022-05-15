(self["webpackChunkfolioblocks_web"]=self["webpackChunkfolioblocks_web"]||[]).push([[997],{2796:(e,t,a)=>{"use strict";a.d(t,{$T:()=>_,_u:()=>d,kb:()=>r,sx:()=>s,uK:()=>n});const o="https://",s=`${o}folioblocks.southeastasia.azurecontainer.io`,n=`${o}codexlink.github.io/folioblocks`,r=100,i=Object.freeze({NODE_GENERAL_CONSENSUS_INIT:1,NODE_GENERAL_REGISTER_INIT:2,NODE_GENERAL_GENESIS_BLOCK_INIT:3,NODE_GENERAL_CONSENSUS_BLOCK_SYNC:4,NODE_GENERAL_CONSENSUS_CONFIRM_NEGOTIATION_START:5,NODE_GENERAL_CONSENSUS_CONCLUDE_NEGOTIATION_PROCESSING:6,INSTITUTION_ORG_GENERATE_STUDENT:7,INSTITUTION_ORG_REFER_NEW_DOCUMENT_OR_IMPORTANT_INFO:8,INSTITUTION_ORG_STUDENT_REFER_EXTRA_INFO:9,ORGANIZATION_USER_REGISTER:10,ORGANIZATION_REFER_EXTRA_INFO:11}),l=Object.freeze({STUDENT_BASE:1,STUDENT_LOG:2,STUDENT_ADDITIONAL:3,ORGANIZATION_BASE:4}),c=Object.freeze({CONSENSUS:1,INIT:2,SYNC:3});function _(e){switch(e){case i.NODE_GENERAL_CONSENSUS_INIT:return"Consensus Initialization";case i.NODE_GENERAL_REGISTER_INIT:return"Node Registration";case i.NODE_GENERAL_GENESIS_BLOCK_INIT:return"Node Genesis Block Creation";case i.NODE_GENERAL_CONSENSUS_BLOCK_SYNC:return"Node Block Sync via Consensus";case i.NODE_GENERAL_CONSENSUS_CONFIRM_NEGOTIATION_START:return"Node Consensus Negotiation Confirmed Start";case i.NODE_GENERAL_CONSENSUS_CONCLUDE_NEGOTIATION_PROCESSING:return"Node Consensus Negotiation Conclusion of Processing";case i.INSTITUTION_ORG_GENERATE_STUDENT:return"Institution Student Generation";case i.INSTITUTION_ORG_REFER_NEW_DOCUMENT_OR_IMPORTANT_INFO:return"Institution New Document / Important Info to Student Reference";case i.INSTITUTION_ORG_STUDENT_REFER_EXTRA_INFO:return"Institution Refer Extra Info to Student";case i.ORGANIZATION_USER_REGISTER:return"Organization Registration";case i.ORGANIZATION_REFER_EXTRA_INFO:return"Extra Info Referral to Organization";default:return"Unidentified Action."}}function d(e){let t=e.hasOwnProperty("content_type")?"User Transaction":"Internal Transaction",a=null;if(e.hasOwnProperty("content_type"))switch(e.content_type){case l.STUDENT_BASE:a="Student Base Portfolio";break;case l.STUDENT_LOG:a="Student Log from Orgs";break;case l.STUDENT_ADDITIONAL:a="Student Additional Info / Remarks";break;case l.ORGANIZATION_BASE:a="Organization Base Registration";break;default:a="Unidentified";break}else switch(e.action){case c.CONSENSUS:a="Internal: Consensus Context";break;case c.INIT:a="Internal: Context Initialization";break;case c.SYNC:a="Internal: Sync from Communication";break;default:a="Unidentified";break}return{identifiedType:t,resolvedTypeValue:a}}},7997:(e,t,a)=>{"use strict";a.r(t),a.d(t,{default:()=>j});var o=a(3673),s=a(8880),n=a(2323);const r=e=>((0,o.dD)("data-v-45506b2c"),e=e(),(0,o.Cn)(),e),i=r((()=>(0,o._)("div",null,[(0,o._)("h2",null,"Welcome to Folioblocks Credential Receipt Explorer")],-1))),l={class:"search"},c=r((()=>(0,o._)("div",{class:"text-h6"},"Blockchain Statistics",-1))),_=r((()=>(0,o._)("div",{class:"text-subtitle1"}," Some interesting minimal information about the blockchain's current state. ",-1))),d={class:"profile status bg-cyan-2"},u=r((()=>(0,o._)("h4",null,"Blocks",-1))),p={class:"dataheader"},N=r((()=>(0,o._)("h4",null,"Transaction Mapping",-1))),h={class:"dataheader"},E=r((()=>(0,o._)("h4",null,"Transactions",-1))),m={class:"dataheader"},T=r((()=>(0,o._)("h4",null,"Addresses",-1))),I={class:"dataheader"},O={class:"main"},S={class:"row gridblock"},b=r((()=>(0,o._)("h5",null,"Latest Transactions",-1))),f={class:"row"},w=r((()=>(0,o._)("h5",null,"Latest Blocks",-1)));function R(e,t,a,r,R,k){const g=(0,o.up)("q-icon"),C=(0,o.up)("q-input"),x=(0,o.up)("q-form"),A=(0,o.up)("q-card-section"),U=(0,o.up)("q-avatar"),G=(0,o.up)("q-card"),D=(0,o.up)("q-btn"),y=(0,o.up)("router-link"),v=(0,o.up)("q-td"),W=(0,o.up)("q-tr"),L=(0,o.up)("q-table"),z=(0,o.up)("q-page-container"),F=(0,o.up)("q-layout");return(0,o.wg)(),(0,o.j4)(F,{view:"hHh lpR lFf"},{default:(0,o.w5)((()=>[(0,o.Wm)(z,null,{default:(0,o.w5)((()=>[i,(0,o._)("div",l,[(0,o.Wm)(x,{onSubmit:(0,s.iM)(e.onSearchSubmit,["prevent"]),class:"q-gutter-md"},{default:(0,o.w5)((()=>[(0,o.Wm)(C,{class:"searchbar",clearable:"",modelValue:e.searchContext,"onUpdate:modelValue":t[0]||(t[0]=t=>e.searchContext=t),debounce:"500",filled:"",placeholder:"Paste or type something here.",hint:"Search by address, transaction hash, or even by block number."},{append:(0,o.w5)((()=>[(0,o.Wm)(g,{name:"search"})])),_:1},8,["modelValue"])])),_:1},8,["onSubmit"])]),(0,o.Wm)(G,{class:"header"},{default:(0,o.w5)((()=>[(0,o.Wm)(A,null,{default:(0,o.w5)((()=>[c,_])),_:1}),(0,o._)("div",d,[(0,o.Wm)(U,{class:"icon",icon:"view_in_ar"}),(0,o._)("div",null,[u,(0,o._)("p",p,(0,n.zw)(e.n_blocks),1)]),(0,o.Wm)(U,{class:"icon",icon:"mdi-sitemap"}),(0,o._)("div",null,[N,(0,o._)("p",h,(0,n.zw)(e.txs_mapping_count),1)]),(0,o.Wm)(U,{class:"icon",icon:"swap_horiz"}),(0,o._)("div",null,[E,(0,o._)("p",m,(0,n.zw)(e.txs_count),1)]),(0,o.Wm)(U,{class:"icon",icon:"person"}),(0,o._)("div",null,[T,(0,o._)("p",I,(0,n.zw)(e.addresses),1)])])])),_:1}),(0,o._)("div",O,[(0,o._)("div",S,[b,(0,o.Wm)(D,{class:"viewall",rounded:"",color:"accent","text-color":"black",label:"View All",to:"/explorer/transactions"})]),(0,o._)("div",f,[w,(0,o.Wm)(D,{class:"viewall",rounded:"",color:"accent","text-color":"black",label:"View All",to:"/explorer/blocks"})]),(0,o.Wm)(L,{rows:e.transaction_rows,columns:e.transaction_cols,"row-key":"name",loading:e.txs_loading_state,"hide-pagination":!0,"no-data-label":"Failed to fetch from the chain or theres no transactions from chain to render."},{body:(0,o.w5)((e=>[(0,o.Wm)(W,{props:e},{default:(0,o.w5)((()=>[(0,o.Wm)(v,{key:"Transaction Hash",props:e},{default:(0,o.w5)((()=>[(0,o.Wm)(y,{to:"/explorer/transaction/"+e.row.tx_hash,style:{"text-decoration":"none"}},{default:(0,o.w5)((()=>[(0,o.Uk)((0,n.zw)(e.row.tx_hash),1)])),_:2},1032,["to"])])),_:2},1032,["props"]),(0,o.Wm)(v,{key:"To Address",props:e},{default:(0,o.w5)((()=>[(0,o.Wm)(y,{to:"/explorer/address/"+e.row.to_address,style:{"text-decoration":"none"}},{default:(0,o.w5)((()=>[(0,o.Uk)((0,n.zw)(e.row.to_address),1)])),_:2},1032,["to"])])),_:2},1032,["props"]),(0,o.Wm)(v,{key:"Timestamp",props:e},{default:(0,o.w5)((()=>[(0,o.Uk)((0,n.zw)(e.row.timestamp),1)])),_:2},1032,["props"])])),_:2},1032,["props"])])),_:1},8,["rows","columns","loading"]),(0,o.Wm)(L,{rows:e.block_rows,columns:e.block_cols,"row-key":"name",loading:e.blocks_loading_state,"hide-pagination":!0,"no-data-label":"Failed to fetch from the chain or theres no blocks from chain to render."},{body:(0,o.w5)((e=>[(0,o.Wm)(W,{props:e},{default:(0,o.w5)((()=>[(0,o.Wm)(v,{key:"Block ID",props:e},{default:(0,o.w5)((()=>[(0,o.Wm)(y,{to:"/explorer/block/"+e.row.id,style:{"text-decoration":"none"}},{default:(0,o.w5)((()=>[(0,o.Uk)((0,n.zw)(e.row.id),1)])),_:2},1032,["to"])])),_:2},1032,["props"]),(0,o.Wm)(v,{key:"Transaction Count",props:e},{default:(0,o.w5)((()=>[(0,o.Uk)((0,n.zw)(e.row.tx_count),1)])),_:2},1032,["props"]),(0,o.Wm)(v,{key:"Validator",props:e},{default:(0,o.w5)((()=>[(0,o.Wm)(y,{to:"/explorer/address/"+e.row.validator,style:{"text-decoration":"none"}},{default:(0,o.w5)((()=>[(0,o.Uk)((0,n.zw)(e.row.validator),1)])),_:2},1032,["to"])])),_:2},1032,["props"]),(0,o.Wm)(v,{key:"Timestamp",props:e},{default:(0,o.w5)((()=>[(0,o.Uk)((0,n.zw)(e.row.timestamp),1)])),_:2},1032,["props"])])),_:2},1032,["props"])])),_:1},8,["rows","columns","loading"])])])),_:1})])),_:1})}var k=a(1959),g=a(52),C=a.n(g),x=a(2796),A=a(9582);a(2642);const U=[{name:"Block ID",align:"center",label:"Block ID",field:"id",sortable:!0},{name:"Transaction Count",align:"center",label:"Transaction Count",field:"tx_count",sortable:!0},{name:"Validator",align:"center",label:"Validator",field:"validator"},{name:"Timestamp",align:"center",label:"Timestamp",field:"timestamp",sortable:!0}],G=[{name:"Transaction Hash",align:"center",label:"Transaction Hash",field:"tx_hash",style:"width: 50px"},{name:"To Address",align:"center",label:"To Address",field:"to_address"},{name:"Timestamp",align:"center",label:"Timestamp",field:"timestamp",sortable:!0}],D=(0,o.aZ)({name:"ExplorerDashboard",data(){return{n_blocks:(0,k.iH)("—"),txs_mapping_count:(0,k.iH)("—"),txs_count:(0,k.iH)("—"),addresses:(0,k.iH)("—"),txs_loading_state:(0,k.iH)(!0),blocks_loading_state:(0,k.iH)(!0),searchContext:(0,k.iH)("")}},setup(){(0,A.tv)();return{transaction_cols:G,transaction_rows:(0,k.iH)([]),block_cols:U,block_rows:(0,k.iH)([])}},mounted(){this.txs_loading_state=!0,this.blocks_loading_state=!0,this.updateDashboard()},methods:{updateDashboard(){C().get(`${x.sx}/explorer/chain`).then((e=>{this.n_blocks=e.data.node_info.total_blocks,this.txs_mapping_count=e.data.node_info.total_tx_mappings,this.txs_count=e.data.node_info.total_transactions,this.addresses=e.data.node_info.total_addresses,this.transaction_rows=e.data.transactions,this.block_rows=e.data.blocks,this.txs_loading_state=!1,this.blocks_loading_state=!1})).catch((e=>{this.$q.notify({color:"red",position:"top",message:`There was an error when fetching from the chain. Please come back and try again later. Reason: ${e.message}`,Interval:5e3,progress:!0,icon:"mdi-cancel"}),this.txs_loading_state=!1,this.blocks_loading_state=!1}))},onSearchSubmit(){this.searchContext.startsWith("fl:")&&35===this.searchContext.length?this.$router.push({path:`/explorer/address/${this.searchContext}`}):64===this.searchContext.length?this.$router.push({path:`/explorer/transaction/${this.searchContext}`}):Number.isInteger(parseInt(this.searchContext))?this.$router.push({path:`/explorer/block/${this.searchContext}`}):this.$q.notify({color:"red",position:"top",message:"Failed to parse the context given, are you sure this is correct?",timeout:5e3,progress:!0,icon:"mdi-cancel"})}}});var y=a(4260),v=a(9214),W=a(2652),L=a(5269),z=a(4689),F=a(4554),Z=a(151),B=a(5589),q=a(5096),H=a(8240),$=a(3243),Q=a(8186),P=a(3884),V=a(7518),M=a.n(V);const K=(0,y.Z)(D,[["render",R],["__scopeId","data-v-45506b2c"]]),j=K;M()(D,"components",{QLayout:v.Z,QPageContainer:W.Z,QForm:L.Z,QInput:z.Z,QIcon:F.Z,QCard:Z.Z,QCardSection:B.Z,QAvatar:q.Z,QBtn:H.Z,QTable:$.Z,QTr:Q.Z,QTd:P.Z})},2642:()=>{}}]);