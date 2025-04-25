cmake_minimum_required(VERSION 4.0)

set(BINDIR $ENV{HOME}/.local/bin/)
set(BINMODE OWNER_EXECUTE OWNER_READ)

install(
  PROGRAMS brew-autoupdate set-remote-power-settings show-hidden-files-in-finder
           viexports zzz
  DESTINATION ${BINDIR}
  PERMISSIONS ${BINMODE})
