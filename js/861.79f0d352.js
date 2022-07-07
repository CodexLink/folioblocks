"use strict";(self["webpackChunkfolioblocks_web"]=self["webpackChunkfolioblocks_web"]||[]).push([[861],{2796:(e,s,t)=>{t.d(s,{$T:()=>N,_u:()=>c,kb:()=>r,oX:()=>i,sx:()=>n,uK:()=>a});const o="https://",n=`${o}folioblocks.southeastasia.azurecontainer.io`,a=`${o}codexlink.github.io/folioblocks`,r=100,i="otpauth://totp/Organization%20Creator:Folioblocks-Web?secret=MNMDQX32IREXQQLIM4YHMYSYLFUHASCBMJFF63TCMU4UY5TNJBTVMWC7OMWTSQLUNJEVCPJRGZQTOZJTMYYDAOLFMJRGMMJWMVSWCOJWGM2TMOBTHBTGMYZTGMZDOZTDGI2TEOJYGM2DMYRRGE3DCYZVGNRTSYRRMQ3WKNZSGAZDG%3D%3D%3D&issuer=Organization%20Creator",d=Object.freeze({NODE_GENERAL_CONSENSUS_INIT:1,NODE_GENERAL_REGISTER_INIT:2,NODE_GENERAL_GENESIS_BLOCK_INIT:3,NODE_GENERAL_CONSENSUS_BLOCK_SYNC:4,NODE_GENERAL_CONSENSUS_CONFIRM_NEGOTIATION_START:5,NODE_GENERAL_CONSENSUS_CONCLUDE_NEGOTIATION_PROCESSING:6,INSTITUTION_ORG_GENERATE_STUDENT:7,INSTITUTION_ORG_REFER_NEW_DOCUMENT_OR_IMPORTANT_INFO:8,INSTITUTION_ORG_STUDENT_REFER_EXTRA_INFO:9,ORGANIZATION_USER_REGISTER:10,ORGANIZATION_REFER_EXTRA_INFO:11}),_=Object.freeze({STUDENT_BASE:1,STUDENT_LOG:2,STUDENT_ADDITIONAL:3,ORGANIZATION_BASE:4}),l=Object.freeze({CONSENSUS:1,INIT:2,SYNC:3});function N(e){switch(e){case d.NODE_GENERAL_CONSENSUS_INIT:return"Consensus Initialization";case d.NODE_GENERAL_REGISTER_INIT:return"Node Registration";case d.NODE_GENERAL_GENESIS_BLOCK_INIT:return"Node Genesis Block Creation";case d.NODE_GENERAL_CONSENSUS_BLOCK_SYNC:return"Node Block Sync via Consensus";case d.NODE_GENERAL_CONSENSUS_CONFIRM_NEGOTIATION_START:return"Node Consensus Negotiation Confirmed Start";case d.NODE_GENERAL_CONSENSUS_CONCLUDE_NEGOTIATION_PROCESSING:return"Node Consensus Negotiation Conclusion of Processing";case d.INSTITUTION_ORG_GENERATE_STUDENT:return"Institution Student Generation";case d.INSTITUTION_ORG_REFER_NEW_DOCUMENT_OR_IMPORTANT_INFO:return"Institution New Document / Important Info to Student Reference";case d.INSTITUTION_ORG_STUDENT_REFER_EXTRA_INFO:return"Institution Refer Extra Info to Student";case d.ORGANIZATION_USER_REGISTER:return"Organization Registration";case d.ORGANIZATION_REFER_EXTRA_INFO:return"Extra Info Referral to Organization";default:return"Unidentified Action."}}function c(e){let s=e.hasOwnProperty("content_type")?"User Transaction":"Internal Transaction",t=null;if(e.hasOwnProperty("content_type"))switch(e.content_type){case _.STUDENT_BASE:t="Student Base Portfolio";break;case _.STUDENT_LOG:t="Student Log from Orgs";break;case _.STUDENT_ADDITIONAL:t="Student Additional Info / Remarks";break;case _.ORGANIZATION_BASE:t="Organization Base Registration";break;default:t="Unidentified";break}else switch(e.action){case l.CONSENSUS:t="Internal: Consensus Context";break;case l.INIT:t="Internal: Context Initialization";break;case l.SYNC:t="Internal: Sync from Communication";break;default:t="Unidentified";break}return{identifiedType:s,resolvedTypeValue:t}}},3861:(e,s,t)=>{t.r(s),t.d(s,{default:()=>k});var o=t(3673),n=t(2323);const a=e=>((0,o.dD)("data-v-63649940"),e=e(),(0,o.Cn)(),e),r={class:"header"},i=a((()=>(0,o._)("h5",null,"Addresses",-1))),d={class:"q-pa-md"},_={class:"disabled"},l=(0,o.Uk)(" Association addresses cannot be viewed in detail due to its minimal information. Please check the user addresses context to find more information about this association / organization. ");function N(e,s,t,a,N,c){const u=(0,o.up)("q-btn"),E=(0,o.up)("q-separator"),T=(0,o.up)("q-td"),O=(0,o.up)("router-link"),I=(0,o.up)("q-tooltip"),p=(0,o.up)("q-tr"),S=(0,o.up)("q-table"),R=(0,o.up)("q-page-container"),f=(0,o.up)("q-layout");return(0,o.wg)(),(0,o.j4)(f,{view:"hHh lpR lFf"},{default:(0,o.w5)((()=>[(0,o.Wm)(R,null,{default:(0,o.w5)((()=>[(0,o._)("div",r,[(0,o.Wm)(u,{class:"back",outline:"",round:"",color:"black",icon:"arrow_back",to:"/explorer"})]),(0,o.Wm)(E,{color:"black"}),i,(0,o.Wm)(E,{color:"black"}),(0,o._)("div",d,[(0,o.Wm)(S,{rows:e.addresses_rows,columns:e.addresses_cols,"row-key":"id",loading:e.addresses_loading_state,"rows-per-page-options":[e.default_addresses_rows],"no-data-label":"Failed to fetch from the chain or theres no addresses from chain to render."},{"top-right":(0,o.w5)((()=>[(0,o.Wm)(u,{color:"green","icon-right":"refresh",label:"Refresh","no-caps":"",onClick:e.getAddresses},null,8,["onClick"])])),body:(0,o.w5)((e=>[(0,o.Wm)(p,{props:e},{default:(0,o.w5)((()=>[(0,o.Wm)(T,{key:"ID",props:e},{default:(0,o.w5)((()=>[(0,o.Uk)((0,n.zw)(e.row.id),1)])),_:2},1032,["props"]),(0,o.Wm)(T,{key:"User Address",props:e},{default:(0,o.w5)((()=>[(0,o.Wm)(O,{to:"/explorer/address/"+e.row.uuid,style:{"text-decoration":"none"}},{default:(0,o.w5)((()=>[(0,o.Uk)((0,n.zw)(e.row.uuid),1)])),_:2},1032,["to"])])),_:2},1032,["props"]),(0,o.Wm)(T,{key:"Association Address",props:e},{default:(0,o.w5)((()=>[(0,o._)("div",_,[(0,o.Uk)((0,n.zw)(e.row.association_uuid)+" ",1),"<No Association>"!==e.row.association_uuid?((0,o.wg)(),(0,o.j4)(I,{key:0,class:"bg-purple text-subtitle2","max-width":"30%"},{default:(0,o.w5)((()=>[l])),_:1})):(0,o.kq)("",!0)])])),_:2},1032,["props"]),(0,o.Wm)(T,{key:"User Type",props:e},{default:(0,o.w5)((()=>[(0,o.Uk)((0,n.zw)(e.row.entity_type),1)])),_:2},1032,["props"]),(0,o.Wm)(T,{key:"Transaction Map Bindings",props:e},{default:(0,o.w5)((()=>[(0,o.Uk)((0,n.zw)(e.row.tx_bindings_count),1)])),_:2},1032,["props"]),(0,o.Wm)(T,{key:"Consensus Negotiations",props:e},{default:(0,o.w5)((()=>[(0,o.Uk)((0,n.zw)(e.row.negotiations_count),1)])),_:2},1032,["props"])])),_:2},1032,["props"])])),_:1},8,["rows","columns","loading","rows-per-page-options"])])])),_:1})])),_:1})}t(71);var c=t(52),u=t.n(c),E=t(1959),T=t(2796);const O=[{name:"ID",align:"center",label:"ID",field:"id",sortable:!0},{name:"User Address",align:"center",label:"User Address",field:"uuid",sortable:!0},{name:"Association Address",align:"center",label:"Association Address",field:"association_uuid",sortable:!0},{name:"User Type",align:"center",label:"User Type",field:"entity_type",sortable:!0},{name:"Transaction Map Bindings",align:"center",label:"Transaction Map Bindings",field:"tx_bindings_count",sortable:!0},{name:"Consensus Negotiations",align:"center",label:"Consensus Negotiations",field:"negotiations_count"}],I=(0,o.aZ)({name:"ExplorerTransaction",components:{},data(){return{addresses_loading_state:(0,E.iH)(!1),first_instance:(0,E.iH)(!0)}},setup(){return{addresses_cols:O,addresses_rows:(0,E.iH)([]),default_addresses_rows:(0,E.iH)(T.kb)}},mounted(){this.getAddresses()},methods:{getAddresses(){this.addresses_loading_state=!0,u().get(`${T.sx}/explorer/addresses`).then((e=>{let s=[],t=1;for(let o of e.data)o.association_uuid=null===o.association_uuid?"<No Association>":o.association_uuid,o.id=t,t+=1,s.push(o);this.addresses_rows=s,this.addresses_loading_state=!1,this.first_instance||this.$q.notify({color:"green",position:"top",message:"Addresses has been updated.",timeout:5e3,progress:!0,icon:"mdi-account-check"}),this.first_instance=!1})).catch((e=>{this.$q.notify({color:"red",position:"top",message:`Failed to fetch transactions from the server. Please try again later. Reason: ${e.message}`,timeout:5e3,progress:!0,icon:"mdi-cancel"}),this.addresses_loading_state=!1}))}}});var p=t(4260),S=t(9214),R=t(2652),f=t(8240),A=t(5869),g=t(3243),C=t(8186),b=t(3884),w=t(8870),G=t(7518),U=t.n(G);const m=(0,p.Z)(I,[["render",N],["__scopeId","data-v-63649940"]]),k=m;U()(I,"components",{QLayout:S.Z,QPageContainer:R.Z,QBtn:f.Z,QSeparator:A.Z,QTable:g.Z,QTr:C.Z,QTd:b.Z,QTooltip:w.Z})}}]);