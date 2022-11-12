# ShyySH

Secure Shell (SSH) connection manager with TUI

<p align="center">
<img alt="screenshot0" src="https://user-images.githubusercontent.com/31232338/201325494-ceb243c7-c72b-4ed5-9c11-7c9c33465cae.png" width="400"/>
<img alt="screenshot1" src="https://user-images.githubusercontent.com/31232338/201325631-94eded7a-24bb-4f8e-8e1e-d9f3f9bc3529.png" width="400"/>
</p>

## Stack

* Python 3.9+
* [asciimatics](https://github.com/peterbrittain/asciimatics)
* [libtmux](https://libtmux.git-pull.com/)
* [TinyDB](https://github.com/msiemens/tinydb)

## Install

### Archlinux

```commandline
yay -S shyysh
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

Validation in 'Connection Edit' frame is for informational purposes only - it will not disallow 
saving unexecutable profiles.

Default location for config file and DB: `~/.config/shyysh`

## Why ShyySH?

> Видишь ящики - грузи в ящики
> 
> ...
> 
> Сломаешь шиш - получишь десятку


## Issues

- Sometimes terminal color scheme is being reset when resizing window.

- Phantomly set options in 'Add Connection' frame after deleting connection profile.