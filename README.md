backup
======

 * Install s3cmd: http://s3tools.org/repositories
 * Install MySQL-python via easy_install
 * Run s3cmd --configure
 * Edit ~/.s3cfg :
   - host_bucket = %(bucket)s.s3.amazonaws.com -> host_bucket = %(bucket)s.s.greenqloud.com
   - host_base = s3.amazonaws.com -> host_base = s.greenqloud.com
