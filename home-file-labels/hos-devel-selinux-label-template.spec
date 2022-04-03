%global modulename MODULENAME

BuildArch: noarch
BuildRequires: hos-devel-selinux-interfaces
License: AGPLv3+
Name: hos-devel-selinux-label-%{modulename}
Release: 1%{?dist}
Requires: selinux-policy-devel
Source0: %{modulename}.if
Summary: SELinux access interfaces for TARGET files
URL: https://github.com/HardHatOS/selinux-label-home/%{modulename}
Version: 1.0

%description
SELinux access interfaces for TARGET files within the $HOME directory

%pre
# RPM macro that defines the SELinux directory where the interface files are placed in
%define _contribdir %{_datadir}/selinux/devel/include/contrib

%install
# Copy the SELinux interface file to the proper directory
%{__install} -D -m 0644 %{SOURCE0} -t %{buildroot}%{_contribdir}

%files
%{_contribdir}/%{modulename}.if
