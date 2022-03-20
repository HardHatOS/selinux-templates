BuildArch: noarch
BuildRequires: hos-devel-selinux-interfaces, make, selinux-policy-devel
License: AGPLv3+
Name: hos-devel-selinux-label-MODULE
Release: 1%{?dist}
Requires: policycoreutils, libselinux-utils
Source0: MODULE.if
Summary: SELinux access interfaces for the TARGET directory
URL: https://github.com/HardHatOS/selinux-app-MODULE
Version: 1.0

%description
SELinux access interfaces for the $HOME/TARGET directory

%pre
# RPM macro that defines the SELinux directory where the interface files are placed in
%define _contribdir %{_datadir}/selinux/devel/include/contrib

%install
# Copy the SELinux interface file to the proper directory
%{__install} -D -m 0644 %{SOURCE0} -t %{buildroot}%{_contribdir}

%files
%attr(0644,root,root) %{_contribdir}/*.if
