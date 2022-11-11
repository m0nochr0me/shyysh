# ShyySH

Secure Shell (SSH) connection manager with TUI

## Stack

* Python 3.9+
* [asciimatics](https://github.com/peterbrittain/asciimatics)
* [libtmux](https://libtmux.git-pull.com/)
* [TinyDB](https://github.com/msiemens/tinydb)

## Usage

Ensure you have installed [tmux](https://github.com/tmux/tmux) in your os.

Install python packages from `requirements.txt`

```commandline
python run.py
```

While being run outside existing tmux session it will start one, 
otherwise shyysh will be started in newly created tmux window.

## Notes

Validation in 'Connection Edit' frame is for informational purposes only - it will not disallow 
saving unexecutable profiles.

## Why ShyySH?

> Видишь ящики - грузи в ящики
> 
> ...
> 
> Сломаешь шиш - получишь десятку


## Issues

- Sometimes terminal color scheme is being reset when resizing window.

- Phantomly set options in 'Add Connection' frame after deleting connection profile.