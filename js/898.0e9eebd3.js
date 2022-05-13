"use strict";(self["webpackChunkfolioblocks_web"]=self["webpackChunkfolioblocks_web"]||[]).push([[898],{2796:(t,e,n)=>{n.d(e,{$T:()=>_,_u:()=>c,kb:()=>o,sx:()=>a});const a="https://folioblocks.southeastasia.azurecontainer.io",o=100,s=Object.freeze({NODE_GENERAL_CONSENSUS_INIT:1,NODE_GENERAL_REGISTER_INIT:2,NODE_GENERAL_GENESIS_BLOCK_INIT:3,NODE_GENERAL_CONSENSUS_BLOCK_SYNC:4,NODE_GENERAL_CONSENSUS_CONFIRM_NEGOTIATION_START:5,NODE_GENERAL_CONSENSUS_CONCLUDE_NEGOTIATION_PROCESSING:6,INSTITUTION_ORG_GENERATE_STUDENT:7,INSTITUTION_ORG_REFER_NEW_DOCUMENT_OR_IMPORTANT_INFO:8,INSTITUTION_ORG_STUDENT_REFER_EXTRA_INFO:9,ORGANIZATION_USER_REGISTER:10,ORGANIZATION_REFER_EXTRA_INFO:11}),r=Object.freeze({STUDENT_BASE:1,STUDENT_LOG:2,STUDENT_ADDITIONAL:3,ORGANIZATION_BASE:4}),i=Object.freeze({CONSENSUS:1,INIT:2,SYNC:3});function _(t){switch(t){case s.NODE_GENERAL_CONSENSUS_INIT:return"Consensus Initialization";case s.NODE_GENERAL_REGISTER_INIT:return"Node Registration";case s.NODE_GENERAL_GENESIS_BLOCK_INIT:return"Node Genesis Block Creation";case s.NODE_GENERAL_CONSENSUS_BLOCK_SYNC:return"Node Block Sync via Consensus";case s.NODE_GENERAL_CONSENSUS_CONFIRM_NEGOTIATION_START:return"Node Consensus Negotiation Confirmed Start";case s.NODE_GENERAL_CONSENSUS_CONCLUDE_NEGOTIATION_PROCESSING:return"Node Consensus Negotiation Conclusion of Processing";case s.INSTITUTION_ORG_GENERATE_STUDENT:return"Institution Student Generation";case s.INSTITUTION_ORG_REFER_NEW_DOCUMENT_OR_IMPORTANT_INFO:return"Institution New Document / Important Info to Student Reference";case s.INSTITUTION_ORG_STUDENT_REFER_EXTRA_INFO:return"Institution Refer Extra Info to Student";case s.ORGANIZATION_USER_REGISTER:return"Organization Registration";case s.ORGANIZATION_REFER_EXTRA_INFO:return"Extra Info Referral to Organization";default:return"Unidentified Action."}}function c(t){let e=t.hasOwnProperty("content_type")?"User Transaction":"Internal Transaction",n=null;if(t.hasOwnProperty("content_type"))switch(t.content_type){case r.STUDENT_BASE:n="Student Base Portfolio";break;case r.STUDENT_LOG:n="Student Log from Orgs";break;case r.STUDENT_ADDITIONAL:n="Student Additional Info / Remarks";break;case r.ORGANIZATION_BASE:n="Organization Base Registration";break;default:n="Unidentified";break}else switch(t.action){case i.CONSENSUS:n="Internal: Consensus Context";break;case i.INIT:n="Internal: Context Initialization";break;case i.SYNC:n="Internal: Sync from Communication";break;default:n="Unidentified";break}return{identifiedType:e,resolvedTypeValue:n}}},4898:(t,e,n)=>{n.r(e),n.d(e,{default:()=>q});var a=n(3673),o=n(2323);const s=t=>((0,a.dD)("data-v-37cbade9"),t=t(),(0,a.Cn)(),t),r={class:"header"},i={class:"wrap-content"},_=s((()=>(0,a._)("div",{class:"text-h6"},"Transaction Information",-1))),c=s((()=>(0,a._)("div",{class:"text-subtitle1"}," Here contains extra information regarding this transaction. Note that some transaction contents are not decrypt since it may contain some sensitive information. ",-1))),l=(0,a.Uk)(" Action: "),d=(0,a.Uk)("( "),N=(0,a.Uk)(" )"),u=s((()=>(0,a._)("div",{class:"text-h6"},"Payload Context",-1))),E=s((()=>(0,a._)("div",{class:"text-subtitle1"}," The following transaction contains the following elements. ",-1))),T=(0,a.Uk)(" Context Type: "),I=(0,a.Uk)(", classified as "),O={style:{color:"red"}},x=(0,a.Uk)(" Payload: "),h={class:"text-justify",style:{background:"aliceblue"}},p=s((()=>(0,a._)("div",{class:"text-h6"},"Transaction Context Signature",-1))),S=s((()=>(0,a._)("div",{class:"text-subtitle1"},[(0,a.Uk)(" For validity, the following fields shows the hash integrity of the context, both in its "),(0,a._)("code",{style:{color:"red"}},"encrypted"),(0,a.Uk)(" and "),(0,a._)("code",{style:{color:"red"}},"raw"),(0,a.Uk)(" form. Note that, for the case of "),(0,a._)("code",{style:{color:"red"}},"Internal Transaction"),(0,a.Uk)(", you can verify the encrypted hash by encrypting the context provided. For the case of "),(0,a._)("code",{style:{color:"red"}},"External Transaction"),(0,a.Uk)(", you can verify the raw hash by decrypting its context. ")],-1))),f=(0,a.Uk)(" Raw: "),R=(0,a.Uk)(" Encrypted: ");function m(t,e,n,s,m,y){const C=(0,a.up)("q-btn"),g=(0,a.up)("q-separator"),w=(0,a.up)("q-linear-progress"),A=(0,a.up)("q-card-section"),k=(0,a.up)("router-link"),U=(0,a.up)("q-card"),b=(0,a.up)("q-page-container"),G=(0,a.up)("q-layout");return(0,a.wg)(),(0,a.j4)(G,{view:"hHh lpR lFf"},{default:(0,a.w5)((()=>[(0,a.Wm)(b,null,{default:(0,a.w5)((()=>[(0,a._)("div",r,[(0,a.Wm)(C,{class:"back",outline:"",round:"",color:"black",icon:"arrow_back",to:"/explorer/transactions"})]),(0,a.Wm)(g,{color:"black"}),(0,a._)("h5",i,"Details of Transaction Hash "+(0,o.zw)(t.tx_hash),1),(0,a.Wm)(g,{color:"black"}),(0,a.Wm)(U,{class:"my-card wrap-content"},{default:(0,a.w5)((()=>[t.isLoadingContextFinished?(0,a.kq)("",!0):((0,a.wg)(),(0,a.j4)(w,{key:0,query:"",color:"secondary",class:"q-mt-sm"})),(0,a.Wm)(A,null,{default:(0,a.w5)((()=>[_,c])),_:1}),(0,a.Wm)(A,{class:"details"},{default:(0,a.w5)((()=>[(0,a._)("div",null,[(0,a.Wm)(k,{to:"/explorer/block/"+t.at_block,style:{"text-decoration":"none"}},{default:(0,a.w5)((()=>[(0,a._)("p",null,"Block Origin: "+(0,o.zw)(t.at_block),1)])),_:1},8,["to"]),(0,a._)("p",null,[l,(0,a._)("strong",null,(0,o.zw)(t.tx_action),1),(0,a._)("em",null,[d,(0,a._)("strong",null,(0,o.zw)(t.tx_action_number),1),N])]),(0,a.Wm)(k,{to:"/explorer/address/"+t.tx_source_address,style:{"text-decoration":"none"}},{default:(0,a.w5)((()=>[(0,a._)("p",null,"From Address: "+(0,o.zw)(t.tx_source_address),1)])),_:1},8,["to"]),(0,a.Wm)(k,{to:"/explorer/address/"+t.tx_dest_address,style:{"text-decoration":"none"}},{default:(0,a.w5)((()=>[(0,a._)("p",null,"To Address: "+(0,o.zw)(t.tx_dest_address),1)])),_:1},8,["to"]),(0,a._)("p",null,"Timestamp: "+(0,o.zw)(t.tx_timestamp),1)])])),_:1}),(0,a.Wm)(g),(0,a.Wm)(A,null,{default:(0,a.w5)((()=>[u,E])),_:1}),(0,a.Wm)(A,{class:"details"},{default:(0,a.w5)((()=>[(0,a._)("p",null,[T,(0,a._)("strong",null,(0,o.zw)(t.tx_context_type),1),I,(0,a._)("code",O,(0,o.zw)(t.tx_context_type_classification),1)]),(0,a._)("p",null,[x,(0,a._)("code",h,(0,o.zw)(t.tx_literal_context),1)])])),_:1}),(0,a.Wm)(g),(0,a.Wm)(A,null,{default:(0,a.w5)((()=>[p,S])),_:1}),(0,a.Wm)(A,{class:"details"},{default:(0,a.w5)((()=>[(0,a._)("p",null,[f,(0,a._)("code",null,(0,o.zw)(t.tx_context_signature_raw),1)]),(0,a._)("p",null,[R,(0,a._)("code",null,(0,o.zw)(t.tx_context_signature_encrypted),1)])])),_:1})])),_:1})])),_:1})])),_:1})}var y=n(1959),C=n(8825),g=n(52),w=n.n(g),A=n(2796),k=n(9582);const U=(0,a.aZ)({name:"ExplorerTransactionDetails",components:{},setup(){(0,k.yj)(),(0,k.tv)(),(0,C.Z)();return{}},data(){return{at_block:(0,y.iH)("—"),isLoadingContextFinished:(0,y.iH)(!1),tx_hash:(0,y.iH)("—"),tx_action:(0,y.iH)("—"),tx_action_number:(0,y.iH)("—"),tx_source_address:(0,y.iH)("—"),tx_dest_address:(0,y.iH)("—"),tx_timestamp:(0,y.iH)("—"),tx_context_type:(0,y.iH)("—"),tx_context_type_classification:(0,y.iH)("—"),tx_literal_context:(0,y.iH)("—"),tx_context_signature_raw:(0,y.iH)("—"),tx_context_signature_encrypted:(0,y.iH)("—")}},mounted(){this.getTransactionContext()},methods:{getTransactionContext(){this.isLoadingContextFinished=!1,w().get(`${A.sx}/explorer/transaction/${this.$route.params.tx_hash}`).then((t=>{let{identifiedType:e,resolvedTypeValue:n}=(0,A._u)(t.data.transaction.payload);this.at_block=t.data.from_block,this.tx_hash=t.data.transaction.tx_hash,this.tx_action=(0,A.$T)(t.data.transaction.action),this.tx_source_address=t.data.transaction.from_address,this.tx_dest_address=t.data.transaction.to_address,this.tx_timestamp=t.data.transaction.timestamp,this.tx_literal_context=t.data.transaction.payload,this.tx_context_signature_raw=t.data.transaction.signatures.raw,this.tx_context_signature_encrypted=t.data.transaction.signatures.encrypted,this.tx_context_type=n,this.tx_context_type_classification=e,this.isLoadingContextFinished=!0})).catch((t=>{404===t.request.status?(this.$q.notify({color:"red",position:"top",message:"Transactions not found.",timeout:5e3,progress:!0,icon:"mdi-cancel"}),this.$router.push({path:"/explorer/transactions"})):this.$q.notify({color:"red",position:"top",message:`There was an error when fetching from the chain. Please come back and try again later. Reason: ${t.message}`,Interval:1e4,progress:!0,icon:"mdi-cancel"}),this.isLoadingContextFinished=!0}))}}});var b=n(4260),G=n(9214),D=n(2652),L=n(8240),v=n(5869),F=n(151),z=n(1598),W=n(5589),H=n(7518),Z=n.n(H);const B=(0,b.Z)(U,[["render",m],["__scopeId","data-v-37cbade9"]]),q=B;Z()(U,"components",{QLayout:G.Z,QPageContainer:D.Z,QBtn:L.Z,QSeparator:v.Z,QCard:F.Z,QLinearProgress:z.Z,QCardSection:W.Z})}}]);