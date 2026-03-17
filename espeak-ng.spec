%define major      1
%define libname    %mklibname %{name}
%define libnamedev %mklibname %{name} -d

%bcond_with	mbrola

Summary:		An open source speech synthesizer that supports 108 languages and accents
Name:	espeak-ng
Version:		1.52.0.1
Release:		1
License:		GPLv3
Group:	Sound
Url:	https://github.com/espeak-ng/espeak-ng
Source0:	%{name}-%{version}.tar.xz
#Source0:	https://github.com/espeak-ng/espeak-ng/archive/refs/tags/%%{version}/%%{name}-%%{version}.tar.gz
Source100:	%{name}.rpmlintrc
BuildRequires:		cmake
BuildRequires:		make
# Not provided yet - https://github.com/numediart/MBROLA
#BuildRequires:		mbrola
BuildRequires:		pkgconfig
#BuildRequires:		ronn
#BuildRequires:		rubygem-ronn
BuildRequires:		pcaudiolib-devel
BuildRequires:		%{_lib}sonic-devel
%rename	espeak

#patchlist

%description
This is an open source speech synthesizer that supports 108 languages and
accents.  It is based on the eSpeak engine created by Jonathan Duddington.
It uses spectral formant synthesis by default which sounds robotic, but can be
configured to use Klatt formant synthesis or MBROLA to give it a more natural
sound.

%files
%license COPYING
%doc docs/*.md ChangeLog.md README.md
%{_bindir}/espeak
%{_bindir}/%{name}
%{_bindir}/speak
%{_bindir}/speak-ng
%dir %{_datadir}/%{name}-data
%{_datadir}/%{name}-data/*_dict
%{_datadir}/%{name}-data/intonations
%dir %{_datadir}/%{name}-data/lang
%{_datadir}/%{name}-data/lang/*
%if %{with mbrola}
%dir %{_datadir}/%{name}-data/mbrola_ph
%{_datadir}/%{name}-data/mbrola_ph/*
%dir %{_datadir}/%{name}-data/voices/mb
%{_datadir}/%{name}-data/voices/mb/*
%endif
%{_datadir}/%{name}-data/phondata
%{_datadir}/%{name}-data/phondata-manifest
%{_datadir}/%{name}-data/phonindex
%{_datadir}/%{name}-data/phontab
%dir %{_datadir}/%{name}-data/voices
%dir %{_datadir}/%{name}-data/voices/!v
%{_datadir}/%{name}-data/voices/!v/*
%{_datadir}/vim/vimfiles/ftdetect/espeakfiletype.vim
%{_datadir}/vim/vimfiles/syntax/espeaklist.vim
%{_datadir}/vim/vimfiles/syntax/espeakrules.vim
%{_datadir}/vim/registry/espeak.yaml

#-----------------------------------------------------------------------------

%package -n %{libname}
Summary: 	Text to speech library (eSpeak NG)
Group:	System/Libraries
Requires:	%{name}  = %{EVRD}

%description -n %{libname}
The eSpeak NG (Next Generation) Text-to-Speech program is an open source speech
synthesizer that supports over 108 languages.

%files -n %{libname}
%license COPYING COPYING.*
%{_libdir}/lib%{name}.so.%{major}*

#-----------------------------------------------------------------------------

%package -n %{libnamedev}
Summary:		Development files for %{name}
Group:	Development/C++
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{libnamedev}
Development files for eSpeak NG, a software speech synthesizer.

%files -n %{libnamedev}
%license COPYING COPYING.*
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_includedir}/espeak/speak_lib.h
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

#-----------------------------------------------------------------------------

%prep
%autosetup -p1 -n %{name}-%{version}


%build
%cmake -DENABLE_TESTS=OFF
%make_build


%install
%make_install -C build

# Put the pkgconfig file in the right place...
mkdir -p %{buildroot}%{_libdir}/pkgconfig/
mv %{buildroot}/usr/lib/pkgconfig/%{name}.pc %{buildroot}%{_libdir}/pkgconfig/
# ... and also the vim registry file
mkdir -p %{buildroot}%{_datadir}/vim/registry/
install -m 0644 vim/registry/espeak.yaml %{buildroot}%{_datadir}/vim/registry/
