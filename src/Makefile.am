## Process this file with automake to produce Makefile.in
## Created by Anjuta


uidir = $(pkgdatadir)/ui
ui_DATA = gradientedescendente.ui


## The main script
bin_SCRIPTS = gradientedescendente.py

## Directory where .class files will be installed
gradientedescendentedir = $(pythondir)/gradientedescendente


gradientedescendente_PYTHON = \
	gradientedescendente.py


EXTRA_DIST = $(ui_DATA)


# Remove ui directory on uninstall
uninstall-local:

	-rm -r $(uidir)

	-rm -r $(pkgdatadir)
