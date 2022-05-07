"use strict";(self["webpackChunkfolioblocks"]=self["webpackChunkfolioblocks"]||[]).push([[532],{2796:(e,t,o)=>{o.d(t,{$T:()=>c,_u:()=>d,kb:()=>r,mX:()=>n});const a=process.env.TARGET_MASTER_NODE_ADDRESS,s=process.env.TARGET_MASTER_NODE_PORT,n=`${a}:${s}`,r=100,i=Object.freeze({NODE_GENERAL_CONSENSUS_INIT:1,NODE_GENERAL_REGISTER_INIT:2,NODE_GENERAL_GENESIS_BLOCK_INIT:3,NODE_GENERAL_CONSENSUS_BLOCK_SYNC:4,NODE_GENERAL_CONSENSUS_CONFIRM_NEGOTIATION_START:5,NODE_GENERAL_CONSENSUS_CONCLUDE_NEGOTIATION_PROCESSING:6,INSTITUTION_ORG_GENERATE_STUDENT:7,INSTITUTION_ORG_REFER_NEW_DOCUMENT_OR_IMPORTANT_INFO:8,INSTITUTION_ORG_STUDENT_REFER_EXTRA_INFO:9,ORGANIZATION_USER_REGISTER:10,ORGANIZATION_REFER_EXTRA_INFO:11}),_=Object.freeze({STUDENT_BASE:1,STUDENT_LOG:2,STUDENT_ADDITIONAL:3,ORGANIZATION_BASE:4}),l=Object.freeze({CONSENSUS:1,INIT:2,SYNC:3});function c(e){switch(e){case i.NODE_GENERAL_CONSENSUS_INIT:return"Consensus Initialization";case i.NODE_GENERAL_REGISTER_INIT:return"Node Registration";case i.NODE_GENERAL_GENESIS_BLOCK_INIT:return"Node Genesis Block Creation";case i.NODE_GENERAL_CONSENSUS_BLOCK_SYNC:return"Node Block Sync via Consensus";case i.NODE_GENERAL_CONSENSUS_CONFIRM_NEGOTIATION_START:return"Node Consensus Negotiation Confirmed Start";case i.NODE_GENERAL_CONSENSUS_CONCLUDE_NEGOTIATION_PROCESSING:return"Node Consensus Negotiation Conclusion of Processing";case i.INSTITUTION_ORG_GENERATE_STUDENT:return"Institution Student Generation";case i.INSTITUTION_ORG_REFER_NEW_DOCUMENT_OR_IMPORTANT_INFO:return"Institution New Document / Important Info to Student Reference";case i.INSTITUTION_ORG_STUDENT_REFER_EXTRA_INFO:return"Institution Refer Extra Info to Student";case i.ORGANIZATION_USER_REGISTER:return"Organization Registration";case i.ORGANIZATION_REFER_EXTRA_INFO:return"Extra Info Referral to Organization";default:return"Unidentified Action."}}function d(e){let t=e.hasOwnProperty("content_type")?"User Transaction":"Internal Transaction",o=null;if(e.hasOwnProperty("content_type"))switch(e.content_type){case _.STUDENT_BASE:o="Student Base Portfolio";break;case _.STUDENT_LOG:o="Student Log from Orgs";break;case _.STUDENT_ADDITIONAL:o="Student Additional Info / Remarks";break;case _.ORGANIZATION_BASE:o="Organization Base Registration";break;default:o="Unidentified";break}else switch(e.action){case l.CONSENSUS:o="Internal: Consensus Context";break;case l.INIT:o="Internal: Context Initialization";break;case l.SYNC:o="Internal: Sync from Communication";break;default:o="Unidentified";break}return{identifiedType:t,resolvedTypeValue:o}}},532:(e,t,o)=>{o.r(t),o.d(t,{default:()=>y});var a=o(3673),s=o(2323);const n=e=>((0,a.dD)("data-v-32d407b2"),e=e(),(0,a.Cn)(),e),r={class:"header"},i=n((()=>(0,a._)("div",{class:"text-h6"},"Block Information",-1))),_=n((()=>(0,a._)("div",{class:"text-subtitle1"}," Here contains extra information regarding this block. ",-1))),l=(0,a.Uk)(" Hash Block: "),c=(0,a.Uk)(" Validator: "),d={class:"q-pa-md my-card"};function N(e,t,o,n,N,E){const T=(0,a.up)("q-btn"),p=(0,a.up)("q-separator"),u=(0,a.up)("q-linear-progress"),I=(0,a.up)("q-card-section"),O=(0,a.up)("router-link"),m=(0,a.up)("q-card"),S=(0,a.up)("q-td"),f=(0,a.up)("q-tr"),R=(0,a.up)("q-table"),h=(0,a.up)("q-page-container"),k=(0,a.up)("q-layout");return(0,a.wg)(),(0,a.j4)(k,{view:"hHh lpR lFf"},{default:(0,a.w5)((()=>[(0,a.Wm)(h,null,{default:(0,a.w5)((()=>[(0,a._)("div",r,[(0,a.Wm)(T,{class:"back",outline:"",round:"",color:"black",icon:"arrow_back",to:"/explorer/blocks"})]),(0,a.Wm)(p,{color:"black"}),(0,a._)("h5",null,"Block #"+(0,s.zw)(e.nth_block),1),(0,a.Wm)(p,{color:"black"}),(0,a.Wm)(m,{class:"my-card wrapped-content"},{default:(0,a.w5)((()=>[e.associated_tx_loading_state?((0,a.wg)(),(0,a.j4)(u,{key:0,query:"",color:"secondary",class:"q-mt-sm"})):(0,a.kq)("",!0),(0,a.Wm)(I,null,{default:(0,a.w5)((()=>[i,_])),_:1}),(0,a.Wm)(I,{class:"details"},{default:(0,a.w5)((()=>[(0,a._)("div",null,[(0,a._)("p",null,[l,(0,a._)("strong",null,(0,s.zw)(e.hash_block_ref),1)]),(0,a._)("p",null,"Prev Hash Block: "+(0,s.zw)(e.prev_hash_block_ref),1),(0,a._)("p",null,"Nonce: "+(0,s.zw)(e.calc_nonce),1),(0,a._)("p",null,"Content Bytes: "+(0,s.zw)(e.block_content_size),1),(0,a.Wm)(O,{to:"/explorer/address/"+e.validator,style:{"text-decoration":"none"}},{default:(0,a.w5)((()=>[(0,a._)("p",null,[c,(0,a._)("strong",null,(0,s.zw)(e.validator),1)])])),_:1},8,["to"]),(0,a._)("p",null,"Timestamp: "+(0,s.zw)(e.timestamp),1)])])),_:1})])),_:1}),(0,a._)("div",d,[(0,a.Wm)(R,{rows:e.tx_rows,columns:e.tx_cols,"row-key":"id",loading:e.associated_tx_loading_state,"rows-per-page-options":[e.default_tx_rows],title:"Associated Transactions","no-data-label":"No associated transactions from this block, or failed to fetch data from the chain."},{body:(0,a.w5)((e=>[(0,a.Wm)(f,{props:e},{default:(0,a.w5)((()=>[(0,a.Wm)(S,{key:"Transaction Number",props:e},{default:(0,a.w5)((()=>[(0,a.Uk)((0,s.zw)(e.row.id),1)])),_:2},1032,["props"]),(0,a.Wm)(S,{key:"Transaction Hash",props:e},{default:(0,a.w5)((()=>[(0,a.Wm)(O,{to:"/explorer/transaction/"+e.row.tx_hash,style:{"text-decoration":"none"}},{default:(0,a.w5)((()=>[(0,a.Uk)((0,s.zw)(e.row.tx_hash),1)])),_:2},1032,["to"])])),_:2},1032,["props"]),(0,a.Wm)(S,{key:"Transaction Action",props:e},{default:(0,a.w5)((()=>[(0,a.Uk)((0,s.zw)(e.row.action),1)])),_:2},1032,["props"]),(0,a.Wm)(S,{key:"From Address",props:e},{default:(0,a.w5)((()=>[(0,a.Wm)(O,{to:"/explorer/address/"+e.row.from_address,style:{"text-decoration":"none"}},{default:(0,a.w5)((()=>[(0,a.Uk)((0,s.zw)(e.row.from_address),1)])),_:2},1032,["to"])])),_:2},1032,["props"]),(0,a.Wm)(S,{key:"To Address",props:e},{default:(0,a.w5)((()=>[(0,a.Wm)(O,{to:"/explorer/address/"+e.row.to_address,style:{"text-decoration":"none"}},{default:(0,a.w5)((()=>[(0,a.Uk)((0,s.zw)(e.row.to_address),1)])),_:2},1032,["to"])])),_:2},1032,["props"]),(0,a.Wm)(S,{key:"Timestamp",props:e},{default:(0,a.w5)((()=>[(0,a.Uk)((0,s.zw)(e.row.timestamp),1)])),_:2},1032,["props"])])),_:2},1032,["props"])])),_:1},8,["rows","columns","loading","rows-per-page-options"])])])),_:1})])),_:1})}o(71);var E=o(1959),T=o(52),p=o.n(T),u=o(2796),I=o(9582);const O=[{name:"Transaction Hash",align:"center",label:"Transaction Hash",field:"tx_hash",required:!0,sortable:!0},{name:"Transaction Action",align:"center",label:"Action",field:"action",sortable:!0},{name:"From Address",align:"center",label:"From Address",field:"from_address",sortable:!0},{name:"To Address",align:"center",label:"To Address",field:"to_address",sortable:!0},{name:"Timestamp",align:"center",label:"Timestamp",field:"timestamp",sortable:!0}],m=(0,a.aZ)({name:"ExplorerBlockDetails",components:{},data(){return{nth_block:(0,E.iH)("—"),block_content_size:(0,E.iH)("—"),hash_block_ref:(0,E.iH)("—"),prev_hash_block_ref:(0,E.iH)("—"),calc_nonce:(0,E.iH)("—"),validator:(0,E.iH)("—"),timestamp:(0,E.iH)("—"),associated_tx_loading_state:(0,E.iH)(!0),default_tx_rows:(0,E.iH)(u.kb)}},setup(){(0,I.yj)(),(0,I.tv)();return{tx_cols:O,tx_rows:(0,E.iH)([])}},mounted(){this.getBlockContext()},methods:{getBlockContext(){this.associated_tx_loading_state=!0,p().get(`http://${u.mX}/explorer/block/${this.$route.params.id}`).then((e=>{this.nth_block=e.data.id,this.block_content_size=e.data.content_bytes_size,this.hash_block_ref=e.data.hash_block,this.prev_hash_block_ref=e.data.prev_hash_block,this.calc_nonce=e.data.contents.nonce,this.validator=e.data.contents.validator,this.timestamp=e.data.contents.timestamp;let t=[];for(let o of e.data.contents.transactions)o.action=(0,u.$T)(o.action),t.push(o);this.tx_rows=t.reverse(),this.associated_tx_loading_state=!1})).catch((e=>{404===e.request.status?(this.$q.notify({color:"red",position:"top",message:"Block not found.",timeout:5e3,progress:!0,icon:"mdi-cancel"}),this.$router.push({path:"/explorer/blocks"})):(this.$q.notify({color:"red",position:"top",message:`Failed to fetch block context from the chain, please try again later. Reason: ${e.message}`,timeout:1e4,progress:!0,icon:"mdi-cancel"}),this.associated_tx_loading_state=!1)}))}}});var S=o(4260),f=o(9214),R=o(2652),h=o(8240),k=o(5869),b=o(151),A=o(1598),w=o(5589),C=o(3243),g=o(8186),G=o(3884),U=o(7518),x=o.n(U);const D=(0,S.Z)(m,[["render",N],["__scopeId","data-v-32d407b2"]]),y=D;x()(m,"components",{QLayout:f.Z,QPageContainer:R.Z,QBtn:h.Z,QSeparator:k.Z,QCard:b.Z,QLinearProgress:A.Z,QCardSection:w.Z,QTable:C.Z,QTr:g.Z,QTd:G.Z})}}]);