# dns_enum.py
import dns.resolver
import requests

def check_subdomain_status(subdomain):
    try:
        response = requests.get(f"http://{subdomain}", timeout=5)
        return response.status_code
    except requests.RequestException:
        return None

def perform_dns_enum(domain):
    results = []

    try:
        if not domain:
            raise ValueError("Please enter a domain.")

        main_domain_answers = dns.resolver.resolve(domain, 'A')
        main_domain_ip = [str(answer) for answer in main_domain_answers]
        results.append({"subdomain": domain, "ip_address": main_domain_ip, "status": check_subdomain_status(domain)})

        subdomains = ["www", "mail", "ftp", "localhost", "webmail", "smtp", "pop", "ns1", "webdisk", "ns2",
                      "cpanel", "whm", "autodiscover", "autoconfig", "m", "imap", "test", "ns", "blog", "pop3",
                      "dev", "www2", "admin", "forum", "news", "vpn", "ns3", "mail2", "new", "mysql", "old",
                      ]

        for subdomain in subdomains:
            subdomain_full = f"{subdomain}.{domain}"
            try:
                subdomain_answers = dns.resolver.resolve(subdomain_full, 'A')
                subdomain_ip = [str(answer) for answer in subdomain_answers]
                subdomain_status = check_subdomain_status(subdomain_full)
                results.append({"subdomain": subdomain_full, "ip_address": subdomain_ip, "status": subdomain_status})
            except dns.resolver.NXDOMAIN:
                results.append({"subdomain": subdomain_full, "error": "Domain not found", }) #"status": None
            except dns.exception.DNSException as e:
                results.append({"subdomain": subdomain_full, "error": str(e), "status": None}) #

    except ValueError as ve:
        results.append({"subdomain": domain, "error": str(ve), "status": None})
    except dns.resolver.NXDOMAIN:
        results.append({"subdomain": domain, "error": "Domain not found", }) #"status": None
    except dns.exception.DNSException as e:
        results.append({"subdomain": domain, "error": str(e), "status": None})

    return results


'''"lists", "support", "mobile", "mx", "static", "docs", "beta", "shop", "sql", "secure", "demo",
                      "cp", "calendar", "wiki", "web", "media", "email", "images", "img", "www1", "intranet",
                      "portal", "video", "sip", "dns2", "api", "cdn", "stats", "dns1", "ns4", "www3", "dns",
                      "search", "staging", "server", "mx1", "chat", "wap", "my", "svn", "mail1", "sites", "proxy",
                      "ads", "host", "crm", "cms", "backup", "mx2", "lyncdiscover", "info", "apps", "download",
                      "remote", "db", "forums", "store", "relay", "files", "newsletter", "app", "live", "owa", "en"'''