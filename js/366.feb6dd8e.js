(self["webpackChunkfolioblocks_web"]=self["webpackChunkfolioblocks_web"]||[]).push([[366],{2796:(e,s,r)=>{"use strict";r.d(s,{$T:()=>u,_u:()=>c,kb:()=>a,oX:()=>n,sx:()=>i,uK:()=>t});const o="https://",i=`${o}folioblocks.southeastasia.azurecontainer.io`,t=`${o}codexlink.github.io/folioblocks`,a=100,n="otpauth://totp/Organization%20Creator:Folioblocks-Web?secret=MNMDQX32IREXQQLIM4YHMYSYLFUHASCBMJFF63TCMU4UY5TNJBTVMWC7OMWTSQLUNJEVCPJRGZQTOZJTMYYDAOLFMJRGMMJWMVSWCOJWGM2TMOBTHBTGMYZTGMZDOZTDGI2TEOJYGM2DMYRRGE3DCYZVGNRTSYRRMQ3WKNZSGAZDG%3D%3D%3D&issuer=Organization%20Creator",l=Object.freeze({NODE_GENERAL_CONSENSUS_INIT:1,NODE_GENERAL_REGISTER_INIT:2,NODE_GENERAL_GENESIS_BLOCK_INIT:3,NODE_GENERAL_CONSENSUS_BLOCK_SYNC:4,NODE_GENERAL_CONSENSUS_CONFIRM_NEGOTIATION_START:5,NODE_GENERAL_CONSENSUS_CONCLUDE_NEGOTIATION_PROCESSING:6,INSTITUTION_ORG_GENERATE_STUDENT:7,INSTITUTION_ORG_REFER_NEW_DOCUMENT_OR_IMPORTANT_INFO:8,INSTITUTION_ORG_STUDENT_REFER_EXTRA_INFO:9,ORGANIZATION_USER_REGISTER:10,ORGANIZATION_REFER_EXTRA_INFO:11}),d=Object.freeze({STUDENT_BASE:1,STUDENT_LOG:2,STUDENT_ADDITIONAL:3,ORGANIZATION_BASE:4}),_=Object.freeze({CONSENSUS:1,INIT:2,SYNC:3});function u(e){switch(e){case l.NODE_GENERAL_CONSENSUS_INIT:return"Consensus Initialization";case l.NODE_GENERAL_REGISTER_INIT:return"Node Registration";case l.NODE_GENERAL_GENESIS_BLOCK_INIT:return"Node Genesis Block Creation";case l.NODE_GENERAL_CONSENSUS_BLOCK_SYNC:return"Node Block Sync via Consensus";case l.NODE_GENERAL_CONSENSUS_CONFIRM_NEGOTIATION_START:return"Node Consensus Negotiation Confirmed Start";case l.NODE_GENERAL_CONSENSUS_CONCLUDE_NEGOTIATION_PROCESSING:return"Node Consensus Negotiation Conclusion of Processing";case l.INSTITUTION_ORG_GENERATE_STUDENT:return"Institution Student Generation";case l.INSTITUTION_ORG_REFER_NEW_DOCUMENT_OR_IMPORTANT_INFO:return"Institution New Document / Important Info to Student Reference";case l.INSTITUTION_ORG_STUDENT_REFER_EXTRA_INFO:return"Institution Refer Extra Info to Student";case l.ORGANIZATION_USER_REGISTER:return"Organization Registration";case l.ORGANIZATION_REFER_EXTRA_INFO:return"Extra Info Referral to Organization";default:return"Unidentified Action."}}function c(e){let s=e.hasOwnProperty("content_type")?"User Transaction":"Internal Transaction",r=null;if(e.hasOwnProperty("content_type"))switch(e.content_type){case d.STUDENT_BASE:r="Student Base Portfolio";break;case d.STUDENT_LOG:r="Student Log from Orgs";break;case d.STUDENT_ADDITIONAL:r="Student Additional Info / Remarks";break;case d.ORGANIZATION_BASE:r="Organization Base Registration";break;default:r="Unidentified";break}else switch(e.action){case _.CONSENSUS:r="Internal: Consensus Context";break;case _.INIT:r="Internal: Context Initialization";break;case _.SYNC:r="Internal: Sync from Communication";break;default:r="Unidentified";break}return{identifiedType:s,resolvedTypeValue:r}}},1366:(e,s,r)=>{"use strict";r.r(s),r.d(s,{default:()=>ue});var o=r(3673),i=r(8880),t=r(3585),a=r.n(t);const n=e=>((0,o.dD)("data-v-123b2f6e"),e=e(),(0,o.Cn)(),e),l=n((()=>(0,o._)("img",{class:"background",src:a(),style:{"background-attachment":"fixed"}},null,-1))),d=n((()=>(0,o._)("div",null,[(0,o._)("h2",null,"Hello! Welcome Back!"),(0,o._)("h4",null," Please login to get started. Or renew your token from logging in. ")],-1))),_={class:"btn"},u=n((()=>(0,o._)("div",null,[(0,o._)("h2",null,"Thank you for taking interest!"),(0,o._)("h4",null,[(0,o.Uk)(" Fill the fields below. Remember, "),(0,o._)("strong",null,"get the authentication code"),(0,o.Uk)(" from your supervisor for you to proceed your regisration. ")])],-1))),c=n((()=>(0,o._)("div",null,[(0,o._)("h4",null,[(0,o._)("strong",null,"Personal Information")]),(0,o._)("h4",null,[(0,o.Uk)(" Following fields are required to identify you "),(0,o._)("strong",null,"internally"),(0,o.Uk)(". Don't worry, your identity will not be exposed "),(0,o._)("strong",null,"except"),(0,o.Uk)(" the contact form which is the "),(0,o._)("strong",null,"email"),(0,o.Uk)(" you inputted from this form. ")])],-1))),g={class:"row"},h=(0,o.Uk)(" E-mail may be already used. Please contact your administrator on this issue. "),m=n((()=>(0,o._)("div",null,[(0,o._)("h4",null,[(0,o._)("strong",null,"Organization Information")]),(0,o._)("h4",null,[(0,o.Uk)(" Following fields require to specify your organization as a new entity from the system. Should there be an existing organization must "),(0,o._)("strong",null,"only fill the organization address"),(0,o.Uk)(" as well as setting the organization type as "),(0,o._)("strong",null,"Existing"),(0,o.Uk)(" and nothing else. ")]),(0,o._)("h4",null,[(0,o.Uk)(" Note that, you have to be "),(0,o._)("strong",null,"very careful"),(0,o.Uk)(" from your inputs as these are unmodifiable due to nature of blockchain. ")])],-1))),p={class:"row"},b=(0,o.Uk)(" If you are inserting an existing organization, please clear this field. "),f=(0,o.Uk)(" This may be required. If you are inserting a new organization, please clear this field, otherwise, proceed. "),y=(0,o.Uk)(" For existing organization, please choose "),N=n((()=>(0,o._)("strong",null,"existing",-1))),w=(0,o.Uk)(" and fill up "),E=n((()=>(0,o._)("strong",null,"ONLY",-1))),T=(0,o.Uk)(" the organization address, otherwise, fill other fields that shows an error. "),v=(0,o.Uk)(" This may be required. If you are inserting an existing organization, please clear this field, otherwise, add a date. "),I={class:"row items-center justify-end"},O=(0,o.Uk)(" This may be required. If you are inserting an existing organization, please clear this field, otherwise, check for other fields. "),S={class:"row"},R=(0,o.Uk)(" Authentication code is invalid. Check your email inbox and try again. "),U=n((()=>(0,o._)("h4",null,[(0,o._)("strong",null,"Notice")],-1))),k=(0,o.Uk)(" Please ensure your inputs are correct before proceeding, there's no going back or be able to change them once submitted. "),C={class:"registerbtn"};function A(e,s,r,t,a,n){const A=(0,o.up)("q-linear-progress"),V=(0,o.up)("q-tab"),P=(0,o.up)("q-tabs"),D=(0,o.up)("q-separator"),G=(0,o.up)("q-input"),W=(0,o.up)("q-icon"),q=(0,o.up)("q-btn"),z=(0,o.up)("q-form"),x=(0,o.up)("q-tab-panel"),F=(0,o.up)("q-select"),L=(0,o.up)("q-date"),Z=(0,o.up)("q-popup-proxy"),M=(0,o.up)("q-card-section"),H=(0,o.up)("q-tab-panels"),$=(0,o.up)("q-card"),Q=(0,o.up)("RegisterContainer"),B=(0,o.Q2)("close-popup");return(0,o.wg)(),(0,o.iD)(o.HY,null,[l,(0,o._)("body",null,[(0,o.Wm)(Q,null,{default:(0,o.w5)((()=>[(0,o.Wm)($,null,{default:(0,o.w5)((()=>[e.isProcessing?((0,o.wg)(),(0,o.j4)(A,{key:0,query:"",color:"secondary",class:"q-mt-sm"})):(0,o.kq)("",!0),(0,o.Wm)(P,{modelValue:e.tab,"onUpdate:modelValue":s[0]||(s[0]=s=>e.tab=s),class:"text-grey tabs","active-color":"secondary","indicator-color":"secondary",align:"justify"},{default:(0,o.w5)((()=>[(0,o.Wm)(V,{name:"login",label:"Login"}),(0,o.Wm)(V,{name:"register",label:"Register"})])),_:1},8,["modelValue"]),(0,o.Wm)(D),(0,o.Wm)(H,{modelValue:e.tab,"onUpdate:modelValue":s[27]||(s[27]=s=>e.tab=s),animated:""},{default:(0,o.w5)((()=>[(0,o.Wm)(x,{name:"login"},{default:(0,o.w5)((()=>[(0,o.Wm)(z,{onSubmit:(0,i.iM)(e.submitLoginRequest,["prevent"]),onValidationError:e.errorOnSubmit,autofocus:!0},{default:(0,o.w5)((()=>[d,(0,o.Wm)(G,{class:"user",color:"secondary",outlined:"",disable:e.isProcessing,modelValue:e.login_username,"onUpdate:modelValue":s[1]||(s[1]=s=>e.login_username=s),label:"Username",rules:[e=>e&&e.length>0||"This is required."]},null,8,["disable","modelValue","rules"]),(0,o.Wm)(G,{class:"password",outlined:"",disable:e.isProcessing,color:"secondary",modelValue:e.login_password,"onUpdate:modelValue":s[3]||(s[3]=s=>e.login_password=s),label:"Password",type:e.login_show_password?"password":"text",rules:[e=>e&&e.length>0||"This is required."]},{append:(0,o.w5)((()=>[(0,o.Wm)(W,{name:e.login_show_password?"visibility_off":"visibility",class:"cursor-pointer",onClick:s[2]||(s[2]=s=>e.login_show_password=!e.login_show_password)},null,8,["name"])])),_:1},8,["disable","modelValue","type","rules"]),(0,o._)("div",_,[(0,o.Wm)(q,{class:"login",rounded:"",color:"red",label:"Back",to:"/"}),(0,o.Wm)(q,{class:"login",rounded:"",color:"secondary",label:"Login",type:"submit",disable:e.isProcessing},null,8,["disable"])])])),_:1},8,["onSubmit","onValidationError"])])),_:1}),(0,o.Wm)(x,{name:"register"},{default:(0,o.w5)((()=>[(0,o.Wm)(z,{onSubmit:(0,i.iM)(e.submitRegisterRequest,["prevent"]),onValidationError:e.errorOnSubmit,autofocus:!0},{default:(0,o.w5)((()=>[u,(0,o.Wm)(D),c,(0,o._)("div",g,[(0,o.Wm)(G,{class:"double",outlined:"",color:"secondary",modelValue:e.first_name,"onUpdate:modelValue":s[4]||(s[4]=s=>e.first_name=s),label:"First Name",counter:"",rules:[e=>e.length>=2&&e.length<=32||"Invalid, this is required. Should contain 2 to 32 characters."],"lazy-rules":"",disable:e.isProcessing},null,8,["modelValue","rules","disable"]),(0,o.Wm)(G,{class:"double",outlined:"",color:"secondary",modelValue:e.last_name,"onUpdate:modelValue":s[5]||(s[5]=s=>e.last_name=s),label:"Last Name",counter:"",rules:[e=>e.length>=2&&e.length<=32||"Invalid, this is required. Should contain 2 to 32 characters."],"lazy-rules":"",disable:e.isProcessing},null,8,["modelValue","rules","disable"])]),(0,o.Wm)(G,{class:"data",outlined:"",color:"secondary",modelValue:e.email,"onUpdate:modelValue":s[6]||(s[6]=s=>e.email=s),type:"email",label:"E-mail",error:e.register_email_invalid,onFocus:s[7]||(s[7]=s=>e.register_email_invalid=!1),counter:"","lazy-rules":"",disable:e.isProcessing,rules:[e=>e.includes("@")||"Invalid email format."]},{error:(0,o.w5)((()=>[h])),_:1},8,["modelValue","error","disable","rules"]),(0,o.Wm)(D),m,(0,o._)("div",p,[(0,o.Wm)(G,{class:"double",outlined:"",color:"secondary",counter:"",modelValue:e.org_name,"onUpdate:modelValue":s[8]||(s[8]=s=>e.org_name=s),error:e.register_org_name_invalid,onFocus:s[9]||(s[9]=s=>e.register_org_name_invalid=!1),label:"Organization Name",hint:"Must be in Title Case.",rules:[e=>!e.length||e.length>=2&&e.length<=64||"Name should not be less than 1 character or more than 64 characters."],"lazy-rules":"",disable:e.isProcessing},{error:(0,o.w5)((()=>[b])),_:1},8,["modelValue","error","rules","disable"]),(0,o.Wm)(G,{class:"double",outlined:"",counter:"",color:"secondary",modelValue:e.org_address,"onUpdate:modelValue":s[10]||(s[10]=s=>e.org_address=s),error:e.register_org_address_invalid,onFocus:s[11]||(s[11]=s=>e.register_org_address_invalid=!1),label:"Organization Address",hint:"Must\n                start with 'fl:'.",rules:[e=>!e.length||35==e.length&&e.startsWith("fl:")||"Invalid format, should start with prefix `fl:` and should be exactly 35 characters."],"lazy-rules":"",disable:e.isProcessing},{error:(0,o.w5)((()=>[f])),_:1},8,["modelValue","error","rules","disable"])]),(0,o.Wm)(F,{class:"data",color:"secondary",outlined:"",modelValue:e.org_type_chosen,"onUpdate:modelValue":s[12]||(s[12]=s=>e.org_type_chosen=s),options:e.org_options,error:e.register_org_type_invalid,onFocus:s[13]||(s[13]=s=>e.register_org_type_invalid=!1),label:"Organization Type",disable:e.isProcessing},{error:(0,o.w5)((()=>[y,N,w,E,T])),_:1},8,["modelValue","options","error","disable"]),(0,o.Wm)(G,{class:"data",outlined:"",color:"secondary",modelValue:e.org_description,"onUpdate:modelValue":s[14]||(s[14]=s=>e.org_description=s),type:"textarea",label:"Organization Description",counter:"",error:e.register_org_description_invalid,onFocus:s[15]||(s[15]=s=>e.register_org_description_invalid=!1),hint:"Be careful, content should be finalized before submitting.",rules:[e=>!e.length||e.length>=8&&e.length<=256||"Cannot go less than 8 characters or more than 256 characters."],"lazy-rules":"",disable:e.isProcessing},{error:(0,o.w5)((()=>[v])),_:1},8,["modelValue","error","rules","disable"]),(0,o.Wm)(G,{filled:"",modelValue:e.org_date,"onUpdate:modelValue":s[19]||(s[19]=s=>e.org_date=s),class:"data",mask:"date",prefix:"Organization Founded",readonly:"",error:e.register_org_founded_invalid,hint:"The date from where your institution or your organization was founded.",disable:e.isProcessing},{append:(0,o.w5)((()=>[e.org_date?((0,o.wg)(),(0,o.j4)(W,{key:0,name:"cancel",onClick:s[16]||(s[16]=(0,i.iM)((s=>{e.org_date="",e.register_org_founded_invalid=!1}),["stop"])),class:"cursor-pointer"})):(0,o.kq)("",!0),(0,o.Wm)(W,{name:"event",class:"cursor-pointer"},{default:(0,o.w5)((()=>[(0,o.Wm)(Z,{ref:"qDateProxy",cover:"","transition-show":"scale","transition-hide":"scale"},{default:(0,o.w5)((()=>[(0,o.Wm)(L,{modelValue:e.org_date,"onUpdate:modelValue":s[17]||(s[17]=s=>e.org_date=s),onClick:s[18]||(s[18]=s=>e.register_org_founded_invalid=!1),color:"secondary","today-btn":"",options:e.optionsFn,disable:e.isProcessing},{default:(0,o.w5)((()=>[(0,o._)("div",I,[(0,o.wy)((0,o.Wm)(q,{label:"Close",color:"primary",flat:""},null,512),[[B]])])])),_:1},8,["modelValue","options","disable"])])),_:1},512)])),_:1})])),error:(0,o.w5)((()=>[O])),_:1},8,["modelValue","error","disable"]),(0,o.Wm)(D),(0,o.Wm)(G,{class:"data",outlined:"",color:"secondary",modelValue:e.register_username,"onUpdate:modelValue":s[20]||(s[20]=s=>e.register_username=s),label:"Username",counter:"",hint:"This will be used to login.",disable:e.isProcessing,rules:[e=>e.length>=8&&e.length<=24||"This should contain not less than 8 characters or more than 24 characters."],"lazy-rules":""},null,8,["modelValue","disable","rules"]),(0,o._)("div",S,[(0,o.Wm)(G,{class:"double",outlined:"",color:"secondary",modelValue:e.register_password,"onUpdate:modelValue":s[22]||(s[22]=s=>e.register_password=s),label:"Password",counter:"",type:e.register_show_password?"text":"password",disable:e.isProcessing,rules:[e=>e.length>=8&&e.length<=64||"This should contain not less than 8 characters or more than 64 characters."],"lazy-rules":""},{append:(0,o.w5)((()=>[(0,o.Wm)(W,{name:e.register_show_password?"visibility":"visibility_off",class:"cursor-pointer",onClick:s[21]||(s[21]=s=>e.register_show_password=!e.register_show_password)},null,8,["name"])])),_:1},8,["modelValue","type","disable","rules"]),(0,o.Wm)(G,{class:"double",outlined:"",color:"secondary",modelValue:e.register_confirm_password,"onUpdate:modelValue":s[24]||(s[24]=s=>e.register_confirm_password=s),label:"Confirm Password",counter:"",type:e.register_show_confirm_password?"text":"password",rules:[s=>s.length>=8&&s.length<=64&&s==e.register_password||"This should match your password to confirm your password."],disable:e.isProcessing},{append:(0,o.w5)((()=>[(0,o.Wm)(W,{name:e.register_show_confirm_password?"visibility":"visibility_off",class:"cursor-pointer",onClick:s[23]||(s[23]=s=>e.register_show_confirm_password=!e.register_show_confirm_password)},null,8,["name"])])),_:1},8,["modelValue","type","rules","disable"])]),(0,o.Wm)(G,{class:"data",outlined:"",color:"secondary",modelValue:e.register_auth_code,"onUpdate:modelValue":s[25]||(s[25]=s=>e.register_auth_code=s),type:"text",label:"Authentication Code",hint:"Remember, talk to your representatives to get your authentication code.",disable:e.isProcessing,error:e.register_auth_code_invalid,onFocus:s[26]||(s[26]=s=>e.register_auth_code_invalid=!1),rules:[e=>e.length||"This cannot be empty!"]},{error:(0,o.w5)((()=>[R])),_:1},8,["modelValue","disable","error","rules"]),(0,o.Wm)(D),(0,o.Wm)(M,null,{default:(0,o.w5)((()=>[U,k])),_:1}),(0,o._)("div",C,[(0,o.Wm)(q,{class:"backbtn",rounded:"",color:"red",label:"Back",to:"/"}),(0,o.Wm)(q,{class:"register",rounded:"",color:"secondary",label:"Register",type:"submit",disable:e.isProcessing},null,8,["disable"])])])),_:1},8,["onSubmit","onValidationError"])])),_:1})])),_:1},8,["modelValue"])])),_:1})])),_:1})])],64)}r(5363),r(7768);var V=r(1959);const P={style:{"max-width":"100%","padding-bottom":"10%"}};function D(e,s){return(0,o.wg)(),(0,o.iD)("div",P,[(0,o.WI)(e.$slots,"default",{},void 0,!0)])}var G=r(4260);const W={},q=(0,G.Z)(W,[["render",D],["__scopeId","data-v-5cf8ec94"]]),z=q;var x=r(9582),F=r(52),L=r.n(F),Z=r(8825),M=r(2796);const H=(0,o.aZ)({name:"EntryForm",components:{RegisterContainer:z},data(){return{first_name:(0,V.iH)(""),last_name:(0,V.iH)(""),email:(0,V.iH)(""),org_name:(0,V.iH)(""),org_address:(0,V.iH)(""),org_description:(0,V.iH)(""),isProcessing:(0,V.iH)(!1),org_date:(0,V.iH)(""),register_username:(0,V.iH)(""),register_password:(0,V.iH)(""),register_confirm_password:(0,V.iH)(""),register_auth_code:(0,V.iH)(""),login_username:(0,V.iH)(""),login_password:(0,V.iH)(""),register_org_name_invalid:(0,V.iH)(!1),register_email_invalid:(0,V.iH)(!1),register_org_address_invalid:(0,V.iH)(!1),register_org_type_invalid:(0,V.iH)(!1),register_org_description_invalid:(0,V.iH)(!1),register_org_founded_invalid:(0,V.iH)(!1),register_username_invalid:(0,V.iH)(!1),register_auth_code_invalid:(0,V.iH)(!1),login_show_password:(0,V.iH)(!0),register_show_password:(0,V.iH)(!1),register_show_confirm_password:(0,V.iH)(!1)}},setup(){const e=(0,x.yj)();(0,x.tv)(),(0,Z.Z)();return{tab:(0,V.iH)(e.params.action),org_options:[{label:"Existing",value:null},{label:"Institution",value:1},{label:"Organization",value:2}],org_type_chosen:(0,V.iH)({label:"Existing",value:null}),date:(new Date).toISOString().slice(0,10).replaceAll("-","/")}},methods:{submitLoginRequest(){this.isProcessing=!0,L().post(`${M.sx}/entity/login`,{username:this.login_username,password:this.login_password}).then((e=>{try{"Archival Miner Node User"==e.data.user_role?(this.$q.notify({color:"negative",position:"top",message:"Archival node accounts are not allowed to use the dashboard. Your account can only be used at logging in folioblocks-cli.",timeout:5e3,progress:!0,icon:"mdi-account-cancel-outline"}),L().post(`${M.sx}/entity/logout`,{},{headers:{"X-Token":e.data.jwt_token}}),this.isProcessing=!1):(this.$q.localStorage.clear(),this.$q.localStorage.set("token",e.data.jwt_token),this.$q.localStorage.set("address",e.data.user_address),this.$q.localStorage.set("role","Master Node User"===e.data.user_role?"Administrator":e.data.user_role),this.$q.notify({color:"green",position:"top",message:"Login successful!",timeout:5e3,progress:!0,icon:"mdi-account-check"}),this.$router.push({path:"/dashboard"}),this.isProcessing=!1)}catch(s){this.$q.clear(),this.isProcessing=!1}})).catch((e=>{const s=void 0===e.response.data?`${e.message}. Server may be unvailable. Please try again later.`:e.response.data.detail;this.$q.notify({color:"negative",position:"top",message:`There was an error when submitting your credentials. | Info: ${s}`,timeout:5e3,progress:!0,icon:"report_problem"}),this.isProcessing=!1}))},optionsFn(e){let s=new Date;return s.setDate(s.getDate()+1),new Date(null).toISOString().slice(0,10).replaceAll("-","/")>=e||e<=s.toISOString().slice(0,10).replaceAll("-","/")},submitRegisterRequest(){this.isProcessing=!0;let e={first_name:this.first_name,last_name:this.last_name,username:this.register_username,password:this.register_confirm_password,email:this.email,auth_code:this.register_auth_code},s=!1;if(console.log(this.org_date,typeof this.org_date),this.org_name.length&&!this.org_address.length&&this.org_description.length&&null!==this.org_type_chosen.value&&""!==this.org_date)e.association_name=this.org_name,e.association_type=this.org_type_chosen.value,e.association_founded=new Date(this.org_date).toISOString(),e.association_description=this.org_description,s=!0;else{if(this.org_name.length||!this.org_address.length||this.org_description.length||null!==this.org_type_chosen.value||null!==this.org_date&&""!==this.org_date)return this.$q.notify({color:"negative",position:"top",message:"Please keep the organization address filled only when the organization exists, otherwise, fill other fields except for the organization address.",timeout:5e3,progress:!0,icon:"report_problem"}),null===this.org_type_chosen.value?(""!==this.org_name?this.register_org_name_invalid=!0:this.register_org_name_invalid=!1,""!==this.org_description?this.register_org_description_invalid=!0:this.register_org_description_invalid=!1,""!==this.org_date?this.register_org_founded_invalid=!0:this.register_org_founded_invalid=!1,""!==this.org_address?this.register_org_address_invalid=!1:this.register_org_address_invalid=!0,this.register_org_type_invalid=!0,void(this.isProcessing=!1)):(""===this.org_name?this.register_org_name_invalid=!0:this.register_org_name_invalid=!1,""===this.org_description?this.register_org_description_invalid=!0:this.register_org_description_invalid=!1,""===this.org_date?this.register_org_founded_invalid=!0:this.register_org_founded_invalid=!1,""===this.org_address?this.register_org_address_invalid=!1:this.register_org_address_invalid=!0,this.register_org_type_invalid=!0,void(this.isProcessing=!1));e.association_address=this.org_address,s=!0}s&&L().post(`${M.sx}/entity/register`,{...e}).then((e=>{this.$q.notify({color:"green",position:"top",message:"Registration successful! Please check your email and login.",timeout:5e3,progress:!0,icon:"mdi-account-check"}),this.isProcessing=!1,this.$router.push({path:"/"})})).catch((e=>{const s=void 0===e.response.data?`${e.message}. Server may be unvailable. Please try again later.`:e.response.data.detail;this.$q.notify({color:"negative",position:"top",message:`There was an error when submitting your credentials. Reason: ${s}`,timeout:5e3,progress:!0,icon:"report_problem"}),this.register_org_address_invalid=!1,this.register_org_name_invalid=!1,this.register_org_type_invalid=!1,this.register_org_description_invalid=!1,this.register_org_founded_invalid=!1,void 0!==e.response.data&&(e.response.data.detail.includes("`auth_token` were not found.")?this.register_auth_code_invalid=!0:e.response.data.detail.includes("UNIQUE constraint failed: users.username")?this.register_username_invalid=!0:e.response.data.detail.includes("UNIQUE constraint failed: users.email")?this.register_email_invalid=!0:e.response.data.detail.includes("The supplied parameter for the `association` address reference does not exist")&&(this.register_auth_code_invalid=!0)),this.isProcessing=!1}))},errorOnSubmit(){this.$q.notify({color:"negative",position:"top",message:"There was an error from one of the fields. Please check and try again.",timeout:5e3,progress:!0,icon:"report_problem"})}}});var $=r(151),Q=r(1598),B=r(7547),Y=r(3269),j=r(5869),J=r(5906),X=r(6602),K=r(5269),ee=r(4689),se=r(4554),re=r(8240),oe=r(3314),ie=r(3944),te=r(6915),ae=r(5589),ne=r(677),le=r(7518),de=r.n(le);const _e=(0,G.Z)(H,[["render",A],["__scopeId","data-v-123b2f6e"]]),ue=_e;de()(H,"components",{QCard:$.Z,QLinearProgress:Q.Z,QTabs:B.Z,QTab:Y.Z,QSeparator:j.Z,QTabPanels:J.Z,QTabPanel:X.Z,QForm:K.Z,QInput:ee.Z,QIcon:se.Z,QBtn:re.Z,QSelect:oe.Z,QPopupProxy:ie.Z,QDate:te.Z,QCardSection:ae.Z}),de()(H,"directives",{ClosePopup:ne.Z})},3585:(e,s,r)=>{e.exports=r.p+"img/pagebackground.496a4276.png"}}]);