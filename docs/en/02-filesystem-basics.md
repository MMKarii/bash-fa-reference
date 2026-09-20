# 2. Filesystem and Basic Commands

## Location and navigation

```bash
pwd
cd /etc
cd ~
cd -
```

For operational scripts, explicit and predictable paths are safer than relying on an unknown current working directory.

## Listing and creating

```bash
ls -lah
mkdir -p workspace/logs
touch workspace/logs/app.log
```

`ls -l` shows permissions and ownership. `-a` includes hidden names and `-h` makes sizes easier to read.

## Copying and moving

```bash
cp file.txt backup.txt
cp -r src/ dst/
mv old_name new_name
```

Before a bulk change, inspect the selected files with a non-destructive command or the target tool's dry-run mode.

## Permissions and ownership

```bash
chmod u+x deploy.sh
chmod 750 private-dir
chown app:app file.txt
```

Numeric permissions combine read=4, write=2, execute=1. Apply least privilege.

## Discover command type and documentation

```bash
type cd
help cd
man ls
command -v bash
```

`type` reveals whether a name is a builtin, alias, function, or external command.
