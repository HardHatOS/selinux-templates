BuildArch: noarch
BuildRequires: hos-selinux-access-interfaces, make, selinux-policy-devel
Group: System Environment/Base
License: GPLv3
Name: hos-selinux-app-MODULE
Release: 1%{?dist}
Requires: policycoreutils, libselinux-utils
Source0: MODULE.te
Source1: MODULE.if
Summary: SELinux policy module for MODULE
URL: https://github.com/HardHatOS/selinux-app-MODULE
Version: 1.0

%description
Description

%pre
# RPM macro that defines the SELinux directory where the interface files are placed in
%define _contribdir %{_datadir}/selinux/devel/include/contrib

# RPM macro to define the name of the SELinux policy module, without a file extension and path
%define _module "$(echo $(basename %{SOURCE0}) | %{__sed} s/\.te$//g)"

# RPM macro to define the filename of the compiled SELinux policy module
%define _pp "%{_module}.pp"

# RPM macro function for relabeling the specified file(s) and/or directory/directories
%define relabel() restorecon -R -v /etc /usr

%build
# Copy the SELinux .te file to the current directory
%{__cp} %{SOURCE0} .

# Compile the SELinux policy module
%{__make} %{?_smp_mflags} NAME=%{_pp} -f %{?policy_devel_root}%{_datadir}/selinux/devel/Makefile

%install
# Copy the compiled SELinux policy module to the proper directory
%{__install} -D -m 0600 %{_pp} -t %{buildroot}%{_datadir}/selinux/packages

# Copy the SELinux interface file to the proper directory
%{__install} -D -m 0644 %{SOURCE1} -t %{buildroot}%{_contribdir}

%files
%attr(0600,root,root) %{_datadir}/selinux/packages/*.pp
%attr(0644,root,root) %{_contribdir}/*.if

%post
# Install the SELinux policy module
semodule --noreload --install=%{_datadir}/selinux/packages/%{_pp};

# Check if SELinux is enabled
if /usr/sbin/selinuxenabled ; then
    # If so, then load the new SELinux policy into the kernel
    load_policy;
    # Relabel the specified file(s) and/or directory/directories
    %{relabel};
fi;

%postun
# Remove the specified SELinux policy module
semodule --noreload --remove=%{_module};

# Check if SELinux is enabled
if /usr/sbin/selinuxenabled ; then
    # If so, then load the new SELinux policy into the kernel
    /usr/sbin/load_policy;
    # Relabel the specified file(s) and/or directory/directories
    %{relabel};
fi;
