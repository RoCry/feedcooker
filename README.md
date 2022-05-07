![ci](https://github.com/RoCry/feedcooker/actions/workflows/ci.yml/badge.svg)

# feedcooker
Cook multi feeds into one using GitHub Actions.

# Setup

- Fork or create repo with this repo as a template.
- Update recipes.py (see [recipes.example.py](./recipes.example.py))
- Uncomment schedule in `.github/workflows/main.yml` if you want to run it automatically.

# Pending Features

- [ ] `.opml` files as recipe
- [ ] Metrics for inactive/dead feeds
- [ ] `async` to improve performance
- [ ] Merge items (summary for multi items)
