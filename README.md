# Dotbot xbps Plugin

For use with [dotbot](https://github.com/anishathalye/dotbot),
this plugin allows one to easily install or upgrade a list of xbps packages
on Void Linux.

This plugin is heavily inspired by the
[apt-get](https://github.com/rubenvereecken/dotbot-apt-get) plugin, and all
the other dotbot package management plugins.

## Usage

Add this plugin to your dotfiles repo as a submodule

```bash
git submodule add https://github.com/m-wynn/dotbot-xbps
```

Modify your install script to use dotbot-xbps as a plugin

```bash
"${BASEDIR}/${DOTBOT_DIR}/${DOTBOT_BIN}" -d "${BASEDIR}" -c "${CONFIG}" \
  --plugin-dir "${BASEDIR}/dotbot-xbps" "${@}"
```

Alternatively, run the install script specifying the plugin with `-p`

```bash
./install -p dotbot-xbps/xbps.py -c install.conf.yaml
```

The plugin will detect if it is not running as root, and will prepend `sudo`
to the `xbps-install` command.

Example for `install.conf.yaml`:

```yaml
- xbps:
  - awesome
  - vim
  - zsh
```
