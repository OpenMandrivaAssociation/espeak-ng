Name:          espeak-ng
Version:       1.52.0
Release:       1
Summary:       eSpeak NG is an open source speech synthesizer that supports 108 languages and accents
Group:         System/Multimedia
URL:           https://github.com/espeak-ng/espeak-ng
Source:        https://github.com/espeak-ng/espeak-ng/archive/refs/tags/%{version}/%{name}-%{version}.tar.gz
# Taken from fork used by piper-phonemized
#Patch0:        espeak-ng-1.51.1+20240504git.f57b594-add-espeak_TextToPhonemesWithTerminator.patch
#Patch0:         https://build.opensuse.org/projects/science/packages/espeak-ng/files/espeak-ng-add-piper-support.patch
License:       GPL

#BuildRequires: ruby-ronn-ng
Requires:      lib%{name} = %{?epoch:%epoch:}%{version}-%{release}
Provides:      espeak
Obsoletes:     espeak < 1.50
Provides:      espeak-mbrola
Obsoletes:     espeak-mbrola < 1.50

%description
eSpeak NG is an open source speech synthesizer that supports 108 languages and accents.

%package -n lib%{name}
Group:         System/Libraries
Summary:       Shared libraries for %{name}

%description -n lib%{name}
This package contains shared libraries for %{name}.

%package -n lib%{name}-devel
Group:         Development/Libraries
Summary:       Development files for %{name}
Requires:      lib%{name} = %{?epoch:%epoch:}%{version}-%{release}
Requires:      pkg-config

%description -n lib%{name}-devel
This package contains libraries and header files for developing applications that use %{name}.

%debug_package

%prep
%autosetup -n %{name}-%{version}

%build
%cmake

%make_build

%install
%make_install -C build

rm -f %{buildroot}%{_libdir}/libespeak.la

%files
%defattr(-,root,root)
%{_bindir}/espeak
%{_bindir}/espeak-ng
%{_bindir}/speak
%{_bindir}/speak-ng
%dir %{_datadir}/espeak-ng-data
%{_datadir}/espeak-ng-data/*_dict
%{_datadir}/espeak-ng-data/intonations
%dir %{_datadir}/espeak-ng-data/lang
%{_datadir}/espeak-ng-data/lang/*
%dir %{_datadir}/espeak-ng-data/mbrola_ph
%{_datadir}/espeak-ng-data/mbrola_ph/*
%{_datadir}/espeak-ng-data/phondata
%{_datadir}/espeak-ng-data/phondata-manifest
%{_datadir}/espeak-ng-data/phonindex
%{_datadir}/espeak-ng-data/phontab
%dir %{_datadir}/espeak-ng-data/voices
%dir %{_datadir}/espeak-ng-data/voices/!v
%{_datadir}/espeak-ng-data/voices/!v/*
%dir %{_datadir}/espeak-ng-data/voices/mb
%{_datadir}/espeak-ng-data/voices/mb/*
%{_datadir}/vim/addons/ftdetect/espeakfiletype.vim
%{_datadir}/vim/addons/syntax/espeaklist.vim
%{_datadir}/vim/addons/syntax/espeakrules.vim
%{_datadir}/vim/registry/espeak.yaml
%{_mandir}/man1/espeak-ng.1*
%{_mandir}/man1/speak-ng.1*

%files -n lib%{name}
%defattr(-,root,root)
%{_libdir}/libespeak-ng.so.*
%doc COPYING

%files -n lib%{name}-devel
%defattr(-,root,root)
%dir %{_includedir}/espeak-ng
%{_includedir}/espeak-ng/*.h
%{_includedir}/espeak/speak_lib.h
%{_libdir}/libespeak-ng.a
%{_libdir}/libespeak-ng.so
%{_libdir}/pkgconfig/espeak-ng.pc
%doc README.md
