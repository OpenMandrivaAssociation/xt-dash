%define	gcj_support	1

%define bname	xt
%define name	%{bname}-dash
%define version	20020426a
%define release	%mkrel 4
%define	jarlibs	servletapi5 xerces-j2 xml-commons-apis	

Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		0
Summary:	A fast, free implementation of XSLT in Java
License:	BSD-style
Group:		Development/Java
Source0:	http://www.blnz.com/xt/%{bname}-%{version}-src.tar.lzma
Source1:	xt-dash-build.xml
Patch0:		xt-dash-20020426a-public.patch
Url:		http://www.blnz.com/xt/index.html
Requires:	%{jarlibs}
BuildRequires:	ant
BuildRequires:	java-rpmbuild >= 0:1.5 lzma
BuildRequires:	%{jarlibs}
%if %{gcj_support}
Requires(post):	java-gcj-compat
Requires(postun):	java-gcj-compat
BuildRequires:	java-gcj-compat-devel
%else
BuildArch:	noarch
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
XT is an implementation in Java of XSL Transformations.

%package	javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java

%description	javadoc
Javadoc for %{name}.

%package	demo
Summary:	Demo for %{name}
Requires:	%{name} = %{version}
Group:		Development/Java

%description	demo
Demonstrations and samples for %{name}.

%prep
%setup -q -n %{bname}-%{version}-src
%patch0 -p1 -b .public
cp %{SOURCE1} build.xml
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;

%build
export CLASSPATH=$(build-classpath %{jarlibs})
ant jar javadoc
for jar in `find -name \*.jar -type f`; do
	if [ -z "`unzip -l $jar|grep META-INF/INDEX.LIST`" ]; then
		jar -i $jar
	fi
done

%install
rm -rf %{buildroot}
# jars
install -m644 build/lib/%{name}.jar -D %{buildroot}%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar %{buildroot}%{_javadir}/%{name}.jar

# javadoc
install -d %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr build/api/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

# data
install -d %{buildroot}%{_datadir}/%{name}
cp -r demo %{buildroot}%{_datadir}/%{name}


%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc copying.txt copyingjc.txt index.html README
%{_javadir}/*.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(-,root,root)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

%files demo
%defattr(-,root,root)
%{_datadir}/%{name}


