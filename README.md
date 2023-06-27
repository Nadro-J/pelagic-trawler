# Pelagic - Domain Monitoring Tool

A comprehensive domain monitoring tool written in Python. Its primary purpose is to safeguard against phishing attempts that exploit domain names similar to legitimate ones. By employing the dnstwist library, the script uncovers permutations of domain names and scrutinizes them for potential threats. In case a suspicious domain is identified, it will be logged with a timestamp and stored in a well-structured JSON file for future analysis.
## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Contribution](#contribution)

## Introduction

In the age of ever-evolving cybersecurity threats, phishing attacks remain a prominent problem. A common tactic involves registering domains similar to a legitimate domain. This tool aims to proactively monitor and detect such domains, which could be potential phishing or malicious attempts. Utilizing the `dnstwist` library, it looks for various permutations of domain names and alerts the user of any suspicious domain names detected.
>While this tool is helpful in identifying potential phishing domains, it does not guarantee detection of all such domains and should be used as part of a broader cybersecurity strategy.

## Features
- **Domain Monitoring:** Monitors for domain names similar to the trusted domains specified in a configuration file.
- **Fuzzy Matching:** Utilizes Levenshtein distance algorithm to measure the similarity between domain names, filtering out the domains that meet a similarity threshold.
- **Configurable:** Allows users to easily specify the domains to monitor and set a similarity threshold through a configuration file.
- **Logging:** Logs the operations, findings, and errors to both the console and a log file with timestamps for auditing and analysis. Logs are stored in '/logs/monitor.log'.
- **Structured Output:** Saves the detected similar domain names in a prettify JSON file for each domain that is being monitored, allowing for easy further analysis. The JSON files are saved in a directory named 'outputs'.
- **Error Handling:** Gracefully handles errors such as configuration file loading issues and URL parsing problems, logging them for user review.
- **Flexible and Extensible:** Designed to be easily extended for additional functionalities such as sending notifications via email or integrating with incident response systems.

---

## Requirements

- Python 3.6+
- dnstwist
- PyYAML


## Installation
1. Clone the repository:
   ```
   git clone https://github.com/Nadro-J/pelagic-trawler
   cd pelagic-trawler
   ```

2. Install the required Python libraries:
    ```
    pip3 install -r requirements.txt
    ```


## Configuration
1. Edit the config.yaml file to specify the domains you want to monitor.
    ```yaml
    urls:
       - 'https://polkadot.js.org'
       - 'https://hydradx.io'
    ```


## Usage
Run the script:
    ```
    python3 peladic.py
    ```


## Contribution
Contributions to this project are welcome! Please fork the repository and create a pull request with your changes or improvements.

---

## Different fuzzer types
Each of these fuzzers is designed to catch different types of typos or changes that could be used in domain squatting or phishing attacks. Knowing what each fuzzer does can help you understand the types of domain variations that dnstwist can detect and the kind of threats each variation represents.

- **Original:** This is not actually a fuzzer, but rather it represents the original domain you are checking against.
- **Addition:** Additional characters are added to the domain.
- **BitSquatting:** This involves changing individual bits in the characters of the domain, exploiting memory errors in some systems.
- **Homoglyph:** Characters in the domain are replaced with similar-looking characters (e.g., replacing "o" with "0").
- **Hyphenation:** Hyphens are inserted between characters in the domain.
- **Insertion:** Characters are inserted at various positions in the domain.
- **Omission:** Characters are omitted from the domain.
- **Repetition:** Characters in the domain are repeated.
- **Replacement:** Characters in the domain are replaced with other characters.
- **Subdomain:** Characters are inserted, and dots are placed to create subdomains.
- **Transposition:** Adjacent characters in the domain are swapped.
- **Vowel-swap:** Vowels in the domain are swapped with other vowels.
