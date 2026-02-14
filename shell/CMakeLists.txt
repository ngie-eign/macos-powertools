cmake_minimum_required(VERSION 4.0)

set(BINDIR $ENV{HOME}/.local/bin/)
set(BINMODE OWNER_EXECUTE OWNER_READ)

file(GLOB SCRIPTS "*.sh")

foreach(script IN LISTS SCRIPTS)
  get_filename_component(script_name ${script} NAME_WE)
  install(
    FILES ${script}
    DESTINATION ${BINDIR}
    PERMISSIONS ${BINMODE}
    RENAME ${script_name}
  )
endforeach()
