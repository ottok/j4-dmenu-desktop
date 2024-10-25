This directory contains shell completions.

All shell completions are managed by
[crazy-complete](https://github.com/crazy-complete/crazy-complete).

# How to get the completions?
Pregenerated completions are provided as [release
artifacts](https://github.com/enkore/j4-dmenu-desktop/releases). This is the
simplest way to get j4-dmenu-desktop's completions. This is also the recommended
way to get completions for package maintainers.

Completions can be generated manually using j4-dmenu-desktop's Meson build
system. J4-dmenu-desktop's CMake build system doesn't support generating
completions.

To build completions, you have to have `crazy-complete` available when
setting up the builddir. You can use `-Dgenerate-shell-completions=enabled`
when doing setup to make sure that completions will be generated:

```
meson setup -Dgenerate-shell-completions=enabled builddir
```

You can then run `ninja` in the builddir to build j4-dmenu-desktop including
its shell completions. If you want to only build the completions, you can run

```
ninja shell-completions
```

from within the builddir. Shell completions will appear in the `etc/`
subdirectory of the builddir.

Installing completions through Meson is fully supported.

The third way to generate completions is to invoke `crazy-complete` manually.
The completion file is located at
[`etc/j4-dmenu-desktop.yaml`](../j4-dmenu-desktop.yaml).

# Why crazy-complete?
Crazy-complete is a niche project with a small user base. Because of this, I,
[meator](https://github.com/meator), will thoroughly test j4-dmenu-desktop's
completions whenever a new release of crazy-complete or j4-dmenu-desktop comes
around.

My research into shell completion generators showed that crazy-complete is the
best completion generator on the market. Its input format is easy to use, the
completions are robust and reasonably readable for a machine-generated shell
script and all major shells (Bash, Fish, ZSH) are supported.

j4-dmenu-desktop provided handwritten shell completions in the past. They can
now be found in the `deprecated/` directory. [Read its README for more
info](deprecated/README.md).
