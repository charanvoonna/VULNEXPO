# modules/vuln_signatures.py
"""
Knowledge base for vulnerability & exposure detection.
Maps detected services → CVEs → possible exploit paths.
Conservative by design (low false positives).
"""

SIGNATURES = [

    # --------------------------------------------------
    # APACHE HTTPD
    # --------------------------------------------------
    {
        "id": "apache_path_traversal",
        "type": "vulnerability",
        "service": "apache",
        "service_aliases": ["apache", "httpd", "apache httpd"],
        "version_match": {
            "type": "lte",
            "value": "2.4.50"
        },
        "cve": "CVE-2021-41773",
        "description": "Apache HTTPD path traversal and possible RCE.",
        "exploit_module": "exploit/multi/http/apache_path_traversal",
        "base_confidence": 0.95
    },

    {
        "id": "apache_struts_rce",
        "type": "vulnerability",
        "service": "apache",
        "service_aliases": ["apache", "httpd"],
        "version_match": {
            "type": "any",
            "value": ""
        },
        "cve": "CVE-2017-5638",
        "description": "Apache Struts OGNL injection RCE.",
        "exploit_module": "exploit/multi/http/struts2_content_type_ognl",
        "base_confidence": 0.40
    },

    # --------------------------------------------------
    # OPENSSH
    # --------------------------------------------------
    {
        "id": "openssh_roaming_leak",
        "type": "vulnerability",
        "service": "openssh",
        "service_aliases": ["openssh", "ssh"],
        "version_match": {
            "type": "lte",
            "value": "7.2"
        },
        "cve": "CVE-2016-0777",
        "description": "OpenSSH roaming information leak.",
        "exploit_module": None,
        "base_confidence": 0.70
    },

    # --------------------------------------------------
    # VSFTPD
    # --------------------------------------------------
    {
        "id": "vsftpd_backdoor",
        "type": "vulnerability",
        "service": "ftp",
        "service_aliases": ["ftp", "vsftpd"],
        "version_match": {
            "type": "contains",
            "value": "2.3.4"
        },
        "cve": "CVE-2011-2523",
        "description": "VSFTPD backdoor command execution.",
        "exploit_module": "exploit/unix/ftp/vsftpd_234_backdoor",
        "base_confidence": 0.98
    },

    # --------------------------------------------------
    # SAMBA
    # --------------------------------------------------
    {
        "id": "samba_usermap_script",
        "type": "vulnerability",
        "service": "netbios-ssn",
        "service_aliases": ["samba", "netbios-ssn", "microsoft-ds"],
        "version_match": {
            "type": "lte",
            "value": "3.0.20"
        },
        "cve": "CVE-2007-2447",
        "description": "Samba usermap script command execution.",
        "exploit_module": "exploit/multi/samba/usermap_script",
        "base_confidence": 0.95
    },

    # --------------------------------------------------
    # TOMCAT
    # --------------------------------------------------
    {
        "id": "tomcat_mgr_upload",
        "type": "vulnerability",
        "service": "http",
        "service_aliases": ["tomcat", "http"],
        "version_match": {
            "type": "any",
            "value": ""
        },
        "cve": None,
        "description": "Apache Tomcat Manager interface exposed (possible WAR upload).",
        "exploit_module": "exploit/multi/http/tomcat_mgr_upload",
        "base_confidence": 0.60
    },

    # --------------------------------------------------
    # MYSQL
    # --------------------------------------------------
    {
        "id": "mysql_weak_auth",
        "type": "misconfiguration",
        "service": "mysql",
        "service_aliases": ["mysql"],
        "version_match": {
            "type": "any",
            "value": ""
        },
        "cve": None,
        "description": "MySQL service exposed; weak or default credentials possible.",
        "exploit_module": None,
        "base_confidence": 0.40
    },

    # --------------------------------------------------
    # POSTGRESQL
    # --------------------------------------------------
    {
        "id": "postgres_trust_auth",
        "type": "misconfiguration",
        "service": "postgresql",
        "service_aliases": ["postgresql"],
        "version_match": {
            "type": "any",
            "value": ""
        },
        "cve": None,
        "description": "PostgreSQL service exposed; trust authentication possible.",
        "exploit_module": None,
        "base_confidence": 0.35
    },

    # --------------------------------------------------
    # SMB (WINDOWS / LINUX)
    # --------------------------------------------------
    {
        "id": "ms17_010_eternalblue",
        "type": "vulnerability",
        "service": "microsoft-ds",
        "service_aliases": ["microsoft-ds", "smb", "netbios-ssn"],
        "version_match": {
            "type": "any",
            "value": ""
        },
        "cve": "CVE-2017-0144",
        "description": "SMBv1 EternalBlue (MS17-010) possible vulnerability.",
        "exploit_module": "exploit/windows/smb/ms17_010_eternalblue",
        "base_confidence": 0.50
    },


    # --------------------------------------------------
    # LEGACY RPC
    # --------------------------------------------------
    {
        "id": "dcom_ms03_026",
        "type": "vulnerability",
        "service": "msrpc",
        "service_aliases": ["msrpc", "dcerpc"],
        "version_match": {
            "type": "any",
            "value": ""
        },
        "cve": "CVE-2003-0352",
        "description": "DCOM/MSRPC vulnerability (MS03-026).",
        "exploit_module": "exploit/windows/dcerpc/dcom_ms03_026",
        "base_confidence": 0.30
    }

]
