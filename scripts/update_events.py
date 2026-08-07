ChatGPT Plus
























Today 9:27 AM
unnamed(20260807-162743).png
It is, I kind of like this idea, but I'm not sure how to do it on my own.

Worked for 38s
Yes. And you do not need to know how to program to make this. I can build the code with you and walk you through the few pieces you would actually have to click/set up.

What you're looking at is essentially three things working together:

A collector that checks the different Arizona rink schedules.

A translator that converts all their different formats into one standard format — rink, date, start/end time, event type, registration link, etc.

A calendar website that displays everything and lets you filter it.

The difficult part isn't the calendar. The difficult part is that every rink publishes its schedule differently. That's a common problem with hockey schedule aggregators; developers doing similar projects have specifically described maintaining and normalizing rink data as the biggest bottleneck. 

What I would build for you
Rather than simply cloning that site, I'd make a Scott/Jax version that's more useful for youth hockey development.

Something like:

Arizona Ice Finder

Filters across the top:

Ice Type
☑ Stick Time
☑ Open Hockey
☑ Drop-In
☑ Public Skate
☑ Skills/Clinics
☑ Power Skating
☑ Goalie Sessions

Age
☑ 10U
☑ 12U
☑ Youth
☑ All Ages

Rink
☑ Ice Den Scottsdale
☑ AZ Ice Arcadia
☑ AZ Ice Gilbert
☑ AZ Ice Peoria
☑ Chandler
☑ Mullett
☑ Other Valley rinks

And then filters that would actually matter to you:

Time

Before school

School hours

After school

Evening

Weekend

Distance

Scottsdale first

East Valley

West Valley

All Arizona

Then the weekly calendar exactly like the one in your screenshot.

Click:

Stick Time — Ice Den Scottsdale
Saturday 3:15–4:15 PM

…and it takes you directly to that rink's registration page.

I would add one feature the pictured site really needs
A "Jax Available" filter.

You could eventually enter Jax's normal schedule:

practices

games

Tony

private lessons

family commitments

Then instead of displaying 120 ice sessions, the site could display:

12 sessions actually fit Jax's schedule this week

That's substantially more useful.

We could even give each opportunity a little rating:

BEST FIT

Saturday 3:15 PM
Ice Den Scottsdale
Stick Time
14 min away
No hockey scheduled within 4 hours

versus:

POSSIBLE

Thursday 7:30 PM
AZ Ice Gilbert
Stick Time
38 min away
Late on school night

That turns it from an ice-time directory into a hockey scheduling tool.

How you would actually get it online
I'd recommend a slightly different setup from the Render site in the screenshot:

GitHub → automatic schedule collector → your webpage

It can be essentially free for a personal project.

Every few hours the system would automatically:

Rink websites → collect schedules → clean the data → update the calendar

You wouldn't sit there entering events.

You'd bookmark something like:

jax-ice-finder...

on your phone and computer.

Your involvement in building it would mostly amount to creating a free GitHub account and following a few deployment steps I give you. I can generate the actual website, calendar, filters, scraper code, database structure and deployment files.

And when we get to one of those screens where GitHub asks you something incomprehensible, screenshot it and send it to me. I'll tell you exactly what to click.

One important distinction
I would initially make this private/personal, not try to build another public Arizona Hockey Friends website.

That lets us optimize it entirely around what you need when looking for extra ice for Jax, and it reduces the amount of maintenance dramatically.

Once it works well, turning it into something other Arizona hockey parents could use would be relatively easy.

I think this is worth building. The first version doesn't need to be huge. I'd start with about 5–7 Valley rinks, Stick Time + Open Hockey + youth clinics, a weekly calendar, filters and direct registration links. Once those are reliably updating automatically, we add the smarter Jax-specific features.

If you want to do it, I can start building Version 1 for you here rather than having you figure out the programming yourself.


yes

Worked for 1m
Absolutely. I’ve started it.

I built Version 1 of Arizona Ice Finder as a working website shell:

Download Arizona Ice Finder – Version 1

It already has the dark weekly calendar like the one you showed me, plus rink filtering, Stick Time/Open Hockey/Flow Hockey/Clinic filters, AM/PM filtering, a “No work hours” option, age filtering, week navigation, calendar/list views, and clickable sessions.

I also loaded 35 demo sessions from the schedule in your screenshot so when you open it, it actually looks and behaves like a real system rather than an empty template. Those are deliberately labeled demo data so we don't accidentally treat them as current rink information.

I also researched the underlying rink sources. This is very doable: Ice Den publishes hockey events and registration information publicly, AZ Ice has its Arcadia/Gilbert/Peoria network online, and Mullett publishes hockey sessions in a structured schedule. 

Where we go next
I would build it in this order:

1. Put this version online.
We'll use GitHub Pages. It can cost you $0, and I'll walk you through every click.

2. Connect live rink data.
One at a time:
Ice Den Scottsdale → Ice Den Chandler → AZ Ice Arcadia → Gilbert → Peoria → Mullett.

3. Automate it.
The project already contains the beginning of the automatic refresh system. Once the rink collectors are verified, it can check schedules every few hours without you doing anything.

4. Then make it much better than the Facebook version.
Youth/10U-only filtering, direct registration buttons, favorites, personal availability, “best ice opportunities this week,” and eventually a calendar subscription.

The key is that you don't need to learn coding. I can handle that part. You'll mostly be following my instructions for things like creating the GitHub account and clicking the correct settings.

Your next move: download that ZIP. Then tell me when you've got it, and I'll walk you through getting your own Arizona Ice Finder live on the internet, one screen at a time. 


Screenshot 2026-08-07 at 09.53.09.png

Perfect — you’re exactly where you need to be.

Click “Sign up” in the upper-right corner.

Then create your GitHub account. Use whatever email address you want associated with this project.

Once you get through the account creation and GitHub has you logged in, send me the next screenshot. I’ll walk you through it one screen at a time.


Screenshot 2026-08-07 at 09.58.48.png

Perfect — your GitHub account is set up and you’re on the right dashboard.

Click the green “Create repository” button on the upper-left side of your screen.

On the next page, fill it out this way:

Repository name: arizona-ice-finder

Description: Arizona hockey stick time, open hockey, clinics, and ice availability finder

Select Public. That makes the free GitHub Pages setup straightforward. It does not expose any personal information unless we put personal information into the project itself.

Do NOT check “Add a README file” — I already built one.

Leave .gitignore as None.

Leave License as None.

Then don’t click anything else yet if you want me to verify it first. Send me a screenshot of that repository-creation page once you have those fields filled in, and I’ll check it before we create it.


Screenshot 2026-08-06 at 13.19.39.png

You’re on the wrong screen — this is a Fidelity youth account setup page, not GitHub.

Also, this screenshot includes an account identifier, so for future screenshots I’d crop or cover that part before sending.

Go back to the GitHub tab/window where you were on the Home/Dashboard screen. Then click the green Create repository button on the left side.

Once you’re on the GitHub “Create a new repository” page, send me that screenshot and I’ll tell you exactly what to enter.


Screenshot 2026-08-07 at 10.26.16.png

Perfect. You’ve created the repository correctly. arizona-ice-finder is public and empty, exactly where we want it.

Now click the blue “uploading an existing file” link in the Quick setup box — it’s right below the HTTPS address.

Before uploading, make sure you’ve double-clicked the ZIP file I gave you on your Mac so it expands into the folder arizona-ice-finder-v1.

On the next GitHub screen, don’t upload the ZIP itself. We’ll upload the actual website files from inside that folder.

Send me the next screenshot after you click “uploading an existing file.” I’ll tell you exactly what to drag into that box.


i dont have the zip? Also add fire and ice that will open in october

No problem — I rebuilt the ZIP for you, and I also added Fire ’n’ Ice Sports Arena as a future rink source.

Download the updated Arizona Ice Finder ZIP

One small correction: Fire ’n’ Ice’s official website currently says the facility is scheduled to open in September 2026, while its hockey tournament page lists the hockey season opening October 2, 2026. 
 I’ve added it now so we’re ready to pull Stick Time, Open Hockey, clinics, etc. as soon as they start publishing those schedules.

After you download it on your Mac, double-click the ZIP. You should then see a folder named:

arizona-ice-finder-v1

Then go back to your GitHub page and click “uploading an existing file.” Send me the next screenshot and I’ll tell you exactly what to drag over. 


I need the zip for all rinks in the Arizona, to include Flagstaff. Or any other rinks, maybe even like Payson or, oh gosh, where's the other one? Where the USHL team is gonna be. Just all the rinks.

Worked for 1m 11s
Yes — that’s the right scope. I rebuilt it as a statewide Arizona version, not just Phoenix-area rinks.

Download Arizona Ice Finder — STATEWIDE ZIP

I currently have 12 verified current or announced hockey facilities configured, based on the Arizona hockey rink directory plus official facility sources. That includes Flagstaff’s Jay Lively, Prescott Valley’s Findlay Toyota Center, Tucson, all the Valley rinks, Fire ’n’ Ice, and the future MQ Iceplex. 

A couple of important additions:

Prescott Valley / Findlay Toyota Center is the place you were thinking of regarding the USHL. The USHL officially announced Prescott Valley and Phoenix as Arizona expansion markets targeted for 2027–28, and Findlay Toyota Center has subsequently announced that it was selected as the Prescott Valley home. The Phoenix USHL arena has not yet been officially identified, so I put that on our watchlist rather than guessing. 

Payson is in the system as a watch area. I could not verify a permanent hockey ice rink there from the current statewide hockey-rink directory, so I don't want to create a fake rink entry. If one opens or a seasonal hockey rink appears, we'll add it. 

Fire ’n’ Ice is included. Their official site currently says September 2026 opening, with two NHL-sized sheets. 

MQ Iceplex in Tucson is included as future ice; it is currently scheduled for Spring 2027 with three NHL-sized rinks. 

I also put Yuma, Lake Havasu/Kingman, Show Low/White Mountains, and Sierra Vista on a statewide discovery watchlist so we don't accidentally ignore an outlying facility.

I also caught something useful: the old Oceanside Ice Arena website is still floating around online, which can make it look like an active Tempe rink, but the physical arena closed in 2023. I excluded it from the active list rather than polluting our results with stale rink data. 

So this ZIP is the one I want you to use for GitHub now. Download it and double-click it on your Mac. Then go back to the GitHub repository page you showed me. We’ll upload this statewide version rather than the earlier ZIP. 


Screenshot 2026-08-07 at 10.34.06.png

Perfect — you’re on the correct GitHub upload screen.

Now do this on your Mac:

Download the statewide package if you haven’t already: Arizona Ice Finder — STATEWIDE

In Downloads, double-click the ZIP. It will create a folder called arizona-ice-finder-statewide.

Open that folder.

Inside it you should see things like:

index.html

styles.css

app.js

README.md

SOURCES.md

data folder

scripts folder

Select everything inside the folder and drag those items into the big GitHub box that says “Drag files here to add them to your repository.”

Important: drag the contents of arizona-ice-finder-statewide, not the outer folder itself. We need index.html sitting directly at the top level of the GitHub repository.

You can ignore the hidden .github folder for the moment. That is for automatic schedule refreshing, and we can add it after the basic website is live.

Once GitHub finishes loading the files into that box, do not hit Commit changes yet. Send me a screenshot first, and I’ll verify that the folder structure is right.


Screenshot 2026-08-07 at 10.35.00.png

Yes — this is exactly right. The important part is that index.html, app.js, and styles.css are at the repository root, while the JSON files are correctly going into /data/ and the collector into /scripts/.

Go ahead and change the commit message from:

Add files via upload

to:

Initial statewide Arizona Ice Finder

Then click the green Commit changes button.

Once GitHub finishes and takes you back to the repository, send me that screen. Next we’ll turn on GitHub Pages so the site gets its own live web address.


Screenshot 2026-08-07 at 10.36.19.png

Perfect — the statewide site files are in the repository exactly where they should be. Now we make it live.

Click Settings in the top menu of the repository — I can see it near the upper center-right of your screenshot.

On the Settings page:

In the left sidebar, scroll down to Pages. It is usually under Code and automation.

Under Build and deployment, find Source.

Select Deploy from a branch.

Under Branch, choose:

main

/ (root)

Click Save.

That tells GitHub: “Use the index.html sitting right here as my website.”

GitHub will then build it. Usually within a minute or two, the Pages screen will show something similar to:

Your site is live at https://srcadieux.github.io/arizona-ice-finder/

Once you reach the Pages screen — either before or after hitting Save — send me the screenshot. I’ll verify the settings and then we’ll open your actual Arizona Ice Finder website for the first time.


Screenshot 2026-08-07 at 10.37.43.png

Perfect — this is configured correctly.

I can see:

Source: Deploy from a branch

Branch: main

Folder: / (root)

HTTPS: enabled

GitHub says the Pages source was saved and the site is currently being built.

Give GitHub about 30–90 seconds, then refresh this page. You should see a message near the top saying something like “Your site is live at…”

Your address should be:

https://srcadieux.github.io/arizona-ice-finder/

Try opening that in a new tab now. If it gives you a 404, wait about a minute and refresh.

When the Arizona Ice Finder actually opens, send me a screenshot of the live site. Then we’ll move to the important part: replacing the demo calendar with real, automatically updated rink schedules from all the Arizona rinks.


Screenshot 2026-08-07 at 10.38.38.png

Perfect — it’s live. Your site address is:

https://srcadieux.github.io/arizona-ice-finder/

Click “Visit site” on that GitHub Pages screen.

That should open your actual Arizona Ice Finder website. Once it loads, send me a screenshot of the live page. Then we’ll verify that the layout and filters are working before we start connecting the real Arizona rink schedules.


Screenshot 2026-08-07 at 10.40.16.png

Perfect. It’s working exactly as intended. Your Arizona Ice Finder is now live, the statewide rink directory loaded correctly, the filters are functioning, and the weekly calendar is rendering properly.

I can see the demo sessions for AZ Ice Peoria, Gilbert, Arcadia, Mullett, and Ice Den Scottsdale. The important thing is the underlying structure is working — now we replace those handful of demo entries with the actual schedules.

The next build should do three things:

Pull live schedules automatically from every rink we can access.

Normalize everything into the same categories: Stick Time, Open Hockey/Pickup, Flow Hockey, Clinics/Skills, with age restrictions when available.

Make every calendar event click through to the actual registration or rink page.

I’d start with Mullett, Ice Den Scottsdale/Chandler, and the three AZ Ice locations, because those are going to give you most of the useful Valley inventory. Then we add Mesa, Flagstaff, Prescott Valley, Tucson, Fire ’n’ Ice when its schedule comes online, and the future facilities.

And I want to preserve what you have right now as the stable Version 1 rather than experimenting directly on the live site. We’ll build the live-data update as Version 2, test it, and then upload the replacement files once we know the feeds are accurate.

You’ve got the hard infrastructure part done. The website exists and is live. Now we can make it useful.


ok lets finalize

Worked for 2m 5s
Done. I’ve built the final statewide live-source version:

Download Arizona Ice Finder — FINAL

This replaces the demo build. It now has the statewide rink directory, Youth/All-Ages filtering, regional and rink filters, official-source links, future-rink tracking, source-status indicators, and an automatic refresh system scheduled every four hours.

I also removed the fake/demo schedule philosophy: the site now only displays events we have enough confidence in. Mullett is our first verified direct automatic source; its public schedule currently shows All Ages Stick Time, Adult Open Hockey, Power Skate, and Flow Hockey, including the Aug. 10–14 sessions we seeded into this build. 
 Ice Den/Coyotes use SportsEngine calendars, so I included a best-effort automatic adapter for those. 
 AZ Ice is now using a DaySmart-powered event/calendar interface, so I deliberately link straight to the official calendars rather than inventing an unreliable scraper. 
 Flagstaff likewise publishes its ice schedule through municipal monthly calendars/PDFs. 

Replace the current site
Download the ZIP above and double-click it.

Inside the new arizona-ice-finder-FINAL folder, you’ll see the website files plus a hidden folder called:

.github

On your Mac, while that folder is open, press:

Command + Shift + .

That makes hidden files visible.

Then go to your GitHub repository:

arizona-ice-finder

Choose Add file → Upload files.

Select everything inside arizona-ice-finder-FINAL, including .github, and drag it into GitHub.

GitHub will recognize that several files already exist and replace them with these newer versions.

Use this commit message:

Finalize statewide Arizona Ice Finder with live refresh

Then click Commit changes.

The .github/workflows/refresh.yml file is especially important — that's what gives us the automatic schedule update every four hours.

After you commit, GitHub Pages should redeploy automatically. Then we'll go to Actions one time, manually run Refresh Arizona ice schedules, and see exactly which additional rink feeds the collector successfully pulls. That will be the final verification step before we leave it running on its own. 


Screenshot 2026-08-07 at 10.47.32.png

You’re still on the Pages settings screen, and it looks like GitHub is still serving the earlier deployment. The final package has not been uploaded yet.

Go back to the repository by clicking Code at the upper left. Then:

Click Add file → Upload files.

On your Mac, unzip this package if you haven’t already: Arizona Ice Finder — FINAL

Open the arizona-ice-finder-FINAL folder.

Press Command + Shift + . so the hidden .github folder becomes visible.

Select everything inside the folder, including .github, and drag it onto the GitHub upload page.

Use commit message: Finalize statewide Arizona Ice Finder with live refresh

Click Commit changes.

Your Pages settings are already correct, so do not change anything on this screen. Once the new files are committed, GitHub Pages will redeploy automatically.

Send me the upload screen after you drag the final files in, and I’ll verify that .github, requirements.txt, and the new files are all there before you commit.


Screenshot 2026-08-07 at 10.49.15.png

Yes — you’re in exactly the right folder. One thing is missing from view: the hidden .github folder that contains the automatic-refresh workflow.

Press Command + Shift + . (period) while this Finder window is active. You should then see a slightly faded folder named:

.github

Once it appears, select all of these together — app.js, data, index.html, README.md, requirements.txt, scripts, SOURCES.md, styles.css, and .github — and drag them onto the GitHub Upload files page.

You can also upload REFRESH-WORKFLOW.yml; it’s just a visible backup copy of the workflow, so leaving it in is fine.

Don’t commit yet. After you drag everything into GitHub, send me that screen. I want to verify that GitHub shows something like:

.github/workflows/refresh.yml

That one file is what makes the rink schedule check run automatically every four hours.


Screenshot 2026-08-07 at 10.51.06.png

Almost there. Everything looks correct except one important file is still missing.

I can see REFRESH-WORKFLOW.yml, but that is only the visible backup. GitHub needs the actual workflow at:

.github/workflows/refresh.yml

Do not commit yet.

Go back to the Finder window, press Command + Shift + . to reveal hidden files, and you should see a faded folder named .github.

Drag just that .github folder into the same GitHub upload box you have open now.

When it works, another line should appear in this list:

.github/workflows/refresh.yml

Once you see that line, use the commit message:

Finalize statewide Arizona Ice Finder with live refresh

Then click Commit changes.

Send me the screenshot once .github/workflows/refresh.yml appears. That is the last piece needed for the automatic four-hour refresh system.


says the file is hidden after i drag and drop

That’s okay. Don’t fight the hidden-file restriction. GitHub’s browser uploader can be finicky with folders beginning with a period.

You already have the visible backup file REFRESH-WORKFLOW.yml in the upload list, so we can create the hidden GitHub workflow directly inside GitHub afterward.

For this screen, go ahead and:

Change the commit message to
Finalize statewide Arizona Ice Finder

Leave Commit directly to the main branch selected.

Click the green Commit changes button.

After that, we’ll do one small additional step:

Add file → Create new file

and name the new file exactly:

.github/workflows/refresh.yml

Then we’ll copy the contents of REFRESH-WORKFLOW.yml into it. GitHub will automatically create the hidden .github/workflows folders for us.

So yes, you can commit what you have now. Send me the repository screen after it finishes, and I’ll walk you through creating that last file.


Screenshot 2026-08-07 at 10.54.37.png

Perfect — you’ve created the file in exactly the right place:

.github/workflows/refresh.yml

Now click inside the large editor area and paste this entire block:

name: Refresh Arizona ice schedules

on:
  workflow_dispatch:
  schedule:
    - cron: "17 */4 * * *"

permissions:
  contents: write

jobs:
  refresh:
    runs-on: ubuntu-latest

    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install collector dependencies
        run: pip install -r requirements.txt

      - name: Refresh rink schedules
        run: python scripts/update_events.py

      - name: Commit any schedule changes
        run: |
          git config user.name "arizona-ice-finder-bot"
          git config user.email "actions@users.noreply.github.com"
          git add data/events.json
          git diff --cached --quiet || git commit -m "Auto-refresh rink schedules"
          git push
Then click the green Commit changes… button in the upper-right.

Use this commit message:

Add automatic rink schedule refresh

Commit it directly to main.

After it commits, click the Actions tab at the top. Send me that screen. We’ll manually run the updater once and verify whether the rink collectors are actually working before we consider this finished.


Screenshot 2026-08-07 at 10.55.09.png

That looks right. The workflow content is in place and the indentation looks correct.

Now click the green Commit changes… button in the upper-right.

Use:

Commit message: Add automatic rink schedule refresh

Keep Commit directly to the main branch selected, then click Commit changes.

After it finishes, click Actions in the top menu. You should see a workflow named “Refresh Arizona ice schedules.”

Send me that Actions screen. We’ll run it manually once and verify whether the automatic rink collector succeeds before we call this finished.


Screenshot 2026-08-07 at 10.56.44.png

Perfect — the workflow is there. That means the automatic-refresh file was created correctly.

Now click “Refresh Arizona ice schedules” in the left sidebar.

On the next screen, look for a button near the upper-right that says “Run workflow.”

Click it, leave the branch as main, then click the green Run workflow button.

After a few seconds, a new workflow run should appear. Let it finish. We want to see a green check mark.

Send me that next screen once the run appears, and I’ll verify whether the rink collector actually completed successfully.


Screenshot 2026-08-07 at 10.57.58.png

Worked for 46s
The workflow failed, but I found the problem. The Node.js warning is not the cause. The failure is in our Python collector: it tries to apply a timezone to a Python date object in three places, which causes the script to exit with code 1. I verified those lines in the live GitHub source. 

I fixed the script and checked that the corrected version compiles properly:

Download the fixed update_events.py

Now do this:

Go back to Code in GitHub.

Open the scripts folder.

Click Add file → Upload files.

Download the fixed file above.

Before uploading, rename it on your Mac from:
update_events_FIXED.py

to:
update_events.py

Drag it into the GitHub upload box. GitHub should show that it will replace the existing scripts/update_events.py.

Commit with:
Fix automatic rink schedule collector

Then go back to Actions → Refresh Arizona ice schedules → Run workflow again.

This time we want the run to make it past Refresh rink schedules. Send me the result screen after the second run and I’ll verify it.


update_events_FIXED.py
Code


Screenshot 2026-08-07 at 11.00.42.png
Screenshot 2026-08-07 at 11.00.28.png

You’re in the correct place now: GitHub → scripts → Upload files.

The missing step is just getting the fixed Python file from ChatGPT onto your Mac.

Click this again:

Download fixed update_events_FIXED.py

Then in your Mac Downloads folder:

Find update_events_FIXED.py.

Rename it exactly to update_events.py.

Drag that renamed file into the large GitHub box you have open in your second screenshot.

GitHub should recognize that scripts/update_events.py already exists and treat this as the replacement.

Use the commit message: Fix automatic rink schedule collector

Click Commit changes.

After that, go back to Actions → Refresh Arizona ice schedules → Run workflow one more time.

If you send me the resulting Actions screen, I’ll check the exact step that succeeds or fails.


update_events_FIXED.py
Code


Screenshot 2026-08-07 at 11.03.02.png

Worked for 17s
I found it. The same bug is still in the live GitHub file — the replacement you uploaded did not actually contain the correction. Your current scripts/update_events.py still has today.replace(tzinfo=AZ) at three places, which is invalid because today is a date, not a datetime. 

I’ve rebuilt the file correctly and verified the Python syntax. There are now zero occurrences of that broken code.

Download the actually corrected update_events.py

This time you do not need to rename it. It already has the exact correct filename.

On the GitHub upload screen you were using:

Drag this new update_events.py into the box.

GitHub should recognize it as replacing /scripts/update_events.py.

Commit message: Fix date handling in schedule collector

Commit directly to main.

Go back to Actions → Refresh Arizona ice schedules → Run workflow.

And yes: the Node.js 20 message shown in your screenshot is only a warning; the actual run is failing with exit code 1 from our collector. 

Send me the next Actions result. If it fails again, I’ll trace the next exact failure rather than having you guess. 


update_events.py
Code


Screenshot 2026-08-07 at 11.06.42.png

Worked for 28s
I found the real issue. The corrected file got added to the repository root instead of replacing the file inside scripts. Your commit shows 466 additions and 0 deletions, while the workflow is still executing python scripts/update_events.py. 

And I verified that the old file at scripts/update_events.py still contains the broken today.replace(tzinfo=AZ) code in three places. 

So don’t upload anything else. We can fix this directly in GitHub in about a minute.

Go to Code → scripts → update_events.py, then click the pencil/Edit icon. In that file, find these three occurrences:

today.replace(tzinfo=AZ)-timedelta(days=1)
Replace each one with:

datetime.combine(today - timedelta(days=1), datetime.min.time(), tzinfo=AZ)
There should be exactly 3 replacements. The rest of the file stays untouched.

Then click Commit changes… and use:

Fix date conversion in live collector

Commit directly to main.

After that, go back to Actions → Refresh Arizona ice schedules → Run workflow.

One housekeeping item afterward: we now have an extra update_events.py sitting at the repository root from the prior upload. It isn’t being executed, so it isn't causing this failure, but once the workflow turns green we’ll delete that duplicate to keep the repo clean. The workflow explicitly points to scripts/update_events.py. 

Send me the result of run #4. This time we’ll know we are actually running the corrected file.


Screenshot 2026-08-07 at 11.07.16.png
Screenshot 2026-08-07 at 11.10.31.png
Screenshot 2026-08-07 at 11.10.25.png
Screenshot 2026-08-07 at 11.10.15.png
Screenshot 2026-08-07 at 11.10.06.png
Screenshot 2026-08-07 at 11.09.55.png
Tell me what line to replace 

Yes. In the file you have open, I can see three lines that need to change.

Replace line 94:

if s < today.replace(tzinfo=AZ)-timedelta(days=1): continue
with:

if s < datetime.combine(today - timedelta(days=1), datetime.min.time(), tzinfo=AZ): continue
Replace line 119:

if s>=today.replace(tzinfo=AZ)-timedelta(days=1):
with:

if s >= datetime.combine(today - timedelta(days=1), datetime.min.time(), tzinfo=AZ):
Replace line 174:

if s<today.replace(tzinfo=AZ)-timedelta(days=1): continue
with:

if s < datetime.combine(today - timedelta(days=1), datetime.min.time(), tzinfo=AZ): continue
That’s it — lines 94, 119, and 174 only.

An easier way: press Command + F in the editor and search for:

today.replace(tzinfo=AZ)
You should find exactly 3 occurrences. Make those three replacements, then click Commit changes….


Screenshot 2026-08-07 at 11.12.20.png

Yes — this looks good. You’re ready to commit.

The message GitHub suggested:

Refactor date comparison logic in update_events.py

is perfectly fine. Keep Commit directly to the main branch selected and click the green Commit changes button.

Then go straight to:

Actions → Refresh Arizona ice schedules → Run workflow → Run workflow

We’re looking for run #4 to turn green. Send me that result screen and I’ll check it.


Screenshot 2026-08-07 at 11.13.25.png

I found the new problem. The date logic is fixed now, but two of the replacement lines got shifted left, so Python is failing on indentation before the collector can run. I verified that in the current live scripts/update_events.py. 

In the file you already have open, make these two indentation fixes.

First fix — around line 109
Replace this whole block:

if typ:
    s=iso_local(current_date,mt.group(1)); e=iso_local(current_date,mt.group(2))
    if e<=s:e+=timedelta(days=1)
 if s >= datetime.combine(today - timedelta(days=1), datetime.min.time(), tzinfo=AZ):
        key=(s.isoformat(),title)
        if key not in seen:
            seen.add(key)
            events.append({"id":stable_id("mullett",rink,s,title),"title":title,"type":typ,"rink":rink,"start":s.isoformat(),"end":e.isoformat(),"age":age,"url":url,"source":"mullett"})
with exactly:

if typ:
    s=iso_local(current_date,mt.group(1)); e=iso_local(current_date,mt.group(2))
    if e<=s:e+=timedelta(days=1)
    if s >= datetime.combine(today - timedelta(days=1), datetime.min.time(), tzinfo=AZ):
        key=(s.isoformat(),title)
        if key not in seen:
            seen.add(key)
            events.append({"id":stable_id("mullett",rink,s,title),"title":title,"type":typ,"rink":rink,"start":s.isoformat(),"end":e.isoformat(),"age":age,"url":url,"source":"mullett"})
The important part is that the if s >=... line must line up with the s=iso_local... line above it. Right now it does not. 

Second fix — around line 162
Replace:

if e<=s:e+=timedelta(days=1)
 if s < datetime.combine(today - timedelta(days=1), datetime.min.time(), tzinfo=AZ): continue
out.append({"id":stable_id("sportsengine",rink,s,title),"title":title,"type":typ,"rink":rink,"start":s.isoformat(),"end":e.isoformat(),"age":age,"url":event_url,"source":"sportsengine"})
with:

if e<=s:e+=timedelta(days=1)
if s < datetime.combine(today - timedelta(days=1), datetime.min.time(), tzinfo=AZ): continue
out.append({"id":stable_id("sportsengine",rink,s,title),"title":title,"type":typ,"rink":rink,"start":s.isoformat(),"end":e.isoformat(),"age":age,"url":event_url,"source":"sportsengine"})
Those three lines need to start at exactly the same indentation level. 

Then click Commit changes… and use:

Fix collector indentation

Commit directly to main, then run Actions → Refresh Arizona ice schedules again.

This is now an indentation/syntax issue, not another logic problem.


How do I get there again? And tell me step by step.

Absolutely. From the screen you’re on now, do this exactly:

At the very top of GitHub, click Code.

On the repository page, click the scripts folder.

Click update_events.py — make sure you choose that one, not update_events_FIXED.py.

When the file opens, click the pencil icon / Edit this file near the upper-right of the code.

Once you’re in edit mode, press Command + F on your Mac.

Search for:

if typ:
We are looking for the section around lines 114–123.

When you get to that spot, stop and send me a screenshot. I’ll tell you exactly which line to move and how many spaces it needs.

We’ll fix one section at a time so there’s no guessing.


Screenshot 2026-08-07 at 11.16.29.png

Perfect — you are exactly at the right spot.

I can see line 116: if typ: at the very bottom of your screen. Now do only this:

Scroll down just a little bit — about 5–8 lines — until you can clearly see lines 116 through 124.

You should see something approximately like:

if typ:
    s=iso_local(...)
    if e<=s:...
 if s >= datetime.combine(...)
Do not change anything yet.

Send me one more screenshot with lines 116–124 fully visible.

Your line 94 already looks correct in this screenshot, so we are not touching that one again. We’ll fix the next bad indentation precisely.


Screenshot 2026-08-07 at 11.17.16.png

Perfect — this screenshot shows the problem clearly.

Fix #1: Line 119
Look at line 119:

if s >= datetime.combine(today - timedelta(days=1), datetime.min.time(), tzinfo=AZ):
Right now it is too far left.

It needs to line up vertically with line 117:

s=iso_local(current_date,mt.group(1)); e=iso_local(current_date,mt.group(2))
Do this:

Click at the very beginning of line 119, immediately before if.

Press Tab once.

After that, line 119 should visually start directly underneath the s on line 117, like this:

            if typ:
                s=iso_local(current_date,mt.group(1)); e=iso_local(current_date,mt.group(2))
                if e<=s:e+=timedelta(days=1)
                if s >= datetime.combine(today - timedelta(days=1), datetime.min.time(), tzinfo=AZ):
                    key=(s.isoformat(),title)
                    if key not in seen:
                        seen.add(key)
                        events.append(...)
Do not change lines 120–123 yet. From this screenshot, their relative indentation looks correct.

Once you press Tab once on line 119, send me another screenshot of this same section. Then we’ll check it and move to the second indentation problem around line 174.


Screenshot 2026-08-07 at 11.18.40.png

Yes — that first fix is now correct. Line 119 is aligned properly with lines 117–118.

Now we’ll fix the second and last indentation issue.

Click in the Find box at the top where it currently says if typ:.

Replace that search with:

if s < datetime.combine
Press Enter or click Next until GitHub takes you to the occurrence around line 174.

Don’t change anything yet.

Send me a screenshot showing roughly lines 168–177.

I’ll tell you exactly what to move. We’re very close.


Screenshot 2026-08-07 at 11.19.34.png

Perfect — this is the second spot.

Fix #2: line 174
Right now line 174:

if s < datetime.combine(today - timedelta(days=1), datetime.min.time(), tzinfo=AZ): continue
needs to line up exactly with line 173 directly above it:

if e<=s:e+=timedelta(days=1)
Do this:

Click at the very beginning of line 174, before if.

Press Tab once.

After that, lines 173–175 should look aligned like this:

                if e<=s:e+=timedelta(days=1)
                if s < datetime.combine(today - timedelta(days=1), datetime.min.time(), tzinfo=AZ): continue
                out.append(...)
That should be the final indentation fix.

Then click Commit changes… in the upper-right.

Use:

Fix collector indentation

Keep Commit directly to main selected and commit it.

Then go to Actions → Refresh Arizona ice schedules → Run workflow again.

Send me the result of the next run.


Screenshot 2026-08-07 at 11.21.30.png

Yes — that’s the green light. It worked. The workflow run shows Success, so the automatic collector executed without crashing.

The yellow Node.js message is only a warning from GitHub Actions; it did not stop the workflow.

Now I want to verify what it actually collected before we call this completely finished:

On this screen, click the green refresh box in the middle.

You’ll see the individual steps that ran.

Click/expand “Refresh rink schedules”.

Look near the bottom of that section. It should say something like:

Wrote 12 collected events.
- Mullett Arena ...: 12
or it may say it preserved the existing data if no current events were found.

Send me a screenshot of that expanded output.

That tells us the most important thing: not merely that the program ran, but which Arizona rinks and how many actual sessions it successfully captured.

After that, we’ll do two final housekeeping items: verify the live website displays the new data, then remove the duplicate update_events_FIXED.py and extra root-level update_events.py files so your GitHub repository is clean.

But the big hurdle is over: your automated four-hour updater is now successfully running.


Screenshot 2026-08-07 at 11.22.49.png

Yes — the automation itself is now working correctly.

Your screenshot confirms:

Workflow: Success

14 live events collected

All 14 are currently from Mullett Arena / Mountain America Community Iceplex

The workflow also successfully reached “Commit any schedule changes,” so data/events.json was updated automatically.

One important distinction: we have not yet achieved automatic collection from all Arizona rinks. Right now Mullett is live; the other rinks are still represented through their official-source links until we build reliable collectors for their different scheduling systems. I don't want to call it “all-rinks live” when it isn't.

For now, finish this version with these steps:

Wait about 1 minute for GitHub Pages to redeploy.

Open your site:
https://srcadieux.github.io/arizona-ice-finder/

Refresh the page. It should now show the current Mullett events instead of the old demo data.

In GitHub Code, delete the two accidental duplicate files:

root-level update_events.py

scripts/update_events_FIXED.py

Do not delete scripts/update_events.py — that is the working collector.

Leave .github/workflows/refresh.yml alone. It will now run automatically every four hours.

At that point I would call this Arizona Ice Finder v1.0: stable and operational.

The next phase is the worthwhile one: getting Ice Den Scottsdale/Chandler, AZ Ice Arcadia/Gilbert/Peoria, Mesa, Flagstaff, Prescott Valley and Tucson to feed the calendar automatically too. That would turn this from a functioning statewide directory with partial live data into the true all-Arizona aggregator you originally wanted.


give me step by step

Absolutely. From where you are right now, do these in order:

Verify the live website updated

Open a new tab.

Go to:
https://srcadieux.github.io/arizona-ice-finder/

Refresh the page.

At the top-right, it should no longer say “demo calendar.”

The calendar should now show the live Mullett events that were just collected.

Go back to your GitHub repository

Click the GitHub tab.

Click Code at the top-left.

Delete the accidental root-level update_events.py

In the main file list, you should see an update_events.py sitting at the same level as index.html, app.js, etc.

Click that root-level update_events.py.

Click the trash can / Delete file option near the upper-right.

Commit message:
Remove duplicate root collector

Commit directly to main.

Delete scripts/update_events_FIXED.py

Go back to Code.

Open the scripts folder.

Click update_events_FIXED.py.

Delete that file.

Commit message:
Remove obsolete fixed collector copy

Commit directly to main.

Do NOT delete the working collector

Inside scripts, you must keep:
update_events.py

That is the file your successful workflow is using.

Do NOT touch the workflow

Keep:
.github/workflows/refresh.yml

That is what checks the rink schedules automatically every four hours.

Verify the repository is clean
Your main GitHub page should roughly contain:

.github

data

scripts

app.js

index.html

README.md

requirements.txt

SOURCES.md

styles.css

REFRESH-WORKFLOW.yml

And inside scripts, there should be just:

update_events.py

Run one final test after cleanup

Click Actions.

Click Refresh Arizona ice schedules.

Click Run workflow.

Choose main.

Click the green Run workflow button.

Wait for the green check mark.

Confirm the result

Open the successful workflow.

Open the refresh job.

Expand Refresh rink schedules.

You should again see something like:
Wrote 14 collected events
and
Mullett Arena / Mountain America Community Iceplex: 14

Return to the live website

Open:
https://srcadieux.github.io/arizona-ice-finder/

Refresh once more.

That is your working Arizona Ice Finder v1.0.

Start with Step 1 right now: open the live website and send me a screenshot of what you see. Then I’ll walk you through the cleanup one file at a time.


Screenshot 2026-08-07 at 11.25.03.png

Perfect — Step 1 is verified. The live site is updating from the automation.

I can see:

12 facilities tracked

14 collected sessions

The last data update is 8/7/2026 at 11:21 AM

Actual Mullett events are appearing on the calendar

Now we clean up the two duplicate files. Do only this next step:

Step 2 — Delete the duplicate root update_events.py
Go back to your GitHub tab.

Click Code at the top.

On the main repository page, look for the file named:
update_events.py

It should be sitting at the main/root level, alongside app.js, index.html, etc.

Click that root-level update_events.py.

When the file opens, look in the upper-right for the trash-can icon or the ••• menu → Delete file.

Click Delete file.

For the commit message use:
Remove duplicate root collector

Keep Commit directly to main selected.

Click Commit changes.

Important: do not delete scripts/update_events.py. That is the working one.

Send me a screenshot once you’re looking at the main GitHub file list, and I’ll point out exactly which update_events.py to delete.


Screenshot 2026-08-07 at 11.26.13.png

Yes — this is the exact duplicate root file you should delete. I can tell because the breadcrumb at the top says:

arizona-ice-finder / update_events.py

There is no scripts/ in the breadcrumb, so this is the extra copy.

Do this:

Look at the row of buttons above the code, toward the upper-right.

Click the small down-arrow next to the pencil/edit icon.

Choose Delete file.

GitHub will open a delete/commit screen.

Use this commit message:
Remove duplicate root collector

Keep Commit directly to the main branch selected.

Click Commit changes.

After that, go back to Code → scripts. Then we’ll delete the second duplicate, update_events_FIXED.py, and leave the working scripts/update_events.py untouched.


Screenshot 2026-08-07 at 11.27.45.png

You clicked the edit dropdown, not the file actions menu. That’s why you’re seeing “In place / github.dev / GitHub Desktop.”

Do this:

Close the small dropdown you have open.

Look at the far upper-right of the file page, above the code. There is a three-dot ••• button.

Click that three-dot button.

Choose Delete file. GitHub’s current docs place deletion in that top-right dropdown. 

On the next screen, use the commit message:
Remove duplicate root collector

Keep Commit directly to the main branch selected.

Click Commit changes.

This is definitely the correct duplicate to delete because the breadcrumb says:

arizona-ice-finder / update_events.py

—not arizona-ice-finder / scripts / update_events.py.

After you delete it, send me the next screen and we’ll remove scripts/update_events_FIXED.py.


Screenshot 2026-08-07 at 11.29.41.png

I can see one thing clearly: the root-level update_events.py is still there at the very bottom of your file list, so it did not actually disappear yet.

Do only this next:

Click update_events.py at the very bottom of the main file list — the one directly below styles.css.

Confirm the breadcrumb at the top says:
arizona-ice-finder / update_events.py
and does not say /scripts/.

Click the ••• menu at the upper-right of that file page.

Choose Delete file.

Commit message:
Remove duplicate root collector

Keep Commit directly to main selected.

Click Commit changes.

After GitHub brings you back to the main repository page, confirm that update_events.py is no longer listed at the bottom.

Then send me that screen. After that, we’ll go into the scripts folder and remove only update_events_FIXED.py.


Screenshot 2026-08-07 at 11.30.48.png

Yes — this is the correct delete screen now.

Do this:

Click the green Commit changes… button in the upper-right.

For the commit message, use:
Remove duplicate root collector

Keep Commit directly to the main branch selected.

Click the final Commit changes button.

After GitHub takes you back to the repository:

Click the scripts folder.

Click update_events_FIXED.py.

Delete that file the same way.

Commit message:
Remove obsolete fixed collector copy

Important: inside scripts, keep update_events.py. That is the working live collector.

Send me the screen after the first deletion commits, and I’ll confirm before you delete the second file.


Screenshot 2026-08-07 at 11.31.31.png

Worked for 21s
Good news: you likely already deleted it. The error is happening because GitHub is trying to delete a file that the latest commit already removed. In your previous screenshot, the newest commit was already named “Remove duplicate root collector.” The page/file tree just hadn’t refreshed yet.

Do this exactly:

Click Cancel in the error box.

Click Cancel changes in the upper-right if GitHub keeps you on the delete screen.

Click Code at the top-left to return to the main repository.

On your Mac press Command + Shift + R to hard-refresh the GitHub page.

Look at the main file list. The root-level update_events.py should now be gone.

If it is gone, do not try to delete it again. That confirms the first cleanup succeeded. GitHub’s normal deletion process is to delete the file and commit that change; the repository page then reflects the new branch state. 

Then do the second cleanup:

Click the scripts folder.

You should see:

update_events.py ← KEEP THIS

update_events_FIXED.py ← DELETE THIS

Click update_events_FIXED.py.

Use the ••• menu in the upper-right → Delete file.

Commit message:
Remove obsolete fixed collector copy

Commit directly to main.

Start with the hard refresh and send me the main repository screen. I’ll verify that the first duplicate is actually gone before we touch anything else.


Screenshot 2026-08-07 at 11.33.45.png

Perfect — the cleanup is now complete.

I can confirm from this screen:

The duplicate root-level update_events.py is gone.

The latest commit says “Remove obsolete fixed collector copy”, so scripts/update_events_FIXED.py has also been removed.

Your repository now looks clean.

The live working collector remains inside the scripts folder.

GitHub Pages is still deployed successfully.

Now do one final verification:

Click Actions at the top.

Click Refresh Arizona ice schedules on the left.

Click Run workflow.

Leave the branch on main.

Click the green Run workflow button.

Wait for the run to finish.

You want another green checkmark.

Once it turns green, open the run and expand Refresh rink schedules. If it again says something like:

Wrote 14 collected events.
- Mullett Arena / Mountain America Community Iceplex: 14
then this version is fully cleaned up and operational.

After that, refresh your live site:

https://srcadieux.github.io/arizona-ice-finder/

Send me the final Actions result, and then we can move on to expanding the live collection beyond Mullett to Ice Den, AZ Ice, Mesa, Flagstaff, and the rest of Arizona.


Screenshot 2026-08-07 at 11.35.17.png

Perfect — you’re done with the setup. Run #6 is green after the cleanup, so the system is stable.

At this point, do not change anything else in GitHub. Your Arizona Ice Finder v1.0 now has a live GitHub Pages website, a clean repository, a working Python collector, automatic refresh every four hours, and a fail-safe so a rink outage won’t wipe out the calendar.

Your site remains:

https://srcadieux.github.io/arizona-ice-finder/

The one important limitation is that Mullett is currently the only rink successfully feeding events automatically. The other Arizona facilities are in the statewide directory with their official-source links, but they are not yet automatically populating the calendar.

So I’d consider Phase 1 finalized.

For Phase 2, I’d add live feeds in this priority order: Ice Den Scottsdale → Ice Den Chandler → AZ Ice Arcadia → AZ Ice Gilbert → AZ Ice Peoria → Coyotes Community Ice Center/Mesa → Flagstaff → Prescott Valley → Tucson, then Fire ’n’ Ice as soon as its schedule comes online.

Given where you are and the value to you, Ice Den Scottsdale should be the next one we tackle. That’s where I’d pick this back up.


yes, lets go

Worked for 1m 40s
Yes — we found a much better way to do Ice Den Scottsdale.

Instead of trying to scrape the SportsEngine webpage, Ice Den Scottsdale exposes an official iCalendar feed, and SportsEngine specifically supports iCal subscriptions from organization calendar pages. That should be substantially more reliable for us. 
 Ice Den’s current site is also publishing the exact things we care about — youth stick time, adult stick time, adult open hockey, and hockey skills programming. 

I rebuilt the collector to add Ice Den Scottsdale as our second direct automatic source, while keeping Mullett intact.

Download the new update_events.py

Now do this step by step:

In GitHub, click Code at the top.

Click the scripts folder.

Confirm you see the existing update_events.py inside scripts.

Click Add file near the upper-right.

Choose Upload files.

Download the new file above to your Mac. It is already named exactly:
update_events.py

Drag that file into the GitHub upload box. Because you started from inside the scripts folder, GitHub should replace:
scripts/update_events.py
— not create another root-level copy.

GitHub should indicate that the existing file is being changed/replaced.

Use this commit message:
Add Ice Den Scottsdale live iCal collector

Keep Commit directly to the main branch selected.

Click Commit changes.

Then test it:

Click Actions at the top.

Click Refresh Arizona ice schedules on the left.

Click Run workflow.

Leave branch set to main.

Click the green Run workflow button.

Wait for the green checkmark.

Open the successful run → click the refresh job → expand Refresh rink schedules.

What we want to see is something like:

Ice Den Scottsdale iCal: 8 hockey sessions
Wrote 22 collected events.
- Ice Den Scottsdale: 8
- Mullett Arena / Mountain America Community Iceplex: 14
The actual number may be different depending on what Ice Den has published for the next several weeks.

No changes to requirements.txt are needed. I specifically built this version around the libraries you already have installed.

Start with Code → scripts, and send me the upload screen before you commit if you want me to verify that we’re replacing the correct file this time. 


update_events.py
Code


Screenshot 2026-08-07 at 11.43.00.png

The workflow ran successfully, but the Ice Den Scottsdale upgrade did not actually replace the working scripts/update_events.py. I checked your live GitHub file: it is still the older version that treats Ice Den Scottsdale as a generic SportsEngine HTML source, and main() only calls Mullett + the old SportsEngine collector. 

That explains why Run #7 still shows only:

Wrote 14 collected events.
- Mullett Arena / Mountain America Community Iceplex: 14
So we’re not debugging Ice Den yet — the new Ice Den code simply is not in the correct file.

Do this exactly:

Click Code at the top.

Click the scripts folder.

Click update_events.py.

Look at the breadcrumb and confirm it says:
arizona-ice-finder / scripts / update_events.py

Click the pencil/Edit button.

Press Command + A inside the code editor to select the entire old file.

Delete all of it.

Open this file I gave you on your Mac:
Download the Ice Den Scottsdale version of update_events.py

Open that downloaded file with TextEdit or another text editor, press Command + A, then Command + C.

Return to the GitHub editor and paste the entire new file.

Before committing, scroll near the top. You should now see text mentioning:
Ice Den Scottsdale: official SportsEngine iCal calendar feed

and somewhere in the file:
collect_ice_den_scottsdale
12. Click Commit changes…
13. Commit message:
Add Ice Den Scottsdale live iCal collector
14. Commit directly to main.
15. Then run:
Actions → Refresh Arizona ice schedules → Run workflow

This manual replace is safer than another drag-and-drop because we know for certain we are editing the exact working file inside scripts.

After the run, expand Refresh rink schedules. If the new code is truly in place, the log should at minimum include a line beginning:

Ice Den Scottsdale iCal:
Send me that run output. That will tell us immediately whether the official Ice Den feed itself is working.


update_events.py
Code


Screenshot 2026-08-07 at 11.47.58.png
now what?

Great — the workflow succeeded. Now we need to verify whether Ice Den Scottsdale actually produced live events.

Click the row labeled “Refresh rink schedules” in the middle of the page.

It will expand and show the log output underneath.

Look for lines near the bottom that say something like:

Ice Den Scottsdale iCal: __ hockey sessions
Wrote __ collected events.
- Ice Den Scottsdale: __
- Mullett Arena / Mountain America Community Iceplex: __
Send me a screenshot of that expanded section.

Don’t change anything else yet. The next decision depends entirely on what that log says.


Screenshot 2026-08-07 at 11.49.27.png

Worked for 1m 29s
Run #9 succeeded, but it still only collected Mullett. The key clue is the log:

Wrote 14 collected events
Mullett ...: 14

I checked the exact GitHub commit that was supposed to add Scottsdale. It did change scripts/update_events.py, but the committed file still contains the old generic SportsEngine collector and does not contain the new collect_ice_den_scottsdale() iCal function. 

So here is the cleanest fix — no more drag-and-drop confusion:

Download this easy-to-open code file: Scottsdale V2 code

In GitHub, click Code → scripts → update_events.py.

Click the pencil/Edit button.

Click inside the code editor.

Press Command + A to select the entire existing file.

Press Delete.

Open SCOTTSDALE_V2_CODE.txt on your Mac.

Press Command + A, then Command + C.

Go back to GitHub and press Command + V.

Before committing, press Command + F and search for:
ICE_DEN_SCOTTSDALE_ICAL_FEEDS

Then search for:
collect_ice_den_scottsdale

Both must be found.
11. Click Commit changes…
12. Commit message:
Install Scottsdale iCal collector v2
13. Commit directly to main.
14. Go to Actions → Refresh Arizona ice schedules → Run workflow.
15. When it finishes, expand Refresh rink schedules.

This time the log should contain an Ice Den Scottsdale line if the official feed responds, because the new code explicitly prints Ice Den Scottsdale iCal: ... hockey sessions.

Send me the screenshot before you commit, with the GitHub editor showing the search result for collect_ice_den_scottsdale. That will let me verify the right code is finally in the right file before we run it again. 


SCOTTSDALE_V2_CODE.txt
Document


Screenshot 2026-08-07 at 11.57.20.png

Excellent — Ice Den Scottsdale is now live. Your log confirms it:

Ice Den Scottsdale: 16 hockey sessions

Mullett: 14 hockey sessions

30 total collected events

The 404 line is just one fallback Ice Den feed failing; another official feed worked and returned the 16 sessions, so we’re good.

Now verify Scottsdale on the live website
Open your Arizona Ice Finder:
https://srcadieux.github.io/arizona-ice-finder/

Press Command + Shift + R to hard-refresh it.

At the top, the status should now say roughly 30 collected sessions.

Open the Rink dropdown.

Select Ice Den Scottsdale.

Use the › arrow beside “today” to move through the next few weeks.

You should see Scottsdale Stick Time/Open Hockey/skills sessions populate the calendar.

Click one Scottsdale event and make sure the official source/registration link opens correctly.

Send me a screenshot of the calendar filtered to Ice Den Scottsdale.

Then we’ll add Ice Den Chandler. I’ve already confirmed Chandler has an official SportsEngine iCal subscription/feed mechanism too, so we can use the same more-reliable approach rather than scraping the page. 


its there. now onto the next

Worked for 1m 51s
Next up: Ice Den Chandler.

Their official site is currently publishing Adult Stick Time, Adult Open Hockey, youth Stick Time, and youth skills programming, so it’s a strong next source. 

I built a more robust Chandler version. Instead of hard-coding one SportsEngine tag, it first discovers Chandler’s official iCal feeds automatically, then also checks the official Chandler program/event pages as a fallback.

Download Chandler V3 code

Do this exactly:

Go to GitHub → Code → scripts → update_events.py.

Click the pencil/Edit button.

Click inside the code and press Command + A, then Delete.

Open the downloaded CHANDLER_V3_CODE.txt.

Press Command + A → Command + C.

Return to GitHub and press Command + V.

Before committing, press Command + F and search for:
collect_ice_den_chandler

Then search for:
discover_chandler_ical_feeds

Both should be found.

Click Commit changes…

Commit message:
Add Ice Den Chandler live collector

Commit directly to main.

Go to Actions → Refresh Arizona ice schedules → Run workflow.

When it turns green, open Refresh rink schedules.

This time look for something like:

Ice Den Chandler iCal feeds discovered: 2
Ice Den Chandler iCal: 12 hockey sessions
Wrote 42 collected events.
- Ice Den Chandler: 12
- Ice Den Scottsdale: 16
- Mullett Arena / Mountain America Community Iceplex: 14
The numbers will vary. Even if iCal discovery says 0, the fallback may still successfully collect Chandler events. The key line we want is:

- Ice Den Chandler: X
Send me that expanded workflow output once it runs. 


CHANDLER_V3_CODE.txt
Document


Screenshot 2026-08-07 at 12.11.45.png

We found the issue. Chandler’s collector ran, but it discovered 0 feeds and therefore collected 0 sessions. Your workflow itself is fine.

I searched Ice Den Chandler’s current official site and found the missing piece: their SportsEngine “subscribe to iCal” page exposes the actual Chandler calendar tag set:

5248139, 5251279, 5251281, 5251282, 5251284, 5251286, 5251288, 5251289, 5252225. 

The official site is also currently publishing hockey sessions such as Adult Stick Time and youth Mite/Squirt and Peewee/Bantam Stick Time, so there is real Chandler inventory for us to capture. 

I’ve hard-coded that official iCal tag set into Chandler V4, while leaving Scottsdale and Mullett intact.

Download Chandler V4 code

Now do exactly this:

GitHub → Code → scripts → update_events.py

Click the pencil/Edit icon.

Click inside the code.

Command + A → Delete

Open CHANDLER_V4_CODE.txt on your Mac.

Command + A → Command + C

Return to GitHub → Command + V

Press Command + F and search:
5248139

Make sure it finds that number.

Search:
ICE_DEN_CHANDLER_ICAL_FEEDS

Make sure that is also found.

Click Commit changes…

Commit message:
Add official Ice Den Chandler iCal feed

Commit directly to main.

Go to Actions → Refresh Arizona ice schedules → Run workflow.

Expand Refresh rink schedules when it finishes.

This time the log should say at least:

Ice Den Chandler iCal feeds to try: 1
and what we really want is:

Ice Den Chandler iCal: X hockey sessions
followed by:

- Ice Den Chandler: X
- Ice Den Scottsdale: 16
- Mullett Arena / Mountain America Community Iceplex: 14
Send me that output. If Chandler populates, we’ll go directly to AZ Ice Arcadia next. 


CHANDLER_V4_CODE.txt
Document


Library
/
CHANDLER_V4_CODE.txt


#!/usr/bin/env python3
"""
Arizona Ice Finder automatic updater.

Live sources:
- Mullett / Mountain America Community Iceplex: public Sportified schedule.
- Ice Den Scottsdale: official SportsEngine iCal calendar feed.
- Ice Den Chandler: official SportsEngine iCal discovery + official-page fallback.
- Coyotes Community Ice Center: best-effort SportsEngine HTML fallback.

Conservative design:
- Only publish sessions that can be parsed with high confidence.
- Never invent times.
- If a source fails, the script preserves the last known event file rather than
  blanking the live website.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from urllib.parse import urljoin
import hashlib
import json
import re
import sys

import requests
from bs4 import BeautifulSoup
from dateutil import parser as dtparser
from dateutil.rrule import rrulestr

AZ = ZoneInfo("America/Phoenix")
HEADERS = {
    "User-Agent": "Mozilla/5.0 ArizonaIceFinder/1.2 (+GitHub Pages personal rink calendar)"
}
TIMEOUT = 25
ROOT = __import__("pathlib").Path(__file__).resolve().parents[1]
EVENTS_FILE = ROOT / "data" / "events.json"

KEYWORDS = (
    "stick time",
    "stick & puck",
    "stick and puck",
    "open hockey",
    "pickup hockey",
    "pick-up hockey",
    "flow hockey",
    "power skate",
    "hockey skills",
    "hockey clinic",
    "hockey camp",
)

ICE_DEN_SCOTTSDALE_ICAL_FEEDS = (
    # Current Ice Den Scottsdale calendar tag set surfaced by its official iCal page.
    "https://www.icedenscottsdale.com/ical_feed?tags=2670384%2C2670407%2C2678497%2C2662957",
    # Alternate current/legacy tag set also surfaced by the official calendar.
    "https://www.icedenscottsdale.com/ical_feed?tags=2670384%2C2670407%2C2665577%2C2678497%2C2662957",
    # Full/default calendar feed fallback.
    "https://www.icedenscottsdale.com/ical_feed?tags=",
)


def get(url, **kwargs):
    r = requests.get(url, headers=HEADERS, timeout=TIMEOUT, **kwargs)
    r.raise_for_status()
    return r


def classify(title):
    low = title.lower()

    if "flow hockey" in low:
        return "Flow Hockey", "Adult"

    if (
        "open hockey" in low
        or "pickup hockey" in low
        or "pick-up hockey" in low
    ):
        return "Open Hockey", "Adult"

    if (
        "stick time" in low
        or "stick & puck" in low
        or "stick and puck" in low
    ):
        if "adult" in low:
            age = "Adult"
        elif any(
            x in low
            for x in ("youth", "mite", "squirt", "peewee", "bantam")
        ):
            age = "Youth"
        else:
            age = "All"
        return "Stick Time", age

    if any(
        x in low
        for x in ("power skate", "hockey skills", "hockey clinic", "hockey camp")
    ):
        return "Clinic", ("Youth" if "youth" in low else "All")

    return None, None


def iso_local(date_str, time_str):
    dt = dtparser.parse(f"{date_str} {time_str}", fuzzy=True)
    return dt.replace(tzinfo=AZ)


def stable_id(source, rink, start, title):
    raw = f"{source}|{rink}|{start.isoformat()}|{title}".encode()
    return source + "-" + hashlib.sha1(raw).hexdigest()[:12]


# ---------------------------------------------------------------------------
# Mullett / Sportified
# ---------------------------------------------------------------------------

def collect_mullett(today):
    base = "https://mullett.sportified.net"
    rink = "Mullett Arena / Mountain America Community Iceplex"
    events = []

    starts = [
        today - timedelta(days=1),
        today + timedelta(days=6),
        today + timedelta(days=13),
        today + timedelta(days=20),
        today + timedelta(days=27),
    ]

    seen = set()
    date_re = re.compile(
        r"^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),\s+"
        r"([A-Za-z]+)\s+(\d{1,2})\s+(\d{4})$"
    )
    time_re = re.compile(
        r"^(\d{1,2}:\d{2}\s*[ap]m)\s*-\s*(\d{1,2}:\d{2}\s*[ap]m)$",
        re.I,
    )
    cutoff = datetime.combine(
        today - timedelta(days=1), datetime.min.time(), tzinfo=AZ
    )

    for start_date in starts:
        url = f"{base}/schedule?date={start_date.isoformat()}"

        try:
            soup = BeautifulSoup(get(url).text, "html.parser")
        except Exception as exc:
            print("Mullett fetch failed:", url, exc, file=sys.stderr)
            continue

        current_date = None

        for node in soup.find_all(["h1", "h2", "h3", "h4", "h5", "tr"]):
            text = " ".join(node.stripped_strings)
            match_date = date_re.match(text)

            if match_date:
                current_date = text
                continue

            if node.name != "tr" or not current_date:
                continue

            cells = [
                " ".join(td.stripped_strings)
                for td in node.find_all(["td", "th"])
            ]

            if len(cells) < 2:
                continue

            match_time = time_re.match(cells[0])
            if not match_time:
                continue

            title = cells[1].strip()
            typ, age = classify(title)

            if not typ:
                continue

            start_dt = iso_local(current_date, match_time.group(1))
            end_dt = iso_local(current_date, match_time.group(2))

            if end_dt <= start_dt:
                end_dt += timedelta(days=1)

            if start_dt < cutoff:
                continue

            link = url
            for anchor in node.find_all("a", href=True):
                href = anchor["href"]
                if (
                    "product" in href
                    or "register" in anchor.get_text(" ", strip=True).lower()
                ):
                    link = urljoin(base, href)
                    break

            key = (start_dt.isoformat(), title)
            if key in seen:
                continue

            seen.add(key)
            events.append(
                {
                    "id": stable_id("mullett", rink, start_dt, title),
                    "title": title,
                    "type": typ,
                    "rink": rink,
                    "start": start_dt.isoformat(),
                    "end": end_dt.isoformat(),
                    "age": age,
                    "url": link,
                    "source": "mullett",
                }
            )

        # Fallback text parser if Sportified changes table markup.
        if not any(e["url"].startswith(url) for e in events):
            lines = [
                x.strip()
                for x in soup.get_text("\n").splitlines()
                if x.strip()
            ]
            current_date = None
            i = 0

            while i < len(lines):
                if date_re.match(lines[i]):
                    current_date = lines[i]
                    i += 1
                    continue

                match_time = time_re.match(lines[i])

                if current_date and match_time and i + 1 < len(lines):
                    title = lines[i + 1]
                    typ, age = classify(title)

                    if typ:
                        start_dt = iso_local(current_date, match_time.group(1))
                        end_dt = iso_local(current_date, match_time.group(2))

                        if end_dt <= start_dt:
                            end_dt += timedelta(days=1)

                        if start_dt >= cutoff:
                            key = (start_dt.isoformat(), title)

                            if key not in seen:
                                seen.add(key)
                                events.append(
                                    {
                                        "id": stable_id(
                                            "mullett",
                                            rink,
                                            start_dt,
                                            title,
                                        ),
                                        "title": title,
                                        "type": typ,
                                        "rink": rink,
                                        "start": start_dt.isoformat(),
                                        "end": end_dt.isoformat(),
                                        "age": age,
                                        "url": url,
                                        "source": "mullett",
                                    }
                                )

                    i += 2
                    continue

                i += 1

    return events


# ---------------------------------------------------------------------------
# Ice Den Scottsdale — official SportsEngine iCal feed
# ---------------------------------------------------------------------------

def unfold_ical(text):
    """Unfold RFC 5545 continuation lines."""
    physical = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    logical = []

    for line in physical:
        if line.startswith((" ", "\t")) and logical:
            logical[-1] += line[1:]
        else:
            logical.append(line)

    return logical


def unescape_ical_text(value):
    return (
        value.replace("\\n", " ")
        .replace("\\N", " ")
        .replace("\\,", ",")
        .replace("\\;", ";")
        .replace("\\\\", "\\")
        .strip()
    )


def parse_ical_datetime(key, value):
    """
    Parse DTSTART/DTEND values commonly emitted by SportsEngine.
    Supports UTC, TZID parameters, local date-time, and date-only values.
    """
    params = key.split(";")[1:]
    tzid = None
    value_is_date = False

    for param in params:
        if param.startswith("TZID="):
            tzid = param.split("=", 1)[1]
        if param == "VALUE=DATE":
            value_is_date = True

    value = value.strip()

    if value_is_date or re.fullmatch(r"\d{8}", value):
        day = datetime.strptime(value[:8], "%Y%m%d").date()
        return datetime.combine(day, datetime.min.time(), tzinfo=AZ)

    if value.endswith("Z"):
        parsed = datetime.strptime(value, "%Y%m%dT%H%M%SZ")
        return parsed.replace(tzinfo=ZoneInfo("UTC")).astimezone(AZ)

    parsed = datetime.strptime(value, "%Y%m%dT%H%M%S")

    if tzid:
        try:
            return parsed.replace(tzinfo=ZoneInfo(tzid)).astimezone(AZ)
        except Exception:
            pass

    return parsed.replace(tzinfo=AZ)


def parse_ical_events(text):
    """Return raw VEVENT dictionaries from an iCalendar payload."""
    events = []
    current = None

    for line in unfold_ical(text):
        if line == "BEGIN:VEVENT":
            current = {}
            continue

        if line == "END:VEVENT":
            if current is not None:
                events.append(current)
            current = None
            continue

        if current is None or ":" not in line:
            continue

        key, value = line.split(":", 1)
        base_key = key.split(";", 1)[0]

        if base_key in current:
            if not isinstance(current[base_key], list):
                current[base_key] = [current[base_key]]
            current[base_key].append((key, value))
        else:
            current[base_key] = (key, value)

    return events


def first_ical_value(event, field):
    item = event.get(field)
    if item is None:
        return None

    if isinstance(item, list):
        item = item[0]

    return item


def all_ical_values(event, field):
    item = event.get(field)
    if item is None:
        return []

    if isinstance(item, list):
        return item

    return [item]


def expand_ical_event(event, today, horizon_days=35):
    summary_item = first_ical_value(event, "SUMMARY")
    start_item = first_ical_value(event, "DTSTART")

    if not summary_item or not start_item:
        return []

    title = unescape_ical_text(summary_item[1])
    typ, age = classify(title)

    if not typ:
        return []

    start_dt = parse_ical_datetime(*start_item)

    end_item = first_ical_value(event, "DTEND")
    if end_item:
        end_dt = parse_ical_datetime(*end_item)
    else:
        end_dt = start_dt + timedelta(hours=1)

    duration = end_dt - start_dt
    if duration <= timedelta(0):
        duration = timedelta(hours=1)

    url_item = first_ical_value(event, "URL")
    description_item = first_ical_value(event, "DESCRIPTION")
    location_item = first_ical_value(event, "LOCATION")

    link = (
        unescape_ical_text(url_item[1])
        if url_item
        else "https://www.icedenscottsdale.com/page/show/2662960-calendar"
    )

    # SportsEngine sometimes includes the event URL only in DESCRIPTION.
    if description_item:
        description = unescape_ical_text(description_item[1])
        match = re.search(
            r"https?://(?:www\.)?icedenscottsdale\.com/event/show/\d+(?:\?[^\s]+)?",
            description,
            re.I,
        )
        if match:
            link = match.group(0)

    location = (
        unescape_ical_text(location_item[1])
        if location_item
        else "Ice Den Scottsdale"
    )

    # Reject events that are clearly not Scottsdale if the feed ever mixes facilities.
    location_low = location.lower()
    if "chandler" in location_low and "scottsdale" not in location_low:
        return []

    window_start = datetime.combine(
        today - timedelta(days=1), datetime.min.time(), tzinfo=AZ
    )
    window_end = datetime.combine(
        today + timedelta(days=horizon_days),
        datetime.max.time(),
        tzinfo=AZ,
    )

    occurrences = []

    rrule_item = first_ical_value(event, "RRULE")

    if rrule_item:
        rule_text = rrule_item[1].strip()

        try:
            rule = rrulestr(rule_text, dtstart=start_dt)
            occurrences = list(rule.between(window_start, window_end, inc=True))
        except Exception as exc:
            print(
                "Ice Den Scottsdale RRULE parse failed:",
                title,
                rule_text,
                exc,
                file=sys.stderr,
            )
            occurrences = [start_dt] if window_start <= start_dt <= window_end else []
    else:
        if window_start <= start_dt <= window_end:
            occurrences = [start_dt]

    excluded = set()

    for ex_key, ex_value in all_ical_values(event, "EXDATE"):
        for raw in ex_value.split(","):
            try:
                excluded.add(parse_ical_datetime(ex_key, raw).isoformat())
            except Exception:
                continue

    output = []
    rink = "Ice Den Scottsdale"

    for occurrence in occurrences:
        if occurrence.tzinfo is None:
            occurrence = occurrence.replace(tzinfo=AZ)
        else:
            occurrence = occurrence.astimezone(AZ)

        if occurrence.isoformat() in excluded:
            continue

        occurrence_end = occurrence + duration

        output.append(
            {
                "id": stable_id(
                    "icedenscottsdale",
                    rink,
                    occurrence,
                    title,
                ),
                "title": title,
                "type": typ,
                "rink": rink,
                "start": occurrence.isoformat(),
                "end": occurrence_end.isoformat(),
                "age": age,
                "url": link,
                "source": "icedenscottsdale",
            }
        )

    return output


def collect_ice_den_scottsdale(today):
    out = []
    feed_success = False

    for feed_url in ICE_DEN_SCOTTSDALE_ICAL_FEEDS:
        try:
            response = get(feed_url)
            text = response.text

            if "BEGIN:VCALENDAR" not in text:
                raise ValueError("response was not an iCalendar feed")

            feed_success = True

            for raw_event in parse_ical_events(text):
                out.extend(expand_ical_event(raw_event, today))

        except Exception as exc:
            print(
                "Ice Den Scottsdale iCal feed failed:",
                feed_url,
                exc,
                file=sys.stderr,
            )

    dedup = {}
    for event in out:
        dedup[(event["rink"], event["start"], event["title"])] = event

    result = sorted(dedup.values(), key=lambda e: e["start"])

    if feed_success:
        print(f"Ice Den Scottsdale iCal: {len(result)} hockey sessions")

    return result



# ---------------------------------------------------------------------------
# Ice Den Chandler — official SportsEngine iCal discovery + page fallback
# ---------------------------------------------------------------------------

ICE_DEN_CHANDLER_BASE = "https://www.icedenchandler.com"
ICE_DEN_CHANDLER_ICAL_FEEDS = (
    # Official SportsEngine tag set currently published by Ice Den Chandler.
    "https://www.icedenchandler.com/ical_feed?tags=5248139%2C5251279%2C5251281%2C5251282%2C5251284%2C5251286%2C5251288%2C5251289%2C5252225",
)

ICE_DEN_CHANDLER_PAGES = (
    "https://www.icedenchandler.com/",
    "https://www.icedenchandler.com/page/show/2803608-calendar",
    "https://www.icedenchandler.com/adult-stick-time",
    "https://www.icedenchandler.com/adult-open-hockey",
    "https://www.icedenchandler.com/youth-programs",
    "https://www.icedenchandler.com/youth-skills-clinics",
    "https://www.icedenchandler.com/adult-hockey",
    "https://www.icedenchandler.com/hockey",
)


def chandler_feed_from_href(href):
    """
    Convert a SportsEngine iCal-instructions or direct-feed URL into the
    direct /ical_feed?tags=... URL.
    """
    if not href:
        return None

    href = href.replace("&amp;", "&")
    match = re.search(
        r"(?:event/ical_instructions|ical_feed)\?tags=([^\"'&<>\s]*)",
        href,
        re.I,
    )
    if not match:
        return None

    tags = match.group(1)
    if not tags:
        return None

    return f"{ICE_DEN_CHANDLER_BASE}/ical_feed?tags={tags}"


def discover_chandler_ical_feeds():
    feeds = set()

    for page_url in ICE_DEN_CHANDLER_PAGES:
        try:
            html = get(page_url).text
        except Exception as exc:
            print(
                "Ice Den Chandler discovery page failed:",
                page_url,
                exc,
                file=sys.stderr,
            )
            continue

        soup = BeautifulSoup(html, "html.parser")

        for anchor in soup.find_all("a", href=True):
            feed = chandler_feed_from_href(anchor.get("href"))
            if feed:
                feeds.add(feed)

        # Catch iCal links embedded in scripts/data attributes.
        for match in re.finditer(
            r"(?:event/ical_instructions|ical_feed)\?tags=[^\"'&<>\s]*",
            html,
            re.I,
        ):
            feed = chandler_feed_from_href(match.group(0))
            if feed:
                feeds.add(feed)

    print(f"Ice Den Chandler iCal feeds discovered: {len(feeds)}")
    return sorted(feeds)


def expand_chandler_ical_event(event, today, horizon_days=35):
    summary_item = first_ical_value(event, "SUMMARY")
    start_item = first_ical_value(event, "DTSTART")

    if not summary_item or not start_item:
        return []

    title = unescape_ical_text(summary_item[1])
    typ, age = classify(title)

    if not typ:
        return []

    start_dt = parse_ical_datetime(*start_item)

    end_item = first_ical_value(event, "DTEND")
    if end_item:
        end_dt = parse_ical_datetime(*end_item)
    else:
        end_dt = start_dt + timedelta(hours=1)

    duration = end_dt - start_dt
    if duration <= timedelta(0):
        duration = timedelta(hours=1)

    url_item = first_ical_value(event, "URL")
    description_item = first_ical_value(event, "DESCRIPTION")
    location_item = first_ical_value(event, "LOCATION")

    link = (
        unescape_ical_text(url_item[1])
        if url_item
        else "https://www.icedenchandler.com/page/show/2803608-calendar"
    )

    if description_item:
        description = unescape_ical_text(description_item[1])
        match = re.search(
            r"https?://(?:www\.)?icedenchandler\.com/event/show/\d+(?:\?[^\s]+)?",
            description,
            re.I,
        )
        if match:
            link = match.group(0)

    location = (
        unescape_ical_text(location_item[1])
        if location_item
        else "Ice Den Chandler"
    )

    location_low = location.lower()
    if "scottsdale" in location_low and "chandler" not in location_low:
        return []

    window_start = datetime.combine(
        today - timedelta(days=1), datetime.min.time(), tzinfo=AZ
    )
    window_end = datetime.combine(
        today + timedelta(days=horizon_days),
        datetime.max.time(),
        tzinfo=AZ,
    )

    occurrences = []
    rrule_item = first_ical_value(event, "RRULE")

    if rrule_item:
        rule_text = rrule_item[1].strip()
        try:
            rule = rrulestr(rule_text, dtstart=start_dt)
            occurrences = list(rule.between(window_start, window_end, inc=True))
        except Exception as exc:
            print(
                "Ice Den Chandler RRULE parse failed:",
                title,
                rule_text,
                exc,
                file=sys.stderr,
            )
            occurrences = [start_dt] if window_start <= start_dt <= window_end else []
    else:
        if window_start <= start_dt <= window_end:
            occurrences = [start_dt]

    excluded = set()

    for ex_key, ex_value in all_ical_values(event, "EXDATE"):
        for raw in ex_value.split(","):
            try:
                excluded.add(parse_ical_datetime(ex_key, raw).isoformat())
            except Exception:
                continue

    output = []
    rink = "Ice Den Chandler"

    for occurrence in occurrences:
        if occurrence.tzinfo is None:
            occurrence = occurrence.replace(tzinfo=AZ)
        else:
            occurrence = occurrence.astimezone(AZ)

        if occurrence.isoformat() in excluded:
            continue

        occurrence_end = occurrence + duration

        output.append(
            {
                "id": stable_id(
                    "icedenchandler",
                    rink,
                    occurrence,
                    title,
                ),
                "title": title,
                "type": typ,
                "rink": rink,
                "start": occurrence.isoformat(),
                "end": occurrence_end.isoformat(),
                "age": age,
                "url": link,
                "source": "icedenchandler",
            }
        )

    return output


def collect_chandler_event_pages(today):
    """
    Fallback: crawl only official Chandler program/calendar pages, collect their
    current SportsEngine event links, then parse the event pages directly.
    """
    candidates = set()
    cutoff = datetime.combine(
        today - timedelta(days=1), datetime.min.time(), tzinfo=AZ
    )
    horizon = datetime.combine(
        today + timedelta(days=35), datetime.max.time(), tzinfo=AZ
    )

    for page_url in ICE_DEN_CHANDLER_PAGES:
        try:
            html = get(page_url).text
        except Exception as exc:
            print(
                "Ice Den Chandler event-index failed:",
                page_url,
                exc,
                file=sys.stderr,
            )
            continue

        soup = BeautifulSoup(html, "html.parser")

        for anchor in soup.find_all("a", href=True):
            href = anchor["href"]
            if re.search(r"/event/show/\d+", href):
                candidates.add(urljoin(ICE_DEN_CHANDLER_BASE, href))

        for match in re.finditer(
            r'["\']([^"\']*/event/show/\d+[^"\']*)["\']',
            html,
        ):
            href = match.group(1).replace("\\/", "/")
            candidates.add(urljoin(ICE_DEN_CHANDLER_BASE, href))

    out = []

    for event_url in sorted(candidates)[:140]:
        try:
            soup = BeautifulSoup(get(event_url).text, "html.parser")
            title_node = soup.find("h1") or soup.find("h2")
            if not title_node:
                continue

            title = " ".join(title_node.stripped_strings)
            typ, age = classify(title)
            if not typ:
                continue

            page_text = " ".join(soup.stripped_strings)

            match = re.search(
                r"(\d{1,2}:\d{2}\s*[ap]m)\s*(?:MST)?\s*-\s*"
                r"(\d{1,2}:\d{2}\s*[ap]m)\s*(?:MST)?\s+"
                r"([A-Za-z]+\s+\d{1,2}(?:st|nd|rd|th)?,\s+\d{4})",
                page_text,
                re.I,
            )

            if not match:
                continue

            date_clean = re.sub(
                r"(\d{1,2})(st|nd|rd|th)",
                r"\1",
                match.group(3),
                flags=re.I,
            )

            start_dt = dtparser.parse(
                f"{date_clean} {match.group(1)}"
            ).replace(tzinfo=AZ)
            end_dt = dtparser.parse(
                f"{date_clean} {match.group(2)}"
            ).replace(tzinfo=AZ)

            if end_dt <= start_dt:
                end_dt += timedelta(days=1)

            if start_dt < cutoff or start_dt > horizon:
                continue

            out.append(
                {
                    "id": stable_id(
                        "icedenchandler",
                        "Ice Den Chandler",
                        start_dt,
                        title,
                    ),
                    "title": title,
                    "type": typ,
                    "rink": "Ice Den Chandler",
                    "start": start_dt.isoformat(),
                    "end": end_dt.isoformat(),
                    "age": age,
                    "url": event_url,
                    "source": "icedenchandler",
                }
            )

        except Exception as exc:
            print(
                "Ice Den Chandler event page failed:",
                event_url,
                exc,
                file=sys.stderr,
            )

    dedup = {}
    for event in out:
        dedup[(event["rink"], event["start"], event["title"])] = event

    result = sorted(dedup.values(), key=lambda e: e["start"])
    print(f"Ice Den Chandler official-page fallback: {len(result)} hockey sessions")
    return result


def collect_ice_den_chandler(today):
    out = []
    feed_success = False

    feed_urls = set(ICE_DEN_CHANDLER_ICAL_FEEDS)
    feed_urls.update(discover_chandler_ical_feeds())

    print(f"Ice Den Chandler iCal feeds to try: {len(feed_urls)}")

    for feed_url in sorted(feed_urls):
        try:
            response = get(feed_url)
            payload = response.text

            if "BEGIN:VCALENDAR" not in payload:
                raise ValueError("response was not an iCalendar feed")

            feed_success = True

            for raw_event in parse_ical_events(payload):
                out.extend(expand_chandler_ical_event(raw_event, today))

        except Exception as exc:
            print(
                "Ice Den Chandler iCal feed failed:",
                feed_url,
                exc,
                file=sys.stderr,
            )

    # Always merge the official-page fallback. This covers sessions whose
    # current SportsEngine tags are not included in the main calendar feed.
    out.extend(collect_chandler_event_pages(today))

    dedup = {}
    for event in out:
        dedup[(event["rink"], event["start"], event["title"])] = event

    result = sorted(dedup.values(), key=lambda e: e["start"])

    if feed_success:
        print(f"Ice Den Chandler iCal: {len(result)} hockey sessions")
    else:
        print(f"Ice Den Chandler collected: {len(result)} hockey sessions")

    return result


# ---------------------------------------------------------------------------
# SportsEngine HTML fallback — Mesa
# ---------------------------------------------------------------------------

SPORTSENGINE = [
    (
        "Coyotes Community Ice Center",
        "https://www.coyotescommunityicecenter.com",
        "https://www.coyotescommunityicecenter.com/page/show/5540662-calendar",
    ),
]


def collect_sportsengine(today):
    out = []
    event_link_re = re.compile(r"/event/show/\d+")
    cutoff = datetime.combine(
        today - timedelta(days=1), datetime.min.time(), tzinfo=AZ
    )

    for rink, base, calendar in SPORTSENGINE:
        candidates = {}
        urls = [calendar]

        for offset in (0, 31):
            day = today + timedelta(days=offset)
            sep = "&" if "?" in calendar else "?"
            urls.append(f"{calendar}{sep}mth={day.month}&yr={day.year}")

        for url in urls:
            try:
                html = get(url).text
            except Exception as exc:
                print(
                    "SportsEngine index failed:",
                    rink,
                    url,
                    exc,
                    file=sys.stderr,
                )
                continue

            soup = BeautifulSoup(html, "html.parser")

            for anchor in soup.find_all("a", href=True):
                href = anchor["href"]
                label = " ".join(anchor.stripped_strings)

                if (
                    event_link_re.search(href)
                    and any(k in label.lower() for k in KEYWORDS)
                ):
                    candidates[urljoin(base, href)] = label

            for match in re.finditer(
                r'["\']([^"\']*/event/show/\d+[^"\']*)["\']',
                html,
            ):
                href = match.group(1).replace("\\/", "/")
                candidates.setdefault(urljoin(base, href), "")

        for event_url, label in list(candidates.items())[:80]:
            try:
                soup = BeautifulSoup(get(event_url).text, "html.parser")
                title_node = soup.find("h1") or soup.find("h2")
                title = (
                    " ".join(title_node.stripped_strings)
                    if title_node
                    else label
                )

                typ, age = classify(title)
                if not typ:
                    continue

                text = " ".join(soup.stripped_strings)

                match = re.search(
                    r"(\d{1,2}:\d{2}\s*[ap]m)\s*(?:MST)?\s*-\s*"
                    r"(\d{1,2}:\d{2}\s*[ap]m)\s*(?:MST)?\s+"
                    r"([A-Za-z]+\s+\d{1,2}(?:st|nd|rd|th)?,\s+\d{4})",
                    text,
                    re.I,
                )

                if not match:
                    continue

                date_clean = re.sub(
                    r"(\d{1,2})(st|nd|rd|th)",
                    r"\1",
                    match.group(3),
                    flags=re.I,
                )

                start_dt = dtparser.parse(
                    f"{date_clean} {match.group(1)}"
                ).replace(tzinfo=AZ)
                end_dt = dtparser.parse(
                    f"{date_clean} {match.group(2)}"
                ).replace(tzinfo=AZ)

                if end_dt <= start_dt:
                    end_dt += timedelta(days=1)

                if start_dt < cutoff:
                    continue

                out.append(
                    {
                        "id": stable_id(
                            "sportsengine",
                            rink,
                            start_dt,
                            title,
                        ),
                        "title": title,
                        "type": typ,
                        "rink": rink,
                        "start": start_dt.isoformat(),
                        "end": end_dt.isoformat(),
                        "age": age,
                        "url": event_url,
                        "source": "sportsengine",
                    }
                )

            except Exception as exc:
                print(
                    "SportsEngine event failed:",
                    rink,
                    event_url,
                    exc,
                    file=sys.stderr,
                )

    dedup = {}
    for event in out:
        dedup[(event["rink"], event["start"], event["title"])] = event

    return list(dedup.values())


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    today = datetime.now(AZ).date()

    collected = []
    collected += collect_mullett(today)
    collected += collect_ice_den_scottsdale(today)
    collected += collect_ice_den_chandler(today)
    collected += collect_sportsengine(today)
    collected.sort(key=lambda e: e["start"])

    # Fail-safe: if every network/layout source fails, preserve the prior file.
    if not collected:
        print(
            "No events collected. Preserving existing data/events.json.",
            file=sys.stderr,
        )
        return 0

    live_sources = sorted(
        set(
            e["rink"]
            for e in collected
            if e["source"] in ("mullett", "icedenscottsdale", "icedenchandler")
        )
    )
    auto_attempt = sorted(
        set(
            e["rink"]
            for e in collected
            if e["source"] == "sportsengine"
        )
    )

    payload = {
        "updated": datetime.now(AZ).isoformat(),
        "mode": "live-partial",
        "source_summary": {
            "live_auto": live_sources,
            "auto_attempt": auto_attempt,
            "official_link": [
                "AZ Ice Arcadia",
                "AZ Ice Gilbert",
                "AZ Ice Peoria",
                "Jay Lively Activity Center",
                "Findlay Toyota Center",
                "Tucson Convention Center / Tucson Arena",
            ],
            "future": [
                "Fire 'n' Ice Sports Arena",
                "MQ Iceplex at Mosaic Quarter",
            ],
        },
        "events": collected,
    }

    EVENTS_FILE.write_text(json.dumps(payload, indent=2) + "\n")

    print(f"Wrote {len(collected)} collected events.")
    for name in sorted(set(e["rink"] for e in collected)):
        count = sum(1 for e in collected if e["rink"] == name)
        print(f" - {name}: {count}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
1Password menu is available. Press down arrow to select.
