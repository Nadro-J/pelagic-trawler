import dnstwist
import time
import logging
import logging.handlers
from urllib.parse import urlparse
import yaml
import json
import os


# Logging Configuration
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# File handler
file_handler = logging.FileHandler('./logs/monitor.log')
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)


def get_domain_name(url):
    try:
        parsed_uri = urlparse(url)
        return '{uri.netloc}'.format(uri=parsed_uri)
    except Exception as e:
        logging.error(f"Error parsing URL {url}: {e}")
        return None


def find_similar_domains(domain):
    try:
        return dnstwist.run(domain=domain, registered=True, lsh='ssdeep', mxcheck=True, format='json')
    except Exception as e:
        logging.error(f"Error finding similar domains for {domain}: {e}")
        return None


def load_config(file_path='config.yaml'):
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        logging.error(f"Error loading configuration file: {e}")
        return None


def levenshtein_distance(s1, s2):
    """
    Calculate the Levenshtein distance between two strings.
    :param s1: The first string
    :param s2: The second string
    :return: The Levenshtein distance
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def filter_by_similarity(original_domain, similar_domains, similarity_threshold=80):
    """
    Filter the similar domains based on the similarity percentage.
    :param original_domain: The original domain name
    :param similar_domains: List of similar domain names
    :param similarity_threshold: The similarity percentage threshold
    :return: Filtered list of similar domain names
    """
    filtered_domains = []
    for domain in similar_domains:
        # Remove schema and extract netloc
        netloc = get_domain_name("https://" + domain['domain'])
        # Calculate the Levenshtein distance
        distance = levenshtein_distance(original_domain, netloc)
        # Calculate the similarity percentage
        similarity = (1 - (distance / max(len(original_domain), len(netloc)))) * 100
        if similarity >= similarity_threshold:
            filtered_domains.append(domain)
    return filtered_domains


def save_results(original_domain, similar_domains):
    """
    Save the similar domains to a JSON file inside the 'outputs' directory.
    :param original_domain: The original domain name
    :param similar_domains: List of similar domain names
    """
    # Create 'outputs' directory if it doesn't exist
    output_directory = 'outputs'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Generate file name with current timestamp
    timestamp = time.strftime("%d%m%y_%H%M")
    file_name = f"{original_domain.replace('.', '_')}_{timestamp}.json"

    # Full path to the file
    output_file_path = os.path.join(output_directory, file_name)

    # Save to file
    try:
        with open(output_file_path, 'w') as file:
            json.dump(similar_domains, file, indent=4)
        logging.info(f"Saved results to {output_file_path}")
    except Exception as e:
        logging.error(f"Error saving results to file: {e}")


def main():
    # Load configuration
    config = load_config()
    if not config:
        logging.error("Failed to load configuration.")
        return

    urls = config.get('urls', [])

    # Loop through the URLs to monitor
    for target_url in urls:
        logging.info(f"Checking {target_url}, please wait...")
        domain = get_domain_name(target_url)
        if domain:
            similar_domains = find_similar_domains(domain)

            # Filter similar domains by Levenshtein distance
            similar_domains = filter_by_similarity(domain, similar_domains)
            logging.info(f"{len(similar_domains)} similar domains found")
            if similar_domains:
                save_results(domain, similar_domains)
            else:
                logging.info("No phishing sites found.")
        logging.info('-' * 80)


if __name__ == "__main__":
    main()
