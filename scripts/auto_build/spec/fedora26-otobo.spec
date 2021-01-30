# --
# OTOBO is a web-based ticketing system for service organisations.
# --
# Copyright (C) 2001-2020 OTRS AG, https://otrs.com/
# Copyright (C) 2019-2021 Rother OSS GmbH, https://otobo.de/
# --
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# --

#
# WARNING: This file is autogenerated from "scripts/auto_build/spec/templates" via
# "bin/otobo.Console.pl Dev::Tools::RPMSpecGenerate". All changes will be lost.
#

Summary:      OTOBO Help Desk.
Name:         otobo
Version:      0.0
Copyright:    GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007
Group:        Applications/Mail
Provides:     otobo
Requires:     bash-completion cronie httpd mod_perl perl perl(Archive::Zip) perl(Crypt::Eksblowfish::Bcrypt) perl(Date::Format) perl(DateTime) perl(DBI) perl(Encode::HanExtra) perl(IO::Socket::SSL) perl(JSON::XS) perl(LWP::UserAgent) perl(Mail::IMAPClient) perl(Net::DNS) perl(Net::LDAP) perl(Template) perl(Text::CSV) perl(Text::CSV_XS) perl(URI) perl(XML::LibXML) perl(XML::LibXSLT) perl(XML::Parser) perl(YAML::XS) perl-core procmail
AutoReqProv:  no
Release:      01
Source0:      otobo-%{version}.tar.bz2
BuildArch:    noarch
BuildRoot:    %{_tmppath}/%{name}-%{version}-build

%description
OTOBO is the new Open source Ticket Request System with many features to manage
customer telephone calls and e-mails. It is distributed under the GNU
General Public License (GPL) and tested on Linux and Mac OS. Do you
receive many e-mails and want to answer them with a team of agents?
You're going to love OTOBO!

%prep
%setup

%build
# copy config file
cp Kernel/Config.pm.dist Kernel/Config.pm
# rename config POD file
mv Kernel/Config.pod.dist Kernel/Config.pod
# copy all crontab dist files
for foo in var/cron/*.dist; do mv $foo var/cron/`basename $foo .dist`; done
# copy all .dist files
cp .procmailrc.dist .procmailrc
cp .fetchmailrc.dist .fetchmailrc
cp .mailfilter.dist .mailfilter

%install
# delete old RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT
# set DESTROOT
export DESTROOT="/opt/otobo/"
# create RPM_BUILD_ROOT DESTROOT
mkdir -p $RPM_BUILD_ROOT/$DESTROOT/
# copy files
cp -R . $RPM_BUILD_ROOT/$DESTROOT
# configure apache
install -d -m 755 $RPM_BUILD_ROOT/etc/httpd/conf.d
install -m 644 scripts/apache2-httpd.include.conf $RPM_BUILD_ROOT/etc/httpd/conf.d/zzz_otobo.conf

# set permission
export OTOBOUSER=otobo
useradd $OTOBOUSER || :
useradd apache || :
groupadd apache || :
$RPM_BUILD_ROOT/opt/otobo/bin/otobo.SetPermissions.pl --web-group=apache

%pre
# useradd
export OTOBOUSER=otobo
echo -n "Check OTOBO user ... "
if id $OTOBOUSER >/dev/null 2>&1; then
    echo "$OTOBOUSER exists."
    # update groups
    usermod -g apache $OTOBOUSER
    # update home dir
    usermod -d /opt/otobo $OTOBOUSER
else
    useradd $OTOBOUSER -d /opt/otobo/ -s /bin/bash -g apache -c 'OTOBO System User' && echo "$OTOBOUSER added."
fi


%post
export OTOBOUSER=otobo

# note
HOST=`hostname -f`
echo ""
echo "Next steps: "
echo ""
echo "[restart web server]"
echo " systemctl restart apache2.service"
echo ""
echo "[install the OTOBO database]"
echo " Make sure your database server is running."
echo " Use a web browser and open this link:"
echo " http://$HOST/otobo/installer.pl"
echo ""
echo "[start OTOBO daemon and corresponding watchdog cronjob]"
echo " /opt/otobo/bin/otobo.Daemon.pl start"
echo " /opt/otobo/bin/Cron.sh start"
echo ""
echo " Your OTOBO Team"
echo ""

%clean
rm -rf $RPM_BUILD_ROOT

%files
%config /etc/httpd/conf.d/zzz_otobo.conf

%config(noreplace) /opt/otobo/Kernel/Config.pm
%config(noreplace) /opt/otobo/.procmailrc
%config(noreplace) /opt/otobo/.fetchmailrc
%config(noreplace) /opt/otobo/.mailfilter

%dir /opt/otobo/
/opt/otobo/RELEASE
/opt/otobo/ARCHIVE
/opt/otobo/.bash_completion
/opt/otobo/.procmailrc.dist
/opt/otobo/.fetchmailrc.dist
/opt/otobo/.mailfilter.dist

%dir /opt/otobo/Custom/
/opt/otobo/Custom/README

%dir /opt/otobo/Kernel/

%dir /opt/otobo/Kernel/Config/
/opt/otobo/Kernel/Config.pm.dist
/opt/otobo/Kernel/Config.pod
/opt/otobo/Kernel/Config/Files/
/opt/otobo/Kernel/Config/Defaults.pm

/opt/otobo/Kernel/GenericInterface*

/opt/otobo/Kernel/Language.pm
%dir /opt/otobo/Kernel/Language/
/opt/otobo/Kernel/Language/*.pm

/opt/otobo/bin*
/opt/otobo/Kernel/Autoload*
/opt/otobo/Kernel/Modules*
/opt/otobo/Kernel/Output*
/opt/otobo/Kernel/System*
/opt/otobo/scripts*
/opt/otobo/i18n/otobo/*

%dir /opt/otobo/var/
%dir /opt/otobo/var/article/
/opt/otobo/var/fonts/
/opt/otobo/var/httpd/
/opt/otobo/var/logo-otobo.png
%dir /opt/otobo/var/cron/
%dir /opt/otobo/var/log/
%dir /opt/otobo/var/sessions/
%dir /opt/otobo/var/spool/
/opt/otobo/var/cron/*
%dir /opt/otobo/var/tmp/
%dir /opt/otobo/var/stats/
/opt/otobo/var/stats/*.xml
%dir /opt/otobo/var/processes/examples/
/opt/otobo/var/processes/examples/*
%dir /opt/otobo/var/webservices/examples/
/opt/otobo/var/webservices/examples/*.pm

/opt/otobo/Kernel/cpan-lib*

%doc /opt/otobo/*.md
%doc /opt/otobo/COPYING
%doc /opt/otobo/COPYING-Third-Party
%doc /opt/otobo/doc*
