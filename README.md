# ShyySH

Secure Shell (SSH) connection manager with TUI

<p align="center">
<img alt="screenshot0" src="https://user-images.githubusercontent.com/31232338/202361474-9625c22d-d6f2-499c-afed-b35c9e288158.png" width="400"/>
<img alt="screenshot1" src="https://user-images.githubusercontent.com/31232338/202361517-97c532b0-c30f-45a5-9236-9da72f0525f5.png" width="400"/>
</p>

![GitHub](https://img.shields.io/github/license/m0nochr0me/shyysh?style=flat-square) ![GitHub last commit](https://img.shields.io/github/last-commit/m0nochr0me/shyysh?style=flat-square) ![AUR version](https://img.shields.io/aur/version/shyysh-git?style=flat-square)

## Stack

* Python 3.9+
* [asciimatics](https://github.com/peterbrittain/asciimatics)
* [libtmux](https://libtmux.git-pull.com/)
* [TinyDB](https://github.com/msiemens/tinydb)

## Install

### Archlinux

```commandline
yay -S shyysh-git
```

### Manual 

Ensure you have installed [tmux](https://github.com/tmux/tmux) in your os.

Install python packages from `requirements.txt`

```commandline
python setup.py build

python setup.py install
```

## Run

```commandline
shyysh
```

While being run outside existing tmux session it will start one, 
otherwise shyysh will be started in newly created tmux window.

## Notes

You may want to change default command key binding in `tmux.conf` to avoid conflicts when tmux session 
being run inside another:

```
unbind C-b
set -g prefix C-a
bind C-a send-prefix
```

---

Validation in 'Connection Edit' frame is for informational purposes only - it will not disallow 
saving unexecutable profiles.

---

Default location for config file and DB: `~/.config/shyysh`

## Why ShyySH?

> Видишь ящики - грузи в ящики
> 
> ...
> 
> Сломаешь шиш - получишь десятку


## Issues

- Sometimes terminal color scheme is being reset when resizing window.
