%global modulename MODULENAME
%global selinuxtype targeted

%{?selinux_requires}
BuildArch: noarch
BuildRequires: hos-devel-selinux-interfaces
License: AGPLv3+
Name: hos-selinux-label-%{modulename}
Release: 1%{?dist}
Requires: bzip2, selinux-policy-%{selinuxtype}
Requires(post): selinux-policy-%{selinuxtype}
Source0: %{modulename}.fc
Source1: %{modulename}.if
Source2: %{modulename}.te
Summary: SELinux policy module (label only) for TARGET files
URL: https://github.com/HardHatOS/selinux-label-home/%{modulename}
Version: 1.0

%description
SELinux policy module (label only) for TARGET files within the $HOME directory

%pre
# RPM macro to define the filename of the compiled SELinux policy module
%define _pp %{modulename}.pp

# RPM macro to define the filename of the compressed SELinux policy module
%define _pp_bz2 %{_pp}.bz2

# RPM macro for relabeling the specified files/directories
%define relabel() restorecon -R -v /home

# RPM macro for SELinux preparation
%selinux_relabel_pre -s %{selinuxtype}

%build
# Copy the SELinux .te file to the current directory
%{__cp} %{SOURCE0} %{SOURCE1} %{SOURCE2} .

# Compile the SELinux policy module
%{__make} %{?_smp_mflags} NAME=%{_pp} -f %{?policy_devel_root}%{_datadir}/selinux/devel/Makefile

# Compress the compiled SELinux policy module
%{__bzip2} --best %{_pp}

%install
# Copy the compiled SELinux policy module to the proper directory
%{__install} -D -m 0644 %{_pp_bz2} -t %{buildroot}%{_datadir}/selinux/packages/%{selinuxtype}

%post
# Install the SELinux policy module
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{selinuxtype}/%{_pp_bz2}

%postun
if [ $1 -eq 0 ]; then
    # Uninstall the specified SELinux policy module
    %selinux_modules_uninstall -s %{selinuxtype} %{modulename}
fi

%posttrans
# Relabel the specified file(s) and/or directories after every transaction
%selinux_relabel_post -s %{selinuxtype}
%{relabel}

%files
%{_datadir}/selinux/packages/%{selinuxtype}/%{_pp_bz2}
