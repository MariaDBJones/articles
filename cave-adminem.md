Securing access to a MariaDB database is essential to protect sensitive data and maintain system integrity. Basic security measures like enforcing strong passwords help prevent unauthorized access, while utilizing TLS (Transport Layer Security) ensures that data is encrypted during transmission. By combining these practices with regular updates and access control, you can significantly reduce the risk of security breaches.
This being said "Quis custodiet ipsos custodes" ? It's all good to have TLS backed connexions, strong passwords, a Maxscale proxy, NAT rules or port knocking, but all this does not prevent inside jobs from happening. Yeah, you think "what are the chances i get to hire a spy ?". Let's not forget the power of grudges. Disgruntled employees/contractors can be very damaging to a naive corporation. If you don't believe me here's an example. It's in french so please find a summary : A fired employee kept admin access during 2 days of her notice period. She did proceed to remove security software and erase financial records about mortgage loans. It took her 40 minutes. Now let's go back to securing our database.
First thing first, we want to know who did what. Using the audit plugin to create an audit log file allows documenting user actions, system changes, and access events in a secure, time-stamped record. This ensures transparency and accountability, helping to identify and analyze security incidents or compliance issues over time.

```
[mariadb]  
...  
\# load plugin  
plugin-load=server_audit=server_audit.so  
\# do not allow users to uninstall plugin nor server to start without it  
server_audit=FORCE_PLUS_PERMANENT  
\# enable logging  
server_audit_logging=ON  
\# you can add more filters   
  
\# pick either flat file or syslog  
\# My pref goes to syslog for tight integration in the system  
\# also syslog is much more complicated for a non sudo/root user to temper with  
  
\# flat file  
server_audit_output_type=FILE  
server_audit_file_path=/var/log/mysql/audit.log  
server_audit_file_rotate_size=1000000  
server_audit_file_rotations=9  
  
\# syslog  
server_audit_output_type=SYSLOG  
server_audit_syslog_facility=LOG_LOCAL6  
server_audit_syslog_ident=mysql_audit  
server_audit_syslog_info=this-host.name  
server_audit_syslog_priority=LOG_INFO
```

Second thing, we need to know who's who. Using nominative admin users instead of a single shared \`root\`@\`localhost\` user improves accountability. It also allows for better access control, enabling customized permissions and the ability to revoke access when necessary, which isn't feasible with a shared root account. We have two ways to handle those :
we use system tied account (meaning ssh access + possibility to tie the linux account password to the company ldap). Most GUI tools have the ssh tunneling ability so it should be okay.
```
CREATE USER 'luke.skywalker'@'localhost' IDENTIFIED via unix_socket WITH MAX_USER_CONNECTIONS 3;

CREATE USER 'darth.vador'@'localhost' IDENTIFIED via unix_socket WITH MAX_USER_CONNECTIONS 3;

CREATE USER 'lando.calrissian'@'localhost' IDENTIFIED via unix_socket WITH MAX_USER_CONNECTIONS 3;
```
We allow remote connexions but they have to use TLS and ECDSA authentication. In that case i would advise setting the host to the admin workstation and use RDP through vpn for remote work.
```
/* replace xx by the company policy about password expiration */

CREATE USER 'luke.skywalker'@'Tatooine' IDENTIFIED via ed25519 REQUIRE SSL WITH MAX_USER_CONNECTIONS 3 PASSWORD EXPIRE INTERVAL xx DAYS;

CREATE USER 'darth.vador'@'DeathStar' IDENTIFIED via ed25519 REQUIRE X509 WITH MAX_USER_CONNECTIONS 3 PASSWORD EXPIRE INTERVAL xx DAYS;

CREATE USER 'lando.calrissian'@'CloudCity' IDENTIFIED via ed25519 REQUIRE NONE WITH MAX_USER_CONNECTIONS 3 PASSWORD EXPIRE INTERVAL xx DAYS;
```
Third thing, let's head to the privileges. By using roles instead of personal grants we can centralize and reduce complexity of access management and minimize the risk of inadvertently leaving unauthorized access in place.
```
CREATE ROLE DBA;
GRANT all privileges ON *.* to DBA WITH GRANT OPTION;


/* replace ??? by the correct host depending on your previous step choice */
GRANT DBA to 'luke.skywalker'@'???' WITH ADMIN OPTION;
GRANT DBA to 'darth.vador'@'???' WITH ADMIN OPTION;
GRANT DBA to 'lando.calrissian'@'???' WITH ADMIN OPTION;


SET DEFAULT ROLE DBA FOR'luke.skywalker'@'???';
SET DEFAULT ROLE DBA FOR 'darth.vador'@'???';
SET DEFAULT ROLE DBA FOR 'lando.calrissian'@'???';
```
Fourth thing, we can also add some other features, such as port knocking by adding a specific port for admin/monitoring/backup users and disallowing them to connect through the main port using ad hoc firewall rules.
```
[mariadb]
...
extra_port = 3307 # or anything else that makes sense in your infra
extra_max_connections = 10 # give enough for all the admins + monitoring + backup tools
```
Now the security features for administrators are established, ensuring a robust framework for access management, we can easily implement account termination protocols. This allows us to swiftly deactivate any administrator accounts while maintaining security and compliance standards. Here's how :
```
Lock the account
/* replace ??? by the correct host depending on your previous choice */

ALTER USER 'darth.vador'@'???' ACCOUNT LOCK;
```
revoke the role from the user
```
/* replace ??? by the correct host depending on your previous choice */

REVOKE DBA FROM 'darth.vador'@'???';
SET DEFAULT ROLE NONE FOR 'darth.vador'@'???';
```
revoke the SSL certificate using CRLs
```
[mariadb]
...
ssl_crl=1
ssl_crlpath=/path/to/certificates/crl/
```
disable the system user

Of course all those operations can be automatized giving the HR and/or management (duh though) a nice app that allows to remove the admin access through one click. Alternatively, you gotta trust the fellow admins to take appropriate actions in due time upon your order.
Whichever way you choose, your admins are now both accountable and supervized.

Quod erat demonstrandum.

