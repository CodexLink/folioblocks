"use strict";(self["webpackChunkfolioblocks"]=self["webpackChunkfolioblocks"]||[]).push([[209],{2796:(t,e,o)=>{o.d(e,{$T:()=>c,_u:()=>d,kb:()=>s,mX:()=>n});const a=process.env.TARGET_MASTER_NODE_ADDRESS,r=process.env.TARGET_MASTER_NODE_PORT,n=`${a}:${r}`,s=100,i=Object.freeze({NODE_GENERAL_CONSENSUS_INIT:1,NODE_GENERAL_REGISTER_INIT:2,NODE_GENERAL_GENESIS_BLOCK_INIT:3,NODE_GENERAL_CONSENSUS_BLOCK_SYNC:4,NODE_GENERAL_CONSENSUS_CONFIRM_NEGOTIATION_START:5,NODE_GENERAL_CONSENSUS_CONCLUDE_NEGOTIATION_PROCESSING:6,INSTITUTION_ORG_GENERATE_STUDENT:7,INSTITUTION_ORG_REFER_NEW_DOCUMENT_OR_IMPORTANT_INFO:8,INSTITUTION_ORG_STUDENT_REFER_EXTRA_INFO:9,ORGANIZATION_USER_REGISTER:10,ORGANIZATION_REFER_EXTRA_INFO:11}),_=Object.freeze({STUDENT_BASE:1,STUDENT_LOG:2,STUDENT_ADDITIONAL:3,ORGANIZATION_BASE:4}),l=Object.freeze({CONSENSUS:1,INIT:2,SYNC:3});function c(t){switch(t){case i.NODE_GENERAL_CONSENSUS_INIT:return"Consensus Initialization";case i.NODE_GENERAL_REGISTER_INIT:return"Node Registration";case i.NODE_GENERAL_GENESIS_BLOCK_INIT:return"Node Genesis Block Creation";case i.NODE_GENERAL_CONSENSUS_BLOCK_SYNC:return"Node Block Sync via Consensus";case i.NODE_GENERAL_CONSENSUS_CONFIRM_NEGOTIATION_START:return"Node Consensus Negotiation Confirmed Start";case i.NODE_GENERAL_CONSENSUS_CONCLUDE_NEGOTIATION_PROCESSING:return"Node Consensus Negotiation Conclusion of Processing";case i.INSTITUTION_ORG_GENERATE_STUDENT:return"Institution Student Generation";case i.INSTITUTION_ORG_REFER_NEW_DOCUMENT_OR_IMPORTANT_INFO:return"Institution New Document / Important Info to Student Reference";case i.INSTITUTION_ORG_STUDENT_REFER_EXTRA_INFO:return"Institution Refer Extra Info to Student";case i.ORGANIZATION_USER_REGISTER:return"Organization Registration";case i.ORGANIZATION_REFER_EXTRA_INFO:return"Extra Info Referral to Organization";default:return"Unidentified Action."}}function d(t){let e=t.hasOwnProperty("content_type")?"User Transaction":"Internal Transaction",o=null;if(t.hasOwnProperty("content_type"))switch(t.content_type){case _.STUDENT_BASE:o="Student Base Portfolio";break;case _.STUDENT_LOG:o="Student Log from Orgs";break;case _.STUDENT_ADDITIONAL:o="Student Additional Info / Remarks";break;case _.ORGANIZATION_BASE:o="Organization Base Registration";break;default:o="Unidentified";break}else switch(t.action){case l.CONSENSUS:o="Internal: Consensus Context";break;case l.INIT:o="Internal: Context Initialization";break;case l.SYNC:o="Internal: Sync from Communication";break;default:o="Unidentified";break}return{identifiedType:e,resolvedTypeValue:o}}},2209:(t,e,o)=>{o.r(e),o.d(e,{default:()=>Z});var a=o(3673),r=o(2323);const n=t=>((0,a.dD)("data-v-4585f852"),t=t(),(0,a.Cn)(),t),s={class:"header"},i={class:"text-white"},_={class:"alias text-white"},l={class:"alias text-white"},c=(0,a.Uk)(" Identified as "),d=(0,a.Uk)(" or "),u={class:"btn"},p={class:"main"},h={class:"output"},g={class:"data"},N={class:"title"},f={class:"text-h6"},E=n((()=>(0,a._)("p",{class:"text-caption"},"Log Percentage by Bar",-1))),m=n((()=>(0,a._)("p",{class:"text-caption"},"Extra Percentage by Bar",-1))),b={class:"output"},x={class:"data"},T={class:"title"};function I(t,e,o,n,I,O){const S=(0,a.up)("q-btn"),R=(0,a.up)("q-card-section"),A=(0,a.up)("q-card"),y=(0,a.up)("q-linear-progress"),C=(0,a.up)("q-icon"),v=(0,a.up)("q-separator"),w=(0,a.up)("q-layout");return(0,a.wg)(),(0,a.j4)(w,{view:"hHh lpR lFf"},{default:(0,a.w5)((()=>[(0,a._)("body",null,[(0,a._)("div",s,[(0,a.Wm)(A,{class:"profile",style:{"background-image":"url(https://cdn.quasar.dev/img/parallax2.jpg)","object-fit":"cover","-webkit-filter":"brightness(95%)",filter:"brightness(95%)"}},{default:(0,a.w5)((()=>[(0,a.Wm)(R,null,{default:(0,a.w5)((()=>[(0,a._)("h2",i,"Hello "+(0,r.zw)(t.first_name)+" "+(0,r.zw)(t.last_name)+"!",1),(0,a._)("h4",_,[(0,a._)("strong",null,(0,r.zw)(t.user_role),1)]),(0,a._)("p",l,[c,(0,a._)("strong",null,(0,r.zw)(t.user_address),1),d,(0,a._)("strong",null,(0,r.zw)(t.user_name),1)]),(0,a._)("div",u,[(0,a.Wm)(S,{outline:"",rounded:"",color:"white",label:t.button_left,to:t.button_left_link},null,8,["label","to"]),(0,a.Wm)(S,{outline:"",rounded:"",color:"white",label:t.button_right,to:t.button_right_link,disable:"Student Dashboard User"===t.user_role},null,8,["label","to","disable"])])])),_:1})])),_:1})]),(0,a._)("div",p,[(0,a.Wm)(A,{class:"blocks"},{default:(0,a.w5)((()=>[(0,a.Wm)(y,{value:t.context_right_progress_top,rounded:"",reverse:"",color:"red"},null,8,["value"]),(0,a.Wm)(C,{name:t.context_right_top_icon,color:"red",size:"6em",style:{"padding-left":"20px","padding-top":"10px"}},null,8,["name"]),(0,a._)("div",h,[(0,a._)("p",g,(0,r.zw)(t.context_right_top),1),(0,a._)("p",N,(0,r.zw)(t.context_right_top_primary),1)])])),_:1}),(0,a.Wm)(A,{flat:"",bordered:"",class:"seminar"},{default:(0,a.w5)((()=>[(0,a.Wm)(R,null,{default:(0,a.w5)((()=>[(0,a._)("div",f,(0,r.zw)(t.context_left),1)])),_:1}),(0,a.Wm)(R,{class:"q-pt-none"},{default:(0,a.w5)((()=>[(0,a.Uk)((0,r.zw)(t.context_left_primary),1)])),_:1}),(0,a.Wm)(R,{class:"q-pt-none"},{default:(0,a.w5)((()=>[(0,a.Wm)(y,{value:t.context_left_progress_top,rounded:"",color:"red",class:"q-mt-sm"},null,8,["value"]),E,(0,a.Wm)(y,{value:t.context_left_progress_bottom,rounded:"",color:"secondary",class:"q-mt-sm"},null,8,["value"]),m])),_:1}),(0,a.Wm)(v),(0,a.Wm)(R,null,{default:(0,a.w5)((()=>[(0,a.Uk)((0,r.zw)(t.context_left_secondary),1)])),_:1})])),_:1}),(0,a.Wm)(A,{class:"transaction"},{default:(0,a.w5)((()=>[(0,a.Wm)(y,{value:t.context_right_progress_bottom,rounded:"",reverse:"",color:"secondary"},null,8,["value"]),(0,a.Wm)(C,{name:t.context_right_bottom_icon,class:"secondary",size:"6em",color:"secondary",style:{"padding-left":"20px","padding-top":"12px"}},null,8,["name"]),(0,a._)("div",b,[(0,a._)("p",x,(0,r.zw)(t.context_right_bottom),1),(0,a._)("p",T,(0,r.zw)(t.context_right_bottom_primary),1)])])),_:1})])])])),_:1})}var O=o(1959),S=o(8825),R=o(52),A=o.n(R),y=o(2796),C=o(9582);let v={student:{buttons:["View Portfolio","—"],links:["/portfolio","#"],context:{left:{title:"Percentage of Logs vs Extra Info",subtitle:"Here contains the progress bar-based visualization on how much you have from both the logs and extra info.",another:"Note that this is the last state since the page has been loaded. Refresh to update this information."},right_top:{title:"Total Credentials Received",icon:"mdi-file-star"},right_bottom:{title:"Portfolio Current Settings",icon:"mdi-file-cog"}}},organization:{buttons:["Generate User","Refer Credentials"],links:["/org/insert/new","/org/insert/standby"],context:{left:{title:"Logs vs Extra Info Dominance",subtitle:"The following visualization is a percetange-equivalent of logs vs extra information being inserted frequently.",another:"The progression bar only visualizes and thurs an estimation as per page refresh."},right_top:{title:"Total Associations",icon:"mdi-account-group"},right_bottom:{title:"Total Student Credentials Inserted",icon:"mdi-file-multiple"}}}};const w=(0,a.aZ)({name:"Dashboard",components:{},data(){return{button_left:(0,O.iH)("—"),button_right:(0,O.iH)("—"),button_left_link:(0,O.iH)("#"),button_right_link:(0,O.iH)("#"),first_name:(0,O.iH)("—"),last_name:(0,O.iH)("—"),user_address:(0,O.iH)("—"),user_role:(0,O.iH)("—"),user_name:(0,O.iH)("—"),context_left:(0,O.iH)("—"),context_left_primary:(0,O.iH)("—"),context_left_secondary:(0,O.iH)("—"),context_right_top:(0,O.iH)("—"),context_right_bottom:(0,O.iH)("—"),context_right_top_primary:(0,O.iH)("—"),context_right_bottom_primary:(0,O.iH)("—"),context_right_top_secondary:(0,O.iH)("—"),context_right_bottom_secondary:(0,O.iH)("—"),context_left_progress_top:(0,O.iH)(0),context_left_progress_bottom:(0,O.iH)(0),context_right_top_icon:(0,O.iH)(""),context_right_bottom_icon:(0,O.iH)(""),context_right_progress_top:(0,O.iH)(0),context_right_progress_bottom:(0,O.iH)(0)}},setup(){(0,C.yj)(),(0,C.tv)(),(0,S.Z)()},mounted(){this.getUserDashboardContext()},methods:{getUserDashboardContext(){A().get(`http://${y.mX}/dashboard`,{headers:{"X-Token":this.$q.localStorage.getItem("token")}}).then((t=>{if(this.first_name=t.data.first_name,this.last_name=t.data.last_name,this.user_address=t.data.address,this.user_role=t.data.role,this.user_name=t.data.username,"Organization Dashboard User"===this.user_role)this.button_left=v.organization.buttons[0],this.button_left_link=v.organization.links[0],this.button_right=v.organization.buttons[1],this.button_right_link=v.organization.links[1],this.context_right_top_icon=v.organization.context.right_top.icon,this.context_right_top=v.organization.context.right_top.title,this.context_right_top_primary=`Currently, there was ${t.data.reports.total_associated} out of ${t.data.reports.total_users} associated users from your organization.`,this.context_right_progress_top=t.data.reports.total_associated/t.data.reports.total_users,this.context_left=v.organization.context.left.title,this.context_left_primary=v.organization.context.left.subtitle,this.context_left_secondary=v.organization.context.left.another,this.context_left_progress_top=t.data.reports.total_associated_logs/t.data.reports.total_overall_info_outside,this.context_left_progress_bottom=t.data.reports.total_associated_extra/t.data.reports.total_overall_info_outside,this.context_right_bottom_icon=v.organization.context.right_bottom.icon,this.context_right_bottom=v.organization.context.right_bottom.title,this.context_right_bottom_primary=`Your organization was able to insert ${t.data.reports.total_associated_logs+t.data.reports.total_associated_extra} out of ${t.data.reports.total_overall_info_outside} student credentials.`,this.context_right_progress_bottom=(t.data.reports.total_associated_logs+t.data.reports.total_associated_extra)/t.data.reports.total_overall_info_outside;else{this.button_left=v.student.buttons[0],this.button_left_link=v.student.links[0],this.button_right=v.student.buttons[1],this.button_right_link=v.student.links[1],this.context_right_top=v.student.context.right_top.title,this.context_right_top_primary=`You currently have ${t.data.reports.logs_associated_count+t.data.reports.extra_associated_count} out of ${t.data.reports.total_txs_overall} given credential/s by your organization.`,this.context_right_progress_top=(t.data.reports.logs_associated_count+t.data.reports.extra_associated_count)/t.data.reports.total_txs_overall,this.context_right_top_icon=v.student.context.right_top.icon,this.context_left=v.student.context.left.title,this.context_left_primary=v.student.context.left.subtitle,this.context_left_secondary=v.student.context.left.another,this.context_left_progress_top=t.data.reports.logs_associated_count/t.data.reports.total_txs_overall,this.context_left_progress_bottom=t.data.reports.extra_associated_count/t.data.reports.total_txs_overall,this.context_right_bottom=v.student.context.right_bottom.title,this.context_right_bottom_primary=`Currently '${t.data.reports.portfolio.enable_sharing?"public":"private"}', e-mail contact info is currently '${t.data.reports.portfolio.expose_email_info?"exposed":"hidden"}, and files were '${t.data.reports.portfolio.show_files?"viewable":"hidden"}'.`,this.context_right_bottom_icon=v.student.context.right_bottom.icon;let e=0,o=0;for(let a in t.data.reports.portfolio)a&&e++,o++;this.context_right_progress_bottom=e/o}})).catch((t=>{this.$q.notify({color:"red",position:"top",message:"Failed to parse data from the dashboard. Please try again.",timeout:1e4,progress:!0,icon:"mdi-cancel"})}))}}});var G=o(4260),U=o(9214),k=o(151),D=o(5589),z=o(8240),L=o(1598),H=o(4554),W=o(5869),q=o(7518),F=o.n(q);const P=(0,G.Z)(w,[["render",I],["__scopeId","data-v-4585f852"]]),Z=P;F()(w,"components",{QLayout:U.Z,QCard:k.Z,QCardSection:D.Z,QBtn:z.Z,QLinearProgress:L.Z,QIcon:H.Z,QSeparator:W.Z})}}]);