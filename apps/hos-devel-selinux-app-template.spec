%global modulename MODULENAME

%{?selinux_requires}
BuildArch: noarch
BuildRequires: hos-devel-selinux-interfaces
License: AGPLv3+
Name: hos-devel-selinux-app-%{modulename}
Release: 1%{?dist}
Source0: %{modulename}.if
Summary: SELinux access interfaces for MODULE
URL: https://github.com/HardHatOS/selinux-app-%{modulename}
Version: 1.0

%description
Hard Hat OS (HOS) SELinux access interfaces for MODULE

%pre
# RPM macro that defines the SELinux directory where the interface files are placed in
%define _contribdir %{_datadir}/selinux/devel/include/contrib

%install
# Copy the SELinux interface file to the proper directory
%{__install} -D -m 0644 %{SOURCE0} -t %{buildroot}%{_contribdir}

%files
%{_contribdir}/%{modulename}.if
