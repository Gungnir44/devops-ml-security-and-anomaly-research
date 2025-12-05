# Literature Review Tracker
# ML-Based Security Anomaly Detection for DevOps

**Version:** 1.0
**Last Updated:** December 2025

---

## Overview

This document helps track relevant papers, articles, and resources for the literature review. Organize by topic and maintain notes on key findings and relevance to your research.

**Target:** 100+ references for comprehensive thesis

---

## Literature Review Categories

1. [DevOps Security & CI/CD Security](#1-devops-security--cicd-security)
2. [Supply Chain Security](#2-supply-chain-security)
3. [Machine Learning for Security](#3-machine-learning-for-security)
4. [Anomaly Detection Algorithms](#4-anomaly-detection-algorithms)
5. [Time-Series Analysis](#5-time-series-analysis)
6. [Feature Engineering for Security](#6-feature-engineering-for-security)
7. [Real-World Attacks & Case Studies](#7-real-world-attacks--case-studies)
8. [Behavioral Analysis](#8-behavioral-analysis)
9. [Commercial Tools & Industry Reports](#9-commercial-tools--industry-reports)
10. [Foundational ML Papers](#10-foundational-ml-papers)

---

## Paper Template

For each paper, track:

```markdown
### [Paper Title]

**Authors:** [Author names]
**Year:** [Year]
**Venue:** [Conference/Journal]
**Link:** [URL or DOI]
**Citation:** [BibTeX or formatted citation]

**Summary:**
[2-3 sentence summary of the paper]

**Key Findings:**
- [Finding 1]
- [Finding 2]
- [Finding 3]

**Relevance to Your Research:**
[How this relates to your work - methodology, results, comparison point, etc.]

**Quotes to Use:**
- "[Important quote]" (p. X)

**Limitations:**
[Any limitations or criticisms]

**Status:** ☐ To Read | ☐ Reading | ☑ Read | ☐ Cited in Thesis
```

---

## 1. DevOps Security & CI/CD Security

### OWASP Top 10 CI/CD Security Risks

**Authors:** OWASP Foundation
**Year:** 2022
**Venue:** Industry Report
**Link:** https://owasp.org/www-project-top-10-ci-cd-security-risks/
**Citation:** OWASP Foundation, "OWASP Top 10 CI/CD Security Risks," 2022.

**Summary:**
Comprehensive list of the most critical security risks in CI/CD environments, including insufficient flow control mechanisms, inadequate identity and access management, dependency chain abuse, and more.

**Key Findings:**
- Top 10 security risks ranked by prevalence and impact
- Detailed attack scenarios for each risk
- Mitigation strategies for each risk category

**Relevance to Your Research:**
Direct foundation for attack scenario design. Maps attack types to real-world CI/CD threats.

**Status:** ☐ To Read | ☐ Reading | ☑ Read | ☐ Cited in Thesis

---

### [Add More Papers Here]

**Suggested Papers:**
- "Towards Continuous Security Certification of Software-as-a-Service" (Cloud security)
- "Security in DevOps: A Systematic Literature Review" (DevSecOps overview)
- "A Survey on DevSecOps Methodologies" (Practices and tools)
- CI/CD security papers from IEEE Security & Privacy, USENIX Security

---

## 2. Supply Chain Security

### SolarWinds Attack Analysis

**Authors:** Multiple sources (CrowdStrike, FireEye, etc.)
**Year:** 2020-2021
**Venue:** Industry Reports & Technical Analysis
**Link:** [Collection of reports]

**Summary:**
Analysis of the SolarWinds supply chain attack where attackers compromised the build system to inject malicious code into software updates, affecting thousands of organizations.

**Key Findings:**
- Build system compromise technique
- Long-term persistence (months)
- Detection challenges
- Impact scope (18,000+ organizations)

**Relevance to Your Research:**
Real-world example of CI/CD pipeline compromise. Informs attack scenario 2.1 (Pipeline backdoor).

**Status:** ☐ To Read | ☐ Reading | ☑ Read | ☐ Cited in Thesis

---

### Codecov Bash Uploader Compromise

**Authors:** Codecov, Security Researchers
**Year:** 2021
**Venue:** Incident Reports
**Link:** https://about.codecov.io/security-update/

**Summary:**
Attackers modified Codecov's bash uploader script to exfiltrate environment variables, potentially exposing credentials from CI/CD pipelines.

**Key Findings:**
- Script modification in CI/CD tooling
- Environment variable exfiltration
- Detection delay (months)
- Widespread impact

**Relevance to Your Research:**
Example of supply chain attack via CI/CD tooling. Informs credential theft scenarios.

**Status:** ☐ To Read | ☐ Reading | ☑ Read | ☐ Cited in Thesis

---

### Dependency Confusion Attacks

**Authors:** Alex Birsan
**Year:** 2021
**Venue:** Medium Article / Security Research
**Link:** https://medium.com/@alex.birsan/dependency-confusion-4a5d60fec610

**Summary:**
Researcher demonstrated how to exploit package manager behavior to inject malicious packages by creating public packages with names matching private internal packages.

**Key Findings:**
- $130,000+ in bug bounties from major companies
- Affected npm, pip, RubyGems, etc.
- Simple attack, high impact
- Defensive measures needed

**Relevance to Your Research:**
Direct example for attack scenario 3.1 (Malicious dependency injection). Informs dependency scanning features.

**Status:** ☐ To Read | ☐ Reading | ☑ Read | ☐ Cited in Thesis

---

**Suggested Papers:**
- "Towards Measuring Supply Chain Attacks on Package Managers for Interpreted Languages"
- "Small World with High Risks: A Study of Security Threats in the npm Ecosystem"
- "A Large-Scale Analysis of the Security of Embedded Software"

---

## 3. Machine Learning for Security

### "Outside the Closed World: On Using Machine Learning for Network Intrusion Detection"

**Authors:** Robin Sommer, Vern Paxson
**Year:** 2010
**Venue:** IEEE Symposium on Security and Privacy
**Link:** [DOI]
**Citation:** R. Sommer and V. Paxson, "Outside the closed world: On using machine learning for network intrusion detection," 2010 IEEE Symposium on Security and Privacy, 2010.

**Summary:**
Critical analysis of machine learning for intrusion detection, highlighting challenges such as training data quality, class imbalance, concept drift, and high cost of errors (false positives).

**Key Findings:**
- ML works well in closed-world (lab) settings but struggles in real-world deployment
- Semantic gap between features and attacks
- High false positive rates are unacceptable in practice
- Need for continuous retraining due to concept drift

**Relevance to Your Research:**
Foundational paper on ML for security. Highlights challenges you must address: false positives, concept drift, realistic evaluation.

**Quotes to Use:**
- "The gap between the features available to a learning system and the information needed to accurately detect attacks is often too large to bridge." (p. 306)

**Status:** ☐ To Read | ☐ Reading | ☑ Read | ☐ Cited in Thesis

---

### "Deep Learning for Cybersecurity Intrusion Detection: Approaches, Datasets, and Comparative Study"

**Authors:** [Authors]
**Year:** 2020
**Venue:** Journal of Information Security and Applications
**Link:** [DOI]

**Summary:**
Comprehensive survey of deep learning approaches for intrusion detection, comparing CNNs, RNNs, LSTMs, and autoencoders on standard datasets.

**Key Findings:**
- [To be filled when read]

**Relevance to Your Research:**
Provides comparison of DL architectures for security. Informs your choice of models (LSTM, autoencoder).

**Status:** ☐ To Read | ☐ Reading | ☐ Read | ☐ Cited in Thesis

---

**Suggested Papers:**
- "Anomaly Detection: A Survey" (Chandola et al., 2009) - foundational anomaly detection
- "A Survey of Data Mining and Machine Learning Methods for Cyber Security Intrusion Detection"
- "Explaining Machine Learning Classifiers through Diverse Counterfactual Explanations" (explainability)

---

## 4. Anomaly Detection Algorithms

### "Isolation Forest"

**Authors:** Fei Tony Liu, Kai Ming Ting, Zhi-Hua Zhou
**Year:** 2008
**Venue:** ICDM 2008
**Link:** [DOI]
**Citation:** F. T. Liu, K. M. Ting, and Z.-H. Zhou, "Isolation forest," 2008 Eighth IEEE International Conference on Data Mining, 2008.

**Summary:**
Introduction of Isolation Forest algorithm, which isolates anomalies by randomly partitioning data. Anomalies are easier to isolate (fewer partitions needed).

**Key Findings:**
- Fast training and prediction
- Effective for high-dimensional data
- No need for distance or density calculations
- Works well with small contamination rates

**Relevance to Your Research:**
Primary unsupervised model in your research. Baseline for anomaly detection.

**Status:** ☐ To Read | ☐ Reading | ☑ Read | ☐ Cited in Thesis

---

### "LOF: Identifying Density-Based Local Outliers"

**Authors:** Markus M. Breunig, Hans-Peter Kriegel, et al.
**Year:** 2000
**Venue:** SIGMOD 2000
**Link:** [DOI]

**Summary:**
Local Outlier Factor (LOF) algorithm identifies anomalies based on local density deviation compared to neighbors.

**Key Findings:**
- [To be filled]

**Relevance to Your Research:**
Alternative unsupervised approach to compare with Isolation Forest.

**Status:** ☐ To Read | ☐ Reading | ☐ Read | ☐ Cited in Thesis

---

**Suggested Papers:**
- "One-Class SVM" papers
- "Autoencoders for anomaly detection" papers
- "DBSCAN and clustering-based anomaly detection"

---

## 5. Time-Series Analysis

### "LSTM-based Encoder-Decoder for Multi-sensor Anomaly Detection"

**Authors:** Pankaj Malhotra, et al.
**Year:** 2016
**Venue:** ICML Workshop
**Link:** [arXiv link]

**Summary:**
Uses LSTM encoder-decoder architecture to model normal time-series behavior and detect anomalies based on reconstruction error.

**Key Findings:**
- [To be filled]

**Relevance to Your Research:**
Informs LSTM model design for sequential event analysis.

**Status:** ☐ To Read | ☐ Reading | ☐ Read | ☐ Cited in Thesis

---

**Suggested Papers:**
- "Time Series Anomaly Detection" surveys
- "Temporal pattern mining" papers
- "Sequential pattern analysis for security"

---

## 6. Feature Engineering for Security

### "Feature Engineering for Security"

**Authors:** [Authors if specific paper, or general topic]
**Year:** Various
**Venue:** Various
**Link:** [Links]

**Summary:**
Collection of papers on effective feature engineering for security applications.

**Key Topics:**
- Behavioral features (user activity patterns)
- Temporal features (time-based anomalies)
- Statistical features (z-scores, distributions)
- Network features (traffic patterns)

**Relevance to Your Research:**
Direct guidance for your feature engineering (210 features).

**Status:** ☐ To Read | ☐ Reading | ☐ Read | ☐ Cited in Thesis

---

**Suggested Papers:**
- Domain-specific feature engineering papers
- "Feature selection for intrusion detection" papers
- "Behavioral analytics for security" papers

---

## 7. Real-World Attacks & Case Studies

### npm Event-Stream Attack

**Authors:** Security researchers
**Year:** 2018
**Venue:** Incident reports
**Link:** [Links to analysis]

**Summary:**
Attacker gained maintainer access to popular npm package (event-stream) and injected malicious code targeting cryptocurrency wallets.

**Key Findings:**
- Social engineering to gain maintainer access
- Delayed activation (targeting specific apps)
- Detected by community, not automated tools
- Supply chain trust issues

**Relevance to Your Research:**
Real-world supply chain attack example. Informs attack scenario 3.1.

**Status:** ☐ To Read | ☐ Reading | ☑ Read | ☐ Cited in Thesis

---

**Suggested Case Studies:**
- SolarWinds (already listed)
- Codecov (already listed)
- ua-parser-js attack
- Log4Shell (supply chain implications)
- GitHub Actions cryptomining
- CircleCI security incidents

---

## 8. Behavioral Analysis

### "User Behavior Analytics: Methods and Applications"

**Authors:** [Authors]
**Year:** [Year]
**Venue:** [Venue]
**Link:** [Link]

**Summary:**
[To be filled]

**Relevance to Your Research:**
Informs behavioral feature engineering and baseline modeling.

**Status:** ☐ To Read | ☐ Reading | ☐ Read | ☐ Cited in Thesis

---

**Suggested Papers:**
- "Insider threat detection using behavioral analytics"
- "User and Entity Behavior Analytics (UEBA)"
- "Detecting compromised accounts through behavior analysis"

---

## 9. Commercial Tools & Industry Reports

### Verizon Data Breach Investigations Report (DBIR)

**Authors:** Verizon
**Year:** 2024 (annual)
**Venue:** Industry Report
**Link:** https://www.verizon.com/business/resources/reports/dbir/

**Summary:**
Annual report analyzing thousands of security incidents and data breaches, providing statistics on attack vectors, threat actors, and trends.

**Key Findings:**
- [Statistics from latest report]
- Common attack patterns
- Time to detect metrics
- Industry-specific trends

**Relevance to Your Research:**
Provides real-world attack statistics to justify research importance.

**Status:** ☐ To Read | ☐ Reading | ☐ Read | ☐ Cited in Thesis

---

### GitHub Advanced Security

**Link:** https://github.com/features/security

**Summary:**
Commercial security platform for code, secrets, and dependency scanning.

**Key Features:**
- CodeQL for SAST
- Secret scanning
- Dependency scanning
- Security advisories

**Relevance to Your Research:**
Existing commercial solution for comparison. Shows gap (no behavioral anomaly detection).

**Status:** ☐ To Review | ☐ Reviewed | ☐ Cited in Thesis

---

### GitLab Security Features

**Link:** https://about.gitlab.com/stages-devops-lifecycle/secure/

**Relevance to Your Research:**
Another commercial baseline for comparison.

**Status:** ☐ To Review | ☐ Reviewed | ☐ Cited in Thesis

---

**Other Tools to Review:**
- Snyk (dependency scanning)
- Aqua Security (container security)
- Checkmarx (SAST)
- Veracode (application security)
- Prisma Cloud (cloud security)

---

## 10. Foundational ML Papers

### "Random Forests"

**Authors:** Leo Breiman
**Year:** 2001
**Venue:** Machine Learning Journal
**Link:** [DOI]

**Summary:**
Introduction of Random Forest algorithm, ensemble of decision trees with randomization.

**Key Findings:**
- Strong performance across domains
- Feature importance measurement
- Robust to overfitting
- Handles high-dimensional data well

**Relevance to Your Research:**
One of your primary supervised models. Foundational citation.

**Status:** ☐ To Read | ☐ Reading | ☑ Read | ☐ Cited in Thesis

---

### "XGBoost: A Scalable Tree Boosting System"

**Authors:** Tianqi Chen, Carlos Guestrin
**Year:** 2016
**Venue:** KDD 2016
**Link:** [DOI]

**Summary:**
Introduction of XGBoost, gradient boosting system optimized for speed and performance.

**Key Findings:**
- State-of-art performance on many benchmarks
- Efficient handling of sparse data
- Built-in regularization
- Parallel processing

**Relevance to Your Research:**
Another primary supervised model. Often outperforms other methods.

**Status:** ☐ To Read | ☐ Reading | ☐ Read | ☐ Cited in Thesis

---

**Other Foundational Papers:**
- "Support Vector Machines" (Vapnik)
- "Neural Networks and Deep Learning" (Goodfellow et al.)
- "LSTM" (Hochreiter & Schmidhuber)
- "Autoencoders" papers
- "Ensemble Methods" papers

---

## Citation Management

### Reference Manager Setup
- [ ] Choose reference manager (Zotero, Mendeley, EndNote)
- [ ] Create project library
- [ ] Set up citation style (IEEE, ACM, APA)
- [ ] Install Word/LaTeX plugin

### BibTeX Organization

Create `references.bib` file:

```bibtex
@inproceedings{sommer2010outside,
  title={Outside the closed world: On using machine learning for network intrusion detection},
  author={Sommer, Robin and Paxson, Vern},
  booktitle={2010 IEEE symposium on security and privacy},
  pages={305--316},
  year={2010},
  organization={IEEE}
}

@inproceedings{liu2008isolation,
  title={Isolation forest},
  author={Liu, Fei Tony and Ting, Kai Ming and Zhou, Zhi-Hua},
  booktitle={2008 eighth ieee international conference on data mining},
  pages={413--422},
  year={2008},
  organization={IEEE}
}

% Add more entries...
```

---

## Reading Schedule

### Month 1-2 (Weeks 1-8)
**Goal:** 20-30 papers
**Focus:** DevOps security, CI/CD security, real-world attacks

- [ ] OWASP Top 10 CI/CD Security Risks
- [ ] SolarWinds analysis reports
- [ ] Codecov incident reports
- [ ] Supply chain security papers (5-10)
- [ ] DevSecOps survey papers (2-3)

### Month 3-4 (Weeks 9-16)
**Goal:** 30-40 papers
**Focus:** Machine learning for security, anomaly detection

- [ ] Sommer & Paxson (ML for security challenges)
- [ ] Isolation Forest paper
- [ ] Autoencoder papers (3-5)
- [ ] LSTM papers (3-5)
- [ ] General anomaly detection surveys (2-3)
- [ ] ML for intrusion detection papers (10-15)

### Month 5-6 (Weeks 17-24)
**Goal:** 30-40 papers
**Focus:** Advanced ML, feature engineering, evaluation

- [ ] Feature engineering papers (5-10)
- [ ] Ensemble methods papers (3-5)
- [ ] Model evaluation papers (3-5)
- [ ] Behavioral analytics papers (5-10)
- [ ] Time-series analysis papers (5-10)

### Month 7-8 (Weeks 25-32)
**Goal:** 10-20 papers + review all
**Focus:** Recent papers, gap filling, specific topics

- [ ] Recent 2024-2025 papers
- [ ] Fill gaps identified during writing
- [ ] Re-read key papers for citations
- [ ] Review all notes and summaries

---

## Paper Search Strategy

### Academic Databases
- [ ] IEEE Xplore
- [ ] ACM Digital Library
- [ ] Google Scholar
- [ ] arXiv.org
- [ ] USENIX
- [ ] SpringerLink
- [ ] ScienceDirect

### Search Keywords

**Primary Keywords:**
- "machine learning" + "security" + "anomaly detection"
- "DevOps security"
- "CI/CD security"
- "supply chain attack"
- "intrusion detection" + "machine learning"
- "behavioral anomaly detection"

**Secondary Keywords:**
- "feature engineering" + "security"
- "time-series anomaly detection"
- "LSTM" + "security"
- "autoencoder" + "anomaly"
- "insider threat detection"
- "continuous integration security"

### Conference & Journal Targets

**Top Security Conferences:**
- IEEE Security & Privacy (Oakland)
- USENIX Security
- ACM CCS
- NDSS
- Black Hat / DEF CON (practitioner focus)

**Top ML Conferences:**
- NeurIPS
- ICML
- ICLR
- KDD

**Relevant Journals:**
- IEEE Transactions on Information Forensics and Security
- Computers & Security
- Journal of Cybersecurity
- ACM Transactions on Privacy and Security

---

## Literature Review Outline (For Thesis Chapter 2)

### 2.1 DevOps Security Landscape (8-10 pages)
- Introduction to DevOps and CI/CD
- Security challenges in DevOps environments
- CI/CD attack vectors (based on OWASP Top 10)
- Supply chain security threats
- Real-world incidents and case studies

### 2.2 Machine Learning for Security (10-12 pages)
- Overview of ML in cybersecurity
- Supervised vs unsupervised approaches
- Challenges: false positives, concept drift, evaluation
- ML for intrusion detection (network, host, application)
- Behavioral analytics and UEBA

### 2.3 Anomaly Detection Techniques (8-10 pages)
- Statistical methods
- Machine learning algorithms
  - Isolation Forest
  - One-Class SVM
  - Autoencoders
  - LOF
- Deep learning approaches
  - LSTM for sequences
  - GANs for anomaly detection
- Ensemble methods

### 2.4 Feature Engineering for Security (5-7 pages)
- Importance of feature engineering
- Temporal features
- Behavioral features
- Network and access features
- Domain-specific features for DevOps

### 2.5 Existing Solutions and Gap Analysis (5-7 pages)
- Commercial tools (GitHub Advanced Security, GitLab, Snyk, etc.)
- Open-source projects
- Academic prototypes
- Identified gaps
  - Lack of behavioral anomaly detection in DevOps
  - Limited ML-based approaches for CI/CD
  - Need for comprehensive evaluation
  - **Your contribution fills these gaps**

---

## Notes Template

### [Topic/Paper] - [Date]

**Key Insights:**
- [Insight 1]
- [Insight 2]

**Questions/Ideas:**
- [Question to explore]
- [Idea for your research]

**Connections to Other Papers:**
- [Paper A] relates to this via [concept]
- [Paper B] contradicts this in [aspect]

**To Do:**
- [ ] Follow up on reference [X]
- [ ] Check related work by [Author Y]

---

## Progress Tracking

| Category | Target Papers | Papers Read | Papers Cited | % Complete |
|----------|---------------|-------------|--------------|------------|
| DevOps Security | 15 | 0 | 0 | 0% |
| Supply Chain | 10 | 0 | 0 | 0% |
| ML for Security | 20 | 0 | 0 | 0% |
| Anomaly Detection | 15 | 0 | 0 | 0% |
| Time-Series | 10 | 0 | 0 | 0% |
| Feature Engineering | 10 | 0 | 0 | 0% |
| Case Studies | 10 | 0 | 0 | 0% |
| Behavioral Analysis | 10 | 0 | 0 | 0% |
| Commercial Tools | 5 | 0 | 0 | 0% |
| Foundational ML | 10 | 0 | 0 | 0% |
| **TOTAL** | **115** | **0** | **0** | **0%** |

---

## Tips for Effective Literature Review

1. **Start Broad, Then Narrow:** Begin with surveys and overview papers, then dive into specific topics.

2. **Take Good Notes:** Summarize key points immediately after reading. Future you will thank present you.

3. **Track Citations:** Note which papers cite each other. Understand the research lineage.

4. **Critical Reading:** Don't just accept findings. Question methodology, evaluate claims.

5. **Synthesize, Don't Summarize:** Find themes, contradictions, and gaps across papers.

6. **Organize Early:** Use reference manager from day one. Organize as you go.

7. **Read Actively:** Have questions in mind. Read with purpose, not just to accumulate papers.

8. **Keep Track of Gaps:** Note what's missing in the literature. This justifies your contribution.

9. **Stay Current:** Set up Google Scholar alerts for key terms. Check recent conference proceedings.

10. **Write As You Go:** Don't wait until the end to write the literature review. Draft sections as you read.

---

**Remember:** Quality over quantity. 100 well-understood papers are better than 200 skimmed papers.

Good luck with your literature review!
