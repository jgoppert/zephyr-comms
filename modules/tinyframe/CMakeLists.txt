set(TINYFRAME_DIR ${ZEPHYR_CURRENT_MODULE_DIR})

zephyr_library()

zephyr_include_directories(
  ${TINYFRAME_DIR}
  ${TINYFRAME_DIR}/TinyFrame
  ${TINYFRAME_DIR}/TinyFrame/demo
  )

zephyr_library_sources(
  ${ZEPHYR_CURRENT_MODULE_DIR}
  ${TINYFRAME_DIR}/TinyFrame/TinyFrame.c
  ${TINYFRAME_DIR}/TinyFrame/demo/utils.c
)