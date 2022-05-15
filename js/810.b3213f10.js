(self["webpackChunkfolioblocks_web"]=self["webpackChunkfolioblocks_web"]||[]).push([[810],{2796:(e,o,s)=>{"use strict";s.d(o,{$T:()=>_,_u:()=>u,kb:()=>a,sx:()=>i,uK:()=>t});const r="https://",i=`${r}folioblocks.southeastasia.azurecontainer.io`,t=`${r}codexlink.github.io/folioblocks`,a=100,n=Object.freeze({NODE_GENERAL_CONSENSUS_INIT:1,NODE_GENERAL_REGISTER_INIT:2,NODE_GENERAL_GENESIS_BLOCK_INIT:3,NODE_GENERAL_CONSENSUS_BLOCK_SYNC:4,NODE_GENERAL_CONSENSUS_CONFIRM_NEGOTIATION_START:5,NODE_GENERAL_CONSENSUS_CONCLUDE_NEGOTIATION_PROCESSING:6,INSTITUTION_ORG_GENERATE_STUDENT:7,INSTITUTION_ORG_REFER_NEW_DOCUMENT_OR_IMPORTANT_INFO:8,INSTITUTION_ORG_STUDENT_REFER_EXTRA_INFO:9,ORGANIZATION_USER_REGISTER:10,ORGANIZATION_REFER_EXTRA_INFO:11}),l=Object.freeze({STUDENT_BASE:1,STUDENT_LOG:2,STUDENT_ADDITIONAL:3,ORGANIZATION_BASE:4}),d=Object.freeze({CONSENSUS:1,INIT:2,SYNC:3});function _(e){switch(e){case n.NODE_GENERAL_CONSENSUS_INIT:return"Consensus Initialization";case n.NODE_GENERAL_REGISTER_INIT:return"Node Registration";case n.NODE_GENERAL_GENESIS_BLOCK_INIT:return"Node Genesis Block Creation";case n.NODE_GENERAL_CONSENSUS_BLOCK_SYNC:return"Node Block Sync via Consensus";case n.NODE_GENERAL_CONSENSUS_CONFIRM_NEGOTIATION_START:return"Node Consensus Negotiation Confirmed Start";case n.NODE_GENERAL_CONSENSUS_CONCLUDE_NEGOTIATION_PROCESSING:return"Node Consensus Negotiation Conclusion of Processing";case n.INSTITUTION_ORG_GENERATE_STUDENT:return"Institution Student Generation";case n.INSTITUTION_ORG_REFER_NEW_DOCUMENT_OR_IMPORTANT_INFO:return"Institution New Document / Important Info to Student Reference";case n.INSTITUTION_ORG_STUDENT_REFER_EXTRA_INFO:return"Institution Refer Extra Info to Student";case n.ORGANIZATION_USER_REGISTER:return"Organization Registration";case n.ORGANIZATION_REFER_EXTRA_INFO:return"Extra Info Referral to Organization";default:return"Unidentified Action."}}function u(e){let o=e.hasOwnProperty("content_type")?"User Transaction":"Internal Transaction",s=null;if(e.hasOwnProperty("content_type"))switch(e.content_type){case l.STUDENT_BASE:s="Student Base Portfolio";break;case l.STUDENT_LOG:s="Student Log from Orgs";break;case l.STUDENT_ADDITIONAL:s="Student Additional Info / Remarks";break;case l.ORGANIZATION_BASE:s="Organization Base Registration";break;default:s="Unidentified";break}else switch(e.action){case d.CONSENSUS:s="Internal: Consensus Context";break;case d.INIT:s="Internal: Context Initialization";break;case d.SYNC:s="Internal: Sync from Communication";break;default:s="Unidentified";break}return{identifiedType:o,resolvedTypeValue:s}}},810:(e,o,s)=>{"use strict";s.r(o),s.d(o,{default:()=>_e});var r=s(3673),i=s(8880),t=s(3585),a=s.n(t);const n=e=>((0,r.dD)("data-v-71a7272c"),e=e(),(0,r.Cn)(),e),l=n((()=>(0,r._)("img",{class:"background",src:a(),style:{"background-attachment":"fixed"}},null,-1))),d=n((()=>(0,r._)("div",null,[(0,r._)("h2",null,"Hello! Welcome Back!"),(0,r._)("h4",null," Please login to get started. Or renew your token from logging in. ")],-1))),_={class:"btn"},u=n((()=>(0,r._)("div",null,[(0,r._)("h2",null,"Thank you for taking interest!"),(0,r._)("h4",null,[(0,r.Uk)(" Fill the fields below. Remember, "),(0,r._)("strong",null,"get the authentication code"),(0,r.Uk)(" from your supervisor for you to proceed your regisration. ")])],-1))),c=n((()=>(0,r._)("div",null,[(0,r._)("h4",null,[(0,r._)("strong",null,"Personal Information")]),(0,r._)("h4",null,[(0,r.Uk)(" Following fields are required to identify you "),(0,r._)("strong",null,"internally"),(0,r.Uk)(". Don't worry, your identity will not be exposed "),(0,r._)("strong",null,"except"),(0,r.Uk)(" the contact form which is the "),(0,r._)("strong",null,"email"),(0,r.Uk)(" you inputted from this form. ")])],-1))),g={class:"row"},h=n((()=>(0,r._)("div",null,[(0,r._)("h4",null,[(0,r._)("strong",null,"Organization Information")]),(0,r._)("h4",null,[(0,r.Uk)(" Following fields require to specify your organization as a new entity from the system. Should there be an existing organization must "),(0,r._)("strong",null,"only fill the organization address"),(0,r.Uk)(" as well as setting the organization type as "),(0,r._)("strong",null,"Existing"),(0,r.Uk)(" and nothing else. ")]),(0,r._)("h4",null,[(0,r.Uk)(" Note that, you have to be "),(0,r._)("strong",null,"very careful"),(0,r.Uk)(" from your inputs as these are unmodifiable due to nature of blockchain. ")])],-1))),m={class:"row"},p=(0,r.Uk)(" If you are inserting an existing organization, please clear this field. "),b=(0,r.Uk)(" This may be required. If you are inserting a new organization, please clear this field, otherwise, proceed. "),f=(0,r.Uk)(" For existing organization, please choose "),y=n((()=>(0,r._)("strong",null,"existing",-1))),N=(0,r.Uk)(" and fill up "),w=n((()=>(0,r._)("strong",null,"ONLY",-1))),E=(0,r.Uk)(" the organization address, otherwise, fill other fields that shows an error. "),v=(0,r.Uk)(" This may be required. If you are inserting an existing organization, please clear this field, otherwise, add a date. "),I={class:"row items-center justify-end"},T=(0,r.Uk)(" This may be required. If you are inserting an existing organization, please clear this field, otherwise, check for other fields. "),S={class:"row"},O=(0,r.Uk)(" Authentication code is invalid. Check your email inbox and try again. "),R=n((()=>(0,r._)("h4",null,[(0,r._)("strong",null,"Notice")],-1))),k=(0,r.Uk)(" Please ensure your inputs are correct before proceeding, there's no going back or be able to change them once submitted. "),U={class:"registerbtn"};function C(e,o,s,t,a,n){const C=(0,r.up)("q-linear-progress"),V=(0,r.up)("q-tab"),A=(0,r.up)("q-tabs"),P=(0,r.up)("q-separator"),W=(0,r.up)("q-input"),q=(0,r.up)("q-icon"),D=(0,r.up)("q-btn"),G=(0,r.up)("q-form"),z=(0,r.up)("q-tab-panel"),x=(0,r.up)("q-select"),L=(0,r.up)("q-date"),F=(0,r.up)("q-popup-proxy"),H=(0,r.up)("q-card-section"),Z=(0,r.up)("q-tab-panels"),$=(0,r.up)("q-card"),B=(0,r.up)("RegisterContainer"),Q=(0,r.Q2)("close-popup");return(0,r.wg)(),(0,r.iD)(r.HY,null,[l,(0,r._)("body",null,[(0,r.Wm)(B,null,{default:(0,r.w5)((()=>[(0,r.Wm)($,null,{default:(0,r.w5)((()=>[e.isProcessing?((0,r.wg)(),(0,r.j4)(C,{key:0,query:"",color:"secondary",class:"q-mt-sm"})):(0,r.kq)("",!0),(0,r.Wm)(A,{modelValue:e.tab,"onUpdate:modelValue":o[0]||(o[0]=o=>e.tab=o),class:"text-grey tabs","active-color":"secondary","indicator-color":"secondary",align:"justify"},{default:(0,r.w5)((()=>[(0,r.Wm)(V,{name:"login",label:"Login"}),(0,r.Wm)(V,{name:"register",label:"Register"})])),_:1},8,["modelValue"]),(0,r.Wm)(P),(0,r.Wm)(Z,{modelValue:e.tab,"onUpdate:modelValue":o[26]||(o[26]=o=>e.tab=o),animated:""},{default:(0,r.w5)((()=>[(0,r.Wm)(z,{name:"login"},{default:(0,r.w5)((()=>[(0,r.Wm)(G,{onSubmit:(0,i.iM)(e.submitLoginRequest,["prevent"]),onValidationError:e.errorOnSubmit,autofocus:!0},{default:(0,r.w5)((()=>[d,(0,r.Wm)(W,{class:"user",color:"secondary",outlined:"",disable:e.isProcessing,modelValue:e.login_username,"onUpdate:modelValue":o[1]||(o[1]=o=>e.login_username=o),label:"Username",rules:[e=>e&&e.length>0||"This is required."]},null,8,["disable","modelValue","rules"]),(0,r.Wm)(W,{class:"password",outlined:"",disable:e.isProcessing,color:"secondary",modelValue:e.login_password,"onUpdate:modelValue":o[3]||(o[3]=o=>e.login_password=o),label:"Password",type:e.login_show_password?"password":"text",rules:[e=>e&&e.length>0||"This is required."]},{append:(0,r.w5)((()=>[(0,r.Wm)(q,{name:e.login_show_password?"visibility_off":"visibility",class:"cursor-pointer",onClick:o[2]||(o[2]=o=>e.login_show_password=!e.login_show_password)},null,8,["name"])])),_:1},8,["disable","modelValue","type","rules"]),(0,r._)("div",_,[(0,r.Wm)(D,{class:"login",rounded:"",color:"red",label:"Back",to:"/"}),(0,r.Wm)(D,{class:"login",rounded:"",color:"secondary",label:"Login",type:"submit",disable:e.isProcessing},null,8,["disable"])])])),_:1},8,["onSubmit","onValidationError"])])),_:1}),(0,r.Wm)(z,{name:"register"},{default:(0,r.w5)((()=>[(0,r.Wm)(G,{onSubmit:(0,i.iM)(e.submitRegisterRequest,["prevent"]),onValidationError:e.errorOnSubmit,autofocus:!0},{default:(0,r.w5)((()=>[u,(0,r.Wm)(P),c,(0,r._)("div",g,[(0,r.Wm)(W,{class:"double",outlined:"",color:"secondary",modelValue:e.first_name,"onUpdate:modelValue":o[4]||(o[4]=o=>e.first_name=o),label:"First Name",counter:"",rules:[e=>e.length>=2&&e.length<=32||"Invalid, this is required. Should contain 2 to 32 characters."],"lazy-rules":"",disable:e.isProcessing},null,8,["modelValue","rules","disable"]),(0,r.Wm)(W,{class:"double",outlined:"",color:"secondary",modelValue:e.last_name,"onUpdate:modelValue":o[5]||(o[5]=o=>e.last_name=o),label:"Last Name",counter:"",rules:[e=>e.length>=2&&e.length<=32||"Invalid, this is required. Should contain 2 to 32 characters."],"lazy-rules":"",disable:e.isProcessing},null,8,["modelValue","rules","disable"])]),(0,r.Wm)(W,{class:"data",outlined:"",color:"secondary",modelValue:e.email,"onUpdate:modelValue":o[6]||(o[6]=o=>e.email=o),type:"email",label:"E-mail",counter:"","lazy-rules":"",disable:e.isProcessing,rules:[e=>e.includes("@")||"Invalid email format."]},null,8,["modelValue","disable","rules"]),(0,r.Wm)(P),h,(0,r._)("div",m,[(0,r.Wm)(W,{class:"double",outlined:"",color:"secondary",counter:"",modelValue:e.org_name,"onUpdate:modelValue":o[7]||(o[7]=o=>e.org_name=o),error:e.register_org_name_invalid,onFocus:o[8]||(o[8]=o=>e.register_org_name_invalid=!1),label:"Organization Name",hint:"Must be in Title Case.",rules:[e=>!e.length||e.length>=2&&e.length<=64||"Name should not be less than 1 character or more than 64 characters."],"lazy-rules":"",disable:e.isProcessing},{error:(0,r.w5)((()=>[p])),_:1},8,["modelValue","error","rules","disable"]),(0,r.Wm)(W,{class:"double",outlined:"",counter:"",color:"secondary",modelValue:e.org_address,"onUpdate:modelValue":o[9]||(o[9]=o=>e.org_address=o),error:e.register_org_address_invalid,onFocus:o[10]||(o[10]=o=>e.register_org_address_invalid=!1),label:"Organization Address",hint:"Must\n                start with 'fl:'.",rules:[e=>!e.length||35==e.length&&e.startsWith("fl:")||"Invalid format, should start with prefix `fl:` and should be exactly 35 characters."],"lazy-rules":"",disable:e.isProcessing},{error:(0,r.w5)((()=>[b])),_:1},8,["modelValue","error","rules","disable"])]),(0,r.Wm)(x,{class:"data",color:"secondary",outlined:"",modelValue:e.org_type_chosen,"onUpdate:modelValue":o[11]||(o[11]=o=>e.org_type_chosen=o),options:e.org_options,error:e.register_org_type_invalid,onFocus:o[12]||(o[12]=o=>e.register_org_type_invalid=!1),label:"Organization Type",disable:e.isProcessing},{error:(0,r.w5)((()=>[f,y,N,w,E])),_:1},8,["modelValue","options","error","disable"]),(0,r.Wm)(W,{class:"data",outlined:"",color:"secondary",modelValue:e.org_description,"onUpdate:modelValue":o[13]||(o[13]=o=>e.org_description=o),type:"textarea",label:"Organization Description",counter:"",error:e.register_org_description_invalid,onFocus:o[14]||(o[14]=o=>e.register_org_description_invalid=!1),hint:"Be careful, content should be finalized before submitting.",rules:[e=>!e.length||e.length>=8&&e.length<=256||"Cannot go less than 8 characters or more than 256 characters."],"lazy-rules":"",disable:e.isProcessing},{error:(0,r.w5)((()=>[v])),_:1},8,["modelValue","error","rules","disable"]),(0,r.Wm)(W,{filled:"",modelValue:e.org_date,"onUpdate:modelValue":o[18]||(o[18]=o=>e.org_date=o),class:"data",mask:"date",prefix:"Organization Founded",readonly:"",error:e.register_org_founded_invalid,hint:"The date from where your institution or your organization was founded.",disable:e.isProcessing},{append:(0,r.w5)((()=>[e.org_date?((0,r.wg)(),(0,r.j4)(q,{key:0,name:"cancel",onClick:o[15]||(o[15]=(0,i.iM)((o=>{e.org_date="",e.register_org_founded_invalid=!1}),["stop"])),class:"cursor-pointer"})):(0,r.kq)("",!0),(0,r.Wm)(q,{name:"event",class:"cursor-pointer"},{default:(0,r.w5)((()=>[(0,r.Wm)(F,{ref:"qDateProxy",cover:"","transition-show":"scale","transition-hide":"scale"},{default:(0,r.w5)((()=>[(0,r.Wm)(L,{modelValue:e.org_date,"onUpdate:modelValue":o[16]||(o[16]=o=>e.org_date=o),onClick:o[17]||(o[17]=o=>e.register_org_founded_invalid=!1),color:"secondary","today-btn":"",options:e.optionsFn,disable:e.isProcessing},{default:(0,r.w5)((()=>[(0,r._)("div",I,[(0,r.wy)((0,r.Wm)(D,{label:"Close",color:"primary",flat:""},null,512),[[Q]])])])),_:1},8,["modelValue","options","disable"])])),_:1},512)])),_:1})])),error:(0,r.w5)((()=>[T])),_:1},8,["modelValue","error","disable"]),(0,r.Wm)(P),(0,r.Wm)(W,{class:"data",outlined:"",color:"secondary",modelValue:e.register_username,"onUpdate:modelValue":o[19]||(o[19]=o=>e.register_username=o),label:"Username",counter:"",hint:"This will be used to login.",disable:e.isProcessing,rules:[e=>e.length>=8&&e.length<=24||"This should contain not less than 8 characters or more than 24 characters."],"lazy-rules":""},null,8,["modelValue","disable","rules"]),(0,r._)("div",S,[(0,r.Wm)(W,{class:"double",outlined:"",color:"secondary",modelValue:e.register_password,"onUpdate:modelValue":o[21]||(o[21]=o=>e.register_password=o),label:"Password",counter:"",type:e.register_show_password?"text":"password",disable:e.isProcessing,rules:[e=>e.length>=8&&e.length<=64||"This should contain not less than 8 characters or more than 64 characters."],"lazy-rules":""},{append:(0,r.w5)((()=>[(0,r.Wm)(q,{name:e.register_show_password?"visibility":"visibility_off",class:"cursor-pointer",onClick:o[20]||(o[20]=o=>e.register_show_password=!e.register_show_password)},null,8,["name"])])),_:1},8,["modelValue","type","disable","rules"]),(0,r.Wm)(W,{class:"double",outlined:"",color:"secondary",modelValue:e.register_confirm_password,"onUpdate:modelValue":o[23]||(o[23]=o=>e.register_confirm_password=o),label:"Confirm Password",counter:"",type:e.register_show_confirm_password?"text":"password",rules:[o=>o.length>=8&&o.length<=64&&o==e.register_password||"This should match your password to confirm your password."],disable:e.isProcessing},{append:(0,r.w5)((()=>[(0,r.Wm)(q,{name:e.register_show_confirm_password?"visibility":"visibility_off",class:"cursor-pointer",onClick:o[22]||(o[22]=o=>e.register_show_confirm_password=!e.register_show_confirm_password)},null,8,["name"])])),_:1},8,["modelValue","type","rules","disable"])]),(0,r.Wm)(W,{class:"data",outlined:"",color:"secondary",modelValue:e.register_auth_code,"onUpdate:modelValue":o[24]||(o[24]=o=>e.register_auth_code=o),type:"text",label:"Authentication Code",hint:"Remember, talk to your representatives to get your authentication code.",disable:e.isProcessing,error:e.register_auth_code_invalid,onFocus:o[25]||(o[25]=o=>e.register_auth_code_invalid=!1),rules:[e=>e.length||"This cannot be empty!"]},{error:(0,r.w5)((()=>[O])),_:1},8,["modelValue","disable","error","rules"]),(0,r.Wm)(P),(0,r.Wm)(H,null,{default:(0,r.w5)((()=>[R,k])),_:1}),(0,r._)("div",U,[(0,r.Wm)(D,{class:"backbtn",rounded:"",color:"red",label:"Back",to:"/"}),(0,r.Wm)(D,{class:"register",rounded:"",color:"secondary",label:"Register",type:"submit",disable:e.isProcessing},null,8,["disable"])])])),_:1},8,["onSubmit","onValidationError"])])),_:1})])),_:1},8,["modelValue"])])),_:1})])),_:1})])],64)}s(5363),s(7768);var V=s(1959);const A={style:{"max-width":"100%","padding-bottom":"10%"}};function P(e,o){return(0,r.wg)(),(0,r.iD)("div",A,[(0,r.WI)(e.$slots,"default",{},void 0,!0)])}var W=s(4260);const q={},D=(0,W.Z)(q,[["render",P],["__scopeId","data-v-dd538fc8"]]),G=D;var z=s(9582),x=s(52),L=s.n(x),F=s(8825),H=s(2796);const Z=(0,r.aZ)({name:"EntryForm",components:{RegisterContainer:G},data(){return{first_name:(0,V.iH)(""),last_name:(0,V.iH)(""),email:(0,V.iH)(""),org_name:(0,V.iH)(""),org_address:(0,V.iH)(""),org_description:(0,V.iH)(""),isProcessing:(0,V.iH)(!1),org_date:(0,V.iH)(""),register_username:(0,V.iH)(""),register_password:(0,V.iH)(""),register_confirm_password:(0,V.iH)(""),register_auth_code:(0,V.iH)(""),login_username:(0,V.iH)(""),login_password:(0,V.iH)(""),register_org_name_invalid:(0,V.iH)(!1),register_org_address_invalid:(0,V.iH)(!1),register_org_type_invalid:(0,V.iH)(!1),register_org_description_invalid:(0,V.iH)(!1),register_org_founded_invalid:(0,V.iH)(!1),register_username_invalid:(0,V.iH)(!1),register_auth_code_invalid:(0,V.iH)(!1),login_show_password:(0,V.iH)(!0),register_show_password:(0,V.iH)(!1),register_show_confirm_password:(0,V.iH)(!1)}},setup(){const e=(0,z.yj)();(0,z.tv)(),(0,F.Z)();return{tab:(0,V.iH)(e.params.action),org_options:[{label:"Existing",value:null},{label:"Institution",value:1},{label:"Organization",value:2}],org_type_chosen:(0,V.iH)({label:"Existing",value:null}),date:(new Date).toISOString().slice(0,10).replaceAll("-","/")}},methods:{submitLoginRequest(){this.isProcessing=!0,L().post(`${H.sx}/entity/login`,{username:this.login_username,password:this.login_password}).then((e=>{try{"Master Node User"==e.data.user_role||"Archival Miner Node User"==e.data.user_role?(this.$q.notify({color:"negative",position:"top",message:"Node-related account is not allowed to use the dashboard. Your account can be used in logging at folioblocks-node-cli.",timeout:5e3,progress:!0,icon:"mdi-account-cancel-outline"}),L().post(`${H.sx}/entity/logout`,{},{headers:{"X-Token":e.data.jwt_token}}),this.isProcessing=!1):(this.$q.localStorage.clear(),this.$q.localStorage.set("token",e.data.jwt_token),this.$q.localStorage.set("address",e.data.user_address),this.$q.localStorage.set("role",e.data.user_role),this.$q.notify({color:"green",position:"top",message:"Login successful!",timeout:5e3,progress:!0,icon:"mdi-account-check"}),this.$router.push({path:"/dashboard"}),this.isProcessing=!1)}catch(o){this.$q.clear(),this.isProcessing=!1}})).catch((e=>{const o=void 0===e.response.data?`${e.message}. Server may be unvailable. Please try again later.`:e.response.data.detail;this.$q.notify({color:"negative",position:"top",message:`There was an error when submitting your credentials. | Info: ${o}`,timeout:5e3,progress:!0,icon:"report_problem"}),this.isProcessing=!1}))},optionsFn(e){let o=new Date;return o.setDate(o.getDate()+1),new Date(null).toISOString().slice(0,10).replaceAll("-","/")>=e||e<=o.toISOString().slice(0,10).replaceAll("-","/")},submitRegisterRequest(){this.isProcessing=!0;let e={first_name:this.first_name,last_name:this.last_name,username:this.register_username,password:this.register_confirm_password,email:this.email,auth_code:this.register_auth_code},o=!1;if(console.log(this.org_date,typeof this.org_date),this.org_name.length&&!this.org_address.length&&this.org_description.length&&null!==this.org_type_chosen.value&&""!==this.org_date)e.association_name=this.org_name,e.association_type=this.org_type_chosen.value,e.association_founded=new Date(this.org_date).toISOString(),e.association_description=this.org_description,o=!0;else{if(this.org_name.length||!this.org_address.length||this.org_description.length||null!==this.org_type_chosen.value||null!==this.org_date&&""!==this.org_date)return this.$q.notify({color:"negative",position:"top",message:"Please keep the organization address filled only when the organization exists, otherwise, fill other fields except for the organization address.",timeout:5e3,progress:!0,icon:"report_problem"}),null===this.org_type_chosen.value?(""!==this.org_name?this.register_org_name_invalid=!0:this.register_org_name_invalid=!1,""!==this.org_description?this.register_org_description_invalid=!0:this.register_org_description_invalid=!1,""!==this.org_date?this.register_org_founded_invalid=!0:this.register_org_founded_invalid=!1,""!==this.org_address?this.register_org_address_invalid=!1:this.register_org_address_invalid=!0,this.register_org_type_invalid=!0,void(this.isProcessing=!1)):(""===this.org_name?this.register_org_name_invalid=!0:this.register_org_name_invalid=!1,""===this.org_description?this.register_org_description_invalid=!0:this.register_org_description_invalid=!1,""===this.org_date?this.register_org_founded_invalid=!0:this.register_org_founded_invalid=!1,""===this.org_address?this.register_org_address_invalid=!1:this.register_org_address_invalid=!0,this.register_org_type_invalid=!0,void(this.isProcessing=!1));e.association_address=this.org_address,o=!0}o&&L().post(`${H.sx}/entity/register`,{...e}).then((e=>{console.log(e),this.$q.notify({color:"green",position:"top",message:"Registration successful! Please check your email and login.",timeout:5e3,progress:!0,icon:"mdi-account-check"}),this.isProcessing=!1,this.$router.push({path:"/"})})).catch((e=>{const o=void 0===e.response.data?`${e.message}. Server may be unvailable. Please try again later.`:e.response.data.detail;this.$q.notify({color:"negative",position:"top",message:`There was an error when submitting your credentials. Reason: ${o}`,timeout:5e3,progress:!0,icon:"report_problem"}),this.register_org_address_invalid=!1,this.register_org_name_invalid=!1,this.register_org_type_invalid=!1,this.register_org_description_invalid=!1,this.register_org_founded_invalid=!1,void 0!==e.response.data&&e.response.data.detail.includes("`auth_token` were not found.")&&(this.register_auth_code_invalid=!0),this.isProcessing=!1}))},errorOnSubmit(){this.$q.notify({color:"negative",position:"top",message:"There was an error from one of the fields. Please check and try again.",timeout:5e3,progress:!0,icon:"report_problem"})}}});var $=s(151),B=s(1598),Q=s(7547),M=s(3269),j=s(5869),Y=s(5906),K=s(6602),X=s(5269),J=s(4689),ee=s(4554),oe=s(8240),se=s(3314),re=s(3944),ie=s(6915),te=s(5589),ae=s(677),ne=s(7518),le=s.n(ne);const de=(0,W.Z)(Z,[["render",C],["__scopeId","data-v-71a7272c"]]),_e=de;le()(Z,"components",{QCard:$.Z,QLinearProgress:B.Z,QTabs:Q.Z,QTab:M.Z,QSeparator:j.Z,QTabPanels:Y.Z,QTabPanel:K.Z,QForm:X.Z,QInput:J.Z,QIcon:ee.Z,QBtn:oe.Z,QSelect:se.Z,QPopupProxy:re.Z,QDate:ie.Z,QCardSection:te.Z}),le()(Z,"directives",{ClosePopup:ae.Z})},3585:(e,o,s)=>{e.exports=s.p+"img/pagebackground.496a4276.png"}}]);