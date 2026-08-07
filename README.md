# Arizona Ice Finder — FINAL live-source build

Public site target:
`https://srcadieux.github.io/arizona-ice-finder/`

## What this final build does

- Tracks the statewide Arizona hockey-rink directory.
- Keeps active, seasonal, future, and discovery-watch facilities separate.
- Shows only sessions that are collected with high confidence.
- Includes filters for event type, region, rink, AM/PM, outside-work-hours, and Youth / All Ages.
- Links every listed session to an official rink/registration source.
- Provides a Rink Coverage directory so facilities without a stable public machine-readable feed are still one click away.
- Includes a GitHub Actions updater that runs every four hours.

## Automatic source policy

The site does **not** fabricate or infer rink times.

### Direct automatic source
- Mullett Arena / Mountain America Community Iceplex — public Sportified schedule.

### Best-effort automatic SportsEngine adapters
- Ice Den Scottsdale
- Ice Den Chandler
- Coyotes Community Ice Center

If SportsEngine changes markup or blocks requests, those facilities remain available by official-source link rather than publishing unverified events.

### Official-link sources
The AZ Ice locations use DaySmart calendars that are JavaScript/account-system driven. Flagstaff publishes monthly municipal PDF calendars. These are intentionally treated as direct official-source links until a stable, public, machine-readable feed is verified:
- AZ Ice Arcadia
- AZ Ice Gilbert
- AZ Ice Peoria
- Jay Lively Activity Center / Flagstaff
- Findlay Toyota Center
- Tucson Convention Center

### Future
- Fire 'n' Ice Sports Arena
- MQ Iceplex at Mosaic Quarter

## GitHub Actions

The workflow file is:
`.github/workflows/refresh.yml`

It runs every four hours and can also be triggered manually from the Actions tab.

If Finder hides the `.github` folder on a Mac, press `Command + Shift + .` to show hidden files before dragging it to GitHub.

## Safety / accuracy behavior

If the updater collects zero events because a source is down or changes layout, it leaves the existing event file untouched rather than blanking the website.
