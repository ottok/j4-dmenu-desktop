enabled_completions = get_option('enabled-shell-completions')

if enabled_completions == []
  subdir_done()
endif

crazy_complete_exe = find_program(
  'crazy-complete',
  native: true,
  version: '>=0.1.0',
  disabler: true,
  required: get_option('generate-shell-completions'),
)

shells = {
  'bash': [
    'j4-dmenu-desktop',
    get_option('datadir') / 'bash-completion/completions',
  ],
  'fish': [
    'j4-dmenu-desktop.fish',
    get_option('datadir') / 'fish/vendor_completions.d',
  ],
  'zsh': ['_j4-dmenu-desktop', get_option('datadir') / 'zsh/site-functions'],
}

completion_targets = []

foreach shell, out_file_data : shells
  out_file = out_file_data[0]
  install_dir = out_file_data[1]

  if shell in enabled_completions
    completion_targets += custom_target(
      command: [crazy_complete_exe, shell, '@INPUT@', '--output', '@OUTPUT@'],
      input: 'j4-dmenu-desktop.yaml',
      output: out_file,
      install: true,
      install_dir: install_dir,
    )
  endif
endforeach

alias_target('shell-completions', completion_targets)
