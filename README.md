# Arizona Ice Finder — Statewide Build

This build is ready to upload to the `arizona-ice-finder` GitHub repository.

## Statewide rink coverage

The project tracks verified current hockey-ice facilities listed by Arizona hockey sources plus announced future facilities:

- AZ Ice Arcadia — Phoenix
- AZ Ice Gilbert — Gilbert
- AZ Ice Peoria — Peoria
- Coyotes Community Ice Center — Mesa
- Ice Den Chandler — Chandler
- Ice Den Scottsdale — Scottsdale
- Mullett Arena / Mountain America Community Iceplex — Tempe
- Jay Lively Activity Center — Flagstaff
- Findlay Toyota Center — Prescott Valley
- Tucson Convention Center / Tucson Arena — Tucson
- Fire 'n' Ice Sports Arena — North Phoenix — opening September 2026
- MQ Iceplex at Mosaic Quarter — Tucson — opening Spring 2027

The project also keeps a discovery watchlist for Payson/Rim Country, the future Phoenix USHL venue, Yuma, Lake Havasu/Kingman, Show Low/White Mountains and Sierra Vista.

## USHL note

USHL announced Prescott Valley and Phoenix as targeted Arizona markets for the 2027-28 West Coast expansion. Findlay Toyota Center has publicly said it was selected as the Prescott Valley home. The Phoenix arena was not identified in the USHL announcement, so the project intentionally keeps that venue as `TBD` until it is officially confirmed.

## Payson note

No permanent hockey ice facility was verified for Payson in the current Arizona hockey-rink directory. Payson is therefore a discovery watch area rather than a fake rink entry.

## What works now

- Statewide rink directory
- Region filter (Phoenix Metro / Northern Arizona / Southern Arizona)
- Rink filter showing all configured facilities, even before they have events
- Weekly calendar and list views
- Event type and AM/PM filters
- Rink coverage dialog
- Future-rink statuses
- GitHub Actions refresh scaffold

## Important

The included calendar events are demo records so the interface can be tested. Do not rely on those demo times for skating. The next phase is connecting and verifying live schedule collectors for each rink.

## GitHub upload

Upload the CONTENTS of this folder to the root of your GitHub repository. Do not upload the ZIP itself as the website content.

After the files are committed:
Settings → Pages → Deploy from a branch → `main` → `/ (root)` → Save.
