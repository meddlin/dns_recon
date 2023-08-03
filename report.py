"""Reporting module."""

###### Imports ######
import pprint
import collections.abc
from dns_recon import Resolv

# Reporting Module pulls domains from here.
domain_list = ["ssl247.biz", "sectigo.com", "comodoca.com", "comodoca.net"]

def list_to_string(data_list):
    '''Convert list to string.'''
    result = '|'.join(data_list)
    return result

def csv_report(domain_list):
    '''CSV report.'''
    print(f"Domain Name,A Record,AAAA Record,NS Record,SPF Record,DMARC Record")
    for dl in domain_list:
        domain_name = dl['domain']
        record_a = dl['domain_record']['A']
        record_aaaa = dl['domain_record']['AAAA']
        record_ns = list_to_string(dl['domain_record']['NS']) if isinstance(dl['domain_record']['NS'], collections.abc.Sequence) else dl['domain_record']['NS']
        record_spf = list_to_string(dl['domain_record']['SPF']) if isinstance(dl['domain_record']['SPF'], collections.abc.Sequence) else dl['domain_record']['SPF']
        record_dmarc = list_to_string(dl['domain_record']['DMARC']) if isinstance(dl['domain_record']['DMARC'], collections.abc.Sequence) else dl['domain_record']['DMARC']
        print(f"{domain_name},{record_a},{record_aaaa},{record_ns},{record_spf},{record_dmarc}")

def idomain(domain):
    '''List of tasks for each domain.'''
    a_record = Resolv.resolv_a(domain)
    aaaa_record = Resolv.resolv_aaaa(domain)
    ns_record = Resolv.resolv_nameserver(domain)
    spf_record = Resolv.resolv_spf(domain)
    dmarc_record = Resolv.resolv_dmarc(domain)
    domain_record = {
        "A" : a_record,
        "AAAA" : aaaa_record,
        "NS" : ns_record,
        "SPF": spf_record,
        "DMARC": dmarc_record
    }
    return {"domain": domain, "domain_record": domain_record}


def main():
    '''Main function.'''
    domain_details = [idomain(domain) for domain in domain_list]
    pretty_print = pprint.PrettyPrinter(indent=4)
    csv_report(domain_details)
    for i in domain_details:
        pretty_print.pprint(i)
        print()
    return True


# Run main function
if __name__ == "__main__":
    main()
