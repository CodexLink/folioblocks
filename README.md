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

### Calculation Basis

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
- _Python AsyncIO: Avoiding Issues when Waiting Multiple Events_ - <https://python.plainenglish.io/how-to-avoid-issues-when-waiting-on-multiple-events-in-python-asyncio-48e22d148de7>
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

This sub-section contains some list from the sub-section `Standards: Initial`, they were changed due to misaligned goals or just incomprehensible to the point where it does not directly shows as a solution or a factor to consider when making the design.


- _PEP 8 — Style Guidelines for Python Code_ - <https://www.python.org/dev/peps/pep-0008/>

### StackOverflow References

**This subsection of the reference is literally very long than the entire README!** I don't blame my willingness to include the credibility of these people from asking these questions! Please use `Table of Contents` to skip this section if you don't want to scroll through it!

Also, this contains references that helped me further debug and do complex implementations, wherein specific cases are very rare to find. Link archiving started from February 01, 2022 and onwards, this implies that I did some early research but not alot than the specified date due to the time set for prototyping a system.

- _API Best Practice Advise: 'Logout: GET or POST?' (Debating what HTTP method should I used for API endpoint `/logout`)_ - <https://stackoverflow.com/questions/3521290/logout-get-or-post>
- _Docker, `dockerfile`: Conditional `COPY`_ - <https://stackoverflow.com/questions/63728819/conditional-copy-in-dockerfile>
- _Docker, `dockerfile`: Conditional `ENV`_ - <https://stackoverflow.com/questions/37057468/conditional-env-in-dockerfile>
- _Docker, `dockerfile`: Passing `ARG` value to the `ENTRYPOINT`_ - <https://stackoverflow.com/questions/34324277/how-to-pass-arg-value-to-entrypoint>
- _Docker, `dockerfile`: `if-else` condition with external arguments_ - <https://stackoverflow.com/questions/43654656/dockerfile-if-else-condition-with-external-arguments>
- _FastAPI: Attempting to multi-thread to do blockchain hashing mechanism without blocking the main thread ('came to a conclusion of using `asyncio.run_in_executor()`')_ - <https://stackoverflow.com/questions/66541289/python-fastapi-multi-threading-processing-start-stop-process-with-api-endpo>
- _FastAPI: API endpoints from Docker is not detected or registered through the logging system_ - <https://stackoverflow.com/questions/63510041/adding-python-logging-to-fastapi-endpoints-hosted-on-docker-doesnt-display-api>
- _FastAPI: Patching the logging system with a customized format through library `logging`_ - <https://stackoverflow.com/questions/62934384/how-to-add-timestamp-to-each-request-in-uvicorn-logs>
- _FastAPI: Understanding the `loggers` and its `handlers` and applying changes to filter levels with `dictConfig()`_ - <https://stackoverflow.com/questions/25187083/python-logging-to-multiple-handlers-at-different-log-levels>
- _FastAPI (Uvicorn Backend), Problem enabling Uvicorn auto-restart when launching programmatically with uvicorn.run_ - <https://stackoverflow.com/questions/52784924/problem-enabling-uvicorn-auto-restart-when-launching-programmatically-with-uvico>
- _FastAPI Models: Value Error Missing when using POST (This was due to `response_model` not set)_ - <https://stackoverflow.com/questions/68139116/value-error-missing-when-using-post-with-fastapi>
- _FastAPI Security: Securing FastAPI with JWT TOken-based Authentication_ - <https://testdriven.io/blog/fastapi-jwt-auth/#jwt-authentication>
- _Function Naming Convention: what was the opposite of `init()`_ - <https://softwareengineering.stackexchange.com/questions/163004/what-is-the-opposite-of-initialize-or-init>
- _HTTP Code, Finding Suitability based on Situation: What is the HTTP Code for `Not Ready Yet, Try Again Later?`_ - <https://stackoverflow.com/questions/9794696/which-http-status-code-means-not-ready-yet-try-again-later#:~:text=Retry%2DAfter%20is%20also%20valid,too%20much%20work%20to%20do>
- _MyPy: Unable to detect modules from other directories_ - <https://stackoverflow.com/questions/60873894/mypy-cant-find-submodule>
- _Python `ArgumentParser` Library: Best practices for the validation of the context passed in the parameter_ - <https://stackoverflow.com/questions/37471636/python-argument-parsing-validation-best-practices>
- _Python AsyncIO: Implementing an Asynchronous `__init__` method for class and use `await` for instantiation_ - <https://stackoverflow.com/questions/33128325/how-to-set-class-attribute-with-await-in-init>
- _Python AsyncIO: Keyword arguments to pass on a async function (**Afaik, this search was made possible by creating a wrapper library that takes `aiohttp` and create an queueing system**)_ - <https://stackoverflow.com/questions/23946895/requests-in-asyncio-keyword-arguments>
- _Python AsyncIO: Understanding the calls for an async method from a class_ - <https://stackoverflow.com/questions/42009202/how-to-call-a-async-function-contained-in-a-class>
- _Python AsyncIO: Understanding why `run_in_executor`() is fine vs. multithreading library_ - <https://stackoverflow.com/questions/55027940/is-run-in-executor-optimized-for-running-in-a-loop-with-coroutines>
- _Python AsyncIO: Pythonic way on waiting a coroutine to finish, (**I forgot to do this, and instead I used their low level API to wait instead of creating an `Event` flag**)_ - <https://stackoverflow.com/questions/65352682/python-asyncio-pythonic-way-of-waiting-until-condition-satisfied>
- _Python AsyncIO: Waiting for `stdin` input stream while there's a background process_ - <https://stackoverflow.com/questions/58454190/python-async-waiting-for-stdin-input-while-doing-other-stuff>
- _Python `datetime`: Converting a string back `isoformat()` to a `datetime` object_ - <https://stackoverflow.com/questions/28331512/how-to-convert-pythons-isoformat-string-back-into-datetime-object>
- _Python Dictionary: Sorting a list from the dictionary_ - <https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary>
- _Python Dictionary: Copying a dictionary without modifying the original reference (**This issue was inspired from the C's datetime object problem wherein a copied object reflects the changes to the original object**)_ - <https://stackoverflow.com/questions/2465921/how-to-copy-a-dictionary-and-only-edit-the-copy>
- _Python Enum Object: Checking if string exists in Enum of Strings_ - <https://stackoverflow.com/questions/63335753/how-to-check-if-string-exists-in-enum-of-strings>
- _Python Enum Objet: Checking if there's an `int` inside of an Enum object_ - <https://stackoverflow.com/questions/43634618/how-do-i-test-if-int-value-exists-in-python-enum-without-using-try-catch>
- _Python Environmental Variable Display on `pwsh` prompt is duplicated_ - <https://stackoverflow.com/questions/16257950/how-to-create-a-python-virtualenv-environment-without-prompt-prefix>
- _Python Exceptions: How to properly ignore them?_ - <https://stackoverflow.com/questions/730764/how-to-properly-ignore-exceptions>
- _Python Function Definition: Understanding the Bare Asterisk (`*`) in the function parameter_ - <https://stackoverflow.com/questions/14301967/bare-asterisk-in-function-parameters>
- _Python Function Definition: Restricting a function to only receive a keyname + value after Bare Asterisk (`*`)_ - <https://stackoverflow.com/questions/2965271/forced-naming-of-parameters-in-python/14298976#14298976>
- _Python IO: Going one back three with `Pathlib`_ - <https://stackoverflow.com/questions/67251538/python-how-to-go-one-folder-back-in-pathlib>
- _Python IO: Checking if a directory exists_ - <https://stackoverflow.com/questions/8933237/how-do-i-check-if-directory-exists-in-python>
- _Python Limits: Identifying the maximum and minimum value of an `Integer`_ - <https://stackoverflow.com/questions/7604966/maximum-and-minimum-values-for-ints>
- _Python MyPy: Untyped decorator makes function untyped (I was unable to resolve this due to the complexity argument of my own decorator, which also takes an argument)_ - <https://stackoverflow.com/questions/65621789/mypy-untyped-decorator-makes-function-my-method-untyped>
- _Python Object: Checking the possibility wherein a singe object is called throughout the whole file (**This search was made possible due to the issue of circular dependencies**)_ - <https://stackoverflow.com/questions/63189935/is-it-possible-to-use-the-same-object-in-multiple-files>
- _Python Object: Determining an object's size_ - <https://stackoverflow.com/questions/449560/how-do-i-determine-the-size-of-an-object-in-python>
- _Python Object Manipulation: Changing a dictionary whilst another changes were done, the workaround_ - <https://stackoverflow.com/questions/11941817/how-can-i-avoid-runtimeerror-dictionary-changed-size-during-iteration-error>
- _Python Object Manipulation: Combining two dictionaries in shorthand_ - <https://stackoverflow.com/questions/38987/how-do-i-merge-two-dictionaries-in-a-single-expression>
- _Python Object: Static methods and how do I call them (**This is just a revisit from actually using `@staticmethod()`)_ - <https://stackoverflow.com/questions/1859959/static-methods-how-to-call-a-method-from-another-method>
- _Python `sockets`: Identifying a port number's state whether it's in-use or not_ - <https://stackoverflow.com/questions/2470971/fast-way-to-test-if-a-port-is-in-use-using-python>
- _Python SQLAlchemy: Concepts behind `backred` and `back_populate`_ - <https://stackoverflow.com/questions/51335298/concepts-of-backref-and-back-populate-in-sqlalchemy>
- _Python SQLAlchemy: Counting a `SELECT *` (**This search was made possible due to the difficulty of finding appropriate API for interacting with the Database**)_ - <https://stackoverflow.com/questions/12941416/how-to-count-rows-with-select-count-with-sqlalchemy>
- _Python SQLAlchemy: `default` parameter doesn't work after sending a payload in the database_ - <https://stackoverflow.com/questions/20348801/why-isnt-sqlalchemys-default-column-value-working>
- _Python SQLAlchemy: `default` parameter for the `datetime` field_ - <https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime>
- _Python SQLAlchemy: `Encrypt a column without automatically decrypting upon retrieval`, (used as a concept but scraped later on and turned in an idea instead)_ - <https://stackoverflow.com/questions/49560609/sqlalchemy-encrypt-a-column-without-automatically-decrypting-upon-retrieval>
- _Python SQLAlchemy: Understanding the use of `back_populate`_ - <https://stackoverflow.com/questions/39869793/when-do-i-need-to-use-sqlalchemy-back-populates>
- _Python STMP: Sending an email with Gmail as provider_ - <https://stackoverflow.com/questions/10147455/how-to-send-an-email-with-gmail-as-provider-using-python>
- _Python STMP: Understanding the SSL version error (**This occured during my prototyping session with the email**)_ - <https://stackoverflow.com/questions/57715289/how-to-fix-ssl-sslerror-ssl-wrong-version-number-wrong-version-number-ssl>
- _Python Stacktrace: Silencing the stacktrace (**This search was made possible due to some coroutines failed to close the connection or do `close`() after attempting to do `CTRL + C` during debugging days**)_ - <https://stackoverflow.com/questions/17784849/print-an-error-message-without-printing-a-traceback-and-close-the-program-when-a>
- _Python `string`: Check if multiple strings exists from the another_ - <https://stackoverflow.com/questions/3389574/check-if-multiple-strings-exist-in-another-string>
- _Python Terminal Call Libraries: Understanding the differences between `subprocess.Popen` and `os.system`_ - <https://stackoverflow.com/questions/4813238/difference-between-subprocess-popen-and-os-system>
- _Python Typing: Cannot import `NoneType`_ - <https://stackoverflow.com/questions/15844714/why-am-i-getting-an-error-message-in-python-cannot-import-name-nonetype>
- _Python Typing: TypeError: unhashable type: 'dict' (Implementation complexity leads me to this error)_ - <https://stackoverflow.com/questions/13264511/typeerror-unhashable-type-dict>
- _Python Type Annotation: Annotating a `class` instead of the `instance`_ - <https://stackoverflow.com/questions/41417679/how-to-annotate-a-type-thats-a-class-object-instead-of-a-class-instance>
- _Python Type Object Conversion (bytes to dict, used to serialize and restore blockchain system)_ - <https://stackoverflow.com/questions/19232011/convert-dictionary-to-bytes-and-back-again-python>
- _Vim: How to get vim to open multiple files into tabs at once (I'm using Visual Studio Code + Vim Extension)_ - <https://superuser.com/questions/171763/how-to-get-vim-to-open-multiple-files-into-tabs-at-once>
- _VSCode: How to allow `.jsonc`?_ - <https://stackoverflow.com/questions/47834825/in-vs-code-disable-error-comments-are-not-permitted-in-json>
- _VSCode: Keybinds for 'Hovering Info' on Cursor (I have to know since my diagnostics tab contains enormous amount of diagnostics)_ - <https://stackoverflow.com/questions/49146283/how-to-show-errors-warnings-by-hotkey-in-vscode/49147540>
- _VSCode: Keybind for searching a file through the 'File Explorer'_ - <https://stackoverflow.com/questions/30095376/how-do-i-search-for-files-in-visual-studio-code>
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
