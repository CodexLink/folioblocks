"use strict";(self["webpackChunkfolioblocks_web"]=self["webpackChunkfolioblocks_web"]||[]).push([[35],{2796:(e,t,o)=>{o.d(t,{$T:()=>c,_u:()=>m,kb:()=>i,oX:()=>n,sx:()=>a,uK:()=>l});const s="https://",a=`${s}folioblocks.southeastasia.azurecontainer.io`,l=`${s}codexlink.github.io/folioblocks`,i=100,n="otpauth://totp/Organization%20Creator:Folioblocks-Web?secret=MNMDQX32IREXQQLIM4YHMYSYLFUHASCBMJFF63TCMU4UY5TNJBTVMWC7OMWTSQLUNJEVCPJRGZQTOZJTMYYDAOLFMJRGMMJWMVSWCOJWGM2TMOBTHBTGMYZTGMZDOZTDGI2TEOJYGM2DMYRRGE3DCYZVGNRTSYRRMQ3WKNZSGAZDG%3D%3D%3D&issuer=Organization%20Creator",r=Object.freeze({NODE_GENERAL_CONSENSUS_INIT:1,NODE_GENERAL_REGISTER_INIT:2,NODE_GENERAL_GENESIS_BLOCK_INIT:3,NODE_GENERAL_CONSENSUS_BLOCK_SYNC:4,NODE_GENERAL_CONSENSUS_CONFIRM_NEGOTIATION_START:5,NODE_GENERAL_CONSENSUS_CONCLUDE_NEGOTIATION_PROCESSING:6,INSTITUTION_ORG_GENERATE_STUDENT:7,INSTITUTION_ORG_REFER_NEW_DOCUMENT_OR_IMPORTANT_INFO:8,INSTITUTION_ORG_STUDENT_REFER_EXTRA_INFO:9,ORGANIZATION_USER_REGISTER:10,ORGANIZATION_REFER_EXTRA_INFO:11}),d=Object.freeze({STUDENT_BASE:1,STUDENT_LOG:2,STUDENT_ADDITIONAL:3,ORGANIZATION_BASE:4}),_=Object.freeze({CONSENSUS:1,INIT:2,SYNC:3});function c(e){switch(e){case r.NODE_GENERAL_CONSENSUS_INIT:return"Consensus Initialization";case r.NODE_GENERAL_REGISTER_INIT:return"Node Registration";case r.NODE_GENERAL_GENESIS_BLOCK_INIT:return"Node Genesis Block Creation";case r.NODE_GENERAL_CONSENSUS_BLOCK_SYNC:return"Node Block Sync via Consensus";case r.NODE_GENERAL_CONSENSUS_CONFIRM_NEGOTIATION_START:return"Node Consensus Negotiation Confirmed Start";case r.NODE_GENERAL_CONSENSUS_CONCLUDE_NEGOTIATION_PROCESSING:return"Node Consensus Negotiation Conclusion of Processing";case r.INSTITUTION_ORG_GENERATE_STUDENT:return"Institution Student Generation";case r.INSTITUTION_ORG_REFER_NEW_DOCUMENT_OR_IMPORTANT_INFO:return"Institution New Document / Important Info to Student Reference";case r.INSTITUTION_ORG_STUDENT_REFER_EXTRA_INFO:return"Institution Refer Extra Info to Student";case r.ORGANIZATION_USER_REGISTER:return"Organization Registration";case r.ORGANIZATION_REFER_EXTRA_INFO:return"Extra Info Referral to Organization";default:return"Unidentified Action."}}function m(e){let t=e.hasOwnProperty("content_type")?"User Transaction":"Internal Transaction",o=null;if(e.hasOwnProperty("content_type"))switch(e.content_type){case d.STUDENT_BASE:o="Student Base Portfolio";break;case d.STUDENT_LOG:o="Student Log from Orgs";break;case d.STUDENT_ADDITIONAL:o="Student Additional Info / Remarks";break;case d.ORGANIZATION_BASE:o="Organization Base Registration";break;default:o="Unidentified";break}else switch(e.action){case _.CONSENSUS:o="Internal: Consensus Context";break;case _.INIT:o="Internal: Context Initialization";break;case _.SYNC:o="Internal: Sync from Communication";break;default:o="Unidentified";break}return{identifiedType:t,resolvedTypeValue:o}}},4035:(e,t,o)=>{o.r(t),o.d(t,{default:()=>at});var s=o(3673),a=o(2323),l=o(8880);const i=e=>((0,s.dD)("data-v-344ea672"),e=e(),(0,s.Cn)(),e),n={class:"header text-h6"},r={class:"q-pt-md"},d=i((()=>(0,s._)("span",{class:"text-weight-bold q-ma-sm q-mb-sm q-pt-md q-ml-lg"}," Address: ",-1))),_=i((()=>(0,s._)("span",{class:"text-weight-bold q-ma-sm q-mb-sm q-ml-xl"}," Institution Reference: ",-1))),c=i((()=>(0,s._)("span",{class:"text-weight-bold q-ma-sm q-mb-sm q-ml-lg"}," Email Contact:",-1))),m=i((()=>(0,s._)("span",{class:"text-weight-bold q-ma-sm q-mb-sm q-ml-lg"}," Program:",-1))),u=i((()=>(0,s._)("span",{class:"text-weight-bold q-ma-sm q-mb-sm q-ml-lg"}," Role Preference in Field:",-1))),p=i((()=>(0,s._)("p",null,null,-1))),f=i((()=>(0,s._)("span",{class:"text-weight-bold q-ma-sm q-ml-lg"}," General Description:",-1))),g=i((()=>(0,s._)("span",{class:"text-weight-bold q-ma-sm q-mb-sm q-ml-lg"}," Skillset: ",-1))),h={class:"row"},b={class:"logs"},w=i((()=>(0,s._)("div",{class:"text-h6"},"Documents / Logs",-1))),y=i((()=>(0,s._)("div",{class:"text-subtitle1"},[(0,s.Uk)(" A set of contentful information that can be known as "),(0,s._)("strong",null,"documents / logs"),(0,s.Uk)(", which should contains supporting context with documents (if given). The following are associated logs to you. Click them to get more information regarding this log. ")],-1))),k={class:"text-weight-bold q-mb-sm"},q=(0,s.Uk)(" |"),N=i((()=>(0,s._)("span",{class:"text-weight-bold q-ma-md q-mb-sm"},"Role:",-1))),S=i((()=>(0,s._)("span",{class:"text-weight-bold text-justify q-mb-sm q-mr-md"}," Description:",-1))),T=i((()=>(0,s._)("span",{class:"text-weight-bold q-ma-md q-mb-sm"},"By:",-1))),E=i((()=>(0,s._)("span",{class:"text-weight-bold text-justify q-mb-sm q-mr-md"},"Timestamp:",-1))),x={class:"logs"},I=i((()=>(0,s._)("div",{class:"text-h6"},"Extras / Remarks",-1))),O=i((()=>(0,s._)("div",{class:"text-subtitle1"},[(0,s.Uk)(" A set of information that can be known as "),(0,s._)("strong",null,"extra / remarks"),(0,s.Uk)(". It may contain judgements that reflects the state of this student. Click them to get to the transaction proof. ")],-1))),U={class:"text-bold"},R=(0,s.Uk)(" | "),W=i((()=>(0,s._)("span",{class:"text-bold q-ma-sm q-mb-sm q-ml-sm"},"Timestamp:",-1))),C=i((()=>(0,s._)("span",{class:"text-weight-bold q-mb-sm q-mr-sm"},"Description:",-1))),v=i((()=>(0,s._)("span",{class:"text-weight-bold q-mb-sm q-mr-sm"},"By:",-1))),D=i((()=>(0,s._)("span",{class:"text-weight-bold q-mb-sm q-mr-sm"},"Transaction:",-1))),A=i((()=>(0,s._)("div",{class:"text-h6"},"Log Detailed Information",-1))),$=i((()=>(0,s._)("div",{class:"text-subtitle1"}," Other fields not shown from the list were shown here. Not that some of the properties are not available for access, for instance, the file. Contact the student for the permission. ",-1))),L=i((()=>(0,s._)("span",{class:"text-weight-bold q-ma-sm q-mb-sm"},"Title:",-1))),P=i((()=>(0,s._)("span",{class:"text-weight-bold q-ma-sm q-mb-sm"},"Transaction:",-1))),G=i((()=>(0,s._)("span",{class:"text-weight-bold q-ma-sm q-mb-sm"},"Description:",-1))),z=i((()=>(0,s._)("span",{class:"text-weight-bold q-ma-sm q-mb-sm"},"Role:",-1))),Z=i((()=>(0,s._)("span",{class:"text-weight-bold q-ma-sm q-mb-sm"}," Inserter / Validated by:",-1))),V=i((()=>(0,s._)("span",{class:"text-weight-bold q-ma-sm q-mb-sm"}," File:",-1))),M=i((()=>(0,s._)("span",{class:"text-weight-bold q-ma-sm q-mb-sm"}," Duration Start:",-1))),H=i((()=>(0,s._)("span",{class:"text-weight-bold q-ma-sm q-mb-sm"}," Duration End:",-1))),j=i((()=>(0,s._)("span",{class:"text-weight-bold q-ma-sm q-mb-sm"}," Transaction Timestamp:",-1))),Q=(0,s.Uk)(" Portfolio Settings "),F={class:"text-h6 text-weight-bold"},Y=(0,s.Uk)(" Share Settings "),B=(0,s.Uk)(" Copies a link inlined with your portfolio's address for outside access. Note that this was enabled, only when the portfolio sharing was enabled. "),X=(0,s.Uk)(" The following switches are states that can affect the output of your portfolio. Which means everyone who access your portfolio is affected, "),J=i((()=>(0,s._)("strong",null,"including you",-1))),K=(0,s.Uk)(". "),ee=i((()=>(0,s._)("strong",null,"Be careful",-1))),te=(0,s.Uk)(", change these settings when necessary. Due to implementation issues, there will be a "),oe=i((()=>(0,s._)("strong",null,"cooldown of 5 seconds",-1))),se=(0,s.Uk)(" before it allows state changes. "),ae=(0,s.Uk)("Enable Portfolio Sharing"),le=(0,s.Uk)("Allow others to see this portfolio by explicitly referring to your address. Note that "),ie=i((()=>(0,s._)("strong",null,"file sharing option pre-requisites this",-1))),ne=(0,s.Uk)(", disabling forbids the requestor to access the file as an applicant / organization entity."),re=(0,s.Uk)("Show Email Info"),de=(0,s.Uk)("Allow others to see your email for contacting purposes. We recommend doing this "),_e=i((()=>(0,s._)("strong",null,"ONLY",-1))),ce=(0,s.Uk)(" when you are currently at job application."),me=(0,s.Uk)("Allow Files"),ue=(0,s.Uk)("Allow others to view and download your files. "),pe=i((()=>(0,s._)("strong",null,"Note that",-1))),fe=(0,s.Uk)(", these are your proof or supporting context behind these logs and extra information. "),ge=i((()=>(0,s._)("strong",null,"You are not liable",-1))),he=(0,s.Uk)(" when there's a data leakage as you are not the one who inserts these information."),be=i((()=>(0,s._)("div",{class:"text-h6 text-weight-bold"},"Editable Information",-1))),we=(0,s.Uk)(" Here are the fields that you can interchange even when blockchain already imprints the initial state of these fields. "),ye=i((()=>(0,s._)("strong",null,"Be careful",-1))),ke=(0,s.Uk)(", change only when necessary. ");function qe(e,t,o,i,qe,Ne){const Se=(0,s.up)("router-link"),Te=(0,s.up)("q-linear-progress"),Ee=(0,s.up)("q-card-section"),xe=(0,s.up)("q-item-label"),Ie=(0,s.up)("q-btn"),Oe=(0,s.up)("q-card-actions"),Ue=(0,s.up)("q-item-section"),Re=(0,s.up)("q-item"),We=(0,s.up)("q-scroll-area"),Ce=(0,s.up)("q-card"),ve=(0,s.up)("q-dialog"),De=(0,s.up)("q-tooltip"),Ae=(0,s.up)("q-page-sticky"),$e=(0,s.up)("q-tab"),Le=(0,s.up)("q-tabs"),Pe=(0,s.up)("q-separator"),Ge=(0,s.up)("q-toggle"),ze=(0,s.up)("q-list"),Ze=(0,s.up)("q-tab-panel"),Ve=(0,s.up)("q-input"),Me=(0,s.up)("q-form"),He=(0,s.up)("q-tab-panels"),je=(0,s.Q2)("close-popup"),Qe=(0,s.Q2)("ripple");return(0,s.wg)(),(0,s.iD)(s.HY,null,[(0,s._)("div",n,[(0,s._)("p",r,[d,(0,s.Wm)(Se,{to:"/explorer/address/"+e.portfolio_user_address,style:{"text-decoration":"none"}},{default:(0,s.w5)((()=>[(0,s.Uk)((0,a.zw)(e.portfolio_user_address),1)])),_:1},8,["to"]),_,(0,s.Uk)(" "+(0,a.zw)(e.portfolio_user_association),1)]),(0,s._)("p",null,[c,(0,s.Uk)((0,a.zw)(e.portfolio_user_email_contact),1)]),(0,s._)("p",null,[m,(0,s.Uk)(" "+(0,a.zw)(e.portfolio_user_program)+" ",1),u,(0,s.Uk)(" "+(0,a.zw)(e.portfolio_user_preferred_role),1)]),p,(0,s._)("p",null,[f,(0,s.Uk)(" "+(0,a.zw)(e.portfolio_user_description),1)]),(0,s._)("p",null,[g,(0,s.Uk)(" "+(0,a.zw)(e.portfolio_user_personal_skills),1)])]),(0,s._)("div",h,[(0,s._)("div",b,[e.portfolio_log_info_rendering_state?((0,s.wg)(),(0,s.j4)(Te,{key:0,query:"",color:"red",class:"q-mt-sm"})):(0,s.kq)("",!0),(0,s.Wm)(Ee,{style:{"margin-bottom":"0.5%"}},{default:(0,s.w5)((()=>[w,y])),_:1}),(0,s.Wm)(We,{style:{height:"100%","max-width":"100%"}},{default:(0,s.w5)((()=>[((0,s.wg)(!0),(0,s.iD)(s.HY,null,(0,s.Ko)(e.portfolio_log_container,(t=>((0,s.wg)(),(0,s.j4)(Re,{key:t.id,class:"logdata"},{default:(0,s.w5)((()=>[(0,s.Wm)(Ue,{class:"text-h6"},{default:(0,s.w5)((()=>[(0,s.Wm)(xe,null,{default:(0,s.w5)((()=>[(0,s._)("span",k,(0,a.zw)(t.context.name),1),q,N,(0,s.Uk)((0,a.zw)(t.context.role),1)])),_:2},1024),(0,s.Wm)(xe,{class:"q-ml-md",style:{"margin-top":"2%"}},{default:(0,s.w5)((()=>[S,(0,s.Uk)((0,a.zw)(t.context.description),1)])),_:2},1024),(0,s.Wm)(xe,{style:{"margin-top":"2%"}},{default:(0,s.w5)((()=>[T,(0,s.Wm)(Se,{to:"/explorer/address/"+t.context.validated_by,style:{"text-decoration":"none"}},{default:(0,s.w5)((()=>[(0,s.Uk)((0,a.zw)(t.context.validated_by),1)])),_:2},1032,["to"])])),_:2},1024),(0,s.Wm)(xe,{class:"q-ml-md",style:{"margin-top":"2%"}},{default:(0,s.w5)((()=>[E,(0,s.Uk)((0,a.zw)(t.context.timestamp)+" ",1),(0,s.Wm)(Oe,{align:"right"},{default:(0,s.w5)((()=>[(0,s.Wm)(Ie,{outline:"",right:"",color:"black",label:"View More",class:"q-mt-md",onClick:o=>e.getLogInfo(t.id)},null,8,["onClick"])])),_:2},1024)])),_:2},1024)])),_:2},1024)])),_:2},1024)))),128))])),_:1})]),(0,s._)("div",x,[e.portfolio_extra_info_rendering_state?((0,s.wg)(),(0,s.j4)(Te,{key:0,query:"",color:"red",class:"q-mt-sm"})):(0,s.kq)("",!0),(0,s.Wm)(Ee,{style:{"margin-bottom":"3.7%"}},{default:(0,s.w5)((()=>[I,O])),_:1}),(0,s.Wm)(We,{style:{height:"100%","max-width":"100%"}},{default:(0,s.w5)((()=>[((0,s.wg)(!0),(0,s.iD)(s.HY,null,(0,s.Ko)(e.portfolio_extra_container,(e=>((0,s.wg)(),(0,s.j4)(Re,{key:e.tx_hash,style:{"text-decoration":"none"},class:"logdata"},{default:(0,s.w5)((()=>[(0,s.Wm)(Ue,{class:"text-h6"},{default:(0,s.w5)((()=>[(0,s.Wm)(xe,{class:"q-mb-sm"},{default:(0,s.w5)((()=>[(0,s._)("span",U,(0,a.zw)(e.context.title),1),R,W,(0,s.Uk)((0,a.zw)(e.context.timestamp),1)])),_:2},1024),(0,s.Wm)(xe,{class:"q-ml-sm text-justify q-mb-sm q-ml-lg",style:{"margin-top":"2%"}},{default:(0,s.w5)((()=>[C,(0,s.Uk)((0,a.zw)(e.context.description),1)])),_:2},1024),(0,s.Wm)(xe,{class:"q-ml-sm text-justify q-mb-sm q-ml-lg",style:{"margin-top":"2%"}},{default:(0,s.w5)((()=>[v,(0,s.Wm)(Se,{to:"/explorer/address/"+e.context.inserter,style:{"text-decoration":"none"}},{default:(0,s.w5)((()=>[(0,s.Uk)((0,a.zw)(e.context.inserter),1)])),_:2},1032,["to"])])),_:2},1024),(0,s.Wm)(xe,{class:"q-ml-sm text-justify q-mb-sm q-ml-lg",style:{"margin-top":"2%"}},{default:(0,s.w5)((()=>[D,(0,s.Wm)(Se,{to:"/explorer/transaction/"+e.tx_hash,style:{"text-decoration":"none"}},{default:(0,s.w5)((()=>[(0,s.Uk)((0,a.zw)(e.context.inserter),1)])),_:2},1032,["to"])])),_:2},1024)])),_:2},1024)])),_:2},1024)))),128))])),_:1})])]),(0,s.Wm)(ve,{modelValue:e.logModalState,"onUpdate:modelValue":t[1]||(t[1]=t=>e.logModalState=t),class:"modal"},{default:(0,s.w5)((()=>[(0,s.Wm)(Ce,{class:"my-card-log"},{default:(0,s.w5)((()=>[(0,s.Wm)(Ee,null,{default:(0,s.w5)((()=>[A,$])),_:1}),(0,s.Wm)(Ee,{class:"wrap-content"},{default:(0,s.w5)((()=>[(0,s.Wm)(Re,null,{default:(0,s.w5)((()=>[(0,s.Wm)(Ue,{class:"text-h6"},{default:(0,s.w5)((()=>[(0,s.Wm)(xe,{class:"q-mb-md"},{default:(0,s.w5)((()=>[L,(0,s.Uk)((0,a.zw)(e.selectedLog.context.name),1)])),_:1}),(0,s.Wm)(xe,{class:"q-mb-md"},{default:(0,s.w5)((()=>[P,(0,s.Wm)(Se,{to:"/explorer/transaction/"+e.selectedLog.tx_hash,style:{"text-decoration":"none"}},{default:(0,s.w5)((()=>[(0,s.Uk)((0,a.zw)(e.selectedLog.tx_hash),1)])),_:1},8,["to"])])),_:1}),(0,s.Wm)(xe,{class:"q-mb-md"},{default:(0,s.w5)((()=>[G,(0,s.Uk)((0,a.zw)(e.selectedLog.context.description),1)])),_:1}),(0,s.Wm)(xe,{class:"q-mb-md"},{default:(0,s.w5)((()=>[z,(0,s.Uk)((0,a.zw)(e.selectedLog.context.role),1)])),_:1}),(0,s.Wm)(xe,{class:"q-mb-md"},{default:(0,s.w5)((()=>[Z,(0,s.Wm)(Se,{to:"/explorer/address/"+e.selectedLog.context.validated_by,style:{"text-decoration":"none"}},{default:(0,s.w5)((()=>[(0,s.Uk)((0,a.zw)(e.selectedLog.context.validated_by),1)])),_:1},8,["to"])])),_:1}),(0,s.Wm)(xe,{class:"q-mb-md"},{default:(0,s.w5)((()=>[V,(0,s.Wm)(Ie,{outline:"",color:"black",label:"View / Download",class:"q-mr-md",onClick:t[0]||(t[0]=t=>e.getFile(e.selectedLog.context.address_origin,e.selectedLog.context.file)),disable:null===e.selectedLog.context.file},null,8,["disable"])])),_:1}),(0,s.Wm)(xe,{class:"q-mb-md"},{default:(0,s.w5)((()=>[M,(0,s.Uk)((0,a.zw)(e.selectedLog.context.duration_start),1)])),_:1}),null!==e.selectedLog.context.duration_end?((0,s.wg)(),(0,s.j4)(xe,{key:0,class:"q-mb-md"},{default:(0,s.w5)((()=>[H,(0,s.Uk)((0,a.zw)(e.selectedLog.context.duration_end),1)])),_:1})):(0,s.kq)("",!0),(0,s.Wm)(xe,{class:"q-mb-md"},{default:(0,s.w5)((()=>[j,(0,s.Uk)((0,a.zw)(e.selectedLog.context.timestamp),1)])),_:1})])),_:1})])),_:1})])),_:1}),(0,s.Wm)(Oe,{align:"right",style:{"padding-bottom":"3%"}},{default:(0,s.w5)((()=>[(0,s.wy)((0,s.Wm)(Ie,{flat:"",label:"Close Modal",style:{color:"#f44336"},class:"q-mr-md"},null,512),[[je],[Qe]])])),_:1})])),_:1})])),_:1},8,["modelValue"]),(0,s.Wm)(Ae,{position:"bottom-right",offset:[24,24]},{default:(0,s.w5)((()=>[e.isStudent?(0,s.wy)(((0,s.wg)(),(0,s.j4)(Ie,{key:0,fab:"",icon:"mdi-file-cog",color:"red",onClick:t[2]||(t[2]=t=>e.portfolio_modal=!0)},{default:(0,s.w5)((()=>[(0,s.Wm)(De,{class:"bg-indigo",offset:[10,10],anchor:"center left",self:"center right"},{default:(0,s.w5)((()=>[Q])),_:1})])),_:1})),[[Qe]]):(0,s.kq)("",!0)])),_:1}),(0,s.Wm)(ve,{modelValue:e.portfolio_modal,"onUpdate:modelValue":t[13]||(t[13]=t=>e.portfolio_modal=t),class:"modal"},{default:(0,s.w5)((()=>[(0,s.Wm)(Ce,{style:{width:"100%"}},{default:(0,s.w5)((()=>[e.isProcessing?((0,s.wg)(),(0,s.j4)(Te,{key:0,rounded:"",query:"",indeterminate:"",color:"red"})):(0,s.kq)("",!0),(0,s.Wm)(Le,{modelValue:e.selected_settings,"onUpdate:modelValue":t[3]||(t[3]=t=>e.selected_settings=t),dense:"",class:"text-grey","active-color":"secondary","indicator-color":"secondary",align:"justify",style:{height:"50px"}},{default:(0,s.w5)((()=>[(0,s.Wm)($e,{name:"share_settings",label:"Settings",class:"tab",disable:e.isProcessing},null,8,["disable"]),(0,s.Wm)($e,{name:"editable_infos",label:"Editables",class:"tab",disable:e.isProcessing},null,8,["disable"])])),_:1},8,["modelValue"]),(0,s.Wm)(Pe),e.isStudent?((0,s.wg)(),(0,s.j4)(He,{key:1,modelValue:e.selected_settings,"onUpdate:modelValue":t[12]||(t[12]=t=>e.selected_settings=t),animated:"",class:"panels"},{default:(0,s.w5)((()=>[(0,s.Wm)(Ze,{name:"share_settings"},{default:(0,s.w5)((()=>[(0,s.Wm)(Ee,null,{default:(0,s.w5)((()=>[(0,s._)("div",F,[Y,e.isStudent?(0,s.wy)(((0,s.wg)(),(0,s.j4)(Ie,{key:0,flat:"",color:"indigo",style:{float:"right"},label:"Copy Portfolio Link",onClick:e.copyPortfolioLink,disable:!e.last_state_portfolio_sharing_state},{default:(0,s.w5)((()=>[(0,s.Wm)(De,{class:"bg-purple",offset:[10,10]},{default:(0,s.w5)((()=>[B])),_:1})])),_:1},8,["onClick","disable"])),[[Qe]]):(0,s.kq)("",!0)])])),_:1}),(0,s.Wm)(Ee,{class:"text-justify"},{default:(0,s.w5)((()=>[X,J,K])),_:1}),(0,s.Wm)(Ee,{class:"text-justify"},{default:(0,s.w5)((()=>[ee,te,oe,se])),_:1}),(0,s.Wm)(ze,{style:{"padding-top":"3%"}},{default:(0,s.w5)((()=>[(0,s.wy)(((0,s.wg)(),(0,s.j4)(Re,{tag:"label"},{default:(0,s.w5)((()=>[(0,s.Wm)(Ue,null,{default:(0,s.w5)((()=>[(0,s.Wm)(xe,null,{default:(0,s.w5)((()=>[ae])),_:1}),(0,s.Wm)(xe,{caption:""},{default:(0,s.w5)((()=>[le,ie,ne])),_:1})])),_:1}),(0,s.Wm)(Ue,{side:""},{default:(0,s.w5)((()=>[(0,s.Wm)(Ge,{color:"red",disable:e.isProcessing,modelValue:e.portfolio_sharing_state,"onUpdate:modelValue":t[4]||(t[4]=t=>e.portfolio_sharing_state=t)},null,8,["disable","modelValue"])])),_:1})])),_:1})),[[Qe]]),(0,s.wy)(((0,s.wg)(),(0,s.j4)(Re,{tag:"label"},{default:(0,s.w5)((()=>[(0,s.Wm)(Ue,null,{default:(0,s.w5)((()=>[(0,s.Wm)(xe,null,{default:(0,s.w5)((()=>[re])),_:1}),(0,s.Wm)(xe,{caption:""},{default:(0,s.w5)((()=>[de,_e,ce])),_:1})])),_:1}),(0,s.Wm)(Ue,{side:"",top:""},{default:(0,s.w5)((()=>[(0,s.Wm)(Ge,{color:"red",disable:e.isProcessing,modelValue:e.portfolio_show_email_state,"onUpdate:modelValue":t[5]||(t[5]=t=>e.portfolio_show_email_state=t)},null,8,["disable","modelValue"])])),_:1})])),_:1})),[[Qe]]),(0,s.wy)(((0,s.wg)(),(0,s.j4)(Re,{tag:"label"},{default:(0,s.w5)((()=>[(0,s.Wm)(Ue,null,{default:(0,s.w5)((()=>[(0,s.Wm)(xe,null,{default:(0,s.w5)((()=>[me])),_:1}),(0,s.Wm)(xe,{caption:""},{default:(0,s.w5)((()=>[ue,pe,fe,ge,he])),_:1})])),_:1}),(0,s.Wm)(Ue,{side:"",top:""},{default:(0,s.w5)((()=>[(0,s.Wm)(Ge,{color:"red",disable:e.isProcessing,modelValue:e.portfolio_allow_file_state,"onUpdate:modelValue":t[6]||(t[6]=t=>e.portfolio_allow_file_state=t)},null,8,["disable","modelValue"])])),_:1})])),_:1})),[[Qe]]),(0,s.Wm)(Oe,{align:"right"},{default:(0,s.w5)((()=>[(0,s.wy)((0,s.Wm)(Ie,{flat:"",style:{color:"#3700b3"},label:"Close Modal",onClick:t[7]||(t[7]=t=>e.portfolio_modal=!1)},null,512),[[Qe]]),(0,s.wy)((0,s.Wm)(Ie,{flat:"",style:{color:"#ff0080"},disable:e.portfolio_setting_btn_click_state,label:"Apply Settings",onClick:e.submitPortfolioSettings},null,8,["disable","onClick"]),[[Qe]])])),_:1})])),_:1})])),_:1}),(0,s.Wm)(Ze,{name:"editable_infos"},{default:(0,s.w5)((()=>[(0,s.Wm)(Me,{onSubmit:(0,l.iM)(e.submitEditableInfo,["prevent"]),onValidationError:e.submitEditableInfoOnError,autofocus:!0},{default:(0,s.w5)((()=>[(0,s.Wm)(Ee,null,{default:(0,s.w5)((()=>[be])),_:1}),(0,s.Wm)(Ee,{class:"text-justify"},{default:(0,s.w5)((()=>[we,ye,ke])),_:1}),(0,s.Wm)(Ee,null,{default:(0,s.w5)((()=>[(0,s.Wm)(Ve,{class:"input",outlined:"",dense:"",color:"secondary",modelValue:e.editable_info_preferred_role,"onUpdate:modelValue":t[8]||(t[8]=t=>e.editable_info_preferred_role=t),label:"Preferred Role",counter:"","lazy-rules":"",hint:"Your preferred role in the industry or in works.",disable:e.isProcessing,rules:[e=>e.length>=4&&e.length<=32||"This should contain not less than 4 characters or more than 32 characters."]},null,8,["modelValue","disable","rules"]),(0,s.Wm)(Ve,{class:"input",outlined:"",dense:"",color:"secondary",modelValue:e.editable_info_personal_skills,"onUpdate:modelValue":t[9]||(t[9]=t=>e.editable_info_personal_skills=t),label:"Personal Skills",counter:"",hint:"Similar to description but is specified to student's capability. Seperate the contents in comma. Please note only important or significant skills that you have.",rules:[e=>e&&e.length>=8||"This is required. Must have 8 characters and above."],"lazy-rules":"",disable:e.isProcessing},null,8,["modelValue","rules","disable"]),(0,s.Wm)(Ve,{class:"input",outlined:"",dense:"",color:"secondary",modelValue:e.editable_info_description,"onUpdate:modelValue":t[10]||(t[10]=t=>e.editable_info_description=t),type:"textarea",label:"Description",hint:"Literally, the description about you, but keep it professional as it was shown in your portfolio.",disable:e.isProcessing,counter:"",rules:[e=>e&&e.length>=8||"This is required. Must have 8 characters and above."],"lazy-rules":""},null,8,["modelValue","disable","rules"])])),_:1}),(0,s.Wm)(Oe,{align:"right"},{default:(0,s.w5)((()=>[(0,s.wy)((0,s.Wm)(Ie,{flat:"",style:{color:"#3700b3"},label:"Close Modal",onClick:t[11]||(t[11]=t=>e.portfolio_modal=!1)},null,512),[[Qe]]),(0,s.wy)((0,s.Wm)(Ie,{flat:"",type:"submit",style:{color:"#ff0080"},label:"Apply New Info",disable:e.editable_info_btn_click_state},null,8,["disable"]),[[Qe]])])),_:1})])),_:1},8,["onSubmit","onValidationError"])])),_:1})])),_:1},8,["modelValue"])):(0,s.kq)("",!0)])),_:1})])),_:1},8,["modelValue"])],64)}o(71),o(7965),o(6016);var Ne=o(1959),Se=o(1914),Te=o(8825),Ee=o(52),xe=o.n(Ee),Ie=o(2796),Oe=o(9582);const Ue=(0,s.aZ)({data(){return{portfolio_user_address:(0,Ne.iH)("—"),portfolio_user_association:(0,Ne.iH)("—"),portfolio_user_program:(0,Ne.iH)("—"),portfolio_user_description:(0,Ne.iH)("—"),portfolio_user_personal_skills:(0,Ne.iH)("—"),portfolio_user_preferred_role:(0,Ne.iH)("—"),portfolio_extra_container:(0,Ne.iH)([]),portfolio_log_container:(0,Ne.iH)([]),portfolio_user_email_contact:(0,Ne.iH)("—"),portfolio_modal:(0,Ne.iH)(!1),selected_settings:(0,Ne.iH)("share_settings"),portfolio_extra_info_rendering_state:(0,Ne.iH)(!0),portfolio_log_info_rendering_state:(0,Ne.iH)(!0),isProcessing:(0,Ne.iH)(!1),portfolio_sharing_state:(0,Ne.iH)(!1),portfolio_show_email_state:(0,Ne.iH)(!1),portfolio_allow_file_state:(0,Ne.iH)(!1),last_state_portfolio_sharing_state:(0,Ne.iH)(!1),portfolio_access_link:(0,Ne.iH)(null),portfolio_setting_btn_click_state:(0,Ne.iH)(!1),editable_info_btn_click_state:(0,Ne.iH)(!1),editable_info_description:(0,Ne.iH)(""),editable_info_preferred_role:(0,Ne.iH)(""),editable_info_personal_skills:(0,Ne.iH)(""),isStudent:(0,Ne.iH)(!1),isOrg:(0,Ne.iH)(!1),isAnonymous:(0,Ne.iH)(!1)}},setup(){const e=(0,Te.Z)(),t=(0,Oe.yj)(),o=(0,Oe.tv)();return{$q:e,$route:t,$router:o,logModalState:(0,Ne.iH)(!1),selectedLog:(0,Ne.iH)(null)}},mounted(){this.getPortfolio(),this.isStudent&&(this.loadPortfolioSettings(),this.loadEditableInfo())},methods:{loadPortfolioSettings(){this.isProcessing=!0,this.portfolio_setting_btn_click_state=!1,xe().get(`${Ie.sx}/dashboard/portfolio_settings`,{headers:{"X-Token":this.$q.localStorage.getItem("token")}}).then((e=>{this.portfolio_sharing_state=e.data.enable_sharing,this.portfolio_show_email_state=e.data.expose_email_info,this.portfolio_allow_file_state=e.data.show_files,this.last_state_portfolio_sharing_state=e.data.enable_sharing,this.last_state_portfolio_sharing_state&&(this.portfolio_access_link=`${Ie.uK}/#/portfolio?address=${this.$q.localStorage.getItem("address")}`),this.isProcessing=!1})).catch((e=>{const t=void 0===e.response.data?`${e.message}. Server may be unvailable. Please try again later.`:e.response.data.detail;this.$q.notify({color:"negative",position:"top",message:`There was an error when fetching your information. Due to this, switches will be disabled. Please refresh and try again. Reason: ${t}`,timeout:5e3,progress:!0,icon:"report_problem"})}))},loadEditableInfo(){this.isProcessing=!0,xe().get(`${Ie.sx}/dashboard/user_profile`,{headers:{"X-Token":this.$q.localStorage.getItem("token")}}).then((e=>{this.editable_info_description=e.data.description,this.editable_info_preferred_role=e.data.preferred_role,this.isProcessing=!1})).catch((e=>{const t=void 0===e.response.data?`${e.message}. Server may be unvailable. Please try again later.`:e.response.data.detail;this.$q.notify({color:"negative",position:"top",message:`There was an error when fetching your information. Due to this, fields will be disabled. Please refresh and try again. Reason: ${t}`,timeout:5e3,progress:!0,icon:"report_problem"})}))},submitEditableInfo(){this.editable_info_btn_click_state=!0,this.isProcessing=!0;let e=new FormData;e.append("description",this.editable_info_description),e.append("personal_skills",this.editable_info_personal_skills),e.append("preferred_role",this.editable_info_preferred_role),xe().post(`${Ie.sx}/dashboard/apply_profile_changes`,e,{headers:{"X-Token":this.$q.localStorage.getItem("token"),"Content-Type":"multipart/form-data"}}).then((e=>{this.$q.notify({color:"green",position:"top",message:"Editable information has been saved! Refreshing in 3 seconds ...",timeout:3e3,progress:!0,icon:"report_problem"}),setTimeout((()=>{this.$router.go()}),3e3)})).catch((e=>{const t=void 0===e.response.data?`${e.message}. Server may be unvailable. Please try again later.`:e.response.data.detail;this.$q.notify({color:"negative",position:"top",message:`There was an error when submitting new information. Reason: ${t}`,timeout:5e3,progress:!0,icon:"report_problem"})})),this.isProcessing=!1},submitEditableInfoOnError(){this.$q.notify({color:"negative",position:"top",message:"There was an error from one of the fields. Please check and try again.",timeout:5e3,progress:!0,icon:"report_problem"})},submitPortfolioSettings(){this.isProcessing=!0,this.portfolio_setting_btn_click_state=!0,xe().post(`${Ie.sx}/dashboard/apply_portfolio_settings`,{enable_sharing:this.portfolio_sharing_state,expose_email_info:this.portfolio_show_email_state,show_files:this.portfolio_allow_file_state},{headers:{"X-Token":this.$q.localStorage.getItem("token")}}).then((e=>{this.$q.notify({color:"green",position:"top",message:"Portfolio settings has been saved! Refreshing in 3 seconds ...",timeout:5e3,progress:!0,icon:"report_problem"}),setTimeout((()=>{this.$router.go()}),3e3)})).catch((e=>{const t=void 0===e.response.data?`${e.message}. Server may be unvailable. Please try again later.`:e.response.data.detail;this.$q.notify({color:"negative",position:"top",message:`There was an error when submitting portfolio settings. Due to this, lease refresh and try again. Reason: ${t}`,timeout:5e3,progress:!0,icon:"report_problem"})})),this.isProcessing=!1},getPortfolio(){let e=`${Ie.sx}/dashboard/portfolio`;if(void 0===this.$route.query.address&&null!==this.$q.localStorage.getItem("token")&&"Student Dashboard User"===this.$q.localStorage.getItem("role"))this.isStudent=!0;else if(void 0!==this.$route.query.address&&null!==this.$q.localStorage.getItem("token")&&"Organization Dashboard User"==this.$q.localStorage.getItem("role"))this.isOrg=!0,e+=`?address=${this.$route.query.address}`;else{if(void 0===this.$route.query.address||null!==this.$q.localStorage.getItem("token"))return this.$router.push({path:"Organization Dashboard User "===this.$q.localStorage.getItem("role")?"/dashboard":"/"}),void this.$q.notify({color:"negative",position:"top",message:"You are not allowed to access this view. If you are an anonymous, please ensure that the address you copied is exactly 35 characters or the address were not found.",timeout:5e3,progress:!0,icon:"report_problem"});this.isAnonymous=!0,e+=`?address=${this.$route.query.address}`}let t={headers:{"X-Token":this.$q.localStorage.getItem("token")}};xe().get(e,this.isOrg||this.isStudent?t:{}).then((e=>{this.$q.notify({color:"blue",position:"top",message:this.isAnonymous?"You are accessing this portfolio as an anonymous.":this.isOrg?"You are accessing this student's portfolio as a preview. Note that you cannot modify these entries anymore.":"You are accessing this as a student, please check your portfolio settings on the bottom-right to adjust your portfolio's output.",timeout:5e3,progress:!0,icon:"info"});let t=null;this.portfolio_user_address=e.data.address,this.portfolio_user_association=e.data.association,this.portfolio_user_program=e.data.program,this.portfolio_user_description=null===e.data.description?"No information":e.data.description,this.portfolio_user_personal_skills=null===e.data.personal_skills?"No information.":e.data.personal_skills,t=this.portfolio_user_personal_skills,this.editable_info_personal_skills=t,this.portfolio_user_preferred_role=e.data.preferred_role,this.portfolio_user_email_contact=null===e.data.email?"Not Available.":e.data.email,this.portfolio_extra_container=e.data.extra,this.portfolio_extra_info_rendering_state=!1;let o=1,s=[];for(let a of e.data.logs)a.id=o,a.context.duration_start=new Date(a.context.duration_start).toLocaleDateString(),null!==a.context.duration_end&&(a.context.duration_end=new Date(a.context.duration_end).toLocaleDateString()),s.push(a),o++;this.portfolio_log_container=s,this.portfolio_log_info_rendering_state=!1})).catch((e=>{const t=void 0===e.response.data?`${e.message}. Server may be unvailable. Please try again later.`:e.response.data.detail;this.$q.notify({color:"negative",position:"top",message:`There was an error when fetching portfolio. Reason: ${t}`,timeout:5e3,progress:!0,icon:"report_problem"}),this.$router.go(-1)}))},getLogInfo(e){this.logModalState=!0,this.selectedLog=this.portfolio_log_container[e-1]},getFile(e,t){let o=`${Ie.sx}/dashboard/portfolio/${e}/file/${t}`;xe().get(o,{responseType:"blob"}).then((e=>{let t=new Blob([e.data],{type:"application/pdf"}),o=window.URL.createObjectURL(t);window.open(o)})).catch((e=>{const t=void 0===e.response.data?`${e.message}. Server may be unvailable. Please try again later.`:e.response.data.detail;this.$q.notify({color:"negative",position:"top",message:`Cannot fetch the file. You may have disabled portfolio access. | Other Reason: ${t}`,timeout:5e3,progress:!0,icon:"report_problem"})}))},copyPortfolioLink(){(0,Se.Z)(this.portfolio_access_link).then((()=>{this.$q.notify({color:"green",position:"top",message:"Portfolio link copied to clipboard.",timeout:3e3,progress:!0,icon:"info"})})).catch((()=>{this.$q.notify({color:"negative",position:"top",message:"Cannot copy the portfolio link to the clipboard.",timeout:3e3,progress:!0,icon:"report_problem"})}))}}});var Re=o(4260),We=o(1598),Ce=o(5589),ve=o(7704),De=o(3414),Ae=o(2035),$e=o(2350),Le=o(9367),Pe=o(8240),Ge=o(6778),ze=o(151),Ze=o(1007),Ve=o(8870),Me=o(7547),He=o(3269),je=o(5869),Qe=o(5906),Fe=o(6602),Ye=o(7011),Be=o(8886),Xe=o(5269),Je=o(4689),Ke=o(677),et=o(6489),tt=o(7518),ot=o.n(tt);const st=(0,Re.Z)(Ue,[["render",qe],["__scopeId","data-v-344ea672"]]),at=st;ot()(Ue,"components",{QLinearProgress:We.Z,QCardSection:Ce.Z,QScrollArea:ve.Z,QItem:De.Z,QItemSection:Ae.Z,QItemLabel:$e.Z,QCardActions:Le.Z,QBtn:Pe.Z,QDialog:Ge.Z,QCard:ze.Z,QPageSticky:Ze.Z,QTooltip:Ve.Z,QTabs:Me.Z,QTab:He.Z,QSeparator:je.Z,QTabPanels:Qe.Z,QTabPanel:Fe.Z,QList:Ye.Z,QToggle:Be.Z,QForm:Xe.Z,QInput:Je.Z}),ot()(Ue,"directives",{ClosePopup:Ke.Z,Ripple:et.Z})}}]);