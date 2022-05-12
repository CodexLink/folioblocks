"use strict";(self["webpackChunkfolioblocks"]=self["webpackChunkfolioblocks"]||[]).push([[476],{2796:(e,t,o)=>{o.d(t,{$T:()=>r,_u:()=>d,kb:()=>a,sx:()=>s});const s="127.0.0.1:6001",a=100,l=Object.freeze({NODE_GENERAL_CONSENSUS_INIT:1,NODE_GENERAL_REGISTER_INIT:2,NODE_GENERAL_GENESIS_BLOCK_INIT:3,NODE_GENERAL_CONSENSUS_BLOCK_SYNC:4,NODE_GENERAL_CONSENSUS_CONFIRM_NEGOTIATION_START:5,NODE_GENERAL_CONSENSUS_CONCLUDE_NEGOTIATION_PROCESSING:6,INSTITUTION_ORG_GENERATE_STUDENT:7,INSTITUTION_ORG_REFER_NEW_DOCUMENT_OR_IMPORTANT_INFO:8,INSTITUTION_ORG_STUDENT_REFER_EXTRA_INFO:9,ORGANIZATION_USER_REGISTER:10,ORGANIZATION_REFER_EXTRA_INFO:11}),i=Object.freeze({STUDENT_BASE:1,STUDENT_LOG:2,STUDENT_ADDITIONAL:3,ORGANIZATION_BASE:4}),n=Object.freeze({CONSENSUS:1,INIT:2,SYNC:3});function r(e){switch(e){case l.NODE_GENERAL_CONSENSUS_INIT:return"Consensus Initialization";case l.NODE_GENERAL_REGISTER_INIT:return"Node Registration";case l.NODE_GENERAL_GENESIS_BLOCK_INIT:return"Node Genesis Block Creation";case l.NODE_GENERAL_CONSENSUS_BLOCK_SYNC:return"Node Block Sync via Consensus";case l.NODE_GENERAL_CONSENSUS_CONFIRM_NEGOTIATION_START:return"Node Consensus Negotiation Confirmed Start";case l.NODE_GENERAL_CONSENSUS_CONCLUDE_NEGOTIATION_PROCESSING:return"Node Consensus Negotiation Conclusion of Processing";case l.INSTITUTION_ORG_GENERATE_STUDENT:return"Institution Student Generation";case l.INSTITUTION_ORG_REFER_NEW_DOCUMENT_OR_IMPORTANT_INFO:return"Institution New Document / Important Info to Student Reference";case l.INSTITUTION_ORG_STUDENT_REFER_EXTRA_INFO:return"Institution Refer Extra Info to Student";case l.ORGANIZATION_USER_REGISTER:return"Organization Registration";case l.ORGANIZATION_REFER_EXTRA_INFO:return"Extra Info Referral to Organization";default:return"Unidentified Action."}}function d(e){let t=e.hasOwnProperty("content_type")?"User Transaction":"Internal Transaction",o=null;if(e.hasOwnProperty("content_type"))switch(e.content_type){case i.STUDENT_BASE:o="Student Base Portfolio";break;case i.STUDENT_LOG:o="Student Log from Orgs";break;case i.STUDENT_ADDITIONAL:o="Student Additional Info / Remarks";break;case i.ORGANIZATION_BASE:o="Organization Base Registration";break;default:o="Unidentified";break}else switch(e.action){case n.CONSENSUS:o="Internal: Consensus Context";break;case n.INIT:o="Internal: Context Initialization";break;case n.SYNC:o="Internal: Sync from Communication";break;default:o="Unidentified";break}return{identifiedType:t,resolvedTypeValue:o}}},476:(e,t,o)=>{o.r(t),o.d(t,{default:()=>Je});var s=o(3673),a=o(2323),l=o(8880);const i=e=>((0,s.dD)("data-v-cef52bf2"),e=e(),(0,s.Cn)(),e),n={class:"header text-h6"},r={class:"q-pt-md"},d=i((()=>(0,s._)("span",{class:"text-weight-bold q-ma-sm q-mb-sm q-pt-md q-ml-lg"}," Address: ",-1))),_=i((()=>(0,s._)("span",{class:"text-weight-bold q-ma-sm q-mb-sm q-ml-xl"}," Institution Reference: ",-1))),c=i((()=>(0,s._)("span",{class:"text-weight-bold q-ma-sm q-mb-sm q-ml-lg"}," Email Contact:",-1))),m=i((()=>(0,s._)("span",{class:"text-weight-bold q-ma-sm q-mb-sm q-ml-lg"}," Program:",-1))),u=i((()=>(0,s._)("span",{class:"text-weight-bold q-ma-sm q-mb-sm q-ml-lg"}," Role Preference in Field:",-1))),p=i((()=>(0,s._)("p",null,null,-1))),f=i((()=>(0,s._)("span",{class:"text-weight-bold q-ma-sm q-ml-lg"}," General Description:",-1))),g=i((()=>(0,s._)("span",{class:"text-weight-bold q-ma-sm q-mb-sm q-ml-lg"}," Skillset: ",-1))),h={class:"row"},b={class:"logs"},w=i((()=>(0,s._)("div",{class:"text-h6"},"Logs",-1))),y=i((()=>(0,s._)("div",{class:"text-subtitle1"},[(0,s.Uk)(" A set of contentful information that can be known as "),(0,s._)("strong",null,"logs"),(0,s.Uk)(", which should contains supporting context with documents (if given). The following are associated logs to you. Click them to get more infomration regarding this log. ")],-1))),k={class:"text-weight-bold q-mb-sm"},q=(0,s.Uk)(" | "),N=i((()=>(0,s._)("span",{class:"text-weight-bold q-ma-md q-mb-sm"}," Role: ",-1))),S=i((()=>(0,s._)("span",{class:"text-weight-bold text-justify q-mb-sm q-mr-md"}," Description: ",-1))),E=i((()=>(0,s._)("span",{class:"text-weight-bold q-ma-md q-mb-sm"}," By:",-1))),x=i((()=>(0,s._)("span",{class:"text-weight-bold text-justify q-mb-sm q-mr-md"}," Duration Start:",-1))),I={key:0},T={key:1,class:"text-weight-bold text-justify q-mb-sm q-mr-md"},O={class:"logs"},U=i((()=>(0,s._)("div",{class:"text-h6"},"Extras",-1))),R=i((()=>(0,s._)("div",{class:"text-subtitle1"},[(0,s.Uk)(" A set of information that can be known as "),(0,s._)("strong",null,"remarks"),(0,s.Uk)(". It may contain judgements that reflects the state of this student. Click them to get to the transaction proof. ")],-1))),W={class:"text-bold"},v=(0,s.Uk)(" | "),A=i((()=>(0,s._)("span",{class:"text-bold q-ma-sm q-mb-sm q-ml-sm"}," Timestamp:",-1))),C=i((()=>(0,s._)("span",{class:"text-weight-bold q-mb-sm q-mr-sm"}," Description:",-1))),D=i((()=>(0,s._)("span",{class:"text-weight-bold q-mb-sm q-mr-sm"}," By:",-1))),P=i((()=>(0,s._)("div",{class:"text-h6"},"Log Detailed Information",-1))),L=i((()=>(0,s._)("div",{class:"text-subtitle1"}," Other fields not shown from the list were shown here. Not that some of the properties are not available for access, for instance, the file. Contact the student for the permission. ",-1))),$=i((()=>(0,s._)("span",{class:"text-weight-bold q-ma-sm q-mb-sm"},"Title:",-1))),G=i((()=>(0,s._)("span",{class:"text-weight-bold q-ma-sm q-mb-sm"},"Transaction:",-1))),z=i((()=>(0,s._)("span",{class:"text-weight-bold q-ma-sm q-mb-sm"},"Description:",-1))),V=i((()=>(0,s._)("span",{class:"text-weight-bold q-ma-sm q-mb-sm"},"Role:",-1))),Z=i((()=>(0,s._)("span",{class:"text-weight-bold q-ma-sm q-mb-sm"}," Inserter / Validated by:",-1))),H=i((()=>(0,s._)("span",{class:"text-weight-bold q-ma-sm q-mb-sm"}," File:",-1))),j=i((()=>(0,s._)("span",{class:"text-weight-bold q-ma-sm q-mb-sm"}," Duration Start:",-1))),Q=i((()=>(0,s._)("span",{class:"text-weight-bold q-ma-sm q-mb-sm"}," Duration End:",-1))),F=i((()=>(0,s._)("span",{class:"text-weight-bold q-ma-sm q-mb-sm"}," Transaction Timestamp:",-1))),B=(0,s.Uk)(" Portfolio Settings "),M=i((()=>(0,s._)("div",{class:"text-h6 text-weight-bold"},"Share Settings",-1))),Y=(0,s.Uk)(" The following switches are states that can affect the output of your portfolio. Which means everyone who access your portfolio is affected, "),X=i((()=>(0,s._)("strong",null,"including you",-1))),K=(0,s.Uk)(". "),J=i((()=>(0,s._)("strong",null,"Be careful",-1))),ee=(0,s.Uk)(", by applying changes (in the means of clicking the apply button) will subject you to rate-limitation of "),te=i((()=>(0,s._)("strong",null,"3 minutes.",-1))),oe=(0,s.Uk)("Enable Portfolio Sharing"),se=(0,s.Uk)("Allow others to see this portfolio by explicitly referring to your address."),ae=(0,s.Uk)("Show Email Info"),le=(0,s.Uk)("Allow others to see your email for contacting purposes. We recommend doing this "),ie=i((()=>(0,s._)("strong",null,"ONLY",-1))),ne=(0,s.Uk)(" when you are currently at job application."),re=(0,s.Uk)("Allow Files"),de=(0,s.Uk)("Allow others to view and download your files. "),_e=i((()=>(0,s._)("strong",null,"Note that",-1))),ce=(0,s.Uk)(", these are your proof or supporting context behind these logs and extra information. "),me=i((()=>(0,s._)("strong",null,"You are not liable",-1))),ue=(0,s.Uk)(" when there's a data leakage as you are not the one who inserts these information."),pe=i((()=>(0,s._)("div",{class:"text-h6 text-weight-bold"},"Editable Information",-1))),fe=(0,s.Uk)(" Here are the fields that you can interchange even when blockchain already imprints the initial state of these fields. "),ge=i((()=>(0,s._)("strong",null,"Be careful",-1))),he=(0,s.Uk)(", change only if necessary. ");function be(e,t,o,i,be,we){const ye=(0,s.up)("router-link"),ke=(0,s.up)("q-linear-progress"),qe=(0,s.up)("q-card-section"),Ne=(0,s.up)("q-item-label"),Se=(0,s.up)("q-btn"),Ee=(0,s.up)("q-card-actions"),xe=(0,s.up)("q-item-section"),Ie=(0,s.up)("q-item"),Te=(0,s.up)("q-scroll-area"),Oe=(0,s.up)("q-card"),Ue=(0,s.up)("q-dialog"),Re=(0,s.up)("q-tooltip"),We=(0,s.up)("q-page-sticky"),ve=(0,s.up)("q-tab"),Ae=(0,s.up)("q-tabs"),Ce=(0,s.up)("q-separator"),De=(0,s.up)("q-toggle"),Pe=(0,s.up)("q-list"),Le=(0,s.up)("q-tab-panel"),$e=(0,s.up)("q-input"),Ge=(0,s.up)("q-form"),ze=(0,s.up)("q-tab-panels"),Ve=(0,s.Q2)("close-popup"),Ze=(0,s.Q2)("ripple");return(0,s.wg)(),(0,s.iD)(s.HY,null,[(0,s._)("div",n,[(0,s._)("p",r,[d,(0,s.Wm)(ye,{to:"/explorer/address/"+e.portfolio_user_address,style:{"text-decoration":"none"}},{default:(0,s.w5)((()=>[(0,s.Uk)((0,a.zw)(e.portfolio_user_address),1)])),_:1},8,["to"]),_,(0,s.Uk)(" "+(0,a.zw)(e.portfolio_user_association),1)]),(0,s._)("p",null,[c,(0,s.Uk)((0,a.zw)(e.portfolio_user_email_contact),1)]),(0,s._)("p",null,[m,(0,s.Uk)(" "+(0,a.zw)(e.portfolio_user_program)+" ",1),u,(0,s.Uk)(" "+(0,a.zw)(e.portfolio_user_preferred_role),1)]),p,(0,s._)("p",null,[f,(0,s.Uk)(" "+(0,a.zw)(e.portfolio_user_description),1)]),(0,s._)("p",null,[g,(0,s.Uk)(" "+(0,a.zw)(e.portfolio_user_personal_skills),1)])]),(0,s._)("div",h,[(0,s._)("div",b,[e.portfolio_log_info_rendering_state?((0,s.wg)(),(0,s.j4)(ke,{key:0,query:"",color:"red",class:"q-mt-sm"})):(0,s.kq)("",!0),(0,s.Wm)(qe,{style:{"margin-bottom":"0.5%"}},{default:(0,s.w5)((()=>[w,y])),_:1}),(0,s.Wm)(Te,{style:{height:"100%","max-width":"100%"}},{default:(0,s.w5)((()=>[((0,s.wg)(!0),(0,s.iD)(s.HY,null,(0,s.Ko)(e.portfolio_log_container,(t=>((0,s.wg)(),(0,s.j4)(Ie,{key:t.id,class:"logdata"},{default:(0,s.w5)((()=>[(0,s.Wm)(xe,{class:"text-h6"},{default:(0,s.w5)((()=>[(0,s.Wm)(Ne,null,{default:(0,s.w5)((()=>[(0,s._)("span",k,(0,a.zw)(t.context.name),1),q,N,(0,s.Uk)((0,a.zw)(t.context.role),1)])),_:2},1024),(0,s.Wm)(Ne,{class:"q-ml-md",style:{"margin-top":"2%"}},{default:(0,s.w5)((()=>[S,(0,s.Uk)((0,a.zw)(t.context.description),1)])),_:2},1024),(0,s.Wm)(Ne,{style:{"margin-top":"2%"}},{default:(0,s.w5)((()=>[E,(0,s.Wm)(ye,{to:"/explorer/address/"+t.context.validated_by,style:{"text-decoration":"none"}},{default:(0,s.w5)((()=>[(0,s.Uk)((0,a.zw)(t.context.validated_by),1)])),_:2},1032,["to"])])),_:2},1024),(0,s.Wm)(Ne,{class:"q-ml-md",style:{"margin-top":"2%"}},{default:(0,s.w5)((()=>[x,(0,s.Uk)((0,a.zw)(t.context.duration_start)+" ",1),t.context.duration_end?((0,s.wg)(),(0,s.iD)("span",I,"|")):(0,s.kq)("",!0),t.context.duration_end?((0,s.wg)(),(0,s.iD)("span",T," Duration End:")):(0,s.kq)("",!0),(0,s.Uk)((0,a.zw)(t.context.duration_end)+" ",1),(0,s.Wm)(Ee,{align:"right"},{default:(0,s.w5)((()=>[(0,s.Wm)(Se,{outline:"",right:"",color:"black",label:"View More",class:"q-mt-md",onClick:o=>e.getLogInfo(t.id)},null,8,["onClick"])])),_:2},1024)])),_:2},1024)])),_:2},1024)])),_:2},1024)))),128))])),_:1})]),(0,s._)("div",O,[e.portfolio_extra_info_rendering_state?((0,s.wg)(),(0,s.j4)(ke,{key:0,query:"",color:"red",class:"q-mt-sm"})):(0,s.kq)("",!0),(0,s.Wm)(qe,{style:{"margin-bottom":"0.5%"}},{default:(0,s.w5)((()=>[U,R])),_:1}),(0,s.Wm)(Te,{style:{height:"100%","max-width":"100%"}},{default:(0,s.w5)((()=>[((0,s.wg)(!0),(0,s.iD)(s.HY,null,(0,s.Ko)(e.portfolio_extra_container,(e=>((0,s.wg)(),(0,s.j4)(Ie,{key:e.tx_hash,to:"/explorer/transaction/"+e.tx_hash,style:{"text-decoration":"none"},clickable:"",class:"logdata"},{default:(0,s.w5)((()=>[(0,s.Wm)(xe,{class:"text-h6"},{default:(0,s.w5)((()=>[(0,s.Wm)(Ne,{class:"q-mb-sm"},{default:(0,s.w5)((()=>[(0,s._)("span",W,(0,a.zw)(e.context.title),1),v,A,(0,s.Uk)((0,a.zw)(e.context.timestamp),1)])),_:2},1024),(0,s.Wm)(Ne,{class:"q-ml-sm text-justify q-mb-sm q-ml-lg",style:{"margin-top":"2%"}},{default:(0,s.w5)((()=>[C,(0,s.Uk)((0,a.zw)(e.context.description),1)])),_:2},1024),(0,s.Wm)(Ne,{class:"q-ml-sm text-justify q-mb-sm q-ml-lg",style:{"margin-top":"2%"}},{default:(0,s.w5)((()=>[D,(0,s.Wm)(ye,{to:"/explorer/address/"+e.context.inserter,style:{"text-decoration":"none"}},{default:(0,s.w5)((()=>[(0,s.Uk)((0,a.zw)(e.context.inserter),1)])),_:2},1032,["to"])])),_:2},1024)])),_:2},1024)])),_:2},1032,["to"])))),128))])),_:1})])]),(0,s.Wm)(Ue,{modelValue:e.logModalState,"onUpdate:modelValue":t[1]||(t[1]=t=>e.logModalState=t),class:"modal"},{default:(0,s.w5)((()=>[(0,s.Wm)(Oe,{class:"my-card-log"},{default:(0,s.w5)((()=>[(0,s.Wm)(qe,null,{default:(0,s.w5)((()=>[P,L])),_:1}),(0,s.Wm)(qe,{class:"wrap-content"},{default:(0,s.w5)((()=>[(0,s.Wm)(Ie,null,{default:(0,s.w5)((()=>[(0,s.Wm)(xe,{class:"text-h6"},{default:(0,s.w5)((()=>[(0,s.Wm)(Ne,{class:"q-mb-md"},{default:(0,s.w5)((()=>[$,(0,s.Uk)((0,a.zw)(e.selectedLog.context.name),1)])),_:1}),(0,s.Wm)(Ne,{class:"q-mb-md"},{default:(0,s.w5)((()=>[G,(0,s.Wm)(ye,{to:"/explorer/transaction/"+e.selectedLog.tx_hash,style:{"text-decoration":"none"}},{default:(0,s.w5)((()=>[(0,s.Uk)((0,a.zw)(e.selectedLog.tx_hash),1)])),_:1},8,["to"])])),_:1}),(0,s.Wm)(Ne,{class:"q-mb-md"},{default:(0,s.w5)((()=>[z,(0,s.Uk)((0,a.zw)(e.selectedLog.context.description),1)])),_:1}),(0,s.Wm)(Ne,{class:"q-mb-md"},{default:(0,s.w5)((()=>[V,(0,s.Uk)((0,a.zw)(e.selectedLog.context.role),1)])),_:1}),(0,s.Wm)(Ne,{class:"q-mb-md"},{default:(0,s.w5)((()=>[Z,(0,s.Wm)(ye,{to:"/explorer/address/"+e.selectedLog.context.validated_by,style:{"text-decoration":"none"}},{default:(0,s.w5)((()=>[(0,s.Uk)((0,a.zw)(e.selectedLog.context.validated_by),1)])),_:1},8,["to"])])),_:1}),(0,s.Wm)(Ne,{class:"q-mb-md"},{default:(0,s.w5)((()=>[H,(0,s.Wm)(Se,{outline:"",color:"black",label:"View / Download",class:"q-mr-md",onClick:t[0]||(t[0]=t=>e.getFile(e.selectedLog.context.address_origin,e.selectedLog.context.file)),disable:null===e.selectedLog.context.file},null,8,["disable"])])),_:1}),(0,s.Wm)(Ne,{class:"q-mb-md"},{default:(0,s.w5)((()=>[j,(0,s.Uk)((0,a.zw)(e.selectedLog.context.duration_start),1)])),_:1}),null!==e.selectedLog.context.duration_end?((0,s.wg)(),(0,s.j4)(Ne,{key:0,class:"q-mb-md"},{default:(0,s.w5)((()=>[Q,(0,s.Uk)((0,a.zw)(e.selectedLog.context.duration_end),1)])),_:1})):(0,s.kq)("",!0),(0,s.Wm)(Ne,{class:"q-mb-md"},{default:(0,s.w5)((()=>[F,(0,s.Uk)((0,a.zw)(e.selectedLog.context.timestamp),1)])),_:1})])),_:1})])),_:1})])),_:1}),(0,s.Wm)(Ee,{align:"right",style:{"padding-bottom":"3%"}},{default:(0,s.w5)((()=>[(0,s.wy)((0,s.Wm)(Se,{flat:"",label:"Close Modal",style:{color:"#f44336"},class:"q-mr-md"},null,512),[[Ve],[Ze]])])),_:1})])),_:1})])),_:1},8,["modelValue"]),(0,s.Wm)(We,{position:"bottom-right",offset:[24,24]},{default:(0,s.w5)((()=>[e.isStudent?(0,s.wy)(((0,s.wg)(),(0,s.j4)(Se,{key:0,fab:"",icon:"mdi-file-cog",color:"red",onClick:t[2]||(t[2]=t=>e.portfolio_modal=!0)},{default:(0,s.w5)((()=>[(0,s.Wm)(Re,{class:"bg-indigo",offset:[10,10],anchor:"center left",self:"center right"},{default:(0,s.w5)((()=>[B])),_:1})])),_:1})),[[Ze]]):(0,s.kq)("",!0)])),_:1}),(0,s.Wm)(Ue,{modelValue:e.portfolio_modal,"onUpdate:modelValue":t[13]||(t[13]=t=>e.portfolio_modal=t),class:"modal"},{default:(0,s.w5)((()=>[(0,s.Wm)(Oe,{style:{width:"100%"}},{default:(0,s.w5)((()=>[e.isProcessing?((0,s.wg)(),(0,s.j4)(ke,{key:0,rounded:"",query:"",indeterminate:"",color:"red"})):(0,s.kq)("",!0),(0,s.Wm)(Ae,{modelValue:e.selected_settings,"onUpdate:modelValue":t[3]||(t[3]=t=>e.selected_settings=t),dense:"",class:"text-grey","active-color":"secondary","indicator-color":"secondary",align:"justify",style:{height:"50px"}},{default:(0,s.w5)((()=>[(0,s.Wm)(ve,{name:"share_settings",label:"Settings",class:"tab",disable:e.isProcessing},null,8,["disable"]),(0,s.Wm)(ve,{name:"editable_infos",label:"Editables",class:"tab",disable:e.isProcessing},null,8,["disable"])])),_:1},8,["modelValue"]),(0,s.Wm)(Ce),e.isStudent?((0,s.wg)(),(0,s.j4)(ze,{key:1,modelValue:e.selected_settings,"onUpdate:modelValue":t[12]||(t[12]=t=>e.selected_settings=t),animated:"",class:"panels"},{default:(0,s.w5)((()=>[(0,s.Wm)(Le,{name:"share_settings"},{default:(0,s.w5)((()=>[(0,s.Wm)(qe,null,{default:(0,s.w5)((()=>[M])),_:1}),(0,s.Wm)(qe,{class:"text-justify"},{default:(0,s.w5)((()=>[Y,X,K])),_:1}),(0,s.Wm)(qe,{class:"text-justify"},{default:(0,s.w5)((()=>[J,ee,te])),_:1}),(0,s.Wm)(Pe,{style:{"padding-top":"3%"}},{default:(0,s.w5)((()=>[(0,s.wy)(((0,s.wg)(),(0,s.j4)(Ie,{tag:"label"},{default:(0,s.w5)((()=>[(0,s.Wm)(xe,null,{default:(0,s.w5)((()=>[(0,s.Wm)(Ne,null,{default:(0,s.w5)((()=>[oe])),_:1}),(0,s.Wm)(Ne,{caption:""},{default:(0,s.w5)((()=>[se])),_:1})])),_:1}),(0,s.Wm)(xe,{side:""},{default:(0,s.w5)((()=>[(0,s.Wm)(De,{color:"red",disable:e.isProcessing,modelValue:e.portfolio_sharing_state,"onUpdate:modelValue":t[4]||(t[4]=t=>e.portfolio_sharing_state=t)},null,8,["disable","modelValue"])])),_:1})])),_:1})),[[Ze]]),(0,s.wy)(((0,s.wg)(),(0,s.j4)(Ie,{tag:"label"},{default:(0,s.w5)((()=>[(0,s.Wm)(xe,null,{default:(0,s.w5)((()=>[(0,s.Wm)(Ne,null,{default:(0,s.w5)((()=>[ae])),_:1}),(0,s.Wm)(Ne,{caption:""},{default:(0,s.w5)((()=>[le,ie,ne])),_:1})])),_:1}),(0,s.Wm)(xe,{side:"",top:""},{default:(0,s.w5)((()=>[(0,s.Wm)(De,{color:"red",disable:e.isProcessing,modelValue:e.portfolio_show_email_state,"onUpdate:modelValue":t[5]||(t[5]=t=>e.portfolio_show_email_state=t)},null,8,["disable","modelValue"])])),_:1})])),_:1})),[[Ze]]),(0,s.wy)(((0,s.wg)(),(0,s.j4)(Ie,{tag:"label"},{default:(0,s.w5)((()=>[(0,s.Wm)(xe,null,{default:(0,s.w5)((()=>[(0,s.Wm)(Ne,null,{default:(0,s.w5)((()=>[re])),_:1}),(0,s.Wm)(Ne,{caption:""},{default:(0,s.w5)((()=>[de,_e,ce,me,ue])),_:1})])),_:1}),(0,s.Wm)(xe,{side:"",top:""},{default:(0,s.w5)((()=>[(0,s.Wm)(De,{color:"red",disable:e.isProcessing,modelValue:e.portfolio_allow_file_state,"onUpdate:modelValue":t[6]||(t[6]=t=>e.portfolio_allow_file_state=t)},null,8,["disable","modelValue"])])),_:1})])),_:1})),[[Ze]]),(0,s.Wm)(Ee,{align:"right"},{default:(0,s.w5)((()=>[(0,s.wy)((0,s.Wm)(Se,{flat:"",style:{color:"#3700b3"},label:"Close Modal",onClick:t[7]||(t[7]=t=>e.portfolio_modal=!1)},null,512),[[Ze]]),(0,s.wy)((0,s.Wm)(Se,{flat:"",style:{color:"#ff0080"},disable:e.portfolio_setting_btn_click_state,label:"Apply Settings",onClick:e.submitPortfolioSettings},null,8,["disable","onClick"]),[[Ze]])])),_:1})])),_:1})])),_:1}),(0,s.Wm)(Le,{name:"editable_infos"},{default:(0,s.w5)((()=>[(0,s.Wm)(Ge,{onSubmit:(0,l.iM)(e.submitEditableInfo,["prevent"]),onValidationError:e.submitEditableInfoOnError,autofocus:!0},{default:(0,s.w5)((()=>[(0,s.Wm)(qe,null,{default:(0,s.w5)((()=>[pe])),_:1}),(0,s.Wm)(qe,{class:"text-justify"},{default:(0,s.w5)((()=>[fe,ge,he])),_:1}),(0,s.Wm)(qe,null,{default:(0,s.w5)((()=>[(0,s.Wm)($e,{class:"input",outlined:"",dense:"",color:"secondary",modelValue:e.editable_info_preferred_role,"onUpdate:modelValue":t[8]||(t[8]=t=>e.editable_info_preferred_role=t),label:"Preferred Role",counter:"","lazy-rules":"",hint:"Your preferred role in the industry or in works.",disable:e.isProcessing,rules:[e=>e.length>=4&&e.length<=32||"This should contain not less than 4 characters or more than 32 characters."]},null,8,["modelValue","disable","rules"]),(0,s.Wm)($e,{class:"input",outlined:"",dense:"",color:"secondary",modelValue:e.editable_info_personal_skills,"onUpdate:modelValue":t[9]||(t[9]=t=>e.editable_info_personal_skills=t),label:"Personal Skills",counter:"",hint:"Similar to description but is specified to student's capability. Seperate the contents in comma. Please note only important or significant skills that you have.",rules:[e=>e&&e.length>=8||"This is required. Must have 8 characters and above."],"lazy-rules":"",disable:e.isProcessing},null,8,["modelValue","rules","disable"]),(0,s.Wm)($e,{class:"input",outlined:"",dense:"",color:"secondary",modelValue:e.editable_info_description,"onUpdate:modelValue":t[10]||(t[10]=t=>e.editable_info_description=t),type:"textarea",label:"Description",hint:"Literally, the description about you, but keep it professional as it was shown in your portfolio.",disable:e.isProcessing,counter:"",rules:[e=>e&&e.length>=8||"This is required. Must have 8 characters and above."],"lazy-rules":""},null,8,["modelValue","disable","rules"])])),_:1}),(0,s.Wm)(Ee,{align:"right"},{default:(0,s.w5)((()=>[(0,s.wy)((0,s.Wm)(Se,{flat:"",style:{color:"#3700b3"},label:"Close Modal",onClick:t[11]||(t[11]=t=>e.portfolio_modal=!1)},null,512),[[Ze]]),(0,s.wy)((0,s.Wm)(Se,{flat:"",type:"submit",style:{color:"#ff0080"},label:"Apply New Info",disable:e.editable_info_btn_click_state},null,8,["disable"]),[[Ze]])])),_:1})])),_:1},8,["onSubmit","onValidationError"])])),_:1})])),_:1},8,["modelValue"])):(0,s.kq)("",!0)])),_:1})])),_:1},8,["modelValue"])],64)}o(71),o(7965),o(6016);var we=o(1959),ye=o(8825),ke=o(52),qe=o.n(ke),Ne=o(2796),Se=o(9582);const Ee=(0,s.aZ)({data(){return{portfolio_user_address:(0,we.iH)("—"),portfolio_user_association:(0,we.iH)("—"),portfolio_user_program:(0,we.iH)("—"),portfolio_user_description:(0,we.iH)("—"),portfolio_user_personal_skills:(0,we.iH)("—"),portfolio_user_preferred_role:(0,we.iH)("—"),portfolio_extra_container:(0,we.iH)([]),portfolio_log_container:(0,we.iH)([]),portfolio_user_email_contact:(0,we.iH)("—"),portfolio_modal:(0,we.iH)(!1),selected_settings:(0,we.iH)("share_settings"),portfolio_extra_info_rendering_state:(0,we.iH)(!0),portfolio_log_info_rendering_state:(0,we.iH)(!0),isProcessing:(0,we.iH)(!1),portfolio_sharing_state:(0,we.iH)(!1),portfolio_show_email_state:(0,we.iH)(!1),portfolio_allow_file_state:(0,we.iH)(!1),portfolio_setting_btn_click_state:(0,we.iH)(!1),editable_info_btn_click_state:(0,we.iH)(!1),editable_info_description:(0,we.iH)(""),editable_info_preferred_role:(0,we.iH)(""),editable_info_personal_skills:(0,we.iH)(""),isStudent:(0,we.iH)(!1),isOrg:(0,we.iH)(!1),isAnonymous:(0,we.iH)(!1)}},setup(){(0,ye.Z)(),(0,Se.yj)(),(0,Se.tv)();return{logModalState:(0,we.iH)(!1),selectedLog:(0,we.iH)(null)}},mounted(){this.getPortfolio(),this.isStudent&&(this.loadPortfolioSettings(),this.loadEditableInfo())},methods:{loadPortfolioSettings(){this.isProcessing=!0,this.portfolio_setting_btn_click_state=!1,qe().get(`http://${Ne.sx}/dashboard/portfolio_settings`,{headers:{"X-Token":this.$q.localStorage.getItem("token")}}).then((e=>{this.portfolio_sharing_state=e.data.enable_sharing,this.portfolio_show_email_state=e.data.expose_email_info,this.portfolio_allow_file_state=e.data.show_files,this.isProcessing=!1})).catch((e=>{const t=void 0===e.response.data?`${e.message}. Server may be unvailable. Please try again later.`:e.response.data.detail;this.$q.notify({color:"negative",position:"top",message:`There was an error when fetching your information. Due to this, switches will be disabled. Please refresh and try again. Reason: ${t}`,timeout:1e4,progress:!0,icon:"report_problem"})}))},loadEditableInfo(){this.isProcessing=!0,qe().get(`http://${Ne.sx}/dashboard/user_profile`,{headers:{"X-Token":this.$q.localStorage.getItem("token")}}).then((e=>{this.editable_info_description=e.data.description,this.editable_info_preferred_role=e.data.preferred_role,this.editable_info_personal_skills=e.data.personal_skills,this.isProcessing=!1})).catch((e=>{const t=void 0===e.response.data?`${e.message}. Server may be unvailable. Please try again later.`:e.response.data.detail;this.$q.notify({color:"negative",position:"top",message:`There was an error when fetching your information. Due to this, fields will be disabled. Please refresh and try again. Reason: ${t}`,timeout:1e4,progress:!0,icon:"report_problem"})}))},submitEditableInfo(){this.editable_info_btn_click_state=!0,this.isProcessing=!0;let e=new FormData;e.append("description",this.editable_info_description),e.append("personal_skills",this.editable_info_personal_skills),e.append("preferred_role",this.editable_info_preferred_role),qe().post(`http://${Ne.sx}/dashboard/apply_profile_changes`,e,{headers:{"X-Token":this.$q.localStorage.getItem("token"),"Content-Type":"multipart/form-data"}}).then((e=>{this.$q.notify({color:"green",position:"top",message:"Editable information has been saved! Refreshing in 3 seconds ...",timeout:1e4,progress:!0,icon:"report_problem"}),setTimeout((()=>{this.$router.go()}),3e3)})).catch((e=>{const t=void 0===e.response.data?`${e.message}. Server may be unvailable. Please try again later.`:e.response.data.detail;this.$q.notify({color:"negative",position:"top",message:`There was an error when submitting new information. Reason: ${t}`,timeout:1e4,progress:!0,icon:"report_problem"})})),this.isProcessing=!1},submitEditableInfoOnError(){this.$q.notify({color:"negative",position:"top",message:"There was an error from one of the fields. Please check and try again.",timeout:1e4,progress:!0,icon:"report_problem"})},submitPortfolioSettings(){this.isProcessing=!0,this.portfolio_setting_btn_click_state=!0,qe().post(`http://${Ne.sx}/dashboard/apply_portfolio_settings`,{enable_sharing:this.portfolio_sharing_state,expose_email_info:this.portfolio_show_email_state,show_files:this.portfolio_allow_file_state},{headers:{"X-Token":this.$q.localStorage.getItem("token")}}).then((e=>{this.$q.notify({color:"green",position:"top",message:"Portfolio settings has been saved! Refreshing in 3 seconds ...",timeout:1e4,progress:!0,icon:"report_problem"}),setTimeout((()=>{this.$router.go()}),3e3)})).catch((e=>{const t=void 0===e.response.data?`${e.message}. Server may be unvailable. Please try again later.`:e.response.data.detail;this.$q.notify({color:"negative",position:"top",message:`There was an error when submitting portfolio settings. Due to this, lease refresh and try again. Reason: ${t}`,timeout:1e4,progress:!0,icon:"report_problem"})})),this.isProcessing=!1},getPortfolio(){let e=`http://${Ne.sx}/dashboard/portfolio`;if(void 0===this.$route.query.address&&null!==this.$q.localStorage.getItem("token")&&"Student Dashboard User"===this.$q.localStorage.getItem("role"))this.isStudent=!0;else if(void 0!==this.$route.query.address&&null!==this.$q.localStorage.getItem("token")&&"Organization Dashboard User"==this.$q.localStorage.getItem("role"))this.isOrg=!0,e+=`?address=${this.$route.query.address}`;else{if(void 0===this.$route.query.address||null!==this.$q.localStorage.getItem("token"))return this.$router.push({path:"Organization Dashboard User "===this.$q.localStorage.getItem("role")?"/dashboard":"/"}),void this.$q.notify({color:"negative",position:"top",message:"You are not allowed to access this view. If you are an anonymous, please ensure that the address you copied is exactly 35 characters or the address were not found.",timeout:1e4,progress:!0,icon:"report_problem"});this.isAnonymous=!0,e+=`?address=${this.$route.query.address}`}let t={headers:{"X-Token":this.$q.localStorage.getItem("token")}};qe().get(e,this.isOrg||this.isStudent?t:{}).then((e=>{this.$q.notify({color:"blue",position:"top",message:this.isAnonymous?"You are accessing this portfolio as an anonymous.":this.isOrg?"You are accessing this student's portfolio as a preview. Note that you cannot modify these entries anymore.":"You are accessing this as a student, please check your portfolio settings on the bottom-right to adjust your portfolio's output.",timeout:1e4,progress:!0,icon:"info"}),this.portfolio_user_address=e.data.address,this.portfolio_user_association=e.data.association,this.portfolio_user_program=e.data.program,this.portfolio_user_description=null===e.data.description?"No information":e.data.description,this.portfolio_user_personal_skills=null===e.data.personal_skills?"No information.":e.data.personal_skills,this.portfolio_user_preferred_role=e.data.preferred_role,this.portfolio_user_email_contact=null===e.data.email?"Not Available.":e.data.email,this.portfolio_extra_container=e.data.extra,this.portfolio_extra_info_rendering_state=!1;let t=1,o=[];for(let s of e.data.logs)s.id=t,s.context.duration_start=new Date(s.context.duration_start).toLocaleDateString(),null!==s.context.duration_end&&(s.context.duration_end=new Date(s.context.duration_end).toLocaleDateString()),o.push(s),t++;this.portfolio_log_container=o,this.portfolio_log_info_rendering_state=!1})).catch((e=>{const t=void 0===e.response.data?`${e.message}. Server may be unvailable. Please try again later.`:e.response.data.detail;this.$q.notify({color:"negative",position:"top",message:`There was an error when fetching portfolio. Reason: ${t}`,timeout:1e4,progress:!0,icon:"report_problem"}),this.$router.go(-1)}))},getLogInfo(e){this.logModalState=!0,this.selectedLog=this.portfolio_log_container[e-1]},getFile(e,t){let o=`http://${Ne.sx}/dashboard/portfolio/${e}/file/${t}`;qe().get(o,{responseType:"blob"}).then((e=>{let t=new Blob([e.data],{type:"application/pdf"}),o=window.URL.createObjectURL(t);window.open(o)}))}}});var xe=o(4260),Ie=o(1598),Te=o(5589),Oe=o(7704),Ue=o(3414),Re=o(2035),We=o(2350),ve=o(9367),Ae=o(8240),Ce=o(6778),De=o(151),Pe=o(1007),Le=o(8870),$e=o(7547),Ge=o(3269),ze=o(5869),Ve=o(5906),Ze=o(6602),He=o(7011),je=o(8886),Qe=o(5269),Fe=o(4689),Be=o(677),Me=o(6489),Ye=o(7518),Xe=o.n(Ye);const Ke=(0,xe.Z)(Ee,[["render",be],["__scopeId","data-v-cef52bf2"]]),Je=Ke;Xe()(Ee,"components",{QLinearProgress:Ie.Z,QCardSection:Te.Z,QScrollArea:Oe.Z,QItem:Ue.Z,QItemSection:Re.Z,QItemLabel:We.Z,QCardActions:ve.Z,QBtn:Ae.Z,QDialog:Ce.Z,QCard:De.Z,QPageSticky:Pe.Z,QTooltip:Le.Z,QTabs:$e.Z,QTab:Ge.Z,QSeparator:ze.Z,QTabPanels:Ve.Z,QTabPanel:Ze.Z,QList:He.Z,QToggle:je.Z,QForm:Qe.Z,QInput:Fe.Z}),Xe()(Ee,"directives",{ClosePopup:Be.Z,Ripple:Me.Z})}}]);