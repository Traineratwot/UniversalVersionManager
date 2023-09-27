# UniversalVersionManage

The purpose of this project to create a universal tool for developers will switch the versions of your tools

**Now supported** `nodejs`

## Install

//TODO

## Usage

### common

- help - print help

```bash
uvm -h 
```

`3 argument version can bee any version string eg: 20, 20.8, 20.8.9, v20.8.9 ...`

### Node

- search [version] - search node versions in net

```bash
uvm node search [version]
```

- list - show installed node versions

```bash
uvm node list
```

- install - install new version

```bash
uvm node install {version}
```

- remove - remove node version

```bash
uvm node remove {version}
```

- use - select version for use if version not installed - download

```bash
uvm node use {version}
```

- off - deselect current version

```bash
uvm node off
```

- path - print path to node folder

```bash
uvm node path {version}
```

- addGlobal - add a global package to all versions, for example: typescript, **you can`t install many package in one command**

```bash
uvm node addGlobal {package}
```

## Uninstall

//TODO