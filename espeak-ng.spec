%define major      1
%define libname    %mklibname %{name}
%define libnamedev %mklibname %{name} -d

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
BuildRequires: pcaudiolib-devel
BuildRequires: %{_lib}sonic-devel
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: pkgconfig
Requires:      %{libname}  = %{EVRD}
Provides:      espeak
Obsoletes:     espeak < 1.50


%description
eSpeak NG is an open source speech synthesizer that supports 108 languages and accents.

%package -n     %{libname}
Summary:        Text to speech library (eSpeak NG)
Group:          System/Libraries
Requires:       %{name}  = %{EVRD}

%description -n %{libname}
The eSpeak NG (Next Generation) Text-to-Speech program is an open source speech
synthesizer that supports over 70 languages. It is based on the eSpeak engine
created by Jonathan Duddington. It uses spectral formant synthesis by default
which sounds robotic, but can be configured to use Klatt formant synthesis
or MBROLA to give it a more natural sound.

#------------------------------------------------

%package -n     %{libnamedev}
Summary:        Development files for %{name}
Group:          Development/C++
Requires:       %{libname}  = %{EVRD}
Provides:       %{name}-devel = %{EVRD}

%description -n %{libnamedev}
Development files for eSpeak NG, a software speech synthesizer.

%prep
%autosetup -n %{name}-%{version}
# needed because (angry.p)
#running autogen.sh cause
#configure.ac:10: error: required file 'config.h.in' not found
#next running autoheader gives configure.ac:4: error: required file './ltmain.sh' not found
#next, running also libtoolize --force --copy cause missing config.h.in but this time in subdir src/ucd-tools.
#running autoreconf in subdir cause: Makefile.am: error: required file './NEWS' not found
#fixed by simple touch NEWS.

aclocal -Im4
libtoolize --force --copy
autoheader
autoconf
automake -a --foreign

pushd src/ucd-tools
touch NEWS
libtoolize --force --copy
autoreconf -fi
popd

%build
# autotools insead of cmake because it fail with this during compilation: espeak-ng: error while loading shared libraries: libespeak-ng.so.1: cannot open shared object file: No such file or directory
# build proces require library before package is build... maybe need some weird bootstrap stuff. Autotools fixes it.
%configure
%make_build

%install
%make_install

rm -f %{buildroot}%{_libdir}/libespeak.la

%files
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

%files -n %{libname}
%{_libdir}/libespeak-ng.so.%{major}*
%doc COPYING

%files -n %{libnamedev}
%dir %{_includedir}/espeak-ng
%{_includedir}/espeak-ng/*.h
%{_includedir}/espeak/speak_lib.h
%{_libdir}/libespeak-ng.so
%{_libdir}/pkgconfig/espeak-ng.pc
%doc README.md
