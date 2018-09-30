DESTDIR=
PREFIX=/usr
SYSCONFDIR=/etc

PIP:=$(shell which pip3)
SYSTEMCTL:=$(shell which systemctl)

install:
	$(PIP) install -r requirements.txt
	if test -x "$(SYSTEMCTL)" && test -d "$(DESTDIR)$(SYSCONFDIR)/systemd/system"; then install -m0644 dash-listeners.service $(DESTDIR)$(SYSCONFDIR)/systemd/system/dash-listeners.service && $(SYSTEMCTL) daemon-reload; else echo "could not find systemd"; fi
	if test -e "$(DESTDIR)$(SYSCONFDIR)/systemd/system/dash-listeners.service" && test ! -e "$(DESTDIR)$(SYSCONFDIR)/systemd/system/multi-user.target.wants/dash-listeners.service"; then $(SYSTEMCTL) enable dash-listeners.service && $(SYSTEMCTL) start dash-listeners.service; else echo "dash-listeners daemon is already enabled"; fi
