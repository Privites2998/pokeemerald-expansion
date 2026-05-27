# Git remotes

This is a soft fork of `rh-hideout/pokeemerald-expansion` with a custom roguelike layer on top.

```
origin    https://github.com/Privites2998/pokeemerald-expansion.git   # our fork (push here)
upstream  https://github.com/rh-hideout/pokeemerald-expansion.git     # RHH (pull from here)
```

## Why fork-and-repoint

- `origin` points at our fork so `git push` works without thinking.
- `upstream` points at RHH so we can pull battle/engine fixes as they land:
  ```
  git fetch upstream
  git merge upstream/master           # or rebase if our local commits are clean
  ```
- Per RHH's attribution requirement, the README credit line stays in place:
  > Based off RHH's pokeemerald-expansion 1.15.2

## Convention

- Direct commits to `master` on `origin` are fine while the project is solo.
- If we ever want to upstream a fix to RHH, branch off `upstream/master` first so the PR diff stays clean.
