scripts = [
  ['ainakan', 'repl'],
  ['ainakan-apk', 'apk'],
  ['ainakan-compile', 'compiler'],
  ['ainakan-create', 'create'],
  ['ainakan-discover', 'discover'],
  ['ainakan-itrace', 'itracer'],
  ['ainakan-join', 'join'],
  ['ainakan-kill', 'kill'],
  ['ainakan-ls', 'ls'],
  ['ainakan-ls-devices', 'lsd'],
  ['ainakan-pm', 'pm'],
  ['ainakan-ps', 'ps'],
  ['ainakan-pull', 'pull'],
  ['ainakan-push', 'push'],
  ['ainakan-rm', 'rm'],
  ['ainakan-trace', 'tracer'],
]

common_cdata = configuration_data()
common_cdata.set('PYTHON', python.full_path())
common_cdata.set('pythondir', python.get_install_dir())

foreach s : scripts
  cdata = configuration_data()
  cdata.merge_from(common_cdata)
  cdata.set('module', s.get(1))

  generated_script = configure_file(
    input: 'script.in',
    output: s.get(0),
    configuration: cdata,
  )

  install_data(generated_script,
    install_dir: get_option('bindir'),
    install_mode: 'rwxr-xr-x',
  )
endforeach
