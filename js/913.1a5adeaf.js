(self["webpackChunkfolioblocks_web"]=self["webpackChunkfolioblocks_web"]||[]).push([[913],{2796:(e,o,s)=>{"use strict";s.d(o,{$T:()=>u,_u:()=>c,kb:()=>n,sx:()=>a,uK:()=>r});const t="https://",a=`${t}folioblocks.southeastasia.azurecontainer.io`,r=`${t}codexlink.github.io`,n=100,i=Object.freeze({NODE_GENERAL_CONSENSUS_INIT:1,NODE_GENERAL_REGISTER_INIT:2,NODE_GENERAL_GENESIS_BLOCK_INIT:3,NODE_GENERAL_CONSENSUS_BLOCK_SYNC:4,NODE_GENERAL_CONSENSUS_CONFIRM_NEGOTIATION_START:5,NODE_GENERAL_CONSENSUS_CONCLUDE_NEGOTIATION_PROCESSING:6,INSTITUTION_ORG_GENERATE_STUDENT:7,INSTITUTION_ORG_REFER_NEW_DOCUMENT_OR_IMPORTANT_INFO:8,INSTITUTION_ORG_STUDENT_REFER_EXTRA_INFO:9,ORGANIZATION_USER_REGISTER:10,ORGANIZATION_REFER_EXTRA_INFO:11}),l=Object.freeze({STUDENT_BASE:1,STUDENT_LOG:2,STUDENT_ADDITIONAL:3,ORGANIZATION_BASE:4}),d=Object.freeze({CONSENSUS:1,INIT:2,SYNC:3});function u(e){switch(e){case i.NODE_GENERAL_CONSENSUS_INIT:return"Consensus Initialization";case i.NODE_GENERAL_REGISTER_INIT:return"Node Registration";case i.NODE_GENERAL_GENESIS_BLOCK_INIT:return"Node Genesis Block Creation";case i.NODE_GENERAL_CONSENSUS_BLOCK_SYNC:return"Node Block Sync via Consensus";case i.NODE_GENERAL_CONSENSUS_CONFIRM_NEGOTIATION_START:return"Node Consensus Negotiation Confirmed Start";case i.NODE_GENERAL_CONSENSUS_CONCLUDE_NEGOTIATION_PROCESSING:return"Node Consensus Negotiation Conclusion of Processing";case i.INSTITUTION_ORG_GENERATE_STUDENT:return"Institution Student Generation";case i.INSTITUTION_ORG_REFER_NEW_DOCUMENT_OR_IMPORTANT_INFO:return"Institution New Document / Important Info to Student Reference";case i.INSTITUTION_ORG_STUDENT_REFER_EXTRA_INFO:return"Institution Refer Extra Info to Student";case i.ORGANIZATION_USER_REGISTER:return"Organization Registration";case i.ORGANIZATION_REFER_EXTRA_INFO:return"Extra Info Referral to Organization";default:return"Unidentified Action."}}function c(e){let o=e.hasOwnProperty("content_type")?"User Transaction":"Internal Transaction",s=null;if(e.hasOwnProperty("content_type"))switch(e.content_type){case l.STUDENT_BASE:s="Student Base Portfolio";break;case l.STUDENT_LOG:s="Student Log from Orgs";break;case l.STUDENT_ADDITIONAL:s="Student Additional Info / Remarks";break;case l.ORGANIZATION_BASE:s="Organization Base Registration";break;default:s="Unidentified";break}else switch(e.action){case d.CONSENSUS:s="Internal: Consensus Context";break;case d.INIT:s="Internal: Context Initialization";break;case d.SYNC:s="Internal: Sync from Communication";break;default:s="Unidentified";break}return{identifiedType:o,resolvedTypeValue:s}}},2913:(e,o,s)=>{"use strict";s.r(o),s.d(o,{default:()=>ee});var t=s(3673),a=s(8880),r=s(3585),n=s.n(r);const i=e=>((0,t.dD)("data-v-0d9fd6bd"),e=e(),(0,t.Cn)(),e),l=i((()=>(0,t._)("img",{class:"background",src:n(),style:{"background-attachment":"fixed"}},null,-1))),d=i((()=>(0,t._)("div",null,[(0,t._)("h2",null,"Hello! Welcome Back!"),(0,t._)("h4",null," Please login to get started. Or renew your token from logging in. ")],-1))),u={class:"btn"},c=i((()=>(0,t._)("div",null,[(0,t._)("h2",null,"Thank you for taking interest!"),(0,t._)("h4",null,[(0,t.Uk)(" Fill the fields below. Remember, "),(0,t._)("strong",null,"get the authentication code"),(0,t.Uk)(" from your supervisor for you to proceed your regisration. ")])],-1))),_=i((()=>(0,t._)("div",null,[(0,t._)("h4",null,[(0,t._)("strong",null,"Personal Information")]),(0,t._)("h4",null,[(0,t.Uk)(" Following fields are required to identify you "),(0,t._)("strong",null,"internally"),(0,t.Uk)(". Don't worry, your identity will not be exposed "),(0,t._)("strong",null,"except"),(0,t.Uk)(" the contact form which is the "),(0,t._)("strong",null,"email"),(0,t.Uk)(" you inputted from this form. ")])],-1))),g={class:"row"},m=i((()=>(0,t._)("div",null,[(0,t._)("h4",null,[(0,t._)("strong",null,"Organization Information")]),(0,t._)("h4",null,[(0,t.Uk)(" Following fields require to specify your organization as a new entity from the system. Should there be an existing organization must "),(0,t._)("strong",null,"only fill the organization address"),(0,t.Uk)(" as well as setting the organization type as "),(0,t._)("strong",null,"Existing"),(0,t.Uk)(" and nothing else. ")]),(0,t._)("h4",null,[(0,t.Uk)(" Note that, you have to be "),(0,t._)("strong",null,"very careful"),(0,t.Uk)(" from your inputs as these are unmodifiable due to nature of blockchain. ")])],-1))),h={class:"row"},p={class:"row items-center justify-end"},b={class:"row"},N=i((()=>(0,t._)("h4",null,[(0,t._)("strong",null,"Notice")],-1))),f=(0,t.Uk)(" Please ensure your inputs are correct before proceeding, there's no going back or be able to change them once submitted. "),y={class:"registerbtn"};function w(e,o,s,r,n,i){const w=(0,t.up)("q-linear-progress"),E=(0,t.up)("q-tab"),I=(0,t.up)("q-tabs"),T=(0,t.up)("q-separator"),S=(0,t.up)("q-input"),O=(0,t.up)("q-icon"),R=(0,t.up)("q-btn"),U=(0,t.up)("q-form"),v=(0,t.up)("q-tab-panel"),k=(0,t.up)("q-select"),V=(0,t.up)("q-date"),C=(0,t.up)("q-popup-proxy"),P=(0,t.up)("q-card-section"),A=(0,t.up)("q-tab-panels"),W=(0,t.up)("q-card"),D=(0,t.up)("RegisterContainer"),q=(0,t.Q2)("close-popup");return(0,t.wg)(),(0,t.iD)(t.HY,null,[l,(0,t._)("body",null,[(0,t.Wm)(D,null,{default:(0,t.w5)((()=>[(0,t.Wm)(W,null,{default:(0,t.w5)((()=>[e.isProcessing?((0,t.wg)(),(0,t.j4)(w,{key:0,query:"",color:"secondary",class:"q-mt-sm"})):(0,t.kq)("",!0),(0,t.Wm)(I,{modelValue:e.tab,"onUpdate:modelValue":o[0]||(o[0]=o=>e.tab=o),class:"text-grey tabs","active-color":"secondary","indicator-color":"secondary",align:"justify"},{default:(0,t.w5)((()=>[(0,t.Wm)(E,{name:"login",label:"Login"}),(0,t.Wm)(E,{name:"register",label:"Register"})])),_:1},8,["modelValue"]),(0,t.Wm)(T),(0,t.Wm)(A,{modelValue:e.tab,"onUpdate:modelValue":o[19]||(o[19]=o=>e.tab=o),animated:""},{default:(0,t.w5)((()=>[(0,t.Wm)(v,{name:"login"},{default:(0,t.w5)((()=>[(0,t.Wm)(U,{onSubmit:(0,a.iM)(e.submitLoginRequest,["prevent"]),onValidationError:e.errorOnSubmit,autofocus:!0},{default:(0,t.w5)((()=>[d,(0,t.Wm)(S,{class:"user",color:"secondary",outlined:"",disable:e.isProcessing,modelValue:e.login_username,"onUpdate:modelValue":o[1]||(o[1]=o=>e.login_username=o),label:"Username",rules:[e=>e&&e.length>0||"This is required."]},null,8,["disable","modelValue","rules"]),(0,t.Wm)(S,{class:"password",outlined:"",disable:e.isProcessing,color:"secondary",modelValue:e.login_password,"onUpdate:modelValue":o[3]||(o[3]=o=>e.login_password=o),label:"Password",type:e.login_show_password?"password":"text",rules:[e=>e&&e.length>0||"This is required."]},{append:(0,t.w5)((()=>[(0,t.Wm)(O,{name:e.login_show_password?"visibility_off":"visibility",class:"cursor-pointer",onClick:o[2]||(o[2]=o=>e.login_show_password=!e.login_show_password)},null,8,["name"])])),_:1},8,["disable","modelValue","type","rules"]),(0,t._)("div",u,[(0,t.Wm)(R,{class:"login",rounded:"",color:"red",label:"Back",to:"/"}),(0,t.Wm)(R,{class:"login",rounded:"",color:"secondary",label:"Login",type:"submit",disable:e.isProcessing},null,8,["disable"])])])),_:1},8,["onSubmit","onValidationError"])])),_:1}),(0,t.Wm)(v,{name:"register"},{default:(0,t.w5)((()=>[(0,t.Wm)(U,{onSubmit:(0,a.iM)(e.submitRegisterRequest,["prevent"]),onValidationError:e.errorOnSubmit,autofocus:!0},{default:(0,t.w5)((()=>[c,(0,t.Wm)(T),_,(0,t._)("div",g,[(0,t.Wm)(S,{class:"double",outlined:"",color:"secondary",modelValue:e.first_name,"onUpdate:modelValue":o[4]||(o[4]=o=>e.first_name=o),label:"First Name",counter:"",rules:[e=>e.length>=2&&e.length<=32||"Invalid, this is required. Should contain 2 to 32 characters."],"lazy-rules":"",disable:e.isProcessing},null,8,["modelValue","rules","disable"]),(0,t.Wm)(S,{class:"double",outlined:"",color:"secondary",modelValue:e.last_name,"onUpdate:modelValue":o[5]||(o[5]=o=>e.last_name=o),label:"Last Name",counter:"",rules:[e=>e.length>=2&&e.length<=32||"Invalid, this is required. Should contain 2 to 32 characters."],"lazy-rules":"",disable:e.isProcessing},null,8,["modelValue","rules","disable"])]),(0,t.Wm)(S,{class:"data",outlined:"",color:"secondary",modelValue:e.email,"onUpdate:modelValue":o[6]||(o[6]=o=>e.email=o),type:"email",label:"E-mail",counter:"","lazy-rules":"",disable:e.isProcessing,rules:[e=>e.includes("@")||"Invalid email format."]},null,8,["modelValue","disable","rules"]),(0,t.Wm)(T),m,(0,t._)("div",h,[(0,t.Wm)(S,{class:"double",outlined:"",color:"secondary",counter:"",modelValue:e.org_name,"onUpdate:modelValue":o[7]||(o[7]=o=>e.org_name=o),label:"Organization Name",hint:"Must be in Title Case.",rules:[e=>!e.length||e.length>=2&&e.length<=64||"Name should not be less than 1 character or more than 64 characters."],"lazy-rules":"",disable:e.isProcessing},null,8,["modelValue","rules","disable"]),(0,t.Wm)(S,{class:"double",outlined:"",counter:"",color:"secondary",modelValue:e.org_address,"onUpdate:modelValue":o[8]||(o[8]=o=>e.org_address=o),label:"Organization Address",hint:"Must\n                start with 'fl:'.",rules:[e=>!e.length||35==e.length&&e.startsWith("fl:")||"Invalid, format, follow the hint, and should be exactly 35 characters."],"lazy-rules":"",disable:e.isProcessing},null,8,["modelValue","rules","disable"])]),(0,t.Wm)(k,{class:"data",color:"secondary",outlined:"",modelValue:e.org_type_chosen,"onUpdate:modelValue":o[9]||(o[9]=o=>e.org_type_chosen=o),options:e.org_options,label:"Organization Type",disable:e.isProcessing},null,8,["modelValue","options","disable"]),(0,t.Wm)(S,{class:"data",outlined:"",color:"secondary",modelValue:e.org_description,"onUpdate:modelValue":o[10]||(o[10]=o=>e.org_description=o),type:"textarea",label:"Organization Description",counter:"",hint:"Be careful, content should be finalized before submitting.",rules:[e=>!e.length||e.length>=8&&e.length<=256||"Cannot go less than 8 characters or more than 256 characters."],"lazy-rules":"",disable:e.isProcessing},null,8,["modelValue","rules","disable"]),(0,t.Wm)(S,{filled:"",modelValue:e.org_date,"onUpdate:modelValue":o[12]||(o[12]=o=>e.org_date=o),class:"data",mask:"date",prefix:"Organization Founded",rules:["org_date"],"lazy-rules":"",readonly:"",hint:"The date from where your institution or your organization was founded.",disable:e.isProcessing},{append:(0,t.w5)((()=>[(0,t.Wm)(O,{name:"event",class:"cursor-pointer"},{default:(0,t.w5)((()=>[(0,t.Wm)(C,{ref:"qDateProxy",cover:"","transition-show":"scale","transition-hide":"scale"},{default:(0,t.w5)((()=>[(0,t.Wm)(V,{modelValue:e.org_date,"onUpdate:modelValue":o[11]||(o[11]=o=>e.org_date=o),color:"secondary","today-btn":"",options:e.optionsFn,disable:e.isProcessing},{default:(0,t.w5)((()=>[(0,t._)("div",p,[(0,t.wy)((0,t.Wm)(R,{label:"Close",color:"primary",flat:""},null,512),[[q]])])])),_:1},8,["modelValue","options","disable"])])),_:1},512)])),_:1})])),_:1},8,["modelValue","disable"]),(0,t.Wm)(T),(0,t.Wm)(S,{class:"data",outlined:"",color:"secondary",modelValue:e.register_username,"onUpdate:modelValue":o[13]||(o[13]=o=>e.register_username=o),label:"Username",counter:"",hint:"This will be used to login.",disable:e.isProcessing,rules:[e=>e.length>=8&&e.length<=24||"This should contain not less than 8 characters or more than 24 characters."],"lazy-rules":""},null,8,["modelValue","disable","rules"]),(0,t._)("div",b,[(0,t.Wm)(S,{class:"double",outlined:"",color:"secondary",modelValue:e.register_password,"onUpdate:modelValue":o[15]||(o[15]=o=>e.register_password=o),label:"Password",counter:"",type:e.register_show_password?"text":"password",disable:e.isProcessing,rules:[e=>e.length>=8&&e.length<=64||"This should contain not less than 8 characters or more than 64 characters."],"lazy-rules":""},{append:(0,t.w5)((()=>[(0,t.Wm)(O,{name:e.register_show_password?"visibility":"visibility_off",class:"cursor-pointer",onClick:o[14]||(o[14]=o=>e.register_show_password=!e.register_show_password)},null,8,["name"])])),_:1},8,["modelValue","type","disable","rules"]),(0,t.Wm)(S,{class:"double",outlined:"",color:"secondary",modelValue:e.register_confirm_password,"onUpdate:modelValue":o[17]||(o[17]=o=>e.register_confirm_password=o),label:"Confirm Password",counter:"",type:e.register_show_confirm_password?"text":"password",rules:[o=>o.length>=8&&o.length<=64&&o==e.register_password||"This should match your password to confirm your password."],disable:e.isProcessing},{append:(0,t.w5)((()=>[(0,t.Wm)(O,{name:e.register_show_confirm_password?"visibility":"visibility_off",class:"cursor-pointer",onClick:o[16]||(o[16]=o=>e.register_show_confirm_password=!e.register_show_confirm_password)},null,8,["name"])])),_:1},8,["modelValue","type","rules","disable"])]),(0,t.Wm)(S,{class:"data",outlined:"",color:"secondary",modelValue:e.register_auth_code,"onUpdate:modelValue":o[18]||(o[18]=o=>e.register_auth_code=o),type:"text",label:"Authentication Code",hint:"Remember, talk to your representatives to get your authentication code.",disable:e.isProcessing,rules:[e=>e.length||"This cannot be empty!"]},null,8,["modelValue","disable","rules"]),(0,t.Wm)(T),(0,t.Wm)(P,null,{default:(0,t.w5)((()=>[N,f])),_:1}),(0,t._)("div",y,[(0,t.Wm)(R,{class:"backbtn",rounded:"",color:"red",label:"Back",to:"/"}),(0,t.Wm)(R,{class:"register",rounded:"",color:"secondary",label:"Register",type:"submit",disable:e.isProcessing},null,8,["disable"])])])),_:1},8,["onSubmit","onValidationError"])])),_:1})])),_:1},8,["modelValue"])])),_:1})])),_:1})])],64)}s(5363),s(7768);var E=s(1959);const I={style:{"max-width":"100%","padding-bottom":"10%"}};function T(e,o){return(0,t.wg)(),(0,t.iD)("div",I,[(0,t.WI)(e.$slots,"default",{},void 0,!0)])}var S=s(4260);const O={},R=(0,S.Z)(O,[["render",T],["__scopeId","data-v-dd538fc8"]]),U=R;var v=s(9582),k=s(52),V=s.n(k),C=s(8825),P=s(2796);const A=(0,t.aZ)({name:"EntryForm",components:{RegisterContainer:U},data(){return{first_name:(0,E.iH)(""),last_name:(0,E.iH)(""),email:(0,E.iH)(""),org_name:(0,E.iH)(""),org_address:(0,E.iH)(""),org_description:(0,E.iH)(""),isProcessing:(0,E.iH)(!1),org_date:(0,E.iH)(""),register_username:(0,E.iH)(""),register_password:(0,E.iH)(""),register_confirm_password:(0,E.iH)(""),register_auth_code:(0,E.iH)(""),login_username:(0,E.iH)(""),login_password:(0,E.iH)(""),login_show_password:(0,E.iH)(!0),register_show_password:(0,E.iH)(!1),register_show_confirm_password:(0,E.iH)(!1)}},setup(){const e=(0,v.yj)();(0,v.tv)(),(0,C.Z)();return{tab:(0,E.iH)(e.params.action),org_options:[{label:"Existing",value:null},{label:"Institution",value:1},{label:"Organization",value:2}],org_type_chosen:(0,E.iH)({label:"Existing",value:null}),date:(new Date).toISOString().slice(0,10).replaceAll("-","/")}},methods:{submitLoginRequest(){this.isProcessing=!0,V().post(`${P.sx}/entity/login`,{username:this.login_username,password:this.login_password}).then((e=>{try{"Master Node User"==e.data.user_role||"Archival Miner Node User"==e.data.user_role?(this.$q.notify({color:"negative",position:"top",message:"Node-related account is not allowed to use the dashboard. Your account can be used in logging at folioblocks-node-cli.",timeout:5e3,progress:!0,icon:"mdi-account-cancel-outline"}),V().post(`${P.sx}/entity/logout`,{},{headers:{"X-Token":e.data.jwt_token}}),this.isProcessing=!1):(this.$q.localStorage.clear(),this.$q.localStorage.set("token",e.data.jwt_token),this.$q.localStorage.set("address",e.data.user_address),this.$q.localStorage.set("role",e.data.user_role),this.$q.notify({color:"green",position:"top",message:"Login successful!",timeout:5e3,progress:!0,icon:"mdi-account-check"}),this.$router.push({path:"/dashboard"}),this.isProcessing=!1)}catch(o){this.$q.clear(),this.isProcessing=!1}})).catch((e=>{const o=void 0===e.response.data?`${e.message}. Server may be unvailable. Please try again later.`:e.response.data.detail;this.$q.notify({color:"negative",position:"top",message:`There was an error when submitting your credentials. | Info: ${o}`,timeout:5e3,progress:!0,icon:"report_problem"}),this.isProcessing=!1}))},optionsFn(e){let o=new Date;return o.setDate(o.getDate()+1),new Date(null).toISOString().slice(0,10).replaceAll("-","/")>=e||e<=o.toISOString().slice(0,10).replaceAll("-","/")},submitRegisterRequest(){this.isProcessing=!0;let e={first_name:this.first_name,last_name:this.last_name,username:this.register_username,password:this.register_confirm_password,email:this.email,auth_code:this.register_auth_code},o=!1;this.org_name.length&&!this.org_address.length&&this.org_description.length&&(1==this.org_type_chosen.value||2==this.org_type_chosen.value)&&this.org_date.length?(e.association_name=this.org_name,e.association_type=this.org_type_chosen.value,e.association_founded=new Date(this.org_date).toISOString(),e.association_description=this.org_description,o=!0):this.org_name.length||!this.org_address.length||this.org_description.length||null!==this.org_type_chosen.value||this.org_date.length?this.$q.notify({color:"negative",position:"top",message:"There was an error when submitting your credentials. Please keep the organization address filled only when the organization exists, otherwise, fill other fields except for the organization address.",timeout:15e3,progress:!0,icon:"report_problem"}):(e.association_address=this.org_address,o=!0),o?V().post(`${P.sx}/entity/register`,{...e}).then((e=>{console.log(e),this.$q.notify({color:"green",position:"top",message:"Registration successful! Please check your email and login.",timeout:5e3,progress:!0,icon:"mdi-account-check"}),this.isProcessing=!1,this.$router.push({path:"/"})})).catch((e=>{const o=void 0===e.response.data?`${e.message}. Server may be unvailable. Please try again later.`:e.response.data.detail;this.$q.notify({color:"negative",position:"top",message:`There was an error when submitting your credentials. Reason: ${o}`,timeout:15e3,progress:!0,icon:"report_problem"}),this.isProcessing=!1})):(this.$q.notify({color:"negative",position:"top",message:"Payload condition regarding organization is not sufficient.",timeout:15e3,progress:!0,icon:"report_problem"}),this.isProcessing=!1)},errorOnSubmit(){this.$q.notify({color:"negative",position:"top",message:"There was an error from one of the fields. Please check and try again.",timeout:5e3,progress:!0,icon:"report_problem"})}}});var W=s(151),D=s(1598),q=s(7547),G=s(3269),z=s(5869),x=s(5906),L=s(6602),Z=s(5269),$=s(4689),F=s(4554),H=s(8240),B=s(3314),Q=s(3944),M=s(6915),j=s(5589),Y=s(677),K=s(7518),X=s.n(K);const J=(0,S.Z)(A,[["render",w],["__scopeId","data-v-0d9fd6bd"]]),ee=J;X()(A,"components",{QCard:W.Z,QLinearProgress:D.Z,QTabs:q.Z,QTab:G.Z,QSeparator:z.Z,QTabPanels:x.Z,QTabPanel:L.Z,QForm:Z.Z,QInput:$.Z,QIcon:F.Z,QBtn:H.Z,QSelect:B.Z,QPopupProxy:Q.Z,QDate:M.Z,QCardSection:j.Z}),X()(A,"directives",{ClosePopup:Y.Z})},3585:(e,o,s)=>{e.exports=s.p+"img/pagebackground.496a4276.png"}}]);