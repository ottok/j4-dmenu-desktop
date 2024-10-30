enabled_completions = get_option('enabled-shell-completions')

if enabled_completions == []
  summary(
    'generated shell completions',
    false,
    section: 'Optional build components',
    bool_yn: true,
  )
  subdir_done()
endif

crazy_complete_min_version = '0.2.0'

crazy_complete_exe = find_program(
  'crazy-complete',
  native: true,
  version: '>=' + crazy_complete_min_version,
  disabler: true,
  required: get_option('generate-shell-completions'),
)

if crazy_complete_exe.found() and crazy_complete_exe.version() != 'unknown'
  crazy_complete_version = crazy_complete_exe.version()
  if crazy_complete_version.version_compare('!=' + crazy_complete_min_version)
    warning(
      f'Version of crazy-complete @crazy_complete_version@ doesn\'t match the',
      f'expected version @crazy_complete_min_version@. Build will proceed, but',
      f'consider using version @crazy_complete_min_version@ if you have',
      'problems with your version.'
    )
  endif
endif

summary(
  'generated shell completions',
  crazy_complete_exe.found(),
  section: 'Optional build components',
  bool_yn: true,
)

shells = {
  'bash': ['@0@', get_option('datadir') / 'bash-completion/completions'],
  'fish': ['@0@.fish', get_option('datadir') / 'fish/vendor_completions.d'],
  'zsh' : ['_@0@', get_option('datadir') / 'zsh/site-functions'],
}

completion_targets = []

foreach shell, out_file_data : shells
  out_file = out_file_data[0]
  install_dir = out_file_data[1]

  if shell in enabled_completions
    completion_targets += custom_target(
      command: [crazy_complete_exe, shell, '@INPUT@', '--output', '@OUTPUT@'],
      input: 'j4-dmenu-desktop.yaml',
      output: out_file.format('j4-dmenu-desktop'),
      install: true,
      install_dir: install_dir,
    )

    if get_option('generate-tests-shell-completion')
      completion_targets += custom_target(
        command: [crazy_complete_exe, shell, '@INPUT@', '--output', '@OUTPUT@'],
        input: 'j4-dmenu-tests.yaml',
        output: out_file.format('j4-dmenu-tests'),
        install: true,
        install_dir: install_dir,
      )
    endif
  endif
endforeach

alias_target('shell-completions', completion_targets)
