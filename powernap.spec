Summary:	Powernap
Name:		powernap
Version:	2.20
Release:	0.1
License:	GPL
Group:		Applications/System
Source0:	https://launchpad.net/powernap/trunk/%{version}/+download/%{name}_%{version}.orig.tar.gz
# Source0-md5:	3aa5bd8f6d5f69045a0f28ad7acca732
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PowerNap is a configurable daemon that will bring a running system to
a lower power state according to a set of configuration preferences.
It acts as a sort of "screensaver" for servers, watching the process
table for activity rather than the keyboard or mouse.

PowerNap will run $ACTION when none of $PROCESSES have executed for
some number of $ABSENCE seconds. For instance, PowerNap can
automatically "pm-suspend" a system if no instance of "kvm" runs for
some contiguous block of "300" seconds.

%package -n powernap-common
Summary:	powernap-common
Group:		Applications/System
Requires:	powernap-common_%{version}=upstart >= 0.6.5

%description -n powernap-common
This package contains the common library files required as a runtime
dependency of powernap.

%package -n powerwake
Summary:	powerwake
Group:		Applications/System
Requires:	powerwake_%{version}=upstart >= 0.6.5

%description -n powerwake
PowerWake is a generic mechanism for remotely waking systems. It is
intended to support wake-on-lan, ipmi, and other remote waking
mechanisms. Currently, wake-on-lan is the only supported mechanism. It
also includes some handy caching of MAC addresses, such that systems
can be awakened by hostname or ip address, in addition to MAC address.

%prep
%setup -q %{name}-%{version}

# developer cruft
rm powernap/.powernap.py.swp

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_bindir},%{_mandir}/man{1,8},%{_sysconfdir}/%{name},%{py_sitescriptdir}} \
	$RPM_BUILD_ROOT/etc/{bash_completion.d,pm/power.d}

install -p sbin/* $RPM_BUILD_ROOT%{_sbindir}
install -p bin/* $RPM_BUILD_ROOT%{_bindir}
cp -p powerwake_completion $RPM_BUILD_ROOT/etc/bash_completion.d
cp -p action config $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
cp -a actions/pm/* $RPM_BUILD_ROOT/etc/pm/power.d
cp -a powernap $RPM_BUILD_ROOT%{py_sitescriptdir}
cp -a man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1
cp -a man/*.8 $RPM_BUILD_ROOT%{_mandir}/man8

%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files -n powernap
%defattr(644,root,root,755)
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/action
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/config
%attr(755,root,root) %{_sbindir}/powernap
%attr(755,root,root) %{_sbindir}/powernap-action
%attr(755,root,root) %{_sbindir}/powernap-now
%attr(755,root,root) %{_sbindir}/powernapd
%attr(755,root,root) %{_sbindir}/powerwake-monitor
%attr(755,root,root) %{_sbindir}/powerwake-now
%attr(755,root,root) %{_sbindir}/powerwaked
%attr(755,root,root) %{_bindir}/powernap_calculator
%{_mandir}/man1/powernap_calculator.1*
%{_mandir}/man8/powernap-action.8*
%{_mandir}/man8/powernap-now.8*
%{_mandir}/man8/powernap.8*
%{_mandir}/man8/powernapd.8*
%{_mandir}/man8/powerwake-now.8*

%files -n powernap-common
%defattr(644,root,root,755)
/etc/pm/power.d/00flag
/etc/pm/power.d/01cpu_online
/etc/pm/power.d/cpu_frequency
/etc/pm/power.d/eth_speed
/etc/pm/power.d/kms_powermode
/etc/pm/power.d/usb
/etc/pm/power.d/usb_autosuspend
/etc/pm/power.d/video
%dir %{py_sitescriptdir}/%{name}
%{py_sitescriptdir}/%{name}/*.py[co]
%dir %{py_sitescriptdir}/%{name}/monitors
%{py_sitescriptdir}/%{name}/monitors/*.py[co]

%files -n powerwake
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/powerwake
%{_mandir}/man1/powerwake.1*
/etc/bash_completion.d/powerwake_completion
