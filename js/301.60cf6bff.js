"use strict";(self["webpackChunkfolioblocks"]=self["webpackChunkfolioblocks"]||[]).push([[301],{2796:(e,t,s)=>{s.d(t,{$T:()=>c,_u:()=>l,kb:()=>i,mX:()=>n});const a="127.0.0.1",o=6001,n=`${a}:${o}`,i=100,r=Object.freeze({NODE_GENERAL_CONSENSUS_INIT:1,NODE_GENERAL_REGISTER_INIT:2,NODE_GENERAL_GENESIS_BLOCK_INIT:3,NODE_GENERAL_CONSENSUS_BLOCK_SYNC:4,NODE_GENERAL_CONSENSUS_CONFIRM_NEGOTIATION_START:5,NODE_GENERAL_CONSENSUS_CONCLUDE_NEGOTIATION_PROCESSING:6,INSTITUTION_ORG_GENERATE_STUDENT:7,INSTITUTION_ORG_REFER_NEW_DOCUMENT_OR_IMPORTANT_INFO:8,INSTITUTION_ORG_STUDENT_REFER_EXTRA_INFO:9,ORGANIZATION_USER_REGISTER:10,ORGANIZATION_REFER_EXTRA_INFO:11}),_=Object.freeze({STUDENT_BASE:1,STUDENT_LOG:2,STUDENT_ADDITIONAL:3,ORGANIZATION_BASE:4}),d=Object.freeze({CONSENSUS:1,INIT:2,SYNC:3});function c(e){switch(e){case r.NODE_GENERAL_CONSENSUS_INIT:return"Consensus Initialization";case r.NODE_GENERAL_REGISTER_INIT:return"Node Registration";case r.NODE_GENERAL_GENESIS_BLOCK_INIT:return"Node Genesis Block Creation";case r.NODE_GENERAL_CONSENSUS_BLOCK_SYNC:return"Node Block Sync via Consensus";case r.NODE_GENERAL_CONSENSUS_CONFIRM_NEGOTIATION_START:return"Node Consensus Negotiation Confirmed Start";case r.NODE_GENERAL_CONSENSUS_CONCLUDE_NEGOTIATION_PROCESSING:return"Node Consensus Negotiation Conclusion of Processing";case r.INSTITUTION_ORG_GENERATE_STUDENT:return"Institution Student Generation";case r.INSTITUTION_ORG_REFER_NEW_DOCUMENT_OR_IMPORTANT_INFO:return"Institution New Document / Important Info to Student Reference";case r.INSTITUTION_ORG_STUDENT_REFER_EXTRA_INFO:return"Institution Refer Extra Info to Student";case r.ORGANIZATION_USER_REGISTER:return"Organization Registration";case r.ORGANIZATION_REFER_EXTRA_INFO:return"Extra Info Referral to Organization";default:return"Unidentified Action."}}function l(e){let t=e.hasOwnProperty("content_type")?"User Transaction":"Internal Transaction",s=null;if(e.hasOwnProperty("content_type"))switch(e.content_type){case _.STUDENT_BASE:s="Student Base Portfolio";break;case _.STUDENT_LOG:s="Student Log from Orgs";break;case _.STUDENT_ADDITIONAL:s="Student Additional Info / Remarks";break;case _.ORGANIZATION_BASE:s="Organization Base Registration";break;default:s="Unidentified";break}else switch(e.action){case d.CONSENSUS:s="Internal: Consensus Context";break;case d.INIT:s="Internal: Context Initialization";break;case d.SYNC:s="Internal: Sync from Communication";break;default:s="Unidentified";break}return{identifiedType:t,resolvedTypeValue:s}}},3301:(e,t,s)=>{s.r(t),s.d(t,{default:()=>q});var a=s(3673),o=s(2323);const n={class:"first-header"},i={class:"second-header wrap-content"},r={style:{"line-height":"initial"}},_={style:{"line-height":"initial"}},d={key:0},c={key:1},l={key:0},N={key:1},u={key:2},E={class:"q-pa-md table"};function T(e,t,s,T,p,I){const O=(0,a.up)("q-btn"),S=(0,a.up)("q-linear-progress"),R=(0,a.up)("q-card-section"),m=(0,a.up)("q-card"),A=(0,a.up)("q-td"),f=(0,a.up)("router-link"),w=(0,a.up)("q-tr"),g=(0,a.up)("q-table"),h=(0,a.up)("q-page-container"),C=(0,a.up)("q-layout");return(0,a.wg)(),(0,a.j4)(C,{view:"hHh lpR lFf"},{default:(0,a.w5)((()=>[(0,a.Wm)(h,null,{default:(0,a.w5)((()=>[(0,a._)("div",n,[(0,a.Wm)(O,{color:"secondary",label:"Go back",rounded:"",icon:"arrow_back",to:"/explorer/addresses"})]),(0,a._)("div",i,[(0,a._)("div",null,[(0,a._)("h3",r,(0,o.zw)(e.user_address),1),(0,a._)("p",_,[e.association_address?((0,a.wg)(),(0,a.iD)("div",d,[(0,a.Uk)(" Association Context: "+(0,o.zw)(e.association_address)+" | ",1),(0,a._)("strong",null,(0,o.zw)(e.association_context),1)])):((0,a.wg)(),(0,a.iD)("div",c," No Association. "))])])]),(0,a._)("div",null,[(0,a.Wm)(m,{class:"my-card wrap-content"},{default:(0,a.w5)((()=>[e.associated_tx_loading_state?((0,a.wg)(),(0,a.j4)(S,{key:0,query:"",color:"secondary",class:"q-mt-sm"})):(0,a.kq)("",!0),(0,a.Wm)(R,{class:"details"},{default:(0,a.w5)((()=>[(0,a._)("p",null,"User Type: "+(0,o.zw)(e.user_type),1),e.tx_bindings?((0,a.wg)(),(0,a.iD)("p",l,"Transaction Bindings: "+(0,o.zw)(e.tx_bindings),1)):(0,a.kq)("",!0),e.negotiations?((0,a.wg)(),(0,a.iD)("p",N,"Consensus Negotiations: "+(0,o.zw)(e.negotiations),1)):(0,a.kq)("",!0),e.description?((0,a.wg)(),(0,a.iD)("p",u,"Description: "+(0,o.zw)(e.description),1)):(0,a.kq)("",!0)])),_:1})])),_:1})]),(0,a._)("div",E,[(0,a.Wm)(g,{rows:e.tx_rows,columns:e.tx_cols,loading:e.associated_tx_loading_state,title:"Associated Transactions","row-key":"name"},{body:(0,a.w5)((e=>[(0,a.Wm)(w,{props:e},{default:(0,a.w5)((()=>[(0,a.Wm)(A,{key:"Transaction Number",props:e},{default:(0,a.w5)((()=>[(0,a.Uk)((0,o.zw)(e.row.id),1)])),_:2},1032,["props"]),(0,a.Wm)(A,{key:"Transaction Hash",props:e},{default:(0,a.w5)((()=>[(0,a.Wm)(f,{to:"/explorer/transaction/"+e.row.tx_hash,style:{"text-decoration":"none"}},{default:(0,a.w5)((()=>[(0,a.Uk)((0,o.zw)(e.row.tx_hash),1)])),_:2},1032,["to"])])),_:2},1032,["props"]),(0,a.Wm)(A,{key:"Transaction Action",props:e},{default:(0,a.w5)((()=>[(0,a.Uk)((0,o.zw)(e.row.action),1)])),_:2},1032,["props"]),(0,a.Wm)(A,{key:"From Address",props:e},{default:(0,a.w5)((()=>[(0,a.Wm)(f,{to:"/explorer/address/"+e.row.from_address,style:{"text-decoration":"none"}},{default:(0,a.w5)((()=>[(0,a.Uk)((0,o.zw)(e.row.from_address),1)])),_:2},1032,["to"])])),_:2},1032,["props"]),(0,a.Wm)(A,{key:"To Address",props:e},{default:(0,a.w5)((()=>[(0,a.Wm)(f,{to:"/explorer/address/"+e.row.to_address,style:{"text-decoration":"none"}},{default:(0,a.w5)((()=>[(0,a.Uk)((0,o.zw)(e.row.to_address),1)])),_:2},1032,["to"])])),_:2},1032,["props"]),(0,a.Wm)(A,{key:"Timestamp",props:e},{default:(0,a.w5)((()=>[(0,a.Uk)((0,o.zw)(e.row.timestamp),1)])),_:2},1032,["props"])])),_:2},1032,["props"])])),_:1},8,["rows","columns","loading"])])])),_:1})])),_:1})}s(71);var p=s(1959),I=s(8825),O=s(52),S=s.n(O),R=s(2796),m=s(9582);const A=[{name:"Transaction Hash",align:"center",label:"Transaction Hash",field:"tx_hash",required:!0,sortable:!0},{name:"Transaction Action",align:"center",label:"Action",field:"action",sortable:!0},{name:"From Address",align:"center",label:"From Address",field:"from_address",sortable:!0},{name:"To Address",align:"center",label:"To Address",field:"to_address",sortable:!0},{name:"Timestamp",align:"center",label:"Timestamp",field:"timestamp",sortable:!0}],f=(0,a.aZ)({name:"ExplorerAccountDetails",components:{},data(){return{tx_rows:(0,p.iH)([]),associated_tx_loading_state:(0,p.iH)(!0),user_name:(0,p.iH)("—"),user_address:(0,p.iH)("—"),association_context:(0,p.iH)("—"),association_address:(0,p.iH)("—"),description:(0,p.iH)("—"),negotiations:(0,p.iH)("—"),tx_bindings:(0,p.iH)("—"),user_type:(0,p.iH)("—")}},setup(){(0,m.yj)(),(0,m.tv)(),(0,I.Z)();return{tx_cols:A}},methods:{getAddressContext(){this.associated_tx_loading_state=!0,S().get(`http://${R.mX}/explorer/address/${this.$route.params.uuid}`).then((e=>{this.user_address=e.data.uuid,this.association_address=e.data.association_uuid,this.user_type=e.data.entity_type,this.tx_bindings=e.data.tx_bindings_count,this.negotiations=e.data.negotiations_count,this.description=e.data.description,this.association_context=e.data.association_name;let t=[],s=1;for(let a of e.data.related_txs)a.action=(0,R.$T)(a.action),a.id=s,s+=1,t.push(a);this.tx_rows=t.reverse(),this.associated_tx_loading_state=!1})).catch((e=>{404===e.request.status?(this.$q.notify({color:"red",position:"top",message:"Address not found.",timeout:5e3,progress:!0,icon:"mdi-cancel"}),this.$router.push({path:"/explorer/addresses"})):(this.$q.notify({color:"red",position:"top",message:`Failed to fetch block context from the chain, please try again later. Reason: ${e.message}`,timeout:1e4,progress:!0,icon:"mdi-cancel"}),this.associated_tx_loading_state=!1)}))}},mounted(){this.getAddressContext()}});var w=s(4260),g=s(9214),h=s(2652),C=s(8240),k=s(151),y=s(1598),U=s(5589),G=s(3243),b=s(8186),x=s(3884),D=s(7518),L=s.n(D);const z=(0,w.Z)(f,[["render",T],["__scopeId","data-v-960d698a"]]),q=z;L()(f,"components",{QLayout:g.Z,QPageContainer:h.Z,QBtn:C.Z,QCard:k.Z,QLinearProgress:y.Z,QCardSection:U.Z,QTable:G.Z,QTr:b.Z,QTd:x.Z})}}]);