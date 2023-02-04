# `folioblocks`

[![wakatime](https://wakatime.com/badge/user/b3774db8-dd9f-4205-a646-ef6d27645187/project/dd222932-a056-4c3b-87e1-d845f3aa14ee.svg)](https://wakatime.com/badge/user/b3774db8-dd9f-4205-a646-ef6d27645187/project/dd222932-a056-4c3b-87e1-d845f3aa14ee)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=CodexLink_folioblocks&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=CodexLink_folioblocks)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=CodexLink_folioblocks&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=CodexLink_folioblocks)

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/2a71cf953cf14f97beae8fa4d614b1c0)](https://www.codacy.com/gh/CodexLink/folioblocks/dashboard?utm_source=github.com&utm_medium=referral&utm_content=CodexLink/folioblocks&utm_campign=Badge_Grade)
[![CodeFactor](https://www.codefactor.io/repository/github/codexlink/folioblocks/badge)](https://www.codefactor.io/repository/github/codexlink/folioblocks)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=CodexLink_folioblocks&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=CodexLink_folioblocks)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=CodexLink_folioblocks&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=CodexLink_folioblocks)

_The monorepo of the thesis' system named as "Design of a Credential Verification System using Blockchain Technology" or "folioblocks"._

**Folioblocks** is a blockchain-based (_consortium-type, from-the-scratch, and opinionated_) **credential verification system** that allows for individuals to safely secure their credentials managed by their trusted and official institution or career/education-based organization.

> This repository is aimed to become as an example as a project where other people who uses similar technologies or other people who is in the same bridge who wants to develop their own blockchain system to relate and understood how things were incorporated from one another.

> This is not provided or was published as a way of free money but is intended for educational purposes only.

## Notice

**This is a project is a highly experimental project and should be known as a Proof-of-Concept (PoC) type of project!**

If you consider on attempting to explore this project even further, please proceed with caution!!! **Do not hesistate to contact me through email if you have any questions!**

## Notice [1]

Some of the contents of this README has been **removed** in the meantime. Please wait for a while as I try to document everything. Please check the issues section for more information.

## Members

The following are the group members or associates of this project.

- **Don G. Noriega** — _Railway Engineering_
- **Janrey T. Licas** — _Intelligent Systems_ | _Backend Developer, Frontend Co-Developer, Project Lead, Project Maintainer, Quality Assurance_
- **Alexander C. Marjes** — _System Administration_
- **Ronan C. Marasigan** — _System Administration_ | _Frontend Developer_
- **Engr. Verlyn Nojor-Vicente** — _Adviser for this Group_

> A detailed contribution of each members will be disclosed soon as the progression of the documentation continues. Please follow this [issue](https://github.com/CodexLink/folioblocks/issues/3) for more information.

## References

The following links are references that we used at a certain section of the documentation or from a certain scenario where it helped us. This may contain references that weren't used or used as a bridge to another reference.

> References may be included from the paper but references from the paper **will not be included!**

## Calculation Basis

References contains an article to which was modified by the lead developer in order to accomodate 5 metrics that differs to the 3 consensus mechanisms.

- _How To Calculate CPU Utilization_ - <https://www.embedded.com/how-to-calculate-cpu-utilization/>
- _Forum: What is CPU utilisation and how it can be calculated or measure?_ - <https://www.eukhost.com/forums/forum/general/technology-forum/22321-what-is-cpu-utilisation-and-how-it-can-be-calculated-or-measure>
- _Stackoverflow: How is CPU usage calculated?_ - <https://stackoverflow.com/questions/3748136/how-is-cpu-usage-calculated>

### Inspiration and Design Considerations for Implementing and Designing Three System as Consortium Mechanism for the Blockchain System

The references were used as a **reading** materials to better understand what part of the system will differ and how it will impact the system as a whole when different approaches where used to implement the blockchain system.

Consortium was in favor with the system that is supposed to be integrated along with the blockchain system because of the need of transparency of the issuance of the certification towards to the user of the system.

- _Consortium Blockchain-Based Decentralized Stock Exchange Platform_ - <https://ieeexplore.ieee.org/abstract/document/9127940>
- _DefenseChain: Consortium Blockchain for Cyber Threat Intelligence Sharing and Defense_ - <https://ieeexplore.ieee.org/abstract/document/9223313>
- _Design Consideration: Calling Conventions for the Participating Nodes in the Blockchain - <https://www.sofi.com/learn/content/what-are-nodes/>
- _Design Consideration: Choosing the right consensus mechanism: Sawtooth's Proof-of-Elapsed-Time (PoET) (Used for extra information) - <https://www.geeksforgeeks.org/consensus-algorithms-in-blockchain/>
- _Design Consideration: Understanding the blockchain vulnerabilities such as the 51% attack_ - <https://s3.ap-northeast-2.amazonaws.com/journal-home/journal/jips/fullText/90/jips_530.pdf>
- _Design Consideration: Understanding Consensus Mechanism and its internal steps to produce consensus, `What Are Consensus Mechanisms in Blockchain and Cryptocurrency?` - <https://www.investopedia.com/terms/c/consensus-mechanism-cryptocurrency.asp>
- _Hybrid-IoT: Hybrid Blockchain Architecture for Internet of Things - PoW Sub-blockchains_ - <https://arxiv.org/pdf/1804.03903.pdf>
- _Proof-of-Elapsed-Time, Concensus of Choice, Backed by Performance ANalaysis from the Sawtooth Blockchain Framework (Used as a final choice as a bias for the development of the blockchain system)_ - <https://www.cs.uoregon.edu/Reports/MS-201906-Corso.pdf>
- _Public, Private, Permissioned Blockchains Compared_ - <https://www.investopedia.com/news/public-private-permissioned-blockchains-compared/>
- _Storing Files on the Blockchain is a “Stupid Idea”_ - <https://www.cryptyk.io/storing-files-blockchain-stupid-idea/>
- _Session-based Authentication: Why JWT for now, and why consider OAuth later_ - <https://stackoverflow.com/questions/39909419/what-are-the-main-differences-between-jwt-and-oauth-authentication>
- _Trends in Development of Databases and Blockchain (**Used as an insight for considering blockchain frameworks and their consensus mechanism**)_ - <https://arxiv.org/pdf/2003.05687.pdf>
- _Why is Fernet only AES-128-CBC? (Design consideration as part of encrypting and decrpyting contents while using SHA256 for the content signature)_ - <https://crypto.stackexchange.com/questions/43120/why-is-fernet-only-aes-128-cbc>

### Additional Courses Taken

The following is the only resources aside from articles that were used in order to build the system with a blockchain system incorporated to it. This was only used by the `lead developer` of the team.

- _Blockchain A-Z™: Learn How To Build Your First Blockchain_ - <https://www.udemy.com/course/build-your-blockchain-az/>

### Git Repository and Issues

This sub-part of the reference includes git issues and repositories that further helped me debug and develop the whole system. Please note that this is far different from the section `Utilities / Tools Used`
- _python/mypy - Class `Base` is invalidated due to dynamic typing not properly handled_ - <https://github.com/python/mypy/issues/6372>
- _python/mypy - dynamic typing were inproperly handled in the case of `sqlalchemy`_ - <https://github.com/python/mypy/issues/2477#issuecomment-703142484>
- _tiangolo/fastapi - Problematic startup due to argument passed is not correct_ - <https://github.com/tiangolo/fastapi/issues/1495#issuecomment-643676192>
- _tiangolo/fastapi - Overriding the default output from the logs with a better log output_ - <https://github.com/tiangolo/fastapi/issues/1508>
- _tiangolo/fastapi - Priting logs without colorization through the `stdout` stream_ - <https://github.com/tiangolo/fastapi/issues/1276#issuecomment-615877177>
- _tiangolo/fastapi - running FastAPI along with other asynchronous processes which results to a monolithic system_ - <https://github.com/tiangolo/fastapi/issues/543>
- _encode/databases - sample code for running simple query tasks with the connected database, at line 188_ - <https://github.com/encode/databases/blob/master/tests/test_databases.py#L188>
- _vue-qrcode, QR code component for Vue.js_ - <https://github.com/fengyuanchen/vue-qrcode>

### Guides for the System Development

This part of the reference section contains alot! They are the onces that helped me the most when I had no one else to help in the development. With that, these references helped me understood some technologies that I have never used.

- _Building An Vue.js App With Azure Static Web Apps Services_ - <https://medium.com/bb-tutorials-and-thoughts/building-an-vue-js-app-with-azure-static-web-apps-service-270be990e39d>
- _Docker: Reference documentation_ - <https://docs.docker.com/reference/>
- _Docker Configuration: How to Set Docker Memory and CPU Usage Limit_ - <https://phoenixnap.com/kb/docker-memory-and-cpu-limit>
- _Docker Configuration: Understanding codenames with respect to sizes_ - <https://medium.com/swlh/alpine-slim-stretch-buster-jessie-bullseye-bookworm-what-are-the-differences-in-docker-62171ed4531d>
- _Azure Container Instance: Creating a YAML single file to multi-container whilst single deploy - <https://learn.microsoft.com/en-us/azure/container-instances/container-instances-reference-yaml>
- _Azure Container Instance: Deploy a multi-container group_ - <https://learn.microsoft.com/en-us/azure/container-instances/container-instances-multi-container-yaml>
- _Azure Container Instance: Deploying a container_ - <https://learn.microsoft.com/en-us/azure/container-instances/container-instances-tutorial-deploy-app>
- _Azure Container Instance: Enabling a TLS endpoint in a sidecar container_ - <https://learn.microsoft.com/en-us/azure/container-instances/container-instances-container-group-ssl>
- _Azure Container Instance: Mount an Azure file share in Azure Container Instances_ - <https://learn.microsoft.com/en-us/azure/container-instances/container-instances-volume-azure-files>
- _Azure Container Instance: Retrieve container logs and events in Azure Container Instances_ - <https://learn.microsoft.com/en-us/azure/container-instances/container-instances-get-logs>
- _Azure Container Instance Troubleshooting: Error while creating container using YML file_: <https://learn.microsoft.com/en-us/answers/questions/35424/error-while-creating-container-using-yml-file(cont>
- _Docker Setup: Multistage Deployment (*Unused due to time limitation on understanding it further*)_ - <https://github.com/akpircher/multistage-dockerfile-demo>
- _Encryption: PyCryptodome - Advanced Encrpytion Standard (AES) Implementation and Usage_ - <https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html>
- _FastAPI: Async SQL (Relational) Databases_ - <https://fastapi.tiangolo.com/advanced/async-sql-databases/?h=sql#import-and-set-up-sqlalchemy>
- _Github: Creating an empty `gh-pages` without inheritance on other branches_ - <https://blog.ediri.io/how-to-create-a-github-gh-pages-branch-in-an-existing-repository>
- _Github Actions: Caching `node_modules` with `yarn`_ - <https://dev.to/mattpocockuk/how-to-cache-nodemodules-in-github-actions-with-yarn-24eh>
- _HTTP Response Status Codes_ - <https://developer.mozilla.org/en-US/docs/Web/HTTP/Status>
- _Logging & Tracing in Python, FastApi, OpenCensus and Azure_ - <https://dev.to/tomas223/logging-tracing-in-python-fastapi-with-opencensus-a-azure-2jcm>
- _Python: Creating Custom Exceptions_ - <https://www.programiz.com/python-programming/user-defined-exception>
- _Python: Deleting files and Directories_ - <https://pynative.com/python-delete-files-and-directories/>
- _Python: Understanding `type <callable>`_ - <https://www.javatpoint.com/python-callable-function>
- _Python: Logging an Exception_ - <https://www.geeksforgeeks.org/how-to-log-a-python-exception/>
- _Python Async Databases: Issue about `PRAGMA` foreign_keys_ - <https://github.com/encode/databases/issues/169>
- _Python AsyncIO: Understanding `run_in_executor` for IO operation_ - <https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.run_in_executor>
- _Python AsyncIO: Avoiding Issues when Waiting Multiple Events - <https://python.plainenglish.io/how-to-avoid-issues-when-waiting-on-multiple-events-in-python-asyncio-48e22d148de7>
- _Python Cryptography: Asymmetric Cryptography with Python (Implementing RSA and ECC, but was unused in implementation, but rather, the general idea)_ - <https://medium.com/@ashiqgiga07/asymmetric-cryptography-with-python-5eed86772731>
- _Python Cryptography: Switching to Full-Crypto-Based Functions and Identifying Unsafe Functions for randomization_ - <https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html#secure-random-number-generation>
- _Python Cryptography: Using AES to decrypt/encrypt contents to render in the main system_ - <https://stackoverflow.com/questions/61420893/python-3-encrypt-and-decrypt-image-using-aes>
- _Python DRY: Parameterized Decorator_ - HOW-TO #1: <https://www.geeksforgeeks.org/creating-decorator-inside-a-class-in-python/>, HOT-TO#2: <https://stackoverflow.com/questions/5929107/decorators-with-parameters>
- _Python OOP: Understanding `@class` and `static` Class methods_ - <https://www.geeksforgeeks.org/class-method-vs-static-method-python/>
- _Python Package Manager: Failing through installation, best practices to avoid timeouts_ - <https://www.tutorialexample.com/best-practice-to-set-python-pip-install-timeout-and-retry-times-for-beginners-python-tutorial/>
- _SSL Certification for the Backend: Auto-generate SSL with Sidecar container `caddy`_ - <https://www.raeffs.dev/blog/2021/05-mai/25-autogenerate-ssl-certificates-for-aci/>
- _SSL Certification for the Backend: Another `but working` guide for SSL auto-generation + use previously saved SSL cert with `caddy`_ - <https://itnext.io/automatic-https-with-azure-container-instances-aci-4c4c8b03e8c9> 
- _Signals: Identifying the right `SYSCALL` to gracefully exit instances_ - <https://bash.cyberciti.biz/guide/Sending_signal_to_Processes>
- _Understanding `Docker Stack`_ - <https://www.ronaldjamesgroup.com/article/docker-stack>
- _Using my `prototype` system as a basis for re-developing the system into fully-pledge (folioblocks-web-prototype)_ - <https://github.com/CodexLink/folioblocks-web-prototype>
- _Vue.js, Baseline Guide for Creating a Search Bar (Not entirely used, used for functionality basis)_ - <https://blog.logrocket.com/create-search-bar-vue/>
- _Vue.js, Watchers_ - <https://vuejs.org/guide/essentials/watchers.html>

### Problem Basis

References were used to formulate the support structure of the problem described in the presentation.

- _Base Problem #1, The rise of fake credentials – A different kind of identity theft_ - <https://www.sterlingrisq.com/blog/the-rise-of-fake-credentials-a-different-kind-of-identity-theft>
- _Base Problem #2, False credentials and fake job histories: How applicants misrepresent themselves_ - <https://checkpoint.cvcheck.com/false-credentials-and-fake-job-histories-how-applicants-misrepresent-themselves/>
- _Confirming that fake credentials that it is a serious threat_ - <http://www.csc.gov.ph/new-updates/2103-fake-credentials-an-offense-of-serious-dishonesty-%E2%80%93-csc.html>
- _Effect from the Base Problems, identifying potential domino effects_ - <https://www.quora.com/How-useful-are-fake-degrees-in-the-employment-field-Do-most-companies-verify-and-what-are-the-risks-to-an-applicant-with-fake-credentials>
- _Extension from the effect of the base problems, the supporting article `False credentials and fake job histories: How applicants misrepresent themselves`_ - <https://checkpoint.cvcheck.com/false-credentials-and-fake-job-histories-how-applicants-misrepresent-themselves/>
- _Basis: Employment Rates and Crisis, The Effects of the East Asian Crisis on the Employment of Women and Men: The Philippine Case_ - <https://www.sciencedirect.com/science/article/abs/pii/S0305750X00000231>
- _Understanding the employee's status as part of identifying the user's of the system_ - <https://www.perkbox.com/uk/resources/blog/worker-or-employee-what-is-employment-status>

### Supporting Documents for the Problems

References were used to further strengthen our stand about credentials being critical being as it was commonly used to abuse the system in terms of integrity.

- _Educational imposters and fake degrees_ - <https://www.sciencedirect.com/science/article/abs/pii/S0276562410000685>

- _An Introduction to the Economics of Fake Degrees_ - <https://www.tandfonline.com/doi/abs/10.1080/00213624.2008.11507173>
- _Educational Authority in the ‘‘Open Door’’ Marketplace: Labor Market Consequences of For-profit, Nonprofit, and Fictional Educational Credentials_ - <https://journals.sagepub.com/doi/abs/10.1177/0038040716652455>
- _The human problem behind credential theft and reuse_ - <https://www.ingentaconnect.com/content/hsp/jcs/2021/00000004/00000003/art00004#Refs>
- _The Real and the Fake Degree and Diploma Mills_ - <https://eric.ed.gov/?id=EJ832770>

### Supporting Documents for the Beneficial Usage of Blockchain to a Main System

- _Exploring blockchain technology and its potential applications for education_ - <https://slejournal.springeropen.com/counter/pdf/10.1186/s40561-017-0050-x.pdf>
- _The Advantages and Disadvantages of the Blockchain Technology_ - <https://ieeexplore.ieee.org/abstract/document/8592253>
- _Proposing a reliable method of securing and verifying the credentials of graduates through blockchain_ - <https://www.proquest.com/docview/2545289280?pq-origsite=gscholar&fromopenview=true>

### Supporting Documents for the Implementation of Components of the Blockchain System

- _A Survey on Consensus Mechanisms and Mining Strategy Management in Blockchain Networks (Choosing the right consensus mechanism)_ - Preview: <https://ieeexplore.ieee.org/document/8629877> | Full Version: <https://arxiv.org/pdf/1805.02707.pdf>
- _Bitcoin: reaching consensus in distributed systems (Understanding the consensus mechanism in the blockchain system)_ - <https://witestlab.poly.edu/blog/get-rich-on-fake-bitcoins/>

### Standards: Initial

References are some of the standards that was used initially, but was changed throughout the thesis project due to inability to use it due to incomplete stage.

- _IEEE 1008-1987 — IEEE Standard for Software Unit Testing_ - <https://ieeexplore.ieee.org/document/27763>
- _ISO/TR 23244:2020 — Blockchain and distributed ledger technologies — Privacy and personally identifiable information protection considerations_ - <https://www.iso.org/obp/ui/#iso:std:iso:tr:23244:ed-1:v1:en>
- _ISO/TR 23455:2019 — Blockchain and distributed ledger technologies — Overview of and interactions between smart contracts in blockchain and distributed ledger technology systems_ - <https://www.iso.org/obp/ui/#iso:std:iso:tr:23455:ed-1:v1:en>
- _PEP 8 — Style Guidelines for Python Code_ - <https://www.python.org/dev/peps/pep-0008/>
- _PEP 484 — Type Hints_ - <https://www.python.org/dev/peps/pep-0484/>

### Standards: Finalized

TODO

### Stackoverflow References

This subsection of the reference is literally very long than the entire README! Please use `Table of Contents` to skip this section if you don't want to scroll through it!

TODO

### Utilities / Tools Used

References indicated are tools or utilities that I used to debug, generate entities for PoC, and etc.

- _Code Image: Carbon_ - <https://carbon.now.sh/>
- _Lorem Picsum (Literally lorem ipsum, but in images)_ - <https://picsum.photos/>
- _Material Design Guidelines: The Color Tool_ - <https://m2.material.io/resources/color/>
- _JSON Formatter and Validator_ - <https://jsonformatter.curiousconcept.com/>
- _QR Code Generator_ - <https://www.qr-code-generator.com/>
- _regex101: build, test, and debug regex_ - <https://regex101.com/>
- _SSL Encryption for the Backend: Let's Encrypt_ - <https://letsencrypt.org>
- _SSL Encryption for the Backend: Certbot_ - <https://certbot.eff.org/> 
- _This Person Does Not Exists_ - <https://thispersondoesnotexist.com/>
- _ui-avatars (For the generation of UI default avatar)_ - <https://github.com/LasseRafn/ui-avatars>
