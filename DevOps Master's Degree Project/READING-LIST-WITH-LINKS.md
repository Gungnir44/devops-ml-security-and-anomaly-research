# Reading List with Links
# ML-Based Security Anomaly Detection for DevOps

**Version:** 1.0
**Last Updated:** December 2025
**Target:** 100+ papers for comprehensive literature review

---

## Priority Reading Order

### 🔴 **Essential (Read First - Week 1-2)**
Must-read foundational papers and reports

### 🟡 **High Priority (Weeks 3-4)**
Important for methodology and background

### 🟢 **Medium Priority (Weeks 5-8)**
Supporting papers and additional context

---

## 1. DevOps Security & CI/CD Security

### 🔴 OWASP Top 10 CI/CD Security Risks (2022)
**Link:** https://owasp.org/www-project-top-10-ci-cd-security-risks/
**Type:** Industry Report
**Why Read:** Foundation for attack scenario design. Defines top CI/CD threats.

### 🔴 CNCF Cloud Native Security Whitepaper
**Link:** https://www.cncf.io/wp-content/uploads/2022/06/CNCF_cloud-native-security-whitepaper-May2022-v2.pdf
**Type:** Industry Report
**Why Read:** Kubernetes and container security best practices.

### 🟡 "Security in DevOps: A Systematic Literature Review"
**Authors:** Schaefer et al.
**Year:** 2019
**Link:** https://ieeexplore.ieee.org/document/8823898
**DOI:** 10.1109/ICSME.2019.00085
**Why Read:** Comprehensive DevSecOps overview and practices.

### 🟡 "Continuous Security in DevOps: A Systematic Literature Review"
**Authors:** Rajapakse et al.
**Year:** 2022
**Link:** https://arxiv.org/abs/2203.11789
**ArXiv:** https://arxiv.org/pdf/2203.11789.pdf
**Why Read:** Recent survey of DevSecOps research.

### 🟢 "Towards Continuous Security Certification of Software-as-a-Service"
**Link:** Search on IEEE Xplore or Google Scholar
**Why Read:** Cloud and SaaS security in CI/CD.

### 🟢 CIS Benchmarks for Kubernetes
**Link:** https://www.cisecurity.org/benchmark/kubernetes
**Type:** Industry Standard
**Why Read:** Security configuration standards.

---

## 2. Supply Chain Security & Real-World Attacks

### 🔴 SolarWinds Attack - Comprehensive Analysis
**Multiple Sources:**

1. **Microsoft Security Blog - SolarWinds Analysis**
   - https://www.microsoft.com/en-us/security/blog/2020/12/18/analyzing-solorigate-the-compromised-dll-file-that-started-a-sophisticated-cyberattack-and-how-microsoft-defender-helps-protect/

2. **FireEye - SUNBURST Analysis**
   - https://www.fireeye.com/blog/threat-research/2020/12/evasive-attacker-leverages-solarwinds-supply-chain-compromises-with-sunburst-backdoor.html

3. **CrowdStrike - SUNSPOT Analysis**
   - https://www.crowdstrike.com/blog/sunspot-malware-technical-analysis/

4. **CISA Advisory**
   - https://www.cisa.gov/news-events/cybersecurity-advisories/aa20-352a

**Why Read:** Most significant supply chain attack. Essential case study.

### 🔴 Codecov Bash Uploader Compromise
**Links:**
1. **Codecov Security Update**
   - https://about.codecov.io/security-update/

2. **Detailed Analysis**
   - https://blog.gitguardian.com/codecov-supply-chain-breach/

**Why Read:** CI/CD tool compromise, credential exfiltration example.

### 🔴 "Dependency Confusion: How I Hacked Into Apple, Microsoft and Dozens of Others"
**Author:** Alex Birsan
**Year:** 2021
**Link:** https://medium.com/@alex.birsan/dependency-confusion-4a5d60fec610
**Why Read:** Supply chain attack technique, $130k in bounties.

### 🟡 npm event-stream Attack Analysis
**Links:**
1. **GitHub Issue**
   - https://github.com/dominictarr/event-stream/issues/116

2. **Snyk Analysis**
   - https://snyk.io/blog/malicious-code-found-in-npm-package-event-stream/

3. **Medium Deep Dive**
   - https://medium.com/intrinsic-blog/compromised-npm-package-event-stream-d47d08605502

**Why Read:** npm supply chain attack, social engineering.

### 🟡 "Towards Measuring Supply Chain Attacks on Package Managers"
**Authors:** Ohm et al.
**Year:** 2020
**Link:** https://arxiv.org/abs/2002.01139
**ArXiv PDF:** https://arxiv.org/pdf/2002.01139.pdf
**Why Read:** Quantitative analysis of package manager attacks.

### 🟡 "Small World with High Risks: A Study of Security Threats in the npm Ecosystem"
**Authors:** Zimmermann et al.
**Year:** 2019
**Link:** https://www.usenix.org/conference/usenixsecurity19/presentation/zimmerman
**PDF:** https://www.usenix.org/system/files/sec19-zimmerman.pdf
**Why Read:** npm ecosystem security analysis.

### 🟢 ua-parser-js Attack (2021)
**Link:** https://github.com/advisories/GHSA-pjwm-rvh2-c87w
**Why Read:** Another npm supply chain incident.

### 🟢 Log4Shell Supply Chain Implications
**Link:** https://www.cisa.gov/news-events/cybersecurity-advisories/aa21-356a
**Why Read:** Dependency vulnerability cascade.

---

## 3. Machine Learning for Security

### 🔴 "Outside the Closed World: On Using Machine Learning for Network Intrusion Detection"
**Authors:** Robin Sommer, Vern Paxson
**Year:** 2010
**Venue:** IEEE Security & Privacy
**Link:** https://ieeexplore.ieee.org/document/5504793
**PDF:** http://www.icir.org/robin/papers/oakland10-ml.pdf
**Why Read:** **ESSENTIAL.** Critical analysis of ML for security challenges.

### 🔴 "Anomaly Detection: A Survey"
**Authors:** Chandola, Banerjee, Kumar
**Year:** 2009
**Venue:** ACM Computing Surveys
**Link:** https://dl.acm.org/doi/10.1145/1541880.1541882
**PDF:** https://www.vs.inf.ethz.ch/edu/HS2011/CPS/papers/chandola09_anomaly-detection-survey.pdf
**Why Read:** **ESSENTIAL.** Foundational anomaly detection survey.

### 🟡 "Deep Learning for Cybersecurity Intrusion Detection: Approaches, Datasets, and Comparative Study"
**Authors:** Apruzzese et al.
**Year:** 2022
**Link:** https://www.sciencedirect.com/science/article/pii/S016740482200083X
**Why Read:** Deep learning approaches for intrusion detection.

### 🟡 "A Survey of Data Mining and Machine Learning Methods for Cyber Security Intrusion Detection"
**Authors:** Buczak, Guven
**Year:** 2016
**Link:** https://ieeexplore.ieee.org/document/7307098
**PDF:** Available via IEEE Xplore
**Why Read:** Comprehensive ML methods for security.

### 🟡 "Machine Learning for Network Intrusion Detection - A Comparative Study"
**Link:** Search on Google Scholar
**Why Read:** Model comparison methodologies.

### 🟢 "Explaining Machine Learning Classifiers through Diverse Counterfactual Explanations"
**Year:** 2020
**Link:** https://arxiv.org/abs/1905.07857
**ArXiv PDF:** https://arxiv.org/pdf/1905.07857.pdf
**Why Read:** Model explainability (important for security).

### 🟢 "Adversarial Machine Learning at Scale"
**Authors:** Kurakin et al.
**Year:** 2017
**Link:** https://arxiv.org/abs/1611.01236
**Why Read:** Adversarial attacks on ML models.

---

## 4. Anomaly Detection Algorithms

### 🔴 "Isolation Forest" (Original Paper)
**Authors:** Fei Tony Liu, Kai Ming Ting, Zhi-Hua Zhou
**Year:** 2008
**Venue:** ICDM
**Link:** https://ieeexplore.ieee.org/document/4781136
**PDF:** https://cs.nju.edu.cn/zhouzh/zhouzh.files/publication/icdm08b.pdf
**Why Read:** **ESSENTIAL.** Your primary unsupervised model.

### 🟡 "LOF: Identifying Density-Based Local Outliers"
**Authors:** Breunig et al.
**Year:** 2000
**Venue:** SIGMOD
**Link:** https://dl.acm.org/doi/10.1145/342009.335388
**PDF:** http://www.dbs.ifi.lmu.de/Publikationen/Papers/LOF.pdf
**Why Read:** Classic density-based anomaly detection.

### 🟡 "One-Class SVMs for Document Classification"
**Authors:** Manevitz, Yousef
**Year:** 2002
**Link:** https://www.jmlr.org/papers/volume2/manevitz01a/manevitz01a.pdf
**Why Read:** One-class SVM for anomaly detection.

### 🟡 "Estimating the Support of a High-Dimensional Distribution" (One-Class SVM)
**Authors:** Schölkopf et al.
**Year:** 2001
**Link:** http://www.gatsby.ucl.ac.uk/~gretton/coursefiles/Scholkopf01a.pdf
**Why Read:** Original one-class SVM paper.

### 🟢 "DBSCAN: A Density-Based Algorithm for Discovering Clusters"
**Authors:** Ester et al.
**Year:** 1996
**Link:** https://www.aaai.org/Papers/KDD/1996/KDD96-037.pdf
**Why Read:** Clustering-based outlier detection.

---

## 5. Time-Series Analysis & Sequential Models

### 🔴 "Long Short-Term Memory" (LSTM Original Paper)
**Authors:** Hochreiter, Schmidhuber
**Year:** 1997
**Link:** https://www.bioinf.jku.at/publications/older/2604.pdf
**DOI:** https://doi.org/10.1162/neco.1997.9.8.1735
**Why Read:** **ESSENTIAL.** Foundation for LSTM model.

### 🟡 "LSTM-based Encoder-Decoder for Multi-sensor Anomaly Detection"
**Authors:** Malhotra et al.
**Year:** 2016
**Venue:** ICML Workshop
**Link:** https://arxiv.org/abs/1607.00148
**ArXiv PDF:** https://arxiv.org/pdf/1607.00148.pdf
**Why Read:** LSTM for anomaly detection in time-series.

### 🟡 "Detecting Spacecraft Anomalies Using LSTMs and Nonparametric Dynamic Thresholding"
**Authors:** Hundman et al.
**Year:** 2018
**Venue:** KDD
**Link:** https://arxiv.org/abs/1802.04431
**ArXiv PDF:** https://arxiv.org/pdf/1802.04431.pdf
**Why Read:** Real-world LSTM anomaly detection application.

### 🟢 "Time Series Anomaly Detection: Detection of Anomalous Drops with Limited Features"
**Link:** https://arxiv.org/abs/2011.14950
**Why Read:** Practical time-series anomaly detection.

### 🟢 "DeepLog: Anomaly Detection and Diagnosis from System Logs through Deep Learning"
**Authors:** Du et al.
**Year:** 2017
**Link:** https://www.cs.utah.edu/~lifeifei/papers/deeplog.pdf
**Why Read:** Log-based anomaly detection using LSTMs.

---

## 6. Autoencoders for Anomaly Detection

### 🟡 "Variational Autoencoder based Anomaly Detection using Reconstruction Probability"
**Authors:** An, Cho
**Year:** 2015
**Link:** http://dm.snu.ac.kr/static/docs/TR/SNUDM-TR-2015-03.pdf
**Why Read:** VAE for anomaly detection.

### 🟡 "Anomaly Detection with Robust Deep Autoencoders"
**Authors:** Zhou, Paffenroth
**Year:** 2017
**Link:** https://dl.acm.org/doi/10.1145/3097983.3098052
**Why Read:** Robust autoencoders for outlier detection.

### 🟢 "Deep Autoencoding Gaussian Mixture Model for Unsupervised Anomaly Detection"
**Year:** 2018
**Link:** https://openreview.net/forum?id=BJJLHbb0-
**Why Read:** Advanced autoencoder architectures.

---

## 7. Ensemble Methods & Model Comparison

### 🔴 "Random Forests"
**Author:** Leo Breiman
**Year:** 2001
**Venue:** Machine Learning Journal
**Link:** https://link.springer.com/article/10.1023/A:1010933404324
**PDF:** https://www.stat.berkeley.edu/~breiman/randomforest2001.pdf
**Why Read:** **ESSENTIAL.** Foundation for Random Forest model.

### 🔴 "XGBoost: A Scalable Tree Boosting System"
**Authors:** Chen, Guestrin
**Year:** 2016
**Venue:** KDD
**Link:** https://dl.acm.org/doi/10.1145/2939672.2939785
**PDF:** https://arxiv.org/pdf/1603.02754.pdf
**Why Read:** **ESSENTIAL.** Foundation for XGBoost model.

### 🟡 "Ensemble Methods: Foundations and Algorithms"
**Author:** Zhou
**Year:** 2012
**Link:** https://www.taylorfrancis.com/books/mono/10.1201/b12207/ensemble-methods-zhi-hua-zhou
**Why Read:** Theoretical foundation for ensemble learning.

### 🟢 "A Survey on Ensemble Learning"
**Authors:** Sagi, Rokach
**Year:** 2018
**Link:** https://dl.acm.org/doi/10.1145/3146371
**Why Read:** Overview of ensemble techniques.

---

## 8. Feature Engineering & Behavioral Analysis

### 🟡 "Feature Engineering for Machine Learning: Principles and Techniques for Data Scientists"
**Authors:** Zheng, Casari
**Year:** 2018
**Link:** O'Reilly book - https://www.oreilly.com/library/view/feature-engineering-for/9781491953235/
**Why Read:** Practical feature engineering techniques.

### 🟡 "User and Entity Behavior Analytics (UEBA) - A Survey"
**Link:** Search on Google Scholar for recent surveys
**Why Read:** Behavioral analytics for security.

### 🟡 "Insider Threat Detection Using Behavioral Analytics"
**Authors:** Various
**Link:** Search IEEE Xplore for recent papers
**Why Read:** Behavioral features for threat detection.

### 🟢 "Detecting Compromised Accounts on Social Networks"
**Authors:** Egele et al.
**Year:** 2013
**Link:** https://www.usenix.org/conference/usenixsecurity13/technical-sessions/paper/egele
**PDF:** https://www.usenix.org/system/files/conference/usenixsecurity13/sec13-paper_egele.pdf
**Why Read:** Account compromise detection via behavior.

---

## 9. Industry Reports & Standards

### 🔴 Verizon Data Breach Investigations Report (DBIR) 2024
**Link:** https://www.verizon.com/business/resources/reports/dbir/
**Type:** Annual Industry Report
**Why Read:** Real-world attack statistics and trends.

### 🟡 MITRE ATT&CK Framework
**Link:** https://attack.mitre.org/
**Specific:** https://attack.mitre.org/matrices/enterprise/
**Why Read:** Attack taxonomy for labeling your attacks.

### 🟡 NIST Cybersecurity Framework
**Link:** https://www.nist.gov/cyberframework
**Why Read:** Security best practices and standards.

### 🟡 "The State of Software Supply Chain Security" - Sonatype
**Link:** https://www.sonatype.com/state-of-the-software-supply-chain
**Type:** Annual Report
**Why Read:** Supply chain attack trends.

### 🟢 IBM Security X-Force Threat Intelligence Index
**Link:** https://www.ibm.com/security/data-breach/threat-intelligence
**Why Read:** Additional attack statistics.

### 🟢 SANS Top 25 Most Dangerous Software Weaknesses
**Link:** https://www.sans.org/top25-software-errors/
**Why Read:** Common vulnerability patterns.

---

## 10. Commercial Tools (For Comparison)

### 🟡 GitHub Advanced Security Documentation
**Link:** https://docs.github.com/en/get-started/learning-about-github/about-github-advanced-security
**Features:** https://github.com/features/security
**Why Review:** Primary commercial baseline.

### 🟡 GitLab Security Features
**Link:** https://docs.gitlab.com/ee/user/application_security/
**Features:** https://about.gitlab.com/stages-devops-lifecycle/secure/
**Why Review:** Another major CI/CD security platform.

### 🟢 Snyk Documentation
**Link:** https://docs.snyk.io/
**Why Review:** Dependency scanning comparison.

### 🟢 Aqua Security Documentation
**Link:** https://docs.aquasec.com/
**Why Review:** Container security comparison.

### 🟢 Checkmarx (SAST)
**Link:** https://checkmarx.com/
**Why Review:** SAST tool comparison.

---

## 11. Additional Foundational ML Papers

### 🟡 "Deep Learning" (Goodfellow et al.)
**Authors:** Goodfellow, Bengio, Courville
**Year:** 2016
**Link:** https://www.deeplearningbook.org/
**Free Online:** https://www.deeplearningbook.org/
**Why Read:** Deep learning foundations.

### 🟡 "Support Vector Networks"
**Authors:** Cortes, Vapnik
**Year:** 1995
**Link:** https://link.springer.com/article/10.1007/BF00994018
**Why Read:** SVM foundations.

### 🟢 "Batch Normalization: Accelerating Deep Network Training"
**Authors:** Ioffe, Szegedy
**Year:** 2015
**Link:** https://arxiv.org/abs/1502.03167
**Why Read:** Neural network training techniques.

### 🟢 "Adam: A Method for Stochastic Optimization"
**Authors:** Kingma, Ba
**Year:** 2014
**Link:** https://arxiv.org/abs/1412.6980
**Why Read:** Optimizer for neural networks.

---

## 12. Model Evaluation & Validation

### 🟡 "A Systematic Analysis of Performance Measures for Classification Tasks"
**Authors:** Sokolova, Lapalme
**Year:** 2009
**Link:** https://www.sciencedirect.com/science/article/pii/S0020025509001303
**Why Read:** Comprehensive guide to evaluation metrics.

### 🟡 "The Relationship Between Precision-Recall and ROC Curves"
**Authors:** Davis, Goadrich
**Year:** 2006
**Link:** https://dl.acm.org/doi/10.1145/1143844.1143874
**PDF:** https://www.biostat.wisc.edu/~page/rocpr.pdf
**Why Read:** Understanding evaluation metrics.

### 🟢 "SMOTE: Synthetic Minority Over-sampling Technique"
**Authors:** Chawla et al.
**Year:** 2002
**Link:** https://arxiv.org/abs/1106.1813
**Why Read:** Handling class imbalance.

---

## 13. Recent Papers (2023-2025)

### Search Strategy for Recent Papers:

**Google Scholar Alerts - Set up for:**
- "DevOps security" + "machine learning"
- "CI/CD security" + "anomaly detection"
- "supply chain attack" + "detection"
- "behavioral analytics" + "security"

**Conference Proceedings to Check:**
- **IEEE Security & Privacy (Oakland) 2024:** https://www.ieee-security.org/TC/SP2024/
- **USENIX Security 2024:** https://www.usenix.org/conference/usenixsecurity24
- **ACM CCS 2024:** https://www.sigsac.org/ccs/CCS2024/
- **NDSS 2024:** https://www.ndss-symposium.org/ndss2024/

**ArXiv Searches:**
- https://arxiv.org/search/?query=devops+security&searchtype=all
- https://arxiv.org/search/?query=CI/CD+security&searchtype=all
- https://arxiv.org/search/?query=supply+chain+attack+detection&searchtype=all

---

## Quick Access Links

### Academic Search Engines
- **Google Scholar:** https://scholar.google.com/
- **Semantic Scholar:** https://www.semanticscholar.org/
- **arXiv:** https://arxiv.org/
- **DBLP:** https://dblp.org/

### Digital Libraries
- **IEEE Xplore:** https://ieeexplore.ieee.org/ (via university access)
- **ACM Digital Library:** https://dl.acm.org/ (via university access)
- **SpringerLink:** https://link.springer.com/ (via university access)
- **ScienceDirect:** https://www.sciencedirect.com/ (via university access)

### Preprint Servers
- **arXiv CS Security:** https://arxiv.org/list/cs.CR/recent
- **IACR ePrint Archive:** https://eprint.iacr.org/

### Research Tools
- **Connected Papers:** https://www.connectedpapers.com/ (find related papers)
- **Research Rabbit:** https://www.researchrabbit.ai/ (paper discovery)
- **Paper Digest:** https://www.paper-digest.com/ (paper summaries)

---

## Reading Schedule (Weeks 1-8)

### Week 1 (5 papers - Foundational)
- [ ] OWASP Top 10 CI/CD Security Risks
- [ ] SolarWinds Attack Analysis (Microsoft + FireEye reports)
- [ ] Codecov Compromise Analysis
- [ ] Dependency Confusion (Alex Birsan)
- [ ] MITRE ATT&CK Framework (browse)

### Week 2 (5 papers - ML Foundations)
- [ ] Outside the Closed World (Sommer & Paxson) **CRITICAL**
- [ ] Anomaly Detection: A Survey (Chandola et al.) **CRITICAL**
- [ ] Isolation Forest (Liu et al.) **CRITICAL**
- [ ] Random Forests (Breiman)
- [ ] XGBoost (Chen & Guestrin)

### Week 3 (6 papers - DevOps Security)
- [ ] Security in DevOps: Systematic Literature Review
- [ ] Continuous Security in DevOps (Rajapakse et al.)
- [ ] CNCF Cloud Native Security Whitepaper
- [ ] npm event-stream attack analysis
- [ ] Small World with High Risks (npm ecosystem study)
- [ ] Towards Measuring Supply Chain Attacks

### Week 4 (6 papers - ML for Security)
- [ ] Deep Learning for Cybersecurity Intrusion Detection
- [ ] Survey of Data Mining and ML for Intrusion Detection
- [ ] LOF: Local Outlier Factor
- [ ] One-Class SVM papers (2 papers)
- [ ] Adversarial Machine Learning at Scale

### Week 5 (6 papers - Time-Series & Deep Learning)
- [ ] LSTM Original Paper (Hochreiter & Schmidhuber)
- [ ] LSTM-based Encoder-Decoder for Anomaly Detection
- [ ] Detecting Spacecraft Anomalies Using LSTMs
- [ ] DeepLog: Anomaly Detection from System Logs
- [ ] Variational Autoencoder for Anomaly Detection
- [ ] Anomaly Detection with Robust Deep Autoencoders

### Week 6 (5 papers - Behavioral & Feature Engineering)
- [ ] Detecting Compromised Accounts (Egele et al.)
- [ ] Feature Engineering for ML (book chapters)
- [ ] Insider Threat Detection papers (2 papers)
- [ ] UEBA survey
- [ ] User behavioral analytics papers

### Week 7 (4 papers - Evaluation & Methods)
- [ ] Performance Measures for Classification Tasks
- [ ] Precision-Recall and ROC Curves
- [ ] SMOTE: Handling Class Imbalance
- [ ] Ensemble Methods survey

### Week 8 (3 papers + Industry Reports)
- [ ] Verizon DBIR 2024
- [ ] State of Software Supply Chain Security (Sonatype)
- [ ] Recent 2024 papers from conferences
- [ ] Review all notes and identify gaps

**Total for Weeks 1-8: 40+ papers**

---

## Tips for Efficient Reading

### For Academic Papers:
1. **Read Abstract First** - Decide if relevant
2. **Skim Introduction & Conclusion** - Get main ideas
3. **Look at Figures & Tables** - Visual summary
4. **Read Methodology** (if using similar approach)
5. **Read Results** (for comparison)
6. **Deep Read** only if highly relevant

### Tools to Help:
- **Sci-Hub** (for papers behind paywalls - use ethically)
- **Unpaywall Browser Extension** - Finds free legal versions
- **Zotero Connector** - Save papers directly from browser
- **PDF annotation tools** - Hypothesis, Mendeley, Zotero

### Note-Taking:
- Use the template from LITERATURE-REVIEW-TRACKER.md
- Take notes immediately after reading
- Tag papers by relevance (🔴 🟡 🟢)
- Note which section of thesis each paper supports

---

## Priority Matrix

| Priority | Papers | Timeline | Purpose |
|----------|--------|----------|---------|
| 🔴 Essential | 15 | Weeks 1-2 | Foundation, must cite |
| 🟡 High Priority | 30 | Weeks 3-6 | Methodology, background |
| 🟢 Medium Priority | 40 | Weeks 7-12 | Supporting, comparison |
| Additional | 15+ | Ongoing | Fill gaps, recent work |
| **TOTAL** | **100+** | **3 months** | **Comprehensive review** |

---

**Good luck with your reading! Start with the 🔴 Essential papers and work your way through systematically.**

**Remember:** Quality over quantity. Understanding 50 papers deeply is better than skimming 100.
