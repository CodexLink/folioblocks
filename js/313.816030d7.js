"use strict";(self["webpackChunkfolioblocks_web"]=self["webpackChunkfolioblocks_web"]||[]).push([[313],{2796:(e,t,o)=>{o.d(t,{$T:()=>N,_u:()=>E,kb:()=>s,oX:()=>i,sx:()=>a,uK:()=>r});const n="https://",a=`${n}folioblocks.southeastasia.azurecontainer.io`,r=`${n}codexlink.github.io/folioblocks`,s=100,i="otpauth://totp/Organization%20Creator:Folioblocks-Web?secret=MNMDQX32IREXQQLIM4YHMYSYLFUHASCBMJFF63TCMU4UY5TNJBTVMWC7OMWTSQLUNJEVCPJRGZQTOZJTMYYDAOLFMJRGMMJWMVSWCOJWGM2TMOBTHBTGMYZTGMZDOZTDGI2TEOJYGM2DMYRRGE3DCYZVGNRTSYRRMQ3WKNZSGAZDG%3D%3D%3D&issuer=Organization%20Creator",l=Object.freeze({NODE_GENERAL_CONSENSUS_INIT:1,NODE_GENERAL_REGISTER_INIT:2,NODE_GENERAL_GENESIS_BLOCK_INIT:3,NODE_GENERAL_CONSENSUS_BLOCK_SYNC:4,NODE_GENERAL_CONSENSUS_CONFIRM_NEGOTIATION_START:5,NODE_GENERAL_CONSENSUS_CONCLUDE_NEGOTIATION_PROCESSING:6,INSTITUTION_ORG_GENERATE_STUDENT:7,INSTITUTION_ORG_REFER_NEW_DOCUMENT_OR_IMPORTANT_INFO:8,INSTITUTION_ORG_STUDENT_REFER_EXTRA_INFO:9,ORGANIZATION_USER_REGISTER:10,ORGANIZATION_REFER_EXTRA_INFO:11}),c=Object.freeze({STUDENT_BASE:1,STUDENT_LOG:2,STUDENT_ADDITIONAL:3,ORGANIZATION_BASE:4}),_=Object.freeze({CONSENSUS:1,INIT:2,SYNC:3});function N(e){switch(e){case l.NODE_GENERAL_CONSENSUS_INIT:return"Consensus Initialization";case l.NODE_GENERAL_REGISTER_INIT:return"Node Registration";case l.NODE_GENERAL_GENESIS_BLOCK_INIT:return"Node Genesis Block Creation";case l.NODE_GENERAL_CONSENSUS_BLOCK_SYNC:return"Node Block Sync via Consensus";case l.NODE_GENERAL_CONSENSUS_CONFIRM_NEGOTIATION_START:return"Node Consensus Negotiation Confirmed Start";case l.NODE_GENERAL_CONSENSUS_CONCLUDE_NEGOTIATION_PROCESSING:return"Node Consensus Negotiation Conclusion of Processing";case l.INSTITUTION_ORG_GENERATE_STUDENT:return"Institution Student Generation";case l.INSTITUTION_ORG_REFER_NEW_DOCUMENT_OR_IMPORTANT_INFO:return"Institution New Document / Important Info to Student Reference";case l.INSTITUTION_ORG_STUDENT_REFER_EXTRA_INFO:return"Institution Refer Extra Info to Student";case l.ORGANIZATION_USER_REGISTER:return"Organization Registration";case l.ORGANIZATION_REFER_EXTRA_INFO:return"Extra Info Referral to Organization";default:return"Unidentified Action."}}function E(e){let t=e.hasOwnProperty("content_type")?"User Transaction":"Internal Transaction",o=null;if(e.hasOwnProperty("content_type"))switch(e.content_type){case c.STUDENT_BASE:o="Student Base Portfolio";break;case c.STUDENT_LOG:o="Student Log from Orgs";break;case c.STUDENT_ADDITIONAL:o="Student Additional Info / Remarks";break;case c.ORGANIZATION_BASE:o="Organization Base Registration";break;default:o="Unidentified";break}else switch(e.action){case _.CONSENSUS:o="Internal: Consensus Context";break;case _.INIT:o="Internal: Context Initialization";break;case _.SYNC:o="Internal: Sync from Communication";break;default:o="Unidentified";break}return{identifiedType:t,resolvedTypeValue:o}}},6313:(e,t,o)=>{o.r(t),o.d(t,{default:()=>A});var n=o(3673),a=o(2323);const r=e=>((0,n.dD)("data-v-1d3f5b32"),e=e(),(0,n.Cn)(),e),s={class:"header"},i=r((()=>(0,n._)("h5",null,"Blocks",-1))),l={class:"q-pa-md"};function c(e,t,o,r,c,_){const N=(0,n.up)("q-btn"),E=(0,n.up)("q-separator"),T=(0,n.up)("router-link"),O=(0,n.up)("q-td"),I=(0,n.up)("q-tr"),d=(0,n.up)("q-table"),u=(0,n.up)("q-page-container"),S=(0,n.up)("q-layout");return(0,n.wg)(),(0,n.j4)(S,{view:"hHh lpR lFf"},{default:(0,n.w5)((()=>[(0,n.Wm)(u,null,{default:(0,n.w5)((()=>[(0,n._)("div",s,[(0,n.Wm)(N,{class:"back",outline:"",round:"",color:"black",icon:"arrow_back",to:"/explorer"})]),(0,n.Wm)(E,{color:"black"}),i,(0,n.Wm)(E,{color:"black"}),(0,n._)("div",l,[(0,n.Wm)(d,{rows:e.block_rows,columns:e.block_cols,"row-key":"id",loading:e.block_loading_state,"rows-per-page-options":[e.default_block_rows],"no-data-label":"Failed to fetch from the chain or theres no blocks from chain to render."},{"top-right":(0,n.w5)((()=>[(0,n.Wm)(N,{color:"green","icon-right":"refresh",label:"Refresh","no-caps":"",onClick:e.getBlocks},null,8,["onClick"])])),body:(0,n.w5)((e=>[(0,n.Wm)(I,{props:e},{default:(0,n.w5)((()=>[(0,n.Wm)(O,{key:"Block ID",props:e},{default:(0,n.w5)((()=>[(0,n.Wm)(T,{to:"/explorer/block/"+e.row.id,style:{"text-decoration":"none"}},{default:(0,n.w5)((()=>[(0,n.Uk)((0,a.zw)(e.row.id),1)])),_:2},1032,["to"])])),_:2},1032,["props"]),(0,n.Wm)(O,{key:"Block Content Byte Size",props:e},{default:(0,n.w5)((()=>[(0,n.Uk)((0,a.zw)(e.row.content_bytes_size),1)])),_:2},1032,["props"]),(0,n.Wm)(O,{key:"Transaction Count",props:e},{default:(0,n.w5)((()=>[(0,n.Uk)((0,a.zw)(e.row.tx_count),1)])),_:2},1032,["props"]),(0,n.Wm)(O,{key:"Validator",props:e},{default:(0,n.w5)((()=>[(0,n.Wm)(T,{to:"/explorer/address/"+e.row.validator,style:{"text-decoration":"none"}},{default:(0,n.w5)((()=>[(0,n.Uk)((0,a.zw)(e.row.validator),1)])),_:2},1032,["to"])])),_:2},1032,["props"]),(0,n.Wm)(O,{key:"Timestamp",props:e},{default:(0,n.w5)((()=>[(0,n.Uk)((0,a.zw)(e.row.timestamp),1)])),_:2},1032,["props"])])),_:2},1032,["props"])])),_:1},8,["rows","columns","loading","rows-per-page-options"])])])),_:1})])),_:1})}o(71);var _=o(1959),N=o(52),E=o.n(N),T=o(2796);const O=[{name:"Block ID",align:"center",label:"Block ID",field:"id",sortable:!0},{name:"Block Content Byte Size",align:"center",label:"Block Content Byte Size",field:"content_bytes_size",sortable:!0},{name:"Transaction Count",align:"center",label:"Transaction Count",field:"tx_count",sortable:!0},{name:"Validator",align:"center",label:"Validator",field:"validator"},{name:"Timestamp",align:"center",label:"Timestamp",field:"timestamp",sortable:!0}],I=(0,n.aZ)({name:"ExplorerTransaction",components:{},data(){return{block_loading_state:(0,_.iH)(!1),first_instance:(0,_.iH)(!0)}},setup(){return{block_cols:O,block_rows:(0,_.iH)([]),default_block_rows:(0,_.iH)(T.kb)}},mounted(){this.getBlocks()},methods:{getBlocks(){this.block_loading_state=!0,E().get(`${T.sx}/explorer/blocks`).then((e=>{let t=[];for(let o of e.data)o.action=(0,T.$T)(o.action),t.push(o);this.block_rows=t,this.block_loading_state=!1,this.first_instance||this.$q.notify({color:"green",position:"top",message:"Blocks has been updated.",timeout:5e3,progress:!0,icon:"mdi-account-check"}),this.first_instance=!1})).catch((e=>{this.$q.notify({color:"red",position:"top",message:`Failed to fetch transactions from the server. Please try again later. Reason: ${e.message}`,timeout:5e3,progress:!0,icon:"mdi-cancel"}),this.block_loading_state=!1}))}}});var d=o(4260),u=o(9214),S=o(2652),p=o(8240),R=o(5869),k=o(3243),f=o(8186),b=o(3884),C=o(7518),m=o.n(C);const G=(0,d.Z)(I,[["render",c],["__scopeId","data-v-1d3f5b32"]]),A=G;m()(I,"components",{QLayout:u.Z,QPageContainer:S.Z,QBtn:p.Z,QSeparator:R.Z,QTable:k.Z,QTr:f.Z,QTd:b.Z})}}]);