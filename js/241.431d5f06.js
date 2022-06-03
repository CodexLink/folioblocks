"use strict";(self["webpackChunkfolioblocks_web"]=self["webpackChunkfolioblocks_web"]||[]).push([[241],{2796:(e,t,s)=>{s.d(t,{$T:()=>u,_u:()=>c,kb:()=>i,oX:()=>r,sx:()=>o,uK:()=>a});const n="https://",o=`${n}folioblocks.southeastasia.azurecontainer.io`,a=`${n}codexlink.github.io/folioblocks`,i=100,r="otpauth://totp/Organization%20Creator:Folioblocks-Web?secret=MNMDQX32IREXQQLIM4YHMYSYLFUHASCBMJFF63TCMU4UY5TNJBTVMWC7OMWTSQLUNJEVCPJRGZQTOZJTMYYDAOLFMJRGMMJWMVSWCOJWGM2TMOBTHBTGMYZTGMZDOZTDGI2TEOJYGM2DMYRRGE3DCYZVGNRTSYRRMQ3WKNZSGAZDG%3D%3D%3D&issuer=Organization%20Creator",l=Object.freeze({NODE_GENERAL_CONSENSUS_INIT:1,NODE_GENERAL_REGISTER_INIT:2,NODE_GENERAL_GENESIS_BLOCK_INIT:3,NODE_GENERAL_CONSENSUS_BLOCK_SYNC:4,NODE_GENERAL_CONSENSUS_CONFIRM_NEGOTIATION_START:5,NODE_GENERAL_CONSENSUS_CONCLUDE_NEGOTIATION_PROCESSING:6,INSTITUTION_ORG_GENERATE_STUDENT:7,INSTITUTION_ORG_REFER_NEW_DOCUMENT_OR_IMPORTANT_INFO:8,INSTITUTION_ORG_STUDENT_REFER_EXTRA_INFO:9,ORGANIZATION_USER_REGISTER:10,ORGANIZATION_REFER_EXTRA_INFO:11}),d=Object.freeze({STUDENT_BASE:1,STUDENT_LOG:2,STUDENT_ADDITIONAL:3,ORGANIZATION_BASE:4}),_=Object.freeze({CONSENSUS:1,INIT:2,SYNC:3});function u(e){switch(e){case l.NODE_GENERAL_CONSENSUS_INIT:return"Consensus Initialization";case l.NODE_GENERAL_REGISTER_INIT:return"Node Registration";case l.NODE_GENERAL_GENESIS_BLOCK_INIT:return"Node Genesis Block Creation";case l.NODE_GENERAL_CONSENSUS_BLOCK_SYNC:return"Node Block Sync via Consensus";case l.NODE_GENERAL_CONSENSUS_CONFIRM_NEGOTIATION_START:return"Node Consensus Negotiation Confirmed Start";case l.NODE_GENERAL_CONSENSUS_CONCLUDE_NEGOTIATION_PROCESSING:return"Node Consensus Negotiation Conclusion of Processing";case l.INSTITUTION_ORG_GENERATE_STUDENT:return"Institution Student Generation";case l.INSTITUTION_ORG_REFER_NEW_DOCUMENT_OR_IMPORTANT_INFO:return"Institution New Document / Important Info to Student Reference";case l.INSTITUTION_ORG_STUDENT_REFER_EXTRA_INFO:return"Institution Refer Extra Info to Student";case l.ORGANIZATION_USER_REGISTER:return"Organization Registration";case l.ORGANIZATION_REFER_EXTRA_INFO:return"Extra Info Referral to Organization";default:return"Unidentified Action."}}function c(e){let t=e.hasOwnProperty("content_type")?"User Transaction":"Internal Transaction",s=null;if(e.hasOwnProperty("content_type"))switch(e.content_type){case d.STUDENT_BASE:s="Student Base Portfolio";break;case d.STUDENT_LOG:s="Student Log from Orgs";break;case d.STUDENT_ADDITIONAL:s="Student Additional Info / Remarks";break;case d.ORGANIZATION_BASE:s="Organization Base Registration";break;default:s="Unidentified";break}else switch(e.action){case _.CONSENSUS:s="Internal: Consensus Context";break;case _.INIT:s="Internal: Context Initialization";break;case _.SYNC:s="Internal: Sync from Communication";break;default:s="Unidentified";break}return{identifiedType:t,resolvedTypeValue:s}}},5241:(t,s,n)=>{n.r(s),n.d(s,{default:()=>fe});var o=n(3673),a=n(2323),i=n(8880);const r=e=>((0,o.dD)("data-v-0a6fcb04"),e=e(),(0,o.Cn)(),e),l={class:"q-pa-md q-gutter-sm"},d=r((()=>(0,o._)("h5",{class:"text-body1",style:{"margin-left":"4%"}},[(0,o._)("strong",null,"Students Available")],-1))),_={class:"form absolute-center"},u={class:"absolute-center insertdata"},c=r((()=>(0,o._)("p",{class:"text-left"}," Insert a Document or a Information to Refer at Student ",-1))),m=r((()=>(0,o._)("p",{class:"text-justify",style:{padding:"2%"}},[(0,o.Uk)(" This form allows you to insert a reference with a "),(0,o._)("strong",null,"proof"),(0,o.Uk)(" from the student. It can be a certification, work experience, promotion, and any other proof that a document or an information can infer. ")],-1))),h=r((()=>(0,o._)("p",{class:"text-justify",style:{padding:"0 2%"}},[(0,o._)("strong",null,"Note that"),(0,o.Uk)(", it is your "),(0,o._)("strong",null,"responsibility"),(0,o.Uk)(" to mask out any detailed information regarding this student. This system does not pseudonymize information within the document and is only designed as a source origin of this claim. ")],-1))),p=(0,o.Uk)("A document or a supporting context in a PDF form is required!"),w={class:"row items-center justify-end"},g=(0,o.Uk)(" The date may be missing or is colliding with the log date end. "),f={class:"row items-center justify-end"},b=(0,o.Uk)(" The date is colliding with the log date start. "),y={class:"text-center q-ma-md"},k=r((()=>(0,o._)("p",{class:"text-left"}," Insert Extra Information / Remarks from the Student ",-1))),T=r((()=>(0,o._)("p",{class:"text-justify",style:{padding:"2%"}},[(0,o.Uk)(" This form allows you to insert an extra information that wasn't significant but is necessary for other people to know. "),(0,o._)("strong",null,"Note that,"),(0,o.Uk)(" regardless of the context, professionalism must be invoked as this extra information is "),(0,o._)("strong",null,"NOT interchangeable"),(0,o.Uk)(" as it was imprinted in blockchain. ")],-1))),N=r((()=>(0,o._)("p",{class:"text-justify",style:{padding:"0 2%"}},[(0,o.Uk)(" Any mistakes or misconceptions regarding the representation of this context towards to the student will be held liable to you, as the "),(0,o._)("strong",null,"source origin was also recorded"),(0,o.Uk)(". Please be careful and make it sure the context was finalized before submitting this form. ")],-1))),S={class:"text-center q-ma-md"},E={class:"absolute-center text-center"},v=r((()=>(0,o._)("p",{class:"text-left"},"Insert a New Student",-1))),I=r((()=>(0,o._)("p",{class:"text-justify",style:{padding:"2%"}}," This form was intended for providing students the capability to store and access their credentials for job application purposes. Note that the information you enter is unchangeable due to blockchain nature. ",-1))),O=r((()=>(0,o._)("p",{class:"text-justify",style:{padding:"0 2%"}},[(0,o._)("strong",null,"Note that"),(0,o.Uk)(", any students who was recently inserted won't be shown immediately as it needs to be "),(0,o._)("strong",null,"processed"),(0,o.Uk)(" by blockchain first! They are accessible but they cannot be referred until that account contains "),(0,o._)("strong",null,"transaction mapping"),(0,o.Uk)(". ")],-1))),R={class:"row"},U={class:"row"},P=(0,o.Uk)(" Please change the value of this field as your input already exists from the system. "),V=(0,o.Uk)(" Please change the value of this field as your input already exists from the system. "),C={class:"row"},q={class:"row"},x={class:"text-center q-ma-md"};function D(e,t,s,n,r,D){const W=(0,o.up)("q-btn"),A=(0,o.up)("q-linear-progress"),F=(0,o.up)("q-avatar"),G=(0,o.up)("q-item-section"),L=(0,o.up)("q-item-label"),$=(0,o.up)("q-item"),H=(0,o.up)("q-scroll-area"),M=(0,o.up)("q-card"),Z=(0,o.up)("q-tab"),z=(0,o.up)("q-tabs"),Q=(0,o.up)("q-separator"),j=(0,o.up)("q-card-section"),B=(0,o.up)("q-input"),Y=(0,o.up)("q-icon"),X=(0,o.up)("q-file"),J=(0,o.up)("q-date"),K=(0,o.up)("q-popup-proxy"),ee=(0,o.up)("q-form"),te=(0,o.up)("q-tab-panel"),se=(0,o.up)("q-tab-panels"),ne=(0,o.up)("q-tooltip"),oe=(0,o.up)("q-page-sticky"),ae=(0,o.Q2)("ripple"),ie=(0,o.Q2)("close-popup");return(0,o.wg)(),(0,o.iD)("div",l,[(0,o.Wm)(W,{outline:"",class:"add",color:"secondary",label:"New Student",icon:"mdi-plus",disable:r.isProcessing,onClick:t[0]||(t[0]=e=>{r.new_user=!0,r.existing_user=!1,n.targetted_address=null,n.targetted_number=0})},null,8,["disable"]),(0,o.Wm)(M,{class:"users"},{default:(0,o.w5)((()=>[r.isFetchingStudent?((0,o.wg)(),(0,o.j4)(A,{key:0,query:"",color:"red"})):(0,o.kq)("",!0),d,(0,o.Wm)(H,{style:{height:"100%","max-width":"100%"}},{default:(0,o.w5)((()=>[((0,o.wg)(!0),(0,o.iD)(o.HY,null,(0,o.Ko)(r.students,(e=>(0,o.wy)(((0,o.wg)(),(0,o.j4)($,{key:e.id,clickable:"",active:n.targetted_number===e.id,"active-class":"selected_student",disable:r.isProcessing,onClick:t=>{r.existing_user=!0,r.new_user=!1,D.setActiveFieldForForm(e.id)}},{default:(0,o.w5)((()=>[(0,o.Wm)(G,{avatar:""},{default:(0,o.w5)((()=>[(0,o.Wm)(F,{class:"icon",icon:"account_circle",size:"3em"})])),_:1}),(0,o.Wm)(G,{class:"text-h6"},{default:(0,o.w5)((()=>[(0,o.Uk)((0,a.zw)(e.first_name)+" "+(0,a.zw)(e.last_name)+" ",1),(0,o.Wm)(L,{overline:""},{default:(0,o.w5)((()=>[(0,o.Uk)((0,a.zw)(e.program),1)])),_:2},1024),(0,o.Wm)(L,{caption:""},{default:(0,o.w5)((()=>[(0,o.Uk)((0,a.zw)(e.address),1)])),_:2},1024)])),_:2},1024)])),_:2},1032,["active","disable","onClick"])),[[ae]]))),128))])),_:1})])),_:1}),(0,o._)("div",_,[(0,o._)("div",u,[(0,o.wy)((0,o.Wm)(M,{class:"my-card"},{default:(0,o.w5)((()=>[r.isProcessing?((0,o.wg)(),(0,o.j4)(A,{key:0,query:"",color:"secondary",class:"q-mt-sm"})):(0,o.kq)("",!0),(0,o.Wm)(z,{modelValue:n.selected_section,"onUpdate:modelValue":t[1]||(t[1]=e=>n.selected_section=e),dense:"",class:"text-grey","active-color":"secondary","indicator-color":"secondary",align:"justify"},{default:(0,o.w5)((()=>[(0,o.Wm)(Z,{name:"insert_docs",label:"Add Document",class:"tab",disable:r.isProcessing},null,8,["disable"]),(0,o.Wm)(Z,{name:"insert_remarks",label:"Add Remarks",class:"tab",disable:r.isProcessing},null,8,["disable"])])),_:1},8,["modelValue"]),(0,o.Wm)(Q),(0,o.Wm)(se,{modelValue:n.selected_section,"onUpdate:modelValue":t[16]||(t[16]=e=>n.selected_section=e),animated:"",class:"panels"},{default:(0,o.w5)((()=>[(0,o.Wm)(te,{name:"insert_docs"},{default:(0,o.w5)((()=>[(0,o.Wm)(ee,{onSubmit:(0,i.iM)(D.submitLog,["prevent"]),onValidationError:D.errorOnLog,autofocus:!0},{default:(0,o.w5)((()=>[(0,o.Wm)(j,{class:"title"},{default:(0,o.w5)((()=>[c])),_:1}),m,h,(0,o.Wm)(B,{class:"input",outlined:"",color:"secondary",modelValue:r.new_log_name,"onUpdate:modelValue":t[2]||(t[2]=e=>r.new_log_name=e),disable:r.isProcessing,counter:"",label:"Log Name",hint:"The name of this log or the general context of it, please keep it concise and easy to understand.",rules:[e=>e.length>=2||"This is required. Must have 2 characters above."],"lazy-rules":""},null,8,["modelValue","disable","rules"]),(0,o.Wm)(B,{class:"input",outlined:"",color:"secondary",modelValue:r.new_log_description,"onUpdate:modelValue":t[3]||(t[3]=e=>r.new_log_description=e),label:"Log Description",disable:r.isProcessing,counter:"",hint:"The context of this log. Please provide enough information as possible, but keep it clean.",rules:[e=>e.length>=8||"This is required. Must have 8 characters and above."],"lazy-rules":""},null,8,["modelValue","disable","rules"]),(0,o.Wm)(B,{class:"input",outlined:"",color:"secondary",modelValue:r.new_log_role,"onUpdate:modelValue":t[4]||(t[4]=e=>r.new_log_role=e),label:"Student's Role",disable:r.isProcessing,counter:"",hint:"The student's role from this log, generally more of a role from the job, keep it concise as possible.",rules:[e=>e.length>=4||"This is required. Must have 4 characters and above."],"lazy-rules":""},null,8,["modelValue","disable","rules"]),(0,o.Wm)(X,{class:"input",modelValue:r.new_log_file,"onUpdate:modelValue":t[5]||(t[5]=e=>r.new_log_file=e),label:"Document Proof (PDF Only, 5MB Max)",hint:"This is optionally recommended as this can be used as a supporting context. Should contain no sensitive information.",filled:"",multiple:"",clearable:"","lazy-rules":"",error:r.new_log_file_invalid,onFocus:t[6]||(t[6]=e=>r.new_log_file_invalid=!1),disable:r.isProcessing,accept:".pdf","max-file-size":"5242880"},{prepend:(0,o.w5)((()=>[(0,o.Wm)(Y,{name:"attach_file"})])),error:(0,o.w5)((()=>[p])),_:1},8,["modelValue","error","disable"]),(0,o.Wm)(B,{class:"input",filled:"",modelValue:r.new_log_date_start,"onUpdate:modelValue":t[9]||(t[9]=e=>r.new_log_date_start=e),mask:"date",label:"Log Date Start",error:r.new_log_date_start_invalid,readonly:"",disable:r.isProcessing,hint:"The date from where this log has started."},{append:(0,o.w5)((()=>[(0,o.Wm)(Y,{name:"event",class:"cursor-pointer"},{default:(0,o.w5)((()=>[(0,o.Wm)(K,{ref:"qDateProxy",cover:"","transition-show":"scale","transition-hide":"scale"},{default:(0,o.w5)((()=>[(0,o.Wm)(J,{modelValue:r.new_log_date_start,"onUpdate:modelValue":t[7]||(t[7]=e=>r.new_log_date_start=e),"today-btn":"",onClick:t[8]||(t[8]=e=>r.new_log_date_start_invalid=!1),options:D.optionsFn,color:"secondary"},{default:(0,o.w5)((()=>[(0,o._)("div",w,[(0,o.wy)((0,o.Wm)(W,{label:"Close",color:"primary",flat:""},null,512),[[ie]])])])),_:1},8,["modelValue","options"])])),_:1},512)])),_:1})])),error:(0,o.w5)((()=>[g])),_:1},8,["modelValue","error","disable"]),(0,o.Wm)(B,{class:"input",filled:"",modelValue:r.new_log_date_end,"onUpdate:modelValue":t[13]||(t[13]=e=>r.new_log_date_end=e),error:r.new_log_date_end_invalid,mask:"date",disable:r.isProcessing,label:"Log Date End",readonly:"",hint:"The date from where this log has ended. This is optional. However, when it contains a date, it should not start as early as the `Log Date Start`!"},{append:(0,o.w5)((()=>[r.new_log_date_end?((0,o.wg)(),(0,o.j4)(Y,{key:0,name:"cancel",onClick:t[10]||(t[10]=(0,i.iM)((e=>{r.new_log_date_end=null,r.new_log_date_end_invalid=!1}),["stop"])),class:"cursor-pointer"})):(0,o.kq)("",!0),(0,o.Wm)(Y,{name:"event",class:"cursor-pointer"},{default:(0,o.w5)((()=>[(0,o.Wm)(K,{ref:"qDateProxy",cover:"","transition-show":"scale","transition-hide":"scale"},{default:(0,o.w5)((()=>[(0,o.Wm)(J,{modelValue:r.new_log_date_end,"onUpdate:modelValue":t[11]||(t[11]=e=>r.new_log_date_end=e),onClick:t[12]||(t[12]=e=>r.new_log_date_end_invalid=!1),"today-btn":"",options:D.optionsFn,color:"secondary"},{default:(0,o.w5)((()=>[(0,o._)("div",f,[(0,o.wy)((0,o.Wm)(W,{label:"Close",color:"primary",flat:""},null,512),[[ie]])])])),_:1},8,["modelValue","options"])])),_:1},512)])),_:1})])),error:(0,o.w5)((()=>[b])),_:1},8,["modelValue","error","disable"]),(0,o._)("div",y,[(0,o.Wm)(W,{outline:"",class:"close",color:"red",label:"Clear Fields",onClick:D.clearLogForm,disable:r.isProcessing},null,8,["onClick","disable"]),(0,o.Wm)(W,{outline:"",type:"submit",class:"insert",color:"secondary",disable:r.isProcessing||null===this.new_log_name||""===this.new_log_name||null===this.new_log_description||""===this.new_log_description||null===this.new_log_role||""===this.new_log_role||null===this.new_log_file||""===this.new_log_file||null===this.new_log_date_start||""===r.new_log_date_start,label:"Insert"},null,8,["disable"])])])),_:1},8,["onSubmit","onValidationError"])])),_:1}),(0,o.Wm)(te,{name:"insert_remarks"},{default:(0,o.w5)((()=>[(0,o.Wm)(ee,{onSubmit:(0,i.iM)(D.submitRemark,["prevent"]),onValidationError:D.errorOnRemark,autofocus:!0},{default:(0,o.w5)((()=>[(0,o.Wm)(j,{class:"title"},{default:(0,o.w5)((()=>[k])),_:1}),T,N,(0,o.Wm)(B,{class:"input",outlined:"",color:"secondary",modelValue:r.new_remark_title,"onUpdate:modelValue":t[14]||(t[14]=e=>r.new_remark_title=e),disable:r.isProcessing,label:"Remark Title",counter:"",hint:"The general context of this remark. Make it concise but minimal as possible.",rules:[e=>e.length>=4||"This is required. Must have 4 characters and above."],"lazy-rules":""},null,8,["modelValue","disable","rules"]),(0,o.Wm)(B,{class:"input",outlined:"",color:"secondary",type:"textarea",disable:r.isProcessing,hint:"Please describe in detail regarding this context.",counter:"",modelValue:r.new_remark_description,"onUpdate:modelValue":t[15]||(t[15]=e=>r.new_remark_description=e),label:"Remark Description",rules:[e=>e.length>=8||"This is required. Must have 8 characters and above."],"lazy-rules":""},null,8,["disable","modelValue","rules"]),(0,o._)("div",S,[(0,o.Wm)(W,{outline:"",class:"close",color:"red",onClick:D.clearRemarkForm,disable:r.isProcessing,label:"Clear Fields"},null,8,["onClick","disable"]),(0,o.Wm)(W,{outline:"",class:"insert",color:"secondary",type:"submit",disable:r.isProcessing||null===r.new_remark_title||""===r.new_remark_title||null===r.new_remark_description||""===r.new_remark_description,label:"Insert"},null,8,["disable"])])])),_:1},8,["onSubmit","onValidationError"])])),_:1})])),_:1},8,["modelValue"])])),_:1},512),[[i.F8,r.existing_user]])]),(0,o._)("div",E,[(0,o.wy)((0,o.Wm)(M,{class:"my-card-new_user"},{default:(0,o.w5)((()=>[r.isProcessing?((0,o.wg)(),(0,o.j4)(A,{key:0,query:"",color:"secondary",class:"q-mt-sm"})):(0,o.kq)("",!0),(0,o.Wm)(j,{class:"title"},{default:(0,o.w5)((()=>[v])),_:1}),I,O,(0,o.Wm)(ee,{onSubmit:(0,i.iM)(D.submitNewStudent,["prevent"]),onValidationError:D.submitStudentFormError,autofocus:!0},{default:(0,o.w5)((()=>[(0,o._)("div",R,[(0,o.Wm)(B,{class:"inputnew",outlined:"",dense:"",color:"secondary",counter:"",modelValue:r.new_student_first_name,"onUpdate:modelValue":t[17]||(t[17]=e=>r.new_student_first_name=e),label:"First Name",rules:[e=>e.length>=2&&e.length<=32||"Invalid, this is required. Should contain 2 to 32 characters."],"lazy-rules":"",disable:r.isProcessing},null,8,["modelValue","rules","disable"]),(0,o.Wm)(B,{class:"inputnew",outlined:"",dense:"",color:"secondary",counter:"",modelValue:r.new_student_last_name,"onUpdate:modelValue":t[18]||(t[18]=e=>r.new_student_last_name=e),label:"Last Name",rules:[e=>e.length>=2&&e.length<=32||"Invalid, this is required. Should contain 2 to 32 characters."],"lazy-rules":"",disable:r.isProcessing},null,8,["modelValue","rules","disable"])]),(0,o.Wm)(B,{class:"input",outlined:"",dense:"",color:"secondary",modelValue:r.new_student_description,"onUpdate:modelValue":t[19]||(t[19]=e=>r.new_student_description=e),label:"Description",counter:"",hint:"Make the description formalized as the first entry will be imprinted in blockchain, student can change this information when logged on.",rules:[e=>!e.length||e.length>=8&&e.length<=256||"Cannot go less than 8 characters or more than 256 characters."],"lazy-rules":"",disable:r.isProcessing},null,8,["modelValue","rules","disable"]),(0,o._)("div",U,[(0,o.Wm)(B,{class:"inputnew",outlined:"",dense:"",color:"secondary",type:"email",modelValue:r.new_student_email,"onUpdate:modelValue":t[20]||(t[20]=e=>r.new_student_email=e),label:"E-mail",counter:"",error:r.new_student_email_invalid,onFocus:t[21]||(t[21]=e=>r.new_student_email_invalid=!1),hint:"Ask the student regarding what email to use as this will be exposed for contacting purposes.",disable:r.isProcessing,rules:[e=>e.includes("@")||"Invalid email format."],"lazy-rules":""},{error:(0,o.w5)((()=>[P])),_:1},8,["modelValue","error","disable","rules"]),(0,o.Wm)(B,{class:"inputnew",outlined:"",dense:"",color:"secondary",modelValue:r.new_student_username,"onUpdate:modelValue":t[22]||(t[22]=e=>r.new_student_username=e),label:"Username",hint:"This will be wary of this as it will be used to login.",error:r.new_student_username_invalid,disable:r.isProcessing,onFocus:t[23]||(t[23]=e=>r.new_student_username_invalid=!1),counter:"",rules:[e=>e.length>=8&&e.length<=24||"This should contain not less than 8 characters or more than 24 characters."],"lazy-rules":""},{error:(0,o.w5)((()=>[V])),_:1},8,["modelValue","error","disable","rules"])]),(0,o.Wm)(B,{class:"input",outlined:"",dense:"",color:"secondary",modelValue:r.new_student_personal_skills,"onUpdate:modelValue":t[24]||(t[24]=e=>r.new_student_personal_skills=e),label:"Personal Skills",counter:"",hint:"Similar to description but is specified to student's capability. Seperate the contents in comma. Be wary of the initial input as it will be imprinted in blockchain. Student can change this later on.",rules:[e=>e.length>=8||"This is required. Must have 8 characters and above."],"lazy-rules":"",disable:r.isProcessing},null,8,["modelValue","rules","disable"]),(0,o._)("div",C,[(0,o.Wm)(B,{class:"inputnew",outlined:"",dense:"",color:"secondary",modelValue:r.new_student_recent_program,"onUpdate:modelValue":t[25]||(t[25]=e=>r.new_student_recent_program=e),label:"Program",hint:"Do not use acronym, and do not prefix it with BS or Bachelor.",disable:r.isProcessing,counter:"",rules:[e=>e.length>=4&&e.length<=64||"This should contain not less than 4 characters or more than 24 characters."],"lazy-rules":""},null,8,["modelValue","disable","rules"]),(0,o.Wm)(B,{class:"inputnew",outlined:"",dense:"",color:"secondary",modelValue:r.new_student_recorded_year_level,"onUpdate:modelValue":t[26]||(t[26]=e=>r.new_student_recorded_year_level=e),label:"Year Level",type:"number",disable:r.isProcessing,hint:"Reference hint whether this student graduated in 3rd year or 5th year.",counter:"",rules:[e=>e>=3&&e<=5||"Year level cannot go below 2."],"lazy-rules":""},null,8,["modelValue","disable","rules"])]),(0,o.Wm)(B,{class:"input",outlined:"",dense:"",color:"secondary",modelValue:r.new_student_prefer_role,"onUpdate:modelValue":t[27]||(t[27]=e=>r.new_student_prefer_role=e),label:"Preferred Employment Role",disable:r.isProcessing,hint:"The preferred role the student infers. This is interchangeable but please provide an initial input. Therefore, ask your student regarding one.",counter:"",rules:[e=>e.length>=2&&e.length<=32||"This should contain not less than 2 characters or more than 32 characters."],"lazy-rules":""},null,8,["modelValue","disable","rules"]),(0,o._)("div",q,[(0,o.Wm)(B,{class:"inputnew",outlined:"",dense:"",color:"secondary",modelValue:r.new_student_password,"onUpdate:modelValue":t[29]||(t[29]=e=>r.new_student_password=e),label:"Student Password",disable:r.isProcessing,type:r.new_student_show_password?"text":"password",hint:"The password that the student will use to login.",counter:"",rules:[e=>e.length>=8&&e.length<=64||"This should contain not less than 8 characters or more than 64 characters."],"lazy-rules":""},{append:(0,o.w5)((()=>[(0,o.Wm)(Y,{name:r.new_student_show_password?"visibility":"visibility_off",class:"cursor-pointer",onClick:t[28]||(t[28]=e=>r.new_student_show_password=!r.new_student_show_password)},null,8,["name"])])),_:1},8,["modelValue","disable","type","rules"]),(0,o.Wm)(B,{class:"inputnew",outlined:"",dense:"",color:"secondary",modelValue:r.new_student_password_confirm,"onUpdate:modelValue":t[31]||(t[31]=e=>r.new_student_password_confirm=e),label:"Student Password Confirm",type:r.new_student_show_confirm_password?"text":"password",disable:r.isProcessing,hint:"Repeat the password to confirm the password.",counter:"",rules:[e=>e.length>=8&&e.length<=64&&e==r.new_student_password||"This should match your password to confirm your password."],"lazy-rules":""},{append:(0,o.w5)((()=>[(0,o.Wm)(Y,{name:r.new_student_show_confirm_password?"visibility":"visibility_off",class:"cursor-pointer",onClick:t[30]||(t[30]=e=>r.new_student_show_confirm_password=!r.new_student_show_confirm_password)},null,8,["name"])])),_:1},8,["modelValue","type","disable","rules"])]),(0,o._)("div",x,[(0,o.Wm)(W,{outline:"",class:"close",color:"red",label:"Clear Fields",onClick:D.clearRegistrationForm,disable:r.isProcessing},null,8,["onClick","disable"]),(0,o.Wm)(W,{outline:"",class:"insert",type:"submit",color:"secondary",disable:r.isProcessing||null===r.new_student_first_name||""===r.new_student_first_name||null===r.new_student_last_name||""===r.new_student_last_name||null===r.new_student_username||""===r.new_student_username||null===r.new_student_email||""===r.new_student_email||null===r.new_student_password||""===r.new_student_password||null===r.new_student_password_confirm||""===r.new_student_password_confirm||null===r.new_student_description||""===r.new_student_description||null===r.new_student_personal_skills||""===r.new_student_personal_skills||null===r.new_student_recent_program||""===r.new_student_recent_program||null===r.new_student_prefer_role||""===r.new_student_prefer_role,label:"Insert"},null,8,["disable"])])])),_:1},8,["onSubmit","onValidationError"])])),_:1},512),[[i.F8,r.new_user]])])]),(0,o.Wm)(oe,{position:"bottom-right",offset:[24,24]},{default:(0,o.w5)((()=>[n.targetted_number>0&&n.targetted_address?(0,o.wy)(((0,o.wg)(),(0,o.j4)(W,{key:0,fab:"",icon:"mdi-text-box-check",color:"amber",onClick:D.directToPortfolio},{default:(0,o.w5)((()=>[(0,o.Wm)(ne,{class:"bg-indigo",offset:[10,10],anchor:"center left",self:"center right"},{default:(0,o.w5)((()=>[(0,o.Uk)(" View Portfolio of "+(0,a.zw)(n.targetted_address),1)])),_:1})])),_:1},8,["onClick"])),[[ae]]):(0,o.kq)("",!0)])),_:1})])}n(5363),n(7768),n(71);var W=n(52),A=n.n(W),F=n(8825),G=n(1959),L=n(9582),$=n(2796);const H={setup(){const e=(0,F.Z)(),t=(0,L.yj)(),s=(0,L.tv)();return{$q:e,$route:t,$router:s,selected_section:(0,G.iH)("insert_docs"),targetted_address:(0,G.iH)(null),targetted_number:(0,G.iH)(null)}},data(){return{students:(0,G.iH)([]),focused_portfolio_address:(0,G.iH)(""),new_student_first_name:(0,G.iH)(""),new_student_last_name:(0,G.iH)(""),new_student_username:(0,G.iH)(""),new_student_email:(0,G.iH)(""),new_student_password:(0,G.iH)(""),new_student_password_confirm:(0,G.iH)(""),new_student_description:(0,G.iH)(""),new_student_personal_skills:(0,G.iH)(""),new_student_recent_program:(0,G.iH)(""),new_student_recorded_year_level:(0,G.iH)(4),new_student_prefer_role:(0,G.iH)(""),new_student_username_invalid:(0,G.iH)(!1),new_student_email_invalid:(0,G.iH)(!1),new_log_date_start_invalid:(0,G.iH)(!1),new_log_date_end_invalid:(0,G.iH)(!1),new_log_file_invalid:(0,G.iH)(!1),new_student_show_password:(0,G.iH)(!1),new_student_show_confirm_password:(0,G.iH)(!1),existing_user:(0,G.iH)(!1),new_user:(0,G.iH)(!1),isProcessing:(0,G.iH)(!1),isFetchingStudent:(0,G.iH)(!0),new_log_name:(0,G.iH)(""),new_log_description:(0,G.iH)(""),new_log_role:(0,G.iH)(""),new_log_file:(0,G.iH)(null),new_log_date_start:(0,G.iH)(null),new_log_date_end:(0,G.iH)(null),new_remark_title:(0,G.iH)(""),new_remark_description:(0,G.iH)("")}},mounted(){"new"===this.$route.params.action?(this.existing_user=!1,this.new_user=!0):(this.existing_user=!1,this.new_user=!1),this.getStudents(),null===this.targetted_number&&!1===this.existing_user&&!1===this.new_user&&this.$q.notify({color:"blue",position:"top",message:"Please select a student from the left side. Otherwise, create a new student.",timeout:5e3,progress:!0,icon:"info"})},methods:{submitNewStudent(){this.isProcessing=!0,A().post(`${$.sx}/node/receive_context`,{first_name:this.new_student_first_name,last_name:this.new_student_last_name,email:this.new_student_email,username:this.new_student_username,password:this.new_student_password_confirm,program:this.new_student_recent_program,year_level:this.new_student_recorded_year_level,preferred_role:this.new_student_prefer_role,description:this.new_student_description,skills:this.new_user_personal_skills},{headers:{"x-token":this.$q.localStorage.getItem("token")}}).then((e=>{this.$q.notify({color:"green",position:"top",message:"Student registration finished! Please let them know that an email has been sent.",timeout:5e3,progress:!0,icon:"report_problem"}),this.clearRegistrationForm(!1),this.isProcessing=!1})).catch((e=>{const t=void 0===e.response.data?`${e.message}. Server may be unvailable. Please try again later.`:e.response.data.detail;if(this.$q.notify({color:"negative",position:"top",message:`There was an error when submitting your credentials. Reason: ${t}`,timeout:5e3,progress:!0,icon:"report_problem"}),void 0!==e.response.data){let t=e.response.data.detail.split("UNIQUE constraint failed: ")[1];"users.email"==t?this.new_student_email_invalid=!0:"users.username"==t&&(this.new_student_username_invalid=!0)}this.isProcessing=!1}))},submitStudentFormError(){this.$q.notify({color:"negative",position:"top",message:"There was an error from one of the fields. Please check and try again.",timeout:5e3,progress:!0,icon:"report_problem"})},clearRegistrationForm(e=!0){this.new_student_first_name=null,this.new_student_last_name=null,this.new_student_username=null,this.new_student_email=null,this.new_student_password=null,this.new_student_password_confirm=null,this.new_student_description=null,this.new_student_personal_skills=null,this.new_student_recent_program=null,this.new_student_recorded_year_level=1,this.new_student_prefer_role=null,this.new_student_show_password=!1,this.new_student_show_confirm_password=!1,this.new_student_email_invalid=!1,this.new_student_username_invalid=!1,e&&this.$q.notify({color:"green",position:"top",message:"Student registration fields has been cleared!",timeout:5e3,progress:!0,icon:"mdi-account-check"})},submitLog(){if(this.isProcessing=!0,null==this.new_log_date_start)this.$q.notify({color:"negative",position:"top",message:"Duration start field is required!",timeout:5e3,progress:!0,icon:"report_problem"}),this.isProcessing=!1;else{if(null!==this.new_log_date_end){let e=new Date(this.new_log_date_start),t=new Date(this.new_log_date_end);if("Invalid Date"!==t.toTimeString()){if(t<e)return this.$q.notify({color:"negative",position:"top",message:"Duration end seems to be earlier than the duration start. Please fix that.",timeout:5e3,progress:!0,icon:"report_problem"}),this.new_log_date_start_invalid=!0,this.new_log_date_end_invalid=!0,void(this.isProcessing=!1)}else this.new_log_date_end=null}let e=new FormData;e.append("address_origin",this.targetted_address),e.append("name",this.new_log_name),e.append("description",this.new_log_description),e.append("role",this.new_log_role),e.append("duration_start",new Date(this.new_log_date_start).toISOString()),null!==this.new_log_date_end&&e.append("duration_end",new Date(this.new_log_date_end).toISOString()),null!==this.new_log_file&&e.append("file",this.new_log_file[0]),A().post(`${$.sx}/node/receive_context_log`,e,{headers:{"X-Token":this.$q.localStorage.getItem("token"),"Content-Type":"multipart/form-data"}}).then((e=>{this.$q.notify({color:"green",position:"top",message:`Log information has been sent from the node to blockchain! Remember about the notice regarding taking the new information in-effect. | Info: ${e.data.detail}`,timeout:5e3,progress:!0,icon:"report_problem"}),this.clearLogForm(!1),this.isProcessing=!1})).catch((e=>{const t=void 0===e.response.data?`${e.message}. Server may be unvailable. Please try again later.`:e.response.data.detail;this.$q.notify({color:"negative",position:"top",message:`There was an error when submitting log information. Reason: ${t}`,timeout:5e3,progress:!0,icon:"report_problem"}),this.isProcessing=!1}))}},errorOnLog(){this.$q.notify({color:"negative",position:"top",message:"There was an error from one of the log fields. Please check and ensure that all conditions are met, then try again.",timeout:5e3,progress:!0,icon:"report_problem"}),null!==this.new_log_file&&""!==this.new_log_file||(this.new_log_file_invalid=!0),null!==this.new_log_date_start&&""!==this.new_log_date_start||(this.new_log_date_start_invalid=!0)},clearLogForm(e=!0){this.new_log_name=null,this.new_log_description=null,this.new_log_role=null,this.new_log_file=null,this.new_log_date_start=null,this.new_log_date_end=null,this.new_log_file_invalid=!1,this.new_log_date_start_invalid=!1,this.new_log_date_end_invalid=!1,e&&this.$q.notify({color:"green",position:"top",message:"Log referral fields has been cleared!",timeout:5e3,progress:!0,icon:"mdi-account-check"})},submitRemark(){this.isProcessing=!0,null==this.targetted_address?this.$q.notify({color:"negative",position:"top",message:`There was an error when submitting extra information. Reason: ${e.request.statusText}`,timeout:5e3,progress:!0,icon:"report_problem"}):A().post(`${$.sx}/node/receive_context`,{address_origin:this.targetted_address,title:this.new_remark_title,description:this.new_remark_description},{headers:{"X-Token":this.$q.localStorage.getItem("token")}}).then((e=>{this.$q.notify({color:"green",position:"top",message:`Extra information has been sent from the nodes to blockchain! Remember about the notice regarding taking the new information in-effect. | Info: ${e.data.detail}`,timeout:5e3,progress:!0,icon:"report_problem"}),this.clearRemarkForm(!1),this.isProcessing=!1})).catch((e=>{const t=void 0===e.response.data?`${e.message}. Server may be unvailable. Please try again later.`:e.response.data.detail;this.$q.notify({color:"negative",position:"top",message:`There was an error when submitting extra information. Reason: ${t}`,timeout:5e3,progress:!0,icon:"report_problem"}),this.isProcessing=!1}))},errorOnRemark(){this.$q.notify({color:"negative",position:"top",message:"There was an error from one of the remark fields. Please check and ensure that all conditions are met, then try again.",timeout:5e3,progress:!0,icon:"report_problem"})},clearRemarkForm(e=!0){this.new_remark_title=null,this.new_remark_description=null,e&&this.$q.notify({color:"green",position:"top",message:"Student remark fields has been cleared!",timeout:5e3,progress:!0,icon:"mdi-account-check"})},optionsFn(e){let t=new Date;return t.setDate(t.getDate()),new Date(null).toISOString().slice(0,10).replaceAll("-","/")>=e||e<=t.toISOString().slice(0,10).replaceAll("-","/")},setActiveFieldForForm(e){this.targetted_number=e,this.targetted_address=this.students[e-1].address,this.clearRemarkForm(!1),this.clearLogForm(!1)},getStudents(){this.isFetchingStudent=!0,A().get(`${$.sx}/dashboard/students`,{headers:{"X-Token":this.$q.localStorage.getItem("token")}}).then((e=>{let t=1,s=[];for(let n of e.data)n.id=t,t+=1,s.push(n);this.students=s,this.isFetchingStudent=!1})).catch((e=>{this.$q.notify({color:"negative",position:"top",message:`Cannot fetch students. Reason: ${e.message}`,timeout:5e3,progress:!0,icon:"report_problem"}),this.isFetchingStudent=!1}))},directToPortfolio(){this.$router.push({path:"/portfolio",query:{address:this.targetted_address}})}}};var M=n(4260),Z=n(8240),z=n(151),Q=n(1598),j=n(7704),B=n(3414),Y=n(2035),X=n(5096),J=n(2350),K=n(7547),ee=n(3269),te=n(5869),se=n(5906),ne=n(6602),oe=n(5269),ae=n(5589),ie=n(4689),re=n(1052),le=n(4554),de=n(3944),_e=n(6915),ue=n(1007),ce=n(8870),me=n(6489),he=n(677),pe=n(7518),we=n.n(pe);const ge=(0,M.Z)(H,[["render",D],["__scopeId","data-v-0a6fcb04"]]),fe=ge;we()(H,"components",{QBtn:Z.Z,QCard:z.Z,QLinearProgress:Q.Z,QScrollArea:j.Z,QItem:B.Z,QItemSection:Y.Z,QAvatar:X.Z,QItemLabel:J.Z,QTabs:K.Z,QTab:ee.Z,QSeparator:te.Z,QTabPanels:se.Z,QTabPanel:ne.Z,QForm:oe.Z,QCardSection:ae.Z,QInput:ie.Z,QFile:re.Z,QIcon:le.Z,QPopupProxy:de.Z,QDate:_e.Z,QPageSticky:ue.Z,QTooltip:ce.Z}),we()(H,"directives",{Ripple:me.Z,ClosePopup:he.Z})}}]);